# Phase 2: Imaging Service Migration

## Overview

Migrate the Imaging Service from Java 8 / Spring Boot to Java 21 / Quarkus 3.x. This service generates thumbnail images from various scientific file formats.

## Current State Analysis

### Legacy Service
- **Location**: `imaging-service/`
- **Stack**: Java 8, Spring Boot
- **Port**: 8986 (via common-file-processor bundle)
- **Purpose**: Generate thumbnail images from scientific files

### Supported File Formats

The service supports rasterization (image generation) for:

1. **Chemical Structures**: MOL, CDX (via `StructureRasterizer` + Indigo)
2. **Crystals**: CIF (via `CifRasterizer`)
3. **Reactions**: RXN (via `ReactionRasterizer` + Indigo)
4. **Office Documents**: DOC, DOCX, XLS, XLSX, PPT, PPTX, ODS, ODT (via `OfficeRasterizer`)
5. **PDF**: PDF (via `PdfRasterizer`)
6. **Images**: JPG, JPEG, PNG, BMP, GIF, SVG, ICO (via `ImageRasterizer`)
7. **Microscopy**: CZI, LIF, IMS (Zeiss BioFormat), LSM, ND2 (Nikon), TIF, TIFF

### Message Contracts

#### Command: `GenerateImage`
```java
public class GenerateImage {
    private UUID id;              // File/Record ID
    private UUID blobId;          // Source blob ID
    private String bucket;        // Storage bucket
    private Image image;          // Image metadata (id, width, height, mimeType)
    private UUID userId;
    private UUID correlationId;
}
```

#### Event: `ImageGenerated`
```java
public class ImageGenerated {
    private UUID id;
    private UUID userId;
    private String timeStamp;
    private Image image;          // Generated image metadata
    private UUID blobId;         // Generated thumbnail blob ID
    private String bucket;
    private UUID correlationId;
}
```

#### Event: `ImageGenerationFailed`
```java
public class ImageGenerationFailed {
    private UUID id;
    private UUID userId;
    private String timeStamp;
    private Image image;          // Image with exception message
    private UUID correlationId;
}
```

### Rasterizer Architecture

The service uses a factory pattern with specialized rasterizers:

- **RasterizationFactory**: Selects appropriate rasterizer by file extension
- **Rasterizer Interface**: `byte[] rasterize(Image image, byte[] fileData, String extension)`
- **Specialized Rasterizers**:
  - `StructureRasterizer` - Chemical structures (Indigo)
  - `CifRasterizer` - Crystal structures
  - `ReactionRasterizer` - Chemical reactions (Indigo)
  - `OfficeRasterizer` - Office documents (Apache POI, LibreOffice)
  - `PdfRasterizer` - PDF files
  - `ImageRasterizer` - Image format conversion/resizing
  - `ZeissBioformatRasterizer` - Microscopy (Bio-Formats library)
  - `LsmRasterizer`, `NikonRasterizer` - Microscopy formats
  - `TiffRasterizer` - TIFF files

### Processing Logic

1. Receive `GenerateImage` command
2. Download source file from blob storage
3. Detect file format by extension
4. Get appropriate rasterizer from factory
5. Generate thumbnail image (byte array)
6. Upload thumbnail to blob storage
7. Publish `ImageGenerated` event
8. On error: Publish `ImageGenerationFailed` event

### Dependencies

- **Indigo SDK**: For chemical structure/reaction rendering
- **Apache POI**: For Office document processing
- **Bio-Formats**: For microscopy file formats
- **ImageIO**: For image format conversion
- **Storage**: Blob storage interface
- **Messaging**: RabbitMQ via jtransit-light

---

## Target Architecture

### Quarkus Service Structure

```
services/imaging/
├── src/main/java/io/leanda/ng/imaging/
│   ├── domain/
│   │   ├── commands/GenerateImageCommand.java
│   │   ├── events/ImageGeneratedEvent.java
│   │   └── models/Image.java
│   ├── application/
│   │   ├── ImagingService.java
│   │   └── RasterizationService.java
│   ├── infrastructure/
│   │   ├── rasterizers/
│   │   │   ├── Rasterizer.java
│   │   │   ├── RasterizationFactory.java
│   │   │   ├── StructureRasterizer.java
│   │   │   ├── CifRasterizer.java
│   │   │   ├── ReactionRasterizer.java
│   │   │   ├── OfficeRasterizer.java
│   │   │   ├── PdfRasterizer.java
│   │   │   ├── ImageRasterizer.java
│   │   │   └── MicroscopyRasterizer.java
│   │   ├── GenerateImageCommandHandler.java
│   │   └── EventPublisher.java
│   └── config/
└── pom.xml
```

### Technology Stack

- **Framework**: Quarkus 3.17+
- **Java**: 21 LTS
- **Chemistry**: Indigo SDK (for structures/reactions)
- **Office**: Apache POI 5.x
- **PDF**: Apache PDFBox 3.x
- **Microscopy**: Bio-Formats library
- **Image Processing**: Java ImageIO, ImageIO-Ext
- **Messaging**: SmallRye Reactive Messaging (Kafka)

---

## Migration Strategy

### Phase 1: Port Rasterizers

1. **Port all rasterizer classes** to Java 21
2. **Update dependencies**:
   - Apache POI 3.x → 5.x
   - PDFBox 2.x → 3.x
   - Bio-Formats (latest version)
3. **Update Indigo integration** (if needed)

### Phase 2: Service Implementation

1. **Create Quarkus project**
2. **Implement command handler** - Consume from `imaging-commands`
3. **Implement rasterization service** - Use factory pattern
4. **Implement event publishing**

### Phase 3: Testing

1. **Unit tests** - Each rasterizer
2. **Integration tests** - End-to-end image generation
3. **Performance tests** - Large file handling

---

## Implementation Details

### Rasterization Factory

```java
@ApplicationScoped
public class RasterizationFactory {
    
    @Inject
    StructureRasterizer structureRasterizer;
    
    @Inject
    CifRasterizer cifRasterizer;
    
    @Inject
    ReactionRasterizer reactionRasterizer;
    
    @Inject
    OfficeRasterizer officeRasterizer;
    
    @Inject
    PdfRasterizer pdfRasterizer;
    
    @Inject
    ImageRasterizer imageRasterizer;
    
    @Inject
    MicroscopyRasterizer microscopyRasterizer;
    
    public Rasterizer getRasterizer(String extension) {
        String ext = extension.toLowerCase();
        
        return switch (ext) {
            case "cif" -> cifRasterizer;
            case "rxn" -> reactionRasterizer;
            case "mol", "cdx" -> structureRasterizer;
            case "pdf" -> pdfRasterizer;
            case "doc", "docx", "xls", "xlsx", "ppt", "pptx", "ods", "odt" -> officeRasterizer;
            case "jpg", "jpeg", "png", "bmp", "gif", "svg", "ico" -> imageRasterizer;
            case "czi", "lif", "ims", "lsm", "nd2", "tif", "tiff" -> microscopyRasterizer;
            default -> throw new UnsupportedFormatException(extension);
        };
    }
}
```

### Imaging Service

```java
@ApplicationScoped
public class ImagingService {
    
    @Inject
    BlobStorageClient blobStorage;
    
    @Inject
    RasterizationFactory rasterizationFactory;
    
    public ImageGenerationResult generateImage(
        UUID fileId,
        UUID blobId,
        String bucket,
        ImageSpec imageSpec
    ) {
        // Download source file
        byte[] fileData = blobStorage.downloadBlob(blobId, bucket);
        BlobInfo blobInfo = blobStorage.getBlobInfo(blobId, bucket);
        
        // Get rasterizer
        String extension = getExtension(blobInfo.getFileName());
        Rasterizer rasterizer = rasterizationFactory.getRasterizer(extension);
        
        // Generate thumbnail
        byte[] thumbnail = rasterizer.rasterize(imageSpec, fileData, extension);
        
        // Upload thumbnail
        UUID thumbnailBlobId = blobStorage.uploadBlob(
            bucket,
            thumbnail,
            imageSpec.getMimeType(),
            Map.of("SourceId", blobId.toString())
        );
        
        return new ImageGenerationResult(
            thumbnailBlobId,
            imageSpec,
            thumbnail.length
        );
    }
}
```

---

## Breaking Changes & Compatibility

### Message Format
- **Changed**: RabbitMQ → Kafka
- **Maintained**: Command/event structure

### Rasterizers
- **Maintained**: All file format support
- **Updated**: Dependencies to latest versions
- **Improved**: Error handling, Java 21 features

---

## Testing Requirements

### Unit Tests (>80% coverage)
- Each rasterizer implementation
- Factory selection logic
- Error handling

### Integration Tests
- Kafka command consumption
- Event publishing
- Sample file rasterization (all formats)

### Performance Tests
- Large file handling (100MB+)
- Concurrent image generation

---

## Dependencies

### Needs From
- Agent 3: Blob Storage service
- Agent 8: Kafka infrastructure

### Provides To
- Core API: Thumbnail images for file preview
- Frontend: Image URLs for display

---

## Success Criteria

- [ ] All rasterizers ported to Java 21
- [ ] Message contracts defined
- [ ] Command handler implemented
- [ ] Event publishing working
- [ ] Unit test coverage >80%
- [ ] Integration tests passing
- [ ] All file formats supported

---

## Timeline

- **Week 1**: Rasterizer port, message contracts
- **Week 2**: Service implementation
- **Week 3**: Testing, integration

**Total: 3 weeks**

