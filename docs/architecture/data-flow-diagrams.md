# Data Flow Diagrams

**Status**: Current State  
**Last Updated**: 2025-01-15

## Overview

Data flow diagrams show how data moves through the Leanda.io system, from user input to storage and processing.

## File Upload Flow

```mermaid
flowchart TD
    Start([User Uploads File]) --> Frontend[Angular Frontend]
    Frontend -->|"POST /api/v1/files<br/>Multipart Form Data"| APIGateway[API Gateway]
    APIGateway -->|"Authenticate"| Cognito[Cognito]
    Cognito -->|"JWT Token"| APIGateway
    APIGateway -->|"Route Request"| CoreAPI[Core API Service]
    CoreAPI -->|"Store File"| BlobStorage[Blob Storage Service]
    BlobStorage -->|"Upload Blob"| S3[S3 Bucket]
    BlobStorage -->|"Store Metadata"| DocumentDB[(DocumentDB)]
    BlobStorage -->|"Publish Event"| MSK[MSK Kafka<br/>file-events Topic]
    BlobStorage -->|"202 Accepted"| CoreAPI
    CoreAPI -->|"202 Accepted"| APIGateway
    APIGateway -->|"202 Accepted"| Frontend
    Frontend -->|"Display Success"| End([File Upload Complete])
    
    MSK -->|"FileCreated Event"| Parser[Domain Parser<br/>Chemical/Crystal/etc.]
    MSK -->|"FileCreated Event"| OfficeProcessor[Office Processor]
    MSK -->|"FileCreated Event"| Imaging[Imaging Service]
```

## File Parsing and Processing Flow

```mermaid
flowchart TD
    Start([FileCreated Event]) --> MSK[MSK Kafka<br/>file-events Topic]
    MSK -->|"Consume Event"| Parser[Domain Parser Service]
    Parser -->|"Fetch File"| BlobStorage[Blob Storage Service]
    BlobStorage -->|"Download from S3"| S3[S3 Bucket]
    S3 -->|"File Data"| BlobStorage
    BlobStorage -->|"File Data"| Parser
    Parser -->|"Parse File"| ParseLogic[Parsing Logic<br/>SDF/MOL/CIF/etc.]
    ParseLogic -->|"Extract Records"| Records[Parsed Records]
    Records -->|"Store Records"| DocumentDB[(DocumentDB)]
    Parser -->|"Publish Event"| MSK2[MSK Kafka<br/>file-events Topic]
    MSK2 -->|"FileParsed Event"| MetaProcessing[Metadata Processing]
    MSK2 -->|"FileParsed Event"| Indexing[Indexing Service]
    MSK2 -->|"FileParsed Event"| ChemicalProps[Chemical Properties]
    
    ParseLogic -->|"Parse Failed"| Error[Error Handling]
    Error -->|"Publish Event"| MSK3[MSK Kafka<br/>file-parse-failed Topic]
```

## Metadata Extraction Flow

```mermaid
flowchart TD
    Start([FileParsed Event]) --> MSK[MSK Kafka<br/>file-events Topic]
    MSK -->|"Consume Event"| MetaProcessing[Metadata Processing Service]
    MetaProcessing -->|"Fetch Parsed Data"| DocumentDB[(DocumentDB)]
    DocumentDB -->|"Parsed Records"| MetaProcessing
    MetaProcessing -->|"Analyze Fields"| TypeQualifier[Type Qualifier<br/>String/Integer/Decimal/Boolean]
    TypeQualifier -->|"Field Types"| MetadataGen[Metadata Generation]
    MetadataGen -->|"Calculate Stats"| Stats[Min/Max Values<br/>Counts, etc.]
    Stats -->|"Generate Metadata"| InfoboxMetadata[Infobox Metadata]
    Stats -->|"Generate Metadata"| EntityMetadata[Entity Metadata]
    InfoboxMetadata -->|"Store"| DocumentDB
    EntityMetadata -->|"Store"| DocumentDB
    MetaProcessing -->|"Publish Event"| MSK2[MSK Kafka<br/>metadata-events Topic]
    MSK2 -->|"MetadataGenerated Event"| Indexing[Indexing Service]
```

## Indexing Flow

```mermaid
flowchart TD
    Start([Entity Event]) --> MSK[MSK Kafka<br/>file-events/folder-events/record-events]
    MSK -->|"Consume Event"| Indexing[Indexing Service]
    Indexing -->|"Fetch Entity Data"| DocumentDB[(DocumentDB)]
    DocumentDB -->|"Entity Data"| Indexing
    Indexing -->|"Fetch Metadata"| DocumentDB
    DocumentDB -->|"Metadata"| Indexing
    Indexing -->|"Build Index Document"| IndexDoc[Index Document<br/>Fields, Metadata, Content]
    IndexDoc -->|"Index to OpenSearch"| OpenSearch[(OpenSearch)]
    OpenSearch -->|"Indexed"| Indexing
    Indexing -->|"Publish Event"| MSK2[MSK Kafka<br/>indexing-events Topic]
    MSK2 -->|"EntityIndexed Event"| Notification[Notification Service<br/>Future]
```

## Search Flow

```mermaid
flowchart TD
    Start([User Searches]) --> Frontend[Angular Frontend]
    Frontend -->|"GET /api/v1/search?q=..."| APIGateway[API Gateway]
    APIGateway -->|"Authenticate"| Cognito[Cognito]
    Cognito -->|"JWT Token"| APIGateway
    APIGateway -->|"Route Request"| CoreAPI[Core API Service]
    CoreAPI -->|"Check Cache"| Redis[(Redis Cache)]
    Redis -->|"Cache Hit?"| CacheHit{Cache Hit?}
    CacheHit -->|"Yes"| ReturnCache[Return Cached Results]
    CacheHit -->|"No"| CoreAPI
    CoreAPI -->|"Query OpenSearch"| OpenSearch[(OpenSearch)]
    OpenSearch -->|"Search Results"| CoreAPI
    CoreAPI -->|"Store in Cache"| Redis
    CoreAPI -->|"Return Results"| APIGateway
    APIGateway -->|"Return Results"| Frontend
    Frontend -->|"Display Results"| End([Search Complete])
    ReturnCache -->|"Return Results"| APIGateway
```

## Event-Driven Processing Flow

```mermaid
flowchart LR
    subgraph "Event Sources"
        FileUpload[File Upload]
        UserAction[User Action]
        SystemEvent[System Event]
    end
    
    subgraph "Event Bus"
        MSK[MSK Kafka<br/>Topics]
    end
    
    subgraph "Event Consumers"
        Parsers[Domain Parsers]
        Processors[Processors]
        Indexing[Indexing]
        Notifications[Notifications]
    end
    
    subgraph "Data Stores"
        DocumentDB[(DocumentDB)]
        S3[(S3)]
        OpenSearch[(OpenSearch)]
    end
    
    FileUpload -->|"FileCreated"| MSK
    UserAction -->|"UserUpdated"| MSK
    SystemEvent -->|"SystemEvent"| MSK
    
    MSK -->|"Subscribe"| Parsers
    MSK -->|"Subscribe"| Processors
    MSK -->|"Subscribe"| Indexing
    MSK -->|"Subscribe"| Notifications
    
    Parsers -->|"Store"| DocumentDB
    Parsers -->|"Store"| S3
    Processors -->|"Store"| DocumentDB
    Indexing -->|"Index"| OpenSearch
```

## Chemical Properties Calculation Flow

```mermaid
flowchart TD
    Start([FileParsed Event<br/>Chemical File]) --> MSK[MSK Kafka<br/>file-events Topic]
    MSK -->|"Consume Event"| ChemicalProps[Chemical Properties Service]
    ChemicalProps -->|"Fetch Parsed Data"| DocumentDB[(DocumentDB)]
    DocumentDB -->|"Chemical Structure"| ChemicalProps
    ChemicalProps -->|"Calculate Properties"| CalcLogic[Property Calculation<br/>Molecular Weight<br/>LogP, etc.]
    CalcLogic -->|"Properties"| Properties[Chemical Properties]
    Properties -->|"Store"| DocumentDB
    ChemicalProps -->|"Publish Event"| MSK2[MSK Kafka<br/>chemical-properties-events Topic]
    MSK2 -->|"PropertiesCalculated Event"| Indexing[Indexing Service]
    MSK2 -->|"PropertiesCalculated Event"| MetaProcessing[Metadata Processing]
```

## Office Document Conversion Flow

```mermaid
flowchart TD
    Start([FileCreated Event<br/>Office Document]) --> MSK[MSK Kafka<br/>file-events Topic]
    MSK -->|"Consume Event"| OfficeProcessor[Office Processor Service]
    OfficeProcessor -->|"Fetch File"| BlobStorage[Blob Storage Service]
    BlobStorage -->|"Download from S3"| S3[S3 Bucket]
    S3 -->|"Office Document"| BlobStorage
    BlobStorage -->|"File Data"| OfficeProcessor
    OfficeProcessor -->|"Convert to PDF"| Conversion[Document Conversion<br/>LibreOffice/Office]
    Conversion -->|"PDF File"| OfficeProcessor
    OfficeProcessor -->|"Extract Metadata"| MetaExtraction[Metadata Extraction<br/>Title, Author, etc.]
    MetaExtraction -->|"Metadata"| OfficeProcessor
    OfficeProcessor -->|"Upload PDF"| BlobStorage
    BlobStorage -->|"Store PDF in S3"| S3
    OfficeProcessor -->|"Store Metadata"| DocumentDB[(DocumentDB)]
    OfficeProcessor -->|"Publish Events"| MSK2[MSK Kafka<br/>office-events Topic]
    MSK2 -->|"ConvertedToPdf Event"| Indexing[Indexing Service]
    MSK2 -->|"MetaExtracted Event"| MetaProcessing[Metadata Processing]
```

## Data Flow Characteristics

### Synchronous Flows
- **User-initiated actions**: File upload, search, user management
- **API requests**: REST API calls with immediate responses
- **Cache lookups**: Redis cache for frequently accessed data

### Asynchronous Flows
- **Event-driven processing**: File parsing, metadata extraction, indexing
- **Background jobs**: Long-running processing tasks
- **Event publishing**: Domain events for loose coupling

### Data Storage Patterns

1. **Write-Through**: Data written to both cache and database
2. **Write-Behind**: Events published, data written asynchronously
3. **Read-Through**: Cache checked first, then database if miss

### Error Handling

- **Retry Logic**: Exponential backoff for transient failures
- **Dead Letter Queues**: Failed events sent to DLQ
- **Error Events**: Error events published for monitoring
- **Circuit Breakers**: Prevent cascading failures

## Related Diagrams

- [Sequence Diagrams](./sequence-diagrams.md) - Detailed interaction sequences
- [Integration Patterns](./integration-patterns.md) - Communication patterns
- [Container Diagram](./container-diagram.md) - System containers

---

**Document Version**: 1.0
