# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import socket

from contrast.agent.framework import Framework
from contrast.agent.heartbeat import Heartbeat
from contrast.agent.protect.mixins.REP_settings import SettingsREPMixin
from contrast.agent.protect.rule.rules_builder import RulesBuilder
from contrast.agent.reaction_processor import ReactionProcessor
from contrast.api.settings_pb2 import (
    AccumulatorSettings,
    AgentSettings,
    ApplicationSettings,
    ServerFeatures,
)
from contrast.configuration import AgentConfig
from contrast.utils.loggers.logger import reset_agent_logger
from contrast.utils.singleton import Singleton
from contrast.utils.string_utils import truncate

import logging

logger = logging.getLogger("contrast")


class SettingsState(Singleton, SettingsREPMixin):
    DEFAULT_HOST = "localhost"
    DEFAULT_PATH = "/"

    def init(self, app_name=None):
        """
        Singletons should override init, not __init__.
        """
        self.config = None
        self.config_features = {}
        self.last_update = None
        self.heartbeat = None
        self.framework = Framework()
        self.sys_module_count = 0

        # Features and Settings from Service
        self.server_features = ServerFeatures()
        self.application_settings = ApplicationSettings()
        self.accumulator_settings = AccumulatorSettings()

        # Server
        self.server_name = None
        self.server_path = None
        self.server_type = None

        self.exclusion_matchers = []

        # Rules
        self.assess_rules = dict()
        self.defend_rules = dict()

        # Initialize values from config file
        # Initialize config and loggers
        self.config = AgentConfig()
        self.application_tags = self.config.get("application.tags", "")
        self.library_tags = self.config.get("inventory.tags", "")

        # Initialize application metadata
        self.app_name = self.get_app_name(app_name)

        # Initialize libraries
        self.libraries = []
        self.unused_libraries = []
        self.top_level_modules = {}
        self.installed_distribution_keys = []

        logger.info("Contrast Agent finished loading settings.")

    def _is_defend_enabled_in_server_features(self):
        return (
            self.server_features
            and self.server_features.defend
            and self.server_features.defend.enabled
        )

    def is_agent_config_enabled(self):
        return self.config.get("enable", True)

    @property
    def is_bundled_enabled(self):
        """The default across agents is to use the bundled service by default"""
        return self.config.get("agent.service.enable", True)

    @property
    def pid(self):
        """
        pid is used by Speedracer to recognize a unique worker process for an application.

        pid must be unique for each worker process of an app.
        :return: int current process id
        """
        return os.getpid()

    def get_app_name(self, app_name):
        # Used in DARPA-Screener to set the app's name (so TS can tell the difference between 5 instances of the app)
        if os.environ.get("CONTRASTSECURITY_APP_NAME"):
            return os.environ.get("CONTRASTSECURITY_APP_NAME")

        if self.config.get("application.name"):
            return self.config.get("application.name")

        return app_name if app_name else "root"

    def establish_heartbeat(self):
        """
        Initialize Heartbeat between Agent and SR if it has not been already initialized.
        """
        if self.heartbeat is None:
            self.heartbeat = Heartbeat(self)
            self.heartbeat.daemon = True
            self.heartbeat.start()

    def process_responses(self, responses):
        """
        :param responses: list of Message responses from SR
        """
        self.establish_heartbeat()

        logger.debug("Processing %s responses", len(responses))

        for response in responses:
            if self.process_service_response(response):
                self.set_assess_rules()
                self.set_protect_rules()

    def process_service_response(self, data):
        reload_rules = False

        if data and isinstance(data, AgentSettings):
            self.last_update = data.sent_ms

            reload_rules = self.process_server_features(data) or reload_rules
            reload_rules = self.process_application_settings(data) or reload_rules
            reload_rules = self.process_accumulator_settings(data) or reload_rules

        if reload_rules:
            logger.debug(
                "Finished processing Contrast Service message and reloading rules."
            )

        return reload_rules

    def process_server_features(self, data):
        if not data.HasField("server_features"):
            return False

        self.server_features = data.server_features
        self.update_logger_from_features()

        self.log_server_features(data.server_features)

        return True

    def log_server_features(self, server_features):
        """
        Record server features received from teamserver (via the contrast service)
        Remove the rule_definitions field before logging because it's long and ugly
        """
        server_features_copy = ServerFeatures()
        server_features_copy.CopyFrom(server_features)
        del server_features_copy.defend.rule_definitions[:]
        logger.debug(
            "Received updated server features (excluding rule_definitions from"
            " log):\n%s",
            server_features_copy,
        )

    @property
    def code_exclusion_matchers(self):
        return [x for x in self.exclusion_matchers if x.is_code]

    def process_application_settings(self, data):
        if not data.HasField("application_settings"):
            return False

        self.application_settings = data.application_settings

        ReactionProcessor.process(data.application_settings, self)

        self.reset_transformed_settings()

        logger.debug(
            "Received updated application settings:\n%s", data.application_settings
        )

        return True

    def reset_transformed_settings(self):
        self.exclusion_matchers = []

    def process_accumulator_settings(self, data):
        if data.HasField("accumulator_settings"):
            self.accumulator_settings = data.accumulator_settings

    def update_logger_from_features(self):
        # Python does not support TRACE level so we use DEBUG for now
        log_level = (
            "DEBUG"
            if self.server_features.log_level == "TRACE"
            else self.server_features.log_level
        )
        reset_agent_logger(self.server_features.log_file, log_level)

    def is_inventory_enabled(self):
        """
        inventory.enable = false: Disables both route coverage and library analysis and reporting
        """
        return self.config.get("inventory.enable", True)

    def is_analyze_libs_enabled(self):
        """
        inventory.analyze_libraries = false: Disables only library analysis/reporting
        """
        return (
            self.config.get("inventory.analyze_libraries", True)
            and self.is_inventory_enabled()
        )

    def is_assess_enabled(self):
        """
        We do not allow assess and defend to be on at the same time. As defend
        is arguably the more important of the two, it will take precedence

        The agent config may enable assess even if it is turned off in TS. This
        allows unlicensed apps to send findings to TS, where they will appear
        as obfuscated results.
        """
        if self.config is None or self.is_protect_enabled():
            return False

        assess_enabled = self.config.get("assess.enable", None)
        if assess_enabled is not None:
            return assess_enabled

        return (
            self.server_features
            and self.server_features.assess
            and self.server_features.assess.enabled
        )

    def is_protect_enabled(self):
        """
        Protect is enabled only if both configuration and server features enable it.
        """
        if self.config is None:
            return False
        config_protect_enabled = self.config.get("protect.enable", True)
        return config_protect_enabled and self._is_defend_enabled_in_server_features()

    def set_assess_rules(self):
        self.assess_rules = RulesBuilder.build_assess_rules(self)

    def set_protect_rules(self):
        """
        Stores all of our defend rules

        """
        if not self._is_defend_enabled_in_server_features():
            self.defend_rules = dict()
            return
        self.defend_rules = RulesBuilder.build_protect_rules(self)
        logger.debug("Built %s protect rules from settings", len(self.defend_rules))

    def get_server_name(self):
        """
        Hostname of the server

        Default is localhost
        """
        if self.server_name is None:
            detected_server = truncate(socket.gethostname(), self.DEFAULT_HOST)
            self.server_name = self.config.get("server.name", detected_server)

        return self.server_name

    def get_server_path(self):
        """
        Working Directory of the server

        Default is root
        """
        if self.server_path is None:
            detected_path = truncate(os.getcwd(), self.DEFAULT_PATH)
            self.server_path = self.config.get("server.path", detected_path)

        return self.server_path

    def get_server_type(self):
        """
        Web Framework of the Application either defined in common config or via discovery.
        """
        if self.server_type is None:
            self.server_type = (
                self.config.get("server.type") or self.framework.name_lower
            )

        return self.server_type
