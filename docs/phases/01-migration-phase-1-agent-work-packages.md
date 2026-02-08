# Phase 1 Agent Work Packages

## Overview

This document defines individual work packages for each agent, enabling parallel execution with clear boundaries and deliverables.

---

## Agent 0: Legacy Spec Extraction (Runs First)

### Scope

Analyze legacy .NET services and generate detailed specifications for Java/Quarkus rewrite. This agent must complete before Phase 1 implementation begins.

### Deliverables

1. **API Specifications** (`shared/specs/api/`)
   - OpenAPI 3.1 specs extracted from WebApi controllers
   - Request/response schemas
   - Authentication/authorization requirements

2. **Event Specifications** (`shared/specs/events/`)
   - AsyncAPI specs from MassTransit contracts
   - Command/event schemas
   - Topic mappings

3. **Data Model Specifications** (`shared/specs/models/`)
   - JSON schemas from MongoDB entities
   - Relationship documentation
   - Collection names and indexes

4. **Implementation Plans** (`shared/specs/implementation/`)
   - .NET to Quarkus mapping
   - Technology choices per component
   - Work breakdown per agent

5. **Test Specifications** (`shared/specs/tests/`)
   - API test specifications
   - Integration test scenarios
   - Test data fixtures

### Week-by-Week Breakdown

#### Week 1

**Day 1-2**: API Specification Extraction
- Read `leanda-core/Sds.Osdr.WebApi/` source code
- Extract all REST endpoints from controllers
- Document request/response DTOs
- Generate OpenAPI 3.1 specification
- Output: `shared/specs/api/core-api.yaml`

**Day 3-4**: Event/Command Extraction
- Read `leanda-core/Sds.Osdr.Domain.BackEnd/` and `Domain.FrontEnd/`
- Extract all MassTransit message contracts
- Document command and event schemas
- Map to Kafka topics
- Generate AsyncAPI specification
- Output: `shared/specs/events/domain-events.yaml`

**Day 5**: Data Model Extraction
- Read `leanda-core/Sds.Osdr.Persistence/` and domain modules
- Extract MongoDB entity classes
- Document relationships and indexes
- Generate JSON Schema for each entity
- Output: `shared/specs/models/*.json`

**Deliverables**:
- [ ] OpenAPI 3.1 spec for core-api
- [ ] AsyncAPI spec for domain events
- [ ] JSON schemas for all entities
- [ ] Data model documentation

#### Week 2

**Day 1-2**: Implementation Plan Creation
- Map each .NET component to Quarkus equivalent
- Define technology choices (Panache, SmallRye, etc.)
- Create work breakdown structure per agent
- Identify dependencies between components
- Output: `shared/specs/implementation/core-services-plan.md`

**Day 3-4**: Documentation & Test Spec Updates
- Update architecture docs with extracted specs
- Create test specifications from contracts
- Generate integration test scenarios
- Create test data fixtures specifications
- Output: `shared/specs/tests/*.md`

**Day 5**: Review and Validation
- Validate all specifications are complete
- Review with team (if applicable)
- Update COORDINATION.md with completion status
- Prepare handoff to Phase 1 agents

**Deliverables**:
- [ ] Implementation plan complete
- [ ] Test specifications created
- [ ] Documentation updated
- [ ] All specs validated and ready

### Process

1. Read .NET source code in `leanda-core/`
2. Extract API endpoints → generate OpenAPI spec
3. Extract message contracts → generate AsyncAPI spec
4. Extract entities → generate JSON schemas
5. Create implementation plan for Quarkus rewrite
6. Update docs with generated specs
7. Create test specifications

### Dependencies

**Needs From**:
- Legacy .NET source code in `leanda-core/`
- Existing architecture documentation

**Provides To**:
- All Phase 1 agents: Complete specifications
- Agent 5: Specs for Docker service configuration
- Agent 1: API contracts for implementation
- Agent 2: Event schemas for implementation
- Agent 3: Data models for implementation
- Agent 4: Test specifications

### Success Criteria

- [ ] All target services have complete specifications
- [ ] OpenAPI and AsyncAPI specs are valid and complete
- [ ] Implementation plans are detailed enough for agents to start work
- [ ] Test specifications enable comprehensive test coverage
- [ ] All documentation updated with extracted specs
- [ ] Phase 1 agents can begin implementation without blockers

### Key Files to Analyze

**API Extraction**:
- `leanda-core/Sds.Osdr.WebApi/Controllers/*.cs`
- `leanda-core/Sds.Osdr.WebApi/Models/*.cs`

**Event Extraction**:
- `leanda-core/Sds.Osdr.Domain.BackEnd/Consumers/*.cs`
- `leanda-core/Sds.Osdr.Domain.FrontEnd/Handlers/*.cs`
- MassTransit message contracts

**Data Model Extraction**:
- `leanda-core/Sds.Osdr.Persistence/Entities/*.cs`
- `leanda-core/Sds.Osdr.Domain.*/Entities/*.cs`
- MongoDB collection configurations

### Output Structure

```
shared/specs/
├── api/
│   └── core-api.yaml          # OpenAPI 3.1 spec
├── events/
│   └── domain-events.yaml     # AsyncAPI spec
├── models/
│   ├── User.json              # JSON Schema
│   ├── File.json
│   └── ...
├── implementation/
│   └── core-services-plan.md  # Implementation plan
└── tests/
    ├── api-tests.md
    ├── integration-tests.md
    └── test-data.md
```

---

## Agent 1: Core API & REST Endpoints

### Scope

Implement REST API endpoints for core functionality:
- User management
- Authentication/authorization
- File metadata operations
- Health checks

### Deliverables

1. **Core API Service** (`services/core-api/`)
   - REST endpoints implementation
   - DTOs and request/response models
   - OpenAPI/Swagger documentation
   - Error handling

2. **API Contracts** (`shared/contracts/core-api.yaml`)
   - Complete OpenAPI 3.1 specification
   - Request/response schemas
   - Authentication requirements

3. **Tests**
   - Unit tests (>80% coverage)
   - Integration tests for all endpoints
   - API contract tests

### Week-by-Week Breakdown

#### Week 1

**Day 1-2**: Wait for Docker setup (Agent 5)
- Review existing API endpoints
- Design API contracts
- Prepare implementation plan

**Day 3-4**: Service Scaffold
- Create Quarkus service structure
- Implement health check endpoints
- Set up OpenAPI/Swagger
- Configure MongoDB, Redis, Kafka connections

**Day 5**: API Contract Definition
- Create `shared/contracts/core-api.yaml`
- Define all endpoint contracts
- Get approval from Agent 4 (testing)

**Deliverables**:
- [ ] Core API service scaffold working
- [ ] Health endpoints functional
- [ ] OpenAPI contract defined
- [ ] Database connections verified

#### Week 2

**Day 1-3**: User Management Endpoints
- Implement `GET /api/v1/users`
- Implement `GET /api/v1/users/{id}`
- Implement `POST /api/v1/users`
- Implement `PUT /api/v1/users/{id}`
- Implement `DELETE /api/v1/users/{id}`
- Write unit tests
- Write integration tests

**Day 4-5**: Authentication & Authorization
- Integrate OIDC (Keycloak)
- Implement JWT validation
- Create authorization filters
- Add role-based access control
- Write security tests

**Deliverables**:
- [ ] All user management endpoints
- [ ] Authentication working
- [ ] Authorization implemented
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests passing

### Dependencies

**Needs From**:
- Agent 5: Docker setup (Week 1 Day 1-2)
- Agent 3: User data model (Week 1 Day 3)
- Agent 4: Test utilities (Week 1 Day 5)

**Provides To**:
- Agent 4: API contracts for testing
- Agent 2: API endpoints for event triggers

### Success Criteria

- [ ] All REST endpoints implemented
- [ ] OpenAPI documentation complete
- [ ] Unit test coverage >80%
- [ ] Integration tests passing
- [ ] Authentication/authorization working

---

## Agent 2: Domain Services & Event Handlers

### Scope

Implement domain logic and event-driven architecture:
- Domain event handlers
- CQRS query handlers
- Saga orchestration
- Event publishing

### Deliverables

1. **Event Handlers** (`services/core-api/src/main/java/.../handlers/`)
   - UserCreated, UserUpdated, UserDeleted handlers
   - FileUploaded, FileProcessed handlers
   - MetadataExtracted handlers

2. **Event Schemas** (`shared/contracts/events.yaml`)
   - AsyncAPI specification
   - Event schemas (JSON Schema)
   - Topic definitions

3. **Saga Orchestration**
   - Saga implementations
   - Compensation logic
   - State management

4. **Tests**
   - Event handler unit tests
   - Saga orchestration tests
   - Integration tests with Kafka

### Week-by-Week Breakdown

#### Week 1

**Day 1-2**: Wait for Docker setup (Agent 5)
- Analyze existing domain events
- Design event schema
- Plan event handler architecture

**Day 3-4**: Event Models & Schema
- Create event model classes
- Define AsyncAPI specification
- Set up Kafka topics configuration
- Create event publisher utilities

**Day 5**: Event Schema Publication
- Finalize `shared/contracts/events.yaml`
- Get approval from Agent 3 (persistence)
- Document event flow

**Deliverables**:
- [ ] Event models defined
- [ ] AsyncAPI contract complete
- [ ] Kafka configuration ready
- [ ] Event publisher utilities

#### Week 2

**Day 1-3**: Event Handler Implementation
- Implement UserCreated handler
- Implement UserUpdated handler
- Implement UserDeleted handler
- Implement FileUploaded handler
- Write handler tests

**Day 4-5**: Saga Orchestration
- Implement file processing saga
- Implement user registration saga
- Add compensation logic
- Write saga tests

**Deliverables**:
- [ ] All event handlers implemented
- [ ] Saga orchestration working
- [ ] Event handler tests passing
- [ ] Saga tests passing

### Dependencies

**Needs From**:
- Agent 5: Docker setup (Week 1 Day 1-2)
- Agent 3: Repository interfaces (Week 1 Day 5)
- Agent 1: API endpoints for triggering events (Week 2)

**Provides To**:
- Agent 3: Event schemas for persistence
- Agent 4: Event schemas for testing

### Success Criteria

- [ ] All event handlers implemented
- [ ] Event schemas documented
- [ ] Saga orchestration working
- [ ] Event handler tests passing
- [ ] Integration with Kafka working

---

## Agent 3: Persistence & Data Layer

### Scope

Implement data persistence layer:
- Repository implementations
- Data models
- Event storage
- Persistence service

### Deliverables

1. **Data Models** (`shared/models/`)
   - User entity
   - File entity
   - Event entities
   - Value objects

2. **Repositories** (`services/core-api/src/main/java/.../repositories/`)
   - UserRepository
   - FileRepository
   - EventRepository

3. **Persistence Service** (`services/persistence-service/`)
   - Event storage implementation
   - MongoDB Change Streams setup
   - Event replay functionality

4. **Tests**
   - Repository unit tests
   - Persistence service tests
   - Data migration tests

### Week-by-Week Breakdown

#### Week 1

**Day 1-2**: Wait for Docker setup (Agent 5)
- Analyze existing MongoDB schema
- Design data model mapping
- Plan repository structure

**Day 3-4**: Data Models & Repositories
- Create User entity (Java)
- Create File entity
- Create event entities
- Implement UserRepository
- Implement FileRepository
- Write repository tests

**Day 5**: Repository Interfaces
- Publish repository interfaces to `shared/interfaces/`
- Document data model mapping
- Get approval from Agents 1, 2

**Deliverables**:
- [ ] Data models defined
- [ ] Repository interfaces published
- [ ] Basic repository implementations
- [ ] Repository tests passing

#### Week 2

**Day 1-3**: Persistence Service
- Create persistence-service Quarkus project
- Implement event storage
- Set up MongoDB Change Streams
- Implement event replay
- Write persistence tests

**Day 4-5**: Data Migration
- Create migration scripts
- Implement dual-write pattern
- Create test data fixtures
- Write migration tests

**Deliverables**:
- [ ] Persistence service complete
- [ ] Event storage working
- [ ] Migration scripts ready
- [ ] Test data fixtures created

### Dependencies

**Needs From**:
- Agent 5: Docker setup (Week 1 Day 1-2)

**Provides To**:
- Agent 1: Data models, Repository interfaces
- Agent 2: Event storage, Repository interfaces
- Agent 4: Test data fixtures

### Success Criteria

- [ ] All data models defined
- [ ] Repository implementations complete
- [ ] Persistence service working
- [ ] Event storage functional
- [ ] Migration scripts ready

---

## Agent 4: Testing Infrastructure

### Scope

Set up comprehensive testing infrastructure:
- Testcontainers configuration
- Test utilities and helpers
- Test data fixtures
- CI/CD pipeline
- Integration test framework

### Deliverables

1. **Test Infrastructure** (`tests/`)
   - Testcontainers setup
   - Test base classes
   - Test utilities
   - Test data fixtures

2. **CI/CD Pipeline** (`.github/workflows/`) — CI/CD is postponed until full migration is complete.
   - Unit test pipeline
   - Integration test pipeline
   - Coverage reporting

3. **Test Documentation**
   - Testing guide
   - Test data management guide
   - CI/CD documentation

### Week-by-Week Breakdown

#### Week 1

**Day 1-2**: Wait for Docker setup (Agent 5)
- Review testing requirements
- Design test infrastructure
- Plan test utilities

**Day 3-4**: Testcontainers Setup
- Configure MongoDB Testcontainer
- Configure Redis Testcontainer
- Configure Kafka Testcontainer (Redpanda)
- Create test base classes
- Create test utilities

**Day 5**: First Integration Test
- Create health check integration test
- Verify test infrastructure works
- Document test setup

**Deliverables**:
- [ ] Testcontainers configured
- [ ] Test utilities created
- [ ] First integration test passing
- [ ] Test documentation started

#### Week 2+

**Continuous Support**:
- Create test data fixtures
- Support other agents with testing
- Set up CI/CD pipeline
- Create E2E test framework
- Maintain test documentation

**Deliverables**:
- [ ] Test data fixtures complete
- [ ] CI/CD pipeline working
- [ ] E2E test framework ready
- [ ] Test documentation complete

### Dependencies

**Needs From**:
- Agent 5: Docker setup (Week 1 Day 1-2)
- Agent 1: API contracts for contract testing (Week 1 Day 5)
- Agent 2: Event schemas for event testing (Week 1 Day 5)
- Agent 3: Test data fixtures (Week 2)

**Provides To**:
- All agents: Test infrastructure, Test utilities

### Success Criteria

- [ ] Testcontainers working
- [ ] Test utilities available
- [ ] CI/CD pipeline functional (postponed until full migration)
- [ ] E2E test framework ready
- [ ] Test documentation complete

---

## Agent 5: Docker & Infrastructure

### Scope

Set up Docker-based development environment:
- Docker Compose configuration
- Service Dockerfiles
- Environment configuration
- Development tooling

### Deliverables

1. **Docker Compose** (`docker-compose.yml`)
   - All infrastructure services
   - All application services
   - Networking configuration
   - Volume management

2. **Dockerfiles** (`services/*/Dockerfile.dev`)
   - Development Dockerfiles
   - Production Dockerfiles (future)

3. **Configuration** (`.env.example`, `Makefile`)
   - Environment variable templates
   - Development scripts
   - Common commands

4. **Documentation**
   - Docker setup guide
   - Development workflow
   - Troubleshooting guide

### Week-by-Week Breakdown

#### Week 1

**Day 1-2**: **CRITICAL PATH** - Docker Compose Setup
- Create `docker-compose.yml` with infrastructure services
- Configure MongoDB 7.0
- Configure Redis 7.2
- Configure Redpanda (Kafka)
- Configure MinIO (S3)
- Set up networking
- Test all services start

**Day 3-4**: Service Dockerfiles
- Create Dockerfile.dev for core-api
- Create Dockerfile.dev for persistence-service
- Configure hot-reload
- Set up volume mounts
- Test service startup

**Day 5**: Environment & Tooling
- Create `.env.example`
- Create `Makefile` with common commands
- Document setup process
- Create troubleshooting guide

**Deliverables**:
- [ ] Docker Compose complete
- [ ] All services start successfully
- [ ] Dockerfiles working
- [ ] Environment configuration ready
- [ ] Makefile with commands
- [ ] Documentation complete

#### Week 2+

**Support & Maintenance**:
- Update Docker setup as services evolve
- Support other agents with infrastructure needs
- Optimize Docker configuration
- Maintain documentation

### Dependencies

**Needs From**:
- None (starts first)

**Provides To**:
- All agents: Docker infrastructure

### Success Criteria

- [ ] All services start in Docker
- [ ] Hot-reload working
- [ ] Environment configuration complete
- [ ] Makefile functional
- [ ] Documentation complete

---

## Coordination Points

### Daily Async Standup

Each agent updates `COORDINATION.md` with:
- Status (In Progress / Blocked / Complete)
- Today's work
- Blockers
- Changes to shared artifacts
- Test status

### Weekly Integration Sprints

**End of Week 1**: All agents integrate Docker setup
**End of Week 2**: Core API + Domain Services integration
**End of Week 3**: Full stack integration
**End of Week 4**: E2E validation

### Change Coordination

When changing shared artifacts:
1. Propose in `COORDINATION.md`
2. Wait for review (4-hour window)
3. Implement if approved
4. Notify all agents

---

## Success Metrics Per Agent

### Agent 1 (Core API)
- REST endpoints: 15+ endpoints
- Test coverage: >80%
- API documentation: Complete
- Integration tests: All passing

### Agent 2 (Domain Services)
- Event handlers: 10+ handlers
- Event schemas: Complete
- Saga implementations: 3+ sagas
- Event tests: All passing

### Agent 3 (Persistence)
- Data models: 10+ entities
- Repositories: 5+ repositories
- Persistence service: Complete
- Migration scripts: Ready

### Agent 4 (Testing)
- Test utilities: Complete
- CI/CD pipeline: Functional
- Test coverage: >80% overall
- E2E tests: Framework ready

### Agent 5 (Docker)
- Docker Compose: Complete
- Services: All start successfully
- Documentation: Complete
- Makefile: All commands working

