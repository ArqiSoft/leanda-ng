# Running Tests in Docker

**Last Updated**: 2025-12-27  
**Agent**: QA-Cloud

## Overview

This guide explains how to run all tests locally using Docker. This ensures consistent test environments and eliminates the need to install dependencies locally.

## Prerequisites

- Docker Desktop (or Docker Engine) installed and running
- Docker Compose v2.0+
- At least 4GB of available RAM
- At least 10GB of available disk space

## Quick Start

### Run All Tests

```bash
cd docker
./run-tests.sh all
```

### Run Specific Test Types

```bash
# Unit tests only
./run-tests.sh unit

# Integration tests only
./run-tests.sh integration

# E2E tests only
./run-tests.sh e2e
```

## Test Types

### Unit Tests

Runs unit tests for all Java services:
- core-api
- blob-storage
- chemical-parser
- chemical-properties
- reaction-parser
- crystal-parser
- spectra-parser
- imaging
- office-processor
- metadata-processing
- indexing

**Command**:
```bash
./run-tests.sh unit
```

**What it does**:
1. Starts MongoDB and Kafka test containers
2. Runs `mvn test` for each service
3. Collects test results
4. Outputs results to `test-results/` directory

### Integration Tests

Runs integration tests with real service containers:
- Starts infrastructure (MongoDB, Kafka, OpenSearch)
- Starts service containers (core-api, blob-storage)
- Runs integration test suite
- Verifies service-to-service communication

**Command**:
```bash
./run-tests.sh integration
```

**What it does**:
1. Starts infrastructure services
2. Starts service containers
3. Waits for services to be healthy
4. Runs integration tests from `tests/integration/`
5. Collects test results

### E2E Tests

Runs Playwright E2E tests against running services:
- Starts infrastructure and service containers
- Installs Playwright and dependencies
- Runs E2E test suite
- Generates HTML reports

**Command**:
```bash
./run-tests.sh e2e
```

**What it does**:
1. Starts infrastructure and service containers
2. Installs Playwright browsers
3. Runs E2E tests from `frontend/e2e/`
4. Generates test reports

### All Tests

Runs all test types sequentially:
1. Unit tests
2. Integration tests
3. E2E tests (if services are available)

**Command**:
```bash
./run-tests.sh all
```

## Manual Docker Compose Usage

You can also use Docker Compose directly:

### Start Infrastructure Only

```bash
cd docker
docker-compose -f docker-compose.test.yml up -d mongodb-test kafka-test zookeeper-test opensearch-test
```

### Run Unit Tests

```bash
docker-compose -f docker-compose.test.yml --profile unit-tests up --build unit-tests-runner
```

### Run Integration Tests

```bash
docker-compose -f docker-compose.test.yml --profile integration-tests up --build integration-tests-runner
```

### Run E2E Tests

```bash
docker-compose -f docker-compose.test.yml --profile e2e-tests up --build e2e-tests-runner
```

### View Test Results

Test results are stored in a Docker volume. To extract them:

```bash
# Create local directory
mkdir -p test-results

# Copy from volume
docker run --rm -v leanda-ng-test-results:/source -v $(pwd)/test-results:/dest alpine sh -c "cp -r /source/* /dest/"
```

Or use the script which does this automatically.

## Test Results

Test results are available in:
- **Local directory**: `docker/test-results/`
- **Docker volume**: `leanda-ng-test-results`

### Result Structure

```
test-results/
├── core-api-unit-tests/
│   └── surefire-reports/
├── blob-storage-unit-tests/
│   └── surefire-reports/
├── integration-tests/
│   └── surefire-reports/
├── e2e-tests/
│   └── playwright-report/
└── summary/
    └── (aggregated results)
```

### Viewing Results

**JUnit XML Reports**: Open `surefire-reports/TEST-*.xml` in your IDE or CI/CD system

**Playwright HTML Report**: 
```bash
cd docker/test-results/e2e-tests/playwright-report
python3 -m http.server 8000
# Open http://localhost:8000 in browser
```

## Troubleshooting

### Tests Fail to Start

**Issue**: Docker containers fail to start  
**Solution**: 
```bash
# Check Docker is running
docker info

# Check available resources
docker system df

# Clean up old containers
docker-compose -f docker-compose.test.yml down -v
```

### Out of Memory

**Issue**: Tests fail with out of memory errors  
**Solution**:
- Increase Docker memory limit (Docker Desktop → Settings → Resources)
- Reduce concurrent test execution
- Run tests one service at a time

### Port Conflicts

**Issue**: Port already in use  
**Solution**: The test compose file uses different ports:
- MongoDB: 27018 (instead of 27017)
- Kafka: 9093 (instead of 9092)
- Services: 8081, 8085 (instead of 8080, 8084)

If conflicts persist, modify ports in `docker-compose.test.yml`.

### Services Not Healthy

**Issue**: Health checks fail  
**Solution**:
```bash
# Check service logs
docker-compose -f docker-compose.test.yml logs mongodb-test
docker-compose -f docker-compose.test.yml logs kafka-test

# Restart services
docker-compose -f docker-compose.test.yml restart
```

### Test Timeouts

**Issue**: Tests timeout waiting for services  
**Solution**: Increase timeout in test configuration or wait longer:
```bash
# Wait manually
docker-compose -f docker-compose.test.yml up -d
sleep 30  # Wait for services
./run-tests.sh integration
```

## Environment Variables

You can customize test execution with environment variables:

```bash
# Java version
export JAVA_VERSION=21

# Maven options
export MAVEN_OPTS="-Xmx2048m"

# Test-specific
export MONGODB_CONNECTION_STRING="mongodb://admin:admin123@mongodb-test:27017/leanda-ng-test?authSource=admin"
export KAFKA_BOOTSTRAP_SERVERS="kafka-test:9092"
```

## CI/CD Integration

The Docker test setup can be used in CI/CD:

```yaml
# Example GitHub Actions
- name: Run tests in Docker
  run: |
    cd docker
    ./run-tests.sh all
```

## Best Practices

1. **Clean Up**: Always clean up test containers after running tests
   ```bash
   docker-compose -f docker-compose.test.yml down -v
   ```

2. **Resource Management**: Don't run all tests simultaneously if resources are limited

3. **Cache Management**: Maven and npm caches are persisted in volumes for faster subsequent runs

4. **Parallel Execution**: Unit tests run in parallel by default. Integration tests run sequentially.

5. **Test Isolation**: Each test run uses fresh containers to ensure isolation

## Comparison: Docker vs Local

| Aspect | Docker | Local |
|--------|--------|-------|
| **Setup** | ✅ No local dependencies | ❌ Requires Java, Maven, Node.js |
| **Consistency** | ✅ Same environment every time | ❌ Environment differences |
| **Isolation** | ✅ Complete isolation | ⚠️ May affect local services |
| **Speed** | ⚠️ Slightly slower (container overhead) | ✅ Faster (no container overhead) |
| **Resource Usage** | ⚠️ Higher (containers) | ✅ Lower (direct execution) |
| **CI/CD Ready** | ✅ Works in CI/CD | ⚠️ Requires setup |

## Next Steps

- ✅ Run tests in Docker: `./run-tests.sh all`
- ⏳ Review test results in `test-results/` directory
- ⏳ Integrate into CI/CD pipeline
- ⏳ Add performance tests
- ⏳ Add security tests

---

**See Also**:
- [Testing Strategy](../../docs/testing/testing-strategy.md)
- [Integration Test Framework](../../tests/integration/README.md)
- [Quick Reference](../../docs/testing/quick-reference.md)

