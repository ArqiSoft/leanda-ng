# Phase 2: Metadata Processing Service Migration

## Overview

Migrate the Metadata Processing Service from .NET Core 2.1 to Java 21 / Quarkus 3.x, maintaining metadata generation functionality.

## Current State Analysis

### Legacy Service
- **Location**: `metadata-processing-service/Sds.MetadataStorage.Processing/`
- **Stack**: .NET Core 2.1
- **Port**: 11050
- **Purpose**: Generate metadata infoboxes and entity metadata from parsed file fields

### Message Contracts

#### Command: `GenerateMetadata`
```csharp
public class GenerateMetadata {
    public Guid FileId { get; set; }
}
```

#### Event: `MetadataGenerated`
```csharp
public class MetadataGenerated {
    public Guid Id { get; set; }  // FileId
}
```

### Processing Logic

1. **Receive `GenerateMetadata` command** from RabbitMQ
2. **Fetch file fields** from MongoDB Files collection
3. **For each field**:
   - Query Records collection to get all values for the field
   - Use `TypeQualifier` to determine data type (string, number, date, etc.)
   - Calculate min/max values (for numeric fields)
   - Build infobox screen parts
4. **Generate infobox metadata**:
   - Title: "Fields"
   - InfoBoxType: "fields"
   - Screen parts with field definitions
5. **Generate entity metadata**:
   - Field definitions with data types
   - Min/max values (for numeric fields)
6. **Store metadata** in MongoDB Metadata collection
7. **Publish `MetadataGenerated` event**

### Type Qualifier

The `TypeQualifier` class analyzes field values to determine:
- **DataType**: string, number, date, boolean
- **MinValue**: Minimum value (for numeric)
- **MaxValue**: Maximum value (for numeric)

### Dependencies

- **MongoDB**: For file/record data and metadata storage
- **MassTransit**: Event consumption
- **Custom**: TypeQualifier logic

---

## Target Architecture

### Quarkus Service Structure

```
services/metadata-processing/
├── src/main/java/io/leanda/ng/metadataprocessing/
│   ├── domain/
│   │   ├── commands/
│   │   │   └── GenerateMetadataCommand.java
│   │   ├── events/
│   │   │   └── MetadataGeneratedEvent.java
│   │   └── models/
│   │       ├── InfoboxMetadata.java
│   │       ├── EntityMetadata.java
│   │       └── FieldDefinition.java
│   ├── application/
│   │   ├── MetadataGenerationService.java
│   │   └── TypeQualifier.java
│   ├── infrastructure/
│   │   ├── GenerateMetadataCommandHandler.java
│   │   ├── MongoMetadataRepository.java
│   │   └── EventPublisher.java
│   └── config/
└── pom.xml
```

### Technology Stack

- **Framework**: Quarkus 3.17+
- **Java**: 21 LTS
- **Database**: MongoDB (via Quarkus MongoDB client)
- **Messaging**: SmallRye Reactive Messaging (Kafka)

---

## Migration Strategy

### Phase 1: Port Type Qualifier

1. **Port TypeQualifier logic** to Java
2. **Implement data type detection**:
   - String detection
   - Number detection (integer, decimal)
   - Date detection
   - Boolean detection
3. **Implement min/max calculation** for numeric fields

### Phase 2: Service Implementation

1. **Create Quarkus project**
2. **Implement command handler** - Consume from `metadata-generate-commands`
3. **Implement metadata generation service**
4. **Implement MongoDB repository**
5. **Implement event publishing**

### Phase 3: Testing

1. **Unit tests** - Type qualifier, metadata generation
2. **Integration tests** - End-to-end metadata generation

---

## Implementation Details

### Type Qualifier

```java
@ApplicationScoped
public class TypeQualifier {
    
    private String dataType = "string";
    private Double minValue = null;
    private Double maxValue = null;
    
    public void qualify(String value) {
        if (value == null || value.isEmpty()) {
            return;
        }
        
        // Try to parse as number
        try {
            double numValue = Double.parseDouble(value);
            if (dataType.equals("string")) {
                dataType = "number";
                minValue = numValue;
                maxValue = numValue;
            } else if (dataType.equals("number")) {
                minValue = Math.min(minValue, numValue);
                maxValue = Math.max(maxValue, numValue);
            }
        } catch (NumberFormatException e) {
            // Not a number, keep as string
        }
        
        // Try to parse as date
        if (isDate(value)) {
            dataType = "date";
        }
        
        // Try to parse as boolean
        if (isBoolean(value)) {
            dataType = "boolean";
        }
    }
    
    public String getDataType() {
        return dataType;
    }
    
    public Double getMinValue() {
        return minValue;
    }
    
    public Double getMaxValue() {
        return maxValue;
    }
}
```

### Metadata Generation Service

```java
@ApplicationScoped
public class MetadataGenerationService {
    
    @Inject
    MongoClient mongoClient;
    
    @Inject
    TypeQualifier typeQualifier;
    
    public MetadataResult generateMetadata(UUID fileId) {
        // Fetch file fields from MongoDB
        List<String> fieldNames = fetchFileFields(fileId);
        
        // Build infobox metadata
        InfoboxMetadata infobox = new InfoboxMetadata();
        infobox.setFileId(fileId);
        infobox.setTitle("Fields");
        infobox.setInfoBoxType("fields");
        
        // Build entity metadata
        EntityMetadata entityMetadata = new EntityMetadata();
        entityMetadata.setId(fileId);
        List<FieldDefinition> fieldDefinitions = new ArrayList<>();
        
        // Process each field
        for (String fieldName : fieldNames) {
            typeQualifier.reset();
            
            // Query all record values for this field
            List<String> values = queryFieldValues(fileId, fieldName);
            for (String value : values) {
                typeQualifier.qualify(value);
            }
            
            // Build screen part
            ScreenPart screenPart = new ScreenPart();
            screenPart.setTitle(fieldName);
            screenPart.setResponseType("text-response");
            screenPart.setDataType(typeQualifier.getDataType());
            screenPart.setResponseTarget("Properties.Fields[@Name='" + fieldName + "'].Value");
            infobox.addScreenPart(screenPart);
            
            // Build field definition
            FieldDefinition fieldDef = new FieldDefinition();
            fieldDef.setName(fieldName);
            fieldDef.setDataType(typeQualifier.getDataType());
            if (typeQualifier.getMinValue() != null) {
                fieldDef.setMinValue(typeQualifier.getMinValue());
                fieldDef.setMaxValue(typeQualifier.getMaxValue());
            }
            fieldDefinitions.add(fieldDef);
        }
        
        entityMetadata.setFields(fieldDefinitions);
        
        return new MetadataResult(infobox, entityMetadata);
    }
}
```

---

## Breaking Changes & Compatibility

### Message Format
- **Changed**: MassTransit / RabbitMQ → Kafka
- **Maintained**: Command/event structure

### Metadata Structure
- **Maintained**: Infobox metadata format
- **Maintained**: Entity metadata format
- **Maintained**: MongoDB storage structure

---

## Testing Requirements

### Unit Tests (>80% coverage)
- Type qualifier logic
- Metadata generation
- Field value aggregation

### Integration Tests
- Kafka command consumption
- MongoDB queries
- Event publishing

---

## Dependencies

### Needs From
- Agent 4: MongoDB access
- Agent 8: Kafka infrastructure

### Provides To
- Core API: Metadata for infoboxes
- Frontend: Field definitions for forms

---

## Success Criteria

- [ ] Type qualifier ported to Java
- [ ] Message contracts defined
- [ ] Command handler implemented
- [ ] Metadata generation working
- [ ] Unit test coverage >80%
- [ ] Integration tests passing

---

## Timeline

- **Week 1**: Type qualifier port, message contracts
- **Week 2**: Service implementation
- **Week 3**: Testing, integration

**Total: 3 weeks**

