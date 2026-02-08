# Phase 2: Agent Work Packages

## Overview

This document defines detailed work packages for each of the 8 agents executing Phase 2 service migrations in parallel.

---

## Agent 1: Java Parsers Group A

### Scope
Migrate Chemical Parser, Chemical Properties, and Reaction Parser services from Java 8/Spring Boot to Java 21/Quarkus.

### Services
1. **Chemical File Parser** - Parse MOL/SDF/CDX files
2. **Chemical Properties** - Calculate molecular properties
3. **Reaction File Parser** - Parse RDF/RXN/CDX reaction files

### Deliverables

1. **Chemical Parser Service** (`services/chemical-parser/`)
   - Quarkus service implementation
   - Indigo SDK integration
   - Kafka command/event handling
   - Unit tests (>80% coverage)

2. **Chemical Properties Service** (`services/chemical-properties/`)
   - Quarkus service implementation
   - Indigo SDK + InChI integration
   - Property calculation logic
   - Unit tests (>80% coverage)

3. **Reaction Parser Service** (`services/reaction-parser/`)
   - Quarkus service implementation
   - Indigo SDK integration
   - Reaction parsing logic
   - Unit tests (>80% coverage)

4. **Message Contracts** (`shared/contracts/events/`)
   - `chemical-parser-events.yaml` (AsyncAPI)
   - `chemical-properties-events.yaml` (AsyncAPI)
   - `reaction-parser-events.yaml` (AsyncAPI)

### Week-by-Week Breakdown

#### Week 1
- **Day 1-2**: Analyze legacy services, define message contracts
- **Day 3-4**: Create Quarkus projects, set up Indigo SDK
- **Day 5**: Publish message contracts to `shared/contracts/`

**Deliverables**:
- [ ] Message contracts defined (AsyncAPI)
- [ ] Quarkus projects created
- [ ] Indigo SDK integrated

#### Week 2
- **Day 1-3**: Implement Chemical Parser service
- **Day 4-5**: Implement Chemical Properties service

**Deliverables**:
- [ ] Chemical Parser complete
- [ ] Chemical Properties complete
- [ ] Unit tests passing

#### Week 3
- **Day 1-3**: Implement Reaction Parser service
- **Day 4-5**: Integration testing, documentation

**Deliverables**:
- [ ] Reaction Parser complete
- [ ] Integration tests passing
- [ ] Documentation complete

### Dependencies

**Needs From**:
- Agent 3: Blob Storage API contract (Week 1 Day 1)
- Agent 8: Kafka infrastructure (Week 1 Day 1)

**Provides To**:
- Agent 4: Parsed chemical data for indexing
- Agent 5: Parsed molecules for ML

### Success Criteria
- [ ] All 3 services implemented
- [ ] Message contracts complete
- [ ] Unit test coverage >80%
- [ ] Integration tests passing

---

## Agent 2: Java Parsers Group B

### Scope
Migrate Crystal Parser, Spectra Parser, and Imaging Service from Java 8/Spring Boot to Java 21/Quarkus.

### Services
1. **Crystal File Parser** - Parse CIF files
2. **Spectra File Parser** - Parse JCAMP-DX files
3. **Imaging Service** - Generate thumbnails from scientific files

### Deliverables

1. **Crystal Parser Service** (`services/crystal-parser/`)
   - Quarkus service implementation
   - CIF parser ported to Java 21
   - Kafka integration
   - Unit tests

2. **Spectra Parser Service** (`services/spectra-parser/`)
   - Quarkus service implementation
   - JCAMP parser ported to Java 21
   - Kafka integration
   - Unit tests

3. **Imaging Service** (`services/imaging/`)
   - Quarkus service implementation
   - All rasterizers ported
   - Kafka integration
   - Unit tests

4. **Message Contracts** (`shared/contracts/events/`)
   - `crystal-parser-events.yaml`
   - `spectra-parser-events.yaml`
   - `imaging-events.yaml`

### Week-by-Week Breakdown

#### Week 1
- **Day 1-2**: Port CIF parser to Java 21
- **Day 3-4**: Port JCAMP parser to Java 21
- **Day 5**: Define message contracts

#### Week 2
- **Day 1-3**: Implement Crystal Parser service
- **Day 4-5**: Implement Spectra Parser service

#### Week 3
- **Day 1-3**: Port rasterizers, implement Imaging service
- **Day 4-5**: Integration testing, documentation

### Dependencies

**Needs From**:
- Agent 3: Blob Storage API (Week 1 Day 1)
- Agent 8: Kafka infrastructure (Week 1 Day 1)

**Provides To**:
- Agent 4: Parsed crystal/spectra data
- Agent 6: Thumbnail images

### Success Criteria
- [ ] All 3 services implemented
- [ ] All parsers ported to Java 21
- [ ] Unit test coverage >80%
- [ ] Integration tests passing

---

## Agent 3: Blob Storage + Office Processor

### Scope
Migrate Blob Storage API and Office Processor services.

### Services
1. **Blob Storage API** - File upload/download service
2. **Office Processor** - Office document conversion and metadata extraction

### Deliverables

1. **Blob Storage Service** (`services/blob-storage/`)
   - Quarkus REST API
   - MongoDB GridFS adapter
   - OpenAPI 3.1 specification
   - Unit tests

2. **Office Processor Service** (`services/office-processor/`)
   - Quarkus service
   - PDF converters ported
   - Metadata extractors ported
   - Unit tests

3. **API Contracts** (`shared/contracts/`)
   - `blob-storage-api.yaml` (OpenAPI 3.1)
   - `office-processor-events.yaml` (AsyncAPI)

### Week-by-Week Breakdown

#### Week 1
- **Day 1-2**: Analyze legacy services, design API contracts
- **Day 3-4**: Create Quarkus projects
- **Day 5**: Publish OpenAPI specification

#### Week 2
- **Day 1-3**: Implement Blob Storage service
- **Day 4-5**: Implement Office Processor service

#### Week 3
- **Day 1-3**: Integration testing
- **Day 4-5**: Documentation, performance testing

### Dependencies

**Needs From**:
- Agent 8: MongoDB infrastructure (Week 1 Day 1)
- Agent 8: Kafka infrastructure (Week 1 Day 1)

**Provides To**:
- All agents: Blob storage interface
- Agent 1, 2: File download/upload

### Success Criteria
- [ ] Blob Storage API complete
- [ ] Office Processor complete
- [ ] OpenAPI specification complete
- [ ] Unit test coverage >80%

---

## Agent 4: Metadata + Indexing

### Scope
Migrate Metadata Processing and Indexing services.

### Services
1. **Metadata Processing** - Generate metadata infoboxes
2. **Indexing Service** - Index entities to OpenSearch

### Deliverables

1. **Metadata Processing Service** (`services/metadata-processing/`)
   - Quarkus service
   - Type qualifier ported
   - MongoDB integration
   - Unit tests

2. **Indexing Service** (`services/indexing/`)
   - Quarkus service
   - OpenSearch Serverless integration
   - Text extraction (Apache Tika)
   - Unit tests

3. **Message Contracts** (`shared/contracts/events/`)
   - `metadata-events.yaml`
   - `indexing-events.yaml`

### Week-by-Week Breakdown

#### Week 1
- **Day 1-2**: Port Type Qualifier to Java
- **Day 3-4**: Set up OpenSearch Serverless
- **Day 5**: Define message contracts

#### Week 2
- **Day 1-3**: Implement Metadata Processing service
- **Day 4-5**: Implement Indexing service

#### Week 3
- **Day 1-3**: Integration testing
- **Day 4-5**: Documentation, search validation

### Dependencies

**Needs From**:
- Agent 3: Blob Storage API (for text extraction)
- Agent 8: OpenSearch Serverless infrastructure
- Agent 8: MongoDB access

**Provides To**:
- Agent 6: Search functionality
- Core API: Metadata for infoboxes

### Success Criteria
- [ ] Metadata Processing complete
- [ ] Indexing Service complete
- [ ] OpenSearch integration working
- [ ] Unit test coverage >80%

---

## Agent 5: ML Services

### Scope
Modernize ML Services to Python 3.12+ / FastAPI.

### Services
1. **Feature Vector Calculator** - Calculate molecular features
2. **ML Modeler** - Train and optimize ML models
3. **ML Predictor** - Predict properties using trained models

### Deliverables

1. **Feature Vector Calculator** (`ml-services/feature-vectors/`)
   - FastAPI application
   - RDKit integration
   - Kafka integration
   - Unit tests

2. **ML Modeler** (`ml-services/modeler/`)
   - FastAPI application
   - Training service
   - Optimization service
   - Report generator
   - Unit tests

3. **ML Predictor** (`ml-services/predictor/`)
   - FastAPI application
   - Batch predictor
   - Single structure predictor
   - Unit tests

4. **API Contracts** (`shared/contracts/ml-services/`)
   - `ml-api.yaml` (OpenAPI 3.1)

### Week-by-Week Breakdown

#### Week 1
- **Day 1-2**: Update dependencies (Python 3.12+, FastAPI)
- **Day 3-4**: Create FastAPI projects
- **Day 5**: Define API contracts

#### Week 2
- **Day 1-3**: Refactor Feature Vector Calculator
- **Day 4-5**: Refactor ML Modeler

#### Week 3
- **Day 1-3**: Refactor ML Predictor
- **Day 4-5**: Integration testing, ML validation

### Dependencies

**Needs From**:
- Agent 3: Blob Storage API
- Agent 1: Chemical Parser (for parsed molecules)
- Agent 8: Kafka infrastructure

**Provides To**:
- Agent 6: ML prediction UI
- Core API: ML predictions

### Success Criteria
- [ ] All 3 services modernized
- [ ] Python 3.12+ compatibility
- [ ] FastAPI applications working
- [ ] Unit test coverage >80%

---

## Agent 6: Frontend

### Scope
Migrate Angular 9 frontend to Angular 21.

### Service
1. **Angular 21 Application** - Complete frontend rewrite

### Deliverables

1. **Angular 21 Application** (`frontend/`)
   - Angular 21 project
   - All views migrated
   - Signal Forms (where applicable)
   - SignalR updated to `@microsoft/signalr`
   - Playwright E2E tests

2. **Component Library**
   - All shared components migrated
   - All views migrated
   - Services updated

3. **Documentation**
   - Migration guide
   - Component documentation

### Week-by-Week Breakdown

#### Week 1
- **Day 1-2**: Create Angular 21 project, set up routing
- **Day 3-4**: Migrate core services (API, Auth, SignalR)
- **Day 5**: Migrate shared components

#### Week 2
- **Day 1-3**: Migrate views (Home, Organize, File View)
- **Day 4-5**: Migrate remaining views

#### Week 3
- **Day 1-3**: Update SignalR, implement Signal Forms
- **Day 4-5**: Playwright E2E tests

#### Week 4
- **Day 1-3**: Integration testing with backend
- **Day 4-5**: Documentation, deployment

### Dependencies

**Needs From**:
- Agent 1-5: All backend APIs
- Agent 8: Infrastructure (S3, CloudFront)

**Provides To**:
- End users: Web interface

### Success Criteria
- [ ] Angular 21 application complete
- [ ] All views migrated
- [ ] Playwright E2E tests passing
- [ ] Unit test coverage >80%
- [ ] Deployed to S3 + CloudFront

---

## Agent 7: Testing Infrastructure

### Scope
Set up comprehensive testing infrastructure for Phase 2.

### Deliverables

1. **Test Utilities** (`tests/`)
   - Testcontainers configuration
   - Test base classes
   - Test data fixtures
   - Mock utilities

2. **Integration Test Framework**
   - Service integration tests
   - End-to-end test framework
   - Test orchestration

3. **CI/CD Pipeline** (`.github/workflows/`) — CI/CD is postponed until full migration is complete.
   - Unit test pipeline
   - Integration test pipeline
   - Coverage reporting

### Week-by-Week Breakdown

#### Week 1
- **Day 1-2**: Set up Testcontainers (MongoDB, Kafka, OpenSearch)
- **Day 3-4**: Create test base classes
- **Day 5**: Create test utilities

#### Week 2+
- **Continuous Support**:
  - Create test fixtures as needed
  - Support other agents with testing
  - Set up CI/CD pipelines (CI/CD postponed until full migration is complete)
  - Maintain test documentation

### Dependencies

**Needs From**:
- All agents: Service implementations for testing

**Provides To**:
- All agents: Test infrastructure, utilities

### Success Criteria
- [ ] Testcontainers configured
- [ ] Test utilities available
- [ ] CI/CD pipeline functional
- [ ] Integration test framework ready

---

## Agent 8: Docker + Integration

### Scope
Set up Docker Compose and service integration.

### Deliverables

1. **Docker Compose** (`docker-compose.yml`)
   - All Phase 2 services
   - Infrastructure services
   - Networking configuration

2. **Integration Tests**
   - Service-to-service integration
   - End-to-end workflows
   - Performance tests

3. **Deployment Scripts**
   - Service deployment scripts
   - Health check scripts
   - Monitoring setup

### Week-by-Week Breakdown

#### Week 1
- **Day 1-2**: Update docker-compose.yml with Phase 2 services
- **Day 3-4**: Set up service networking
- **Day 5**: Create integration test framework

#### Week 2+
- **Continuous Support**:
  - Update Docker setup as services are completed
  - Run integration tests
  - Support other agents with infrastructure needs

### Dependencies

**Needs From**:
- All agents: Service implementations

**Provides To**:
- All agents: Docker infrastructure, integration testing

### Success Criteria
- [ ] Docker Compose complete
- [ ] All services start successfully
- [ ] Integration tests passing
- [ ] Deployment scripts ready

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
- **End of Week 1**: All message contracts defined
- **End of Week 2**: First services integrated
- **End of Week 3**: Major services integrated
- **End of Week 4**: Full stack integration

### Change Coordination
When changing shared artifacts:
1. Propose in `COORDINATION.md`
2. Wait for review (4-hour window)
3. Implement if approved
4. Notify all agents

---

## Success Metrics Per Agent

### Agent 1 (Java Parsers A)
- Services: 3 services
- Test coverage: >80%
- Message contracts: Complete

### Agent 2 (Java Parsers B)
- Services: 3 services
- Test coverage: >80%
- Parsers ported: All

### Agent 3 (Blob + Office)
- Services: 2 services
- API documentation: Complete
- Test coverage: >80%

### Agent 4 (Metadata + Indexing)
- Services: 2 services
- OpenSearch: Integrated
- Test coverage: >80%

### Agent 5 (ML Services)
- Services: 3 services
- Python: 3.12+
- Test coverage: >80%

### Agent 6 (Frontend)
- Application: Angular 21
- E2E tests: Playwright
- Test coverage: >80%

### Agent 7 (Testing)
- Test utilities: Complete
- CI/CD: Functional (postponed until full migration)
- Framework: Ready

### Agent 8 (Docker + Integration)
- Docker Compose: Complete
- Integration tests: Passing
- Deployment: Ready

