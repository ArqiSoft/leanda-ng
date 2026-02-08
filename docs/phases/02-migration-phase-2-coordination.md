# Phase 2: Multi-Agent Coordination Framework

## Overview

This document defines the coordination framework for parallel execution of Phase 2 service migrations using multiple AI agents in Cursor.

## Coordination Structure

### Shared Artifacts Location

```
leanda-ng-phase2/
├── COORDINATION.md              # Live coordination file (updated by all agents)
├── AGENT_PROMPTS.md             # Ready-to-use prompts for each agent
├── shared/
│   ├── contracts/
│   │   ├── core-api.yaml        # OpenAPI specs
│   │   ├── events/
│   │   │   ├── chemical-parser-events.yaml
│   │   │   ├── blob-events.yaml
│   │   │   └── ...
│   │   └── ml-services/
│   │       └── ml-api.yaml
│   └── models/
│       ├── File.java
│       ├── User.java
│       ├── Record.java
│       └── ...
├── scripts/
│   ├── check-status.sh          # Check agent status
│   ├── check-dependencies.sh    # Check service dependencies
│   └── validate-contracts.sh    # Validate API contracts
└── README.md
```

### COORDINATION.md Format

The coordination file is a live document updated by all agents:

```markdown
# Phase 2 Coordination Status

Last Updated: 2025-01-XX

## Agent Status

### Agent 1: Java Parsers Group A
- Status: In Progress
- Services: Chemical Parser, Chemical Properties, Reaction Parser
- Current Task: Implementing Chemical Parser command handler
- Blockers: None
- Dependencies Met: ✅ Blob Storage API contract
- Next: Complete Chemical Parser, start Chemical Properties

### Agent 2: Java Parsers Group B
- Status: Pending
- Services: Crystal Parser, Spectra Parser, Imaging Service
- Current Task: Waiting for Agent 1 to complete message contracts
- Blockers: Need shared event schemas
- Dependencies Met: ⏳ Waiting for shared contracts
- Next: Start Crystal Parser implementation

[... other agents ...]

## Shared Artifacts Status

### Contracts
- [x] Blob Storage API (OpenAPI 3.1)
- [x] Chemical Parser Events (AsyncAPI)
- [ ] Chemical Properties Events
- [ ] Crystal Parser Events
- [...]

### Models
- [x] File.java
- [x] User.java
- [ ] Record.java
- [...]

## Integration Checkpoints

### Week 1 Checkpoint (YYYY-MM-DD)
- [ ] All message contracts defined
- [ ] All shared models defined
- [ ] Docker infrastructure ready

### Week 2 Checkpoint (YYYY-MM-DD)
- [ ] Agent 1: Chemical Parser complete
- [ ] Agent 3: Blob Storage complete
- [ ] Integration test: Chemical Parser + Blob Storage

[... more checkpoints ...]
```

## Agent Responsibilities

### Agent 1: Java Parsers Group A
- **Services**: Chemical Parser, Chemical Properties, Reaction Parser
- **Deliverables**:
  - Chemical Parser Quarkus service
  - Chemical Properties Quarkus service
  - Reaction Parser Quarkus service
  - Message contracts (AsyncAPI)
- **Updates COORDINATION.md**: Daily status, blockers, completed tasks

### Agent 2: Java Parsers Group B
- **Services**: Crystal Parser, Spectra Parser, Imaging Service
- **Deliverables**:
  - Crystal Parser Quarkus service
  - Spectra Parser Quarkus service
  - Imaging Service Quarkus service
  - Message contracts
- **Updates COORDINATION.md**: Daily status

### Agent 3: Blob Storage + Indexing
- **Services**: Blob Storage, Office Processor
- **Deliverables**:
  - Blob Storage Quarkus service
  - Office Processor Quarkus service
  - OpenAPI specifications
- **Updates COORDINATION.md**: API contracts, service status

### Agent 4: Metadata + Core Services
- **Services**: Metadata Processing, Indexing Service
- **Deliverables**:
  - Metadata Processing Quarkus service
  - Indexing Service Quarkus service
  - OpenSearch integration
- **Updates COORDINATION.md**: Service status, search functionality

### Agent 5: ML Services
- **Services**: Feature Calculator, Modeler, Predictor
- **Deliverables**:
  - FastAPI services (3 services)
  - Updated dependencies
  - Kafka integration
- **Updates COORDINATION.md**: Service status, ML functionality

### Agent 6: Frontend
- **Service**: Angular 21 Frontend
- **Deliverables**:
  - Angular 21 application
  - Migrated components and views
  - Playwright E2E tests
- **Updates COORDINATION.md**: UI status, integration points

### Agent 7: Testing Infrastructure
- **Scope**: Testing framework, CI/CD (CI/CD postponed until full migration is complete)
- **Deliverables**:
  - Test utilities
  - Integration test framework
  - CI/CD pipelines (postponed until full migration)
- **Updates COORDINATION.md**: Test coverage, CI/CD status

### Agent 8: Docker + Integration
- **Scope**: Docker Compose, service integration
- **Deliverables**:
  - Updated docker-compose.yml
  - Service integration tests
  - Deployment scripts
- **Updates COORDINATION.md**: Infrastructure status

## Coordination Rules

### 1. Shared Artifacts
- **Contracts**: All API/event contracts go in `shared/contracts/`
- **Models**: Shared domain models go in `shared/models/`
- **No Direct Edits**: Agents must propose changes via COORDINATION.md first

### 2. Dependency Management
- **Check Dependencies**: Before starting work, check COORDINATION.md for dependencies
- **Update Status**: When dependencies are met, update COORDINATION.md
- **Blockers**: If blocked, update COORDINATION.md immediately

### 3. Integration Checkpoints
- **Weekly Checkpoints**: All agents must report status by Friday EOD
- **Integration Tests**: Run integration tests at checkpoints
- **Merge Conflicts**: Resolve conflicts immediately, update COORDINATION.md

### 4. Change Coordination
- **Propose Changes**: Post proposed changes in COORDINATION.md
- **Review Window**: 4-hour review window for shared artifacts
- **Approval**: If no objections, implement after review window

## Agent Workflow

### Daily Workflow

1. **Read COORDINATION.md** - Check status, dependencies, blockers
2. **Check Dependencies** - Verify all dependencies are met
3. **Update Status** - Set status to "In Progress"
4. **Do Work** - Implement assigned tasks
5. **Update Artifacts** - Commit shared artifacts if created
6. **Update COORDINATION.md** - Update status, completed tasks, blockers
7. **Run Tests** - Run unit/integration tests
8. **Commit Changes** - Commit work with clear messages

### Weekly Checkpoint Workflow

1. **Status Report** - Update COORDINATION.md with week's progress
2. **Integration Test** - Run integration tests with other services
3. **Documentation** - Update service documentation
4. **Next Week Planning** - Plan next week's work in COORDINATION.md

## Conflict Resolution

### Shared Artifact Conflicts
1. **Identify Conflict** - Check COORDINATION.md for proposed changes
2. **Discuss** - Add discussion in COORDINATION.md comments
3. **Resolve** - Agree on resolution, update COORDINATION.md
4. **Implement** - Implement agreed-upon changes

### Code Conflicts
1. **Pull Latest** - Always pull latest before starting work
2. **Resolve Immediately** - Don't let conflicts accumulate
3. **Update COORDINATION.md** - Note conflict resolution

## Success Metrics

### Per Agent
- [ ] All assigned services implemented
- [ ] Unit test coverage >80%
- [ ] Integration tests passing
- [ ] Documentation complete
- [ ] COORDINATION.md updated daily

### Overall
- [ ] All 12 services migrated
- [ ] All message contracts defined
- [ ] All integration tests passing
- [ ] Docker Compose working
- [ ] End-to-end tests passing

---

## Quick Reference

### Check Status
```bash
./scripts/check-status.sh
```

### Check Dependencies
```bash
./scripts/check-dependencies.sh <service-name>
```

### Validate Contracts
```bash
./scripts/validate-contracts.sh
```

### Update Coordination
1. Read `COORDINATION.md`
2. Update your agent's section
3. Commit changes

