import psycopg2
import requests
from ddtrace import tracer
from ddtrace.appsec import trace_utils as appsec_trace_utils
from flask import Flask, Response
from flask import request as flask_request
from iast import (
    weak_cipher,
    weak_cipher_secure_algorithm,
    weak_hash,
    weak_hash_duplicates,
    weak_hash_multiple,
    weak_hash_secure_algorithm,
)

try:
    from ddtrace.contrib.trace_utils import set_user
except ImportError:
    set_user = lambda *args, **kwargs: None

POSTGRES_CONFIG = dict(
    host="postgres", port="5433", user="system_tests_user", password="system_tests", dbname="system_tests",
)

app = Flask(__name__)

tracer.trace("init.service").finish()


@app.route("/")
def hello_world():
    return "Hello, World!\\n"


@app.route("/sample_rate_route/<i>")
def sample_rate(i):
    return "OK"


_TRACK_CUSTOM_APPSEC_EVENT_NAME = "system_tests_appsec_event"


@app.route("/waf", methods=["GET", "POST", "OPTIONS"])
@app.route("/waf/", methods=["GET", "POST", "OPTIONS"])
@app.route("/waf/<path:url>", methods=["GET", "POST", "OPTIONS"])
@app.route("/params/<path>", methods=["GET", "POST", "OPTIONS"])
@app.route("/tag_value/<string:value>/<int:code>", methods=["GET", "POST", "OPTIONS"])
def waf(*args, **kwargs):
    if "value" in kwargs:
        appsec_trace_utils.track_custom_event(
            tracer, event_name=_TRACK_CUSTOM_APPSEC_EVENT_NAME, metadata={"value": kwargs["value"]}
        )
        return "Value tagged", kwargs["code"], flask_request.args
    return "Hello, World!\\n"


@app.route("/read_file", methods=["GET"])
def read_file():
    if "file" not in flask_request.args:
        return "Please provide a file parameter", 400

    filename = flask_request.args.get("file")

    with open(filename, "r") as f:
        return f.read()


@app.route("/headers")
def headers():
    resp = Response("OK")
    resp.headers["Content-Language"] = "en-US"
    return resp


@app.route("/status")
def status_code():
    code = flask_request.args.get("code", default=200, type=int)
    return Response("OK, probably", status=code)


@app.route("/make_distant_call")
def make_distant_call():
    url = flask_request.args["url"]
    response = requests.get(url)

    result = {
        "url": url,
        "status_code": response.status_code,
        "request_headers": dict(response.request.headers),
        "response_headers": dict(response.headers),
    }

    return result


@app.route("/identify")
def identify():
    set_user(
        tracer,
        user_id="usr.id",
        email="usr.email",
        name="usr.name",
        session_id="usr.session_id",
        role="usr.role",
        scope="usr.scope",
    )
    return Response("OK")


@app.route("/identify-propagate")
def identify_propagate():
    set_user(
        tracer,
        user_id="usr.id",
        email="usr.email",
        name="usr.name",
        session_id="usr.session_id",
        role="usr.role",
        scope="usr.scope",
        propagate=True,
    )
    return Response("OK")


@app.route("/users")
def users():
    user = flask_request.args.get("user")
    set_user(
        tracer,
        user_id=user,
        email="usr.email",
        name="usr.name",
        session_id="usr.session_id",
        role="usr.role",
        scope="usr.scope",
    )
    return Response("OK")


@app.route("/dbm")
def dbm():
    integration = flask_request.args.get("integration")
    if integration == "psycopg":
        postgres_db = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = postgres_db.cursor()
        operation = flask_request.args.get("operation")
        if operation == "execute":
            cursor.execute("select 'blah'")
            return Response("OK")
        elif operation == "executemany":
            cursor.executemany("select %s", (("blah",), ("moo",)))
            return Response("OK")
        return Response(f"Cursor method is not supported: {operation}", 406)

    return Response(f"Integration is not supported: {integration}", 406)


@app.route("/iast/insecure_hashing/multiple_hash")
def view_weak_hash_multiple_hash():
    weak_hash_multiple()
    return Response("OK")


@app.route("/iast/insecure_hashing/test_secure_algorithm")
def view_weak_hash_secure_algorithm():
    result = weak_hash_secure_algorithm()
    return Response("OK")


@app.route("/iast/insecure_hashing/test_md5_algorithm")
def view_weak_hash_md5_algorithm():
    result = weak_hash()
    return Response("OK")


@app.route("/iast/insecure_hashing/deduplicate")
def view_weak_hash_deduplicate():
    weak_hash_duplicates()
    return Response("OK")


@app.route("/iast/insecure_cipher/test_insecure_algorithm")
def view_weak_cipher_insecure():
    weak_cipher()
    return Response("OK")


@app.route("/iast/insecure_cipher/test_secure_algorithm")
def view_weak_cipher_secure():
    weak_cipher_secure_algorithm()
    return Response("OK")


_TRACK_METADATA = {
    "metadata0": "value0",
    "metadata1": "value1",
}


_TRACK_USER = "system_tests_user"


@app.route("/user_login_success_event")
def track_user_login_success_event():
    appsec_trace_utils.track_user_login_success_event(tracer, user_id=_TRACK_USER, metadata=_TRACK_METADATA)
    return Response("OK")


@app.route("/user_login_failure_event")
def track_user_login_failure_event():
    appsec_trace_utils.track_user_login_failure_event(
        tracer, user_id=_TRACK_USER, exists=True, metadata=_TRACK_METADATA,
    )
    return Response("OK")


_TRACK_CUSTOM_EVENT_NAME = "system_tests_event"


@app.route("/custom_event")
def track_custom_event():
    appsec_trace_utils.track_custom_event(tracer, event_name=_TRACK_CUSTOM_EVENT_NAME, metadata=_TRACK_METADATA)
    return Response("OK")


@app.route("/iast/sqli/test_secure", methods=["POST"])
def view_sqli_secure():
    sql = "SELECT * FROM IAST_USER WHERE USERNAME = ? AND PASSWORD = ?"
    postgres_db = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = postgres_db.cursor()
    cursor.execute(sql, flask_request.form["username"], flask_request.form["password"])
    return Response("OK")


@app.route("/iast/sqli/test_insecure", methods=["POST"])
def view_sqli_insecure():
    sql = (
        "SELECT * FROM IAST_USER WHERE USERNAME = '"
        + flask_request.form["username"]
        + "' AND PASSWORD = '"
        + flask_request.form["password"]
        + "'"
    )
    postgres_db = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = postgres_db.cursor()
    cursor.execute(sql)
    return Response("OK")
