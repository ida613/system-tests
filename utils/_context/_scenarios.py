from logging import FileHandler
import os
from pathlib import Path
import shutil
import time

import pytest

from utils._context.containers import TestedContainer, WeblogContainer, AgentContainer, create_network
from utils._context.library_version import LibraryVersion
from utils.tools import logger, get_log_formatter, update_environ_with_local_env

current_scenario = None


class _Scenario:
    def __init__(self, name) -> None:
        self.name = name

        if os.environ.get("SYSTEMTESTS_SCENARIO", "EMPTY_SCENARIO") == self.name:
            global current_scenario
            current_scenario = self

            shutil.rmtree(self.host_log_folder, ignore_errors=True)
            Path(self.host_log_folder).mkdir(parents=True)

            handler = FileHandler(f"{self.host_log_folder}/tests.log", encoding="utf-8")
            handler.setFormatter(get_log_formatter())

            logger.addHandler(handler)

            update_environ_with_local_env()

    @property
    def is_current_scenario(self):
        return current_scenario is self

    def __call__(self, test_method):
        # handles @scenarios.scenario_name
        pytest.mark.scenario(self.name)(test_method)

        return test_method

    def session_start(self, session):
        """ called at the very begning of the process """

    def _get_warmups(self):
        return []

    def execute_warmups(self):
        """ Called before any setup """

        try:
            for warmup in self._get_warmups():
                logger.info(f"Executing warmup {warmup}")
                warmup()
        except:
            self.collect_logs()
            raise

    def post_setup(self, session):
        """ called after test setup """

    def collect_logs(self):
        """ Called after setup """

    @property
    def host_log_folder(self):
        return "logs" if self.name == "DEFAULT" else f"logs_{self.name.lower()}"

    @property
    def library(self):
        return None

    @property
    def agent_version(self):
        return None

    @property
    def weblog_variant(self):
        return None

    @property
    def php_appsec(self):
        return None

    def get_junit_properties(self):
        return {"dd_tags[systest.suite.context.scenario]": self.name}

    def __str__(self) -> str:
        return f"Scenario '{self.name}'"


class TestTheTestScenario(_Scenario):
    @property
    def host_log_folder(self):
        return "logs"

    @property
    def library(self):
        return LibraryVersion("java", "0.66.0")

    @property
    def weblog_variant(self):
        return "spring"


class EndToEndScenario(_Scenario):
    """ Scenario that implier an instrumented HTTP application shipping a tracer (weblog) and an agent """

    def __init__(
        self,
        name,
        weblog_env=None,
        proxy_state=None,
        tracer_sampling_rate=None,
        appsec_rules=None,
        appsec_enabled=True,
        additional_trace_header_tags=(),
        library_interface_timeout=None,
        agent_interface_timeout=None,
        backend_interface_timeout=0,
        include_postgres_db=False,
        include_cassandra_db=False,
        include_mongo_db=False,
        use_proxy=True,
        include_kafka=False,
    ) -> None:
        super().__init__(name)

        if not self.is_current_scenario:
            return

        self.agent_container = AgentContainer(host_log_folder=self.host_log_folder, use_proxy=use_proxy)
        self.weblog_container = WeblogContainer(
            self.host_log_folder,
            environment=weblog_env,
            tracer_sampling_rate=tracer_sampling_rate,
            appsec_rules=appsec_rules,
            appsec_enabled=appsec_enabled,
            additional_trace_header_tags=additional_trace_header_tags,
            use_proxy=use_proxy,
        )
        self.use_proxy = use_proxy
        self.proxy_state = proxy_state
        self.include_postgres_db = include_postgres_db

        self.weblog_container.environment["SYSTEMTESTS_SCENARIO"] = self.name

        self._required_containers = []

        if include_postgres_db:
            self._required_containers.append(
                TestedContainer(
                    image_name="postgres:latest",
                    name="postgres",
                    host_log_folder=self.host_log_folder,
                    user="postgres",
                    environment={"POSTGRES_PASSWORD": "password", "PGPORT": "5433"},
                    volumes={
                        "./utils/build/docker/postgres-init-db.sh": {
                            "bind": "/docker-entrypoint-initdb.d/init_db.sh",
                            "mode": "ro",
                        }
                    },
                )
            )

        if include_mongo_db:
            self._required_containers.append(
                TestedContainer(
                    image_name="mongo:latest",
                    name="mongodb",
                    host_log_folder=self.host_log_folder,
                    allow_old_container=True,
                )
            )
        if include_cassandra_db:
            self._required_containers.append(
                TestedContainer(
                    image_name="cassandra:latest",
                    name="cassandra_db",
                    host_log_folder=self.host_log_folder,
                    allow_old_container=True,
                )
            )

        if include_kafka:
            self._required_containers.append(
                TestedContainer(
                    image_name="bitnami/kafka:latest",
                    name="kafka",
                    host_log_folder=self.host_log_folder,
                    environment={
                        "KAFKA_LISTENERS": "PLAINTEXT://:9092",
                        "KAFKA_ADVERTISED_LISTENERS": "PLAINTEXT://kafka:9092",
                        "ALLOW_PLAINTEXT_LISTENER": "yes",
                        "KAFKA_ADVERTISED_HOST_NAME": "kafka",
                        "KAFKA_ADVERTISED_PORT": "9092",
                        "KAFKA_PORT": "9092",
                        "KAFKA_BROKER_ID": "1",
                        "KAFKA_ZOOKEEPER_CONNECT": "zookeeper:2181",
                    },
                    allow_old_container=True,
                )
            )
            self._required_containers.append(
                TestedContainer(
                    image_name="bitnami/zookeeper:latest",
                    name="zookeeper",
                    host_log_folder=self.host_log_folder,
                    environment={"ALLOW_ANONYMOUS_LOGIN": "yes",},
                    allow_old_container=True,
                )
            )

        if agent_interface_timeout is None:
            self.agent_interface_timeout = 5
        else:
            self.agent_interface_timeout = agent_interface_timeout

        self.backend_interface_timeout = backend_interface_timeout

        if library_interface_timeout is not None:
            self.library_interface_timeout = library_interface_timeout
        else:
            if self.weblog_container.library == "java":
                self.library_interface_timeout = 80
            elif self.weblog_container.library.library in ("golang",):
                self.library_interface_timeout = 10
            elif self.weblog_container.library.library in ("nodejs",):
                self.library_interface_timeout = 5
            elif self.weblog_container.library.library in ("php",):
                # possibly something weird on obfuscator, let increase the delay for now
                self.library_interface_timeout = 10
            elif self.weblog_container.library.library in ("python",):
                self.library_interface_timeout = 25
            else:
                self.library_interface_timeout = 40

    def session_start(self, session):
        super().session_start(session)

        for interface in ("agent", "library", "backend"):
            Path(f"{self.host_log_folder}/interfaces/{interface}").mkdir(parents=True, exist_ok=True)

        # called at the very begning of the process
        terminal = session.config.pluginmanager.get_plugin("terminalreporter")

        def print_info(info):
            logger.info(info)
            terminal.write_line(info)

        terminal.write_sep("=", "Test context", bold=True)
        print_info(f"Scenario: {self.name}")
        print_info(f"Logs folder: ./{self.host_log_folder}")
        print_info(f"Library: {self.library}")
        print_info(f"Agent: {self.agent_version}")
        if self.library == "php":
            print_info(f"AppSec: {self.weblog_container.php_appsec}")

        if self.weblog_container.libddwaf_version:
            print_info(f"libddwaf: {self.weblog_container.libddwaf_version}")

        if self.weblog_container.appsec_rules_file:
            print_info(f"AppSec rules version: {self.weblog_container.appsec_rules_version}")

        if self.weblog_container.uds_mode:
            print_info(f"UDS socket: {self.weblog_container.uds_socket}")

        print_info(f"Weblog variant: {self.weblog_container.weblog_variant}")
        print_info(f"Backend: {self.agent_container.dd_site}")

    def _get_warmups(self):
        from utils.proxy.core import start_proxy  # prevent circular import

        warmups = [create_network]

        if self.use_proxy:
            warmups.append(lambda: start_proxy(self.proxy_state))

        for container in self._required_containers:
            warmups.append(container.start)

        warmups += [
            self.agent_container.start,
            self.weblog_container.start,
            self._wait_for_app_readiness,
        ]

        return warmups

    def _wait_for_app_readiness(self):
        from utils import interfaces  # import here to avoid circular import

        if self.use_proxy:
            logger.debug("Wait for app readiness")

            if not interfaces.library.ready.wait(40):
                pytest.exit("Library not ready", 1)
            logger.debug("Library ready")

            if not interfaces.agent.ready.wait(40):
                pytest.exit("Datadog agent not ready", 1)
            logger.debug("Agent ready")

    def post_setup(self, session):
        from utils import interfaces

        if self.use_proxy:
            self._wait_interface(interfaces.library, session, self.library_interface_timeout)
            self._wait_interface(interfaces.agent, session, self.agent_interface_timeout)
            self._wait_interface(interfaces.backend, session, self.backend_interface_timeout)

            self.collect_logs()

            self._wait_interface(interfaces.library_stdout, session, 0)
            self._wait_interface(interfaces.library_dotnet_managed, session, 0)
            self._wait_interface(interfaces.agent_stdout, session, 0)
        else:
            self.collect_logs()

        containers = [self.agent_container, self.weblog_container] + self._required_containers

        for container in containers:
            try:
                container.remove()
            except:
                logger.exception(f"Failed to remove container {container}")

    @staticmethod
    def _wait_interface(interface, session, timeout):
        terminal = session.config.pluginmanager.get_plugin("terminalreporter")
        terminal.write_sep("-", f"Wait for {interface} ({timeout}s)")
        terminal.flush()

        interface.wait(timeout)

    def collect_logs(self):
        for container in (self.weblog_container, self.agent_container):
            try:
                container.save_logs()
            except:
                logger.exception(f"Fail to save logs for container {container}")

    @property
    def library(self):
        return self.weblog_container.library

    @property
    def agent_version(self):
        return self.agent_container.agent_version

    @property
    def weblog_variant(self):
        return self.weblog_container.weblog_variant

    @property
    def php_appsec(self):
        return self.weblog_container.php_appsec

    def get_junit_properties(self):
        result = super().get_junit_properties()

        result["dd_tags[systest.suite.context.agent]"] = self.agent_version
        result["dd_tags[systest.suite.context.library.name]"] = self.library.library
        result["dd_tags[systest.suite.context.library.version]"] = self.library.version
        result["dd_tags[systest.suite.context.weblog_variant]"] = self.weblog_variant
        result["dd_tags[systest.suite.context.sampling_rate]"] = self.weblog_container.tracer_sampling_rate
        result["dd_tags[systest.suite.context.libddwaf_version]"] = self.weblog_container.libddwaf_version
        result["dd_tags[systest.suite.context.appsec_rules_file]"] = self.weblog_container.appsec_rules_file

        return result


class CgroupScenario(EndToEndScenario):

    # cgroup test
    # require a dedicated warmup. Need to check the stability before
    # merging it into the default scenario

    def _get_warmups(self):
        warmups = super()._get_warmups()
        warmups.append(self._wait_for_weblog_cgroup_file)
        return warmups

    def _wait_for_weblog_cgroup_file(self):
        max_attempts = 10  # each attempt = 1 second
        attempt = 0

        filename = f"{self.host_log_folder}/docker/weblog/logs/weblog.cgroup"
        while attempt < max_attempts and not os.path.exists(filename):

            logger.debug(f"{filename} is missing, wait")
            time.sleep(1)
            attempt += 1

        if attempt == max_attempts:
            pytest.exit("Failed to access cgroup file from weblog container", 1)

        return True


class PerformanceScenario(EndToEndScenario):
    """ A not very used scenario : its aim is to measure CPU and MEM usage across a basic run"""

    def __init__(self, name) -> None:
        super().__init__(name, appsec_enabled=self.appsec_enabled, use_proxy=False)

    @property
    def appsec_enabled(self):
        return os.environ.get("DD_APPSEC_ENABLED") == "true"

    @property
    def host_log_folder(self):
        return "logs_with_appsec" if self.appsec_enabled else "logs_without_appsec"

    def _get_warmups(self):
        result = super()._get_warmups()
        result.append(self._extra_weblog_warmup)

        return result

    def _extra_weblog_warmup(self):
        import requests

        WARMUP_REQUEST_COUNT = 10
        WARMUP_LAST_SLEEP_DURATION = 3

        for _ in range(WARMUP_REQUEST_COUNT):
            requests.get("http://localhost:7777", timeout=10)
            time.sleep(0.6)

        time.sleep(WARMUP_LAST_SLEEP_DURATION)


class scenarios:
    empty_scenario = _Scenario("EMPTY_SCENARIO")
    todo = _Scenario("TODO")  # scenario that skips tests not yest executed
    test_the_test = TestTheTestScenario("TEST_THE_TEST")

    default = EndToEndScenario("DEFAULT", include_postgres_db=True)
    cgroup = CgroupScenario("CGROUP")
    custom = EndToEndScenario("CUSTOM")
    sleep = EndToEndScenario("SLEEP")

    # performance scenario just spawn an agent and a weblog, and spies the CPU and mem usage
    performances = PerformanceScenario("PERFORMANCES")

    # scenario for weblog arch that does not support Appsec
    appsec_unsupported = EndToEndScenario("APPSEC_UNSUPORTED")

    integrations = EndToEndScenario(
        "INTEGRATIONS",
        weblog_env={"DD_DBM_PROPAGATION_MODE": "full"},
        include_postgres_db=True,
        include_cassandra_db=True,
        include_mongo_db=True,
        include_kafka=True,
    )

    profiling = EndToEndScenario("PROFILING", library_interface_timeout=160, agent_interface_timeout=160)

    sampling = EndToEndScenario("SAMPLING", tracer_sampling_rate=0.5)

    trace_propagation_style_w3c = EndToEndScenario(
        "TRACE_PROPAGATION_STYLE_W3C",
        weblog_env={"DD_TRACE_PROPAGATION_STYLE_INJECT": "W3C", "DD_TRACE_PROPAGATION_STYLE_EXTRACT": "W3C",},
    )
    # Telemetry scenarios
    telemetry_dependency_loaded_test_for_dependency_collection_disabled = EndToEndScenario(
        "TELEMETRY_DEPENDENCY_LOADED_TEST_FOR_DEPENDENCY_COLLECTION_DISABLED",
        weblog_env={"DD_TELEMETRY_DEPENDENCY_COLLECTION_ENABLED": "false"},
    )
    telemetry_app_started_products_disabled = EndToEndScenario(
        "TELEMETRY_APP_STARTED_PRODUCTS_DISABLED",
        weblog_env={
            "DD_APPSEC_ENABLED": "false",
            "DD_PROFILING_ENABLED": "false",
            "DD_DYNAMIC_INSTRUMENTATION_ENABLED": "false",
        },
    )
    telemetry_message_batch_event_order = EndToEndScenario(
        "TELEMETRY_MESSAGE_BATCH_EVENT_ORDER", weblog_env={"DD_FORCE_BATCHING_ENABLE": "true"}
    )
    telemetry_log_generation_disabled = EndToEndScenario(
        "TELEMETRY_LOG_GENERATION_DISABLED", weblog_env={"DD_TELEMETRY_LOGS_COLLECTION_ENABLED": "false",},
    )
    telemetry_metric_generation_disabled = EndToEndScenario(
        "TELEMETRY_METRIC_GENERATION_DISABLED", weblog_env={"DD_TELEMETRY_METRICS_COLLECTION_ENABLED": "false",},
    )

    # ASM scenarios
    appsec_missing_rules = EndToEndScenario("APPSEC_MISSING_RULES", appsec_rules="/donotexists")
    appsec_corrupted_rules = EndToEndScenario("APPSEC_CORRUPTED_RULES", appsec_rules="/appsec_corrupted_rules.yml")
    appsec_custom_rules = EndToEndScenario("APPSEC_CUSTOM_RULES", appsec_rules="/appsec_custom_rules.json")
    appsec_blocking = EndToEndScenario("APPSEC_BLOCKING", appsec_rules="/appsec_blocking_rule.json")
    appsec_rules_monitoring_with_errors = EndToEndScenario(
        "APPSEC_RULES_MONITORING_WITH_ERRORS", appsec_rules="/appsec_custom_rules_with_errors.json"
    )
    appsec_disabled = EndToEndScenario(
        "APPSEC_DISABLED", weblog_env={"DD_APPSEC_ENABLED": "false"}, appsec_enabled=False
    )
    appsec_low_waf_timeout = EndToEndScenario("APPSEC_LOW_WAF_TIMEOUT", weblog_env={"DD_APPSEC_WAF_TIMEOUT": "1"})
    appsec_custom_obfuscation = EndToEndScenario(
        "APPSEC_CUSTOM_OBFUSCATION",
        weblog_env={
            "DD_APPSEC_OBFUSCATION_PARAMETER_KEY_REGEXP": "hide-key",
            "DD_APPSEC_OBFUSCATION_PARAMETER_VALUE_REGEXP": ".*hide_value",
        },
    )
    appsec_rate_limiter = EndToEndScenario("APPSEC_RATE_LIMITER", weblog_env={"DD_APPSEC_TRACE_RATE_LIMIT": "1"})

    appsec_waf_telemetry = EndToEndScenario(
        "APPSEC_WAF_TELEMETRY",
        weblog_env={"DD_INSTRUMENTATION_TELEMETRY_ENABLED": "true", "DD_TELEMETRY_METRICS_INTERVAL_SECONDS": "2.0"},
    )
    # The spec says that if  DD_APPSEC_RULES is defined, then rules won't be loaded from remote config.
    # In this scenario, we use remote config. By the spec, whem remote config is available, rules file embedded in the tracer will never be used (it will be the file defined in DD_APPSEC_RULES, or the data coming from remote config).
    # So, we set  DD_APPSEC_RULES to None to enable loading rules from remote config.
    # and it's okay not testing custom rule set for dev mode, as in this scenario, rules are always coming from remote config.
    appsec_ip_blocking = EndToEndScenario(
        "APPSEC_IP_BLOCKING",
        proxy_state={"mock_remote_config_backend": "ASM_DATA"},
        weblog_env={"DD_APPSEC_RULES": None},
    )

    appsec_request_blocking = EndToEndScenario(
        "APPSEC_REQUEST_BLOCKING",
        proxy_state={"mock_remote_config_backend": "ASM"},
        weblog_env={"DD_APPSEC_RULES": None},
    )

    appsec_runtime_activation = EndToEndScenario(
        "APPSEC_RUNTIME_ACTIVATION",
        proxy_state={"mock_remote_config_backend": "ASM_ACTIVATE_ONLY"},
        appsec_enabled=False,
        weblog_env={
            "DD_RC_TARGETS_KEY_ID": "TEST_KEY_ID",
            "DD_RC_TARGETS_KEY": "1def0961206a759b09ccdf2e622be20edf6e27141070e7b164b7e16e96cf402c",
            "DD_REMOTE_CONFIG_INTEGRITY_CHECK_ENABLED": "true",
        },
    )

    # Remote config scenarios
    # library timeout is set to 100 seconds
    # default polling interval for tracers is very low (5 seconds)
    # TODO configure the polling interval to a lower value instead of increasing the timeout

    remote_config_mocked_backend_asm_features = EndToEndScenario(
        "REMOTE_CONFIG_MOCKED_BACKEND_ASM_FEATURES",
        proxy_state={"mock_remote_config_backend": "ASM_FEATURES"},
        appsec_enabled=False,
        weblog_env={"DD_REMOTE_CONFIGURATION_ENABLED": "true"},
        library_interface_timeout=100,
    )

    remote_config_mocked_backend_live_debugging = EndToEndScenario(
        "REMOTE_CONFIG_MOCKED_BACKEND_LIVE_DEBUGGING",
        proxy_state={"mock_remote_config_backend": "LIVE_DEBUGGING"},
        weblog_env={
            "DD_DYNAMIC_INSTRUMENTATION_ENABLED": "1",
            "DD_DEBUGGER_ENABLED": "1",
            "DD_REMOTE_CONFIG_ENABLED": "true",
            "DD_INTERNAL_RCM_POLL_INTERVAL": "1000",
        },
        library_interface_timeout=100,
    )

    # The spec says that if  DD_APPSEC_RULES is defined, then rules won't be loaded from remote config.
    # In this scenario, we use remote config. By the spec, whem remote config is available, rules file embedded in the tracer will never be used (it will be the file defined in DD_APPSEC_RULES, or the data coming from remote config).
    # So, we set  DD_APPSEC_RULES to None to enable loading rules from remote config.
    # and it's okay not testing custom rule set for dev mode, as in this scenario, rules are always coming from remote config.
    remote_config_mocked_backend_asm_dd = EndToEndScenario(
        "REMOTE_CONFIG_MOCKED_BACKEND_ASM_DD",
        proxy_state={"mock_remote_config_backend": "ASM_DD"},
        weblog_env={"DD_APPSEC_RULES": None},
        library_interface_timeout=100,
    )

    remote_config_mocked_backend_asm_features_nocache = EndToEndScenario(
        "REMOTE_CONFIG_MOCKED_BACKEND_ASM_FEATURES_NOCACHE",
        proxy_state={"mock_remote_config_backend": "ASM_FEATURES_NO_CACHE"},
        weblog_env={"DD_APPSEC_ENABLED": "false", "DD_REMOTE_CONFIGURATION_ENABLED": "true",},
        library_interface_timeout=100,
    )

    remote_config_mocked_backend_asm_features_nocache = EndToEndScenario(
        "REMOTE_CONFIG_MOCKED_BACKEND_ASM_FEATURES_NOCACHE",
        proxy_state={"mock_remote_config_backend": "ASM_FEATURES_NO_CACHE"},
        weblog_env={"DD_APPSEC_ENABLED": "false", "DD_REMOTE_CONFIGURATION_ENABLED": "true",},
        library_interface_timeout=100,
    )

    remote_config_mocked_backend_live_debugging_nocache = EndToEndScenario(
        "REMOTE_CONFIG_MOCKED_BACKEND_LIVE_DEBUGGING_NOCACHE",
        proxy_state={"mock_remote_config_backend": "LIVE_DEBUGGING_NO_CACHE"},
        weblog_env={
            "DD_DYNAMIC_INSTRUMENTATION_ENABLED": "1",
            "DD_DEBUGGER_ENABLED": "1",
            "DD_REMOTE_CONFIG_ENABLED": "true",
        },
        library_interface_timeout=100,
    )

    remote_config_mocked_backend_asm_dd_nocache = EndToEndScenario(
        "REMOTE_CONFIG_MOCKED_BACKEND_ASM_DD_NOCACHE",
        proxy_state={"mock_remote_config_backend": "ASM_DD_NO_CACHE"},
        library_interface_timeout=100,
    )

    # APM tracing end-to-end scenarios
    apm_tracing_e2e = EndToEndScenario("APM_TRACING_E2E", backend_interface_timeout=5)
    apm_tracing_e2e_single_span = EndToEndScenario(
        "APM_TRACING_E2E_SINGLE_SPAN",
        weblog_env={
            "DD_SPAN_SAMPLING_RULES": '[{"service": "weblog", "name": "*single_span_submitted", "sample_rate": 1.0, "max_per_second": 50}]',
            "DD_TRACE_SAMPLE_RATE": "0",
        },
        backend_interface_timeout=5,
    )

    library_conf_custom_headers_short = EndToEndScenario(
        "LIBRARY_CONF_CUSTOM_HEADERS_SHORT", additional_trace_header_tags=("header-tag1", "header-tag2")
    )
    library_conf_custom_headers_long = EndToEndScenario(
        "LIBRARY_CONF_CUSTOM_HEADERS_LONG",
        additional_trace_header_tags=("header-tag1:custom.header-tag1", "header-tag2:custom.header-tag2"),
    )


if current_scenario is None:
    current_scenario_name = os.environ.get("SYSTEMTESTS_SCENARIO", "EMPTY_SCENARIO")
    raise ValueError(f"Scenario {current_scenario_name} does not exists")

logger.info(f"Current scenario is {current_scenario}")
