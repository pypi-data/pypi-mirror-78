# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.applies import apply_rule
from contrast.utils.patch_utils import patch_cls_or_instance

import logging

logger = logging.getLogger("contrast")


def protect_patch(original_func, patch_policy, *args, **kwargs):
    """
    Protect patch that will run in addition to running original_func.
    If we cannot run the protect rule, at the very least run the original_func.
    """
    return apply_rule(patch_policy, original_func, args, kwargs)


def apply_protect_patch(patch_site, patch_policy):
    logger.debug("Applying protect patch to %s", patch_policy.name)

    patch_cls_or_instance(
        patch_site, patch_policy.method_name, protect_patch, patch_policy=patch_policy
    )
