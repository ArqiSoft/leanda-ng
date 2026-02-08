# Phase 2: Indexing Service Migration

## Overview

Migrate the Indexing Service from .NET Core / Elasticsearch to Java 21 / Quarkus 3.x / OpenSearch Serverless, maintaining search functionality while modernizing the stack.

## Current State Analysis

### Legacy Service
- **Location**: `indexing-service/Sds.Indexing/`
- **Stack**: .NET Core, Elasticsearch (NEST client)
- **Port**: 11090
- **Purpose**: Index entities (Files, Folders, Records, Users, Models) for full-text search

### Indexed Entity Types

1. **Files** - File metadata and content (for PDF, TXT, CSV, etc.)
2. **Folders** - Folder metadata
3. **Records** - Parsed record data
4. **Users** - User profiles
5. **Models** - ML model metadata

### Event Handlers

The service consumes domain events and updates Elasticsearch indices:

- **FileEventHandler**: Handles `FilePersisted`, `FileDeleted`, `FileNamePersisted`, `FileParentPersisted`, `NodeStatusPersisted`, `PermissionsChanged`
- **FolderEventHandler**: Handles folder events
- **RecordEventHandler**: Handles record events
- **ModelEventHandler**: Handles model events
- **UserEventHandlers**: Handles user events

### Processing Logic

1. **Consume domain events** from RabbitMQ (via MassTransit)
2. **Fetch entity data** from MongoDB
3. **Index to Elasticsearch**:
   - For text files (PDF, TXT, CSV, etc.): Download blob, extract text, index with base64 content
   - For other files: Index metadata only
4. **Update permissions** in Elasticsearch access control
5. **Handle deletions** - Remove from index

### Elasticsearch Pipeline

The service uses an Elasticsearch pipeline `process_blob` to:
- Extract text from base64-encoded blob content
- Index extracted text for full-text search

### Dependencies

- **Elasticsearch**: NEST client for .NET
- **MongoDB**: MongoDB driver for entity data
- **MassTransit**: Event consumption
- **Blob Storage**: For downloading file content

---

## Target Architecture

### Quarkus Service Structure

```
services/indexing/
├── src/main/java/io/leanda/ng/indexing/
│   ├── domain/
│   │   ├── events/
│   │   │   ├── FilePersistedEvent.java
│   │   │   ├── FileDeletedEvent.java
│   │   │   └── ...
│   │   └── models/
│   │       └── IndexedEntity.java
│   ├── application/
│   │   ├── IndexingService.java
│   │   ├── TextExtractionService.java
│   │   └── PermissionService.java
│   ├── infrastructure/
│   │   ├── opensearch/
│   │   │   ├── OpenSearchClient.java
│   │   │   └── IndexManager.java
│   │   ├── eventhandlers/
│   │   │   ├── FileEventHandler.java
│   │   │   ├── FolderEventHandler.java
│   │   │   ├── RecordEventHandler.java
│   │   │   ├── ModelEventHandler.java
│   │   │   └── UserEventHandler.java
│   │   └── EventConsumer.java
│   └── config/
└── pom.xml
```

### Technology Stack

- **Framework**: Quarkus 3.17+
- **Java**: 21 LTS
- **Search**: OpenSearch Serverless (AWS managed)
- **Client**: OpenSearch Java Client 2.x
- **Text Extraction**: Apache Tika (for PDF, Office docs)
- **Messaging**: SmallRye Reactive Messaging (Kafka)
- **Database**: MongoDB client (for entity data)

---

## Migration Strategy

### Phase 1: OpenSearch Setup

1. **Create OpenSearch Serverless collection** (via CDK)
2. **Define index mappings**:
   - `files` index
   - `folders` index
   - `records` index
   - `users` index
   - `models` index
3. **Define access policies** (for permissions)

### Phase 2: Service Implementation

1. **Create Quarkus project**
2. **Implement OpenSearch client** - Connect to OpenSearch Serverless
3. **Port event handlers** - Convert from .NET to Java
4. **Implement text extraction** - Use Apache Tika
5. **Implement indexing logic** - Index entities to OpenSearch

### Phase 3: Testing

1. **Unit tests** - Indexing logic, text extraction
2. **Integration tests** - OpenSearch indexing, event consumption

---

## Implementation Details

### OpenSearch Client

```java
@ApplicationScoped
public class OpenSearchClient {
    
    private final RestClient restClient;
    private final ObjectMapper objectMapper;
    
    @ConfigProperty(name = "opensearch.endpoint")
    String endpoint;
    
    @ConfigProperty(name = "opensearch.region")
    String region;
    
    @PostConstruct
    void init() {
        // Initialize AWS OpenSearch Serverless client
        Aws4Signer signer = Aws4Signer.create();
        // ... configure client with IAM auth
    }
    
    public void indexDocument(String index, String id, Map<String, Object> document) {
        // Index document to OpenSearch
        Request request = new Request("PUT", "/" + index + "/_doc/" + id);
        request.setJsonEntity(objectMapper.writeValueAsString(document));
        restClient.performRequest(request);
    }
    
    public void deleteDocument(String index, String id) {
        Request request = new Request("DELETE", "/" + index + "/_doc/" + id);
        restClient.performRequest(request);
    }
}
```

### File Event Handler

```java
@ApplicationScoped
public class FileEventHandler {
    
    @Inject
    OpenSearchClient openSearchClient;
    
    @Inject
    BlobStorageClient blobStorage;
    
    @Inject
    TextExtractionService textExtractionService;
    
    @Inject
    MongoClient mongoClient;
    
    @Incoming("file-events")
    public CompletionStage<Void> handleFileEvent(FilePersistedEvent event) {
        return CompletableFuture.runAsync(() -> {
            // Fetch file from MongoDB
            BsonDocument file = fetchFileFromMongo(event.getId());
            
            // Check if file should be indexed (PDF, TXT, CSV, etc.)
            String extension = getExtension(file.getString("FileName").getValue());
            if (shouldIndexContent(extension)) {
                // Download blob and extract text
                byte[] blobContent = blobStorage.downloadBlob(
                    file.getDocument("Blob").getString("id").getValue(),
                    file.getString("Bucket").getValue()
                );
                String extractedText = textExtractionService.extractText(blobContent, extension);
                
                // Index with content
                Map<String, Object> document = buildDocument(file, extractedText);
                openSearchClient.indexDocument("files", event.getId().toString(), document);
            } else {
                // Index metadata only
                Map<String, Object> document = buildDocument(file, null);
                openSearchClient.indexDocument("files", event.getId().toString(), document);
            }
        });
    }
    
    @Incoming("file-events")
    public CompletionStage<Void> handleFileDeleted(FileDeletedEvent event) {
        return CompletableFuture.runAsync(() -> {
            openSearchClient.deleteDocument("files", event.getId().toString());
            // Also delete related records
            openSearchClient.deleteByQuery("records", 
                Map.of("FileId", event.getId().toString()));
        });
    }
}
```

### Text Extraction Service

```java
@ApplicationScoped
public class TextExtractionService {
    
    private final Tika tika;
    
    @PostConstruct
    void init() {
        tika = new Tika();
    }
    
    public String extractText(byte[] content, String extension) {
        try {
            return tika.parseToString(new ByteArrayInputStream(content));
        } catch (Exception e) {
            LOGGER.error("Failed to extract text from {}: {}", extension, e.getMessage());
            return "";
        }
    }
}
```

---

## Breaking Changes & Compatibility

### Search Backend
- **Changed**: Elasticsearch → OpenSearch Serverless
- **Changed**: NEST client → OpenSearch Java Client
- **Maintained**: Index structure (mappings, fields)

### Event Format
- **Changed**: MassTransit / RabbitMQ → Kafka
- **Maintained**: Event structure (field names, types)

### Text Extraction
- **Changed**: Elasticsearch pipeline → Apache Tika
- **Maintained**: Supported file formats (PDF, TXT, CSV, Office)

---

## Testing Requirements

### Unit Tests (>80% coverage)
- Indexing logic
- Text extraction
- Event handling
- Permission updates

### Integration Tests
- OpenSearch indexing
- Kafka event consumption
- Text extraction from sample files

### Performance Tests
- Large file indexing
- Concurrent indexing

---

## Dependencies

### Needs From
- Agent 3: Blob Storage service
- Agent 4: MongoDB access
- Agent 8: OpenSearch Serverless infrastructure

### Provides To
- Core API: Search functionality
- Frontend: Search results

---

## Success Criteria

- [ ] OpenSearch Serverless collection created
- [ ] All event handlers ported
- [ ] Text extraction working
- [ ] Indexing working for all entity types
- [ ] Unit test coverage >80%
- [ ] Integration tests passing
- [ ] Search functionality verified

---

## Timeline

- **Week 1**: OpenSearch setup, event handler port
- **Week 2**: Service implementation, text extraction
- **Week 3**: Testing, integration

**Total: 3 weeks**

