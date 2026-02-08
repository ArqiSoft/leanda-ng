# Phase 2: Spectra File Parser Service Migration

## Overview

Migrate the Spectra File Parser service from Java 8 / Spring Boot to Java 21 / Quarkus 3.x.

## Current State Analysis

### Legacy Service
- **Location**: `spectra-file-parser-service/`
- **Stack**: Java 8, Spring Boot
- **Supported Formats**: DX, JDX (JCAMP-DX format)
- **Parser**: Custom `JcampReader` implementation

### Message Contracts

Same structure as other parsers:
- **Command**: `ParseFile`
- **Events**: `FileParsed`, `RecordParsed`, `FileParseFailed`, `RecordParseFailed`

### Processing Logic

1. Receive `ParseFile` command
2. Download JCAMP-DX file from blob storage
3. Parse using `JcampReader` (custom implementation)
4. Extract spectrum records
5. For each record:
   - Upload parsed record as new blob (.jdx)
   - Extract properties/fields
   - Publish `RecordParsed` event
6. Publish `FileParsed` event
7. **Record Limit**: 100 records per file (temporary limitation)

### Key Components

- **JcampReader**: Reads JCAMP-DX format
- **JcampRecordsIterator**: Iterates over spectra in file
- **JSVSpectrum**: Spectrum data model
- **JSpecViewReader**: Alternative reader implementation

### Dependencies

- **Storage**: `com.github.arqisoft:storage:0.16`
- **Messaging**: `com.github.arqisoft:messaging:1.1`
- **Custom**: JCAMP-DX parsing logic

---

## Target Architecture

### Quarkus Service Structure

```
services/spectra-parser/
├── src/main/java/io/leanda/ng/spectraparser/
│   ├── domain/
│   │   ├── commands/ParseFileCommand.java
│   │   ├── events/FileParsedEvent.java
│   │   └── models/Field.java
│   ├── application/
│   │   ├── SpectraParserService.java
│   │   └── JcampParser.java              # Port JCAMP parser
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
- **Parser**: Port existing JCAMP parser to Java 21

---

## Migration Strategy

### Phase 1: Port JCAMP Parser

1. **Port JCAMP parsing classes**:
   - `JcampReader.java`
   - `JcampRecordsIterator.java`
   - `JSVSpectrum.java`
   - `JSpecViewReader.java`

2. **Update to Java 21**:
   - Use modern Java features
   - Improve error handling
   - Add validation

### Phase 2: Service Implementation

1. **Create Quarkus project**
2. **Implement command handler** - Consume from `spectra-parse-commands`
3. **Integrate JCAMP parser**
4. **Implement event publishing**

### Phase 3: Testing

1. **Unit tests** - JCAMP parsing logic
2. **Integration tests** - End-to-end parsing

---

## Implementation Details

### JCAMP Parser Port

```java
@ApplicationScoped
public class JcampParser implements Iterable<SpectrumRecord> {
    
    private final InputStream inputStream;
    
    public JcampParser(InputStream inputStream) {
        this.inputStream = inputStream;
    }
    
    @Override
    public Iterator<SpectrumRecord> iterator() {
        return new JcampRecordsIterator(new JcampReader(inputStream));
    }
}

public record SpectrumRecord(
    long index,
    String data,                    // JCAMP-DX data
    List<SpectrumField> properties
) {}

public record SpectrumField(
    String name,
    String value
) {}
```

### Parser Service

```java
@ApplicationScoped
public class SpectraParserService {
    
    @Inject
    BlobStorageClient blobStorage;
    
    public ParsingResult parseFile(UUID fileId, UUID blobId, String bucket) {
        // Download JCAMP-DX file
        byte[] fileData = blobStorage.downloadBlob(blobId, bucket);
        
        // Parse JCAMP-DX
        JcampParser parser = new JcampParser(new ByteArrayInputStream(fileData));
        
        List<RecordParsedEvent> recordEvents = new ArrayList<>();
        long parsedCount = 0;
        long failedCount = 0;
        Set<String> uniqueFields = new HashSet<>();
        
        int index = 0;
        for (SpectrumRecord record : parser) {
            if (index >= 100) break; // Temporary limit
            
            try {
                // Upload parsed record
                UUID recordBlobId = blobStorage.uploadBlob(
                    bucket,
                    record.data().getBytes(),
                    "chemical/x-jcamp-dx"
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

### JCAMP Parser
- **Maintained**: JCAMP-DX format support
- **Maintained**: Record structure
- **Improved**: Error handling, Java 21 features

---

## Testing Requirements

### Unit Tests (>80% coverage)
- JCAMP parsing logic
- Field extraction
- Record iteration
- Error handling

### Integration Tests
- Kafka command consumption
- Event publishing
- Sample JCAMP-DX file parsing

---

## Dependencies

### Needs From
- Agent 3: Blob Storage service
- Agent 8: Kafka infrastructure

### Provides To
- Core API: Parsed spectra records
- Indexing: Spectra data for search

---

## Success Criteria

- [ ] JCAMP parser ported to Java 21
- [ ] Message contracts defined
- [ ] Command handler implemented
- [ ] Event publishing working
- [ ] Unit test coverage >80%
- [ ] Integration tests passing
- [ ] Supports DX, JDX formats

---

## Timeline

- **Week 1**: JCAMP parser port, message contracts
- **Week 2**: Service implementation
- **Week 3**: Testing, integration

**Total: 3 weeks**

