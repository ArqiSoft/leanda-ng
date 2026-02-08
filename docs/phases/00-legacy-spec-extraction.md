# Phase 0: Legacy .NET Spec Extraction

## Objective

Systematically analyze legacy .NET services and generate detailed specifications for Java/Quarkus rewrite. This phase must be completed before Phase 1 implementation begins.

## Target Services

The following .NET services need spec extraction:

- `Sds.Osdr.WebApi` → `core-api`
- `Sds.Osdr.Domain.BackEnd` → event handlers in `core-api`
- `Sds.Osdr.Domain.FrontEnd` → query handlers in `core-api`
- `Sds.Osdr.Persistence` → `persistence-service`
- `Sds.Osdr.Generic` → `generic-domain`
- `Sds.Osdr.Chemicals` → `chemical-domain`
- `Sds.Osdr.Crystals` → `crystal-domain`
- `Sds.Osdr.Spectra` → (handled by spectra-parser service)
- `Sds.Osdr.Reactions` → (handled by reaction-parser service)
- `Sds.Osdr.MachineLearning` → `ml-orchestrator`

## Spec Extraction Process

### Step 1: API Specification Extraction

**Source**: `leanda-core/Sds.Osdr.WebApi/`

**Tasks**:
- Extract all REST endpoints from WebApi controllers
- Document request/response DTOs
- Identify authentication/authorization requirements
- Document error response formats
- Generate OpenAPI 3.1 specification

**Output**: `shared/specs/api/core-api.yaml` (OpenAPI 3.1)

**Key Information to Extract**:
- HTTP methods (GET, POST, PUT, DELETE, etc.)
- Route paths and parameters
- Request body schemas
- Response status codes and schemas
- Authentication requirements (OIDC, JWT)
- Authorization rules (roles, permissions)
- Validation rules
- Error codes and messages

### Step 2: Event/Command Extraction

**Source**: `leanda-core/Sds.Osdr.Domain.BackEnd/`, `leanda-core/Sds.Osdr.Domain.FrontEnd/`

**Tasks**:
- Extract all MassTransit message contracts
- Document command schemas
- Document event schemas
- Identify event handlers and their logic
- Map to Kafka topics
- Generate AsyncAPI specification

**Output**: `shared/specs/events/domain-events.yaml` (AsyncAPI 2.x)

**Key Information to Extract**:
- Command classes (e.g., `CreateUser`, `UploadFile`)
- Event classes (e.g., `UserCreated`, `FileUploaded`)
- Message properties and types
- Topic/routing key mappings
- Event handler logic and side effects
- Saga orchestration patterns
- Compensation logic

### Step 3: Data Model Extraction

**Source**: `leanda-core/Sds.Osdr.Persistence/`, `leanda-core/Sds.Osdr.Domain.*/`

**Tasks**:
- Extract MongoDB entity classes
- Document relationships and indexes
- Extract value objects
- Document aggregate boundaries
- Generate JSON Schema for each entity
- Document MongoDB collection names

**Output**: `shared/specs/models/*.json` (JSON Schema)

**Key Information to Extract**:
- Entity class names and properties
- Property types and constraints
- Relationships (references, embedded documents)
- MongoDB indexes
- Collection names
- Validation rules
- Aggregate root boundaries

### Step 4: Build Implementation Plan

**Tasks**:
- Map each .NET component to Quarkus equivalent
- Define technology choices (Panache, SmallRye Reactive Messaging, etc.)
- Create work breakdown structure per agent
- Identify dependencies between components
- Document migration risks and mitigation strategies

**Output**: `shared/specs/implementation/core-services-plan.md`

**Mapping Examples**:
- ASP.NET Core Controllers → Quarkus REST Resources
- MassTransit Consumers → SmallRye Reactive Messaging
- MongoDB Driver → Quarkus Panache MongoDB
- Entity Framework → Quarkus Panache
- SignalR → Quarkus WebSockets

### Step 5: Update Documentation & Tests

**Tasks**:
- Update architecture docs with new specs
- Create test specifications from extracted contracts
- Generate integration test scenarios
- Document API contract tests
- Create test data fixtures specifications

**Output**: 
- `shared/specs/tests/api-tests.md`
- `shared/specs/tests/integration-tests.md`
- `shared/specs/tests/test-data.md`

## Deliverables Checklist

### API Specifications
- [ ] OpenAPI 3.1 spec for `core-api` (`shared/specs/api/core-api.yaml`)
- [ ] All REST endpoints documented
- [ ] Request/response schemas defined
- [ ] Authentication/authorization documented

### Event Specifications
- [ ] AsyncAPI spec for domain events (`shared/specs/events/domain-events.yaml`)
- [ ] All commands documented
- [ ] All events documented
- [ ] Topic mappings defined
- [ ] Event handler logic documented

### Data Model Specifications
- [ ] JSON schemas for all entities (`shared/specs/models/*.json`)
- [ ] Relationships documented
- [ ] Indexes documented
- [ ] Collection names documented

### Implementation Plans
- [ ] .NET to Quarkus mapping document (`shared/specs/implementation/core-services-plan.md`)
- [ ] Technology choices documented
- [ ] Work breakdown per agent
- [ ] Dependencies identified

### Test Specifications
- [ ] API test specifications (`shared/specs/tests/api-tests.md`)
- [ ] Integration test scenarios (`shared/specs/tests/integration-tests.md`)
- [ ] Test data fixtures (`shared/specs/tests/test-data.md`)

## Agent Assignment

**Agent 0: Legacy Spec Extractor** is responsible for this entire phase.

See:
- [Agent 0 Work Package](./01-migration-phase-1-agent-work-packages.md#agent-0-legacy-spec-extraction-runs-first)
- [Agent 0 Prompt](../agents/AGENT_PROMPTS.md)

## Timeline

**Duration**: 1-2 weeks (depending on complexity of legacy code)

**Week 1**:
- Days 1-2: API specification extraction
- Days 3-4: Event/command extraction
- Day 5: Data model extraction

**Week 2**:
- Days 1-2: Implementation plan creation
- Days 3-4: Documentation and test spec updates
- Day 5: Review and validation

## Success Criteria

- [ ] All target services have complete specifications
- [ ] OpenAPI and AsyncAPI specs are valid and complete
- [ ] Implementation plans are detailed enough for agents to start work
- [ ] Test specifications enable comprehensive test coverage
- [ ] All documentation updated with extracted specs
- [ ] Phase 1 agents can begin implementation without blockers

## Dependencies

**Inputs**:
- Legacy .NET source code in `leanda-core/`
- Existing architecture documentation

**Outputs**:
- Complete specifications for Phase 1 agents
- Implementation plans
- Test specifications

## Next Steps

After Phase 0 completion:
1. Review specifications with team
2. Validate completeness
3. Begin Phase 1 implementation (Agent 5 starts Docker setup)

