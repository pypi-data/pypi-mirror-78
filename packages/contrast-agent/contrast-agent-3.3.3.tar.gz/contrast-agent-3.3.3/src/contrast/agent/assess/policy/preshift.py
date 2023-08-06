# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.utils.assess.duck_utils import safe_obj_length


class Preshift(object):
    """
    Holder class for information prior to shifting
    """

    def __init__(self, self_obj, args, kwargs):
        self.obj = self_obj
        self.obj_length = safe_obj_length(self_obj)
        self.args = args or []
        self.kwargs = kwargs or {}
