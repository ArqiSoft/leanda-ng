# Core Services Implementation Plan

## Overview

This document maps legacy .NET services to their Quarkus equivalents, defining technology choices, patterns, and implementation strategies for the Leanda NG migration.

**Status**: Phase 2 services complete ✅ | Phase 1 services pending ⏳

**Last Updated**: 2025-12-27

This plan documents:
- **Phase 2 (Complete)**: Parsers, blob storage, metadata, indexing, frontend - all implemented and tested
- **Phase 1 (Pending)**: Core API, persistence service, domain event handlers - planned but not yet started
- **Future**: ML services orchestration

## Technology Mapping

### Framework & Runtime

| Legacy (.NET Core 3.1) | Target (Java 21 + Quarkus 3.x) |
|------------------------|--------------------------------|
| ASP.NET Core MVC | Quarkus REST (RESTEasy Reactive) |
| Entity Framework Core | Quarkus Panache MongoDB |
| MassTransit | SmallRye Reactive Messaging (Kafka) |
| SignalR | Quarkus WebSockets |
| CQRSlite (CQRS) | Custom CQRS with CDI |
| EventStore | DynamoDB Streams / Kafka |
| MongoDB.Driver | Quarkus MongoDB with Panache |
| Redis | Quarkus Redis |
| Serilog | Quarkus Logging (JBoss Logging + Slf4j) |
| Swagger/OpenAPI | Quarkus OpenAPI (SmallRye) |

### Messaging Patterns

| MassTransit Pattern | SmallRye Reactive Messaging |
|---------------------|----------------------------|
| `IBusControl.Publish<T>()` | `@Channel @Outgoing` with Emitter |
| `IConsumer<T>` | `@Incoming` annotated method |
| `ISaga` / `IStateMachine` | Saga pattern with Kafka Streams or custom |
| Request/Response | Kafka with reply topics or REST |
| Correlation | Message headers with `correlationId` |

### Data Access

| .NET Pattern | Quarkus Pattern |
|--------------|-----------------|
| `IMongoCollection<T>` | `PanacheMongoRepository<T>` or `PanacheMongoEntity` |
| MongoDB Aggregations | Quarkus MongoDB with Panache + raw MongoDB |
| Redis IDistributedCache | Quarkus Redis with `@CacheResult` |
| GridFS | Quarkus GridFS client or S3 |

### Phase 2 Patterns (Actually Implemented)

| Pattern | Implementation | Location |
|---------|----------------|----------|
| **REST Client** | Quarkus REST Client for blob-storage integration | `services/*/infrastructure/BlobStorageClient.java` |
| **Event-Driven** | SmallRye Reactive Messaging with Kafka | All parser services use `@Incoming` / `@Outgoing` |
| **Shared Models** | Domain models in `shared/models/` directory | `shared/models/BlobInfo.java`, `Property.java`, etc. |
| **Test Utilities** | Reusable test base classes and mocks | `tests/` directory with `QuarkusIntegrationTestBase` |
| **Docker Compose** | Local development with hot-reload | `docker-compose.yml` with all Phase 2 services |
| **Integration Tests** | Testcontainers with workflow tests | `tests/integration/workflows/` |

## Service Mapping

### Completed Services (Phase 2) ✅

| Legacy Project | Quarkus Service | Port | Status | Agent |
|----------------|-----------------|------|--------|-------|
| Sds.Osdr.Chemicals (Parser) | chemical-parser | 8083 | ✅ Complete | Agent 1 |
| Sds.Osdr.Chemicals (Properties) | chemical-properties | 8086 | ✅ Complete | Agent 1 |
| Sds.Osdr.Reactions (Parser) | reaction-parser | 8087 | ✅ Complete | Agent 1 |
| Sds.Osdr.Crystals (Parser) | crystal-parser | 8089 | ✅ Complete | Agent 2 |
| Sds.Osdr.Spectra (Parser) | spectra-parser | 8090 | ✅ Complete | Agent 2 |
| Sds.Osdr.Image (Rasterizer) | imaging | 8091 | ✅ Complete | Agent 2 |
| Sds.Storage.Blob.Core | blob-storage | 8084 | ✅ Complete | Agent 3 |
| Sds.Osdr.Office (Processor) | office-processor | 8088 | ✅ Complete | Agent 3 |
| Sds.Osdr.Generic (Metadata) | metadata-processing | 8098 | ✅ Complete | Agent 4 |
| Sds.Indexing | indexing | 8099 | ✅ Complete | Agent 4 |
| leanda-ui (Angular 9) | frontend (Angular 21) | - | ✅ Complete | Agent 6 |

### Remaining Services (Phase 1 & Future)

| Legacy Project | Quarkus Service | Port | Status | Phase |
|----------------|-----------------|------|--------|-------|
| Sds.Osdr.WebApi | core-api | 8080 | ⏳ Pending | Phase 1 |
| Sds.Osdr.Domain.BackEnd | core-api (handlers) | 8080 | ⏳ Pending | Phase 1 |
| Sds.Osdr.Domain.FrontEnd | core-api (handlers) | 8080 | ⏳ Pending | Phase 1 |
| Sds.Osdr.Persistence | persistence-service | 8081 | ⏳ Pending | Phase 1 |
| Sds.Osdr.Generic | shared/models + core-api | - | ✅ Partial | Phase 2 |
| Sds.Osdr.MachineLearning | ml-orchestrator | TBD | ⏳ Pending | Agent 5 |

## Core API Implementation

### REST Resources (replacing Controllers)

```java
// Legacy: NodesController.cs
// Target: io.leanda.core.api.NodesResource.java

@Path("/api/nodes")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
@Authenticated
public class NodesResource {
    
    @Inject
    NodeService nodeService;
    
    @GET
    @Path("/{id}")
    public Uni<Response> getNode(@PathParam("id") UUID id, 
                                  @QueryParam("$projection") String projection) {
        return nodeService.findById(id, projection)
            .onItem().ifNotNull().transform(node -> Response.ok(node).build())
            .onItem().ifNull().continueWith(Response.status(404).build());
    }
    
    @GET
    public Uni<PagedList<Node>> getNodeList(
            @QueryParam("$filter") String filter,
            @QueryParam("pageNumber") @DefaultValue("1") int pageNumber,
            @QueryParam("pageSize") @DefaultValue("20") int pageSize) {
        return nodeService.findAll(filter, pageNumber, pageSize);
    }
}
```

### Event Handlers (replacing MassTransit Consumers)

```java
// Legacy: UserCreatedConsumer.cs
// Target: io.leanda.core.handlers.UserEventHandler.java

@ApplicationScoped
public class UserEventHandler {
    
    @Inject
    UserRepository userRepository;
    
    @Inject
    @Channel("user-events-out")
    Emitter<UserPersisted> userPersistedEmitter;
    
    @Incoming("user-created")
    @Transactional
    public Uni<Void> onUserCreated(UserCreated event) {
        return userRepository.persist(User.fromEvent(event))
            .onItem().invoke(user -> {
                userPersistedEmitter.send(new UserPersisted(user.id));
            })
            .replaceWithVoid();
    }
}
```

### CQRS Implementation

```java
// Command Handler
@ApplicationScoped
public class CreateFolderCommandHandler implements CommandHandler<CreateFolder> {
    
    @Inject
    FolderRepository folderRepository;
    
    @Inject
    EventPublisher eventPublisher;
    
    @Override
    public Uni<Void> handle(CreateFolder command) {
        Folder folder = new Folder(command);
        return folderRepository.persist(folder)
            .onItem().invoke(() -> {
                eventPublisher.publish(new FolderCreated(folder));
            })
            .replaceWithVoid();
    }
}

// Query Handler
@ApplicationScoped
public class GetFolderByIdQueryHandler implements QueryHandler<GetFolderById, Folder> {
    
    @Inject
    FolderRepository folderRepository;
    
    @Override
    public Uni<Folder> handle(GetFolderById query) {
        return folderRepository.findById(query.getId());
    }
}
```

## Data Layer Implementation

### Entity Classes (Panache MongoDB)

```java
// Legacy: BaseNode.cs → Nodes collection
// Target: io.leanda.core.domain.Node.java

@MongoEntity(collection = "Nodes")
public class Node extends PanacheMongoEntity {
    
    @BsonId
    public UUID id;
    
    public String type;
    public String subType;
    public String name;
    public UUID ownedBy;
    public UUID createdBy;
    public Instant createdDateTime;
    public UUID updatedBy;
    public Instant updatedDateTime;
    public UUID parentId;
    public String status;
    public boolean isDeleted;
    public Blob blob;
    public List<Image> images;
    public Integer totalRecords;
    public AccessPermissions accessPermissions;
    public Integer version;
    
    // Finder methods
    public static Uni<Node> findByIdForUser(UUID id, UUID userId) {
        return find("_id = ?1 and ownedBy = ?2 and isDeleted != true", id, userId)
            .firstResult();
    }
    
    public static Uni<List<Node>> findChildren(UUID parentId, UUID userId) {
        return find("parentId = ?1 and ownedBy = ?2 and isDeleted != true", parentId, userId)
            .list();
    }
}
```

### Repository Pattern

```java
@ApplicationScoped
public class NodeRepository implements PanacheMongoRepository<Node> {
    
    public Uni<PagedList<Node>> findWithFilter(BsonDocument filter, int page, int size) {
        return mongoClient().getDatabase("leanda")
            .getCollection("Nodes", Node.class)
            .find(filter)
            .skip((page - 1) * size)
            .limit(size)
            .collect().asList()
            .onItem().transform(nodes -> new PagedList<>(nodes, page, size));
    }
    
    public Uni<List<Node>> aggregateWithBreadcrumbs(UUID nodeId, UUID userId) {
        // MongoDB aggregation pipeline for breadcrumbs
        List<Bson> pipeline = List.of(
            Aggregates.match(Filters.eq("_id", nodeId)),
            Aggregates.graphLookup("Nodes", "$parentId", "_id", "parentId", "parents")
        );
        return mongoClient().getDatabase("leanda")
            .getCollection("Nodes", Node.class)
            .aggregate(pipeline)
            .collect().asList();
    }
}
```

## Messaging Implementation

### Kafka Configuration

```yaml
# application.yaml
mp:
  messaging:
    incoming:
      user-commands:
        connector: smallrye-kafka
        topic: leanda.users.commands
        value.deserializer: io.quarkus.kafka.client.serialization.JsonbDeserializer
        group.id: core-api-users
        
      folder-commands:
        connector: smallrye-kafka
        topic: leanda.folders.commands
        value.deserializer: io.quarkus.kafka.client.serialization.JsonbDeserializer
        group.id: core-api-folders
        
    outgoing:
      user-events:
        connector: smallrye-kafka
        topic: leanda.users.events
        value.serializer: io.quarkus.kafka.client.serialization.JsonbSerializer
        
      folder-events:
        connector: smallrye-kafka
        topic: leanda.folders.events
        value.serializer: io.quarkus.kafka.client.serialization.JsonbSerializer
```

### Event Publishing

```java
@ApplicationScoped
public class EventPublisher {
    
    @Inject
    @Channel("user-events")
    Emitter<UserEvent> userEventEmitter;
    
    @Inject
    @Channel("folder-events")
    Emitter<FolderEvent> folderEventEmitter;
    
    @Inject
    @Channel("file-events")
    Emitter<FileEvent> fileEventEmitter;
    
    public void publish(UserEvent event) {
        userEventEmitter.send(Message.of(event)
            .addMetadata(OutgoingKafkaRecordMetadata.builder()
                .withKey(event.getId().toString())
                .withHeaders(new RecordHeaders()
                    .add("correlationId", event.getCorrelationId().toString().getBytes())
                    .add("timestamp", Instant.now().toString().getBytes()))
                .build()));
    }
}
```

## Authentication & Authorization

### OIDC Integration

```java
// application.yaml
quarkus:
  oidc:
    auth-server-url: ${KEYCLOAK_URL}/realms/leanda
    client-id: leanda-api
    credentials:
      secret: ${OIDC_CLIENT_SECRET}
    tls:
      verification: required
  http:
    auth:
      permission:
        authenticated:
          paths: /api/*
          policy: authenticated
        public:
          paths: /api/nodes/public,/api/entities/*/public,/health,/ready
          policy: permit
```

### Security Filter

```java
@Provider
@Priority(Priorities.AUTHENTICATION)
public class UserInfoFilter implements ContainerRequestFilter {
    
    @Inject
    SecurityIdentity securityIdentity;
    
    @Override
    public void filter(ContainerRequestContext requestContext) {
        if (securityIdentity.isAnonymous()) {
            return;
        }
        
        UUID userId = UUID.fromString(securityIdentity.getPrincipal().getName());
        requestContext.setProperty("userId", userId);
    }
}
```

## Work Breakdown by Agent

### Phase 2 Completed Work ✅

#### Agent 1: Java Parsers Group A (Phase 2)
- [x] Create `chemical-parser` service (Port 8083)
- [x] Create `chemical-properties` service (Port 8086)
- [x] Create `reaction-parser` service (Port 8087)
- [x] Implement Indigo SDK integration
- [x] Implement Kafka command handlers
- [x] Implement event publishing
- [x] Create integration tests with WireMock

#### Agent 2: Java Parsers Group B (Phase 2)
- [x] Create `crystal-parser` service (Port 8089)
- [x] Create `spectra-parser` service (Port 8090)
- [x] Create `imaging` service (Port 8091)
- [x] Implement CIF parser
- [x] Implement JCAMP-DX parser
- [x] Implement rasterizers (Image, PDF, Microscopy, CIF, Structure, Reaction, Office)
- [x] Create integration tests

#### Agent 3: Blob Storage + Office Processor (Phase 2)
- [x] Create `blob-storage` service (Port 8084)
- [x] Create `office-processor` service (Port 8088)
- [x] Implement MongoDB GridFS storage
- [x] Implement REST API endpoints
- [x] Implement Office document converters (8 formats)
- [x] Implement metadata extractors (4 types)
- [x] Create comprehensive tests

#### Agent 4: Metadata + Indexing (Phase 2)
- [x] Create `metadata-processing` service (Port 8098)
- [x] Create `indexing` service (Port 8099)
- [x] Implement TypeQualifier for field detection
- [x] Implement OpenSearch integration
- [x] Implement text extraction with Apache Tika
- [x] Create event handlers for file/folder/record indexing

#### Agent 6: Frontend (Phase 2)
- [x] Migrate Angular 9 → Angular 21
- [x] Implement zoneless configuration
- [x] Migrate core services (Auth, SignalR)
- [x] Migrate shared components (9 components)
- [x] Migrate file view components (8 components)
- [x] Create unit tests (15+ test files)
- [x] Create integration testing guide

#### Agent 7: Testing Infrastructure (Phase 2)
- [x] Configure Testcontainers (MongoDB, Kafka, OpenSearch)
- [x] Create test base classes (`QuarkusIntegrationTestBase`, etc.)
- [x] Create test utilities (`KafkaTestUtil`, `MongoTestUtil`, etc.)
- [x] Create test fixtures (`TestDataFixtures`)
- [x] Create REST client mocking (WireMock)
- [x] Create blob storage mock helpers
- [x] Set up CI/CD pipelines

#### Agent 8: Docker + Integration (Phase 2)
- [x] Create `docker-compose.yml` with all infrastructure
- [x] Create Dockerfiles for all Quarkus services
- [x] Configure hot-reload for development
- [x] Set up environment variables
- [x] Create deployment scripts
- [x] Create integration test framework
- [x] Add Prometheus and Grafana monitoring
- [x] Create workflow tests

### Phase 1 Pending Work ⏳

#### Agent 1: Core API & REST Endpoints (Phase 1)
- [ ] Create `NodesResource` (GET, POST nodes)
- [ ] Create `EntitiesResource` (CRUD for files, folders, records, models)
- [ ] Create `UsersResource` (user management)
- [ ] Create `ExportsResource` (file export)
- [ ] Create `MachineLearningResource` (ML endpoints)
- [ ] Implement pagination with `PagedList`
- [ ] Implement filter parsing (OData-style)
- [ ] Configure OIDC authentication
- [ ] Generate OpenAPI documentation

#### Agent 2: Domain Services & Event Handlers (Phase 1)
- [ ] Create `UserEventHandler` (UserCreated, UserUpdated)
- [ ] Create `FolderEventHandler` (FolderCreated, etc.)
- [ ] Create `FileEventHandler` (FileCreated, etc.)
- [ ] Create `RecordEventHandler`
- [ ] Create `EventPublisher` utility
- [ ] Implement Saga patterns for file processing
- [ ] Configure Kafka topics and consumers
- [ ] Implement correlation ID propagation

#### Agent 3: Persistence & Data Layer (Phase 1)
- [ ] Create `Node` entity with Panache
- [ ] Create `User`, `File`, `Folder`, `Record`, `Model` entities
- [ ] Create repository classes
- [ ] Implement MongoDB aggregations
- [ ] Set up GridFS for blob storage (already done in blob-storage service)
- [ ] Implement event sourcing (optional)
- [ ] Create database migrations
- [ ] Set up indexes

### Future Work

#### Agent 5: ML Services
- [ ] Create Feature Calculator service
- [ ] Create Modeler service
- [ ] Create Predictor service
- [ ] Integrate with ML pipeline

## Architecture Patterns (Phase 2 Implementation)

### Event-Driven Parsing Pipeline

The Phase 2 services implement a clean event-driven architecture:

```
Kafka Command → Parser Service → Parse File → Publish Events
                                      ↓
                              Properties Service (optional)
                                      ↓
                              Metadata Processing
                                      ↓
                              Indexing Service
                                      ↓
                              OpenSearch Index
```

**Implementation Details**:
- Commands consumed via `@Incoming` annotations
- Events published via `@Outgoing` with `Emitter<T>`
- Correlation IDs propagated through message headers
- Error events published for failures

### Blob Storage Integration Pattern

All parser services use REST client pattern for blob operations:

```java
@RegisterRestClient(configKey = "blob-storage")
public interface BlobStorageClient {
    @GET
    @Path("/api/blobs/{bucket}/{blobId}")
    Uni<Response> downloadBlob(@PathParam("bucket") String bucket, 
                               @PathParam("blobId") UUID blobId);
    
    @GET
    @Path("/api/blobs/{bucket}/{blobId}/info")
    Uni<BlobInfo> getBlobInfo(@PathParam("bucket") String bucket,
                              @PathParam("blobId") UUID blobId);
}
```

**Benefits**:
- Clean separation of concerns
- Easy to mock in tests (WireMock)
- Type-safe API contracts
- Automatic retry and circuit breaker support

### Shared Models Pattern

Domain models shared across services prevent duplication:

- `shared/models/BlobInfo.java` - Blob metadata (id, bucket, length, md5, contentType)
- `shared/models/LoadedBlobInfo.java` - Blob with content
- `shared/models/Property.java` - Entity properties (name, value, category)
- `shared/models/VersionInfo.java` - Service version information

**Usage**: All services reference these models via Maven dependency on `shared` module.

### Integration Testing Pattern

Comprehensive testing framework using Testcontainers:

**Base Classes**:
- `QuarkusIntegrationTestBase` - Automatic Testcontainers setup (MongoDB, Kafka, OpenSearch)
- `QuarkusUnitTestBase` - Unit test base without containers
- `QuarkusRestClientTestBase` - REST client testing with WireMock

**Test Utilities**:
- `BlobStorageTestUtils` - Helper methods for blob operations in tests
- `KafkaTestUtil` - Kafka message publishing/consumption helpers
- `MongoTestUtil` - MongoDB query helpers
- `BlobStorageMock` - WireMock setup for blob storage API

**Workflow Tests**:
- `ChemicalParsingWorkflowTest` - End-to-end chemical file processing
- `BlobStorageWorkflowTest` - Blob upload/download/delete flows
- `OfficeProcessorWorkflowTest` - Office document conversion
- `MetadataProcessingWorkflowTest` - Metadata generation
- `IndexingWorkflowTest` - Search indexing
- `CompletePipelineWorkflowTest` - Full pipeline with all services

### Service Port Assignments

| Service | External Port | Internal Port | Notes |
|---------|--------------|---------------|-------|
| blob-storage | 8084 | 8084 | REST API |
| chemical-parser | 8083 | 8083 | Kafka consumer |
| chemical-properties | 8086 | 8086 | Kafka consumer |
| reaction-parser | 8087 | 8087 | Kafka consumer |
| office-processor | 8088 | 8080 | Kafka consumer |
| crystal-parser | 8089 | 8080 | Kafka consumer |
| spectra-parser | 8090 | 8080 | Kafka consumer |
| imaging | 8091 | 8080 | Kafka consumer |
| metadata-processing | 8098 | 8088 | Kafka consumer |
| indexing | 8099 | 8089 | Kafka consumer |

## Dependencies Between Components

### Phase 2 Architecture (Current)

```
Infrastructure (Docker Compose)
  ├── MongoDB (27017)
  ├── Redis (6379)
  ├── Redpanda/Kafka (9092)
  ├── OpenSearch (9200)
  │
  ├── Blob Storage API (8084)
  │   ├── Chemical Parser (8083) ──┐
  │   ├── Chemical Properties (8086) ──┐
  │   ├── Reaction Parser (8087) ──┐    │
  │   ├── Crystal Parser (8089) ──┼────┼── Kafka Events
  │   ├── Spectra Parser (8090) ──┘    │
  │   ├── Imaging (8091) ──────────────┘
  │   └── Office Processor (8088)
  │
  ├── Metadata Processing (8098)
  │   └── Indexing (8099) → OpenSearch
  │
  └── Frontend (Angular 21)
      └── (Will connect to Core API when built)
```

### Phase 1 Architecture (Planned)

```
┌─────────────────────────────────────────────────────────┐
│                     Core API Service (8080)              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │   REST      │  │   Event     │  │    Security    │ │
│  │  Resources  │──│  Handlers   │──│    Filters     │ │
│  └──────┬──────┘  └──────┬──────┘  └────────────────┘ │
│         │                │                              │
│  ┌──────▼──────────────▼──────┐                        │
│  │        Domain Services      │                        │
│  │  (CommandHandlers, Queries) │                        │
│  └──────────────┬──────────────┘                        │
│                 │                                        │
│  ┌──────────────▼──────────────┐                        │
│  │        Repositories         │                        │
│  │   (Panache MongoDB)         │                        │
│  └──────────────┬──────────────┘                        │
└─────────────────┼───────────────────────────────────────┘
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│ MongoDB │  │  Kafka  │  │  Redis  │
└─────────┘  └─────────┘  └─────────┘
```

## Legacy-only domain events (add when migrating record/Pdf/Reaction backends)

The file `specs/events/domain-events.yaml` currently covers User, Folder, File, Record (RecordCreated, RecordParsed, RecordFieldsUpdated, RecordPersisted), ML, Export, Processing, and Notifications. The following events and commands exist in legacy but are **not** yet in domain-events.yaml. Add them when implementing or migrating the corresponding backends:

- **RecordsFile** (Sds.Osdr.RecordsFile): RecordDeleted, FieldsAdded, TotalRecordsUpdated, AggregatedPropertiesAdded, RecordsFileCreated, FieldsUpdated, IssueAdded, InvalidRecordCreated, PropertyAdded, ImageAdded, PropertiesAdded, IssuesAdded; commands: AddFields, AddProperties, UpdateFields, DeleteRecord, AddImage, AddIssues, AddAggregatedProperties, UpdateTotalRecords, ChangeStatus, CreateInvalidRecord, SetAccessPermissions, CopyRecord.
- **Pdf** (Sds.Osdr.Pdf): PdfFileCreated.
- **Reactions** (Sds.Osdr.Reactions): ReactionCreated; command CreateReaction.

Extend `leanda.records.events` / `leanda.records.commands` (and file-type-specific channels if needed) in domain-events.yaml with the above message refs and payload schemas when those workflows are migrated.

## Migration Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Event schema incompatibility | High | Create versioned event schemas, implement schema evolution |
| MongoDB aggregation complexity | Medium | Port aggregations incrementally, add tests for each |
| OIDC token format differences | Medium | Use standard JWT claims, test with Keycloak |
| Kafka consumer offset management | Medium | Use consumer groups, implement idempotent handlers |
| Hot-reload issues | Low | Configure Quarkus dev mode properly |

## Phase 2 Lessons Learned

### What Worked Well ✅

1. **REST Client Pattern for Blob Storage**
   - All parser services use Quarkus REST Client to interact with blob-storage API
   - Clean separation of concerns, easy to mock in tests
   - Location: `services/*/infrastructure/BlobStorageClient.java`

2. **Shared Models Directory**
   - Domain models in `shared/models/` prevent duplication
   - Used across blob-storage, parsers, and other services
   - Examples: `BlobInfo`, `Property`, `VersionInfo`

3. **Test Utilities Framework**
   - Reusable test base classes in `tests/` directory
   - `QuarkusIntegrationTestBase` automatically sets up Testcontainers
   - `BlobStorageMock` simplifies blob operations in tests
   - Location: `tests/` directory

4. **Docker Compose for Local Development**
   - Single command to start all infrastructure and services
   - Hot-reload configured for all Quarkus services
   - Health checks ensure services are ready
   - Location: `docker-compose.yml`

5. **Integration Test Framework**
   - Workflow tests verify end-to-end flows
   - Testcontainers provide real infrastructure
   - Examples: `ChemicalParsingWorkflowTest`, `BlobStorageWorkflowTest`
   - Location: `tests/integration/workflows/`

6. **Event-Driven Architecture**
   - Kafka commands trigger parsing workflows
   - Events flow through: Parse → Properties → Metadata → Indexing
   - Clean separation between services

### Challenges & Solutions

1. **Port Conflicts**: Services use different internal/external ports
   - Solution: Document port mappings clearly in docker-compose.yml

2. **Test Data Management**: Need consistent test fixtures
   - Solution: `TestDataFixtures` class with reusable test data

3. **Service Dependencies**: Services depend on blob-storage
   - Solution: REST client pattern with health checks

## Success Criteria

### Phase 2 Complete ✅

- [x] All parser services implemented (chemical, crystal, spectra, reaction)
- [x] Blob storage API with GridFS backend
- [x] Office processor with 8 converters
- [x] Metadata processing service
- [x] Indexing service with OpenSearch
- [x] Frontend migrated to Angular 21
- [x] Unit test coverage > 80% for all services
- [x] Integration tests passing
- [x] Docker setup working with hot-reload
- [x] CI/CD pipeline functional
- [x] Monitoring with Prometheus and Grafana

### Phase 1 Pending ⏳

- [ ] Core API service implemented (REST endpoints)
- [ ] Domain event handlers implemented
- [ ] Persistence service implemented
- [ ] All REST endpoints with OpenAPI docs
- [ ] Authentication working with Keycloak
- [ ] MongoDB aggregations for node queries
- [ ] Event sourcing (optional)

### Future Work

- [ ] ML Services (Feature Calculator, Modeler, Predictor)
- [ ] Integration with SageMaker
- [ ] Apache Iceberg integration

