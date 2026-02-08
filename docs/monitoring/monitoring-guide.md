# Monitoring Guide

This guide explains how to use CloudWatch dashboards, metrics, and logs to monitor the Leanda NG platform.

## Overview

The Leanda NG platform uses AWS CloudWatch for comprehensive monitoring:
- **CloudWatch Dashboards**: Visualize metrics and logs
- **CloudWatch Alarms**: Automated alerting on thresholds
- **CloudWatch Logs**: Centralized logging from all services
- **X-Ray**: Distributed tracing across services
- **Container Insights**: ECS task-level metrics

---

## CloudWatch Dashboards

### Main Dashboard

**Location**: CloudWatch → Dashboards → `leanda-ng-main-{environment}`

The main dashboard provides an overview of:
- Service health status
- Key metrics across all services
- Recent alerts and incidents

### Service-Specific Dashboards

**Location**: CloudWatch → Dashboards → `leanda-ng-{service}-{environment}`

Each service has its own dashboard with:
- **CPU Utilization**: Average CPU usage over time
- **Memory Utilization**: Average memory usage over time
- **Request Count**: Number of requests per minute
- **Error Rate**: Percentage of failed requests
- **Latency**: Response time percentiles (p50, p95, p99)

**Available Service Dashboards**:
- `leanda-ng-core-api-{environment}`
- `leanda-ng-blob-storage-{environment}`
- `leanda-ng-indexing-{environment}`
- `leanda-ng-metadata-processing-{environment}`
- `leanda-ng-chemical-parser-{environment}`
- `leanda-ng-chemical-properties-{environment}`
- `leanda-ng-reaction-parser-{environment}`
- `leanda-ng-crystal-parser-{environment}`
- `leanda-ng-spectra-parser-{environment}`
- `leanda-ng-imaging-{environment}`
- `leanda-ng-office-processor-{environment}`

### Business Metrics Dashboard

**Location**: CloudWatch → Dashboards → `leanda-ng-business-metrics-{environment}`

Tracks business-level metrics:
- File uploads per hour/day
- Processing job completion rates
- Parser success/failure rates
- Data processing throughput

### Performance Dashboard

**Location**: CloudWatch → Dashboards → `leanda-ng-performance-{environment}`

Tracks performance metrics:
- Latency percentiles (p50, p95, p99)
- Throughput metrics
- Error rates
- Request rates

---

## CloudWatch Metrics

### ECS Service Metrics

**Namespace**: `AWS/ECS`

**Key Metrics**:
- `CPUUtilization`: Average CPU utilization percentage
- `MemoryUtilization`: Average memory utilization percentage
- `RunningTaskCount`: Number of running tasks
- `DesiredTaskCount`: Desired number of tasks

**Dimensions**:
- `ServiceName`: `leanda-ng-{service}-{environment}`
- `ClusterName`: `leanda-ng-cluster-{environment}`

### Application Load Balancer Metrics

**Namespace**: `AWS/ApplicationELB`

**Key Metrics**:
- `RequestCount`: Number of requests
- `TargetResponseTime`: Response time from targets
- `HTTPCode_Target_2XX_Count`: Successful responses
- `HTTPCode_Target_4XX_Count`: Client errors
- `HTTPCode_Target_5XX_Count`: Server errors

**Dimensions**:
- `TargetGroup`: `leanda-ng-{service}-tg-{environment}`
- `LoadBalancer`: `leanda-ng-alb-{environment}`

### DocumentDB Metrics

**Namespace**: `AWS/DocDB`

**Key Metrics**:
- `CPUUtilization`: CPU utilization percentage
- `DatabaseConnections`: Number of database connections
- `ReadLatency`: Read operation latency
- `WriteLatency`: Write operation latency

**Dimensions**:
- `DBClusterIdentifier`: `leanda-ng-docdb-{environment}`

### ElastiCache Redis Metrics

**Namespace**: `AWS/ElastiCache`

**Key Metrics**:
- `CPUUtilization`: CPU utilization percentage
- `DatabaseMemoryUsagePercentage`: Memory usage percentage
- `Evictions`: Number of evicted keys
- `CacheHits`: Number of cache hits
- `CacheMisses`: Number of cache misses

**Dimensions**:
- `CacheClusterId`: `leanda-ng-redis-{environment}`

### MSK Metrics

**Namespace**: `AWS/Kafka`

**Key Metrics**:
- `SumOffsetLag`: Total consumer lag across all partitions
- `BytesInPerSec`: Incoming message rate
- `BytesOutPerSec`: Outgoing message rate

**Dimensions**:
- `ClusterName`: `leanda-ng-msk-{environment}`

### S3 Metrics

**Namespace**: `AWS/S3`

**Key Metrics**:
- `BucketSizeBytes`: Total bucket size
- `NumberOfObjects`: Number of objects in bucket
- `4xxErrors`: Client error count
- `5xxErrors`: Server error count

**Dimensions**:
- `BucketName`: `leanda-ng-data-{environment}-{account-id}`
- `StorageType`: `StandardStorage`, `IntelligentTiering`, etc.

---

## CloudWatch Logs

### Log Groups

All services log to CloudWatch Logs with the following structure:

**Service Logs**: `/aws/leanda-ng/services/{service}/{environment}`

**ECS Logs**: `/ecs/leanda-ng-{environment}`

### Log Retention

- **Production**: 1 year
- **Staging**: 1 week
- **Development**: 1 week

### Log Queries

Use CloudWatch Logs Insights to query logs:

**Error Analysis**:
```
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 100
```

**Performance Analysis**:
```
fields @timestamp, duration
| stats avg(duration), max(duration), min(duration) by bin(5m)
```

**Service-Specific Errors**:
```
fields @timestamp, @message, service
| filter service = "core-api" and @message like /ERROR/
| sort @timestamp desc
| limit 100
```

---

## OpenTelemetry Distributed Tracing

### Overview

The Leanda NG platform uses OpenTelemetry (OTel) as the vendor-neutral standard for distributed tracing. All services export traces via OTLP (OpenTelemetry Protocol) to CloudWatch Application Signals, while maintaining X-Ray compatibility.

### Configuration

All services are configured with:
- **OTLP Endpoint**: Configured via `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable
- **Protocol**: gRPC (default)
- **Service Name**: Automatically set from `quarkus.application.name`
- **Resource Attributes**: Service name and version included in all traces

### Trace Context Propagation

OpenTelemetry automatically propagates trace context via:
- **HTTP Headers**: W3C Trace Context headers (`traceparent`, `tracestate`)
- **Kafka Headers**: Trace context included in Kafka message headers
- **MDC (Mapped Diagnostic Context)**: Trace IDs available in logs via `LoggingUtils`

### Viewing Traces

**Location**: CloudWatch → Application Signals → Traces

OpenTelemetry traces are automatically discovered and displayed in CloudWatch Application Signals:
- Service map visualization
- Trace details with spans
- Error analysis
- Latency percentiles

### Integration with X-Ray

Both OpenTelemetry and X-Ray traces are exported:
- **OpenTelemetry**: Primary standard for vendor-neutral observability
- **X-Ray**: Maintained for compatibility with existing tooling
- **Dual Export**: Services export to both systems simultaneously

---

## Structured Logging with Correlation IDs

### Overview

All services use structured JSON logging with correlation IDs for log-trace correlation. This enables tracing requests across services by correlating logs with traces.

### Log Format

All log entries are in JSON format with the following structure:
```json
{
  "timestamp": "2025-01-15T10:00:00.000Z",
  "level": "INFO",
  "service": "core-api",
  "correlationId": "550e8400-e29b-41d4-a716-446655440000",
  "traceId": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
  "spanId": "00f067aa0ba902b7",
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "message": "Processing request",
  "logger": "io.leanda.coreapi.services.UserService",
  "thread": "executor-thread-1"
}
```

### Correlation ID Propagation

Correlation IDs are propagated through:
1. **Events**: All domain events include `correlationId` field
2. **Logs**: Correlation IDs set in MDC via `LoggingUtils.setCorrelationId()`
3. **Traces**: Correlation IDs included as trace attributes

### Using LoggingUtils

Services should use `shared/utils/LoggingUtils` to set correlation IDs:

```java
import io.leanda.shared.utils.LoggingUtils;
import java.util.UUID;

// Set correlation ID from event
LoggingUtils.setCorrelationId(event.getCorrelationId());

// Set user ID
LoggingUtils.setUserId(event.getUserId());

// Log entry will automatically include correlation ID and user ID
LOG.infof("Processing event: %s", eventId);

// Clear request context after processing
LoggingUtils.clearRequestContext();
```

### Log Queries with Correlation IDs

Use CloudWatch Logs Insights to query logs by correlation ID:

```sql
fields @timestamp, @message, service, correlationId, traceId
| filter correlationId = "550e8400-e29b-41d4-a716-446655440000"
| sort @timestamp asc
```

### Log Retention

- **Production**: 1 year
- **Staging**: 1 week
- **Development**: 1 week

---

## Event Observability (MELT - Events Pillar)

### Overview

Event observability provides visibility into Kafka event publishing and consumption, completing the MELT observability model (Metrics, Logs, Traces, Events).

### Event Dashboard

**Location**: CloudWatch → Dashboards → `leanda-ng-events-{environment}`

The event observability dashboard includes:
- **Events Published per Topic**: Line chart showing event publishing rate
- **Events Consumed per Topic**: Line chart showing event consumption rate
- **Event Processing Latency**: p50, p95, p99 percentiles
- **Event Error Rate**: Percentage of failed event processing
- **MSK Consumer Lag**: Consumer lag per topic

### Event Metrics

Services publish event metrics to CloudWatch custom metrics namespace `LeandaNG/Events`:

- **Published**: Count of events published per topic
- **Consumed**: Count of events consumed per topic
- **ProcessingTime**: Time to process events (milliseconds)
- **Errors**: Count of event processing errors

**Dimensions**:
- `Service`: Service name (e.g., `core-api`, `blob-storage`)
- `EventType`: Event type (e.g., `FilePersisted`, `UserCreated`)
- `Topic`: Kafka topic name
- `Environment`: Environment name (e.g., `production`, `staging`)

### Event Alarms

- **Event Error Rate High**: Triggers when event error rate > 1% for 5 minutes (P2 - Warning)
- **Consumer Lag High**: Already exists, enhanced with event context (P2 - Warning)

### Publishing Event Metrics

Services should publish event metrics when publishing/consuming events:

```java
// Example: Publish event metric (to be implemented in EventPublisher classes)
cloudWatch.putMetricData(PutMetricDataRequest.builder()
    .namespace("LeandaNG/Events")
    .metricData(MetricDatum.builder()
        .metricName("Published")
        .value(1.0)
        .dimensions(
            Dimension.builder().name("Service").value("core-api").build(),
            Dimension.builder().name("EventType").value("UserCreated").build(),
            Dimension.builder().name("Topic").value("user-events").build()
        )
        .timestamp(Instant.now())
        .build())
    .build());
```

---

## Prometheus Metrics

### Overview

All services expose Prometheus-compatible metrics endpoints alongside CloudWatch metrics, enabling integration with standard observability tooling.

### Metrics Endpoint

**Location**: `http://{service-host}:{port}/metrics`

All services expose metrics in Prometheus format at `/metrics` endpoint:
- **Format**: Prometheus text format
- **Authentication**: Public access (health endpoints)
- **Content**: Micrometer metrics (JVM, HTTP, custom)

### Available Metrics

Standard Micrometer metrics include:
- **JVM Metrics**: Memory, GC, threads, class loading
- **HTTP Metrics**: Request count, latency, error rate
- **Custom Metrics**: Business metrics (to be added by services)

### Example Metrics

```
# HELP http_server_requests_seconds Duration of HTTP server requests
# TYPE http_server_requests_seconds summary
http_server_requests_seconds_count{method="GET",status="200",uri="/health/live"} 100.0
http_server_requests_seconds_sum{method="GET",status="200",uri="/health/live"} 0.5

# HELP jvm_memory_used_bytes Amount of used memory
# TYPE jvm_memory_used_bytes gauge
jvm_memory_used_bytes{area="heap",id="PS Survivor Space"} 1.048576E7
```

### CloudWatch Integration

CloudWatch Container Insights can scrape Prometheus endpoints:
- Automatic discovery of `/metrics` endpoints
- Aggregation of metrics across services
- Integration with CloudWatch dashboards

---

## CloudWatch Application Signals (APM)

### Overview

CloudWatch Application Signals provides advanced Application Performance Monitoring (APM) capabilities, including automatic service discovery, service maps, and SLO tracking.

### Service Discovery

Application Signals automatically discovers services when they:
1. Export traces via OpenTelemetry with proper resource attributes
2. Include `service.name` in OpenTelemetry resource attributes
3. Run in ECS with Container Insights enabled

**Service Names** (automatically discovered):
- `core-api`
- `blob-storage`
- `indexing`
- `metadata-processing`
- `chemical-parser`
- `chemical-properties`
- `reaction-parser`
- `crystal-parser`
- `spectra-parser`
- `imaging`
- `office-processor`

### Service Map

**Location**: CloudWatch → Application Signals → Service Map

The service map visualizes:
- Service dependencies and relationships
- Request flows between services
- Error rates and latency per service
- Database and external service dependencies

### Service-Level Objectives (SLOs)

SLOs are defined for each service:
- **Availability**: 99.9% (less than 43 minutes downtime per month)
- **Latency**: p95 < 500ms for 95% of requests
- **Error Rate**: < 0.1% error rate

**Error Budget Tracking**:
- Error budgets tracked automatically
- Alerts when error budget consumed > 50% or > 80%
- Error budget dashboards available in Application Signals

### Anomaly Detection

CloudWatch Application Signals includes:
- Automatic anomaly detection for key metrics
- Predictive alerting based on ML models
- Reduced false positives compared to threshold-based alerts

---

## X-Ray Distributed Tracing

### Service Map

**Location**: X-Ray → Service Map

The service map visualizes:
- Service dependencies
- Request flow between services
- Error rates and latency per service

### Traces

**Location**: X-Ray → Traces

View individual traces to:
- Identify slow operations
- Debug errors
- Understand request flow

### Sampling Rules

X-Ray uses sampling rules to balance cost and visibility:
- **Errors**: 100% sampling (all errors are traced)
- **Success**: 10% sampling (10% of successful requests)

### Custom Segments

Services can add custom segments for:
- Database queries
- External API calls
- Business operations

---

## Container Insights

### Task-Level Metrics

**Location**: CloudWatch → Container Insights → Performance Monitoring

Container Insights provides:
- CPU and memory utilization per task
- Network I/O per task
- Storage I/O per task

### Service-Level Aggregations

Container Insights aggregates metrics at the service level:
- Average CPU/memory across all tasks
- Task count and health status
- Resource utilization trends

---

## Custom Metrics

### Publishing Custom Metrics

Services can publish custom CloudWatch metrics using the AWS SDK:

**Java Example**:
```java
CloudWatchClient cloudWatch = CloudWatchClient.builder()
    .region(Region.US_EAST_1)
    .build();

PutMetricDataRequest request = PutMetricDataRequest.builder()
    .namespace("LeandaNG/Business")
    .metricData(MetricDatum.builder()
        .metricName("FileUploads")
        .value(1.0)
        .dimensions(
            Dimension.builder().name("Service").value("blob-storage").build(),
            Dimension.builder().name("Format").value("sdf").build()
        )
        .timestamp(Instant.now())
        .build())
    .build();

cloudWatch.putMetricData(request);
```

### Metric Dimensions

Use dimensions to filter and aggregate metrics:
- `Service`: Service name (e.g., `core-api`, `blob-storage`)
- `Environment`: Environment name (e.g., `production`, `staging`)
- `Format`: File format (e.g., `sdf`, `mol`, `cif`)
- `User`: User identifier (for user-specific metrics)

---

## Alerting

### Alert Severity Levels

- **P1 (Critical)**: Immediate response required
- **P2 (Warning)**: Response within 1 hour
- **P3 (Info)**: Response within 24 hours

### SNS Topics

Alerts are sent to SNS topics:
- **Critical Alerts**: `leanda-ng-alerts-critical-{environment}`
- **Warning Alerts**: `leanda-ng-alerts-warning-{environment}`
- **Info Alerts**: `leanda-ng-alerts-info-{environment}`

### Alarm Actions

Alarms can trigger:
- SNS notifications
- Auto Scaling actions
- Lambda function invocations

---

## Service-Level Objectives (SLOs)

### SLO Definitions

Each service has defined SLOs:

**Availability**: 99.9% (less than 43 minutes downtime per month)
**Latency**: p95 < 500ms for 95% of requests
**Error Rate**: < 0.1% error rate

### Error Budget Tracking

Error budgets are tracked in CloudWatch:
- **Error Budget**: 100% - SLO target
- **Consumed Budget**: Actual error rate / Error budget
- **Alerts**: Triggered when error budget consumed > 50% or > 80%

---

## Best Practices

### Dashboard Usage

1. **Regular Review**: Check dashboards daily for trends
2. **Baseline Establishment**: Establish baseline metrics during normal operation
3. **Anomaly Detection**: Watch for deviations from baseline
4. **Correlation**: Correlate metrics across services

### Log Analysis

1. **Structured Logging**: Use structured logging (JSON format)
2. **Correlation IDs**: Include correlation IDs in all log entries
3. **Log Levels**: Use appropriate log levels (ERROR, WARN, INFO, DEBUG)
4. **Sensitive Data**: Never log sensitive data (PII, credentials)

### Metric Publishing

1. **Business Metrics**: Publish business metrics for visibility
2. **Cost Awareness**: Be mindful of CloudWatch costs (custom metrics)
3. **Dimension Strategy**: Use dimensions strategically for filtering
4. **Metric Math**: Use metric math for derived metrics

---

## Troubleshooting

### High CPU Utilization

1. Check CloudWatch dashboard for CPU trends
2. Review Container Insights for task-level metrics
3. Check application logs for CPU-intensive operations
4. Consider scaling out or optimizing code

### High Memory Utilization

1. Check CloudWatch dashboard for memory trends
2. Review Container Insights for task-level metrics
3. Check for memory leaks (gradual increase over time)
4. Consider scaling out or increasing task memory

### High Error Rate

1. Check CloudWatch logs for error patterns
2. Review X-Ray traces for failed requests
3. Check database connectivity and health
4. Review recent deployments or configuration changes

### Slow Response Times

1. Check latency metrics in dashboards
2. Review X-Ray traces for slow operations
3. Check database query performance
4. Review downstream service dependencies

---

## Additional Resources

- [AWS CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
- [AWS X-Ray Documentation](https://docs.aws.amazon.com/xray/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [CloudWatch Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Signals.html)
- [Prometheus Metrics Format](https://prometheus.io/docs/instrumenting/exposition_formats/)
- [Alerting Runbook](./alerting-runbook.md)
- [Service-Level Objectives](./slo-definitions.md)
- [Best Practices](./best-practices.md)
- [Observability Architecture ADR](../adr/0011-observability-architecture.md)

---

**Last Updated**: 2025-01-15

