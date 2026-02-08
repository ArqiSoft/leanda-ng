# Phase 2: Chemical File Parser Service Migration

## Overview

Migrate the Chemical File Parser service from Java 8 / Spring Boot 2.0 RC1 to Java 21 / Quarkus 3.x, maintaining message contract compatibility while modernizing the implementation.

## Current State Analysis

### Legacy Service
- **Location**: `chemical-file-parser-service/`
- **Stack**: Java 8, Spring Boot 2.0.0.RC1
- **Main Class**: `sds.chemicalfileparser.Application`
- **Messaging**: RabbitMQ via `jtransit-light` library
- **Chemistry Library**: Indigo SDK 1.3.0beta.r16

### Supported File Formats
- **MOL** - MDL Molfile format
- **SDF** - Structure-Data File format
- **CDX** - ChemDraw binary format

### Message Contracts

#### Command: `ParseFile`
```java
public class ParseFile {
    private UUID id;              // File ID
    private UUID blobId;          // Blob storage ID
    private String bucket;         // Storage bucket
    private UUID userId;           // User ID
    private UUID correlationId;    // Correlation ID for saga
}
```

#### Event: `FileParsed`
```java
public class FileParsed {
    private UUID id;
    private long parsedRecords;
    private long failedRecords;
    private long totalRecords;
    private List<String> fields;      // Unique field names found
    private UUID correlationId;
    private UUID userId;
    private String timeStamp;
}
```

#### Event: `RecordParsed`
```java
public class RecordParsed {
    private UUID id;                 // Record ID
    private UUID fileId;             // Parent file ID
    private long index;               // Record index in file
    private List<Field> fields;      // Record properties
    private UUID blobId;             // Parsed record blob ID
    private String bucket;
    private UUID correlationId;
    private UUID userId;
    private String timeStamp;
}
```

#### Event: `FileParseFailed`
```java
public class FileParseFailed {
    private UUID id;
    private long parsedRecords;
    private long failedRecords;
    private long totalRecords;
    private String message;          // Error message
    private UUID correlationId;
    private UUID userId;
    private String timeStamp;
}
```

#### Event: `RecordParseFailed`
```java
public class RecordParseFailed {
    private UUID id;
    private UUID fileId;
    private long index;
    private String message;
    private UUID correlationId;
    private UUID userId;
    private String timeStamp;
}
```

### Processing Logic

1. **Receive `ParseFile` command** from RabbitMQ queue
2. **Download blob** from storage using `BlobStorage` interface
3. **Detect file format** by extension (.mol, .sdf, .cdx)
4. **Parse file** using Indigo SDK:
   - `indigo.iterateSDFile()` for SDF/MOL
   - `indigo.iterateCDXFile()` for CDX
5. **For each record**:
   - Extract MOL file string
   - Extract properties/fields
   - Upload parsed record as new blob
   - Publish `RecordParsed` event
6. **On completion**: Publish `FileParsed` event with summary
7. **On error**: Publish `FileParseFailed` or `RecordParseFailed`

### Dependencies

- **Indigo SDK**: `com.epam.indigo:indigo:1.3.0beta.r16`
- **Storage**: `com.github.arqisoft:storage:0.16` (BlobStorage interface)
- **Messaging**: `com.github.arqisoft:messaging:1.1` (jtransit-light wrapper)
- **MongoDB**: `org.mongodb:mongo-java-driver` (for storage)
- **Spring Boot**: 2.0.0.RC1

---

## Target Architecture

### Quarkus Service Structure

```
services/chemical-parser/
├── src/main/java/io/leanda/ng/chemicalparser/
│   ├── domain/
│   │   ├── commands/
│   │   │   └── ParseFileCommand.java
│   │   ├── events/
│   │   │   ├── FileParsedEvent.java
│   │   │   ├── RecordParsedEvent.java
│   │   │   ├── FileParseFailedEvent.java
│   │   │   └── RecordParseFailedEvent.java
│   │   └── models/
│   │       └── Field.java
│   ├── application/
│   │   ├── ChemicalParserService.java    # Main parsing logic
│   │   └── IndigoAdapter.java            # Indigo SDK wrapper
│   ├── infrastructure/
│   │   ├── ParseFileCommandHandler.java  # Kafka consumer
│   │   └── EventPublisher.java           # Kafka producer
│   └── config/
│       └── ChemicalParserConfig.java
├── src/test/java/
│   ├── ChemicalParserServiceTest.java
│   └── ParseFileCommandHandlerTest.java
└── pom.xml
```

### Technology Stack

- **Framework**: Quarkus 3.17+
- **Java**: 21 LTS
- **Chemistry**: Indigo SDK (native library integration)
- **Messaging**: SmallRye Reactive Messaging (Kafka)
- **Storage**: Blob Storage client (HTTP/gRPC)
- **Testing**: JUnit 5, Testcontainers

---

## Migration Strategy

### Phase 1: Message Contract Definition

1. **Create AsyncAPI Specification**
   - Define `ParseFile` command schema
   - Define all event schemas
   - Define Kafka topics
   - Location: `shared/contracts/events/chemical-parser-events.yaml`

2. **Define Domain Models**
   - `ParseFileCommand`, `FileParsedEvent`, `RecordParsedEvent`
   - Location: `shared/models/chemical-parser/`

### Phase 2: Service Implementation

1. **Create Quarkus Project**
   ```bash
   mvn io.quarkus.platform:quarkus-maven-plugin:3.17.0:create \
     -DprojectGroupId=io.leanda.ng \
     -DprojectArtifactId=chemical-parser \
     -Dextensions="kafka,reactive-messaging"
   ```

2. **Implement Command Handler**
   - Consume `ParseFile` commands from Kafka topic `chemical-parse-commands`
   - Process files using Indigo SDK
   - Publish events to Kafka topics

3. **Implement Indigo Adapter**
   - Wrap Indigo SDK calls
   - Handle native library loading
   - Configure Indigo options (timeout, error handling)

4. **Implement Event Publishing**
   - Publish `FileParsed` to `chemical-file-parsed`
   - Publish `RecordParsed` to `chemical-record-parsed`
   - Publish failure events to error topics

### Phase 3: Testing & Integration

1. **Unit Tests**
   - Test parsing logic for MOL/SDF/CDX
   - Test field extraction
   - Test error handling

2. **Integration Tests**
   - Test with Kafka Testcontainer
   - Test with sample chemical files
   - Test blob storage integration

---

## Implementation Details

### Command Handler

```java
@ApplicationScoped
public class ParseFileCommandHandler {
    
    @Inject
    ChemicalParserService parserService;
    
    @Inject
    EventPublisher eventPublisher;
    
    @Incoming("chemical-parse-commands")
    public CompletionStage<Void> process(ParseFileCommand command) {
        return CompletableFuture.runAsync(() -> {
            try {
                ParsingResult result = parserService.parseFile(
                    command.getId(),
                    command.getBlobId(),
                    command.getBucket()
                );
                
                // Publish record events
                for (RecordParsedEvent recordEvent : result.getRecordEvents()) {
                    eventPublisher.publishRecordParsed(recordEvent);
                }
                
                // Publish file completion event
                eventPublisher.publishFileParsed(result.getFileParsedEvent());
                
            } catch (Exception e) {
                eventPublisher.publishFileParseFailed(
                    command.getId(),
                    command.getCorrelationId(),
                    command.getUserId(),
                    e.getMessage()
                );
            }
        });
    }
}
```

### Parser Service

```java
@ApplicationScoped
public class ChemicalParserService {
    
    @Inject
    BlobStorageClient blobStorage;
    
    @Inject
    IndigoAdapter indigo;
    
    public ParsingResult parseFile(UUID fileId, UUID blobId, String bucket) {
        // Download blob
        byte[] fileData = blobStorage.downloadBlob(blobId, bucket);
        
        // Detect format
        String extension = detectExtension(blobId, bucket);
        
        // Parse with Indigo
        List<Record> records = indigo.parseFile(fileData, extension);
        
        // Process records
        List<RecordParsedEvent> recordEvents = new ArrayList<>();
        long parsedCount = 0;
        long failedCount = 0;
        Set<String> uniqueFields = new HashSet<>();
        
        for (Record record : records) {
            try {
                // Upload parsed record blob
                UUID recordBlobId = blobStorage.uploadBlob(
                    bucket,
                    record.getMolFile(),
                    "chemical/x-mdl-molfile"
                );
                
                // Extract fields
                List<Field> fields = extractFields(record);
                uniqueFields.addAll(fields.stream()
                    .map(Field::getName)
                    .collect(Collectors.toList()));
                
                // Create event
                RecordParsedEvent event = RecordParsedEvent.builder()
                    .id(UUID.randomUUID())
                    .fileId(fileId)
                    .index(parsedCount)
                    .fields(fields)
                    .blobId(recordBlobId)
                    .bucket(bucket)
                    .build();
                    
                recordEvents.add(event);
                parsedCount++;
                
            } catch (Exception e) {
                // Publish record failure
                eventPublisher.publishRecordParseFailed(
                    fileId, parsedCount, e.getMessage()
                );
                failedCount++;
            }
        }
        
        // Create file completion event
        FileParsedEvent fileEvent = FileParsedEvent.builder()
            .id(fileId)
            .parsedRecords(parsedCount)
            .failedRecords(failedCount)
            .totalRecords(parsedCount + failedCount)
            .fields(new ArrayList<>(uniqueFields))
            .build();
        
        return new ParsingResult(recordEvents, fileEvent);
    }
}
```

### Indigo Adapter

```java
@ApplicationScoped
public class IndigoAdapter {
    
    private Indigo indigo;
    
    @PostConstruct
    void init() {
        indigo = new Indigo();
        indigo.setOption("ignore-stereochemistry-errors", "true");
        indigo.setOption("unique-dearomatization", "false");
        indigo.setOption("ignore-noncritical-query-features", "true");
        indigo.setOption("timeout", "600000");
    }
    
    public List<Record> parseFile(byte[] fileData, String extension) {
        File tempFile = createTempFile(fileData);
        
        try {
            IndigoObject records;
            switch (extension.toLowerCase()) {
                case "mol":
                case "sdf":
                    records = indigo.iterateSDFile(tempFile.getAbsolutePath());
                    break;
                case "cdx":
                    records = indigo.iterateCDXFile(tempFile.getAbsolutePath());
                    break;
                default:
                    throw new UnsupportedFormatException(extension);
            }
            
            List<Record> result = new ArrayList<>();
            for (IndigoObject record : records) {
                String molFile = record.molfile();
                List<Field> fields = extractProperties(record);
                result.add(new Record(molFile, fields));
            }
            
            return result;
            
        } finally {
            tempFile.delete();
        }
    }
    
    private List<Field> extractProperties(IndigoObject record) {
        List<Field> fields = new ArrayList<>();
        for (IndigoObject property : record.iterateProperties()) {
            fields.add(new Field(
                property.name(),
                property.rawData()
            ));
        }
        return fields;
    }
}
```

---

## Breaking Changes & Compatibility

### Message Format
- **Changed**: RabbitMQ → Kafka
- **Changed**: jtransit-light → Avro/JSON Schema
- **Maintained**: Command/event structure (field names, types)

### Processing Logic
- **Maintained**: Indigo SDK usage
- **Maintained**: File format support (MOL, SDF, CDX)
- **Maintained**: Field extraction logic

### Migration Path
1. Deploy Quarkus service alongside Java service
2. Route commands to both services (dual-write)
3. Compare outputs for validation
4. Switch traffic to Quarkus service
5. Decommission Java service

---

## Testing Requirements

### Unit Tests (>80% coverage)
- File format detection
- Indigo parsing logic
- Field extraction
- Error handling

### Integration Tests
- Kafka command consumption
- Event publishing
- Blob storage integration
- Sample file parsing (MOL, SDF, CDX)

### Performance Tests
- Large SDF files (1000+ records)
- Concurrent parsing (multiple files)

---

## Dependencies

### Needs From
- Agent 3: Blob Storage service (for download/upload)
- Agent 8: Kafka infrastructure
- Agent 7: Test infrastructure

### Provides To
- Core API: Parsed chemical records
- Chemical Properties: Parsed molecules for property calculation
- Indexing: Chemical structure data for search

---

## Success Criteria

- [ ] All message contracts defined (AsyncAPI)
- [ ] Command handler implemented
- [ ] Indigo SDK integration working
- [ ] Event publishing to Kafka working
- [ ] Unit test coverage >80%
- [ ] Integration tests passing
- [ ] Supports MOL, SDF, CDX formats
- [ ] Performance meets or exceeds Java 8 version

---

## Timeline

- **Week 1**: Message contract definition, Quarkus project setup
- **Week 2**: Parser implementation, Indigo integration
- **Week 3**: Testing, documentation, integration

**Total: 3 weeks**

