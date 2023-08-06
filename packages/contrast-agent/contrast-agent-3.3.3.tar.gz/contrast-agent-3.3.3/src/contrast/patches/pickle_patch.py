# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.extern.wrapt import register_post_import_hook

from contrast.agent.policy import patch_manager
from contrast.applies.deserialization import apply_rule
from contrast.utils.patch_utils import patch_cls_or_instance

LOAD = "load"

PICKLE = "pickle"
DESERIALIZER = PICKLE


def load(original_load, patch_policy=None, *args, **kwargs):

    read_obj = args[0]

    try:
        seek_loc = read_obj.tell()
    except Exception:
        seek_loc = 0

    try:
        data = read_obj.read()
    except Exception:
        data = ""

    try:
        read_obj.seek(seek_loc)
    except Exception:
        pass

    return apply_rule(original_load, DESERIALIZER, data, args, kwargs)


def patch_pickle(pickle_module):
    # TODO: PYT-975
    # Eventually we hope to be able to handle this patch with policy as well but it's
    # slightly more complicated due to the safe stream handling behavior.
    patch_cls_or_instance(pickle_module, LOAD, load)


def register_patches():
    register_post_import_hook(patch_pickle, "pickle")


def reverse_patches():
    pickle = sys.modules.get("pickle")
    if not pickle:
        return

    patch_manager.reverse_patches_by_owner(pickle)
