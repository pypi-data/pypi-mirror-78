# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import copy
import mock

import pytest
from contrast.extern import six

from contrast.agent.policy import constants
from contrast.agent.assess.policy import source_policy
from contrast.agent.middlewares.base_middleware import BaseMiddleware
from contrast.api.dtm_pb2 import Library, TraceEvent
from contrast.api.settings_pb2 import AgentSettings
from contrast.test.settings_builder import SettingsBuilder
from contrast.test.contract.events import check_event
from contrast.utils import patch_utils


@pytest.fixture(autouse=True)
def disable_service_client(mocker):
    """Prevent the test suite from inadvertently starting the service"""
    mocker.patch("contrast.agent.service_client.time.sleep")
    mocker.patch("contrast.agent.service_client._ServiceState.start_service")
    mocker.patch(
        "contrast.agent.service_client._ServiceState.send_dtm",
        return_value=AgentSettings(),
    )


@pytest.fixture(autouse=True)
def modified_modules_to_ignore_prefixes(monkeypatch):
    """
    In most uses of the agent we ignore module such as contrast...
    so we don't bother patching them, but since our apptests often start
    with contrast., we need to make sure these modules are not in the
    modules to ignore.
    """
    new_prefixes = list(patch_utils.MODULES_TO_IGNORE_PREFIXES[:])
    new_prefixes.remove("contrast.")
    new_prefixes = tuple(new_prefixes)

    monkeypatch.setattr(patch_utils, "MODULES_TO_IGNORE_PREFIXES", new_prefixes)


@pytest.fixture(autouse=True)
def reset_base_middleware():
    BaseMiddleware._loaded = False
    yield


@pytest.fixture(autouse=True, scope="module")
def disable_heartbeat():
    patch_heartbeat = mock.patch(
        "contrast.agent.settings_state.SettingsState.establish_heartbeat"
    )

    patch_heartbeat.start()
    yield
    patch_heartbeat.stop()


@pytest.fixture(autouse=True, scope="module")
def disable_providers():
    """
    Providers iterate over all loaded modules so it's an expensive
    """
    patch_enable_providers = mock.patch(
        "contrast.agent.middlewares.base_middleware.enable_providers"
    )

    patch_enable_providers.start()

    yield

    patch_enable_providers.stop()


def assert_django_sqli_finding_events(finding, source_class_name):
    assert len(finding.events) == 5

    check_event(
        finding.events[0],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.CREATION_TYPE),
        class_name=source_class_name,
        method_name="__getitem__",
        source_types=[source_policy.PARAMETER_TYPE],
        first_parent=None,
    )

    check_event(
        finding.events[1],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.PARAMETER + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="django.utils.safestring",
        method_name="mark_safe",
        source_types=[],
        first_parent=finding.events[0],
    )

    check_event(
        finding.events[2],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="concat",
        source_types=[],
        first_parent=finding.events[1],
    )

    check_event(
        finding.events[3],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="concat",
        source_types=[],
        first_parent=finding.events[2],
    )

    check_event(
        finding.events[4],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.TRIGGER_TYPE),
        class_name="SQLite3",
        method_name="execute",
        source_types=[],
        first_parent=finding.events[3],
    )


def assert_xss_cookie_finding_events(finding):
    import django

    legacy_django = django.__version__ < "1.11"

    assert len(finding.events) == 9

    check_event(
        finding.events[0],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.CREATION_TYPE),
        class_name="django.http.request.HttpRequest",
        method_name="__getattribute__",
        source_types=[source_policy.COOKIE_TYPE],
        first_parent=None,
    )

    check_event(
        finding.events[1],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        first_parent=finding.events[0],
    )

    check_event(
        finding.events[2],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="cformat",
        source_types=[],
        first_parent=finding.events[1],
    )

    check_event(
        finding.events[3],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="join",
        source_types=[],
        first_parent=finding.events[2],
    )

    check_event(
        finding.events[8],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.TRIGGER_TYPE),
        class_name="django.core.handlers.base" if not legacy_django else "app",
        method_name="_get_response" if not legacy_django else "app",
        source_types=[],
        first_parent=finding.events[7],
    )


def assert_subprocess_popen_finding_events(findings):
    events = findings[0].events
    assert len(events) == 9

    check_event(
        events[0],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.CREATION_TYPE),
        class_name="wsgi.environ",
        method_name="QUERY_STRING",
        source_types=[source_policy.QUERYSTRING_TYPE],
        first_parent=None,
        source="",
        target=constants.RETURN,
        ret_value="user_input=echo+attack",
    )

    offset = 0 if six.PY3 else 1

    check_event(
        events[1 + offset],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.OBJECT_KEY + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="encode" if six.PY3 else "split",
        source_types=[],
        first_parent=events[0 + offset],
        source=constants.OBJECT,
        target=constants.RETURN,
        ret_value="user_input=echo+attack" if six.PY3 else "echo+attack",
    )

    check_event(
        events[2 + offset],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.OBJECT_KEY + constants.TO_MARKER + constants.RETURN_KEY
        )
        if six.PY3
        else TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="decode" if six.PY3 else "replace",
        source_types=[],
        first_parent=events[1 + offset],
        source=constants.OBJECT if six.PY3 else "OBJ,P1",
        target=constants.RETURN,
        ret_value="user_input=echo+attack" if six.PY3 else "echo attack",
    )

    offset += 1 if six.PY3 else 0

    check_event(
        events[3 + offset],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.OBJECT_KEY + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="split",
        source_types=[],
        first_parent=events[2 + offset],
        source=constants.OBJECT,
        target=constants.RETURN,
        ret_value="echo+attack" if six.PY3 else "echo attack",
    )

    check_event(
        events[4 + offset],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str" if six.PY3 else "urllib",
        method_name="replace" if six.PY3 else "unquote",
        source_types=[],
        first_parent=events[3 + offset],
        source="OBJ,P1" if six.PY3 else "P0,KWARG:s",
        target=constants.RETURN,
        ret_value="echo attack",
    )

    check_event(
        events[5 + offset],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        )
        if six.PY3
        else TraceEvent.Action.Value(
            constants.OBJECT_KEY + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="urllib.parse" if six.PY3 else "str",
        method_name="unquote" if six.PY3 else "decode",
        source_types=[],
        first_parent=events[4 + offset],
        source="P0,KWARG:string" if six.PY3 else constants.OBJECT,
        target=constants.RETURN,
        ret_value="echo attack",
    )

    check_event(
        events[6 + offset],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.CREATION_TYPE),
        class_name="django.utils.datastructures.MultiValueDict",
        method_name="__getitem__",
        source_types=[source_policy.PARAMETER_TYPE],
        first_parent=None,  # TODO: PYT-922 wrong?
        source="",  # TODO: PYT-922 wrong?
        target=constants.RETURN,
        ret_value="echo attack",
    )

    check_event(
        events[7 + offset],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.TRIGGER_TYPE),
        class_name="subprocess.Popen",
        method_name="__init__",
        source_types=[],
        first_parent=events[6 + offset],
        source="P0,KWARG:args",
        target="",
        ret_value="None",  # TODO: PYT-922 is "None" ret value expected?
    )


def _build_lxml_lib():
    fake_lxml = Library()
    fake_lxml.version = "1.11.1"
    fake_lxml.manifest = "test"
    fake_lxml.class_count = 100
    fake_lxml.used_class_count = 50
    fake_lxml.file_path = "lxml"
    fake_lxml.url = "lxml.com"
    fake_lxml.hash_code = "123499789"
    fake_lxml.external_ms = 1
    fake_lxml.internal_ms = 1

    return fake_lxml


def _build_django_lib():
    fake_django = Library()
    fake_django.version = "7.7.7"
    fake_django.manifest = "test"
    fake_django.class_count = 100
    fake_django.used_class_count = 50
    fake_django.file_path = "django"
    fake_django.url = "djangoproject.com"
    fake_django.hash_code = "987654321"
    fake_django.external_ms = 1
    fake_django.internal_ms = 1

    return fake_django


def _build_yaml_lib():
    fake_yaml = Library()
    fake_yaml.version = "1.11.1"
    fake_yaml.manifest = "test"
    fake_yaml.class_count = 100
    fake_yaml.used_class_count = 50
    fake_yaml.file_path = "pyyaml"
    fake_yaml.url = "yaml.org"
    fake_yaml.hash_code = "123456789"
    fake_yaml.external_ms = 1
    fake_yaml.internal_ms = 1

    return fake_yaml


def _build_sqlalchemy_lib():
    fake_sqlalchemy = Library()
    fake_sqlalchemy.version = "1.3.1"
    fake_sqlalchemy.manifest = "test"
    fake_sqlalchemy.class_count = 100
    fake_sqlalchemy.used_class_count = 50
    fake_sqlalchemy.file_path = "sqlalchemy"
    fake_sqlalchemy.url = "sqlalchemy.org"
    fake_sqlalchemy.hash_code = "123456789"
    fake_sqlalchemy.external_ms = 1
    fake_sqlalchemy.internal_ms = 1

    return fake_sqlalchemy


def _build_markupsafe_lib():
    fake_markupsafe = Library()
    fake_markupsafe.version = "1.1.1"
    fake_markupsafe.manifest = "test"
    fake_markupsafe.class_count = 100
    fake_markupsafe.used_class_count = 50
    fake_markupsafe.file_path = "markupsafe"
    fake_markupsafe.url = "markupsafe.org"
    fake_markupsafe.hash_code = "123456789"
    fake_markupsafe.external_ms = 1
    fake_markupsafe.internal_ms = 1

    return fake_markupsafe


def build_extra_libs():
    """
    When adding a vulnerability that requires a 3rd party library, make sure to add the library here!

    This is used to mimic actual libraries being found on pip
    """
    return [
        _build_django_lib(),
        _build_lxml_lib(),
        _build_yaml_lib(),
        _build_markupsafe_lib(),
    ]


def validate_observed_route(request_context, method, url, source_name, source_type):
    observed_route = request_context.observed_route

    assert observed_route.verb == method
    assert observed_route.url == url

    sources = observed_route.sources
    matching_source = [src for src in sources if src.name == source_name][0]

    assert matching_source.name == source_name
    assert matching_source.type == source_type


def assert_route_appended(findings, url, verb):
    """
    Asserts that 1 route with the url and verb are in the findings

    Fail if we never found a matching route
    """
    for finding in findings:
        for route in finding.routes:
            if route.url == url and route.verb == verb:
                return

    routes_message = " Routes: {}".format(findings[0].routes) if findings else ""
    pytest.fail("Unable to find route in findings;" + routes_message)


def build_assess_settings():
    features = copy.deepcopy(SettingsBuilder.DEFAULT_FEATURES)
    features["defend"]["enabled"] = False
    features["assess"] = {"enabled": True}

    settings = SettingsBuilder().build_assess()

    # disable non dataflow rules
    settings.application_settings.disabled_assess_rules.append("crypto-weak-randomness")
    settings.application_settings.disabled_assess_rules.append("crypto-bad-mac")
    settings.application_settings.disabled_assess_rules.append("crypto-bad-ciphers")

    settings.libraries = build_extra_libs()

    return settings


def find_routes_by_verb(routes, verb):
    return [x for x in routes if x.verb == verb]


def current_routes_by_url(routes, url):
    return [x for x in routes.values() if x.url == url]


def assert_routes_count(routes, routes_count):
    assert len(routes) == routes_count


def assert_ssrf_finding(module, request_context, mocked):
    assert mocked.called
    assert mocked.call_args[0][1].name == "ssrf"

    # This case results in multiple findings for reasons that are not entirely understood
    num_findings = (
        2
        if module in ["urllib2_obj", "urllib2_str", "urllib.request_obj"]
        or six.PY2
        and module == "urllib"
        else 1
    )

    assert len(request_context.activity.findings) == num_findings
    assert request_context.activity.findings[0].rule_id == six.u("ssrf")
