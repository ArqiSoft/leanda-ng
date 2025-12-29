# Test Data Fixtures Specification

## Overview

This document defines test data fixtures for Leanda NG services, providing consistent test data across all test categories.

## Test Users

### testUser1 (Primary Test User)
```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "displayName": "Test User One",
  "firstName": "Test",
  "lastName": "User",
  "loginName": "testuser1",
  "email": "testuser1@example.com",
  "avatar": "https://example.com/avatar1.png",
  "createdBy": "00000000-0000-0000-0000-000000000001",
  "createdDateTime": "2024-01-01T00:00:00Z",
  "updatedBy": "00000000-0000-0000-0000-000000000001",
  "updatedDateTime": "2024-01-01T00:00:00Z",
  "version": 1
}
```

### testUser2 (Secondary Test User)
```json
{
  "id": "00000000-0000-0000-0000-000000000002",
  "displayName": "Test User Two",
  "firstName": "Second",
  "lastName": "User",
  "loginName": "testuser2",
  "email": "testuser2@example.com",
  "avatar": "https://example.com/avatar2.png",
  "createdBy": "00000000-0000-0000-0000-000000000002",
  "createdDateTime": "2024-01-01T00:00:00Z",
  "updatedBy": "00000000-0000-0000-0000-000000000002",
  "updatedDateTime": "2024-01-01T00:00:00Z",
  "version": 1
}
```

### adminUser (Admin User)
```json
{
  "id": "00000000-0000-0000-0000-000000000099",
  "displayName": "Admin User",
  "firstName": "Admin",
  "lastName": "User",
  "loginName": "admin",
  "email": "admin@example.com",
  "version": 1
}
```

## Test Folders

### rootFolder (User1 Root)
```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "type": "User",
  "name": "Test User One",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": null,
  "status": "Created",
  "isDeleted": false,
  "version": 1
}
```

### testFolder1 (Standard Folder)
```json
{
  "id": "10000000-0000-0000-0000-000000000001",
  "type": "Folder",
  "name": "Test Folder 1",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "createdBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "00000000-0000-0000-0000-000000000001",
  "status": "Created",
  "isDeleted": false,
  "accessPermissions": {
    "isPublic": false,
    "users": [],
    "groups": []
  },
  "version": 1
}
```

### sharedFolder (Public Folder)
```json
{
  "id": "10000000-0000-0000-0000-000000000002",
  "type": "Folder",
  "name": "Shared Folder",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "00000000-0000-0000-0000-000000000001",
  "status": "Created",
  "isDeleted": false,
  "accessPermissions": {
    "isPublic": true,
    "users": [],
    "groups": []
  },
  "version": 1
}
```

### nestedFolder (Nested Folder)
```json
{
  "id": "10000000-0000-0000-0000-000000000003",
  "type": "Folder",
  "name": "Nested Folder",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "10000000-0000-0000-0000-000000000001",
  "status": "Created",
  "isDeleted": false,
  "version": 1
}
```

### emptyFolder (Empty Folder)
```json
{
  "id": "10000000-0000-0000-0000-000000000004",
  "type": "Folder",
  "name": "Empty Folder",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "00000000-0000-0000-0000-000000000001",
  "status": "Created",
  "isDeleted": false,
  "version": 1
}
```

## Test Files

### chemicalFile (SDF File with Records)
```json
{
  "id": "20000000-0000-0000-0000-000000000001",
  "type": "File",
  "subType": "Records",
  "name": "chemicals.sdf",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "createdBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "10000000-0000-0000-0000-000000000001",
  "bucket": "00000000-0000-0000-0000-000000000001",
  "blobId": "b0000000-0000-0000-0000-000000000001",
  "length": 102400,
  "md5": "d41d8cd98f00b204e9800998ecf8427e",
  "status": "Processed",
  "totalRecords": 10,
  "images": [
    {
      "id": "i0000000-0000-0000-0000-000000000001",
      "bucket": "00000000-0000-0000-0000-000000000001",
      "height": 300,
      "width": 300,
      "mimeType": "image/png",
      "scale": "medium"
    }
  ],
  "blob": {
    "id": "b0000000-0000-0000-0000-000000000001",
    "bucket": "00000000-0000-0000-0000-000000000001",
    "length": 102400,
    "md5": "d41d8cd98f00b204e9800998ecf8427e"
  },
  "isDeleted": false,
  "version": 5
}
```

### pdfFile (PDF Document)
```json
{
  "id": "20000000-0000-0000-0000-000000000002",
  "type": "File",
  "subType": "Pdf",
  "name": "document.pdf",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "10000000-0000-0000-0000-000000000001",
  "bucket": "00000000-0000-0000-0000-000000000001",
  "blobId": "b0000000-0000-0000-0000-000000000002",
  "length": 51200,
  "status": "Processed",
  "images": [
    {
      "id": "i0000000-0000-0000-0000-000000000002",
      "bucket": "00000000-0000-0000-0000-000000000001",
      "mimeType": "image/png",
      "scale": "thumbnail"
    }
  ],
  "isDeleted": false,
  "version": 2
}
```

### imageFile (Image File)
```json
{
  "id": "20000000-0000-0000-0000-000000000003",
  "type": "File",
  "subType": "Image",
  "name": "structure.png",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "10000000-0000-0000-0000-000000000001",
  "bucket": "00000000-0000-0000-0000-000000000001",
  "blobId": "b0000000-0000-0000-0000-000000000003",
  "length": 25600,
  "status": "Processed",
  "isDeleted": false,
  "version": 1
}
```

### processingFile (File in Processing)
```json
{
  "id": "20000000-0000-0000-0000-000000000004",
  "type": "File",
  "subType": "Records",
  "name": "large-file.sdf",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "10000000-0000-0000-0000-000000000001",
  "bucket": "00000000-0000-0000-0000-000000000001",
  "blobId": "b0000000-0000-0000-0000-000000000004",
  "status": "Processing",
  "isDeleted": false,
  "version": 2
}
```

### failedFile (Failed File)
```json
{
  "id": "20000000-0000-0000-0000-000000000005",
  "type": "File",
  "subType": "Records",
  "name": "corrupted.sdf",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "10000000-0000-0000-0000-000000000001",
  "bucket": "00000000-0000-0000-0000-000000000001",
  "blobId": "b0000000-0000-0000-0000-000000000005",
  "status": "Failed",
  "isDeleted": false,
  "version": 2
}
```

## Test Records

### chemicalRecord1 (Chemical Structure)
```json
{
  "id": "30000000-0000-0000-0000-000000000001",
  "type": "Chemical",
  "fileId": "20000000-0000-0000-0000-000000000001",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "bucket": "00000000-0000-0000-0000-000000000001",
  "blobId": "b0000000-0000-0000-0000-000000000010",
  "index": 0,
  "status": "Processed",
  "images": [
    {
      "id": "i0000000-0000-0000-0000-000000000010",
      "bucket": "00000000-0000-0000-0000-000000000001",
      "mimeType": "image/svg+xml",
      "scale": "vector"
    }
  ],
  "properties": {
    "fields": [
      {"name": "Compound_Name", "value": "Aspirin"},
      {"name": "CAS", "value": "50-78-2"},
      {"name": "MW", "value": 180.16}
    ],
    "chemicalProperties": {
      "molecularFormula": "C9H8O4",
      "molecularWeight": 180.16,
      "inchi": "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)",
      "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"
    }
  },
  "version": 1
}
```

### crystalRecord1 (Crystal Structure)
```json
{
  "id": "30000000-0000-0000-0000-000000000002",
  "type": "Crystal",
  "fileId": "20000000-0000-0000-0000-000000000001",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "bucket": "00000000-0000-0000-0000-000000000001",
  "blobId": "b0000000-0000-0000-0000-000000000011",
  "index": 1,
  "status": "Processed",
  "properties": {
    "fields": [
      {"name": "Cell_a", "value": 5.43},
      {"name": "Cell_b", "value": 5.43},
      {"name": "Cell_c", "value": 5.43},
      {"name": "Space_Group", "value": "Fm-3m"}
    ]
  },
  "version": 1
}
```

## Test Models

### publicModel (Public ML Model)
```json
{
  "id": "40000000-0000-0000-0000-000000000001",
  "type": "Model",
  "name": "Solubility Predictor",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "10000000-0000-0000-0000-000000000001",
  "status": "Trained",
  "blob": {
    "id": "b0000000-0000-0000-0000-000000000020",
    "bucket": "00000000-0000-0000-0000-000000000001"
  },
  "property": {
    "name": "Solubility",
    "type": "Regression",
    "units": "log(mol/L)"
  },
  "method": "RandomForest",
  "fingerprints": [
    {"type": "ECFP", "size": 2048, "radius": 3}
  ],
  "metrics": {
    "r2": 0.85,
    "rmse": 0.42
  },
  "accessPermissions": {
    "isPublic": true,
    "users": [],
    "groups": []
  },
  "version": 3
}
```

### privateModel (Private ML Model)
```json
{
  "id": "40000000-0000-0000-0000-000000000002",
  "type": "Model",
  "name": "Toxicity Classifier",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "10000000-0000-0000-0000-000000000001",
  "status": "Trained",
  "blob": {
    "id": "b0000000-0000-0000-0000-000000000021",
    "bucket": "00000000-0000-0000-0000-000000000001"
  },
  "property": {
    "name": "Toxicity",
    "type": "Classification"
  },
  "method": "SVM",
  "accessPermissions": {
    "isPublic": false,
    "users": [],
    "groups": []
  },
  "version": 2
}
```

### trainingModel (Model in Training)
```json
{
  "id": "40000000-0000-0000-0000-000000000003",
  "type": "Model",
  "name": "Activity Predictor",
  "ownedBy": "00000000-0000-0000-0000-000000000001",
  "parentId": "10000000-0000-0000-0000-000000000001",
  "status": "Training",
  "version": 1
}
```

## Test Blobs

### sdfBlob (SDF Content)
```
Chemical file content for testing.
File path: test-resources/chemicals.sdf
Size: 102400 bytes
MD5: d41d8cd98f00b204e9800998ecf8427e
Content-Type: chemical/x-mdl-sdfile
```

### pdfBlob (PDF Content)
```
PDF file content for testing.
File path: test-resources/document.pdf
Size: 51200 bytes
Content-Type: application/pdf
```

### imageBlob (Image Content)
```
PNG image content for testing.
File path: test-resources/structure.png
Size: 25600 bytes
Content-Type: image/png
```

## Test Events

### fileCreatedEvent
```json
{
  "id": "20000000-0000-0000-0000-000000000001",
  "userId": "00000000-0000-0000-0000-000000000001",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": 1,
  "bucket": "00000000-0000-0000-0000-000000000001",
  "blobId": "b0000000-0000-0000-0000-000000000001",
  "parentId": "10000000-0000-0000-0000-000000000001",
  "fileName": "chemicals.sdf",
  "length": 102400,
  "md5": "d41d8cd98f00b204e9800998ecf8427e",
  "fileStatus": "Loaded",
  "fileType": "Records"
}
```

### userCreatedCommand
```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "userId": "00000000-0000-0000-0000-000000000001",
  "correlationId": "c0000000-0000-0000-0000-000000000001",
  "displayName": "Test User One",
  "firstName": "Test",
  "lastName": "User",
  "loginName": "testuser1",
  "email": "testuser1@example.com"
}
```

## Java Test Fixtures Class

```java
public class TestDataFixtures {
    
    // User IDs
    public static final UUID USER_1_ID = UUID.fromString("00000000-0000-0000-0000-000000000001");
    public static final UUID USER_2_ID = UUID.fromString("00000000-0000-0000-0000-000000000002");
    public static final UUID ADMIN_ID = UUID.fromString("00000000-0000-0000-0000-000000000099");
    
    // Folder IDs
    public static final UUID FOLDER_1_ID = UUID.fromString("10000000-0000-0000-0000-000000000001");
    public static final UUID SHARED_FOLDER_ID = UUID.fromString("10000000-0000-0000-0000-000000000002");
    
    // File IDs
    public static final UUID CHEMICAL_FILE_ID = UUID.fromString("20000000-0000-0000-0000-000000000001");
    public static final UUID PDF_FILE_ID = UUID.fromString("20000000-0000-0000-0000-000000000002");
    
    // Record IDs
    public static final UUID CHEMICAL_RECORD_ID = UUID.fromString("30000000-0000-0000-0000-000000000001");
    
    // Model IDs
    public static final UUID PUBLIC_MODEL_ID = UUID.fromString("40000000-0000-0000-0000-000000000001");
    
    public static User testUser1() {
        return User.builder()
            .id(USER_1_ID)
            .displayName("Test User One")
            .firstName("Test")
            .lastName("User")
            .loginName("testuser1")
            .email("testuser1@example.com")
            .build();
    }
    
    public static Folder testFolder1() {
        return Folder.builder()
            .id(FOLDER_1_ID)
            .name("Test Folder 1")
            .ownedBy(USER_1_ID)
            .parentId(USER_1_ID)
            .status(FolderStatus.CREATED)
            .build();
    }
    
    public static File chemicalFile() {
        return File.builder()
            .id(CHEMICAL_FILE_ID)
            .name("chemicals.sdf")
            .ownedBy(USER_1_ID)
            .parentId(FOLDER_1_ID)
            .type(FileType.RECORDS)
            .status(FileStatus.PROCESSED)
            .totalRecords(10)
            .build();
    }
    
    public static Record chemicalRecord() {
        return Record.builder()
            .id(CHEMICAL_RECORD_ID)
            .fileId(CHEMICAL_FILE_ID)
            .ownedBy(USER_1_ID)
            .index(0)
            .type(RecordType.CHEMICAL)
            .status(RecordStatus.PROCESSED)
            .build();
    }
    
    public static Model publicModel() {
        return Model.builder()
            .id(PUBLIC_MODEL_ID)
            .name("Solubility Predictor")
            .ownedBy(USER_1_ID)
            .status(ModelStatus.TRAINED)
            .accessPermissions(AccessPermissions.builder().isPublic(true).build())
            .build();
    }
    
    public static void seedDatabase(MongoDatabase db) {
        db.getCollection("Users").insertOne(Document.parse(testUser1Json()));
        db.getCollection("Folders").insertOne(Document.parse(testFolder1Json()));
        db.getCollection("Files").insertOne(Document.parse(chemicalFileJson()));
        db.getCollection("Records").insertOne(Document.parse(chemicalRecordJson()));
        db.getCollection("Models").insertOne(Document.parse(publicModelJson()));
    }
    
    public static void clearDatabase(MongoDatabase db) {
        db.getCollection("Users").drop();
        db.getCollection("Folders").drop();
        db.getCollection("Files").drop();
        db.getCollection("Records").drop();
        db.getCollection("Models").drop();
        db.getCollection("Nodes").drop();
    }
}
```

## MongoDB Seed Script

```javascript
// File: test-resources/seed-test-data.js

// Users
db.Users.insertMany([
  {
    _id: UUID("00000000-0000-0000-0000-000000000001"),
    displayName: "Test User One",
    firstName: "Test",
    lastName: "User",
    loginName: "testuser1",
    email: "testuser1@example.com",
    version: 1
  },
  {
    _id: UUID("00000000-0000-0000-0000-000000000002"),
    displayName: "Test User Two",
    firstName: "Second",
    lastName: "User",
    loginName: "testuser2",
    email: "testuser2@example.com",
    version: 1
  }
]);

// Nodes (unified view)
db.Nodes.insertMany([
  // User nodes
  {
    _id: UUID("00000000-0000-0000-0000-000000000001"),
    Type: "User",
    Name: "Test User One",
    OwnedBy: UUID("00000000-0000-0000-0000-000000000001"),
    IsDeleted: false,
    Version: 1
  },
  // Folder nodes
  {
    _id: UUID("10000000-0000-0000-0000-000000000001"),
    Type: "Folder",
    Name: "Test Folder 1",
    OwnedBy: UUID("00000000-0000-0000-0000-000000000001"),
    ParentId: UUID("00000000-0000-0000-0000-000000000001"),
    Status: "Created",
    IsDeleted: false,
    Version: 1
  },
  // File nodes
  {
    _id: UUID("20000000-0000-0000-0000-000000000001"),
    Type: "File",
    SubType: "Records",
    Name: "chemicals.sdf",
    OwnedBy: UUID("00000000-0000-0000-0000-000000000001"),
    ParentId: UUID("10000000-0000-0000-0000-000000000001"),
    Status: "Processed",
    TotalRecords: 10,
    IsDeleted: false,
    Version: 5
  }
]);

// Access Permissions
db.AccessPermissions.insertMany([
  {
    _id: UUID("10000000-0000-0000-0000-000000000002"),
    IsPublic: true,
    Users: [],
    Groups: []
  },
  {
    _id: UUID("40000000-0000-0000-0000-000000000001"),
    IsPublic: true,
    Users: [],
    Groups: []
  }
]);

print("Test data seeded successfully!");
```

