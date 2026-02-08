# Phase 2: Reaction File Parser Service Migration

## Overview

Migrate the Reaction File Parser service from Java 8 / Spring Boot to Java 21 / Quarkus 3.x.

## Current State Analysis

### Legacy Service
- **Location**: `reaction-file-parser-service/`
- **Stack**: Java 8, Spring Boot
- **Supported Formats**: RDF, RXN, CDX
- **Chemistry Library**: Indigo SDK

### Message Contracts

Same structure as Chemical Parser:
- **Command**: `ParseFile`
- **Events**: `FileParsed`, `RecordParsed`, `FileParseFailed`, `RecordParseFailed`

### Processing Logic

1. Receive `ParseFile` command
2. Download reaction file from blob storage
3. Parse using Indigo SDK:
   - `indigo.iterateRDFile()` for RDF/RXN
   - `indigo.iterateCDXFile()` for CDX
4. For each reaction record:
   - Extract RXN file string (`record.rxnfile()`)
   - Extract properties
   - Upload parsed record as new blob (.rxn)
   - Publish `RecordParsed` event
5. Publish `FileParsed` event

### Key Differences from Chemical Parser

- **Format**: RDF, RXN, CDX (reactions, not molecules)
- **Extraction**: `record.rxnfile()` instead of `record.molfile()`
- **MIME Type**: `chemical/x-mdl-rxn` instead of `chemical/x-mdl-molfile`

### Dependencies

- **Indigo SDK**: `com.epam.indigo:indigo:1.3.0beta.r16`
- **Storage**: `com.github.arqisoft:storage:0.16`
- **Messaging**: `com.github.arqisoft:messaging:1.1`

---

## Target Architecture

### Quarkus Service Structure

```
services/reaction-parser/
├── src/main/java/io/leanda/ng/reactionparser/
│   ├── domain/
│   │   ├── commands/ParseFileCommand.java
│   │   ├── events/FileParsedEvent.java
│   │   └── models/Field.java
│   ├── application/
│   │   ├── ReactionParserService.java
│   │   └── IndigoReactionAdapter.java
│   ├── infrastructure/
│   │   ├── ParseFileCommandHandler.java
│   │   └── EventPublisher.java
│   └── config/
└── pom.xml
```

### Technology Stack

- **Framework**: Quarkus 3.17+
- **Java**: 21 LTS
- **Chemistry**: Indigo SDK
- **Messaging**: SmallRye Reactive Messaging (Kafka)

---

## Migration Strategy

### Phase 1: Message Contract Definition

1. **Create AsyncAPI Specification**
   - Define `ParseFile` command
   - Define events
   - Location: `shared/contracts/events/reaction-parser-events.yaml`

### Phase 2: Service Implementation

1. **Create Quarkus project**
2. **Implement Indigo adapter** - Similar to chemical parser but for reactions
3. **Implement command handler** - Consume from `reaction-parse-commands`
4. **Implement event publishing**

### Phase 3: Testing

1. **Unit tests** - Reaction parsing logic
2. **Integration tests** - End-to-end parsing

---

## Implementation Details

### Indigo Reaction Adapter

```java
@ApplicationScoped
public class IndigoReactionAdapter {
    
    private Indigo indigo;
    
    @PostConstruct
    void init() {
        indigo = new Indigo();
        indigo.setOption("ignore-stereochemistry-errors", "true");
        indigo.setOption("unique-dearomatization", "false");
        indigo.setOption("ignore-noncritical-query-features", "true");
        indigo.setOption("timeout", "600000");
    }
    
    public List<ReactionRecord> parseFile(byte[] fileData, String extension) {
        File tempFile = createTempFile(fileData);
        
        try {
            IndigoObject reactions;
            switch (extension.toLowerCase()) {
                case "rdf":
                case "rxn":
                    reactions = indigo.iterateRDFile(tempFile.getAbsolutePath());
                    break;
                case "cdx":
                    reactions = indigo.iterateCDXFile(tempFile.getAbsolutePath());
                    break;
                default:
                    throw new UnsupportedFormatException(extension);
            }
            
            List<ReactionRecord> result = new ArrayList<>();
            for (IndigoObject reaction : reactions) {
                String rxnFile = reaction.rxnfile();
                List<Field> fields = extractProperties(reaction);
                result.add(new ReactionRecord(rxnFile, fields));
            }
            
            return result;
            
        } finally {
            tempFile.delete();
        }
    }
}
```

### Parser Service

```java
@ApplicationScoped
public class ReactionParserService {
    
    @Inject
    BlobStorageClient blobStorage;
    
    @Inject
    IndigoReactionAdapter indigo;
    
    public ParsingResult parseFile(UUID fileId, UUID blobId, String bucket) {
        // Download reaction file
        byte[] fileData = blobStorage.downloadBlob(blobId, bucket);
        String extension = detectExtension(blobId, bucket);
        
        // Parse with Indigo
        List<ReactionRecord> reactions = indigo.parseFile(fileData, extension);
        
        // Process reactions (similar to chemical parser)
        // ... upload blobs, extract fields, publish events
        
        return new ParsingResult(recordEvents, fileEvent);
    }
}
```

---

## Breaking Changes & Compatibility

### Message Format
- **Changed**: RabbitMQ → Kafka
- **Maintained**: Command/event structure

### Processing Logic
- **Maintained**: Indigo SDK usage
- **Maintained**: RDF/RXN/CDX format support
- **Maintained**: Field extraction

---

## Testing Requirements

### Unit Tests (>80% coverage)
- Reaction parsing logic
- Field extraction
- Error handling

### Integration Tests
- Kafka command consumption
- Event publishing
- Sample reaction file parsing (RDF, RXN, CDX)

---

## Dependencies

### Needs From
- Agent 3: Blob Storage service
- Agent 8: Kafka infrastructure

### Provides To
- Core API: Parsed reaction records
- Indexing: Reaction data for search

---

## Success Criteria

- [ ] Message contracts defined
- [ ] Command handler implemented
- [ ] Indigo SDK integration working
- [ ] Event publishing working
- [ ] Unit test coverage >80%
- [ ] Integration tests passing
- [ ] Supports RDF, RXN, CDX formats

---

## Timeline

- **Week 1**: Message contracts, Quarkus setup
- **Week 2**: Parser implementation
- **Week 3**: Testing, integration

**Total: 3 weeks**

