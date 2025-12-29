# API Test Specifications

## Overview

This document defines API test scenarios for the Leanda Core API, derived from the OpenAPI specification at `shared/specs/api/core-api.yaml`.

## Test Categories

### 1. Unit Tests
- Test individual resource methods in isolation
- Mock dependencies (services, repositories)
- Fast execution, high coverage

### 2. Integration Tests  
- Test full request/response cycle
- Use Testcontainers for real infrastructure
- Verify database operations

### 3. Contract Tests
- Validate OpenAPI specification compliance
- Test request/response schemas
- Ensure backwards compatibility

## Nodes API Tests

### GET /api/nodes

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getNodeList_authenticated_returnsNodes` | Authenticated user gets their nodes | 200 OK with paginated nodes |
| `test_getNodeList_withFilter_filtersResults` | Apply $filter parameter | 200 OK with filtered nodes |
| `test_getNodeList_withProjection_limitedFields` | Apply $projection parameter | 200 OK with limited fields |
| `test_getNodeList_pagination_returnsPaginationHeaders` | Request page 2 | 200 OK with X-Pagination header |
| `test_getNodeList_unauthenticated_returns401` | No auth token | 401 Unauthorized |
| `test_getNodeList_invalidFilter_returns400` | Malformed filter | 400 Bad Request |

### GET /api/nodes/{id}

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getNodeById_exists_returnsNode` | Get existing node | 200 OK with node details |
| `test_getNodeById_notFound_returns404` | Get non-existent node | 404 Not Found |
| `test_getNodeById_otherUserNode_returns404` | Get another user's private node | 404 Not Found |
| `test_getNodeById_sharedNode_returnsNode` | Get shared node | 200 OK |
| `test_getNodeById_includeBreadcrumbs` | Verify X-Breadcrumbs header | Header present with path |

### GET /api/nodes/{id}/nodes

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getInnerNodes_returnsChildren` | Get folder children | 200 OK with child nodes |
| `test_getInnerNodes_emptyFolder_returnsEmpty` | Get empty folder | 200 OK with empty list |
| `test_getInnerNodes_filterByType_filtered` | Filter by type=File | 200 OK with files only |

### GET /api/nodes/public

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getPublicNodes_noAuth_returnsNodes` | Anonymous access | 200 OK with public nodes |
| `test_getPublicNodes_empty_returnsEmpty` | No public nodes exist | 200 OK with empty list |

### POST /api/nodes/current

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_setCurrentNode_valid_returnsNode` | Set valid node | 200 OK with node |
| `test_setCurrentNode_notFound_returns404` | Set non-existent node | 404 Not Found |

### GET /api/nodes/{id}.zip

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_downloadZip_folder_returnsZip` | Download folder as ZIP | 200 OK with ZIP content |
| `test_downloadZip_file_returnsZip` | Download file as ZIP | 200 OK with ZIP content |
| `test_downloadZip_empty_returnsEmptyZip` | Download empty folder | 200 OK with empty ZIP |

## Entities API Tests

### GET /api/entities/{type}

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getEntityList_files_returnsFiles` | Get files list | 200 OK with files |
| `test_getEntityList_folders_returnsFolders` | Get folders list | 200 OK with folders |
| `test_getEntityList_records_returnsRecords` | Get records list | 200 OK with records |
| `test_getEntityList_models_returnsModels` | Get models list | 200 OK with models |
| `test_getEntityList_invalidType_returns400` | Invalid type parameter | 400 Bad Request |

### GET /api/entities/{type}/{id}

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getSingleEntity_exists_returnsEntity` | Get existing entity | 200 OK with entity |
| `test_getSingleEntity_notFound_returns404` | Non-existent entity | 404 Not Found |
| `test_getSingleEntity_withProjection_limitedFields` | Limited fields | 200 OK with projection |

### POST /api/entities/folders

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_createFolder_valid_returns202` | Create valid folder | 202 Accepted with Location |
| `test_createFolder_invalidName_returns400` | Invalid folder name | 400 Bad Request |
| `test_createFolder_missingName_returns400` | Missing name | 400 Bad Request |
| `test_createFolder_duplicateName_returns202` | Duplicate name allowed | 202 Accepted |

### PATCH /api/entities/files/{id}

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_patchFile_rename_returns202` | Rename file | 202 Accepted |
| `test_patchFile_move_returns202` | Move file | 202 Accepted |
| `test_patchFile_updateMetadata_returns202` | Update metadata | 202 Accepted |
| `test_patchFile_grantAccess_returns202` | Grant access | 202 Accepted |
| `test_patchFile_notFound_returns404` | Non-existent file | 404 Not Found |
| `test_patchFile_invalidPatch_returns400` | Invalid JSON Patch | 400 Bad Request |

### GET /api/entities/{type}/{id}/blobs/{blobId}

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getBlob_exists_returnsBlob` | Get existing blob | 200 OK with binary |
| `test_getBlob_attachment_contentDisposition` | Download as attachment | Content-Disposition header |
| `test_getBlob_notFound_returns404` | Non-existent blob | 404 Not Found |

### GET /api/entities/{type}/{id}/images/{imageId}

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getImage_exists_returnsImage` | Get existing image | 200 OK with image |
| `test_getImage_notFound_returns404` | Non-existent image | 404 Not Found |

### GET /api/entities/{type}/{id}/metadata

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getMetadata_exists_returnsMetadata` | Get entity metadata | 200 OK with metadata |
| `test_getMetadata_noMetadata_returnsEmpty` | Entity without metadata | 200 OK with empty object |

## Users API Tests

### PUT /api/users/{id}

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_createUser_new_returns202` | Create new user | 202 Accepted |
| `test_updateUser_existing_returns202` | Update existing user | 202 Accepted |
| `test_createUser_invalidEmail_returns400` | Invalid email format | 400 Bad Request |

### GET /api/users/{id}

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getUserById_self_returnsUser` | Get own profile | 200 OK with user |
| `test_getUserById_other_returns403` | Get other's profile | 403 Forbidden |
| `test_getUserById_notFound_returns404` | Non-existent user | 404 Not Found |

### GET /api/me

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getCurrentUser_authenticated_returnsUser` | Get current user | 200 OK with user |
| `test_getCurrentUser_unauthenticated_returns401` | No auth | 401 Unauthorized |

### GET /api/users/{id}/public-info

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getPublicInfo_exists_returnsInfo` | Get public info | 200 OK with limited info |
| `test_getPublicInfo_noAuth_allowed` | Anonymous access | 200 OK |

## Machine Learning API Tests

### POST /api/machinelearning/models

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_createModel_valid_returns202` | Start training | 202 Accepted with IDs |
| `test_createModel_invalidSource_returns400` | Invalid source blob | 400 Bad Request |
| `test_createModel_missingMethod_returns400` | Missing ML method | 400 Bad Request |

### POST /api/machinelearning/predictions

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_createPrediction_valid_returns202` | Create prediction | 202 Accepted |
| `test_createPrediction_invalidModel_returns400` | Invalid model | 400 Bad Request |

### POST /api/machinelearning/predictions/structure

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_predictStructure_mol_returns200` | MOL format | 200 OK with prediction ID |
| `test_predictStructure_smiles_returns200` | SMILES format | 200 OK with prediction ID |
| `test_predictStructure_invalidFormat_returns400` | Invalid format | 400 Bad Request |
| `test_predictStructure_modelNotPublic_returns400` | Non-public model | 400 Bad Request |

### GET /api/machinelearning/predictions/{id}/status

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_getPredictionStatus_calculating_returnsCalculating` | In progress | 200 OK with CALCULATING |
| `test_getPredictionStatus_completed_returnsCompleted` | Completed | 200 OK with COMPLETED |
| `test_getPredictionStatus_notFound_returns404` | Non-existent | 404 Not Found |

## Exports API Tests

### POST /api/exports/files

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_exportFile_sdf_returns202` | Export as SDF | 202 Accepted with Location |
| `test_exportFile_csv_returns202` | Export as CSV | 202 Accepted |
| `test_exportFile_invalidFormat_returns400` | Invalid format | 400 Bad Request |
| `test_exportFile_withMapping_returns202` | With property mapping | 202 Accepted |

## Health API Tests

### GET /health

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_health_allUp_returns200` | All checks pass | 200 OK with UP status |
| `test_health_dbDown_returns503` | DB check fails | 503 with DOWN status |

### GET /ready

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_ready_ready_returns200` | Service ready | 200 OK |
| `test_ready_notReady_returns503` | Service not ready | 503 Service Unavailable |

## Test Data Requirements

### Users
- `testUser1`: Standard authenticated user
- `testUser2`: Second user for access control tests
- `adminUser`: Admin user for privileged operations

### Folders
- `rootFolder`: User's root folder
- `childFolder`: Subfolder for hierarchy tests
- `sharedFolder`: Publicly shared folder
- `emptyFolder`: Empty folder for edge cases

### Files
- `chemicalFile`: SDF file with 10 records
- `pdfFile`: PDF document
- `imageFile`: PNG image
- `processedFile`: Fully processed file
- `failedFile`: File that failed processing

### Records
- `chemicalRecord`: Chemical structure record
- `crystalRecord`: Crystal structure record

### Models
- `publicModel`: Public ML model for predictions
- `privateModel`: Private ML model
- `trainingModel`: Model in training state

## Test Utilities

```java
public class TestDataFixtures {
    
    public static User createTestUser() {
        return User.builder()
            .id(UUID.randomUUID())
            .displayName("Test User")
            .email("test@example.com")
            .loginName("testuser")
            .build();
    }
    
    public static Folder createTestFolder(UUID userId, UUID parentId) {
        return Folder.builder()
            .id(UUID.randomUUID())
            .name("Test Folder")
            .ownedBy(userId)
            .parentId(parentId)
            .status(FolderStatus.Created)
            .build();
    }
    
    public static File createTestFile(UUID userId, UUID parentId) {
        return File.builder()
            .id(UUID.randomUUID())
            .name("test.sdf")
            .ownedBy(userId)
            .parentId(parentId)
            .type(FileType.Records)
            .status(FileStatus.Processed)
            .blobId(UUID.randomUUID())
            .bucket(userId.toString())
            .build();
    }
}
```

## Coverage Requirements

- Unit tests: > 80% line coverage
- Integration tests: All endpoints covered
- Contract tests: All OpenAPI operations validated
- Error handling: All error codes tested

