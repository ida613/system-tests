import pytest

from utils.parametric.spec.trace import find_trace_by_root
from utils.parametric.spec.trace import find_span_in_traces
from utils.parametric.spec.trace import find_span
from utils.parametric.spec.otel_trace import OtelSpan
from utils import missing_feature, context, scenarios

# this global mark applies to all tests in this file.
#   DD_TRACE_OTEL_ENABLED=true is required in some tracers (.NET, Python?)
#   CORECLR_ENABLE_PROFILING=1 is required in .NET to enable auto-instrumentation
pytestmark = pytest.mark.parametrize(
    "library_env", [{"DD_TRACE_OTEL_ENABLED": "true", "CORECLR_ENABLE_PROFILING": "1"}],
)


@scenarios.parametric
class Test_Otel_Tracer:
    @missing_feature(context.library == "dotnet", reason="Span names don't match expectations")
    @missing_feature(context.library == "ruby", reason="Not implemented")
    @missing_feature(context.library == "php", reason="Not implemented")
    def test_otel_simple_trace(self, test_agent, test_library):
        """
            Perform two traces
        """
        with test_library:
            with test_library.otel_start_span("root_one") as parent:
                parent.set_attributes({"parent_k1": "parent_v1"})
                with test_library.otel_start_span(name="child", parent_id=parent.span_id) as child:
                    assert parent.span_context()["trace_id"] == child.span_context()["trace_id"]
                    child.end_span()
                parent.end_span()
            with test_library.otel_start_span("root_two") as parent:
                with test_library.otel_start_span(name="child", parent_id=parent.span_id) as child:
                    assert parent.span_context()["trace_id"] == child.span_context()["trace_id"]
                    child.end_span()
                parent.end_span()

        traces = test_agent.wait_for_num_traces(2)
        trace_one = find_trace_by_root(traces, OtelSpan(name="root_one"))
        assert len(trace_one) == 2

        root_span = find_span(trace_one, OtelSpan(name="root_one"))
        assert root_span["name"] == "root_one"
        assert root_span["meta"]["parent_k1"] == "parent_v1"

        child_span = find_span(trace_one, OtelSpan(name="child"))
        assert child_span["name"] == "child"

        trace_two = find_trace_by_root(traces, OtelSpan(name="root_two"))
        assert len(trace_two) == 2

        root_span = find_span(trace_two, OtelSpan(name="root_two"))
        assert root_span["name"] == "root_two"

        child_span = find_span(trace_one, OtelSpan(name="child"))
        assert child_span["name"] == "child"

    @missing_feature(
        context.library == "dotnet",
        reason="Span names don't match expectations: 'ApmTestClient.internal' == 'test_span'",
    )
    @missing_feature(context.library == "php", reason="Not implemented")
    @missing_feature(context.library == "ruby", reason="Not implemented")
    def test_force_flush_otel(self, test_agent, test_library):
        """
            Verify that force flush flushed the spans
        """
        with test_library:
            with test_library.otel_start_span(name="test_span") as span:
                span.end_span()
            # force flush with 5 second time out
            flushed = test_library.otel_flush(5)
            assert flushed, "ForceFlush error"
            # check if trace is flushed
            traces = test_agent.wait_for_num_traces(1)
            span = find_span_in_traces(traces, OtelSpan(name="test_span"))
            assert span.get("name") == "test_span"
