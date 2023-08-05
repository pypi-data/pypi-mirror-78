# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent.protect.rule.deserialization_rule import Deserialization
from contrast.agent.settings_state import SettingsState


def apply_rule(orig_func, method_name, value, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context is not None and SettingsState().is_protect_enabled():
        # TODO: PYT-975: remove creating fake policy node and patch loc policy
        from contrast.agent.policy.patch_location_policy import PatchLocationPolicy
        from contrast.agent.policy.trigger_node import TriggerNode

        trigger_node = TriggerNode("unused", "unused", True, method_name, "ARG_0")
        patch_policy = PatchLocationPolicy(trigger_node)

        rule = SettingsState().defend_rules.get(Deserialization.NAME)
        rule.protect(patch_policy, value, args, kwargs)

    return orig_func(*args, **kwargs)
