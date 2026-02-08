# Leanda.io Cloud Architecture Design

**Status**: 🟢 In Progress  
**Last Updated**: 2025-12-27  
**Architect**: Agent PROD-0 (Cloud Architect)

## Executive Summary

This document provides a comprehensive cloud architecture design for Leanda.io, an open science data repository platform. The architecture is designed following AWS Well-Architected Framework principles and supports 11 microservices processing scientific data across multiple domains (chemical, crystal, spectra, imaging, documents).

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [AWS Well-Architected Framework Review](#aws-well-architected-framework-review)
3. [Service Architecture](#service-architecture)
4. [Scalability Design](#scalability-design)
5. [Performance Design](#performance-design)
6. [Disaster Recovery](#disaster-recovery)
7. [Security Architecture](#security-architecture)
8. [Cost Optimization](#cost-optimization)
9. [Integration Patterns](#integration-patterns)
10. [Deployment Strategy](#deployment-strategy)

---

## Architecture Overview

### Current State

Leanda.io consists of:
- **11 Java/Quarkus microservices** (core-api, blob-storage, 8 domain parsers, metadata-processing, indexing)
- **Event-driven architecture** using Kafka (MSK Serverless)
- **DocumentDB** for metadata storage (MongoDB-compatible)
- **OpenSearch** for search and indexing
- **S3** for blob storage
- **Redis** for caching
- **Angular 21 frontend**

### Target Architecture

The platform follows a **serverless-first, event-driven microservices architecture** on AWS:

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet / Users                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Amazon CloudFront + API Gateway                  │
│              (CDN + API Management + Auth)                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌──────────────────┐          ┌──────────────────┐
│  Angular 21      │          │  API Gateway    │
│  (Amplify Host)  │          │  (REST APIs)     │
└──────────────────┘          └────────┬─────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
        ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐
        │  ECS Fargate     │  │  Lambda      │  │  Step        │
        │  (Microservices) │  │  Functions   │  │  Functions   │
        └────────┬─────────┘  └──────┬───────┘  └──────┬───────┘
                 │                  │                  │
        ┌────────┴─────────┐        │                  │
        │                  │        │                  │
        ▼                  ▼        ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  MSK         │  │  EventBridge │  │  S3          │
│  (Kafka)     │  │  (Events)    │  │  (Storage)   │
└──────┬───────┘  └──────────────┘  └──────┬───────┘
       │                                    │
       │                                    │
       ▼                                    ▼
┌──────────────┐                  ┌──────────────┐
│  DocumentDB  │                  │  OpenSearch  │
│  (Metadata)  │                  │  (Search)    │
└──────────────┘                  └──────────────┘
```

### Key Design Principles

1. **Serverless-First**: Prefer managed services (ECS Fargate, Lambda, MSK Serverless) over self-managed
2. **Event-Driven**: Asynchronous communication via Kafka and EventBridge
3. **Multi-AZ Resilience**: All services deployed across 2+ availability zones
4. **Security by Design**: Least privilege IAM, encryption at rest and in transit
5. **Observability**: Comprehensive logging, metrics, and tracing
6. **Cost Optimization**: Right-sizing, auto-scaling, and pay-per-use services

---

## AWS Well-Architected Framework Review

### Pillar 1: Operational Excellence

#### Current State Assessment

✅ **Strengths**:
- Infrastructure as Code (CDK)
- Container-based deployment (ECS)
- Basic observability (CloudWatch)

⚠️ **Gaps**:
- No automated deployment pipelines (CI/CD postponed until full migration is complete)
- Limited runbooks and operational procedures
- No automated testing in production-like environments
- Limited incident response procedures

#### Recommendations

1. **CI/CD Pipeline** (Coordinate with PROD-2) — **CI/CD is postponed until full migration is complete.**
   - GitHub Actions → AWS CodePipeline
   - Automated testing (unit, integration, E2E)
   - Automated deployment to dev/staging/prod
   - Blue/Green deployments for zero-downtime

2. **Operational Runbooks**
   - Service startup/shutdown procedures
   - Database backup/restore procedures
   - Incident response playbooks
   - Rollback procedures

3. **Monitoring and Alerting** (Coordinate with PROD-3)
   - CloudWatch dashboards per service
   - SLO-based alerting (error rate, latency)
   - Automated incident detection
   - On-call rotation management

4. **Change Management**
   - Feature flags for gradual rollouts
   - Canary deployments
   - Automated rollback on health check failures

**Success Metrics**:
- Deployment frequency: Daily
- Mean time to recovery (MTTR): < 30 minutes
- Change failure rate: < 5%

### Pillar 2: Security

#### Current State Assessment

✅ **Strengths**:
- VPC with private subnets
- Security groups configured
- IAM roles for services
- S3 encryption enabled

⚠️ **Gaps**:
- No API authentication/authorization (API Gateway + Cognito)
- Secrets management not fully implemented
- No WAF protection
- Limited security monitoring (GuardDuty, Security Hub)
- No data encryption at application level

#### Recommendations

1. **Identity and Access Management** (Coordinate with PROD-4)
   - Amazon Cognito for user authentication
   - API Gateway with Cognito authorizers
   - IAM roles with least privilege
   - Service-to-service authentication via IAM roles

2. **Data Protection**
   - AWS KMS for encryption keys
   - Encryption at rest (S3, DocumentDB, EBS)
   - TLS 1.2+ for all communications
   - Secrets Manager for credentials

3. **Network Security**
   - VPC with private subnets only
   - Security groups with minimal rules
   - AWS WAF for API Gateway
   - VPC Flow Logs enabled

4. **Security Monitoring**
   - AWS GuardDuty for threat detection
   - AWS Security Hub for centralized findings
   - CloudTrail for API audit logging
   - AWS Config for compliance monitoring

**Success Metrics**:
- Zero critical security vulnerabilities
- 100% encrypted data at rest
- Security incidents: < 1 per quarter

### Pillar 3: Reliability

#### Current State Assessment

✅ **Strengths**:
- Multi-AZ VPC configuration
- DocumentDB with multi-AZ option
- ECS Fargate with auto-scaling capability

⚠️ **Gaps**:
- No disaster recovery plan
- No multi-region deployment
- Limited fault tolerance testing
- No automated backup/restore procedures

#### Recommendations

1. **Multi-AZ Deployment**
   - All services in 2+ availability zones
   - DocumentDB with 2+ instances (production)
   - Application Load Balancer for traffic distribution
   - Auto-scaling groups with AZ distribution

2. **Fault Tolerance**
   - Circuit breakers for external calls
   - Retry logic with exponential backoff
   - Dead letter queues for failed messages
   - Health checks and auto-recovery

3. **Disaster Recovery** (See [Disaster Recovery](#disaster-recovery))
   - RTO: 4 hours
   - RPO: 1 hour
   - Multi-region backup strategy
   - Automated failover procedures

4. **Backup and Restore**
   - Automated DocumentDB snapshots (daily)
   - S3 versioning and cross-region replication
   - Point-in-time recovery for DocumentDB
   - Regular restore testing

**Success Metrics**:
- Availability: 99.9% (3 nines)
- RTO: < 4 hours
- RPO: < 1 hour

### Pillar 4: Performance Efficiency

#### Current State Assessment

✅ **Strengths**:
- ECS Fargate for container orchestration
- MSK Serverless for auto-scaling messaging
- S3 for scalable storage

⚠️ **Gaps**:
- No caching layer (CloudFront, ElastiCache)
- No CDN for static assets
- Limited database query optimization
- No performance testing

#### Recommendations

1. **Compute Optimization**
   - Right-sizing ECS tasks (CPU/memory)
   - Auto-scaling based on CPU/memory/custom metrics
   - Graviton instances for 20-40% cost savings
   - Reserved capacity for predictable workloads

2. **Caching Strategy**
   - CloudFront for frontend assets
   - ElastiCache Redis for API response caching
   - Application-level caching (Quarkus cache)
   - Cache invalidation strategies

3. **Database Optimization**
   - DocumentDB read replicas for read-heavy workloads
   - Query optimization and indexing
   - Connection pooling
   - Database monitoring and slow query alerts

4. **Content Delivery**
   - CloudFront for static assets
   - S3 Transfer Acceleration for uploads
   - Regional endpoints for lower latency

**Success Metrics**:
- API response time: p95 < 500ms
- Frontend load time: < 2 seconds
- Database query time: p95 < 100ms

### Pillar 5: Cost Optimization

#### Current State Assessment

✅ **Strengths**:
- Serverless services (MSK Serverless, ECS Fargate)
- S3 lifecycle policies

⚠️ **Gaps**:
- No cost allocation tags
- No cost monitoring/alerting
- Limited right-sizing analysis
- No reserved capacity planning

#### Recommendations

1. **Cost Allocation** (Coordinate with PROD-5)
   - Resource tagging strategy (Project, Environment, Service, CostCenter)
   - Cost allocation reports by service/environment
   - Budget alerts and cost anomaly detection

2. **Right-Sizing**
   - Regular review of ECS task sizes
   - DocumentDB instance sizing optimization
   - S3 storage class optimization (Intelligent-Tiering)
   - Reserved capacity for predictable workloads

3. **Cost Monitoring**
   - AWS Cost Explorer dashboards
   - Budget alerts (daily, weekly, monthly)
   - Cost anomaly detection
   - Regular cost reviews

4. **Optimization Opportunities**
   - Use Graviton instances (20-40% savings)
   - S3 Intelligent-Tiering for automatic optimization
   - Spot instances for non-critical workloads
   - Savings Plans for committed usage

**Success Metrics**:
- Cost per user: Track and optimize
- Cost variance: < 10% month-over-month
- Reserved capacity coverage: 60%+ for predictable workloads

---

## Service Architecture

### Service Inventory

| Service | Type | Port | Dependencies | Scaling Strategy |
|---------|------|------|--------------|------------------|
| core-api | REST API | 8080 | MongoDB, Kafka | Auto-scale: CPU > 70% |
| blob-storage | REST API | 8084 | MongoDB, S3, Kafka | Auto-scale: Request count |
| chemical-parser | Event Consumer | 8083 | Blob Storage, Kafka | Auto-scale: Queue depth |
| chemical-properties | Event Consumer | 8086 | Blob Storage, Kafka | Auto-scale: Queue depth |
| reaction-parser | Event Consumer | 8087 | Blob Storage, Kafka | Auto-scale: Queue depth |
| crystal-parser | Event Consumer | 8089 | Blob Storage, Kafka | Auto-scale: Queue depth |
| spectra-parser | Event Consumer | 8090 | Blob Storage, Kafka | Auto-scale: Queue depth |
| imaging | Event Consumer | 8091 | Blob Storage, Kafka | Auto-scale: Queue depth |
| office-processor | Event Consumer | 8088 | Blob Storage, Kafka | Auto-scale: Queue depth |
| metadata-processing | Event Consumer | 8098 | MongoDB, Kafka | Auto-scale: Queue depth |
| indexing | Event Consumer | 8099 | OpenSearch, Kafka | Auto-scale: Queue depth |

### Service Deployment Pattern

All services follow a consistent deployment pattern:

1. **Container Image**: Built from Dockerfile, stored in ECR
2. **ECS Task Definition**: Defines CPU, memory, environment variables
3. **ECS Service**: Manages desired count, auto-scaling, load balancing
4. **Application Load Balancer**: Routes traffic to healthy tasks
5. **Service Discovery**: AWS Cloud Map for service-to-service communication

### Service Communication Patterns

1. **Synchronous**: REST APIs via API Gateway → ALB → ECS
2. **Asynchronous**: Kafka topics for event-driven communication
3. **Service Discovery**: AWS Cloud Map for internal service discovery

---

## Scalability Design

### Horizontal Scaling Strategy

#### Compute Scaling (ECS Fargate)

**Auto-Scaling Policies**:
- **Target Tracking**: CPU utilization 70%, Memory utilization 80%
- **Step Scaling**: Scale out on queue depth, scale in gradually
- **Scheduled Scaling**: Scale up during known peak hours

**Scaling Configuration**:
```typescript
// Example: core-api service
minCapacity: 2
maxCapacity: 20
targetCpuUtilization: 70
targetMemoryUtilization: 80
scaleInCooldown: 300s
scaleOutCooldown: 60s
```

#### Database Scaling (DocumentDB)

- **Read Replicas**: 2+ read replicas for read-heavy workloads
- **Instance Sizing**: Start with db.t3.medium, scale to db.r5.large as needed
- **Connection Pooling**: Configured at application level

#### Messaging Scaling (MSK Serverless)

- **Auto-Scaling**: MSK Serverless automatically scales based on throughput
- **Partition Strategy**: Partition topics by domain (chemical, crystal, etc.)
- **Consumer Groups**: One consumer group per service

### Vertical Scaling Strategy

- **ECS Tasks**: Start with 0.25 vCPU / 512MB, scale to 1 vCPU / 2GB as needed
- **DocumentDB**: Scale instance size during maintenance windows
- **OpenSearch**: Scale instance type or add nodes

### Data Partitioning Strategy

1. **S3 Buckets**: Partition by domain and date
   - `s3://leanda-data/chemical/2025/01/15/`
   - `s3://leanda-data/crystal/2025/01/15/`

2. **Kafka Topics**: Partition by domain
   - `chemical-file-created` (10 partitions)
   - `crystal-file-created` (10 partitions)

3. **DocumentDB Collections**: Shard by user ID or domain

---

## Performance Design

### Caching Strategy

#### Layer 1: CloudFront (CDN)
- **Purpose**: Static assets, API responses
- **TTL**: 1 hour for static, 5 minutes for API responses
- **Invalidation**: On deployment

#### Layer 2: ElastiCache Redis
- **Purpose**: API response caching, session storage
- **TTL**: 15 minutes for API responses, 24 hours for sessions
- **Eviction Policy**: LRU

#### Layer 3: Application Cache (Quarkus)
- **Purpose**: In-memory caching for frequently accessed data
- **TTL**: 5 minutes
- **Size**: 100MB per service instance

### Database Optimization

1. **Indexing Strategy**
   - Compound indexes on frequently queried fields
   - TTL indexes for time-based data
   - Text indexes for search fields

2. **Query Optimization**
   - Use projection to limit fields returned
   - Pagination for large result sets
   - Aggregation pipelines for complex queries

3. **Connection Pooling**
   - Max connections: 50 per service instance
   - Connection timeout: 30 seconds
   - Idle timeout: 5 minutes

### API Performance

1. **Response Compression**: Gzip compression for all API responses
2. **Pagination**: Limit 100 items per page, cursor-based pagination
3. **Async Processing**: Long-running operations return 202 Accepted with job ID
4. **Rate Limiting**: 1000 requests/minute per user

---

## Disaster Recovery

### Recovery Objectives

- **RTO (Recovery Time Objective)**: 4 hours
- **RPO (Recovery Point Objective)**: 1 hour

### Backup Strategy

#### DocumentDB Backups
- **Automated Snapshots**: Daily at 2 AM UTC
- **Retention**: 7 days (development), 30 days (production)
- **Cross-Region Replication**: Enabled for production

#### S3 Backups
- **Versioning**: Enabled on all buckets
- **Cross-Region Replication**: Enabled for production
- **Lifecycle Policies**: Transition to Glacier after 90 days

#### Application State
- **ECS Task Definitions**: Versioned in ECR
- **Infrastructure**: Versioned in Git, deployed via CDK
- **Configuration**: Stored in Parameter Store / Secrets Manager

### Disaster Recovery Procedures

#### Scenario 1: Single AZ Failure
- **Impact**: Minimal (services in multiple AZs)
- **Recovery**: Automatic failover via ALB
- **RTO**: < 5 minutes

#### Scenario 2: Region Failure
- **Impact**: Complete service outage
- **Recovery**: Failover to secondary region
- **RTO**: 4 hours
- **Steps**:
  1. Activate secondary region infrastructure
  2. Restore DocumentDB from cross-region snapshot
  3. Update DNS to point to secondary region
  4. Restore S3 data from cross-region replication

#### Scenario 3: Data Corruption
- **Impact**: Data loss
- **Recovery**: Restore from point-in-time backup
- **RPO**: 1 hour (last backup)
- **Steps**:
  1. Identify corruption time window
  2. Restore DocumentDB to point-in-time
  3. Restore S3 objects from version history
  4. Replay Kafka events from backup

### Multi-Region Architecture (Future)

**Primary Region**: us-east-1 (N. Virginia)  
**Secondary Region**: us-west-2 (Oregon)

**Replication Strategy**:
- DocumentDB: Cross-region read replica
- S3: Cross-region replication
- MSK: Multi-region cluster (future)

---

## Security Architecture

See [Security Architecture Document](./security-architecture.md) (to be created by PROD-4)

**Key Components**:
- Amazon Cognito for authentication
- API Gateway with authorizers
- IAM roles with least privilege
- AWS KMS for encryption
- AWS WAF for DDoS protection
- GuardDuty for threat detection

---

## Cost Optimization

See [Cost Optimization Document](./cost-optimization.md) (to be created by PROD-5)

**Key Strategies**:
- Resource tagging for cost allocation
- Right-sizing ECS tasks and databases
- S3 Intelligent-Tiering
- Reserved capacity for predictable workloads
- Graviton instances for 20-40% savings

---

## Integration Patterns

### Event-Driven Integration

**Pattern**: Publish-Subscribe via Kafka

```
Service A → Kafka Topic → Service B (subscriber)
                        → Service C (subscriber)
```

**Event Types**:
- `FileCreated` → Triggers parsers
- `FileParsed` → Triggers indexing
- `EntityIndexed` → Triggers notifications

### Synchronous Integration

**Pattern**: REST API via API Gateway

```
Client → API Gateway → ALB → ECS Service
```

**Authentication**: Cognito JWT tokens
**Rate Limiting**: 1000 req/min per user

### Service Discovery

**Pattern**: AWS Cloud Map

```
Service A → Cloud Map → Service B endpoint
```

---

## Deployment Strategy

### Environments

1. **Development**: Single AZ, minimal resources
2. **Staging**: Multi-AZ, production-like resources
3. **Production**: Multi-AZ, full resources, monitoring

### Deployment Process

1. **Build**: GitHub Actions builds Docker images
2. **Test**: Automated tests (unit, integration, E2E)
3. **Deploy**: CDK deploys infrastructure, ECS updates services
4. **Verify**: Health checks and smoke tests
5. **Monitor**: CloudWatch alarms and dashboards

### Blue/Green Deployment

- **Strategy**: ECS blue/green deployments
- **Traffic Shifting**: 10% → 50% → 100% over 30 minutes
- **Rollback**: Automatic on health check failures

---

## Architecture Diagrams

See [Architecture Diagrams](./architecture-diagrams.md) for detailed visual representations of:
- High-level architecture
- Event-driven flow
- Multi-AZ deployment
- Scalability architecture
- Caching layers
- Disaster recovery
- Security architecture
- Service integration patterns
- Observability

## Next Steps

1. ✅ Architecture design complete
2. ✅ ADRs created for major decisions
3. ✅ Architecture diagrams created
4. ⏳ PROD-1: Implement CDK stacks with enhancements
5. ⏳ PROD-2: CI/CD postponed until full migration is complete
6. ⏳ PROD-3: Set up monitoring and alerting
7. ⏳ PROD-4: Implement security architecture
8. ⏳ PROD-5: Implement cost optimization strategies

---

## References

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Architecture Decision Records](./adr/)
- [Architecture Diagrams](./architecture-diagrams.md)
- [Service Documentation](../services/)
- [Infrastructure Code](../infrastructure/)

