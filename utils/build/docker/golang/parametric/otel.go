package main

import (
	"context"
	"fmt"
	"strconv"
	"strings"
	"time"

	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/codes"
	otel_trace "go.opentelemetry.io/otel/trace"
	"gopkg.in/DataDog/dd-trace-go.v1/ddtrace"
	ddotel "gopkg.in/DataDog/dd-trace-go.v1/ddtrace/opentelemetry"
	"gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
)

func (s *apmClientServer) OtelStartSpan(ctx context.Context, args *OtelStartSpanArgs) (*OtelStartSpanReturn, error) {
	var pCtx = context.Background()
	var ddOpts []tracer.StartSpanOption
	if pid := args.GetParentId(); pid != 0 {
		parent, ok := s.otelSpans[pid]
		if ok {
			pCtx = tracer.ContextWithSpan(context.Background(), parent.(ddtrace.Span))
		}
	}
	var otelOpts = []otel_trace.SpanStartOption{
		otel_trace.WithSpanKind(otel_trace.ValidateSpanKind(otel_trace.SpanKind(args.GetSpanKind()))),
	}
	if t := args.GetTimestamp(); t != 0 {
		tm := time.UnixMicro(t)
		otelOpts = append(otelOpts, otel_trace.WithTimestamp(tm))
	}
	if args.GetAttributes() != nil {
		for k, lv := range args.GetAttributes().KeyVals {
			n := len(lv.GetVal())
			if n == 0 {
				continue
			}
			// all values are represented as slices
			first := lv.GetVal()[0]
			switch first.Val.(type) {
			case *AttrVal_StringVal:
				inp := make([]string, n)
				for i, v := range lv.GetVal() {
					inp[i] = v.GetStringVal()
				}
				if len(inp) > 1 {
					otelOpts = append(otelOpts, otel_trace.WithAttributes(attribute.StringSlice(k, inp)))
				} else {
					otelOpts = append(otelOpts, otel_trace.WithAttributes(attribute.String(k, inp[0])))
				}
			case *AttrVal_BoolVal:
				inp := make([]bool, n)
				for i, v := range lv.GetVal() {
					inp[i] = v.GetBoolVal()
				}
				if len(inp) > 1 {
					otelOpts = append(otelOpts, otel_trace.WithAttributes(attribute.BoolSlice(k, inp)))
				} else {
					otelOpts = append(otelOpts, otel_trace.WithAttributes(attribute.Bool(k, inp[0])))
				}
			case *AttrVal_DoubleVal:
				inp := make([]float64, n)
				for i, v := range lv.GetVal() {
					inp[i] = v.GetDoubleVal()
				}
				if len(inp) > 1 {
					otelOpts = append(otelOpts, otel_trace.WithAttributes(attribute.Float64Slice(k, inp)))
				} else {
					otelOpts = append(otelOpts, otel_trace.WithAttributes(attribute.Float64(k, inp[0])))
				}
			case *AttrVal_IntegerVal:
				inp := make([]int64, n)
				for i, v := range lv.GetVal() {
					inp[i] = v.GetIntegerVal()
				}
				if len(inp) > 1 {
					otelOpts = append(otelOpts, otel_trace.WithAttributes(attribute.Int64Slice(k, inp)))
				} else {
					otelOpts = append(otelOpts, otel_trace.WithAttributes(attribute.Int64(k, inp[0])))
				}
			}
		}
	}
	if args.GetHttpHeaders() != nil && len(args.HttpHeaders.HttpHeaders) != 0 {
		headers := map[string]string{}
		for _, headerTuple := range args.HttpHeaders.HttpHeaders {
			k := headerTuple.GetKey()
			v := headerTuple.GetValue()
			if k != "" && v != "" {
				headers[k] = v
			}
		}
		sctx, err := tracer.NewPropagator(nil).Extract(tracer.TextMapCarrier(headers))
		if err != nil {
			fmt.Println("failed in StartSpan", err, args.HttpHeaders.HttpHeaders)
		} else {
			ddOpts = append(ddOpts, tracer.ChildOf(sctx))
		}
	}
	_, span := s.tracer.Start(ddotel.ContextWithStartOptions(pCtx, ddOpts...), args.Name, otelOpts...)
	hexSpanId := hex2int(span.SpanContext().SpanID().String())
	s.otelSpans[hexSpanId] = span
	return &OtelStartSpanReturn{
		SpanId:  hexSpanId,
		TraceId: hex2int(span.SpanContext().TraceID().String()),
	}, nil
}

func (s *apmClientServer) OtelEndSpan(ctx context.Context, args *OtelEndSpanArgs) (*OtelEndSpanReturn, error) {
	span, ok := s.otelSpans[args.Id]
	if !ok {
		fmt.Sprintf("OtelEndSpan call failed, span with id=%s not found", args.Id)
	}
	endOpts := []otel_trace.SpanEndOption{}
	if t := args.GetTimestamp(); t != 0 {
		tm := time.UnixMicro(t)
		endOpts = append(endOpts, otel_trace.WithTimestamp(tm))
	}
	span.End(endOpts...)
	return &OtelEndSpanReturn{}, nil
}

func (s *apmClientServer) OtelSetAttributes(ctx context.Context, args *OtelSetAttributesArgs) (*OtelSetAttributesReturn, error) {
	span, ok := s.otelSpans[args.SpanId]
	if !ok {
		fmt.Sprintf("OtelSetAttributes call failed, span with id=%s not found", args.SpanId)
	}
	for k, lv := range args.Attributes.KeyVals {
		n := len(lv.GetVal())
		if n == 0 {
			continue
		}
		// all values are represented as slices
		first := lv.GetVal()[0]
		switch first.Val.(type) {
		case *AttrVal_StringVal:
			inp := make([]string, n)
			for i, v := range lv.GetVal() {
				inp[i] = v.GetStringVal()
			}
			if len(inp) > 1 {
				span.SetAttributes(attribute.StringSlice(k, inp))
			} else {
				span.SetAttributes(attribute.String(k, inp[0]))
			}
		case *AttrVal_BoolVal:
			inp := make([]bool, n)
			for i, v := range lv.GetVal() {
				inp[i] = v.GetBoolVal()
			}
			if len(inp) > 1 {
				span.SetAttributes(attribute.BoolSlice(k, inp))
			} else {
				span.SetAttributes(attribute.Bool(k, inp[0]))
			}
		case *AttrVal_DoubleVal:
			inp := make([]float64, n)
			for i, v := range lv.GetVal() {
				inp[i] = v.GetDoubleVal()
			}
			if len(inp) > 1 {
				span.SetAttributes(attribute.Float64Slice(k, inp))
			} else {
				span.SetAttributes(attribute.Float64(k, inp[0]))
			}
		case *AttrVal_IntegerVal:
			inp := make([]int64, n)
			for i, v := range lv.GetVal() {
				inp[i] = v.GetIntegerVal()
			}
			if len(inp) > 1 {
				span.SetAttributes(attribute.Int64Slice(k, inp))
			} else {
				span.SetAttributes(attribute.Int64(k, inp[0]))
			}
		}

	}
	return &OtelSetAttributesReturn{}, nil
}

func (s *apmClientServer) OtelSetName(ctx context.Context, args *OtelSetNameArgs) (*OtelSetNameReturn, error) {
	span, ok := s.otelSpans[args.SpanId]
	if !ok {
		fmt.Sprintf("OtelSetName call failed, span with id=%s not found", args.SpanId)
	}
	span.SetName(args.Name)
	return &OtelSetNameReturn{}, nil
}

func (s *apmClientServer) OtelFlushSpans(ctx context.Context, args *OtelFlushSpansArgs) (*OtelFlushSpansReturn, error) {
	s.otelSpans = make(map[uint64]otel_trace.Span)
	success := false
	s.tp.ForceFlush(time.Duration(args.Seconds)*time.Second, func(ok bool) { success = ok })
	return &OtelFlushSpansReturn{Success: success}, nil
}

func (s *apmClientServer) OtelFlushTraceStats(context.Context, *OtelFlushTraceStatsArgs) (*OtelFlushTraceStatsReturn, error) {
	s.otelSpans = make(map[uint64]otel_trace.Span)
	return &OtelFlushTraceStatsReturn{}, nil
}

func (s *apmClientServer) OtelIsRecording(ctx context.Context, args *OtelIsRecordingArgs) (*OtelIsRecordingReturn, error) {
	span, ok := s.otelSpans[args.SpanId]
	if !ok {
		fmt.Printf("OtelIsRecording call failed, span with id=%s not found", args.SpanId)
	}
	return &OtelIsRecordingReturn{IsRecording: span.IsRecording()}, nil
}

func (s *apmClientServer) OtelSpanContext(ctx context.Context, args *OtelSpanContextArgs) (*OtelSpanContextReturn, error) {
	span, ok := s.otelSpans[(args.SpanId)]
	if !ok {
		fmt.Printf("OtelSpanContext call failed, span with id=%s not found", args.SpanId)
	}
	sctx := span.SpanContext()
	return &OtelSpanContextReturn{
		SpanId:     sctx.SpanID().String(),
		TraceId:    sctx.TraceID().String(),
		TraceFlags: sctx.TraceFlags().String(),
		TraceState: sctx.TraceState().String(),
		Remote:     sctx.IsRemote(),
	}, nil
}

func (s *apmClientServer) OtelSetStatus(ctx context.Context, args *OtelSetStatusArgs) (*OtelSetStatusReturn, error) {
	span, ok := s.otelSpans[args.SpanId]
	if !ok {
		fmt.Sprintf("OtelSetStatus call failed, span with id=%d not found", args.SpanId)
	}
	switch args.Code {
	case "UNSET":
		span.SetStatus(codes.Unset, args.Description)
	case "ERROR":
		span.SetStatus(codes.Error, args.Description)
	case "OK":
		span.SetStatus(codes.Ok, args.Description)
	default:
		fmt.Sprintf("Invalid code")
	}
	return &OtelSetStatusReturn{}, nil
}

func hex2int(hexStr string) uint64 {
	// remove 0x suffix if found in the input string
	cleaned := strings.Replace(hexStr, "0x", "", -1)

	// base 16 for hexadecimal
	result, err := strconv.ParseUint(cleaned, 16, 64)
	if err != nil {
		fmt.Printf("Converting hex string to uint64 failed, hex string : %s\n", hexStr)
	}
	return result
}
