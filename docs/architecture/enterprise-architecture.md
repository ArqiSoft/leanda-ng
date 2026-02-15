# Leanda.io Enterprise Architecture

**Status**: Current State Analysis  
**Last Updated**: 2025-01-15  
**Architect**: Enterprise Architecture Team

## Executive Summary

Leanda.io is an extensible open science data repository platform designed to enable researchers to consume, process, visualize, and analyze diverse scientific data types, formats, and volumes. The platform features a modular microservices architecture built on modern cloud-native technologies, following Domain-Driven Design (DDD) principles and AWS Well-Architected Framework best practices.

### Key Characteristics

- **Architecture Style**: Event-driven microservices
- **Deployment Model**: Cloud-native (AWS) with container orchestration
- **Technology Stack**: Java 21/Quarkus (backend), Angular 21 (frontend), Python 3.12+ (ML services)
- **Data Storage**: DocumentDB (MongoDB-compatible), S3, OpenSearch
- **Messaging**: Kafka (MSK Serverless) for event-driven communication
- **Design Patterns**: Domain-Driven Design, CQRS, Event Sourcing (partial)

## Architecture Overview

### System Purpose

Leanda.io addresses key deficiencies in existing open science tools by providing:

- Real-time automated + manual data curation with AI-powered metadata extraction
- Ontology-based property assignment and complex semantic searches
- On-the-fly data mining, text extraction, and format conversion during deposition
- Granular security model supporting private, shared, and public data
- Rapid ML training dataset composition from integrated sources and processed data
- Embedded ML framework for research and drug discovery pipelines

### Supported Data Domains

The platform handles a wide range of scientific formats:

- Generic images (PNG, GIF, TIFF, BMP)
- Documents (PDF, MS Office, OpenOffice)
- Tabular data (CSV, TSV, Excel)
- Chemical structures (SDF, MOL, SMILES, CDX)
- Chemical reactions (RXN)
- Crystallographic data (CIF)
- Spectra (JDX)
- Microscopy imaging files
- Machine learning models & weights

## System Context

See [System Context Diagram](./system-context.md) for detailed visualization.

### External Actors

1. **Researchers**: Primary users who upload, manage, and analyze scientific data
2. **Administrators**: System administrators managing users, permissions, and system configuration
3. **External Systems**: ML frameworks, scientific tools, and third-party integrations
4. **AWS Services**: Managed cloud services (DocumentDB, S3, MSK, etc.)

### System Boundaries

- **Frontend**: Angular 21 web application
- **Backend Services**: 11 Java/Quarkus microservices
- **ML Services**: Python/FastAPI services for ML pipelines
- **Infrastructure**: AWS cloud infrastructure (ECS, DocumentDB, S3, MSK, etc.)

## Bounded Contexts (DDD Perspective)

See [Bounded Contexts Diagram](./bounded-contexts.md) for detailed visualization.

### Core Domain Contexts

1. **User Management Context**
   - User registration and authentication
   - User profile management
   - Access control and permissions
   - Service: `core-api`

2. **File Management Context**
   - File upload and storage
   - File metadata management
   - File versioning and lifecycle
   - Services: `core-api`, `blob-storage`

3. **Data Processing Context**
   - File parsing and format conversion
   - Metadata extraction
   - Data transformation
   - Services: Domain parsers, `metadata-processing`, `office-processor`

### Supporting Contexts

1. **Parsing Context**
   - Chemical structure parsing (SDF, MOL)
   - Reaction parsing (RXN)
   - Crystal structure parsing (CIF)
   - Spectra parsing (JDX)
   - Services: `chemical-parser`, `reaction-parser`, `crystal-parser`, `spectra-parser`

2. **Indexing Context**
   - Full-text search indexing
   - Entity indexing (Files, Folders, Records, Users)
   - Search query processing
   - Service: `indexing`

3. **Metadata Context**
   - Metadata generation and extraction
   - Property type qualification
   - Infobox metadata generation
   - Service: `metadata-processing`

### Generic Contexts

1. **Storage Context**
   - Blob storage (S3)
   - Metadata storage (DocumentDB)
   - Cache storage (Redis)
   - Service: `blob-storage`

2. **Messaging Context**
   - Event publishing and consumption
   - Event routing and delivery
   - Service: MSK Serverless (Kafka)

## Technology Stack

See [Technology Stack Diagram](./technology-stack.md) for detailed visualization.

### Frontend Layer

- **Framework**: Angular 21
- **Language**: TypeScript
- **Architecture**: Zoneless architecture with Signal Forms
- **Testing**: Playwright for E2E tests
- **Deployment**: AWS Amplify Hosting

### Backend Layer

- **Framework**: Quarkus 3.17+
- **Language**: Java 21 LTS
- **Architecture**: Microservices with DDD
- **Messaging**: SmallRye Reactive Messaging (Kafka)
- **Data Access**: Quarkus Panache MongoDB
- **Testing**: JUnit 5, Testcontainers
- **Deployment**: ECS Fargate

### ML Services Layer

- **Framework**: FastAPI
- **Language**: Python 3.12+
- **Deployment**: ECS Fargate or Lambda (future)

### Data Layer

- **Metadata Database**: Amazon DocumentDB 5.0 (MongoDB 7.0 compatible)
- **Cache**: Amazon ElastiCache Redis 7.2
- **Object Storage**: Amazon S3
- **Search**: Amazon OpenSearch 2.11

### Infrastructure Layer

- **Container Orchestration**: Amazon ECS Fargate
- **Messaging**: Amazon MSK Serverless (Kafka)
- **API Gateway**: Amazon API Gateway
- **CDN**: Amazon CloudFront
- **Infrastructure as Code**: AWS CDK (TypeScript)
- **Monitoring**: Amazon CloudWatch, X-Ray, Prometheus, Grafana

## Integration Patterns

See [Integration Patterns Diagram](./integration-patterns.md) for detailed visualization.

### Synchronous Communication

- **Pattern**: REST APIs via API Gateway
- **Protocol**: HTTP/HTTPS
- **Authentication**: OIDC/OAuth2 (Cognito)
- **Rate Limiting**: API Gateway throttling
- **Services**: All microservices expose REST APIs

### Asynchronous Communication

- **Pattern**: Event-driven via Kafka
- **Protocol**: Kafka protocol
- **Event Types**: Domain events (FileCreated, FileParsed, etc.)
- **Consumer Groups**: One per service
- **Topics**: Domain-specific topics (file-events, folder-events, etc.)

### Service Discovery

- **Pattern**: AWS Cloud Map
- **Mechanism**: Service registry with DNS-based discovery
- **Scope**: Internal service-to-service communication

### API Gateway Pattern

- **Entry Point**: Amazon API Gateway
- **Routing**: Path-based routing to backend services
- **Authentication**: Cognito authorizers
- **Rate Limiting**: Per-user and per-API limits

## Non-Functional Requirements

### Performance

- **API Response Time**: p95 < 500ms
- **Frontend Load Time**: < 2 seconds
- **Database Query Time**: p95 < 100ms
- **File Upload Throughput**: Support concurrent uploads

### Scalability

- **Horizontal Scaling**: Auto-scaling ECS services (2-20 tasks)
- **Database Scaling**: DocumentDB read replicas, connection pooling
- **Messaging Scaling**: MSK Serverless auto-scaling
- **Storage Scaling**: S3 unlimited capacity

### Availability

- **Target**: 99.9% (3 nines) availability
- **Multi-AZ Deployment**: All services across 2+ availability zones
- **Health Checks**: Liveness and readiness probes
- **Auto-Recovery**: Automatic task replacement on failure

### Security

- **Encryption**: At rest (KMS) and in transit (TLS 1.2+)
- **Authentication**: OIDC/OAuth2 via Cognito
- **Authorization**: RBAC with IAM roles
- **Network Security**: VPC with private subnets, security groups
- **Monitoring**: GuardDuty, Security Hub, CloudTrail

### Reliability

- **RTO**: 4 hours (Recovery Time Objective)
- **RPO**: 1 hour (Recovery Point Objective)
- **Backup Strategy**: Automated DocumentDB snapshots, S3 versioning
- **Disaster Recovery**: Multi-region backup strategy

### Observability

- **Logging**: Structured JSON logs to CloudWatch
- **Metrics**: CloudWatch Metrics, Prometheus
- **Tracing**: X-Ray with OpenTelemetry
- **Alerting**: SNS topics with severity levels (P1/P2/P3)
- **Dashboards**: CloudWatch and Grafana dashboards

## Architecture Principles and Decisions

### Design Principles

1. **Serverless-First**: Prefer managed services (ECS Fargate, MSK Serverless) over self-managed
2. **Event-Driven**: Asynchronous communication via Kafka for loose coupling
3. **Domain-Driven Design**: Organize code by bounded contexts
4. **Microservices**: Independent deployable services with clear boundaries
5. **API-First**: OpenAPI specifications for all REST APIs
6. **Infrastructure as Code**: All infrastructure defined in CDK
7. **Security by Design**: Least privilege, encryption, network isolation
8. **Observability**: Comprehensive logging, metrics, and tracing

### Key Architectural Decisions

See [Architecture Decision Records](../adr/) for detailed ADRs.

1. **ADR-0001**: Use ECS Fargate for compute (serverless containers)
2. **ADR-0002**: Use MSK Serverless for messaging (auto-scaling Kafka)
3. **ADR-0003**: Use DocumentDB for metadata (MongoDB-compatible)
4. **ADR-0004**: Multi-AZ deployment strategy
5. **ADR-0005**: Three-layer caching strategy (CloudFront, Redis, application)
6. **ADR-0006**: Disaster recovery strategy (RTO: 4h, RPO: 1h)
7. **ADR-0011**: Observability architecture (MELT: Metrics, Events, Logs, Traces)

## Current State Assessment

See [Current State Assessment](./current-state-assessment.md) for detailed analysis.

### Strengths

- Modern technology stack (Java 21, Quarkus, Angular 21)
- Event-driven architecture for loose coupling
- Infrastructure as Code (CDK)
- Multi-AZ deployment for high availability
- Comprehensive observability setup
- Domain-Driven Design approach

### Gaps and Risks

- Limited CI/CD automation (CI/CD postponed until full migration is complete)
- No automated disaster recovery testing
- Limited performance testing
- Security monitoring needs enhancement
- Cost optimization opportunities exist

## Future State Recommendations

See [Future State Recommendations](./future-state-recommendations.md) for detailed roadmap.

### Short-Term (0-3 months)

- Implement CI/CD pipelines (GitHub Actions → CodePipeline) — postponed until full migration is complete
- Enhance security monitoring (GuardDuty, Security Hub)
- Performance testing and optimization
- Cost allocation and monitoring

### Medium-Term (3-6 months)

- Multi-region deployment
- Advanced caching strategies
- ML services modernization
- Enhanced observability (Application Signals)

### Long-Term (6-12 months)

- Serverless migration for appropriate services (Lambda)
- Advanced ML capabilities
- Data lake integration (Apache Iceberg)
- Enhanced collaboration features

## Visual Artifacts

This document references the following visual artifacts:

1. [System Context Diagram](./system-context.md) - External actors and system boundaries
2. [Container Diagram](./container-diagram.md) - High-level system containers
3. [Component Diagrams](./component-diagrams.md) - Service component details
4. [Deployment Diagram](./deployment-diagram.md) - AWS infrastructure deployment
5. [Data Flow Diagrams](./data-flow-diagrams.md) - Data processing flows
6. [Sequence Diagrams](./sequence-diagrams.md) - Key interaction sequences
7. [Bounded Contexts Diagram](./bounded-contexts.md) - DDD bounded contexts
8. [Technology Stack Diagram](./technology-stack.md) - Technology layers
9. [Integration Patterns Diagram](./integration-patterns.md) - Communication patterns
10. [Security Architecture Diagram](./security-architecture.md) - Security layers
11. [Observability Architecture Diagram](./observability-architecture.md) - Observability stack

## References

- [Cloud Architecture Design](../cloud-architecture.md)
- [Architecture Diagrams](../architecture-diagrams.md)
- [Architecture Decision Records](../adr/)
- [AWS Well-Architected Framework Review](../cloud-architecture.md#aws-well-architected-framework-review)
- [Service Documentation](../../services/)
- [Infrastructure Code](../../infrastructure/)

---

**Document Version**: 1.0  
**Next Review**: 2025-04-15
