# QA Service Test Coverage and Mocking Plan

## Overview

As QA Tech Lead, this plan addresses two critical testing gaps:

1. **Service-level integration tests currently use real Docker infrastructure** (MongoDB, Kafka via Docker Compose) - need to convert to mocked infrastructure
2. **Missing unit tests** for application services and domain logic across all services

## Current State Analysis

### Integration Test Infrastructure Issues

**Current Pattern (Needs Fixing):**

- `IsolatedIntegrationTestBase` uses `DockerComposeManager` to start real MongoDB/Kafka containers
- Tests like `BlobStorageIntegrationTest`, `CoreApiIntegrationTest` use real infrastructure
- `QuarkusRestClientTestBase` uses WireMock for REST clients but still uses real infrastructure

**Services with Integration Tests Using Real Infrastructure:**

- `blob-storage`: `BlobStorageIntegrationTest`, `KafkaEventIntegrationTest`
- `core-api`: `CoreApiIntegrationTest`, `CoreApiRestApiIntegrationTest`
- `chemical-parser`: `BlobStorageClientIntegrationTest` (uses WireMock but real Kafka/MongoDB)
- All parser services: Similar pattern
- All processing services: Similar pattern

### Unit Test Coverage Gaps

**Services Missing Unit Tests:**

1. **chemical-parser**: `ChemicalParserService` - no unit tests
2. **crystal-parser**: `CrystalParserService` - no unit tests
3. **reaction-parser**: `ReactionParserService` - no unit tests
4. **spectra-parser**: `SpectraParserService` - no unit tests
5. **chemical-properties**: `ChemicalPropertiesService` - no unit tests
6. **imaging**: `ImagingService` - no unit tests
7. **metadata-processing**: `MetadataGenerationService` - no unit tests
8. **indexing**: `IndexingService` - no unit tests (has `TextExtractionServiceTest` but missing `IndexingService` tests)
9. **core-api**: Missing unit tests for `EventPublisher`, handlers
10. **blob-storage**: Has `BlobServiceTest` ✅, but missing tests for `BlobEventPublisher`

**Services with Good Unit Test Coverage:**

- `office-processor`: Has `OfficeConversionServiceTest`, `MetadataExtractionServiceTest` ✅
- `indexing`: Has `TextExtractionServiceTest` ✅
- `blob-storage`: Has `BlobServiceTest` ✅

## Implementation Plan

### Phase 1: Create Mocked Infrastructure Test Base

**Goal**: Replace Docker Compose with in-memory/mocked infrastructure for service-level integration tests

**Tasks:**

1. **Create `MockedIntegrationTestBase`** in `tests/utils/src/main/java/io/leanda/tests/utils/`

      - Use MongoDB Embedded Server or Fongo (in-memory MongoDB)
      - Use embedded Kafka (kafka-embedded) or MockKafka
      - Extend `QuarkusRestClientTestBase` for WireMock REST client mocking
      - Provide helper methods for test data setup

2. **Update `IsolatedIntegrationTestBase`** to support both modes:

      - Add flag to choose between mocked vs real infrastructure
      - Keep real infrastructure option for full integration tests in `tests/integration/`
      - Default to mocked for service-level tests

3. **Create MongoDB Mock Utilities**:

      - `MongoMockHelper` - setup/teardown, test data insertion
      - Use embedded MongoDB or Fongo for in-memory testing

4. **Create Kafka Mock Utilities**:

      - `KafkaMockHelper` - embedded Kafka or MockKafka
      - Message verification utilities

### Phase 2: Convert Service-Level Integration Tests to Mocked Infrastructure

**Goal**: Update all service-level integration tests to use mocked infrastructure

**Services to Update:**

1. **blob-storage** (`services/blob-storage/src/test/`):

      - `BlobStorageIntegrationTest` - use mocked MongoDB
      - `KafkaEventIntegrationTest` - use mocked Kafka
      - `GridFsBlobStorageTest` - use mocked MongoDB

2. **core-api** (`services/core-api/src/test/`):

      - `CoreApiIntegrationTest` - use mocked MongoDB and Kafka
      - `CoreApiRestApiIntegrationTest` - use mocked MongoDB

3. **chemical-parser** (`services/chemical-parser/src/test/`):

      - `BlobStorageClientIntegrationTest` - already uses WireMock ✅, but add mocked Kafka
      - `ChemicalParserCommandIntegrationTest` - use mocked infrastructure
      - `ChemicalParserEventIntegrationTest` - use mocked Kafka

4. **All other parser services** (crystal-parser, reaction-parser, spectra-parser):

      - Similar pattern to chemical-parser

5. **All processing services** (chemical-properties, imaging, metadata-processing, indexing, office-processor):

      - Convert integration tests to use mocked infrastructure

### Phase 3: Implement Missing Unit Tests

**Goal**: Add comprehensive unit tests for all application services and domain logic

**Unit Test Implementation Plan:**

#### 3.1 Parser Services Unit Tests

**chemical-parser**:

- `ChemicalParserServiceTest` - test parsing logic with mocked `BlobStorageClient` and `IndigoAdapter`
- Test cases: successful parsing, unsupported format, blob download failure, record processing errors

**crystal-parser**:

- `CrystalParserServiceTest` - similar pattern

**reaction-parser**:

- `ReactionParserServiceTest` - similar pattern

**spectra-parser**:

- `SpectraParserServiceTest` - similar pattern

#### 3.2 Processing Services Unit Tests

**chemical-properties**:

- `ChemicalPropertiesServiceTest` - test property calculation with mocked dependencies

**imaging**:

- `ImagingServiceTest` - test image generation/rasterization

**metadata-processing**:

- `MetadataGenerationServiceTest` - test metadata extraction and generation

**indexing**:

- `IndexingServiceTest` - test indexing operations (has `TextExtractionServiceTest` ✅)

#### 3.3 Core API Unit Tests

**core-api**:

- `EventPublisherTest` - test Kafka event publishing with mocked producer
- `UserCreatedHandlerTest` - test event handler logic
- `UserUpdatedHandlerTest` - test event handler logic
- `FileCreatedHandlerTest` - test event handler logic

#### 3.4 Blob Storage Unit Tests

**blob-storage**:

- `BlobEventPublisherTest` - test event publishing (has `BlobServiceTest` ✅)

### Phase 4: Test Infrastructure and Utilities

**Goal**: Create reusable test utilities and ensure consistent patterns

**Tasks:**

1. **Create Test Data Builders**:

      - `BlobInfoTestBuilder` - for creating test blob info objects
      - `UserTestBuilder` - for creating test user objects
      - `EventTestBuilder` - for creating test event objects

2. **Create Mock Factories**:

      - `BlobStorageClientMockFactory` - consistent mocking of blob storage client
      - `KafkaProducerMockFactory` - consistent mocking of Kafka producers
      - `MongoClientMockFactory` - consistent mocking of MongoDB clients

3. **Update Test Documentation**:

      - Document mocked vs real infrastructure usage
      - Update `docs/testing/` with new patterns
      - Create guide for writing service-level tests

## File Structure

### New Files to Create

```
tests/utils/src/main/java/io/leanda/tests/utils/
 - MockedIntegrationTestBase.java          # Base class for mocked infrastructure tests
 - MongoMockHelper.java                    # MongoDB mocking utilities
 - KafkaMockHelper.java                    # Kafka mocking utilities
 - TestDataBuilders.java                   # Test data builder classes
 - MockFactories.java                      # Mock factory classes

services/[service-name]/src/test/java/io/leanda/[service]/application/
 - [Service]ServiceTest.java               # Unit tests for application services

services/[service-name]/src/test/java/io/leanda/[service]/infrastructure/
 - [Updated]IntegrationTest.java           # Updated to use mocked infrastructure
```

### Files to Update

```
tests/utils/src/main/java/io/leanda/tests/utils/
 - IsolatedIntegrationTestBase.java       # Add mocked infrastructure option

services/*/src/test/java/.../
 - All *IntegrationTest.java files        # Convert to use mocked infrastructure
```

## Testing Standards

### Unit Test Requirements

- Use `@ExtendWith(MockitoExtension.class)`
- Mock all external dependencies (databases, HTTP clients, Kafka producers/consumers)
- Test both happy paths and error scenarios
- Aim for >80% code coverage
- Use descriptive test names: `test_should_[action]*given*[condition]`

### Integration Test Requirements (Service-Level)

- Use mocked infrastructure (MongoDB, Kafka) - NOT Docker Compose
- Use WireMock for REST client mocking
- Test service boundaries and interactions
- Keep tests fast (< 5 seconds per test)

### Full Integration Tests (tests/integration/)

- Keep using real infrastructure via Docker Compose
- These test end-to-end workflows across services
- Located in `tests/integration/` directory

## Success Criteria

1. ✅ All service-level integration tests use mocked infrastructure (no Docker Compose)
2. ✅ All application services have unit tests with >80% coverage
3. ✅ All domain logic has unit tests
4. ✅ Test execution time reduced (mocked tests run faster)
5. ✅ Tests can run without Docker (except full integration tests)
6. ✅ Consistent test patterns across all services

## Dependencies

- **Mockito** - Already in use ✅
- **WireMock** - Already in use ✅
- **Embedded MongoDB** or **Fongo** - Need to add
- **Embedded Kafka** or **MockKafka** - Need to add

## Estimated Effort

- **Phase 1**: 2-3 hours (mock infrastructure base classes)
- **Phase 2**: 4-6 hours (convert ~20 integration tests)
- **Phase 3**: 8-12 hours (implement ~15 unit test classes)
- **Phase 4**: 2-3 hours (utilities and documentation)

**Total**: ~16-24 hours