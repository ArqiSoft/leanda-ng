# Phase 2: Blob Storage Service Migration

## Overview

Migrate the Blob Storage API service from .NET Core 3.1 to Java 21 / Quarkus 3.x, maintaining full API compatibility while modernizing the implementation.

## Current State Analysis

### Legacy Service
- **Location**: `leanda-services/Source/Services/BlobStorage/Sds.Storage.Blob.WebApi/`
- **Stack**: .NET Core 3.1, ASP.NET Core MVC
- **Port**: 18006
- **Storage Backend**: MongoDB GridFS (via `Sds.Storage.Blob.GridFS`)
- **Messaging**: MassTransit / RabbitMQ

### API Endpoints

#### GET `/api/blobs/{bucket}/{id}`
- **Purpose**: Download blob by ID
- **Query Parameters**: `content-disposition` (inline|attachment)
- **Response**: Binary file stream with Content-Disposition header
- **Status Codes**: 200 OK, 404 Not Found

#### POST `/api/blobs/{bucket}`
- **Purpose**: Upload blob(s) via multipart/form-data
- **Request**: Multipart form with file(s)
- **Response**: Array of uploaded blob IDs (Guid[])
- **Events Published**: `BlobLoaded` event per uploaded file
- **Status Codes**: 200 OK

#### DELETE `/api/blobs/{bucket}/{id}`
- **Purpose**: Delete blob by ID
- **Response**: 204 No Content or 404 Not Found
- **Status Codes**: 204 No Content, 404 Not Found

#### GET `/api/blobs/{bucket}/{id}/info`
- **Purpose**: Get blob metadata
- **Response**: BlobInfo object (JSON)
- **Status Codes**: 200 OK, 404 Not Found

#### GET `/api/version`
- **Purpose**: Get API version
- **Response**: VersionInfo object

### Domain Models

#### BlobInfo
```csharp
public class BlobInfo
{
    public Guid Id { get; set; }
    public string FileName { get; set; }
    public string ContentType { get; set; }
    public long Length { get; set; }
    public string MD5 { get; set; }
    public DateTimeOffset UploadDateTime { get; set; }
    public Dictionary<string, object> Metadata { get; set; }
}
```

#### LoadedBlobInfo (Event)
```csharp
public class LoadedBlobInfo
{
    public Guid Id { get; set; }
    public string FileName { get; set; }
    public long Length { get; set; }
    public Guid UserId { get; set; }
    public DateTimeOffset UploadDateTime { get; set; }
    public string MD5 { get; set; }
    public string Bucket { get; set; }
    public Dictionary<string, object> Metadata { get; set; }
}
```

### Dependencies

- **Storage Interface**: `IBlobStorage` (GridFS implementation)
- **Messaging**: MassTransit `IBusControl` for publishing `BlobLoaded` events
- **Authentication**: OIDC (Keycloak) via `[Authorize]` attribute
- **File Upload**: Custom `DisableFormValueModelBindingAttribute` for streaming uploads

---

## Target Architecture

### Quarkus Service Structure

```
services/blob-storage/
├── src/main/java/io/leanda/ng/blobstorage/
│   ├── api/
│   │   ├── BlobsResource.java          # REST endpoints
│   │   └── VersionResource.java
│   ├── domain/
│   │   ├── BlobInfo.java               # Domain model
│   │   └── BlobMetadata.java
│   ├── application/
│   │   ├── BlobService.java             # Business logic
│   │   └── BlobEventPublisher.java     # Event publishing
│   ├── infrastructure/
│   │   ├── GridFsBlobStorage.java      # MongoDB GridFS adapter
│   │   └── S3BlobStorage.java          # Future: S3 adapter
│   └── config/
│       └── BlobStorageConfig.java
├── src/test/java/
│   ├── BlobsResourceTest.java
│   └── BlobServiceTest.java
└── pom.xml
```

### Technology Stack

- **Framework**: Quarkus 3.17+
- **Java**: 21 LTS
- **Storage**: MongoDB GridFS (via Quarkus MongoDB client)
- **Messaging**: SmallRye Reactive Messaging (Kafka)
- **Validation**: Hibernate Validator
- **OpenAPI**: Quarkus OpenAPI extension
- **Testing**: REST Assured, Testcontainers

---

## Migration Strategy

### Phase 1: API Contract Definition

1. **Create OpenAPI 3.1 Specification**
   - Document all endpoints with request/response schemas
   - Define error responses (404, 400, 500)
   - Include authentication requirements
   - Location: `shared/contracts/blob-storage-api.yaml`

2. **Define Event Schemas**
   - `BlobLoaded` event (AsyncAPI)
   - Location: `shared/contracts/events/blob-events.yaml`

### Phase 2: Service Implementation

1. **Create Quarkus Project**
   ```bash
   mvn io.quarkus.platform:quarkus-maven-plugin:3.17.0:create \
     -DprojectGroupId=io.leanda.ng \
     -DprojectArtifactId=blob-storage \
     -DclassName="io.leanda.ng.blobstorage.BlobsResource" \
     -Dpath="/api/blobs"
   ```

2. **Implement REST Endpoints**
   - `GET /api/blobs/{bucket}/{id}` - Download with streaming
   - `POST /api/blobs/{bucket}` - Multipart upload
   - `DELETE /api/blobs/{bucket}/{id}` - Delete
   - `GET /api/blobs/{bucket}/{id}/info` - Metadata
   - `GET /api/version` - Version info

3. **Implement Storage Adapter**
   - MongoDB GridFS adapter (maintain compatibility)
   - Future: S3 adapter for AWS migration

4. **Implement Event Publishing**
   - Publish `BlobLoaded` events to Kafka topic `blob-loaded`

### Phase 3: Testing & Integration

1. **Unit Tests**
   - Test blob upload/download/delete operations
   - Test metadata retrieval
   - Test error handling

2. **Integration Tests**
   - Test with MongoDB Testcontainer
   - Test with Kafka Testcontainer (Redpanda)
   - Test multipart upload with large files

3. **API Contract Tests**
   - Verify OpenAPI spec compliance
   - Test backward compatibility

---

## Implementation Details

### REST Endpoint Implementation

#### Download Blob
```java
@GET
@Path("/{bucket}/{id}")
@Produces(MediaType.APPLICATION_OCTET_STREAM)
public Response downloadBlob(
    @PathParam("bucket") String bucket,
    @PathParam("id") UUID id,
    @QueryParam("content-disposition") @DefaultValue("inline") String contentDisposition
) {
    BlobInfo blobInfo = blobService.getBlobInfo(id, bucket);
    if (blobInfo == null) {
        return Response.status(404).build();
    }
    
    StreamingOutput stream = output -> {
        blobService.downloadBlob(id, bucket, output);
    };
    
    return Response.ok(stream)
        .header("Content-Disposition", 
            String.format("%s; filename=\"%s\"", contentDisposition, blobInfo.getFileName()))
        .header("Content-Type", blobInfo.getContentType())
        .build();
}
```

#### Upload Blob
```java
@POST
@Path("/{bucket}")
@Consumes(MediaType.MULTIPART_FORM_DATA)
public Response uploadBlob(
    @PathParam("bucket") String bucket,
    @FormParam("file") InputStream fileStream,
    @FormParam("fileName") String fileName,
    @FormParam("contentType") String contentType
) {
    UUID blobId = blobService.uploadBlob(bucket, fileName, fileStream, contentType);
    
    BlobInfo blobInfo = blobService.getBlobInfo(blobId, bucket);
    
    // Publish event
    eventPublisher.publishBlobLoaded(blobId, blobInfo, bucket);
    
    return Response.ok(List.of(blobId)).build();
}
```

### Storage Adapter (GridFS)

```java
@ApplicationScoped
public class GridFsBlobStorage implements BlobStorage {
    
    @Inject
    MongoClient mongoClient;
    
    private GridFSBucket getBucket(String bucketName) {
        MongoDatabase database = mongoClient.getDatabase("leanda");
        return GridFSBuckets.create(database, bucketName);
    }
    
    @Override
    public UUID uploadBlob(String bucket, String fileName, InputStream stream, String contentType) {
        GridFSBucket gridFS = getBucket(bucket);
        ObjectId fileId = gridFS.uploadFromStream(fileName, stream);
        return UUID.fromString(fileId.toString());
    }
    
    @Override
    public void downloadBlob(UUID id, String bucket, OutputStream output) {
        GridFSBucket gridFS = getBucket(bucket);
        gridFS.downloadToStream(new ObjectId(id.toString()), output);
    }
}
```

### Event Publishing

```java
@ApplicationScoped
public class BlobEventPublisher {
    
    @Channel("blob-loaded")
    Emitter<BlobLoadedEvent> blobLoadedEmitter;
    
    public void publishBlobLoaded(UUID blobId, BlobInfo blobInfo, String bucket) {
        BlobLoadedEvent event = BlobLoadedEvent.builder()
            .blobId(blobId)
            .fileName(blobInfo.getFileName())
            .length(blobInfo.getLength())
            .userId(getCurrentUserId())
            .uploadDateTime(blobInfo.getUploadDateTime())
            .md5(blobInfo.getMd5())
            .bucket(bucket)
            .metadata(blobInfo.getMetadata())
            .timestamp(Instant.now())
            .build();
            
        blobLoadedEmitter.send(event);
    }
}
```

---

## Breaking Changes & Compatibility

### API Compatibility
- **Maintained**: All endpoint paths and query parameters
- **Maintained**: Response formats (binary streams, JSON)
- **Maintained**: Status codes
- **Changed**: Event format (MassTransit → Kafka Avro/JSON Schema)

### Storage Compatibility
- **Maintained**: MongoDB GridFS bucket structure
- **Maintained**: Blob ID format (UUID)
- **Maintained**: Metadata structure

### Migration Path
1. Deploy Quarkus service alongside .NET service
2. Route traffic gradually (10% → 50% → 100%)
3. Monitor for errors
4. Decommission .NET service after full migration

---

## Testing Requirements

### Unit Tests (>80% coverage)
- BlobService upload/download/delete operations
- BlobInfo domain model validation
- Event publishing logic

### Integration Tests
- MongoDB GridFS operations with Testcontainers
- Kafka event publishing with Redpanda Testcontainer
- Multipart file upload handling
- Authentication/authorization

### Performance Tests
- Large file upload (100MB+)
- Concurrent uploads (10+ simultaneous)
- Download throughput

---

## Dependencies

### Needs From
- Agent 8: Docker setup with MongoDB and Kafka
- Agent 4: Authentication/authorization framework
- Agent 7: Test infrastructure

### Provides To
- All parsers: Blob storage interface
- Core API: Blob download endpoints
- Frontend: Blob upload/download URLs

---

## Success Criteria

- [ ] All REST endpoints implemented and tested
- [ ] OpenAPI 3.1 specification complete
- [ ] MongoDB GridFS storage working
- [ ] Kafka event publishing working
- [ ] Unit test coverage >80%
- [ ] Integration tests passing
- [ ] API backward compatibility verified
- [ ] Performance meets or exceeds .NET version

---

## Timeline

- **Week 1**: API contract definition, Quarkus project setup
- **Week 2**: REST endpoints implementation, storage adapter
- **Week 3**: Event publishing, testing, documentation

**Total: 3 weeks**

