# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.request import Request
from contrast.test import helper


class ExampleRequest(Request):
    def __init__(self, environ=None):
        super(Request, self).__init__(environ or helper.get_simple_request())
