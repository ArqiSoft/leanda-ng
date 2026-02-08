# Phase 2: Office File Processor Service Migration

## Overview

Migrate the Office File Processor service from Java 8 / Spring Boot to Java 21 / Quarkus 3.x. This service converts Office documents to PDF and extracts metadata.

## Current State Analysis

### Legacy Service
- **Location**: `office-file-processor-service/`
- **Stack**: Java 8, Spring Boot
- **Port**: 8987 (via common-file-processor bundle)
- **Purpose**: Convert Office documents to PDF and extract metadata

### Supported File Formats

1. **Word Documents**: DOC, DOCX
2. **Spreadsheets**: XLS, XLSX, ODS
3. **Presentations**: PPT, PPTX, ODT

### Message Contracts

#### Command: `ConvertToPdf`
```java
public class ConvertToPdf {
    private UUID id;              // File ID
    private UUID blobId;          // Source blob ID
    private String bucket;        // Storage bucket
    private UUID userId;
    private UUID correlationId;
}
```

#### Event: `ConvertedToPdf`
```java
public class ConvertedToPdf {
    private UUID id;
    private UUID blobId;         // Generated PDF blob ID
    private String bucket;
    private UUID userId;
    private String timeStamp;
    private UUID correlationId;
}
```

#### Command: `ExtractMeta`
```java
public class ExtractMeta {
    private UUID id;
    private UUID blobId;
    private String bucket;
    private UUID userId;
    private UUID correlationId;
}
```

#### Event: `MetaExtracted`
```java
public class MetaExtracted {
    private UUID id;
    private UUID userId;
    private String timeStamp;
    private List<Property> properties;  // Extracted metadata
    private UUID correlationId;
}
```

### Processing Logic

#### PDF Conversion
1. Receive `ConvertToPdf` command
2. Download Office file from blob storage
3. Detect format (DOC, DOCX, XLS, XLSX, PPT, PPTX, ODT)
4. Convert to PDF using appropriate converter:
   - `DocToPdf`, `DocxToPdf` - Word documents
   - `XlsToPdf`, `XlsxToPdf`, `OdsToPdf` - Spreadsheets
   - `PptToPdf`, `PptxToPdf` - Presentations
   - `OdtToPdf` - OpenDocument text
5. Upload PDF to blob storage
6. Publish `ConvertedToPdf` event

#### Metadata Extraction
1. Receive `ExtractMeta` command
2. Download Office file
3. Extract metadata using:
   - `DocMetaExtractor` - Word documents
   - `ExcelMetaExtractor` - Spreadsheets
   - `PresentationMetaExtractor` - Presentations
4. Publish `MetaExtracted` event with properties

### Dependencies

- **Apache POI**: For Office document processing
- **LibreOffice**: For ODT/ODS conversion (via JODConverter)
- **Storage**: Blob storage interface
- **Messaging**: RabbitMQ via jtransit-light

---

## Target Architecture

### Quarkus Service Structure

```
services/office-processor/
├── src/main/java/io/leanda/ng/officeprocessor/
│   ├── domain/
│   │   ├── commands/
│   │   │   ├── ConvertToPdfCommand.java
│   │   │   └── ExtractMetaCommand.java
│   │   ├── events/
│   │   │   ├── ConvertedToPdfEvent.java
│   │   │   ├── MetaExtractedEvent.java
│   │   │   └── ConversionFailedEvent.java
│   │   └── models/
│   │       └── Property.java
│   ├── application/
│   │   ├── OfficeConversionService.java
│   │   ├── MetadataExtractionService.java
│   │   └── converters/
│   │       ├── PdfConverter.java
│   │       ├── WordConverter.java
│   │       ├── ExcelConverter.java
│   │       └── PresentationConverter.java
│   ├── infrastructure/
│   │   ├── ConvertToPdfCommandHandler.java
│   │   ├── ExtractMetaCommandHandler.java
│   │   └── EventPublisher.java
│   └── config/
└── pom.xml
```

### Technology Stack

- **Framework**: Quarkus 3.17+
- **Java**: 21 LTS
- **Office Processing**: Apache POI 5.x
- **PDF Generation**: Apache PDFBox 3.x
- **LibreOffice**: JODConverter (for ODT/ODS)
- **Messaging**: SmallRye Reactive Messaging (Kafka)

---

## Migration Strategy

### Phase 1: Port Converters

1. **Port converter classes**:
   - `DocToPdf`, `DocxToPdf`
   - `XlsToPdf`, `XlsxToPdf`, `OdsToPdf`
   - `PptToPdf`, `PptxToPdf`
   - `OdtToPdf`

2. **Port metadata extractors**:
   - `DocMetaExtractor`
   - `ExcelMetaExtractor`
   - `PresentationMetaExtractor`

3. **Update dependencies**:
   - Apache POI 3.x → 5.x
   - PDFBox 2.x → 3.x

### Phase 2: Service Implementation

1. **Create Quarkus project**
2. **Implement command handlers**:
   - `ConvertToPdfCommandHandler` - Consume from `office-convert-commands`
   - `ExtractMetaCommandHandler` - Consume from `office-extract-meta-commands`
3. **Implement conversion/extraction services**
4. **Implement event publishing**

### Phase 3: Testing

1. **Unit tests** - Each converter and extractor
2. **Integration tests** - End-to-end conversion and extraction

---

## Implementation Details

### PDF Converter

```java
@ApplicationScoped
public class OfficeConversionService {
    
    @Inject
    BlobStorageClient blobStorage;
    
    @Inject
    PdfConverterFactory converterFactory;
    
    public ConversionResult convertToPdf(UUID fileId, UUID blobId, String bucket) {
        // Download Office file
        byte[] fileData = blobStorage.downloadBlob(blobId, bucket);
        BlobInfo blobInfo = blobStorage.getBlobInfo(blobId, bucket);
        
        // Get converter
        String extension = getExtension(blobInfo.getFileName());
        PdfConverter converter = converterFactory.getConverter(extension);
        
        // Convert to PDF
        InputStream pdfStream = converter.convert(new ByteArrayInputStream(fileData));
        
        // Upload PDF
        UUID pdfBlobId = blobStorage.uploadBlob(
            bucket,
            pdfStream,
            "application/pdf"
        );
        
        return new ConversionResult(pdfBlobId, bucket);
    }
}
```

### Metadata Extractor

```java
@ApplicationScoped
public class MetadataExtractionService {
    
    @Inject
    BlobStorageClient blobStorage;
    
    @Inject
    MetadataExtractorFactory extractorFactory;
    
    public ExtractionResult extractMetadata(UUID fileId, UUID blobId, String bucket) {
        // Download Office file
        byte[] fileData = blobStorage.downloadBlob(blobId, bucket);
        BlobInfo blobInfo = blobStorage.getBlobInfo(blobId, bucket);
        
        // Get extractor
        String extension = getExtension(blobInfo.getFileName());
        MetadataExtractor extractor = extractorFactory.getExtractor(extension);
        
        // Extract metadata
        List<Property> properties = extractor.extract(new ByteArrayInputStream(fileData));
        
        return new ExtractionResult(properties);
    }
}
```

---

## Breaking Changes & Compatibility

### Message Format
- **Changed**: RabbitMQ → Kafka
- **Maintained**: Command/event structure

### Converters
- **Maintained**: All Office format support
- **Updated**: Apache POI to 5.x
- **Improved**: Error handling

---

## Testing Requirements

### Unit Tests (>80% coverage)
- Each converter implementation
- Each metadata extractor
- Error handling

### Integration Tests
- Kafka command consumption
- Event publishing
- Sample file conversion/extraction

---

## Dependencies

### Needs From
- Agent 3: Blob Storage service
- Agent 8: Kafka infrastructure

### Provides To
- Core API: PDF versions of Office files
- Indexing: Extracted metadata for search

---

## Success Criteria

- [ ] All converters ported to Java 21
- [ ] All metadata extractors ported
- [ ] Message contracts defined
- [ ] Command handlers implemented
- [ ] Event publishing working
- [ ] Unit test coverage >80%
- [ ] Integration tests passing

---

## Timeline

- **Week 1**: Converter/extractor port, message contracts
- **Week 2**: Service implementation
- **Week 3**: Testing, integration

**Total: 3 weeks**

