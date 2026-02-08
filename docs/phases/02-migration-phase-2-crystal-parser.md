# Phase 2: Crystal File Parser Service Migration

## Overview

Migrate the Crystal File Parser service from Java 8 / Spring Boot to Java 21 / Quarkus 3.x.

## Current State Analysis

### Legacy Service
- **Location**: `crystal-file-parser-service/`
- **Stack**: Java 8, Spring Boot
- **Supported Format**: CIF (Crystallographic Information File)
- **Parser**: Custom `CifParser` implementation

### Message Contracts

Same structure as Chemical Parser:
- **Command**: `ParseFile`
- **Events**: `FileParsed`, `RecordParsed`, `FileParseFailed`, `RecordParseFailed`

### Processing Logic

1. Receive `ParseFile` command
2. Download CIF file from blob storage
3. Parse using `CifParser` (custom implementation)
4. Extract CIF records (data blocks)
5. For each record:
   - Upload parsed record as new blob (.cif)
   - Extract properties/fields
   - Publish `RecordParsed` event
6. Publish `FileParsed` event with summary

### Key Differences from Chemical Parser

- **No Indigo SDK** - Uses custom CIF parser
- **Format**: CIF only (not MOL/SDF/CDX)
- **Record Limit**: 100 records per file (temporary limitation)
- **Parser**: `CifParser`, `CifReader`, `CifRecordsIterator`

### Dependencies

- **Storage**: `com.github.arqisoft:storage:0.16`
- **Messaging**: `com.github.arqisoft:messaging:1.1`
- **Custom**: CIF parsing logic (no external chemistry library)

---

## Target Architecture

### Quarkus Service Structure

```
services/crystal-parser/
├── src/main/java/io/leanda/ng/crystalparser/
│   ├── domain/
│   │   ├── commands/ParseFileCommand.java
│   │   ├── events/FileParsedEvent.java
│   │   └── models/Field.java
│   ├── application/
│   │   ├── CrystalParserService.java
│   │   └── CifParser.java              # Port CIF parser
│   ├── infrastructure/
│   │   ├── ParseFileCommandHandler.java
│   │   └── EventPublisher.java
│   └── config/
└── pom.xml
```

### Technology Stack

- **Framework**: Quarkus 3.17+
- **Java**: 21 LTS
- **Messaging**: SmallRye Reactive Messaging (Kafka)
- **Parser**: Port existing CIF parser to Java 21

---

## Migration Strategy

### Phase 1: Port CIF Parser

1. **Port CIF parsing classes**:
   - `CifParser.java`
   - `CifReader.java`
   - `CifRecordsIterator.java`
   - `Field.java`, `PropertyValue.java`, `Record.java`

2. **Update to Java 21**:
   - Use modern Java features (records, pattern matching)
   - Improve error handling
   - Add validation

### Phase 2: Service Implementation

1. **Create Quarkus project**
2. **Implement command handler** - Consume from `crystal-parse-commands`
3. **Integrate CIF parser**
4. **Implement event publishing**

### Phase 3: Testing

1. **Unit tests** - CIF parsing logic
2. **Integration tests** - End-to-end parsing

---

## Implementation Details

### CIF Parser Port

```java
@ApplicationScoped
public class CifParser implements Iterable<CifRecord> {
    
    private final InputStream inputStream;
    
    public CifParser(InputStream inputStream) {
        this.inputStream = inputStream;
    }
    
    @Override
    public Iterator<CifRecord> iterator() {
        return new CifRecordsIterator(new CifReader(inputStream));
    }
}

public record CifRecord(
    long index,
    String data,
    List<CifField> properties
) {}

public record CifField(
    String name,
    String value
) {}
```

### Parser Service

```java
@ApplicationScoped
public class CrystalParserService {
    
    @Inject
    BlobStorageClient blobStorage;
    
    public ParsingResult parseFile(UUID fileId, UUID blobId, String bucket) {
        // Download CIF file
        byte[] fileData = blobStorage.downloadBlob(blobId, bucket);
        
        // Parse CIF
        CifParser parser = new CifParser(new ByteArrayInputStream(fileData));
        
        List<RecordParsedEvent> recordEvents = new ArrayList<>();
        long parsedCount = 0;
        long failedCount = 0;
        Set<String> uniqueFields = new HashSet<>();
        
        int index = 0;
        for (CifRecord record : parser) {
            if (index >= 100) break; // Temporary limit
            
            try {
                // Upload parsed record
                UUID recordBlobId = blobStorage.uploadBlob(
                    bucket,
                    record.data().getBytes(),
                    "chemical/x-cif"
                );
                
                // Extract fields
                List<Field> fields = record.properties().stream()
                    .map(f -> new Field(f.name(), f.value()))
                    .collect(Collectors.toList());
                
                uniqueFields.addAll(fields.stream()
                    .map(Field::getName)
                    .collect(Collectors.toSet()));
                
                // Create event
                RecordParsedEvent event = RecordParsedEvent.builder()
                    .id(UUID.randomUUID())
                    .fileId(fileId)
                    .index(index)
                    .fields(fields)
                    .blobId(recordBlobId)
                    .bucket(bucket)
                    .build();
                    
                recordEvents.add(event);
                parsedCount++;
                
            } catch (Exception e) {
                // Publish record failure
                eventPublisher.publishRecordParseFailed(fileId, index, e.getMessage());
                failedCount++;
            }
            
            index++;
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

---

## Breaking Changes & Compatibility

### Message Format
- **Changed**: RabbitMQ → Kafka
- **Maintained**: Command/event structure

### CIF Parser
- **Maintained**: CIF format support
- **Maintained**: Record structure
- **Improved**: Error handling, Java 21 features

---

## Testing Requirements

### Unit Tests (>80% coverage)
- CIF parsing logic
- Field extraction
- Record iteration
- Error handling

### Integration Tests
- Kafka command consumption
- Event publishing
- Sample CIF file parsing

---

## Dependencies

### Needs From
- Agent 3: Blob Storage service
- Agent 8: Kafka infrastructure

### Provides To
- Core API: Parsed crystal structures
- Indexing: Crystal data for search

---

## Success Criteria

- [ ] CIF parser ported to Java 21
- [ ] Message contracts defined
- [ ] Command handler implemented
- [ ] Event publishing working
- [ ] Unit test coverage >80%
- [ ] Integration tests passing

---

## Timeline

- **Week 1**: CIF parser port, message contracts
- **Week 2**: Service implementation
- **Week 3**: Testing, integration

**Total: 3 weeks**

