# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
NOTE: This API is deprecated in favor of the one provided by
contrast.applies.sqli. It should be removed once all SQL patches have been
updated to use the new rule.
"""
import contrast
from contrast.agent import scope
from contrast.agent.protect.rule.sqli_rule import SqlInjection
from contrast.agent.assess.policy.utils import skip_analysis
from contrast.agent.settings_state import SettingsState
from contrast.applies.assess.applies_sqli_rule import apply_rule as assess_rule


def apply_rule_sqlalchemy(database, method, orig_func, sql, obj, args, kwargs):
    """
    Universal method to run Protect and Assess on a patched function for SQl Alchemy

    Protect must occur first so we can block prior to original function if need be

    Assess must occur after so we can check the result of the function

    :param database: database being used
    :param method: method name used in driver
    :param orig_func: original patched function
    :param sql: str query
    :param obj: driver object, Example: Cursor()
    :param args: args used in method
    :param kwargs: kwargs used in method
    :return: result of original function
    """
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context and SettingsState().is_protect_enabled():

        # TODO: PYT-975: remove creating fake policy node and patch loc policy
        from contrast.agent.policy.patch_location_policy import PatchLocationPolicy
        from contrast.agent.policy.trigger_node import TriggerNode

        trigger_node = TriggerNode(database, "unused", True, method, "ARG_0")
        patch_policy = PatchLocationPolicy(trigger_node)

        rule = SettingsState().defend_rules.get(SqlInjection.NAME)
        rule.protect(patch_policy, sql, args, kwargs)

    try:
        result = orig_func(*args, **kwargs)
    except Exception:
        result = None
        raise
    finally:
        if not skip_analysis(context):
            with scope.contrast_scope():
                assess_rule(context, database, method, sql, obj, result, args, kwargs)

    return result
