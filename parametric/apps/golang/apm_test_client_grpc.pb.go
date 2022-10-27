// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             v3.21.8
// source: protos/apm_test_client.proto

package main

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// APMClientClient is the client API for APMClient service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type APMClientClient interface {
	StartSpan(ctx context.Context, in *StartSpanArgs, opts ...grpc.CallOption) (*StartSpanReturn, error)
	FinishSpan(ctx context.Context, in *FinishSpanArgs, opts ...grpc.CallOption) (*FinishSpanReturn, error)
	SpanSetMeta(ctx context.Context, in *SpanSetMetaArgs, opts ...grpc.CallOption) (*SpanSetMetaReturn, error)
	SpanSetMetric(ctx context.Context, in *SpanSetMetricArgs, opts ...grpc.CallOption) (*SpanSetMetricReturn, error)
	SpanSetError(ctx context.Context, in *SpanSetErrorArgs, opts ...grpc.CallOption) (*SpanSetErrorReturn, error)
	InjectHeaders(ctx context.Context, in *InjectHeadersArgs, opts ...grpc.CallOption) (*InjectHeadersReturn, error)
	FlushSpans(ctx context.Context, in *FlushSpansArgs, opts ...grpc.CallOption) (*FlushSpansReturn, error)
	FlushTraceStats(ctx context.Context, in *FlushTraceStatsArgs, opts ...grpc.CallOption) (*FlushTraceStatsReturn, error)
	StopTracer(ctx context.Context, in *StopTracerArgs, opts ...grpc.CallOption) (*StopTracerReturn, error)
}

type aPMClientClient struct {
	cc grpc.ClientConnInterface
}

func NewAPMClientClient(cc grpc.ClientConnInterface) APMClientClient {
	return &aPMClientClient{cc}
}

func (c *aPMClientClient) StartSpan(ctx context.Context, in *StartSpanArgs, opts ...grpc.CallOption) (*StartSpanReturn, error) {
	out := new(StartSpanReturn)
	err := c.cc.Invoke(ctx, "/APMClient/StartSpan", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *aPMClientClient) FinishSpan(ctx context.Context, in *FinishSpanArgs, opts ...grpc.CallOption) (*FinishSpanReturn, error) {
	out := new(FinishSpanReturn)
	err := c.cc.Invoke(ctx, "/APMClient/FinishSpan", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *aPMClientClient) SpanSetMeta(ctx context.Context, in *SpanSetMetaArgs, opts ...grpc.CallOption) (*SpanSetMetaReturn, error) {
	out := new(SpanSetMetaReturn)
	err := c.cc.Invoke(ctx, "/APMClient/SpanSetMeta", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *aPMClientClient) SpanSetMetric(ctx context.Context, in *SpanSetMetricArgs, opts ...grpc.CallOption) (*SpanSetMetricReturn, error) {
	out := new(SpanSetMetricReturn)
	err := c.cc.Invoke(ctx, "/APMClient/SpanSetMetric", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *aPMClientClient) SpanSetError(ctx context.Context, in *SpanSetErrorArgs, opts ...grpc.CallOption) (*SpanSetErrorReturn, error) {
	out := new(SpanSetErrorReturn)
	err := c.cc.Invoke(ctx, "/APMClient/SpanSetError", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *aPMClientClient) InjectHeaders(ctx context.Context, in *InjectHeadersArgs, opts ...grpc.CallOption) (*InjectHeadersReturn, error) {
	out := new(InjectHeadersReturn)
	err := c.cc.Invoke(ctx, "/APMClient/InjectHeaders", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *aPMClientClient) FlushSpans(ctx context.Context, in *FlushSpansArgs, opts ...grpc.CallOption) (*FlushSpansReturn, error) {
	out := new(FlushSpansReturn)
	err := c.cc.Invoke(ctx, "/APMClient/FlushSpans", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *aPMClientClient) FlushTraceStats(ctx context.Context, in *FlushTraceStatsArgs, opts ...grpc.CallOption) (*FlushTraceStatsReturn, error) {
	out := new(FlushTraceStatsReturn)
	err := c.cc.Invoke(ctx, "/APMClient/FlushTraceStats", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *aPMClientClient) StopTracer(ctx context.Context, in *StopTracerArgs, opts ...grpc.CallOption) (*StopTracerReturn, error) {
	out := new(StopTracerReturn)
	err := c.cc.Invoke(ctx, "/APMClient/StopTracer", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// APMClientServer is the server API for APMClient service.
// All implementations must embed UnimplementedAPMClientServer
// for forward compatibility
type APMClientServer interface {
	StartSpan(context.Context, *StartSpanArgs) (*StartSpanReturn, error)
	FinishSpan(context.Context, *FinishSpanArgs) (*FinishSpanReturn, error)
	SpanSetMeta(context.Context, *SpanSetMetaArgs) (*SpanSetMetaReturn, error)
	SpanSetMetric(context.Context, *SpanSetMetricArgs) (*SpanSetMetricReturn, error)
	SpanSetError(context.Context, *SpanSetErrorArgs) (*SpanSetErrorReturn, error)
	InjectHeaders(context.Context, *InjectHeadersArgs) (*InjectHeadersReturn, error)
	FlushSpans(context.Context, *FlushSpansArgs) (*FlushSpansReturn, error)
	FlushTraceStats(context.Context, *FlushTraceStatsArgs) (*FlushTraceStatsReturn, error)
	StopTracer(context.Context, *StopTracerArgs) (*StopTracerReturn, error)
	mustEmbedUnimplementedAPMClientServer()
}

// UnimplementedAPMClientServer must be embedded to have forward compatible implementations.
type UnimplementedAPMClientServer struct {
}

func (UnimplementedAPMClientServer) StartSpan(context.Context, *StartSpanArgs) (*StartSpanReturn, error) {
	return nil, status.Errorf(codes.Unimplemented, "method StartSpan not implemented")
}
func (UnimplementedAPMClientServer) FinishSpan(context.Context, *FinishSpanArgs) (*FinishSpanReturn, error) {
	return nil, status.Errorf(codes.Unimplemented, "method FinishSpan not implemented")
}
func (UnimplementedAPMClientServer) SpanSetMeta(context.Context, *SpanSetMetaArgs) (*SpanSetMetaReturn, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SpanSetMeta not implemented")
}
func (UnimplementedAPMClientServer) SpanSetMetric(context.Context, *SpanSetMetricArgs) (*SpanSetMetricReturn, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SpanSetMetric not implemented")
}
func (UnimplementedAPMClientServer) SpanSetError(context.Context, *SpanSetErrorArgs) (*SpanSetErrorReturn, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SpanSetError not implemented")
}
func (UnimplementedAPMClientServer) InjectHeaders(context.Context, *InjectHeadersArgs) (*InjectHeadersReturn, error) {
	return nil, status.Errorf(codes.Unimplemented, "method InjectHeaders not implemented")
}
func (UnimplementedAPMClientServer) FlushSpans(context.Context, *FlushSpansArgs) (*FlushSpansReturn, error) {
	return nil, status.Errorf(codes.Unimplemented, "method FlushSpans not implemented")
}
func (UnimplementedAPMClientServer) FlushTraceStats(context.Context, *FlushTraceStatsArgs) (*FlushTraceStatsReturn, error) {
	return nil, status.Errorf(codes.Unimplemented, "method FlushTraceStats not implemented")
}
func (UnimplementedAPMClientServer) StopTracer(context.Context, *StopTracerArgs) (*StopTracerReturn, error) {
	return nil, status.Errorf(codes.Unimplemented, "method StopTracer not implemented")
}
func (UnimplementedAPMClientServer) mustEmbedUnimplementedAPMClientServer() {}

// UnsafeAPMClientServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to APMClientServer will
// result in compilation errors.
type UnsafeAPMClientServer interface {
	mustEmbedUnimplementedAPMClientServer()
}

func RegisterAPMClientServer(s grpc.ServiceRegistrar, srv APMClientServer) {
	s.RegisterService(&APMClient_ServiceDesc, srv)
}

func _APMClient_StartSpan_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(StartSpanArgs)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(APMClientServer).StartSpan(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/APMClient/StartSpan",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(APMClientServer).StartSpan(ctx, req.(*StartSpanArgs))
	}
	return interceptor(ctx, in, info, handler)
}

func _APMClient_FinishSpan_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(FinishSpanArgs)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(APMClientServer).FinishSpan(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/APMClient/FinishSpan",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(APMClientServer).FinishSpan(ctx, req.(*FinishSpanArgs))
	}
	return interceptor(ctx, in, info, handler)
}

func _APMClient_SpanSetMeta_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SpanSetMetaArgs)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(APMClientServer).SpanSetMeta(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/APMClient/SpanSetMeta",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(APMClientServer).SpanSetMeta(ctx, req.(*SpanSetMetaArgs))
	}
	return interceptor(ctx, in, info, handler)
}

func _APMClient_SpanSetMetric_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SpanSetMetricArgs)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(APMClientServer).SpanSetMetric(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/APMClient/SpanSetMetric",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(APMClientServer).SpanSetMetric(ctx, req.(*SpanSetMetricArgs))
	}
	return interceptor(ctx, in, info, handler)
}

func _APMClient_SpanSetError_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SpanSetErrorArgs)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(APMClientServer).SpanSetError(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/APMClient/SpanSetError",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(APMClientServer).SpanSetError(ctx, req.(*SpanSetErrorArgs))
	}
	return interceptor(ctx, in, info, handler)
}

func _APMClient_InjectHeaders_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(InjectHeadersArgs)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(APMClientServer).InjectHeaders(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/APMClient/InjectHeaders",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(APMClientServer).InjectHeaders(ctx, req.(*InjectHeadersArgs))
	}
	return interceptor(ctx, in, info, handler)
}

func _APMClient_FlushSpans_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(FlushSpansArgs)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(APMClientServer).FlushSpans(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/APMClient/FlushSpans",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(APMClientServer).FlushSpans(ctx, req.(*FlushSpansArgs))
	}
	return interceptor(ctx, in, info, handler)
}

func _APMClient_FlushTraceStats_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(FlushTraceStatsArgs)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(APMClientServer).FlushTraceStats(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/APMClient/FlushTraceStats",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(APMClientServer).FlushTraceStats(ctx, req.(*FlushTraceStatsArgs))
	}
	return interceptor(ctx, in, info, handler)
}

func _APMClient_StopTracer_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(StopTracerArgs)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(APMClientServer).StopTracer(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/APMClient/StopTracer",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(APMClientServer).StopTracer(ctx, req.(*StopTracerArgs))
	}
	return interceptor(ctx, in, info, handler)
}

// APMClient_ServiceDesc is the grpc.ServiceDesc for APMClient service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var APMClient_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "APMClient",
	HandlerType: (*APMClientServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "StartSpan",
			Handler:    _APMClient_StartSpan_Handler,
		},
		{
			MethodName: "FinishSpan",
			Handler:    _APMClient_FinishSpan_Handler,
		},
		{
			MethodName: "SpanSetMeta",
			Handler:    _APMClient_SpanSetMeta_Handler,
		},
		{
			MethodName: "SpanSetMetric",
			Handler:    _APMClient_SpanSetMetric_Handler,
		},
		{
			MethodName: "SpanSetError",
			Handler:    _APMClient_SpanSetError_Handler,
		},
		{
			MethodName: "InjectHeaders",
			Handler:    _APMClient_InjectHeaders_Handler,
		},
		{
			MethodName: "FlushSpans",
			Handler:    _APMClient_FlushSpans_Handler,
		},
		{
			MethodName: "FlushTraceStats",
			Handler:    _APMClient_FlushTraceStats_Handler,
		},
		{
			MethodName: "StopTracer",
			Handler:    _APMClient_StopTracer_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "protos/apm_test_client.proto",
}
