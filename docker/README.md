# Docker Test Environment

**Last Updated**: 2025-12-27  
**Agent**: QA-Cloud

## Quick Start

Run all tests in Docker:

```bash
cd docker
./run-tests.sh all
```

## What's Included

- ✅ **Unit Tests**: All Java service unit tests
- ✅ **Integration Tests**: Full integration test suite
- ✅ **E2E Tests**: Playwright browser tests
- ✅ **Infrastructure**: MongoDB, Kafka, OpenSearch test containers
- ✅ **Service Containers**: Core services for integration/E2E tests

## Files

- `docker-compose.test.yml` - Test environment compose file
- `Dockerfile.test-runner` - Java/Maven test runner
- `Dockerfile.e2e-runner` - Playwright E2E test runner
- `run-tests.sh` - Convenience script to run tests
- `TESTING.md` - Detailed testing documentation

## Usage

See [TESTING.md](./TESTING.md) for complete documentation.

---

**See Also**:
- [Testing Strategy](../../docs/testing/testing-strategy.md)
- [Integration Tests](../../tests/integration/README.md)

