### Overview of Observability in Modern Systems

In cloud serverless and Kubernetes (K8s) microservice-based architectures, observability encompasses the ability to understand system behavior through external outputs, enabling proactive issue detection, performance optimization, and efficient debugging. This goes beyond traditional monitoring by integrating metrics, logs, traces, and sometimes events (MELT) to provide a holistic view. Cutting-edge practices emphasize vendor-neutral standards, automation, and AI-driven insights to handle the dynamic, ephemeral nature of these environments.

### Core Pillars of Observability

Observability relies on three primary pillars, often extended to include events:

- **Metrics**: Quantitative data on system health, such as CPU usage, latency, error rates, and throughput. They provide high-level overviews and are essential for alerting on thresholds.
- **Logs**: Timestamped records of events, offering detailed context for debugging. Structured logs (e.g., JSON) with correlation IDs are key for tracing issues across services.
- **Traces**: End-to-end views of request paths through distributed systems, highlighting bottlenecks and dependencies.
- **Events**: Discrete occurrences like pod creations or failures, useful for auditing and real-time notifications.

Unified platforms that correlate these signals in a single interface are recommended for faster root cause analysis.

### Best Practices for Logging

Logging in microservices must address distributed, high-volume data without overwhelming storage. Key practices include:

- **Structured Logging**: Use JSON or key-value formats instead of plain text. Include contextual fields like trace IDs, span IDs, user IDs, request IDs, and log levels (DEBUG, INFO, WARN, ERROR, FATAL) for easy querying and correlation.
- **Centralized Aggregation**: Collect logs from all services into a single platform using agents like Fluentd or Fluent Bit (run as DaemonSets in K8s). Avoid local storage; route to tools like Elasticsearch or managed services for indexing and search.
- **Data Minimization and Security**: Mask sensitive information (e.g., PII, tokens) and implement retention policies to balance compliance with cost. Use log rotation to prevent disk exhaustion.
- **Context Enrichment**: Add correlation IDs to link logs across services, enabling quick navigation from errors to related traces.
- **For Serverless**: Capture logs during short execution windows with cloud-native tools like AWS CloudWatch or Azure Monitor, which handle ephemeral functions automatically.
- **For K8s**: Deploy lightweight collectors on every node to tail container logs before pods terminate.

These practices reduce noise and enable efficient analytics.

### Best Practices for Monitoring (Metrics and Alerts)

Monitoring focuses on real-time health checks and proactive alerting:

- **Key Metrics to Track**: Align with business KPIs, including the "Golden Signals" (latency, traffic, errors, saturation) plus resource utilization (CPU, memory, network). In K8s, monitor cluster-level (nodes, pods) and application-level metrics.
- **Collection and Visualization**: Use Prometheus for scraping metrics in K8s environments, paired with Grafana for dashboards. For serverless, leverage provider-specific metrics (e.g., invocation counts, cold starts).
- **Alerting and SLOs**: Define Service Level Objectives (SLOs) early (e.g., 99.9% availability) and set burn rate alerts. Integrate AI for anomaly detection to reduce false positives.
- **Auto-Scaling Integration**: Tie metrics to horizontal pod autoscaling in K8s or function scaling in serverless.
- **Cost Optimization**: Monitor telemetry data volume to avoid high costs; filter redundant data at the source.

Implement these with automated discovery for dynamic setups.

### Best Practices for Distributed Tracing

Tracing is crucial for understanding request flows in microservices:

- **Instrumentation**: Adopt OpenTelemetry (OTel) as the standard for automatic instrumentation across languages and services. It supports metrics, logs, and traces in one framework.
- **Context Propagation**: Use protocols like W3C Trace Context for propagating trace IDs across HTTP, gRPC, or message queues (e.g., RabbitMQ, Kafka).
- **Sampling and Analysis**: Apply head-based or tail-based sampling to manage data volume. Tools should provide service maps showing dependencies and latencies.
- **For Serverless**: Trace across function invocations, API gateways, and queues, handling cold starts with low-overhead agents.
- **For K8s**: Integrate with service meshes like Istio for automatic tracing without code changes.
- **eBPF Enhancement**: Use eBPF (extended Berkeley Packet Filter) for kernel-level visibility into network and system calls, ideal for low-overhead tracing in production.

Correlate traces with logs and metrics for unified debugging.

### Recommended Tools and Technologies

| Category | Tools for K8s | Tools for Serverless | Key Features |
|----------|---------------|----------------------|--------------|
| **Unified Platforms** | Datadog, Dynatrace, New Relic, Logz.io | AWS X-Ray, Azure Application Insights, Google Cloud Operations | AI insights, auto-discovery, MELT correlation |
| **Open-Source** | Prometheus + Grafana, Jaeger/Zipkin for traces, ELK Stack (Elasticsearch, Logstash, Kibana) | OpenTelemetry Collector, Honeycomb | Vendor-neutral, cost-effective, extensible |
| **Logging Collectors** | Fluent Bit (lightweight for nodes) | CloudWatch Logs, Fluentd | High-performance collection |
| **Advanced** | Splunk, Elastic Observability, Chronosphere | Edge Delta Telemetry Pipelines | Scalable analytics, cost control |

Choose based on scale: Open-source for flexibility, SaaS for managed ease.

### Environment-Specific Considerations

- **Cloud Serverless**: Focus on real-time data capture due to ephemeral functions. Use provider-native tools for seamless integration, but standardize with OTel to avoid vendor lock-in. Handle challenges like cold starts and variable scaling with anomaly detection.
- **K8s Microservices**: Emphasize cluster-wide visibility (pods, nodes, control plane). Deploy agents as sidecars or DaemonSets. Integrate with CI/CD for SLO validation when resumed (CI/CD postponed until full migration) and use service meshes for enhanced tracing.

### Emerging Trends in 2026

- **AI-Powered Observability**: Automated root cause analysis and predictive alerting.
- **Cross-Platform Consistency**: Unified tools for hybrid environments (virtualized, cloud-native).
- **Sustainability**: Optimize telemetry to reduce data costs and environmental impact.
- **Security Integration**: Embed observability in zero-trust models with encrypted traces and compliance-focused logging.

Adopting these practices ensures resilient, scalable systems with minimal downtime.

---

## Leanda NG Implementation

### Current Implementation Status

The Leanda NG platform implements modern observability best practices as follows:

#### OpenTelemetry Integration ✅

- **Status**: Enabled in all 11 services
- **Configuration**: OTLP export to CloudWatch Application Signals
- **Protocol**: gRPC
- **Service Discovery**: Automatic via OpenTelemetry resource attributes
- **X-Ray Compatibility**: Dual export maintained for compatibility

**Services Configured**:
- core-api, blob-storage, indexing, metadata-processing
- chemical-parser, chemical-properties, reaction-parser
- crystal-parser, spectra-parser, imaging, office-processor

#### Structured Logging ✅

- **Status**: JSON logging enabled in all services
- **Correlation IDs**: Propagated via `LoggingUtils` utility
- **MDC Context**: Trace ID, span ID, user ID, correlation ID in all logs
- **Log Format**: Structured JSON with contextual fields

**Shared Utility**: `shared/utils/LoggingUtils.java` provides MDC management

#### Event Observability ✅

- **Status**: Dashboard and metrics infrastructure created
- **Dashboard**: `leanda-ng-events-{environment}` CloudWatch dashboard
- **Metrics Namespace**: `LeandaNG/Events`
- **Metrics**: Published, Consumed, ProcessingTime, Errors
- **Alarms**: Event error rate alarm configured

**Note**: Event metrics publishing requires code changes in EventPublisher classes (future enhancement)

#### Prometheus Metrics ✅

- **Status**: `/metrics` endpoints enabled in all services
- **Format**: Prometheus text format
- **Registry**: Micrometer Prometheus registry
- **Integration**: CloudWatch Container Insights can scrape endpoints

#### CloudWatch Application Signals ✅

- **Status**: Automatic service discovery enabled
- **Service Map**: Automatic generation from OpenTelemetry traces
- **SLO Tracking**: Error budget tracking configured
- **Anomaly Detection**: ML-based anomaly detection enabled

### Architecture Decisions

See [ADR 0011: Observability Architecture](../adr/0011-observability-architecture.md) for detailed architecture decisions and trade-offs.

### Implementation Files

- **Infrastructure**: `infrastructure/lib/stacks/observability-stack.ts`
- **Shared Utilities**: `shared/utils/LoggingUtils.java`
- **Service Configuration**: `services/*/src/main/resources/application.properties`
- **Dependencies**: `services/*/pom.xml`

### Next Steps

1. **Event Metrics Publishing**: Add CloudWatch metrics publishing to EventPublisher classes
2. **Correlation ID Propagation**: Ensure all services use LoggingUtils for correlation IDs
3. **Custom Business Metrics**: Add business metrics to Prometheus endpoints
4. **SLO Dashboard**: Create SLO dashboards in CloudWatch Application Signals
