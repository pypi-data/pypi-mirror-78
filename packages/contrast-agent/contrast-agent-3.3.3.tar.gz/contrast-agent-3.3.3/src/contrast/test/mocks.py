# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""Central location for commonly used mocks"""
import mock

from contrast.agent.assess.apply_trigger import build_finding
from contrast.agent.assess.policy.trigger_policy import TriggerPolicy
from contrast.api.dtm_pb2 import UserInput
from contrast.api.settings_pb2 import InputAnalysis, InputAnalysisResult

apply_trigger = mock.patch(
    "contrast.agent.assess.policy.trigger_policy.TriggerPolicy.apply",
    side_effect=TriggerPolicy.apply,
)
build_finding = mock.patch(
    "contrast.agent.assess.apply_trigger.build_finding", side_effect=build_finding
)


def nosqli_input_analysis():
    """
    Return input analysis results as if Speedracer had processed the input.
    Note that the score_level may be different than what real Speedracer returns.
    """
    result = InputAnalysisResult(
        rule_id="nosql-injection",
        value='{"title": "Record One"}',
        path="user_input",
        key="user_input",
        input_type=UserInput.PARAMETER_VALUE,
        score_level=InputAnalysisResult.DEFINITEATTACK,
        ids=[],
    )

    return InputAnalysis(results=[result])


nosqli_input_analysis_mock = mock.patch(
    "contrast.agent.middlewares.base_middleware.get_input_analysis",
    return_value=nosqli_input_analysis(),
)
