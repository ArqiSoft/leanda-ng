# Integration Testing Documentation

This directory contains documentation for the Leanda integration testing infrastructure.

## Status

- **Test Infrastructure**: ✅ Fully functional
- **Minimal Distribution Tests**: ⚠️ Partially passing (2/5) due to known limitation
- **Docker Infrastructure**: ✅ All services operational

## Which script?

| Goal | Script |
|------|--------|
| **E2E locally vs EC2 APIs** (frontend + Playwright, backend on EC2) | `./scripts/run-e2e-local-ec2.sh` — resolves EC2 IP, tunnel + local frontend + Phase 1 tests. Use `--deploy` to deploy minimal on EC2 first. |
| Backend integration, EC2 infra + local JVM apps (Java tests only) | `./scripts/run-e2e-minimal-ec2-tunnel.sh` |
| Backend integration, all on EC2 (build + run on EC2) | `./scripts/run-system-integration-tests-ec2-tunnel.sh --minimal` |
| Local-only (Docker infra + local JVM, frontend E2E) | `./scripts/start-minimal-distro-local.sh` then `./scripts/run-frontend-e2e-minimal-local.sh` |

See [E2E_LOCAL_EC2.md](./E2E_LOCAL_EC2.md) for E2E vs EC2; [RAPID_E2E_TESTING.md](./RAPID_E2E_TESTING.md) for local-only.

## Key Documents

### E2E locally against EC2 APIs and infra
- **[E2E_LOCAL_EC2.md](./E2E_LOCAL_EC2.md)** - Run E2E tests locally connecting to EC2 backend and infra
  - **One command**: `./scripts/run-e2e-local-ec2.sh` (resolves EC2 IP, tunnel + local frontend + Phase 1 tests)
  - With deploy first: `./scripts/run-e2e-local-ec2.sh --deploy`
  - Or: `./scripts/run-phase1-tests-ec2.sh --skip-infra` after setting `EC2_PUBLIC_IP`

### Rapid E2E Testing
- **[RAPID_E2E_TESTING.md](./RAPID_E2E_TESTING.md)** - Guide for rapid E2E testing with local JVM services
  - Infrastructure in Docker, application services in local JVM
  - Faster iteration, easier debugging, hot reload support
  - Scripts: `start-minimal-distro-local.sh`, `run-integration-tests-minimal-local.sh`, `run-frontend-e2e-minimal-local.sh`

### Test Infrastructure
- **[test-runner-ec2.md](./test-runner-ec2.md)** - Cost-optimized EC2 instance for integration/E2E testing
  - Auto-stops after 30 minutes of inactivity
  - Pre-configured with Docker, Java 21, Maven
  - Estimated cost: ~$8/month (mostly EBS storage when stopped)

### Authentication Testing
- **[AUTHENTICATION_SETUP.md](./AUTHENTICATION_SETUP.md)** - Backend authentication configuration and status
  - Frontend: ✅ OIDC implemented
  - Backend: ❌ Authentication not yet implemented
  - Tests: ✅ Created (handle both states)
- **[AUTHENTICATION_TESTS.md](./AUTHENTICATION_TESTS.md)** - Authentication test documentation
  - Integration tests: `tests/integration/src/test/java/io/leanda/tests/integration/auth/`
  - E2E tests: `frontend/e2e/integration/auth.spec.ts`, `login-flow.spec.ts`

### Test Status & Results
- **[MINIMAL_DISTRIBUTION_TEST_STATUS.md](./MINIMAL_DISTRIBUTION_TEST_STATUS.md)** - Current test results and status
- Passing: 2/5 tests (blob-storage operations, OpenSearch connectivity)
- Failing: 3/5 tests (imaging, office-processor, indexing) - Jandex limitation

### Technical Issues
- **[JANDEX_REST_CLIENT_LIMITATION.md](./JANDEX_REST_CLIENT_LIMITATION.md)** - Detailed analysis of Quarkus limitation
- Root cause: REST client interfaces in external JARs cannot be used in local JAR mode
- Solution: Use Docker for service deployment (works correctly)

## Quick Reference

### Rapid E2E Testing (Recommended for Development)

```bash
# Start minimal distribution (infra in Docker, apps in JVM)
./scripts/start-minimal-distro-local.sh

# Run backend integration tests
./scripts/run-integration-tests-minimal-local.sh

# Run frontend E2E tests
./scripts/run-frontend-e2e-minimal-local.sh

# Run all E2E tests
./scripts/run-all-e2e-minimal-local.sh

# Stop services
./scripts/stop-minimal-distro-local.sh
```

See [RAPID_E2E_TESTING.md](./RAPID_E2E_TESTING.md) for detailed guide.

### Running Tests (Traditional Docker Mode)

```bash
# Run minimal distribution tests
cd tests/integration
mvn test -Dtest=MinimalDistributionServiceTest -Ddistribution.mode=minimal

# Expected: 2/5 passing (known limitation with remaining 3)
```

### Docker Infrastructure

```bash
# Start integration infrastructure
docker-compose -f docker/docker-compose.yml up -d

# Services:
# - MongoDB: localhost:27019
# - Kafka: localhost:19093
# - OpenSearch: localhost:9202
# - MinIO: localhost:9001
# - Redis: localhost:6380
```

### Test Services

When tests run, these services start:
- core-api (8080)
- blob-storage (8084)
- imaging (8090)
- office-processor (8091)
- indexing (8099)

## Known Limitations

1. **Jandex REST Client Issue**: Services using `BlobStorageApi` from `shared-models.jar` fail in local JAR mode
   - Affects: imaging, office-processor, indexing
   - Workaround: Deploy services to Docker (full functionality)
   - Details: See [JANDEX_REST_CLIENT_LIMITATION.md](./JANDEX_REST_CLIENT_LIMITATION.md)

2. **Local JVM Limitations**: Running services as `java -jar` has constraints
   - REST clients from external JARs not supported
   - Use Docker or `./mvnw quarkus:dev` instead

## Production Deployment

✅ **Services work correctly in production deployment modes:**
- Docker Compose
- Kubernetes
- Native image (GraalVM)

The Jandex limitation **only affects local JAR testing**, not production.

## Contributing

When adding new tests:
1. Document any external dependencies
2. Update test status documents
3. Note any known limitations
4. Verify tests pass in Docker mode

---

**Last Updated**: 2026-01-18
