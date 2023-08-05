# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.utils.base64_utils import base64_decode
from contrast.extern import six


def check_event(
    event,
    event_type,
    action,
    class_name,
    method_name,
    source_types,
    first_parent,
    source=None,
    target=None,
    ret_value=None,
):
    """

    Assert values for TraceEvent dtm.
    """
    assert event.type == event_type
    assert event.action == action
    assert event.signature.class_name == class_name
    assert event.signature.method_name == method_name

    assert all([s.type in source_types for s in event.event_sources])

    assert (
        event.parent_object_ids[0].id == first_parent.object_id
        if first_parent
        else True
    )

    if source:
        assert event.source == source

    if target:
        assert event.target == target

    if ret_value:
        # ret value is the right side of the vulnerability > details page in TS
        assert base64_decode(event.ret.value) == ret_value
        if ret_value == "None":
            # TODO: PYT-922 investigate why trigger event has taint ranges but ret
            #  val is None
            return
        if six.PY2 and method_name in ("replace", "split", "unquote", "decode"):
            # TODO: PYT-922 investigate why taint ranges in some legacy django events are
            #  different
            return
        for taint_range in event.taint_ranges:
            assert taint_range.range == "0:{}".format(len(ret_value))
