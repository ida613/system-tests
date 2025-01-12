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
class TestWeakRandomness:
    """Test weak randomness detection."""

    sink_fixture = SinkFixture(
        vulnerability_type="WEAK_RANDOMNESS",
        http_method="GET",
        insecure_endpoint="/iast/weak_randomness/test_insecure",
        secure_endpoint="/iast/weak_randomness/test_secure",
        data=None,
        location_map={"java": "com.datadoghq.system_tests.iast.utils.WeakRandomnessExamples"},
    )

    def setup_insecure(self):
        self.sink_fixture.setup_insecure()

    def test_insecure(self):
        self.sink_fixture.test_insecure()

    def setup_secure(self):
        self.sink_fixture.setup_secure()

    def test_secure(self):
        self.sink_fixture.test_secure()
