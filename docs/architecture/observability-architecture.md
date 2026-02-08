# Observability Architecture Diagram

**Status**: Current State  
**Last Updated**: 2025-01-15

## Overview

The Observability Architecture diagram shows how Leanda.io implements comprehensive observability using the MELT model (Metrics, Events, Logs, Traces).

## Observability Architecture Diagram

```mermaid
graph TD
    subgraph "Application Layer"
        Services[Microservices<br/>11 Java/Quarkus Services]
    end
    
    subgraph "Logging Layer"
        StructuredLogs[Structured Logs<br/>JSON Format]
        CloudWatchLogs[CloudWatch Logs<br/>Log Groups per Service]
        LogGroups[Log Groups<br/>/aws/leanda/services/{service}]
        LogRetention[Log Retention<br/>1 Year Production<br/>1 Week Development]
    end
    
    subgraph "Metrics Layer"
        CustomMetrics[Custom Metrics<br/>Business & Technical]
        CloudWatchMetrics[CloudWatch Metrics<br/>Namespace: LeandaNG]
        PrometheusMetrics[Prometheus Metrics<br/>Prometheus-Compatible]
        ContainerInsights[Container Insights<br/>ECS Metrics]
        ServiceMetrics[Service Metrics<br/>CPU, Memory, Request Count]
        BusinessMetrics[Business Metrics<br/>Files Uploaded, Searches, etc.]
    end
    
    subgraph "Tracing Layer"
        OpenTelemetry[OpenTelemetry<br/>Tracing Standard]
        XRay[X-Ray<br/>Distributed Tracing]
        ServiceMap[Service Map<br/>Automatic Discovery]
        Traces[Trace Analysis<br/>Request Flows]
        Sampling[Sampling Rules<br/>100% Errors, 10% Success]
    end
    
    subgraph "Events Layer"
        DomainEvents[Domain Events<br/>FileCreated, FileParsed, etc.]
        EventMetrics[Event Metrics<br/>Published, Consumed, Errors]
        EventDashboard[Event Dashboard<br/>CloudWatch Dashboard]
    end
    
    subgraph "Alerting Layer"
        CloudWatchAlarms[CloudWatch Alarms<br/>CPU, Memory, Error Rate]
        SNSTopics[SNS Topics<br/>P1, P2, P3 Alerts]
        EmailAlerts[Email Alerts<br/>P2, P3]
        PagerDuty[PagerDuty<br/>P1 Critical]
        Slack[Slack<br/>P2, P3]
    end
    
    subgraph "Dashboards Layer"
        CloudWatchDashboards[CloudWatch Dashboards<br/>Service-Specific]
        GrafanaDashboards[Grafana Dashboards<br/>Custom Visualizations]
        MainDashboard[Main Dashboard<br/>System Overview]
        ServiceDashboards[Service Dashboards<br/>Per-Service Metrics]
        BusinessDashboard[Business Dashboard<br/>Business Metrics]
        PerformanceDashboard[Performance Dashboard<br/>Latency, Throughput]
        EventDashboard2[Event Dashboard<br/>Event Metrics]
    end
    
    Services -->|"Emit Logs"| StructuredLogs
    StructuredLogs -->|"Send to"| CloudWatchLogs
    CloudWatchLogs -->|"Store in"| LogGroups
    LogGroups -->|"Retention"| LogRetention
    
    Services -->|"Emit Metrics"| CustomMetrics
    CustomMetrics -->|"Send to"| CloudWatchMetrics
    CustomMetrics -->|"Send to"| PrometheusMetrics
    Services -->|"ECS Metrics"| ContainerInsights
    ContainerInsights -->|"Send to"| CloudWatchMetrics
    Services -->|"Service Metrics"| ServiceMetrics
    Services -->|"Business Metrics"| BusinessMetrics
    ServiceMetrics --> CloudWatchMetrics
    BusinessMetrics --> CloudWatchMetrics
    
    Services -->|"Emit Traces"| OpenTelemetry
    OpenTelemetry -->|"Send to"| XRay
    XRay -->|"Generate"| ServiceMap
    XRay -->|"Analyze"| Traces
    XRay -->|"Apply"| Sampling
    
    Services -->|"Publish Events"| DomainEvents
    DomainEvents -->|"Track Metrics"| EventMetrics
    EventMetrics -->|"Display in"| EventDashboard
    
    CloudWatchMetrics -->|"Evaluate"| CloudWatchAlarms
    ServiceMetrics -->|"Evaluate"| CloudWatchAlarms
    BusinessMetrics -->|"Evaluate"| CloudWatchAlarms
    EventMetrics -->|"Evaluate"| CloudWatchAlarms
    
    CloudWatchAlarms -->|"Trigger"| SNSTopics
    SNSTopics -->|"P1 Alerts"| PagerDuty
    SNSTopics -->|"P2, P3 Alerts"| EmailAlerts
    SNSTopics -->|"P2, P3 Alerts"| Slack
    
    CloudWatchMetrics -->|"Visualize"| CloudWatchDashboards
    PrometheusMetrics -->|"Visualize"| GrafanaDashboards
    ServiceMetrics -->|"Visualize"| ServiceDashboards
    BusinessMetrics -->|"Visualize"| BusinessDashboard
    ServiceMetrics -->|"Visualize"| PerformanceDashboard
    EventMetrics -->|"Visualize"| EventDashboard2
    
    CloudWatchDashboards --> MainDashboard
    GrafanaDashboards --> MainDashboard
```

## Observability Pillars (MELT)

### Metrics

#### Technical Metrics
- **CPU Utilization**: Per-service CPU usage
- **Memory Utilization**: Per-service memory usage
- **Request Count**: API request counts
- **Error Rate**: 4xx, 5xx error rates
- **Latency**: p50, p95, p99 response times
- **Throughput**: Requests per second

#### Business Metrics
- **Files Uploaded**: Count of files uploaded
- **Searches Performed**: Search query count
- **Users Active**: Active user count
- **Processing Time**: File processing duration
- **Indexing Rate**: Documents indexed per hour

#### Infrastructure Metrics
- **Database Connections**: DocumentDB connection count
- **Cache Hit Rate**: Redis cache hit ratio
- **Queue Depth**: Kafka consumer lag
- **Storage Usage**: S3 bucket size

### Events

#### Domain Events
- **FileCreated**: File upload events
- **FileParsed**: File parsing completion
- **MetadataGenerated**: Metadata extraction completion
- **EntityIndexed**: Search indexing completion

#### Event Metrics
- **Events Published**: Count per topic
- **Events Consumed**: Count per consumer
- **Event Processing Time**: Time to process events
- **Event Error Rate**: Failed event processing

### Logs

#### Structured Logging
- **Format**: JSON
- **Fields**: timestamp, level, service, message, correlation_id, trace_id
- **Levels**: ERROR, WARN, INFO, DEBUG
- **Correlation**: Request IDs, trace IDs

#### Log Groups
- **Structure**: `/aws/leanda/services/{service}/{environment}`
- **Retention**: 1 year (production), 1 week (development)
- **Search**: CloudWatch Logs Insights

#### Log Content
- **Request Logs**: HTTP requests and responses
- **Error Logs**: Exceptions and stack traces
- **Business Logs**: Domain events and state changes
- **Audit Logs**: Security and access events

### Traces

#### Distributed Tracing
- **Standard**: OpenTelemetry
- **Service**: X-Ray
- **Coverage**: All microservices
- **Propagation**: HTTP headers, Kafka message attributes

#### Trace Information
- **Service Map**: Automatic service discovery
- **Request Flows**: End-to-end request tracing
- **Latency Breakdown**: Per-service latency
- **Error Tracking**: Failed request traces

#### Sampling
- **Errors**: 100% sampling
- **Success**: 10% sampling
- **Custom Rules**: Based on service, path, method

## Alerting

### Alert Severity Levels

#### P1 (Critical)
- **Response Time**: Immediate
- **Examples**: Service down, high error rate, security breach
- **Channel**: PagerDuty

#### P2 (Warning)
- **Response Time**: < 1 hour
- **Examples**: High CPU, memory pressure, degraded performance
- **Channel**: Email, Slack

#### P3 (Info)
- **Response Time**: < 24 hours
- **Examples**: Storage growth, capacity planning
- **Channel**: Email, Slack

### Alert Types

#### Service Health Alarms
- **CPU Utilization**: > 80% for 5 minutes
- **Memory Utilization**: > 80% for 5 minutes
- **Error Rate**: > 5% for 5 minutes
- **Health Check Failures**: > 3 consecutive failures

#### Database Alarms
- **DocumentDB CPU**: > 80% for 5 minutes
- **DocumentDB Connections**: > 80% of max
- **Redis Memory**: > 80% for 5 minutes
- **Redis Evictions**: > 0

#### Messaging Alarms
- **MSK Consumer Lag**: > 1000 messages
- **Event Error Rate**: > 1% for 5 minutes
- **Dead Letter Queue**: > 0 messages

#### Storage Alarms
- **S3 Bucket Size**: > 1TB
- **S3 Request Errors**: > 10 errors in 5 minutes

## Dashboards

### Main Dashboard
- **Purpose**: System overview
- **Metrics**: Overall health, request rates, error rates
- **Services**: All services status
- **Location**: CloudWatch

### Service Dashboards
- **Purpose**: Per-service monitoring
- **Metrics**: CPU, memory, request count, latency, errors
- **Services**: One dashboard per service
- **Location**: CloudWatch

### Business Dashboard
- **Purpose**: Business metrics
- **Metrics**: Files uploaded, searches, users active
- **Location**: CloudWatch

### Performance Dashboard
- **Purpose**: Performance metrics
- **Metrics**: Latency percentiles, throughput, cache hit rate
- **Location**: CloudWatch

### Event Dashboard
- **Purpose**: Event metrics
- **Metrics**: Events published, consumed, processing time, errors
- **Location**: CloudWatch

### Grafana Dashboards
- **Purpose**: Custom visualizations
- **Data Source**: Prometheus, CloudWatch
- **Features**: Custom queries, advanced visualizations

## Observability Best Practices

### Structured Logging
- **Format**: JSON for machine parsing
- **Fields**: Consistent field names
- **Correlation**: Request IDs, trace IDs
- **Levels**: Appropriate log levels

### Metrics Naming
- **Convention**: `namespace.metric_name.unit`
- **Examples**: `leanda.files.uploaded.count`, `leanda.api.latency.milliseconds`
- **Dimensions**: Service, environment, operation

### Trace Context
- **Propagation**: HTTP headers, message attributes
- **Correlation**: Trace IDs in logs and metrics
- **Sampling**: Balance cost and visibility

### Alert Tuning
- **Thresholds**: Based on SLOs
- **Evaluation Periods**: Prevent false positives
- **Suppression**: During maintenance windows

## Related Diagrams

- [Deployment Diagram](./deployment-diagram.md) - Infrastructure deployment
- [Security Architecture](./security-architecture.md) - Security monitoring
- [Integration Patterns](./integration-patterns.md) - Service communication

---

**Document Version**: 1.0
