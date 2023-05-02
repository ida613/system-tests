# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from utils import context, coverage, interfaces, irrelevant, missing_feature, released, rfc, scenarios, weblog


@released(cpp="?", dotnet="2.27.0", php_appsec="0.7.0", python="?", nodejs="?", golang="?", ruby="1.0.0")
@coverage.basic
@scenarios.appsec_blocking
@released(
    java={
        "spring-boot": "0.110.0",
        "sprint-boot-jetty": "0.111.0",
        "spring-boot-undertow": "0.111.0",
        "spring-boot-openliberty": "0.115.0",
        "ratpack": "1.6.0",
        "jersey-grizzly2": "1.7.0",
        "resteasy-netty3": "1.7.0",
        "vertx3": "1.7.0",
        "*": "?",
    }
)
class Test_BlockingAddresses:
    """Test the addresses supported for blocking"""

    def setup_request_method(self):
        self.rm_req = weblog.request("OPTIONS")

    @missing_feature(context.library == "ruby")
    def test_request_method(self):
        """can block on server.request.method"""

        interfaces.library.assert_waf_attack(self.rm_req, rule="tst-037-006")
        assert self.rm_req.status_code == 403

    def setup_request_uri(self):
        self.ruri_req = weblog.get("/waf/foo.git")

    def test_request_uri(self):
        """can block on server.request.uri.raw"""

        interfaces.library.assert_waf_attack(self.ruri_req, rule="tst-037-002")
        assert self.ruri_req.status_code == 403

    def setup_path_params(self):
        self.pp_req = weblog.get("/params/AiKfOeRcvG45")

    @missing_feature(library="java", reason="When supported, path parameter detection happens on subsequent WAF run")
    @irrelevant(context.library == "ruby" and context.weblog_variant == "rack")
    def test_path_params(self):
        """can block on server.request.path_params"""

        interfaces.library.assert_waf_attack(self.pp_req, rule="tst-037-007")
        assert self.pp_req.status_code == 403

    def setup_request_query(self):
        self.rq_req = weblog.get("/waf", params={"foo": "xtrace"})

    def test_request_query(self):
        """can block on server.request.query"""

        interfaces.library.assert_waf_attack(self.rq_req, rule="tst-037-001")
        assert self.rq_req.status_code == 403

    def setup_cookies(self):
        self.c_req = weblog.get("/", headers={"Cookie": "mycookie=jdfoSDGFkivRG_234"})

    def test_cookies(self):
        """can block on server.request.cookies"""

        interfaces.library.assert_waf_attack(self.c_req, rule="tst-037-008")
        assert self.c_req.status_code == 403

    def setup_request_body_urlencoded(self):
        self.rbue_req = weblog.post("/waf", data={"foo": "bsldhkuqwgervf"})

    @missing_feature(context.library == "java", reason="Happens on a subsequent WAF run")
    def test_request_body_urlencoded(self):
        """can block on server.request.body (urlencoded variant)"""

        interfaces.library.assert_waf_attack(self.rbue_req, rule="tst-037-004")
        assert self.rbue_req.status_code == 403

    def setup_request_body_multipart(self):
        self.rbmp_req = weblog.post("/waf", files={"foo": (None, "bsldhkuqwgervf")})

    @missing_feature(context.library == "dotnet", reason="Don't support multipart yet")
    @missing_feature(context.library == "php", reason="Don't support multipart yet")
    @missing_feature(context.library == "java", reason="Happens on a subsequent WAF run")
    def test_request_body_multipart(self):
        """can block on server.request.body (multipart/form-data variant)"""

        interfaces.library.assert_waf_attack(self.rbmp_req, rule="tst-037-004")
        assert self.rbmp_req.status_code == 403

    def setup_response_status(self):
        self.rss_req = weblog.get(path="/status", params={"code": "418"})

    @missing_feature(context.library == "dotnet", reason="only support blocking on 404 status at the moment")
    @missing_feature(context.library == "java", reason="Happens on a subsequent WAF run")
    @missing_feature(context.library < "ruby@1.10.0")
    def test_response_status(self):
        """can block on server.response.status"""

        interfaces.library.assert_waf_attack(self.rss_req, rule="tst-037-005")
        assert self.rss_req.status_code == 403

    def setup_not_found(self):
        self.rnf_req = weblog.get(path="/finger_print")

    @missing_feature(context.library == "java", reason="Happens on a subsequent WAF run")
    @missing_feature(context.library == "ruby", reason="Not working")
    def test_not_found(self):
        """can block on server.response.status"""

        interfaces.library.assert_waf_attack(self.rnf_req, rule="tst-037-010")
        assert self.rnf_req.status_code == 403

    def setup_response_header(self):
        self.rsh_req = weblog.get(path="/headers")

    @missing_feature(context.library == "java", reason="Happens on a subsequent WAF run")
    @missing_feature(context.library == "ruby")
    @missing_feature(context.library == "php", reason="Headers already sent at this stage")
    @missing_feature(context.library == "dotnet", reason="Address not supported yet")
    def test_response_header(self):
        """can block on server.response.headers.no_cookies"""

        interfaces.library.assert_waf_attack(self.rsh_req, rule="tst-037-009")
        assert self.rsh_req.status_code == 403

    @missing_feature(reason="No endpoint defined yet")
    def test_response_cookies(self):
        assert False


def _assert_custom_event_tag_presence(expected_value):
    def wrapper(span):
        tag = "appsec.events.system_tests_appsec_event.value"
        assert tag in span["meta"], f"Can't find {tag} in span's meta"
        value = span["meta"][tag]
        assert value == expected_value
        return True

    return wrapper


def _assert_custom_event_tag_absence():
    def wrapper(span):
        tag = "appsec.events.system_tests_appsec_event.value"
        assert tag not in span["meta"], f"Found {tag} in span's meta"
        return True

    return wrapper


@rfc("https://datadoghq.atlassian.net/wiki/spaces/APS/pages/2667021177/Suspicious+requests+blocking")
@scenarios.appsec_blocking
@coverage.good
@released(
    cpp="?",
    dotnet="2.29.0",
    golang="?",
    java="?",
    nodejs="?",
    php_appsec="?",
    python={"django-poc": "1.10", "flask-poc": "1.10", "*": "?"},
    ruby="?",
)
class Test_Blocking_request_method:
    """Test if blocking is supported on server.request.method address"""

    def setup_blocking(self):
        self.rm_req_block = weblog.request("OPTIONS")

    def test_blocking(self):
        """Test if requests that should be blocked are blocked"""
        assert self.rm_req_block.status_code == 403
        interfaces.library.assert_waf_attack(self.rm_req_block, rule="tst-037-006")

    def setup_non_blocking(self):
        self.rm_req_nonblock = weblog.request("GET")

    def test_non_blocking(self):
        """Test if requests that should not be blocked are not blocked"""
        assert self.rm_req_nonblock.status_code == 200

    def setup_blocking_before(self):
        self.set_req1 = weblog.request("GET", path="/tag_value/clean_value_3876/200")
        self.block_req2 = weblog.request("OPTIONS", path="/tag_value/tainted_value_6512/200")

    def test_blocking_before(self):
        """Test that blocked requests are blocked before being processed"""
        # first request should not block and must set the tag in span accordingly
        assert self.set_req1.status_code == 200
        assert self.set_req1.content == b"Value tagged"
        interfaces.library.validate_spans(self.set_req1, _assert_custom_event_tag_presence("clean_value_3876"))
        # second request should block and must not set the tag in span
        assert self.block_req2.status_code == 403
        interfaces.library.assert_waf_attack(self.block_req2, rule="tst-037-006")
        interfaces.library.validate_spans(self.block_req2, _assert_custom_event_tag_absence())


@rfc("https://datadoghq.atlassian.net/wiki/spaces/APS/pages/2667021177/Suspicious+requests+blocking")
@scenarios.appsec_blocking
@coverage.good
@released(
    cpp="?",
    dotnet="?",
    golang="?",
    java="?",
    nodejs="?",
    php_appsec="?",
    python={"django-poc": "1.10", "flask-poc": "1.10", "*": "?"},
    ruby="?",
)
class Test_Blocking_request_uri:
    """Test if blocking is supported on server.request.uri.raw address"""

    def setup_blocking(self):
        self.rm_req_block1 = self.ruri_req = weblog.get("/waf/foo.git")
        # query parameters are part of uri
        self.rm_req_block2 = weblog.get("/waf?foo=.git")

    def test_blocking(self):
        """Test if requests that should be blocked are blocked"""
        for response in (self.rm_req_block1, self.rm_req_block2):
            assert response.status_code == 403
            interfaces.library.assert_waf_attack(response, rule="tst-037-002")

    def setup_non_blocking(self):
        self.rm_req_nonblock = weblog.get("/waf/legit")

    def test_non_blocking(self):
        """Test if requests that should not be blocked are not blocked"""
        assert self.rm_req_nonblock.status_code == 200

    def setup_blocking_before(self):
        self.set_req1 = weblog.get("/tag_value/clean_value_3877/200")
        self.block_req2 = weblog.get("/tag_value/tainted_value_6512.git/200")

    def test_blocking_before(self):
        """Test that blocked requests are blocked before being processed"""
        # first request should not block and must set the tag in span accordingly
        assert self.set_req1.status_code == 200
        assert self.set_req1.content == b"Value tagged"
        interfaces.library.validate_spans(self.set_req1, _assert_custom_event_tag_presence("clean_value_3877"))
        # second request should block and must not set the tag in span
        assert self.block_req2.status_code == 403
        interfaces.library.assert_waf_attack(self.block_req2, rule="tst-037-002")
        interfaces.library.validate_spans(self.block_req2, _assert_custom_event_tag_absence())


@rfc("https://datadoghq.atlassian.net/wiki/spaces/APS/pages/2667021177/Suspicious+requests+blocking")
@scenarios.appsec_blocking
@coverage.good
@released(
    cpp="?",
    dotnet="2.29.0",
    golang="?",
    java="?",
    nodejs="?",
    php_appsec="?",
    python={"django-poc": "1.10", "flask-poc": "1.13", "*": "?"},
    ruby="?",
)
class Test_Blocking_request_path_params:
    """Test if blocking is supported on server.request.path_params address"""

    def setup_blocking(self):
        self.rm_req_block1 = weblog.get("/params/AiKfOeRcvG45")
        self.rm_req_block2 = weblog.get("/waf/AiKfOeRcvG45")

    def test_blocking(self):
        """Test if requests that should be blocked are blocked"""
        for response in (self.rm_req_block1, self.rm_req_block2):
            assert response.status_code == 403
            interfaces.library.assert_waf_attack(response, rule="tst-037-007")

    def setup_non_blocking(self):
        # query parameters are not a part of path parameters
        self.rm_req_nonblock = weblog.get("/waf/noharm?value=AiKfOeRcvG45")

    def test_non_blocking(self):
        """Test if requests that should not be blocked are not blocked"""
        assert self.rm_req_nonblock.status_code == 200

    def setup_blocking_before(self):
        self.set_req1 = weblog.get("/tag_value/clean_value_3878/200")
        self.block_req2 = weblog.get("/tag_value/tainted_value_AiKfOeRcvG45/200")

    def test_blocking_before(self):
        """Test that blocked requests are blocked before being processed"""
        # first request should not block and must set the tag in span accordingly
        assert self.set_req1.status_code == 200
        assert self.set_req1.content == b"Value tagged"
        interfaces.library.validate_spans(self.set_req1, _assert_custom_event_tag_presence("clean_value_3878"))
        # second request should block and must not set the tag in span
        assert self.block_req2.status_code == 403
        interfaces.library.assert_waf_attack(self.block_req2, rule="tst-037-007")
        interfaces.library.validate_spans(self.block_req2, _assert_custom_event_tag_absence())


@rfc("https://datadoghq.atlassian.net/wiki/spaces/APS/pages/2667021177/Suspicious+requests+blocking")
@scenarios.appsec_blocking
@coverage.good
@released(
    cpp="?",
    dotnet="2.29.0",
    golang="?",
    java="?",
    nodejs="?",
    php_appsec="?",
    python={"django-poc": "1.10", "flask-poc": "1.10", "*": "?"},
    ruby="?",
)
class Test_Blocking_request_query:
    """Test if blocking is supported on server.request.query address"""

    def setup_blocking(self):
        self.rm_req_block1 = weblog.get("/waf", params={"foo": "xtrace"})
        self.rm_req_block2 = weblog.get("/waf?foo=xtrace")

    def test_blocking(self):
        """Test if requests that should be blocked are blocked"""
        for response in (self.rm_req_block1, self.rm_req_block2):
            assert response.status_code == 403
            interfaces.library.assert_waf_attack(response, rule="tst-037-001")

    def setup_non_blocking(self):
        # path parameters are not a part of query parameters
        self.rm_req_nonblock1 = weblog.get("/waf/xtrace")
        # query parameters are blocking only on value not parameter name
        self.rm_req_nonblock2 = weblog.get("/waf?xtrace=foo")

    def test_non_blocking(self):
        """Test if requests that should not be blocked are not blocked"""
        for response in (self.rm_req_nonblock1, self.rm_req_nonblock2):
            assert response.status_code == 200

    def setup_blocking_before(self):
        self.set_req1 = weblog.get("/tag_value/clean_value_3879/200")
        self.block_req2 = weblog.get("/tag_value/tainted_value_a1b2c3/200?foo=xtrace")

    def test_blocking_before(self):
        """Test that blocked requests are blocked before being processed"""
        # first request should not block and must set the tag in span accordingly
        assert self.set_req1.status_code == 200
        assert self.set_req1.content == b"Value tagged"
        interfaces.library.validate_spans(self.set_req1, _assert_custom_event_tag_presence("clean_value_3879"))
        # second request should block and must not set the tag in span
        assert self.block_req2.status_code == 403
        interfaces.library.assert_waf_attack(self.block_req2, rule="tst-037-001")
        interfaces.library.validate_spans(self.block_req2, _assert_custom_event_tag_absence())


@rfc("https://datadoghq.atlassian.net/wiki/spaces/APS/pages/2667021177/Suspicious+requests+blocking")
@scenarios.appsec_blocking
@coverage.good
@released(
    cpp="?",
    dotnet="2.29.0",
    golang="?",
    java="?",
    nodejs="?",
    php_appsec="?",
    python={"django-poc": "1.10", "flask-poc": "1.10", "*": "?"},
    ruby="?",
)
class Test_Blocking_request_headers:
    """Test if blocking is supported on server.request.headers.no_cookies address"""

    def setup_blocking(self):
        self.rm_req_block1 = weblog.get("/waf", headers={"foo": "asldhkuqwgervf"})
        self.rm_req_block2 = weblog.get("/waf", headers={"Accept-Language": "asldhkuqwgervf"})

    def test_blocking(self):
        """Test if requests that should be blocked are blocked"""
        for response in (self.rm_req_block1, self.rm_req_block2):
            assert response.status_code == 403
            interfaces.library.assert_waf_attack(response, rule="tst-037-003")

    def setup_non_blocking(self):
        # query parameters are not a part of headers
        self.rm_req_nonblock1 = weblog.get("/waf?value=asldhkuqwgervf")
        # header parameters are blocking only on value not parameter name
        self.rm_req_nonblock2 = weblog.get("/waf", headers={"asldhkuqwgervf": "foo"})

    def test_non_blocking(self):
        """Test if requests that should not be blocked are not blocked"""
        for response in (self.rm_req_nonblock1, self.rm_req_nonblock2):
            assert response.status_code == 200

    def setup_blocking_before(self):
        self.set_req1 = weblog.get("/tag_value/clean_value_3880/200")
        self.block_req2 = weblog.get("/tag_value/tainted_value_xyz/200", headers={"foo": "asldhkuqwgervf"})

    def test_blocking_before(self):
        """Test that blocked requests are blocked before being processed"""
        # first request should not block and must set the tag in span accordingly
        assert self.set_req1.status_code == 200
        assert self.set_req1.content == b"Value tagged"
        interfaces.library.validate_spans(self.set_req1, _assert_custom_event_tag_presence("clean_value_3880"))
        # second request should block and must not set the tag in span
        assert self.block_req2.status_code == 403
        interfaces.library.assert_waf_attack(self.block_req2, rule="tst-037-003")
        interfaces.library.validate_spans(self.block_req2, _assert_custom_event_tag_absence())


@rfc("https://datadoghq.atlassian.net/wiki/spaces/APS/pages/2667021177/Suspicious+requests+blocking")
@scenarios.appsec_blocking
@coverage.good
@released(
    cpp="?",
    dotnet="2.29.0",
    golang="?",
    java="?",
    nodejs="?",
    php_appsec="?",
    python={"django-poc": "1.10", "flask-poc": "1.10", "*": "?"},
    ruby="?",
)
class Test_Blocking_request_cookies:
    """Test if blocking is supported on server.request.cookies address"""

    def setup_blocking(self):
        self.rm_req_block1 = weblog.get("/waf", cookies={"foo": "jdfoSDGFkivRG_234"})
        self.rm_req_block2 = weblog.get("/waf", cookies={"Accept-Language": "jdfoSDGFkivRG_234"})

    def test_blocking(self):
        """Test if requests that should be blocked are blocked"""
        for response in (self.rm_req_block1, self.rm_req_block2):
            assert response.status_code == 403
            interfaces.library.assert_waf_attack(response, rule="tst-037-008")

    def setup_non_blocking(self):
        # headers parameters are not a part of cookies
        self.rm_req_nonblock1 = weblog.get("/waf" "/waf", headers={"foo": "jdfoSDGFkivRG_234"})
        # cookies parameters are blocking only on value not parameter name
        self.rm_req_nonblock2 = weblog.get("/waf", headers={"jdfoSDGFkivRG_234": "foo"})

    def test_non_blocking(self):
        """Test if requests that should not be blocked are not blocked"""
        for response in (self.rm_req_nonblock1, self.rm_req_nonblock2):
            assert response.status_code == 200

    def setup_blocking_before(self):
        self.set_req1 = weblog.get("/tag_value/clean_value_3881/200")
        self.block_req2 = weblog.get("/tag_value/tainted_value_cookies/200", cookies={"foo": "jdfoSDGFkivRG_234"})

    def test_blocking_before(self):
        """Test that blocked requests are blocked before being processed"""
        # first request should not block and must set the tag in span accordingly
        assert self.set_req1.status_code == 200
        assert self.set_req1.content == b"Value tagged"
        interfaces.library.validate_spans(self.set_req1, _assert_custom_event_tag_presence("clean_value_3881"))
        # second request should block and must not set the tag in span
        assert self.block_req2.status_code == 403
        interfaces.library.assert_waf_attack(self.block_req2, rule="tst-037-008")
        interfaces.library.validate_spans(self.block_req2, _assert_custom_event_tag_absence())


@rfc("https://datadoghq.atlassian.net/wiki/spaces/APS/pages/2667021177/Suspicious+requests+blocking")
@scenarios.appsec_blocking
@coverage.good
@released(
    cpp="?",
    dotnet="2.29.0",
    golang="?",
    java="?",
    nodejs="?",
    php_appsec="?",
    python={"django-poc": "1.10", "flask-poc": "1.10", "*": "?"},
    ruby="?",
)
class Test_Blocking_request_body:
    """Test if blocking is supported on server.request.body address for urlencoded body"""

    def setup_blocking(self):
        self.rm_req_block1 = weblog.post("/waf", data={"value1": "bsldhkuqwgervf"})
        self.rm_req_block2 = weblog.post("/waf", data={"foo": "bsldhkuqwgervf"})

    def test_blocking(self):
        """Test if requests that should be blocked are blocked"""
        for response in (self.rm_req_block1, self.rm_req_block2):
            assert response.status_code == 403
            interfaces.library.assert_waf_attack(response, rule="tst-037-004")

    def setup_non_blocking(self):
        # raw body are never parsed
        self.rm_req_nonblock1 = weblog.post(
            "/waf", data=b'\x00{"value3": "bsldhkuqwgervf"}\xFF', headers={"content-type": "application/octet-stream"}
        )
        self.rm_req_nonblock2 = weblog.post(
            "/waf", data=b'{"value4": "bsldhkuqwgervf"}', headers={"content-type": "text/plain"}
        )

    def test_non_blocking(self):
        """Test if requests that should not be blocked are not blocked"""
        for response in (self.rm_req_nonblock1, self.rm_req_nonblock2):
            assert response.status_code == 200

    def setup_blocking_before(self):
        self.set_req1 = weblog.post("/tag_value/clean_value_3882/200", data="None")
        self.block_req2 = weblog.post("/tag_value/tainted_value_body/200", data={"value5": "bsldhkuqwgervf"},)

    def test_blocking_before(self):
        """Test that blocked requests are blocked before being processed"""
        # first request should not block and must set the tag in span accordingly
        assert self.set_req1.status_code == 200
        assert self.set_req1.content == b"Value tagged"
        interfaces.library.validate_spans(self.set_req1, _assert_custom_event_tag_presence("clean_value_3882"))
        # second request should block and must not set the tag in span
        assert self.block_req2.status_code == 403
        interfaces.library.assert_waf_attack(self.block_req2, rule="tst-037-004")
        interfaces.library.validate_spans(self.block_req2, _assert_custom_event_tag_absence())


@rfc("https://datadoghq.atlassian.net/wiki/spaces/APS/pages/2667021177/Suspicious+requests+blocking")
@scenarios.appsec_blocking
@coverage.good
@released(
    cpp="?",
    dotnet="?",
    golang="?",
    java="?",
    nodejs="?",
    php_appsec="?",
    python={"django-poc": "1.10", "flask-poc": "1.10", "*": "?"},
    ruby="?",
)
class Test_Blocking_response_status:
    """Test if blocking is supported on server.response.status address"""

    def setup_blocking(self):
        self.rm_req_block = {status: weblog.get(f"/tag_value/anything/{status}") for status in (415, 416, 417, 418)}

    def test_blocking(self):
        """Test if requests that should be blocked are blocked"""
        for code, response in self.rm_req_block.items():
            assert response.status_code == 403, response.request.url
            interfaces.library.assert_waf_attack(response, rule="tst-037-005")

    def setup_non_blocking(self):
        self.rm_req_nonblock = {status: weblog.get(f"/tag_value/anything/{status}") for status in (411, 412, 413, 414)}

    def test_non_blocking(self):
        """Test if requests that should not be blocked are not blocked"""
        for code, response in self.rm_req_nonblock.items():
            assert response.status_code == code, response.request.url


@rfc("https://datadoghq.atlassian.net/wiki/spaces/APS/pages/2667021177/Suspicious+requests+blocking")
@scenarios.appsec_blocking
@coverage.good
@released(
    cpp="?",
    dotnet="?",
    golang="?",
    java="?",
    nodejs="?",
    php_appsec="?",
    python={"django-poc": "1.10", "flask-poc": "1.10", "*": "?"},
    ruby="?",
)
class Test_Blocking_response_headers:
    """Test if blocking is supported on server.response.headers.no_cookies address"""

    def setup_blocking(self):
        self.rm_req_block1 = weblog.get(f"/tag_value/anything/200?content-language=en-us")
        self.rm_req_block2 = weblog.get(f"/tag_value/anything/200?content-language=krypton")

    def test_blocking(self):
        """Test if requests that should be blocked are blocked"""
        for response in (self.rm_req_block1, self.rm_req_block2):
            assert response.status_code == 403, response.request.url
            interfaces.library.assert_waf_attack(response, rule="tst-037-009")

    def setup_non_blocking(self):
        self.rm_req_nonblock1 = weblog.get(f"/tag_value/anything/200?content-color=en-us")
        self.rm_req_nonblock2 = weblog.get(f"/tag_value/anything/200?content-language=fr")

    def test_non_blocking(self):
        """Test if requests that should not be blocked are not blocked"""
        for response in (self.rm_req_nonblock1, self.rm_req_nonblock2):
            assert response.status_code == 200


@rfc("https://datadoghq.atlassian.net/wiki/spaces/APS/pages/2667021177/Suspicious+requests+blocking")
@coverage.not_implemented
@released(cpp="?", dotnet="2.29.0", php_appsec="?", python="?", nodejs="?", golang="?", ruby="?")
class Test_Suspicious_Request_Blocking:
    """Test if blocking on multiple addresses with multiple rules is supported"""

    def test_blocking(self):
        """Test if requests that should be blocked are blocked"""
        # TODO

    def test_non_blocking(self):
        """Test if requests that should not be blocked are not blocked"""
        # TODO

    def test_blocking_before(self):
        """Test that blocked requests are blocked before being processed"""
        # TODO
