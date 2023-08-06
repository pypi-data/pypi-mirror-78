# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import print_function

import os
import platform
import sys

from contrast import __version__
from contrast.agent import patch_controller, service_client, scope
from contrast.agent.policy.loader import Policy
from contrast.agent.assess.policy.trigger_policy import TriggerPolicy
from contrast.agent.assess.preflight import update_preflight_hashes
from contrast.agent.assess.rules.providers.enable import enable_providers
from contrast.agent.middlewares.route_coverage.routes_mixin import RoutesMixin
from contrast.agent.settings_state import SettingsState
from contrast.agent.speedracer_input_analysis import get_input_analysis
from contrast.api.dtm_pb2 import AttackResult
from contrast.utils.decorators import cached_property
from contrast.utils.exceptions.contrast_service_exception import (
    ContrastServiceException,
)
from contrast.utils.exceptions.disable_agent_exception import DisableAgentException
from contrast.utils.exceptions.security_exception import SecurityException
from contrast.utils.library_reader import LibraryReader
from contrast.utils.loggers.logger import setup_agent_logger, setup_basic_agent_logger

# initialize a basic logger until config is parsed
logger = setup_basic_agent_logger()


class BaseMiddleware(RoutesMixin):
    """
    BaseMiddleware contains all the initial setup for the framework middlewares

    Requirements:

        1. It's callable
        2. It has call_with_agent
        3. It has call_without_agent

    Pre and post filter calls should not block the flow that this class has.

    Pre -> get_response -> post
    """

    _loaded = False
    app_name = ""  # This should be overridden by child classes

    DIAGNOSTIC_ENDPOINT = "/save-contrast-security-config"
    DIAGNOSTIC_ALLOWED_SERVER = "localhost"
    DIAGNOSTIC_ALLOWED_IP = "127.0.0.1"
    OVERRIDE_MESSAGE = (
        "A security filter prevented original response from being returned."
    )
    LOGS_SEPARATOR = "-" * 120

    def __init__(self):
        # use _loaded to call our middleware only once because of runserver and WSGIHandler being initialized twice.
        if BaseMiddleware._loaded:
            return

        # id to distinguish middlewares created by different processes
        self.id = id(self)

        self.log_initialize()

        self.settings = None

        self.routes = {}
        self.first_request = True

        if not self.initialize_settings(self.app_name):
            logger.error("Unable to initialize Contrast Agent.")
            return

        if not self.settings.is_agent_config_enabled():
            logger.warning("Contrast Agent is not enabled.")
            return

        setup_agent_logger(self.settings.config)
        self.log_environment()

        if not self.initialize_service_client():
            logger.error("Unable to initialize Contrast Agent.")
            return

        self.initialize_libraries()

        if (
            self.settings.config
            and self.settings.config.get("protect.enable", True)
            and self.settings.config.get("assess.enable")
        ):
            logger.warning("Assess and Protect both enabled in agent configuration")
            logger.warning("Defaulting to Protect behavior only")

        patch_controller.enable_patches()

        if self.settings.is_assess_enabled():
            enable_providers()

        self.log_finish_initialize()

        BaseMiddleware._loaded = True

    def initialize_settings(self, app_name):
        """
        Initialize agent settings.

        Returns True on settings being initialized and False if any failure.
        """
        try:
            self.settings = SettingsState(app_name=app_name)
        except (Exception, DisableAgentException) as e:
            logger.error(e)
            return False
        return True

    def initialize_service_client(self):
        """
        Initialize connection to service.

        Returns True on service being initialized and False if any failure.
        """
        try:
            service_client.send_startup_messages()
        except (Exception, ContrastServiceException) as e:
            logger.error(e)
            return False
        return True

    def log_environment(self):
        """
        Log current working directory, python version and pip version
        """
        banner = "{0}ENVIRONMENT{0}".format("-" * 50)
        logger.debug(banner)
        logger.debug("Current Working Dir: %s", os.getcwd())
        logger.debug("Python Version: %s", sys.version)
        logger.debug("Framework Version: %s", self.settings.framework)
        logger.debug("Contrast Python Agent Version: %s", __version__)
        logger.debug(
            "Contrast Service Version %s",
            self.settings.server_features.contrast_service,
        )
        logger.debug("Platform %s", platform.platform())

        try:
            import pip

            logger.debug("Pip Version: %s", pip.__version__)
        except:
            pass

        logger.debug(banner)

    def initialize_libraries(self):
        """
        If enabled, read libraries from the application
        :return: True
        """
        if not self.settings.is_analyze_libs_enabled():
            return

        # Similar to the heartbeat thread, settings is required in order to send messages to SR
        self.library_reader = LibraryReader(self.settings.library_tags, self.settings)
        self.library_reader.start_library_analysis_thread()

    def is_agent_enabled(self):
        """
        Agent is considered enabled if all of the following are true:
        1. config value for 'enable' is True (or empty, defaults to True)
            (meaning no errors during initialization process including initial connection to Speedracer)
        2. ServiceClient connection to Speedracer is True

        NOTE: If #3 is false (the connection to Speedracer is down at any time during the request cycle) then
        the agent is automatically disabled.
        """
        if self.settings is None:
            return False

        if not self.settings.is_agent_config_enabled():
            return False

        if not service_client.is_connected():
            try:
                service_client.send_startup_messages()
            except ContrastServiceException:
                return False

        return service_client.is_connected()

    def call_with_agent(self, context, environ, start_response):
        pass

    def call_without_agent(self):
        """
        If Agent was not initialized due to either entire settings initialization failing
        or just loggers failing, then we should print to stdout that the Agent is not running.
        """
        logger.warning("Contrast Agent is not running.")

    def handle_ensure(self, context, request):
        """
        Method that should run for all middlewares AFTER every request is made.
        """
        if context is None:
            logger.error("Context not defined in middleware ensure")
            return

        with scope.contrast_scope():
            if self.settings.is_assess_enabled():
                # route discovery and storage needs to occur before sending messages
                self.handle_routes(context, request)

                logger.debug("Updating preflight hashes with route info")
                update_preflight_hashes(context)

            logger.debug("Sending final messages for reporting.")

            service_client.send_messages(self.final_messages(context))

    def final_messages(self, context):
        final_messages = [
            context.server_activity,
            context.activity,
        ]

        # TODO: PYT-972
        # Currently we do not report an observed route if the route signature is empty
        # and/or missing. In the future, we want to try to generate a reasonable
        # substitute for the signature value if possible.
        if self.settings.is_assess_enabled() and context.observed_route.signature:
            final_messages.append(context.observed_route)

        if self.first_request:
            # ApplicationUpdate message only sent at first request once we have routes
            final_messages.append(service_client.build_update_message(self.routes))
            self.first_request = False

        return final_messages

    def update_libraries(self, context):
        """
        After the app code is executed and a response is received, check for
        newly loaded modules and determine if to update library information.
        """

        # TODO: PYT-807 will address reporting files loaded after our catch phase.
        # Disabled so it doesn't throw off the results sent up in ApplicationUpdate

        # from contrast.utils.patch_utils import get_loaded_modules
        # from contrast.utils import inventory_utils

        # if not self.settings.is_analyze_libs_enabled():
        #     return

        # if self.settings.unused_libraries:
        #     sys_modules = get_loaded_modules().values()

        #     if len(sys_modules) != self.settings.sys_module_count:
        #         self.settings.sys_module_count = len(sys_modules)
        #         self._get_updated_file_count(self.settings.libraries, sys_modules)
        #         # should we be updating info for unused libraries, and if so
        #         # should we move unused libraries that now have used_count > 0 to used libraries?
        #         self._get_updated_file_count(
        #             self.settings.unused_libraries, sys_modules
        #         )

        # inventory_utils.append_libraries(context.activity, self.settings)
        pass

    def _get_updated_file_count(self, libraries, sys_modules):
        """
        Check if there are any new files in libraries that were added to the sys path
        """

        for library in libraries:
            new_used_count = self._search_modules_for_library(
                library.file_path, sys_modules
            )
            library.used_class_count = new_used_count

    def _search_modules_for_library(self, library_name, sys_modules):
        """
        Searches every module to see if it is associated with the current package being looked at
        If the package hasn't been found, it gets the metadata for the package, otherwise it
        just keeps updating used file count
        :param sys_modules: current loaded sys modules
        :param library_name: name of the library
        :return: The new used file count for this library
        """
        all_lib_modules = [
            x for x in sys_modules if (x.__name__ + ".").startswith(library_name)
        ]

        return len(set(all_lib_modules))

    def generate_security_exception_response(self):
        """
        Generate a response to be returned in the case of a SecurityException.

        Middlewares must override this method in order to provide the kind
        of response object that is expected by that framework.
        """
        raise NotImplementedError(
            "Middlewares must provide their own security response generator"
        )

    def handle_exception(self, exception):
        """
        Handle an exception being thrown especially if it is a SecurityException
        """
        logger.debug(
            "Handling %s raised in %s",
            exception.__class__.__name__,
            self.__class__.__name__,
        )
        if isinstance(exception, SecurityException):
            logger.info("%s: %s", exception.__class__.__name__, exception)
            logger.debug("Overriding response in Contrast Middleware")
            return self.generate_security_exception_response()

        logger.error("Reraising %r", exception)
        raise

    def prefilter(self, context):
        """
        Prefilter - AKA input analysis - is performed mostly in Speedracer but partly in the agent.

        This is PROTECT only.

        In this method we call on speedracer to do input analysis, which can result in:
        1. Speedracer finds an attack in which case we block the request
        2. Speedracer returns input analysis to use for later sink / infilter analysis,
            in which case we store it here in the request context.
        """
        if not self.settings.is_protect_enabled():
            return

        context.timer.set_start("prefilter")

        logger.debug("Running prefilter.")
        context.speedracer_input_analysis = get_input_analysis()

        self.agent_prefilter()

        logger.debug("Completed prefilter.")

        context.timer.set_end("prefilter")

    def agent_prefilter(self):
        """
        Prefilter for any rules that do not yet use speedracer
        """
        scope.enter_contrast_scope()
        try:
            self.prefilter_defend()
        except SecurityException:
            logger.exception("PROTECT: threw security exception in prefilter")
            raise
        except:
            logger.exception("PROTECT: threw exception in prefilter")
        finally:
            scope.exit_contrast_scope()

    def prefilter_defend(self):
        rules = self.settings.defend_rules
        logger.debug("PROTECT: Running Agent prefilter.")

        for rule in rules.values():
            is_prefilter = rule.is_prefilter()

            if is_prefilter:
                rule.prefilter()

    def postfilter(self, context):
        """
        For all postfilter enabled rules.
        """
        context.timer.set_start("postfilter")

        if self.settings.is_protect_enabled():
            try:
                self.postfilter_defend()
            except SecurityException as e:
                logger.exception("PROTECT: threw security exception in postfilter")
                raise e
            except Exception:
                logger.exception("PROTECT: threw exception in postfilter")

        if self.settings.is_assess_enabled():
            scope.enter_contrast_scope()
            try:
                self.postfilter_assess(context)
            except Exception:
                logger.exception("ASSESS: threw exception in postfilter")
            scope.exit_contrast_scope()

        context.timer.set_end("postfilter")

    def _process_trigger_handler(self, handler):
        """
        Gather metadata about response handler callback for xss trigger node

        We need to check whether the response handler callback is an instance method or
        not. This affects the way that our policy machinery works, and it also affects
        reporting, so we need to make sure to account for the possibility that handler
        is a method of some class rather than a standalone function.

        This should be called by the `trigger_node` method in child classes.
        """
        module = handler.__module__
        class_name = ""

        if hasattr(handler, "__self__"):
            class_name = handler.__self__.__class__.__name__
            args = (handler.__self__,)
            instance_method = True
        else:
            args = ()
            instance_method = False

        return module, class_name, args, instance_method

    @cached_property
    def trigger_node(self):
        """
        Trigger node property used by assess reflected xss postfilter rule

        This must be overridden by child classes that make use of the reflected
        xss postfilter rule.
        """
        raise NotImplementedError("Children must define trigger_node property")

    def assess_reflected_xss_postfilter(self, context):
        """
        Evaluate xss rule for assess

        The xss rule is applied to the response body in order to determine whether it
        contains untrusted data. We rely on propagation through any template rendering
        and through the framework. The expectation is that untrusted data from
        a request will propagate successfully all the way to the response body, which
        we are able to see here.

        Each child middleware class must implement specific logic for the trigger node
        since the reporting will differ between frameworks.
        """
        policy = Policy()

        rule = policy.triggers["reflected-xss"]

        # We need to exit scope here in order to account for the fact that some
        # frameworks evaluate the content lazily. We don't want to be in scope when
        # that occurs since it would make us lose propagation. This would prevent us
        # from seeing the response as a tracked string, which we require in order to
        # apply the rule.
        with scope.pop_contrast_scope():
            result = context.response.body

        trigger_node, args = self.trigger_node

        # TODO: PYT-721 this trigger scope is already and shouldn't be required.
        # If/when we consolidate all scope levels, this scope should be removed
        # entirely since the postfilter is already in scope when it's called.
        with scope.trigger_scope():
            TriggerPolicy.apply(rule, [trigger_node], result, args, {})

    def postfilter_assess(self, context):
        """
        Run postfilter for any assess rules. Reflected xss rule runs by default.
        May be overridden in child classes.

        If the response content type matches a allowed content type, do not run
        xss postfilter assess This is because the security team
        considers reflected xss within these content types to be a false positive.
        """
        logger.debug("ASSESS: Running Agent postfilter.")

        # it is possible other forms (capital case) variants exist
        accepted_xss_response_content_types = [
            "/csv",
            "/javascript",
            "/json",
            "/pdf",
            "/x-javascript",
            "/x-json",
        ]

        content_type = context.response.headers.get("content-type", "")

        if not any(
            [
                name
                for name in accepted_xss_response_content_types
                if name in content_type
            ]
        ):
            self.assess_reflected_xss_postfilter(context)

    def postfilter_defend(self):
        rules = self.settings.defend_rules
        logger.debug("PROTECT: Running Agent postfilter.")

        for rule in rules.values():
            if rule.is_postfilter():
                rule.postfilter()

    def check_for_blocked(self, context):
        """
        Checks for BLOCK events in case SecurityException was caught by app code

        This should be called by each middleware after the view is generated
        but before returning the response (it can be before or after
        postfilter).

        If we make it to this call, it implies that either no SecurityException
        occurred, or if one did occur, it was caught by the application. If we
        find a BLOCK here, it necessarily implies that an attack was detected
        in the application, but the application caught our exception. If the
        application hadn't caught our exception, we never would have made it
        this far because the exception would have already bubbled up to the
        middleware exception handler. So this is really our first and our last
        opportunity to check for this particular edge case.
        """
        for result in context.activity.results:
            if result.response == AttackResult.BLOCKED:
                msg = "Rule {} threw a security exception".format(result.rule_id)
                raise SecurityException(None, message=msg)

    def log_start_request_analysis(self, request_path):
        logger.debug("Contrast Agent analyzing request: %s", request_path)

    def log_end_request_analysis(self, request_path):
        logger.debug(
            "Contrast Agent finished analyzing request: %s \n\n%s\n",
            request_path,
            self.LOGS_SEPARATOR,
        )

    def log_initialize(self):
        logger.info(
            "Initializing Contrast Agent %s [id=%s]", self.__class__.__name__, self.id
        )

        logger.info("Contrast Python Agent Version: %s\n", __version__)

    def log_finish_initialize(self):
        logger.info(
            "Finished Initializing Contrast Agent %s [id=%s] \n\n%s\n",
            self.__class__.__name__,
            self.id,
            self.LOGS_SEPARATOR,
        )
