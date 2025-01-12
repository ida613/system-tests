# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

import pytest
from utils import context, coverage, released, missing_feature
from ..iast_fixtures import SinkFixture

if context.library == "cpp":
    pytestmark = pytest.mark.skip("not relevant")


@coverage.basic
@released(dotnet="?", java="?", golang="?", php_appsec="?", python="?", ruby="?", nodejs="?")
class TestNoHttponlyCookie:
    """Test no HttpOnly cookie detection."""

    sink_fixture = SinkFixture(
        vulnerability_type="NO_HTTPONLY_COOKIE",
        http_method="GET",
        insecure_endpoint="/iast/no-httponly-cookie/test_insecure",
        secure_endpoint="/iast/no-httponly-cookie/test_secure",
        data={},
        location_map={"nodejs": "iast/index.js",},
    )

    sink_fixture_empty_cookie = SinkFixture(
        vulnerability_type="NO_HTTPONLY_COOKIE",
        http_method="GET",
        insecure_endpoint="",
        secure_endpoint="/iast/no-httponly-cookie/test_empty_cookie",
        data={},
        location_map={"nodejs": "iast/index.js",},
    )

    def setup_insecure(self):
        self.sink_fixture.setup_insecure()

    def test_insecure(self):
        self.sink_fixture.test_insecure()

    def setup_secure(self):
        self.sink_fixture.setup_secure()

    def test_secure(self):
        self.sink_fixture.test_secure()

    def setup_empty_cookie(self):
        self.sink_fixture_empty_cookie.setup_secure()

    def test_empty_cookie(self):
        self.sink_fixture_empty_cookie.test_secure()

    def setup_telemetry_metric_instrumented_sink(self):
        self.sink_fixture.setup_telemetry_metric_instrumented_sink()

    @missing_feature(library="nodejs", reason="Metrics implemented")
    def test_telemetry_metric_instrumented_sink(self):
        self.sink_fixture.test_telemetry_metric_instrumented_sink()

    def setup_telemetry_metric_executed_sink(self):
        self.sink_fixture.setup_telemetry_metric_executed_sink()

    @missing_feature(library="nodejs", reason="Metrics implemented")
    def test_telemetry_metric_executed_sink(self):
        self.sink_fixture.test_telemetry_metric_executed_sink()
