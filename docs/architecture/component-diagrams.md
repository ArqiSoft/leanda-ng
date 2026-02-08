# Component Diagrams

**Status**: Current State  
**Last Updated**: 2025-01-15

## Overview

Component diagrams show the internal structure of key containers, breaking them down into their constituent components.

## Core API Service Components

```mermaid
graph TD
    subgraph "Core API Service"
        subgraph "API Layer"
            UsersResource[UsersResource<br/>REST Endpoint]
            EventsResource[EventsResource<br/>REST Endpoint]
            WebSocketEndpoint[WebSocketEndpoint<br/>Real-time Updates]
        end
        
        subgraph "Application Layer"
            UserService[UserService<br/>Business Logic]
            EventPublisher[EventPublisher<br/>Event Publishing]
            WebSocketManager[WebSocketManager<br/>Connection Management]
        end
        
        subgraph "Domain Layer"
            User[User Entity<br/>Domain Model]
            UserCreated[UserCreated Event<br/>Domain Event]
            UserUpdated[UserUpdated Event<br/>Domain Event]
        end
        
        subgraph "Infrastructure Layer"
            UserRepository[UserRepository<br/>MongoDB Access]
            KafkaProducer[KafkaProducer<br/>Event Publishing]
            MongoClient[MongoDB Client<br/>Database Connection]
        end
    end
    
    subgraph "External"
        DocumentDB[(DocumentDB)]
        MSK[MSK Kafka]
    end
    
    UsersResource --> UserService
    EventsResource --> EventPublisher
    WebSocketEndpoint --> WebSocketManager
    
    UserService --> User
    UserService --> UserRepository
    EventPublisher --> UserCreated
    EventPublisher --> UserUpdated
    EventPublisher --> KafkaProducer
    
    UserRepository --> MongoClient
    MongoClient --> DocumentDB
    KafkaProducer --> MSK
```

## Blob Storage Service Components

```mermaid
graph TD
    subgraph "Blob Storage Service"
        subgraph "API Layer"
            BlobResource[BlobResource<br/>REST Endpoint]
            HealthResource[HealthResource<br/>Health Checks]
        end
        
        subgraph "Application Layer"
            BlobService[BlobService<br/>Business Logic]
            EventPublisher[EventPublisher<br/>Event Publishing]
        end
        
        subgraph "Domain Layer"
            BlobInfo[BlobInfo<br/>Domain Model]
            FileCreated[FileCreated Event<br/>Domain Event]
            BlobLoaded[BlobLoaded Event<br/>Domain Event]
        end
        
        subgraph "Infrastructure Layer"
            GridFsBlobStorage[GridFsBlobStorage<br/>MongoDB GridFS]
            S3Client[S3Client<br/>S3 Integration]
            KafkaProducer[KafkaProducer<br/>Event Publishing]
            MongoClient[MongoDB Client]
        end
    end
    
    subgraph "External"
        DocumentDB[(DocumentDB<br/>GridFS)]
        S3[(S3)]
        MSK[MSK Kafka]
    end
    
    BlobResource --> BlobService
    HealthResource --> BlobService
    
    BlobService --> BlobInfo
    BlobService --> GridFsBlobStorage
    BlobService --> S3Client
    EventPublisher --> FileCreated
    EventPublisher --> BlobLoaded
    EventPublisher --> KafkaProducer
    
    GridFsBlobStorage --> MongoClient
    MongoClient --> DocumentDB
    S3Client --> S3
    KafkaProducer --> MSK
```

## Chemical Parser Service Components

```mermaid
graph TD
    subgraph "Chemical Parser Service"
        subgraph "API Layer"
            HealthResource[HealthResource<br/>Health Checks]
        end
        
        subgraph "Application Layer"
            ChemicalParserService[ChemicalParserService<br/>Parsing Logic]
            EventPublisher[EventPublisher<br/>Event Publishing]
        end
        
        subgraph "Domain Layer"
            ParseFileCommand[ParseFileCommand<br/>Domain Command]
            FileParsedEvent[FileParsedEvent<br/>Domain Event]
            RecordParsedEvent[RecordParsedEvent<br/>Domain Event]
            FileParseFailedEvent[FileParseFailedEvent<br/>Domain Event]
        end
        
        subgraph "Infrastructure Layer"
            ParseFileCommandHandler[ParseFileCommandHandler<br/>Kafka Consumer]
            BlobStorageClient[BlobStorageClient<br/>HTTP Client]
            KafkaProducer[KafkaProducer<br/>Event Publishing]
        end
    end
    
    subgraph "External"
        MSK[MSK Kafka]
        BlobStorage[Blob Storage Service]
    end
    
    HealthResource --> ChemicalParserService
    
    ParseFileCommandHandler --> ParseFileCommand
    ParseFileCommandHandler --> ChemicalParserService
    ChemicalParserService --> BlobStorageClient
    ChemicalParserService --> EventPublisher
    
    EventPublisher --> FileParsedEvent
    EventPublisher --> RecordParsedEvent
    EventPublisher --> FileParseFailedEvent
    EventPublisher --> KafkaProducer
    
    ParseFileCommandHandler --> MSK
    BlobStorageClient --> BlobStorage
    KafkaProducer --> MSK
```

## Metadata Processing Service Components

```mermaid
graph TD
    subgraph "Metadata Processing Service"
        subgraph "API Layer"
            HealthResource[HealthResource<br/>Health Checks]
        end
        
        subgraph "Application Layer"
            MetadataGenerationService[MetadataGenerationService<br/>Metadata Logic]
            TypeQualifier[TypeQualifier<br/>Type Detection]
            EventPublisher[EventPublisher<br/>Event Publishing]
        end
        
        subgraph "Domain Layer"
            GenerateMetadataCommand[GenerateMetadataCommand<br/>Domain Command]
            MetadataGeneratedEvent[MetadataGeneratedEvent<br/>Domain Event]
            InfoboxMetadata[InfoboxMetadata<br/>Domain Model]
            EntityMetadata[EntityMetadata<br/>Domain Model]
            FieldDefinition[FieldDefinition<br/>Domain Model]
        end
        
        subgraph "Infrastructure Layer"
            GenerateMetadataCommandHandler[GenerateMetadataCommandHandler<br/>Kafka Consumer]
            MongoRepository[MongoRepository<br/>MongoDB Access]
            KafkaProducer[KafkaProducer<br/>Event Publishing]
            MongoClient[MongoDB Client]
        end
    end
    
    subgraph "External"
        MSK[MSK Kafka]
        DocumentDB[(DocumentDB)]
    end
    
    HealthResource --> MetadataGenerationService
    
    GenerateMetadataCommandHandler --> GenerateMetadataCommand
    GenerateMetadataCommandHandler --> MetadataGenerationService
    MetadataGenerationService --> TypeQualifier
    MetadataGenerationService --> InfoboxMetadata
    MetadataGenerationService --> EntityMetadata
    MetadataGenerationService --> FieldDefinition
    MetadataGenerationService --> MongoRepository
    MetadataGenerationService --> EventPublisher
    
    EventPublisher --> MetadataGeneratedEvent
    EventPublisher --> KafkaProducer
    
    GenerateMetadataCommandHandler --> MSK
    MongoRepository --> MongoClient
    MongoClient --> DocumentDB
    KafkaProducer --> MSK
```

## Indexing Service Components

```mermaid
graph TD
    subgraph "Indexing Service"
        subgraph "API Layer"
            HealthResource[HealthResource<br/>Health Checks]
        end
        
        subgraph "Application Layer"
            IndexingService[IndexingService<br/>Indexing Logic]
            EventPublisher[EventPublisher<br/>Event Publishing]
        end
        
        subgraph "Domain Layer"
            FilePersistedEvent[FilePersistedEvent<br/>Domain Event]
            FolderPersistedEvent[FolderPersistedEvent<br/>Domain Event]
            RecordPersistedEvent[RecordPersistedEvent<br/>Domain Event]
            EntityIndexedEvent[EntityIndexedEvent<br/>Domain Event]
            IndexedEntity[IndexedEntity<br/>Domain Model]
        end
        
        subgraph "Infrastructure Layer"
            FileEventHandler[FileEventHandler<br/>Kafka Consumer]
            FolderEventHandler[FolderEventHandler<br/>Kafka Consumer]
            RecordEventHandler[RecordEventHandler<br/>Kafka Consumer]
            OpenSearchClient[OpenSearchClient<br/>HTTP Client]
            KafkaProducer[KafkaProducer<br/>Event Publishing]
        end
    end
    
    subgraph "External"
        MSK[MSK Kafka]
        OpenSearch[(OpenSearch)]
    end
    
    HealthResource --> IndexingService
    
    FileEventHandler --> FilePersistedEvent
    FolderEventHandler --> FolderPersistedEvent
    RecordEventHandler --> RecordPersistedEvent
    
    FileEventHandler --> IndexingService
    FolderEventHandler --> IndexingService
    RecordEventHandler --> IndexingService
    
    IndexingService --> IndexedEntity
    IndexingService --> OpenSearchClient
    IndexingService --> EventPublisher
    
    EventPublisher --> EntityIndexedEvent
    EventPublisher --> KafkaProducer
    
    FileEventHandler --> MSK
    FolderEventHandler --> MSK
    RecordEventHandler --> MSK
    OpenSearchClient --> OpenSearch
    KafkaProducer --> MSK
```

## Component Responsibilities

### API Layer
- **Purpose**: Handle HTTP requests and responses
- **Components**: REST endpoints, WebSocket endpoints, health checks
- **Responsibilities**:
  - Request validation
  - Response formatting
  - Error handling
  - Authentication/authorization

### Application Layer
- **Purpose**: Business logic and orchestration
- **Components**: Services, managers, coordinators
- **Responsibilities**:
  - Business rule enforcement
  - Transaction management
  - Service orchestration
  - Event publishing

### Domain Layer
- **Purpose**: Core domain models and logic
- **Components**: Entities, value objects, domain events, commands
- **Responsibilities**:
  - Domain model representation
  - Business invariants
  - Domain events
  - Commands

### Infrastructure Layer
- **Purpose**: Technical implementation details
- **Components**: Repositories, clients, adapters
- **Responsibilities**:
  - Database access
  - External service integration
  - Message queue integration
  - File system access

## Design Patterns

### Repository Pattern
- **Usage**: Data access abstraction
- **Examples**: UserRepository, MongoRepository
- **Benefits**: Decouples domain from persistence

### Command Handler Pattern
- **Usage**: Event-driven command processing
- **Examples**: ParseFileCommandHandler, GenerateMetadataCommandHandler
- **Benefits**: Decouples command from execution

### Event Publisher Pattern
- **Usage**: Asynchronous event publishing
- **Examples**: EventPublisher in all services
- **Benefits**: Loose coupling between services

### Client Pattern
- **Usage**: External service integration
- **Examples**: BlobStorageClient, OpenSearchClient
- **Benefits**: Abstraction of external dependencies

## Related Diagrams

- [Container Diagram](./container-diagram.md) - High-level containers
- [Deployment Diagram](./deployment-diagram.md) - Infrastructure deployment
- [Sequence Diagrams](./sequence-diagrams.md) - Component interactions

---

**Document Version**: 1.0
