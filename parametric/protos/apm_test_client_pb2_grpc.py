# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from parametric.protos import apm_test_client_pb2 as protos_dot_apm__test__client__pb2


class APMClientStub(object):
    """Interface of APM clients to be used for shared testing.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StartSpan = channel.unary_unary(
                '/APMClient/StartSpan',
                request_serializer=protos_dot_apm__test__client__pb2.StartSpanArgs.SerializeToString,
                response_deserializer=protos_dot_apm__test__client__pb2.StartSpanReturn.FromString,
                )
        self.FinishSpan = channel.unary_unary(
                '/APMClient/FinishSpan',
                request_serializer=protos_dot_apm__test__client__pb2.FinishSpanArgs.SerializeToString,
                response_deserializer=protos_dot_apm__test__client__pb2.FinishSpanReturn.FromString,
                )
        self.SpanSetMeta = channel.unary_unary(
                '/APMClient/SpanSetMeta',
                request_serializer=protos_dot_apm__test__client__pb2.SpanSetMetaArgs.SerializeToString,
                response_deserializer=protos_dot_apm__test__client__pb2.SpanSetMetaReturn.FromString,
                )
        self.SpanSetMetric = channel.unary_unary(
                '/APMClient/SpanSetMetric',
                request_serializer=protos_dot_apm__test__client__pb2.SpanSetMetricArgs.SerializeToString,
                response_deserializer=protos_dot_apm__test__client__pb2.SpanSetMetricReturn.FromString,
                )
        self.SpanSetError = channel.unary_unary(
                '/APMClient/SpanSetError',
                request_serializer=protos_dot_apm__test__client__pb2.SpanSetErrorArgs.SerializeToString,
                response_deserializer=protos_dot_apm__test__client__pb2.SpanSetErrorReturn.FromString,
                )
        self.InjectHeaders = channel.unary_unary(
                '/APMClient/InjectHeaders',
                request_serializer=protos_dot_apm__test__client__pb2.InjectHeadersArgs.SerializeToString,
                response_deserializer=protos_dot_apm__test__client__pb2.InjectHeadersReturn.FromString,
                )
        self.FlushSpans = channel.unary_unary(
                '/APMClient/FlushSpans',
                request_serializer=protos_dot_apm__test__client__pb2.FlushSpansArgs.SerializeToString,
                response_deserializer=protos_dot_apm__test__client__pb2.FlushSpansReturn.FromString,
                )
        self.FlushTraceStats = channel.unary_unary(
                '/APMClient/FlushTraceStats',
                request_serializer=protos_dot_apm__test__client__pb2.FlushTraceStatsArgs.SerializeToString,
                response_deserializer=protos_dot_apm__test__client__pb2.FlushTraceStatsReturn.FromString,
                )
        self.StopTracer = channel.unary_unary(
                '/APMClient/StopTracer',
                request_serializer=protos_dot_apm__test__client__pb2.StopTracerArgs.SerializeToString,
                response_deserializer=protos_dot_apm__test__client__pb2.StopTracerReturn.FromString,
                )


class APMClientServicer(object):
    """Interface of APM clients to be used for shared testing.
    """

    def StartSpan(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FinishSpan(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SpanSetMeta(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SpanSetMetric(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SpanSetError(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InjectHeaders(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FlushSpans(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FlushTraceStats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopTracer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_APMClientServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StartSpan': grpc.unary_unary_rpc_method_handler(
                    servicer.StartSpan,
                    request_deserializer=protos_dot_apm__test__client__pb2.StartSpanArgs.FromString,
                    response_serializer=protos_dot_apm__test__client__pb2.StartSpanReturn.SerializeToString,
            ),
            'FinishSpan': grpc.unary_unary_rpc_method_handler(
                    servicer.FinishSpan,
                    request_deserializer=protos_dot_apm__test__client__pb2.FinishSpanArgs.FromString,
                    response_serializer=protos_dot_apm__test__client__pb2.FinishSpanReturn.SerializeToString,
            ),
            'SpanSetMeta': grpc.unary_unary_rpc_method_handler(
                    servicer.SpanSetMeta,
                    request_deserializer=protos_dot_apm__test__client__pb2.SpanSetMetaArgs.FromString,
                    response_serializer=protos_dot_apm__test__client__pb2.SpanSetMetaReturn.SerializeToString,
            ),
            'SpanSetMetric': grpc.unary_unary_rpc_method_handler(
                    servicer.SpanSetMetric,
                    request_deserializer=protos_dot_apm__test__client__pb2.SpanSetMetricArgs.FromString,
                    response_serializer=protos_dot_apm__test__client__pb2.SpanSetMetricReturn.SerializeToString,
            ),
            'SpanSetError': grpc.unary_unary_rpc_method_handler(
                    servicer.SpanSetError,
                    request_deserializer=protos_dot_apm__test__client__pb2.SpanSetErrorArgs.FromString,
                    response_serializer=protos_dot_apm__test__client__pb2.SpanSetErrorReturn.SerializeToString,
            ),
            'InjectHeaders': grpc.unary_unary_rpc_method_handler(
                    servicer.InjectHeaders,
                    request_deserializer=protos_dot_apm__test__client__pb2.InjectHeadersArgs.FromString,
                    response_serializer=protos_dot_apm__test__client__pb2.InjectHeadersReturn.SerializeToString,
            ),
            'FlushSpans': grpc.unary_unary_rpc_method_handler(
                    servicer.FlushSpans,
                    request_deserializer=protos_dot_apm__test__client__pb2.FlushSpansArgs.FromString,
                    response_serializer=protos_dot_apm__test__client__pb2.FlushSpansReturn.SerializeToString,
            ),
            'FlushTraceStats': grpc.unary_unary_rpc_method_handler(
                    servicer.FlushTraceStats,
                    request_deserializer=protos_dot_apm__test__client__pb2.FlushTraceStatsArgs.FromString,
                    response_serializer=protos_dot_apm__test__client__pb2.FlushTraceStatsReturn.SerializeToString,
            ),
            'StopTracer': grpc.unary_unary_rpc_method_handler(
                    servicer.StopTracer,
                    request_deserializer=protos_dot_apm__test__client__pb2.StopTracerArgs.FromString,
                    response_serializer=protos_dot_apm__test__client__pb2.StopTracerReturn.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'APMClient', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class APMClient(object):
    """Interface of APM clients to be used for shared testing.
    """

    @staticmethod
    def StartSpan(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/APMClient/StartSpan',
            protos_dot_apm__test__client__pb2.StartSpanArgs.SerializeToString,
            protos_dot_apm__test__client__pb2.StartSpanReturn.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FinishSpan(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/APMClient/FinishSpan',
            protos_dot_apm__test__client__pb2.FinishSpanArgs.SerializeToString,
            protos_dot_apm__test__client__pb2.FinishSpanReturn.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SpanSetMeta(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/APMClient/SpanSetMeta',
            protos_dot_apm__test__client__pb2.SpanSetMetaArgs.SerializeToString,
            protos_dot_apm__test__client__pb2.SpanSetMetaReturn.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SpanSetMetric(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/APMClient/SpanSetMetric',
            protos_dot_apm__test__client__pb2.SpanSetMetricArgs.SerializeToString,
            protos_dot_apm__test__client__pb2.SpanSetMetricReturn.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SpanSetError(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/APMClient/SpanSetError',
            protos_dot_apm__test__client__pb2.SpanSetErrorArgs.SerializeToString,
            protos_dot_apm__test__client__pb2.SpanSetErrorReturn.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InjectHeaders(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/APMClient/InjectHeaders',
            protos_dot_apm__test__client__pb2.InjectHeadersArgs.SerializeToString,
            protos_dot_apm__test__client__pb2.InjectHeadersReturn.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FlushSpans(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/APMClient/FlushSpans',
            protos_dot_apm__test__client__pb2.FlushSpansArgs.SerializeToString,
            protos_dot_apm__test__client__pb2.FlushSpansReturn.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FlushTraceStats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/APMClient/FlushTraceStats',
            protos_dot_apm__test__client__pb2.FlushTraceStatsArgs.SerializeToString,
            protos_dot_apm__test__client__pb2.FlushTraceStatsReturn.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StopTracer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/APMClient/StopTracer',
            protos_dot_apm__test__client__pb2.StopTracerArgs.SerializeToString,
            protos_dot_apm__test__client__pb2.StopTracerReturn.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
