# Claude Code Agent Prompts for Leanda NG

Ready-to-use prompts optimized for Claude Code (CLI) working on the Leanda NG modernization project.

**Current Status**:
- Phase 1: Complete
- Phase 2: Complete
- Phase 3: Skipped
- Phase 4: 86% Complete (6/7 agents done)
- Continuous: Active (Team Lead, QA, UI/UX)

---

## How to Use These Prompts

1. Start Claude Code in the project root: `claude`
2. Copy the prompt for your desired agent role
3. Paste into Claude Code and press Enter
4. Claude Code will read necessary files and begin work

---

## General Instructions for Claude Code Agents

When working as any agent:

1. **First, read coordination status**:
   - Read `docs/agents/COORDINATION.md`
   - Check dependencies and blockers
   - Verify prerequisites are complete

2. **Use TodoWrite for task tracking**:
   - Create todo list at start of work
   - Mark tasks in_progress/completed
   - Track blockers

3. **Follow standards**:
   - 80%+ test coverage
   - Update service READMEs
   - Create/update contracts in `shared/`

4. **Update status**:
   - Edit COORDINATION.md when starting/completing work
   - Document results and blockers

---

## Active Agent Prompts

### Agent: Team Lead (Technology Oversight)

**Status**: Continuous

```
I need you to act as the Team Lead agent for Leanda NG. Your role is technology oversight and best practices enforcement.

First, read these files to understand current state:
1. docs/agents/COORDINATION.md - Check project status
2. CLAUDE.md - Review technology standards

Your responsibilities:
1. Monitor latest stable versions of technologies (Java, Quarkus, Angular, AWS)
2. Enforce coding standards and best practices
3. Review security advisories for dependencies
4. Coordinate technology decisions

Please start by:
1. Reading COORDINATION.md
2. Checking current dependency versions in services/*/pom.xml
3. Identifying any outdated dependencies
4. Reporting findings with recommendations

Use TodoWrite to track your review tasks.
```

### Agent: QA-Cloud (Testing Strategies)

**Status**: Continuous

```
I need you to act as the Senior Cloud QA agent for Leanda NG. Your role is continuous testing strategy and quality assurance.

First, read these files:
1. docs/agents/COORDINATION.md - Check current QA status
2. docs/testing/testing-strategy.md - Review testing approach
3. docs/testing/integration-test-inventory.md - Check test coverage

Your responsibilities:
1. Review test coverage across all services
2. Identify gaps in testing
3. Recommend testing improvements
4. Guide on cloud-native testing patterns

Please start by:
1. Using Explore agent to analyze test files in tests/ and services/*/src/test/
2. Creating a coverage report
3. Identifying critical gaps
4. Proposing improvements

Use TodoWrite to track your analysis tasks.
```

### Agent: QA-Test-Impl (Test Implementation)

**Status**: Continuous

```
I need you to act as the Integration Test Implementation agent for Leanda NG.

First, read these files:
1. docs/agents/COORDINATION.md - Check test implementation status
2. docs/testing/INTEGRATION_TEST_GAP_ANALYSIS_DETAILED.md - Review gaps
3. docs/testing/TEST_PLANS_FOR_GAPS.md - Review planned tests

Your responsibilities:
1. Implement missing integration tests
2. Ensure contract compliance testing
3. Add workflow tests across services
4. Maintain test documentation

Please start by:
1. Reading the gap analysis documents
2. Identifying highest priority tests to implement
3. Creating todo list with specific tests to write
4. Implementing tests one by one

Focus areas:
- Contract compliance tests (OpenAPI/AsyncAPI)
- Cross-service workflow tests
- Error handling tests
```

### Agent: UI-UX (Frontend Design)

**Status**: Continuous

```
I need you to act as the Senior UI/UX Engineer agent for Leanda NG.

First, read these files:
1. docs/agents/COORDINATION.md - Check frontend status
2. frontend/README.md - Review frontend architecture
3. frontend/MIGRATION_STATUS.md - Check migration progress

Your responsibilities:
1. Review component architecture and patterns
2. Ensure accessibility compliance (WCAG 2.1 AA)
3. Guide on responsive design
4. Recommend UX improvements

Please start by:
1. Using Explore agent to analyze frontend/src/ structure
2. Reviewing component organization
3. Checking for accessibility issues
4. Documenting recommendations

Use TodoWrite to track your review tasks.
```

### Agent: PROD-6 (Saga Pattern Modernization)

**Status**: Planned (Ready to Start)

```
I need you to act as Agent PROD-6 for Saga Pattern Modernization in Leanda NG.

First, read these files:
1. docs/agents/COORDINATION.md - Check PROD-6 section for requirements
2. docs/legacy-sagas-inventory.md - Review legacy saga implementations
3. shared/contracts/events/ - Review existing event contracts

Your scope:
- Modernize legacy MassTransit/Automatonymous sagas
- Design AWS Step Functions workflows
- Create saga orchestration in core-api
- Implement compensation patterns

Your workflow:
1. Analyze all 16 legacy saga types from inventory
2. Design modern saga contracts (AsyncAPI)
3. Create FileProcessingOrchestrator in core-api
4. Implement Step Functions CDK stack
5. Create migration strategy

Please start by:
1. Reading the legacy sagas inventory
2. Creating a todo list with analysis tasks
3. Documenting each saga's state machine
4. Designing the modern orchestration approach

Success criteria:
- All 16 legacy sagas analyzed
- Modern contracts designed
- Orchestrator implemented
- Step Functions workflows created
- Tests passing (80%+ coverage)
```

---

## Exploration Prompts

### Explore Codebase Structure

```
I need you to explore and document the Leanda NG codebase structure.

Use the Explore agent to:
1. Map out all services in services/
2. Document the shared/ directory structure
3. List all contracts in shared/contracts/
4. Identify infrastructure components
5. Document the testing structure

Create a summary report with:
- Service inventory with their purposes
- Contract types and coverage
- Test organization
- Key configuration files
```

### Explore Service Architecture

```
I need you to explore a specific service's architecture.

Please analyze the [SERVICE_NAME] service:
1. Read the service README
2. Explore the directory structure
3. Identify main components (controllers, handlers, services)
4. Review event producers/consumers
5. Check test coverage

Report on:
- Architecture pattern used
- Dependencies on other services
- Events published and consumed
- Test coverage and gaps
```

### Explore Testing Patterns

```
I need you to explore the testing patterns used in this project.

Use the Explore agent to analyze:
1. tests/integration/ - Integration test patterns
2. tests/e2e/ - End-to-end test patterns
3. services/*/src/test/ - Service unit tests
4. frontend/src/**/*.spec.ts - Frontend tests

Document:
- Base test classes and utilities
- Mocking strategies
- Test data management
- CI/CD integration (CI/CD postponed until full migration is complete)
```

---

## Implementation Prompts

### Add New Endpoint

```
I need you to add a new endpoint to a service.

Service: [SERVICE_NAME]
Endpoint: [DESCRIPTION]

Please:
1. Read the existing service code to understand patterns
2. Read the OpenAPI contract if it exists
3. Create todo list for implementation
4. Implement the endpoint following existing patterns
5. Add unit and integration tests
6. Update the OpenAPI contract
7. Run tests to verify

Follow these standards:
- Use RESTEasy Reactive
- Proper error handling
- Input validation
- Documentation
```

### Add Integration Test

```
I need you to add integration tests for a scenario.

Scenario: [DESCRIPTION]
Services involved: [LIST]

Please:
1. Read tests/integration/ to understand patterns
2. Read BaseIntegrationTest for utilities
3. Create the test class following conventions
4. Implement test cases covering:
   - Happy path
   - Error cases
   - Edge cases
5. Run tests to verify
6. Update test documentation

Ensure tests use:
- @RequiresServices annotation for dependencies
- Testcontainers for infrastructure
- Proper cleanup between tests
```

### Add CDK Stack

```
I need you to add a new CDK stack for infrastructure.

Resource: [DESCRIPTION]
Purpose: [PURPOSE]

Please:
1. Read infrastructure/lib/stacks/ to understand patterns
2. Read the tagging utility for cost allocation
3. Create the new stack following conventions
4. Add proper dependencies in bin/leanda-ng.ts
5. Apply cost allocation tags
6. Test with cdk synth

Follow these standards:
- Multi-environment support (dev/staging/prod)
- KMS encryption for data at rest
- Security best practices
- Proper stack outputs
```

---

## Maintenance Prompts

### Update Dependencies

```
I need you to check and update project dependencies.

Please:
1. Check Java dependencies in services/*/pom.xml
2. Check frontend dependencies in frontend/package.json
3. Check infrastructure dependencies in infrastructure/package.json
4. Identify outdated or vulnerable dependencies
5. Propose updates with compatibility notes
6. Create a dependency update plan

Focus on:
- Security vulnerabilities (CVEs)
- Major version upgrades
- Deprecated packages
```

### Health Check All Services

```
I need you to verify the health of all services.

Please:
1. Start local development environment (docker-compose up)
2. Check health endpoints for all services
3. Verify Kafka connectivity
4. Verify MongoDB connectivity
5. Verify OpenSearch connectivity
6. Report any issues

Run:
- cd docker && docker-compose up -d
- Check each service's /q/health endpoint
- Report status for each service
```

### Run Full Test Suite

```
I need you to run the complete test suite.

Please:
1. Run Java service tests: cd services/[service] && mvn test
2. Run integration tests: cd tests/integration && mvn test
3. Run frontend tests: cd frontend && npm test
4. Run E2E tests: cd frontend && npm run e2e
5. Report results with any failures

Create a summary with:
- Total tests run
- Pass/fail counts
- Failed test details
- Coverage metrics
```

---

## Documentation Prompts

### Create ADR

```
I need you to create an Architecture Decision Record.

Decision: [TITLE]
Context: [CONTEXT]

Please create an ADR in docs/adr/ following this format:
1. Title (ADR-NNNN: Title)
2. Status (Proposed/Accepted/Deprecated)
3. Context (Why this decision is needed)
4. Decision (What we decided)
5. Consequences (Positive and negative impacts)
6. Alternatives Considered

Reference existing ADRs in docs/adr/ for format.
```

### Update Service README

```
I need you to update or create the README for a service.

Service: [SERVICE_NAME]

The README should include:
1. Service description and purpose
2. Technology stack
3. API endpoints (if REST)
4. Events published/consumed
5. Configuration options
6. Local development setup
7. Testing instructions
8. Deployment notes

Read the service code to gather accurate information.
```

### Document API Endpoints

```
I need you to document the API endpoints for a service.

Service: [SERVICE_NAME]

Please:
1. Read the service controllers/resources
2. Create or update OpenAPI spec in shared/contracts/
3. Document each endpoint with:
   - Path and method
   - Request/response schemas
   - Authentication requirements
   - Example requests/responses
4. Ensure spec validates with OpenAPI tools
```

---

## Quick Commands

These are simple commands you can give to Claude Code:

```
# Check project status
"Read COORDINATION.md and summarize the current status"

# Find files
"Find all files related to [topic]"

# Run specific tests
"Run tests for the [service] service"

# Check service health
"Check if all Docker services are running and healthy"

# View logs
"Show me the logs for [service]"

# Start development environment
"Start the local development environment"

# Update a file
"Update [file] to [change]"

# Create a todo list
"Create a todo list for [task]"
```

---

## Troubleshooting Commands

```
# Service won't start
"Check docker-compose logs for [service] and diagnose the issue"

# Tests failing
"Run tests for [service] with verbose output and explain failures"

# Dependency issues
"Check Maven dependencies for [service] and look for conflicts"

# Port conflicts
"Check what's using port [PORT] and how to resolve"

# Database issues
"Check MongoDB connection and verify database is accessible"
```

---

**See Also**:
- `CLAUDE_COORDINATION.md` - Claude Code coordination guide
- `COORDINATION.md` - Full agent status and dependencies
- `README.md` - Agent system overview
- `CLAUDE.md` - Main Claude Code configuration
