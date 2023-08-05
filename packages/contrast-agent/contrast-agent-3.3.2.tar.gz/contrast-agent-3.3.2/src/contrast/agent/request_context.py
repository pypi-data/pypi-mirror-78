# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import ensure_binary, iteritems
from contrast.agent import scope

from contrast.agent.request import Request
from contrast.agent.settings_state import SettingsState
from contrast.api.dtm_pb2 import Activity, ServerActivity, ObservedRoute
from contrast.utils.timer import Timer

import logging

logger = logging.getLogger("contrast")


class RequestContext(object):
    def __init__(self, environ, body=None):

        logger.debug("Initializing Request Context")

        scope.enter_contrast_scope()

        self.timer = Timer()

        self.request = Request(environ, body)

        dtm = self.request.get_dtm()
        self.activity = Activity()
        self.activity.http_request.CopyFrom(dtm)

        self.server_activity = ServerActivity()

        self.speedracer_input_analysis = None
        self.do_not_track = False

        # to be populated with a RouteCoverage instance
        self.current_route = None

        self.observed_route = ObservedRoute()

        scope.exit_contrast_scope()

    @property
    def propagate_assess(self):
        # TODO: PYT-644 move this property of out this class?
        return SettingsState().is_assess_enabled() and not scope.in_scope()

    def extract_response_to_context(self, response):
        """
        Append response to request context and populate the HttpResponse DTM

        :response: Subclass of BaseResponseWrapper
        """
        self.response = response

        self.activity.http_response.response_code = response.status_code

        # From the dtm for normalized_response_headers:
        #   Key is UPPERCASE_UNDERSCORE
        #
        #   Example: Content-Type: text/html; charset=utf-8
        #   "CONTENT_TYPE" => Content-Type,["text/html; charset=utf8"]
        for key, values in iteritems(response.headers.dict_of_lists()):
            normalized_key = key.upper().replace("-", "_")
            response_headers = self.activity.http_response.normalized_response_headers
            response_headers[normalized_key].key = key
            response_headers[normalized_key].values.extend(values)

        self.activity.http_response.response_body_binary = ensure_binary(
            response.body or ""
        )

    def get_xss_findings(self):
        """
        Return a list of Finding obj of rule_id reflected-xss, if any exist in Activity
        """
        return [
            finding
            for finding in self.activity.findings
            if finding.rule_id == "reflected-xss"
        ]
