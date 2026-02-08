# Phase 2: Chemical Properties Service Migration

## Overview

Migrate the Chemical Properties calculation service from Java 8 / Spring Boot 2.0.3 to Java 21 / Quarkus 3.x, maintaining message contract compatibility.

## Current State Analysis

### Legacy Service
- **Location**: `chemical-properties-service/`
- **Stack**: Java 8, Spring Boot 2.0.3.RELEASE
- **Main Class**: `com.sds.chemicalproperties.Application`
- **Chemistry Library**: Indigo SDK + Indigo InChI

### Message Contracts

#### Command: `CalculateChemicalProperties`
```java
public class CalculateChemicalProperties {
    private UUID id;              // Record ID
    private UUID blobId;          // Blob storage ID
    private String bucket;        // Storage bucket
    private UUID userId;
    private UUID correlationId;
}
```

#### Event: `ChemicalPropertiesCalculated`
```java
public class ChemicalPropertiesCalculated {
    private UUID id;
    private UUID userId;
    private String timeStamp;
    private CalculatedProperties result;
    private UUID correlationId;
}
```

#### CalculatedProperties
```java
public class CalculatedProperties {
    private List<Issue> issues;      // Validation issues
    private List<Property> properties; // Calculated properties
}
```

#### Property
```java
public class Property {
    private String name;        // Property name
    private String value;       // Property value (string)
    private double severity;    // Issue severity (0.0 = no issue)
}
```

### Calculated Properties

The service calculates the following molecular properties:

1. **SMILES** - Canonical SMILES string
2. **MOLECULAR_FORMULA** - Gross molecular formula (e.g., "C6H6")
3. **MOLECULAR_WEIGHT** - Molecular weight (double)
4. **MONOISOTOPIC_MASS** - Monoisotopic mass (double)
5. **MOST_ABUNDANT_MASS** - Most abundant mass (double)
6. **InChI** - InChI identifier string
7. **InChIKey** - InChI key (27 characters)

### Processing Logic

1. Receive `CalculateChemicalProperties` command
2. Download blob (MOL file) from storage
3. Load molecule into Indigo
4. Calculate each property using Indigo/InChI APIs
5. Publish `ChemicalPropertiesCalculated` event with results
6. On error: Publish `ChemicalPropertiesCalculationFailed` event

### Dependencies

- **Indigo SDK**: `com.epam.indigo:indigo:1.3.0beta.r16`
- **Indigo InChI**: `com.epam.indigo:indigo-inchi:1.3.0beta.r16`
- **Storage**: `com.github.arqisoft:storage:0.16`
- **Messaging**: `com.github.arqisoft:messaging:1.1`

---

## Target Architecture

### Quarkus Service Structure

```
services/chemical-properties/
├── src/main/java/io/leanda/ng/chemicalproperties/
│   ├── domain/
│   │   ├── commands/
│   │   │   └── CalculateChemicalPropertiesCommand.java
│   │   ├── events/
│   │   │   ├── ChemicalPropertiesCalculatedEvent.java
│   │   │   └── ChemicalPropertiesCalculationFailedEvent.java
│   │   └── models/
│   │       ├── Property.java
│   │       └── CalculatedProperties.java
│   ├── application/
│   │   ├── ChemicalPropertiesService.java
│   │   └── IndigoPropertiesCalculator.java
│   ├── infrastructure/
│   │   ├── CalculatePropertiesCommandHandler.java
│   │   └── EventPublisher.java
│   └── config/
│       └── ChemicalPropertiesConfig.java
└── pom.xml
```

### Technology Stack

- **Framework**: Quarkus 3.17+
- **Java**: 21 LTS
- **Chemistry**: Indigo SDK + Indigo InChI
- **Messaging**: SmallRye Reactive Messaging (Kafka)

---

## Migration Strategy

### Phase 1: Message Contract Definition

1. **Create AsyncAPI Specification**
   - Define `CalculateChemicalProperties` command
   - Define success/failure events
   - Location: `shared/contracts/events/chemical-properties-events.yaml`

### Phase 2: Service Implementation

1. **Create Quarkus Project** with Kafka extensions
2. **Implement Command Handler** - Consume from `chemical-properties-commands`
3. **Implement Properties Calculator** - Wrap Indigo SDK calls
4. **Implement Event Publishing** - Publish to `chemical-properties-calculated`

### Phase 3: Testing

1. **Unit Tests** - Test each property calculation
2. **Integration Tests** - Test with Kafka and sample molecules

---

## Implementation Details

### Properties Calculator

```java
@ApplicationScoped
public class IndigoPropertiesCalculator {
    
    private Indigo indigo;
    private IndigoInchi indigoInchi;
    
    @PostConstruct
    void init() {
        indigo = new Indigo();
        indigo.setOption("ignore-stereochemistry-errors", "true");
        indigo.setOption("unique-dearomatization", "false");
        indigo.setOption("ignore-noncritical-query-features", "true");
        indigo.setOption("timeout", "600000");
        indigoInchi = new IndigoInchi(indigo);
    }
    
    public CalculatedProperties calculateProperties(String molFile) {
        List<Property> properties = new ArrayList<>();
        
        try {
            IndigoObject molecule = indigo.loadMolecule(molFile);
            String inchiString = indigoInchi.getInchi(molecule);
            
            // Calculate each property
            addProperty(properties, "SMILES", molecule.canonicalSmiles());
            addProperty(properties, "MOLECULAR_FORMULA", molecule.grossFormula());
            addProperty(properties, "MOLECULAR_WEIGHT", String.valueOf(molecule.molecularWeight()));
            addProperty(properties, "MONOISOTOPIC_MASS", String.valueOf(molecule.monoisotopicMass()));
            addProperty(properties, "MOST_ABUNDANT_MASS", String.valueOf(molecule.mostAbundantMass()));
            addProperty(properties, "InChI", inchiString);
            addProperty(properties, "InChIKey", indigoInchi.getInchiKey(inchiString));
            
        } catch (Exception e) {
            // Handle calculation errors
            throw new PropertyCalculationException("Failed to calculate properties", e);
        }
        
        return new CalculatedProperties(new ArrayList<>(), properties);
    }
    
    private void addProperty(List<Property> properties, String name, String value) {
        try {
            properties.add(new Property(name, value, 0.0));
        } catch (Exception e) {
            // Log error but continue with other properties
            LOGGER.error("Failed to calculate {}: {}", name, e.getMessage());
        }
    }
}
```

---

## Breaking Changes & Compatibility

### Message Format
- **Changed**: RabbitMQ → Kafka
- **Maintained**: Command/event structure

### Property Calculation
- **Maintained**: All 7 properties calculated
- **Maintained**: Indigo SDK usage
- **Maintained**: Error handling per property

---

## Testing Requirements

### Unit Tests (>80% coverage)
- Each property calculation method
- Error handling
- InChI/InChIKey generation

### Integration Tests
- Kafka command consumption
- Event publishing
- Sample molecule calculations

---

## Dependencies

### Needs From
- Agent 3: Blob Storage service
- Agent 1: Chemical Parser (for parsed molecules)
- Agent 8: Kafka infrastructure

### Provides To
- Core API: Chemical properties for display
- Indexing: Properties for search

---

## Success Criteria

- [ ] All 7 properties calculated correctly
- [ ] Message contracts defined (AsyncAPI)
- [ ] Command handler implemented
- [ ] Event publishing working
- [ ] Unit test coverage >80%
- [ ] Integration tests passing

---

## Timeline

- **Week 1**: Message contracts, Quarkus setup
- **Week 2**: Implementation, testing
- **Week 3**: Integration, documentation

**Total: 3 weeks**

