# Sequence Diagrams

**Status**: Current State  
**Last Updated**: 2025-01-15

## Overview

Sequence diagrams show the detailed interaction sequences between components for key system flows.

## File Upload Sequence

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant APIGateway
    participant Cognito
    participant CoreAPI
    participant BlobStorage
    participant S3
    participant DocumentDB
    participant MSK
    participant Parser
    
    User->>Frontend: Upload File
    Frontend->>APIGateway: POST /api/v1/files (multipart)
    APIGateway->>Cognito: Validate JWT Token
    Cognito-->>APIGateway: Token Valid
    APIGateway->>CoreAPI: Forward Request
    CoreAPI->>BlobStorage: POST /api/v1/blobs (store file)
    BlobStorage->>S3: Upload File
    S3-->>BlobStorage: File Stored
    BlobStorage->>DocumentDB: Store File Metadata
    DocumentDB-->>BlobStorage: Metadata Stored
    BlobStorage->>MSK: Publish FileCreated Event
    MSK-->>BlobStorage: Event Published
    BlobStorage-->>CoreAPI: 202 Accepted
    CoreAPI-->>APIGateway: 202 Accepted
    APIGateway-->>Frontend: 202 Accepted
    Frontend-->>User: Upload Success
    
    MSK->>Parser: FileCreated Event (async)
    Parser->>BlobStorage: GET /api/v1/blobs/{id}
    BlobStorage->>S3: Download File
    S3-->>BlobStorage: File Data
    BlobStorage-->>Parser: File Data
    Parser->>Parser: Parse File
    Parser->>MSK: Publish FileParsed Event
```

## File Parsing Sequence

```mermaid
sequenceDiagram
    participant MSK
    participant Parser
    participant BlobStorage
    participant S3
    participant DocumentDB
    participant ChemicalProps
    participant MetaProcessing
    participant Indexing
    
    MSK->>Parser: FileCreated Event
    Parser->>BlobStorage: GET /api/v1/blobs/{blobId}
    BlobStorage->>S3: Get Object
    S3-->>BlobStorage: File Data
    BlobStorage-->>Parser: File Data
    Parser->>Parser: Parse File (SDF/MOL/CIF/etc.)
    Parser->>DocumentDB: Store Parsed Records
    DocumentDB-->>Parser: Records Stored
    Parser->>MSK: Publish FileParsed Event
    
    MSK->>ChemicalProps: FileParsed Event (if chemical)
    ChemicalProps->>DocumentDB: Fetch Parsed Data
    DocumentDB-->>ChemicalProps: Chemical Structure
    ChemicalProps->>ChemicalProps: Calculate Properties
    ChemicalProps->>DocumentDB: Store Properties
    ChemicalProps->>MSK: Publish PropertiesCalculated Event
    
    MSK->>MetaProcessing: FileParsed Event
    MetaProcessing->>DocumentDB: Fetch Parsed Data
    DocumentDB-->>MetaProcessing: Parsed Records
    MetaProcessing->>MetaProcessing: Analyze Fields (TypeQualifier)
    MetaProcessing->>MetaProcessing: Generate Metadata
    MetaProcessing->>DocumentDB: Store Metadata
    MetaProcessing->>MSK: Publish MetadataGenerated Event
    
    MSK->>Indexing: FileParsed Event
    Indexing->>DocumentDB: Fetch Entity Data
    DocumentDB-->>Indexing: Entity + Metadata
    Indexing->>Indexing: Build Index Document
    Indexing->>OpenSearch: Index Document
    OpenSearch-->>Indexing: Indexed
    Indexing->>MSK: Publish EntityIndexed Event
```

## Metadata Generation Sequence

```mermaid
sequenceDiagram
    participant MSK
    participant MetaProcessing
    participant DocumentDB
    participant TypeQualifier
    participant MetadataGen
    participant Indexing
    
    MSK->>MetaProcessing: FileParsed Event
    MetaProcessing->>DocumentDB: Fetch Parsed Records
    DocumentDB-->>MetaProcessing: Records with Fields
    
    loop For each Record
        loop For each Field
            MetaProcessing->>TypeQualifier: Qualify Field Type
            TypeQualifier->>TypeQualifier: Analyze Values
            TypeQualifier-->>MetaProcessing: Field Type (String/Integer/Decimal/Boolean)
        end
        
        MetaProcessing->>MetadataGen: Generate Metadata
        MetadataGen->>MetadataGen: Calculate Min/Max (numeric)
        MetadataGen->>MetadataGen: Calculate Counts
        MetadataGen->>MetadataGen: Generate Infobox Metadata
        MetadataGen->>MetadataGen: Generate Entity Metadata
        MetadataGen-->>MetaProcessing: Metadata Objects
        MetaProcessing->>DocumentDB: Store Metadata
        DocumentDB-->>MetaProcessing: Metadata Stored
    end
    
    MetaProcessing->>MSK: Publish MetadataGenerated Event
    MSK->>Indexing: MetadataGenerated Event
    Indexing->>DocumentDB: Fetch Updated Entity
    DocumentDB-->>Indexing: Entity with Metadata
    Indexing->>OpenSearch: Update Index
```

## Search Sequence

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant APIGateway
    participant Cognito
    participant CoreAPI
    participant Redis
    participant OpenSearch
    
    User->>Frontend: Search Query
    Frontend->>APIGateway: GET /api/v1/search?q=...
    APIGateway->>Cognito: Validate JWT Token
    Cognito-->>APIGateway: Token Valid
    APIGateway->>CoreAPI: Forward Request
    
    CoreAPI->>Redis: Get Cache Key (search:{query})
    Redis-->>CoreAPI: Cache Miss
    
    CoreAPI->>OpenSearch: Search Query
    OpenSearch->>OpenSearch: Execute Search
    OpenSearch-->>CoreAPI: Search Results
    
    CoreAPI->>Redis: Set Cache Key (TTL: 15 min)
    Redis-->>CoreAPI: Cached
    CoreAPI-->>APIGateway: 200 OK (Results)
    APIGateway-->>Frontend: 200 OK (Results)
    Frontend-->>User: Display Results
    
    Note over User,OpenSearch: Subsequent searches with same query<br/>will hit Redis cache
```

## User Management Sequence

```mermaid
sequenceDiagram
    participant Admin
    participant Frontend
    participant APIGateway
    participant Cognito
    participant CoreAPI
    participant DocumentDB
    participant MSK
    participant Indexing
    
    Admin->>Frontend: Create User
    Frontend->>APIGateway: POST /api/v1/users
    APIGateway->>Cognito: Validate Admin Token
    Cognito-->>APIGateway: Token Valid (Admin Role)
    APIGateway->>CoreAPI: Forward Request
    
    CoreAPI->>Cognito: Create User in User Pool
    Cognito-->>CoreAPI: User Created
    CoreAPI->>DocumentDB: Store User Metadata
    DocumentDB-->>CoreAPI: User Stored
    CoreAPI->>MSK: Publish UserCreated Event
    MSK-->>CoreAPI: Event Published
    CoreAPI-->>APIGateway: 201 Created
    APIGateway-->>Frontend: 201 Created
    Frontend-->>Admin: User Created Success
    
    MSK->>Indexing: UserCreated Event (async)
    Indexing->>DocumentDB: Fetch User Data
    DocumentDB-->>Indexing: User Data
    Indexing->>OpenSearch: Index User
    OpenSearch-->>Indexing: Indexed
    Indexing->>MSK: Publish EntityIndexed Event
```

## Office Document Conversion Sequence

```mermaid
sequenceDiagram
    participant MSK
    participant OfficeProcessor
    participant BlobStorage
    participant S3
    participant DocumentDB
    participant Indexing
    participant MetaProcessing
    
    MSK->>OfficeProcessor: FileCreated Event (Office Document)
    OfficeProcessor->>BlobStorage: GET /api/v1/blobs/{blobId}
    BlobStorage->>S3: Get Object
    S3-->>BlobStorage: Office Document
    BlobStorage-->>OfficeProcessor: Document Data
    
    OfficeProcessor->>OfficeProcessor: Convert to PDF (LibreOffice)
    OfficeProcessor->>OfficeProcessor: Extract Metadata (Title, Author, etc.)
    
    OfficeProcessor->>BlobStorage: POST /api/v1/blobs (PDF)
    BlobStorage->>S3: Upload PDF
    S3-->>BlobStorage: PDF Stored
    BlobStorage-->>OfficeProcessor: PDF Blob ID
    
    OfficeProcessor->>DocumentDB: Store PDF Metadata
    DocumentDB-->>OfficeProcessor: Metadata Stored
    
    OfficeProcessor->>MSK: Publish ConvertedToPdf Event
    OfficeProcessor->>MSK: Publish MetaExtracted Event
    
    MSK->>Indexing: ConvertedToPdf Event
    Indexing->>DocumentDB: Fetch Updated File
    DocumentDB-->>Indexing: File with PDF
    Indexing->>OpenSearch: Update Index
    
    MSK->>MetaProcessing: MetaExtracted Event
    MetaProcessing->>DocumentDB: Fetch File Metadata
    DocumentDB-->>MetaProcessing: Extracted Metadata
    MetaProcessing->>DocumentDB: Store Metadata
    MetaProcessing->>MSK: Publish MetadataGenerated Event
```

## Error Handling Sequence

```mermaid
sequenceDiagram
    participant Parser
    participant BlobStorage
    participant S3
    participant MSK
    participant DLQ
    participant Monitoring
    
    Parser->>BlobStorage: GET /api/v1/blobs/{id}
    BlobStorage->>S3: Get Object
    S3-->>BlobStorage: Error (File Not Found)
    BlobStorage-->>Parser: 404 Not Found
    
    Parser->>Parser: Handle Error
    Parser->>MSK: Publish FileParseFailed Event
    
    alt Retry Logic
        Parser->>Parser: Retry (Exponential Backoff)
        Parser->>BlobStorage: GET /api/v1/blobs/{id} (retry)
        BlobStorage->>S3: Get Object
        S3-->>BlobStorage: File Data
        BlobStorage-->>Parser: File Data
        Parser->>Parser: Parse File (Success)
    else Max Retries Exceeded
        Parser->>MSK: Publish FileParseFailed Event (Final)
        MSK->>DLQ: Send to Dead Letter Queue
        DLQ->>Monitoring: Alert (Failed Event)
    end
```

## Related Diagrams

- [Data Flow Diagrams](./data-flow-diagrams.md) - High-level data flows
- [Component Diagrams](./component-diagrams.md) - Component structure
- [Integration Patterns](./integration-patterns.md) - Communication patterns

---

**Document Version**: 1.0
