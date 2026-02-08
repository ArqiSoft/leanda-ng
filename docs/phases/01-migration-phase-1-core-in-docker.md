# Migration Phase 1: Core Distribution in Docker

## Overview

This document outlines the plan to create the first Leanda NG core distribution running locally in Docker. This phase focuses on migrating the essential core services from .NET to Java/Quarkus, establishing a solid foundation for subsequent phases.

## Objectives

1. **Create minimal viable core distribution** - Replace core .NET services with Java/Quarkus equivalents
2. **Establish Docker-based local development** - All services run in Docker Compose
3. **Implement comprehensive testing** - Unit tests, integration tests, and E2E validation
4. **Maintain feature parity** - Core API endpoints match existing functionality
5. **Enable parallel running** - Run alongside existing Leanda Lite for validation

## Current State Analysis

### Leanda Lite Core Services

| Service | Technology | Port | Purpose |
|---------|-----------|------|---------|
| `core-lite` | .NET Core 3.1 | 18006 | Main API (WebApi + BackEnd + FrontEnd + SagaHost) |
| `blob-storage-api` | .NET Core 3.1 | 18006 | File/blob storage API |
| `persistence-service` | .NET Core 3.1 | Internal | Event persistence |
| `domain-backend` | .NET Core 3.1 | Internal | Domain event handlers |
| `domain-frontend` | .NET Core 3.1 | Internal | Domain query handlers |
| `saga-host` | .NET Core 3.1 | Internal | Saga orchestration |

### Infrastructure Dependencies

| Service | Current | Target (Phase 1) |
|---------|---------|-----------------|
| Database | MongoDB 3.6 | MongoDB 7.0 (compatible) |
| Cache | Redis 4 | Redis 7.2 |
| Messaging | RabbitMQ | Redpanda (Kafka-compatible) |
| Event Store | EventStore 4.0.2 | DynamoDB Streams (Phase 2) or MongoDB Change Streams |
| Search | Elasticsearch | OpenSearch Serverless (Phase 2) |
| Storage | Local/GridFS | MinIO (S3-compatible) |

## Target Architecture - Phase 1

```mermaid
flowchart TB
    subgraph docker [Docker Compose - Leanda NG Core]
        subgraph core [Core Services - Quarkus]
            CoreAPI[core-api:8080<br/>WebApi + Domain]
            Persistence[persistence-service:8084<br/>Event Persistence]
        end
        
        subgraph data [Data Services]
            MongoDB[(MongoDB 7.0:27017)]
            Redis[(Redis 7.2:6379)]
            Redpanda[Redpanda:19092]
            MinIO[MinIO:9000]
        end
        
        subgraph tests [Test Infrastructure]
            TestContainers[Testcontainers]
            IntegrationTests[Integration Tests]
        end
    end
    
    Developer[Developer] --> docker
    core --> MongoDB
    core --> Redis
    core --> Redpanda
    core --> MinIO
    tests --> core
```

## Migration Strategy

### Phase 1.1: Core API Service (Week 1-2)

**Objective**: Migrate `Sds.Osdr.WebApi` to `core-api` Quarkus service

**Key Endpoints to Migrate**:
- Health checks (`/health/live`, `/health/ready`)
- Authentication endpoints (OIDC integration)
- User management endpoints
- File upload/download endpoints
- Metadata endpoints

**Deliverables**:
- [ ] Quarkus REST endpoints matching existing API contracts
- [ ] OpenAPI/Swagger documentation
- [ ] Authentication/authorization integration
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests for all endpoints

### Phase 1.2: Domain Services (Week 2-3)

**Objective**: Migrate domain logic from `Sds.Osdr.Domain.*` to Quarkus services

**Services to Migrate**:
- `Sds.Osdr.Domain.BackEnd` → Event handlers in `core-api`
- `Sds.Osdr.Domain.FrontEnd` → Query handlers in `core-api`
- `Sds.Osdr.Persistence` → Separate `persistence-service`

**Key Features**:
- CQRS pattern implementation
- Event sourcing (using MongoDB Change Streams initially)
- Saga orchestration (using SmallRye Reactive Messaging)

**Deliverables**:
- [ ] Event handlers for domain events
- [ ] Query handlers for read models
- [ ] Persistence service for event storage
- [ ] Integration tests for event flow

### Phase 1.3: Data Migration & Compatibility (Week 3-4)

**Objective**: Ensure data compatibility between old and new systems

**Tasks**:
- [ ] MongoDB schema analysis from existing system
- [ ] Data model mapping (.NET entities → Java entities)
- [ ] Migration scripts for test data
- [ ] Dual-write pattern for validation
- [ ] Data validation tests

**Deliverables**:
- [ ] Data model documentation
- [ ] Migration scripts
- [ ] Validation test suite
- [ ] Rollback procedures

### Phase 1.4: Testing Infrastructure (Week 4-5)

**Objective**: Comprehensive test coverage

**Unit Tests**:
- [ ] Domain logic tests (business rules)
- [ ] Service layer tests (use cases)
- [ ] Repository tests (data access)
- [ ] API endpoint tests (contracts)

**Integration Tests**:
- [ ] Testcontainers setup for MongoDB, Redis, Redpanda
- [ ] Service-to-service communication tests
- [ ] Database integration tests
- [ ] Message queue integration tests

**E2E Tests**:
- [ ] Full stack tests in Docker Compose
- [ ] API contract validation
- [ ] Authentication flow tests
- [ ] File upload/download tests

**Deliverables**:
- [ ] Test infrastructure setup
- [ ] Test data fixtures
- [ ] CI/CD test pipeline (CI/CD postponed until full migration)
- [ ] Test coverage reports (>80%)

## Multi-Agent Parallel Execution

This plan is designed for execution by **5 parallel agents**. See:
- [Coordination Framework](./01-migration-phase-1-core-in-docker-coordination.md) - How agents coordinate
- [Agent Work Packages](./01-migration-phase-1-agent-work-packages.md) - Individual agent tasks

### Agent Assignment

| Agent | Focus Area | Critical Path |
|-------|-----------|---------------|
| **Agent 1** | Core API & REST Endpoints | Week 1 Day 3+ |
| **Agent 2** | Domain Services & Event Handlers | Week 1 Day 3+ |
| **Agent 3** | Persistence & Data Layer | Week 1 Day 3+ |
| **Agent 4** | Testing Infrastructure | Week 1 Day 5+ |
| **Agent 5** | Docker & Infrastructure | **Week 1 Day 1-2 (CRITICAL)** |

### Parallel Execution Timeline

```mermaid
gantt
    title Phase 1 Multi-Agent Timeline
    dateFormat  YYYY-MM-DD
    section Agent 5 (Docker)
    Docker Setup           :crit, a5, 2025-01-01, 2d
    Dockerfiles            :a5, after a5, 2d
    Environment Config     :a5, after a5, 1d
    section Agent 1 (Core API)
    Wait for Docker        :a1, 2025-01-01, 2d
    Service Scaffold       :a1, after a5, 2d
    API Contracts          :a1, after a1, 1d
    User Endpoints         :a1, after a1, 3d
    Auth/Authorization     :a1, after a1, 2d
    section Agent 2 (Domain)
    Wait for Docker        :a2, 2025-01-01, 2d
    Event Models           :a2, after a5, 2d
    Event Schema           :a2, after a2, 1d
    Event Handlers         :a2, after a2, 3d
    Saga Orchestration     :a2, after a2, 2d
    section Agent 3 (Persistence)
    Wait for Docker        :a3, 2025-01-01, 2d
    Data Models            :a3, after a5, 2d
    Repositories           :a3, after a3, 1d
    Persistence Service    :a3, after a3, 3d
    Data Migration         :a3, after a3, 2d
    section Agent 4 (Testing)
    Wait for Docker        :a4, 2025-01-01, 2d
    Testcontainers Setup   :a4, after a5, 2d
    First Integration Test :a4, after a4, 1d
    Test Support           :a4, after a4, 10d
```

## Implementation Plan

### Week 1: Foundation Setup

#### Day 1-2: Project Structure & Docker Compose

**Tasks**:
1. Create `leanda-ng-core-distro/` directory structure
2. Set up Docker Compose with data services (MongoDB, Redis, Redpanda, MinIO)
3. Configure service networking and volumes
4. Create development Dockerfiles for Quarkus services

**Deliverables**:
- `docker-compose.yml` with all infrastructure services
- Development Dockerfiles
- Environment configuration files
- Makefile for common operations

#### Day 3-4: Core API Scaffold

**Tasks**:
1. Create `core-api` Quarkus service with basic structure
2. Implement health check endpoints
3. Set up OpenAPI/Swagger
4. Configure MongoDB, Redis, Kafka connections
5. Create basic authentication structure

**Deliverables**:
- Working `core-api` service
- Health endpoints functional
- Database connections verified
- Basic API documentation

#### Day 5: Initial Testing Setup

**Tasks**:
1. Set up Testcontainers for integration tests
2. Create test base classes
3. Write first integration test (health check)
4. Configure test data fixtures

**Deliverables**:
- Testcontainers configuration
- First passing integration test
- Test utilities and helpers

### Week 2: Core API Migration

#### Day 1-3: User Management Endpoints

**Tasks**:
1. Analyze existing user management API endpoints
2. Create domain models (User entity, DTOs)
3. Implement repository layer (MongoDB Panache)
4. Implement service layer (business logic)
5. Create REST endpoints
6. Write unit tests
7. Write integration tests

**Endpoints to Migrate**:
- `GET /api/v1/users` - List users
- `GET /api/v1/users/{id}` - Get user by ID
- `POST /api/v1/users` - Create user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

**Deliverables**:
- User management API endpoints
- Unit tests (>80% coverage)
- Integration tests
- API documentation

#### Day 4-5: Authentication & Authorization

**Tasks**:
1. Integrate OIDC authentication (Keycloak)
2. Implement JWT token validation
3. Create authorization filters
4. Add role-based access control
5. Write security tests

**Deliverables**:
- OIDC integration working
- JWT validation
- Authorization filters
- Security test suite

### Week 3: Domain Services Migration

#### Day 1-2: Event Handlers (BackEnd)

**Tasks**:
1. Analyze existing domain event handlers
2. Create event models
3. Implement event handlers using SmallRye Reactive Messaging
4. Set up Kafka topics and consumers
5. Write event handler tests

**Key Events to Handle**:
- UserCreated, UserUpdated, UserDeleted
- FileUploaded, FileProcessed
- MetadataExtracted

**Deliverables**:
- Event handler implementations
- Kafka consumer configuration
- Event handler tests

#### Day 3-4: Query Handlers (FrontEnd)

**Tasks**:
1. Analyze existing query handlers
2. Create read models (MongoDB collections)
3. Implement query handlers
4. Set up CQRS read model updates
5. Write query handler tests

**Deliverables**:
- Query handler implementations
- Read model updates
- Query handler tests

#### Day 5: Persistence Service

**Tasks**:
1. Create separate `persistence-service`
2. Implement event persistence logic
3. Set up MongoDB Change Streams for event sourcing
4. Create event replay functionality
5. Write persistence tests

**Deliverables**:
- Persistence service
- Event storage working
- Event replay capability
- Persistence tests

### Week 4: File Management & Data Migration

#### Day 1-2: File Upload/Download

**Tasks**:
1. Analyze existing blob storage API
2. Implement file upload to MinIO
3. Implement file download from MinIO
4. Add file metadata management
5. Write file operation tests

**Endpoints to Migrate**:
- `POST /api/v1/files/upload` - Upload file
- `GET /api/v1/files/{id}/download` - Download file
- `GET /api/v1/files/{id}` - Get file metadata
- `DELETE /api/v1/files/{id}` - Delete file

**Deliverables**:
- File upload/download endpoints
- MinIO integration
- File metadata management
- File operation tests

#### Day 3-4: Data Migration

**Tasks**:
1. Analyze existing MongoDB collections
2. Create data model mapping document
3. Write migration scripts
4. Create test data fixtures
5. Implement dual-write pattern for validation

**Deliverables**:
- Data model documentation
- Migration scripts
- Test data fixtures
- Dual-write validation

#### Day 5: Integration Testing

**Tasks**:
1. Create comprehensive integration test suite
2. Test full user workflows
3. Test file upload/download workflows
4. Test event-driven flows
5. Performance baseline tests

**Deliverables**:
- Complete integration test suite
- Workflow tests
- Performance baseline

### Week 5: E2E Testing & Validation

#### Day 1-2: E2E Test Framework

**Tasks**:
1. Set up Playwright for E2E tests
2. Create test scenarios
3. Implement API contract tests
4. Create test data management

**Test Scenarios**:
- User registration and login
- File upload and processing
- Metadata extraction
- Search functionality

**Deliverables**:
- E2E test framework
- Test scenarios
- API contract tests

#### Day 3-4: Parallel Running Setup

**Tasks**:
1. Configure both Leanda Lite and Leanda NG to run simultaneously
2. Set up data synchronization
3. Create comparison tests
4. Implement feature flags

**Deliverables**:
- Parallel running configuration
- Data sync setup
- Comparison test suite
- Feature flag system

#### Day 5: Documentation & Handoff

**Tasks**:
1. Complete API documentation
2. Write migration guide
3. Create troubleshooting guide
4. Document test procedures
5. Prepare handoff materials

**Deliverables**:
- Complete documentation
- Migration guide
- Troubleshooting guide
- Test procedures

## Testing Strategy

### Unit Tests

**Coverage Target**: >80% code coverage

**Test Categories**:
1. **Domain Logic Tests**
   - Business rule validation
   - Entity behavior
   - Value object validation

2. **Service Layer Tests**
   - Use case execution
   - Error handling
   - Edge cases

3. **Repository Tests**
   - Data access operations
   - Query correctness
   - Transaction handling

4. **API Layer Tests**
   - Request/response mapping
   - Validation
   - Error responses

**Tools**:
- JUnit 5
- Mockito for mocking
- AssertJ for assertions

### Integration Tests

**Test Categories**:
1. **Database Integration**
   - MongoDB operations
   - Redis operations
   - Data consistency

2. **Message Queue Integration**
   - Kafka producer/consumer
   - Event handling
   - Saga orchestration

3. **Service Integration**
   - Service-to-service communication
   - API endpoint testing
   - Authentication flow

**Tools**:
- Testcontainers (MongoDB, Redis, Kafka)
- REST Assured for API testing
- WireMock for external service mocking

### E2E Tests

**Test Scenarios**:
1. **User Workflows**
   - Registration → Login → File Upload → Search
   - Authentication → Authorization → Data Access

2. **File Processing Workflows**
   - Upload → Processing → Metadata Extraction → Search

3. **Event-Driven Workflows**
   - Event Publishing → Event Handling → State Updates

**Tools**:
- Playwright for browser automation
- Docker Compose for full stack
- Test data fixtures

## Docker Compose Configuration

### Core Services

```yaml
version: '3.8'

services:
  # Data Services (from existing docker-compose.yml)
  mongodb:
    image: mongo:7.0
    # ... existing config
  
  redis:
    image: redis:7.2-alpine
    # ... existing config
  
  redpanda:
    image: docker.redpanda.com/vectorized/redpanda:latest
    # ... existing config
  
  minio:
    image: minio/minio:latest
    # ... existing config

  # Core API Service
  core-api:
    build:
      context: ../services/core-api
      dockerfile: Dockerfile.dev
    container_name: leanda-ng-core-api
    ports:
      - "8080:8080"
      - "5005:5005"  # Debug port
    environment:
      QUARKUS_HTTP_PORT: 8080
      MONGODB_CONNECTION_STRING: mongodb://admin:admin123@mongodb:27017/leanda-ng?authSource=admin
      KAFKA_BOOTSTRAP_SERVERS: redpanda:9092
      REDIS_HOST: redis
      REDIS_PORT: 6379
      S3_ENDPOINT: http://minio:9000
      S3_ACCESS_KEY: minioadmin
      S3_SECRET_KEY: minioadmin123
    volumes:
      - ../services/core-api/src:/app/src:ro
    networks:
      - leanda-ng-network
    depends_on:
      mongodb:
        condition: service_healthy
      redis:
        condition: service_healthy
      redpanda:
        condition: service_healthy

  # Persistence Service
  persistence-service:
    build:
      context: ../services/persistence-service
      dockerfile: Dockerfile.dev
    container_name: leanda-ng-persistence
    ports:
      - "8084:8084"
    environment:
      QUARKUS_HTTP_PORT: 8084
      MONGODB_CONNECTION_STRING: mongodb://admin:admin123@mongodb:27017/leanda-ng?authSource=admin
      KAFKA_BOOTSTRAP_SERVERS: redpanda:9092
    volumes:
      - ../services/persistence-service/src:/app/src:ro
    networks:
      - leanda-ng-network
    depends_on:
      mongodb:
        condition: service_healthy
      redpanda:
        condition: service_healthy
```

## Success Criteria

### Functional Requirements

- [ ] All core API endpoints implemented and tested
- [ ] Authentication and authorization working
- [ ] File upload/download functional
- [ ] Event-driven workflows operational
- [ ] Data persistence working correctly

### Non-Functional Requirements

- [ ] Unit test coverage >80%
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] API response times <500ms (p95)
- [ ] Zero critical security vulnerabilities
- [ ] Documentation complete

### Migration Validation

- [ ] Data model compatibility verified
- [ ] API contract compatibility verified
- [ ] Parallel running successful
- [ ] Feature parity confirmed
- [ ] Performance baseline established

## Risk Mitigation

### Technical Risks

1. **Data Model Incompatibility**
   - **Risk**: MongoDB schema differences between .NET and Java
   - **Mitigation**: Early schema analysis, migration scripts, dual-write pattern

2. **Event Store Migration**
   - **Risk**: EventStore 4.0.2 → MongoDB Change Streams complexity
   - **Mitigation**: Start with MongoDB Change Streams, plan DynamoDB Streams for Phase 2

3. **Authentication Integration**
   - **Risk**: OIDC/Keycloak integration complexity
   - **Mitigation**: Use Quarkus OIDC extension, test early

4. **Performance Degradation**
   - **Risk**: Java/Quarkus performance vs .NET
   - **Mitigation**: Performance testing, optimization, native builds

### Process Risks

1. **Scope Creep**
   - **Risk**: Adding features beyond core functionality
   - **Mitigation**: Strict phase boundaries, feature freeze

2. **Testing Gaps**
   - **Risk**: Insufficient test coverage
   - **Mitigation**: Test-driven development, coverage gates

3. **Documentation Debt**
   - **Risk**: Incomplete documentation
   - **Mitigation**: Documentation as part of definition of done

## Deliverables Checklist

### Code

- [ ] Core API service (Quarkus)
- [ ] Persistence service (Quarkus)
- [ ] Domain event handlers
- [ ] Query handlers
- [ ] Repository implementations
- [ ] Service layer implementations
- [ ] REST API endpoints
- [ ] Authentication/authorization

### Tests

- [ ] Unit test suite (>80% coverage)
- [ ] Integration test suite
- [ ] E2E test suite
- [ ] Test data fixtures
- [ ] Test utilities and helpers

### Infrastructure

- [ ] Docker Compose configuration
- [ ] Development Dockerfiles
- [ ] Environment configuration
- [ ] Makefile/scripts
- [ ] CI/CD pipeline (postponed until full migration)

### Documentation

- [ ] API documentation (OpenAPI/Swagger)
- [ ] Architecture documentation
- [ ] Migration guide
- [ ] Testing guide
- [ ] Troubleshooting guide
- [ ] Developer setup guide

## Timeline Summary

| Week | Focus | Deliverables |
|------|-------|--------------|
| 1 | Foundation Setup | Docker Compose, Core API scaffold, Test setup |
| 2 | Core API Migration | User management, Authentication |
| 3 | Domain Services | Event handlers, Query handlers, Persistence |
| 4 | File Management & Data | File operations, Data migration |
| 5 | E2E Testing & Validation | E2E tests, Parallel running, Documentation |

**Total Duration**: 5 weeks

## Next Steps After Phase 1

1. **Phase 2**: Domain-specific services (Chemicals, Crystals, Spectra)
2. **Phase 3**: File parsers migration
3. **Phase 4**: ML services integration
4. **Phase 5**: Frontend migration
5. **Phase 6**: AWS deployment

## References

- [Leanda NG Plan](../05-leanda-ng-plan.md)
- [Local Docker Development Plan](../../leanda-ng/docker/README.md)
- [Leanda Lite Configuration](../../configuration/leanda-lite/readme.md)

