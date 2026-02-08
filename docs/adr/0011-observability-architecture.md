# 0011. Observability Architecture - OpenTelemetry, Structured Logging, and Event Observability

## Status
Accepted

## Context

The Leanda NG platform requires comprehensive observability to monitor, debug, and optimize a distributed microservices architecture. The initial observability implementation (Agent PROD-3) provided CloudWatch dashboards, X-Ray tracing, and basic alarms, but lacked:

1. **Vendor-neutral observability standard**: Services used AWS X-Ray exclusively, creating vendor lock-in
2. **Structured logging with correlation IDs**: Logs lacked correlation IDs for cross-service tracing
3. **Event observability**: Kafka events were published but not tracked/observed (missing 4th pillar of MELT)
4. **Prometheus metrics**: Workspace rules required Prometheus-compatible endpoints, but they weren't implemented
5. **CloudWatch Application Signals**: Advanced APM capabilities were not enabled

Modern observability best practices (as documented in `docs/monitoring/best-practices.md`) recommend:
- OpenTelemetry (OTel) as vendor-neutral standard
- Structured JSON logging with correlation IDs
- Event observability as 4th pillar (MELT: Metrics, Logs, Traces, Events)
- Prometheus-compatible metrics endpoints
- CloudWatch Application Signals for advanced APM

## Decision

We will enhance the observability architecture with:

1. **OpenTelemetry Integration**:
   - Enable OpenTelemetry in all 11 services with OTLP export to CloudWatch
   - Maintain X-Ray compatibility (dual export) for existing tooling
   - Configure OTLP endpoint via environment variable (`OTEL_EXPORTER_OTLP_ENDPOINT`)
   - Use CloudWatch Application Signals to receive OTel traces

2. **Structured Logging with Correlation IDs**:
   - Enable JSON logging in all services (`quarkus.log.console.json=true`)
   - Create shared `LoggingUtils` utility for MDC (Mapped Diagnostic Context) management
   - Ensure correlation IDs propagate from events to log context
   - Include trace ID, span ID, user ID, service name in all log entries

3. **Event Observability (MELT - Events Pillar)**:
   - Create CloudWatch custom metrics namespace: `LeandaNG/Events`
   - Metrics: `Published`, `Consumed`, `ProcessingTime`, `Errors`
   - Create event observability dashboard with event flow visualization
   - Add event error rate alarms

4. **Prometheus Metrics**:
   - Add `quarkus-micrometer-registry-prometheus` to all services
   - Expose `/metrics` endpoint in Prometheus format
   - Enable alongside CloudWatch metrics (dual export)

5. **CloudWatch Application Signals**:
   - Leverage automatic service discovery via OpenTelemetry resource attributes
   - Configure service names and resource attributes for discovery
   - Enable service maps and SLO tracking

## Consequences

### Positive

- **Vendor-neutral observability**: OpenTelemetry provides flexibility to switch observability backends
- **Better debugging**: Correlation IDs enable tracing requests across services
- **Event visibility**: Event observability dashboard provides visibility into event-driven workflows
- **Standard metrics**: Prometheus endpoints enable integration with standard tooling
- **Advanced APM**: CloudWatch Application Signals provides service maps and SLO tracking
- **Compliance**: Aligns with workspace rules and modern best practices

### Negative

- **Additional dependencies**: Each service now includes OpenTelemetry and Prometheus dependencies
- **Configuration complexity**: Services require OTLP endpoint configuration
- **Cost**: CloudWatch Application Signals and custom metrics have associated costs
- **Maintenance**: Event metrics must be published by each service (requires code changes)

### Neutral

- **Dual export**: Both X-Ray and OpenTelemetry traces are exported (maintains compatibility)
- **Gradual adoption**: Event metrics publishing can be added incrementally per service

## Alternatives Considered

1. **X-Ray Only**:
   - Pros: Simpler, AWS-native
   - Cons: Vendor lock-in, no vendor-neutral standard
   - Rejected: Doesn't align with best practices for vendor-neutral observability

2. **OpenTelemetry Only (Remove X-Ray)**:
   - Pros: Single standard, simpler
   - Cons: Loses X-Ray compatibility, requires migration
   - Rejected: Maintains X-Ray for compatibility while adding OTel

3. **Prometheus Server**:
   - Pros: Full Prometheus ecosystem
   - Cons: Additional infrastructure, operational overhead
   - Rejected: CloudWatch can scrape Prometheus endpoints, no need for separate server

4. **Third-party APM (Datadog, New Relic)**:
   - Pros: Advanced features, managed service
   - Cons: Additional cost, vendor lock-in
   - Rejected: CloudWatch Application Signals provides sufficient APM capabilities

## Implementation Notes

- All 11 services updated with OpenTelemetry, Prometheus, and structured logging
- Shared `LoggingUtils` utility created in `shared/utils/`
- Event observability dashboard added to ObservabilityStack
- CloudWatch Application Signals leverages automatic service discovery
- Event metrics publishing requires code changes in EventPublisher classes (future enhancement)

## References

- `docs/monitoring/best-practices.md` - Modern observability best practices
- `docs/monitoring/monitoring-guide.md` - Monitoring guide with new features
- `.cursor/rules/09-observability-resilience.mdc` - Observability workspace rules
- `.cursor/rules/14-aws-monitoring.mdc` - AWS monitoring patterns
