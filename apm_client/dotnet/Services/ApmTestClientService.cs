﻿using System.Reflection;
using Datadog.Trace;
using Grpc.Core;

namespace ApmTestClient.Services
{
    public class ApmTestClientService : APMClient.APMClientBase
    {
        private static readonly Type SpanType = Type.GetType("Datadog.Trace.Span, Datadog.Trace", throwOnError: true)!;
        private static readonly MethodInfo SetMetric = SpanType.GetMethod("SetMetric")!;
        private static readonly Dictionary<ulong, ISpan> Spans = new();
        private readonly ILogger<ApmTestClientService> _logger;
        public ApmTestClientService(ILogger<ApmTestClientService> logger)
        {
            _logger = logger;
        }

        public override Task<StartSpanReturn> StartSpan(StartSpanArgs request, ServerCallContext context)
        {
            var creationSettings = new SpanCreationSettings()
            {
                FinishOnClose = false,
            };

            if (request.HasParentId && request.ParentId > 0)
            {
                var parentSpan = Spans[request.ParentId];
                creationSettings.Parent = new SpanContext(parentSpan.TraceId, parentSpan.SpanId);
            }

            using var scope = Tracer.Instance.StartActive(operationName: request.Name, creationSettings);
            var span = scope.Span;

            if (request.HasService)
            {
                span.ServiceName = request.Service;
            }

            if (request.HasResource)
            {
                span.ResourceName = request.Resource;
            }

            Spans[span.SpanId] = span;

            return Task.FromResult(new StartSpanReturn
            {
                SpanId = span.SpanId,
                TraceId = span.TraceId,
            });
        }

        public override Task<SpanSetMetaReturn> SpanSetMeta(SpanSetMetaArgs request, ServerCallContext context)
        {
            var span = Spans[request.SpanId];
            span.SetTag(request.Key, request.Value);
            return Task.FromResult(new SpanSetMetaReturn());
        }

        public override Task<SpanSetMetricReturn> SpanSetMetric(SpanSetMetricArgs request, ServerCallContext context)
        {
            var span = Spans[request.SpanId];
            SetMetric.Invoke(span, new object[] { request.Key, request.Value });
            return Task.FromResult(new SpanSetMetricReturn());
        }

        public override Task<FinishSpanReturn> FinishSpan(FinishSpanArgs request, ServerCallContext context)
        {
            var span = Spans[request.Id];
            Spans.Remove(request.Id);
            span.Finish();
            return Task.FromResult(new FinishSpanReturn());
        }

        public override async Task<FlushSpansReturn> FlushSpans(FlushSpansArgs request, ServerCallContext context)
        {
            await Tracer.Instance.ForceFlushAsync();
            return new FlushSpansReturn();
        }

        public override Task<FlushTraceStatsReturn> FlushTraceStats(FlushTraceStatsArgs request, ServerCallContext context)
        {
            // No-op for now
            return Task.FromResult(new FlushTraceStatsReturn());
        }
    }
}
