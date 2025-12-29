# Integration Test Specifications

## Overview

This document defines integration test scenarios for Leanda NG services, focusing on end-to-end workflows and inter-service communication.

## Infrastructure Requirements

### Testcontainers Configuration

```java
@QuarkusTestResource(MongoDBTestResource.class)
@QuarkusTestResource(KafkaTestResource.class)
@QuarkusTestResource(RedisTestResource.class)
public class IntegrationTestBase {
    
    @Container
    static MongoDBContainer mongodb = new MongoDBContainer("mongo:7.0");
    
    @Container
    static RedpandaContainer kafka = new RedpandaContainer("redpandadata/redpanda:v23.3.0");
    
    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7.2-alpine")
        .withExposedPorts(6379);
}
```

## Event Handler Integration Tests

### User Events

| Test Case | Description | Steps | Expected Result |
|-----------|-------------|-------|-----------------|
| `test_userCreated_persistsUser` | User creation flow | 1. Publish CreateUser command<br>2. Wait for UserCreated event<br>3. Query database | User persisted in MongoDB |
| `test_userUpdated_updatesUser` | User update flow | 1. Create user<br>2. Publish UpdateUser<br>3. Query database | User updated with new values |
| `test_userCreated_sendsUserPersisted` | Event chain | 1. Publish CreateUser<br>2. Listen for UserPersisted | UserPersisted event received |

### Folder Events

| Test Case | Description | Steps | Expected Result |
|-----------|-------------|-------|-----------------|
| `test_folderCreated_persistsFolder` | Folder creation | 1. Publish CreateFolder<br>2. Query database | Folder in MongoDB |
| `test_folderMoved_updatesParent` | Folder move | 1. Create folder<br>2. Publish MoveFolder<br>3. Verify parentId | ParentId updated |
| `test_folderDeleted_softDeletes` | Folder deletion | 1. Create folder<br>2. Publish DeleteFolder | isDeleted = true |
| `test_folderRenamed_updatesName` | Folder rename | 1. Create folder<br>2. Publish RenameFolder | Name updated |

### File Events

| Test Case | Description | Steps | Expected Result |
|-----------|-------------|-------|-----------------|
| `test_fileCreated_persistsFile` | File creation | 1. Publish FileCreated event<br>2. Query database | File in MongoDB |
| `test_fileStatusChanged_updates` | Status change | 1. Create file<br>2. Publish StatusChanged | Status updated |
| `test_fileImageAdded_addsImage` | Image addition | 1. Create file<br>2. Publish ImageAdded | Image in images array |
| `test_fileMetadataUpdated_updatesMetadata` | Metadata update | 1. Create file<br>2. Publish MetadataUpdated | Metadata updated |
| `test_fileDeleted_softDeletes` | File deletion | 1. Create file<br>2. Publish FileDeleted | isDeleted = true |

### Record Events

| Test Case | Description | Steps | Expected Result |
|-----------|-------------|-------|-----------------|
| `test_recordCreated_persistsRecord` | Record creation | 1. Publish RecordCreated<br>2. Query database | Record in MongoDB |
| `test_recordFieldsUpdated_updatesFields` | Fields update | 1. Create record<br>2. Publish FieldsUpdated | Fields array updated |

## Saga Integration Tests

### File Processing Saga

```gherkin
Scenario: Complete file processing workflow
  Given a user uploads a chemical file
  When the file is uploaded to blob storage
  Then a FileCreated event is published
  And the file status changes to "Parsing"
  And the parser service processes the file
  And RecordCreated events are published for each record
  And the file status changes to "Processed"
  And a FileProcessed event is published
  And the file totalRecords is updated
```

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_fileProcessingSaga_success` | Complete flow | File status = Processed |
| `test_fileProcessingSaga_parserFails` | Parser failure | File status = Failed, error logged |
| `test_fileProcessingSaga_partialSuccess` | Some records fail | File status = ProcessedPartially |
| `test_fileProcessingSaga_compensation` | Rollback on failure | Previous state restored |

### ML Training Saga

```gherkin
Scenario: Complete ML training workflow
  Given a user starts model training
  When the training command is published
  Then a folder is created for the model
  And the training service processes the dataset
  And a Model entity is created
  And the model status changes to "Trained"
  And a ModelTrained event is published
```

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_trainingStarted_createsModel` | Start training | Model in database |
| `test_trainingCompleted_updatesModel` | Complete training | Model status = Trained |
| `test_trainingFailed_marksAsFailed` | Training failure | Model status = Failed |

## Database Integration Tests

### MongoDB Operations

| Test Case | Description | Query Type |
|-----------|-------------|------------|
| `test_findNodesByParent_returnsChildren` | Find children | Simple query |
| `test_findNodesWithFilter_appliesFilter` | OData filter | Dynamic filter |
| `test_aggregateWithBreadcrumbs_returnPath` | Breadcrumbs | GraphLookup aggregation |
| `test_findPublicNodes_joinsAccessPermissions` | Public nodes | Lookup + Match |
| `test_paginatedQuery_returnsCorrectPage` | Pagination | Skip + Limit |
| `test_indexUsage_queriesUseIndex` | Index verification | Explain plan |

### MongoDB Aggregation Tests

```java
@Test
public void test_getNodesAggregation_returnsCorrectData() {
    // Given
    UUID userId = createTestUser();
    UUID folderId = createTestFolder(userId, null);
    createTestFile(userId, folderId);
    createTestFile(userId, folderId);
    
    // When
    List<Node> nodes = nodeRepository.getNodesWithAccessPermissions(folderId, userId);
    
    // Then
    assertThat(nodes).hasSize(2);
    assertThat(nodes).allMatch(n -> n.getOwnedBy().equals(userId));
}
```

## Kafka Integration Tests

### Event Publishing

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_publishEvent_eventReceived` | Basic publish | Event in topic |
| `test_publishEvent_headersSet` | Message headers | correlationId, timestamp present |
| `test_publishEvent_keySet` | Partition key | Event ID as key |

### Event Consumption

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_consumeEvent_handlerCalled` | Basic consume | Handler invoked |
| `test_consumeEvent_idempotent` | Duplicate event | Processed once |
| `test_consumeEvent_errorRetry` | Transient error | Retry with backoff |
| `test_consumeEvent_dlq` | Permanent error | Sent to DLQ |

### Consumer Group Tests

```java
@Test
public void test_consumerGroup_balancesPartitions() {
    // Given - multiple consumer instances
    
    // When - publish 100 events
    
    // Then - events distributed across consumers
}
```

## Redis Integration Tests

### Caching

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_cacheResult_stored` | Cache hit | Value from cache |
| `test_cacheExpiry_expires` | TTL expiry | Value refetched |
| `test_cacheInvalidation_clears` | Manual invalidation | Cache cleared |

### Session Storage

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_currentNode_stored` | Store current node | Value in Redis |
| `test_currentNode_retrieved` | Retrieve node | Correct node ID |
| `test_currentNode_expired` | Session expiry | Null after expiry |

## Cross-Service Integration Tests

### Core API → Parser Service

```java
@Test
public void test_fileUpload_triggersParser() {
    // Given - file uploaded via REST API
    Response response = given()
        .multiPart("file", testFile)
        .when()
        .post("/api/files");
    
    // When - wait for processing
    await().atMost(30, SECONDS).until(() -> {
        return getFileStatus(response.getHeader("Location")) == "Processed";
    });
    
    // Then - records created
    List<Record> records = getRecords(fileId);
    assertThat(records).isNotEmpty();
}
```

### Core API → ML Service

```java
@Test
public void test_modelTraining_completesSuccessfully() {
    // Given - training dataset
    UUID datasetId = uploadTrainingDataset();
    
    // When - start training
    Response response = given()
        .body(trainingRequest)
        .when()
        .post("/api/machinelearning/models");
    
    // Then - model trained
    await().atMost(5, MINUTES).until(() -> {
        return getModelStatus(modelId) == "Trained";
    });
}
```

## Performance Integration Tests

### Load Testing Scenarios

| Test Case | Load | Duration | Expected |
|-----------|------|----------|----------|
| `test_getNodes_100rps` | 100 req/s | 60s | p99 < 200ms |
| `test_fileUpload_10concurrent` | 10 concurrent | 5 min | All complete |
| `test_eventProcessing_1000events` | 1000 events | - | All processed < 30s |

### Stress Testing

```java
@Test
public void test_highLoad_handlesGracefully() {
    // Simulate 500 concurrent users
    // Verify no errors, acceptable latency
}
```

## Data Consistency Tests

### Eventual Consistency

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_nodeCreated_eventuallyInNodes` | New file | In Nodes collection |
| `test_fileUpdated_eventuallyConsistent` | File update | All collections updated |
| `test_fileDeleted_cascadeDeletes` | Delete file | Related records deleted |

### Concurrency

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_concurrentUpdates_noDataLoss` | Parallel updates | All updates applied |
| `test_optimisticLocking_conflictHandled` | Version conflict | 409 Conflict response |

## Error Handling Tests

### Transient Errors

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_dbTimeout_retries` | DB timeout | Retry with backoff |
| `test_kafkaUnavailable_buffers` | Kafka down | Events buffered |
| `test_redisDown_fallback` | Redis down | DB fallback |

### Permanent Errors

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_invalidEvent_sentToDlq` | Malformed event | Sent to DLQ |
| `test_persistentDbError_alertsMonitoring` | DB error | Alert triggered |

## Test Environment Setup

```yaml
# test-resources/application-test.yaml
quarkus:
  mongodb:
    connection-string: ${MONGODB_URI}
    database: leanda_test
  kafka:
    bootstrap-servers: ${KAFKA_BROKER}
  redis:
    hosts: ${REDIS_HOST}
    
mp:
  messaging:
    incoming:
      test-events:
        topic: leanda.test.events
        auto.offset.reset: earliest
```

## CI/CD Integration

```yaml
# .github/workflows/integration-tests.yml
jobs:
  integration-tests:
    runs-on: ubuntu-latest
    services:
      mongodb:
        image: mongo:7.0
      redis:
        image: redis:7.2-alpine
      kafka:
        image: redpandadata/redpanda:v23.3.0
    steps:
      - uses: actions/checkout@v4
      - name: Run integration tests
        run: ./mvnw verify -Pintegration-tests
```

