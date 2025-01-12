In system-tests, a scenario is a set of:

* a tested architecture, which can be a set of docker containers, a single container, or even nothing
* a list of setup executed on this tested architecture
* and a list of test

## How to identify a scenario?

Every scenarios are identified by an unique identifier in capital letter, like `APPSEC_IP_BLOCKING_FULL_DENYLIST`. To specify a scenario, simply use its name after `run.sh`:

```bash
./run.sh APPSEC_IP_BLOCKING_FULL_DENYLIST
```

If no scenario is specified, the `DEFAULT` scenario is executed.

## How to define a tested architecture?

Scenario's architecture is defined in python, in the file `utils/_context/scenarios.py`. Most of them are based on `EndToEndScenario` class. It spwans a container with an weblog (shipping a datadog tracer), an container with an datadog agent, and a proxy that spies everything coming from tracer and agent. Optionnaly, some other containers can be added (mostly databases).

## How to define setup?

A setup is a class method with the same name of a test method. They are all executed before any test starts. If a test is not executed (whatever the reason), the setup method won't be executed.

## How to define test executed by a scenario

The `scenarios` singleton is available under `utils` module. It exposes decorators with  all possible scenarios. Simply decorate your test class/method with it :

```python
@scenarios.my_scenario
class Test_Something:
    ...
```
