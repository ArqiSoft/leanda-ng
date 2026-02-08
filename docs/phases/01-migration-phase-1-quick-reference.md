# Phase 1 Quick Reference Guide

## For All Agents

### Daily Workflow

1. **Morning**: Read `COORDINATION.md` for updates
2. **Work**: Implement assigned tasks
3. **Update**: Update `COORDINATION.md` with progress
4. **Evening**: Commit work, update test results

### Shared Artifacts Location

```
leanda-ng-core-distro/shared/
├── contracts/     # API/Event contracts
├── models/        # Data models
├── interfaces/    # Service interfaces
└── config/        # Shared config
```

### Change Protocol (Quick)

1. **Propose** → Update `COORDINATION.md` with change
2. **Wait** → 4-hour review window
3. **Implement** → If approved, make change
4. **Notify** → Update `COORDINATION.md` with notification

### Git Workflow

- **Feature Branch**: `agent-N/feature-name`
- **Daily Commits**: Commit to feature branch
- **Weekly Integration**: Merge to `integration/week-N`

---

## Agent 1: Core API

### Key Files
- `services/core-api/` - Main service
- `shared/contracts/core-api.yaml` - API contract

### Dependencies
- Needs: Docker (Agent 5), Data models (Agent 3)
- Provides: API contracts, REST endpoints

### Quick Commands
```bash
# Start service
cd services/core-api
mvn quarkus:dev

# Run tests
mvn test
mvn verify

# Generate OpenAPI
mvn quarkus:build
# Check target/openapi.json
```

---

## Agent 2: Domain Services

### Key Files
- `services/core-api/src/.../handlers/` - Event handlers
- `shared/contracts/events.yaml` - Event schemas

### Dependencies
- Needs: Docker (Agent 5), Repositories (Agent 3)
- Provides: Event schemas, Event handlers

### Quick Commands
```bash
# Test event publishing
# Use Kafka console producer
docker-compose exec redpanda rpk topic produce test-topic

# Test event consumption
# Check logs for handler execution
docker-compose logs -f core-api
```

---

## Agent 3: Persistence

### Key Files
- `shared/models/` - Data models
- `services/core-api/src/.../repositories/` - Repositories
- `services/persistence-service/` - Persistence service

### Dependencies
- Needs: Docker (Agent 5)
- Provides: Data models, Repositories

### Quick Commands
```bash
# Access MongoDB
docker-compose exec mongodb mongosh -u admin -p admin123 --authenticationDatabase admin leanda-ng

# Test repository
mvn test -Dtest=UserRepositoryTest

# Check data
db.users.find().pretty()
```

---

## Agent 4: Testing

### Key Files
- `tests/integration/` - Integration tests
- `tests/fixtures/` - Test data
- `.github/workflows/` - CI/CD (postponed until full migration)

### Dependencies
- Needs: Docker (Agent 5), Services (Agents 1-3)
- Provides: Test infrastructure, Test utilities

### Quick Commands
```bash
# Run all tests
mvn test

# Run integration tests
mvn verify

# Check coverage
mvn test jacoco:report
open target/site/jacoco/index.html
```

---

## Agent 5: Docker

### Key Files
- `docker-compose.yml` - Main compose file
- `services/*/Dockerfile.dev` - Service Dockerfiles
- `Makefile` - Common commands

### Dependencies
- Needs: None (starts first)
- Provides: Docker infrastructure

### Quick Commands
```bash
# Start all services
make up

# Check status
make status

# View logs
make logs
make logs SERVICE=core-api

# Stop services
make down

# Clean start
make clean
make up
```

---

## Common Issues & Solutions

### Port Already in Use
```bash
# Find process
lsof -i :8080

# Kill process
kill -9 <PID>

# Or change port in .env
CORE_API_PORT=8081
```

### Service Won't Start
```bash
# Check logs
docker-compose logs SERVICE_NAME

# Check health
docker-compose ps

# Restart service
docker-compose restart SERVICE_NAME
```

### Test Failures
```bash
# Run single test
mvn test -Dtest=TestName

# Debug test
mvn test -Dtest=TestName -Dmaven.surefire.debug

# Check Testcontainers
docker ps | grep testcontainers
```

### Shared Artifact Conflict
1. Check `COORDINATION.md` for pending changes
2. Propose your change
3. Wait for approval
4. Coordinate update timing

---

## Integration Checkpoint Checklist

### End of Week 1
- [ ] All services start in Docker
- [ ] Health checks pass
- [ ] First integration test passes
- [ ] All agents synced

### End of Week 2
- [ ] Core API endpoints working
- [ ] Event handlers working
- [ ] Data persistence working
- [ ] Integration tests passing

### End of Week 3
- [ ] Full domain functionality
- [ ] All integration tests pass
- [ ] Performance baseline

### End of Week 4
- [ ] File operations working
- [ ] E2E tests passing
- [ ] Data migration validated

### End of Week 5
- [ ] All tests pass
- [ ] Documentation complete
- [ ] Ready for Phase 2

---

## Emergency Contacts

### Critical Blocker
1. Tag `#urgent` in `COORDINATION.md`
2. Notify all agents immediately
3. Escalate if no response in 2 hours

### Integration Issues
1. Document in `COORDINATION.md`
2. Create integration branch
3. Coordinate fix with affected agents

### Test Failures
1. Document in `TEST_RESULTS.md`
2. Identify root cause
3. Fix or coordinate with service owner

---

## Useful Links

- [Main Plan](./01-migration-phase-1-core-in-docker.md)
- [Coordination Framework](./01-migration-phase-1-core-in-docker-coordination.md)
- [Agent Work Packages](./01-migration-phase-1-agent-work-packages.md)
- [Coordination Template](./01-migration-phase-1-coordination-template.md)

