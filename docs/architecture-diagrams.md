# Leanda.io Architecture Diagrams

**Status**: Complete  
**Last Updated**: 2025-12-27  
**Architect**: Agent PROD-0 (Cloud Architect)

## High-Level Architecture

```mermaid
graph TB
    subgraph "Internet"
        Users[Users & Applications]
    end
    
    subgraph "AWS Cloud - us-east-1"
        subgraph "Edge Layer"
            CF[CloudFront CDN]
            APIGW[API Gateway]
        end
        
        subgraph "Frontend"
            Amplify[Amplify Hosting<br/>Angular 21]
        end
        
        subgraph "Compute Layer"
            ALB[Application Load Balancer]
            ECS[ECS Fargate Cluster]
            subgraph "Microservices"
                CoreAPI[core-api:8080]
                BlobStorage[blob-storage:8084]
                ChemParser[chemical-parser:8083]
                ChemProps[chemical-properties:8086]
                ReactionParser[reaction-parser:8087]
                CrystalParser[crystal-parser:8089]
                SpectraParser[spectra-parser:8090]
                Imaging[imaging:8091]
                OfficeProc[office-processor:8088]
                MetaProc[metadata-processing:8098]
                Indexing[indexing:8099]
            end
        end
        
        subgraph "Data Layer"
            DocDB[(DocumentDB<br/>Metadata)]
            Redis[(ElastiCache Redis<br/>Cache)]
            S3[(S3<br/>Blob Storage)]
            OpenSearch[(OpenSearch<br/>Search)]
        end
        
        subgraph "Messaging Layer"
            MSK[MSK Serverless<br/>Kafka]
            EB[EventBridge<br/>Events]
        end
        
        subgraph "Observability"
            CW[CloudWatch<br/>Logs & Metrics]
            XRay[X-Ray<br/>Tracing]
        end
    end
    
    Users --> CF
    Users --> APIGW
    CF --> Amplify
    APIGW --> ALB
    ALB --> ECS
    ECS --> CoreAPI
    ECS --> BlobStorage
    ECS --> ChemParser
    ECS --> ChemProps
    ECS --> ReactionParser
    ECS --> CrystalParser
    ECS --> SpectraParser
    ECS --> Imaging
    ECS --> OfficeProc
    ECS --> MetaProc
    ECS --> Indexing
    
    CoreAPI --> DocDB
    CoreAPI --> MSK
    BlobStorage --> DocDB
    BlobStorage --> S3
    BlobStorage --> MSK
    
    ChemParser --> MSK
    ChemParser --> BlobStorage
    ChemProps --> MSK
    ReactionParser --> MSK
    CrystalParser --> MSK
    SpectraParser --> MSK
    Imaging --> MSK
    OfficeProc --> MSK
    MetaProc --> DocDB
    MetaProc --> MSK
    Indexing --> OpenSearch
    Indexing --> MSK
    
    CoreAPI --> Redis
    BlobStorage --> Redis
    
    ECS --> CW
    ECS --> XRay
```

## Event-Driven Architecture Flow

```mermaid
sequenceDiagram
    participant User
    participant CoreAPI
    participant BlobStorage
    participant Kafka
    participant Parser
    participant MetaProc
    participant Indexing
    participant OpenSearch
    
    User->>CoreAPI: Upload File (POST /api/v2/files)
    CoreAPI->>BlobStorage: Store File
    BlobStorage->>S3: Upload to S3
    BlobStorage->>Kafka: Publish FileCreated Event
    CoreAPI->>User: 202 Accepted
    
    Kafka->>Parser: FileCreated Event
    Parser->>BlobStorage: Fetch File
    Parser->>Parser: Parse File
    Parser->>Kafka: Publish FileParsed Event
    
    Kafka->>MetaProc: FileParsed Event
    MetaProc->>MetaProc: Extract Metadata
    MetaProc->>Kafka: Publish MetadataExtracted Event
    
    Kafka->>Indexing: MetadataExtracted Event
    Indexing->>OpenSearch: Index Document
    Indexing->>Kafka: Publish EntityIndexed Event
    
    User->>CoreAPI: Search (GET /api/v2/search?q=...)
    CoreAPI->>OpenSearch: Query
    OpenSearch->>CoreAPI: Results
    CoreAPI->>User: 200 OK
```

## Multi-AZ Deployment Architecture

```mermaid
graph TB
    subgraph "AWS Region: us-east-1"
        subgraph "Availability Zone: us-east-1a"
            subgraph "Public Subnet 1a"
                NAT1[NAT Gateway 1]
                ALB1[ALB Node 1]
            end
            subgraph "Private Subnet 1a"
                ECS1[ECS Tasks 1]
            end
            subgraph "Isolated Subnet 1a"
                DocDB1[DocumentDB Instance 1]
                Redis1[Redis Node 1]
            end
        end
        
        subgraph "Availability Zone: us-east-1b"
            subgraph "Public Subnet 1b"
                NAT2[NAT Gateway 2]
                ALB2[ALB Node 2]
            end
            subgraph "Private Subnet 1b"
                ECS2[ECS Tasks 2]
            end
            subgraph "Isolated Subnet 1b"
                DocDB2[DocumentDB Instance 2]
                Redis2[Redis Node 2]
            end
        end
        
        Internet[Internet] --> ALB1
        Internet --> ALB2
        ALB1 --> ECS1
        ALB2 --> ECS2
        ECS1 --> DocDB1
        ECS1 --> DocDB2
        ECS2 --> DocDB1
        ECS2 --> DocDB2
        ECS1 --> Redis1
        ECS2 --> Redis2
    end
```

## Scalability Architecture

```mermaid
graph LR
    subgraph "Auto-Scaling Triggers"
        CPU[CPU > 70%]
        Memory[Memory > 80%]
        Queue[Queue Depth > 100]
        Requests[Request Count > 1000/min]
    end
    
    subgraph "ECS Auto-Scaling"
        Min[Min: 2 Tasks]
        Desired[Desired: Auto]
        Max[Max: 20 Tasks]
    end
    
    subgraph "Load Distribution"
        ALB[Application Load Balancer]
        Task1[Task 1]
        Task2[Task 2]
        TaskN[Task N]
    end
    
    CPU --> ECS
    Memory --> ECS
    Queue --> ECS
    Requests --> ECS
    
    ECS --> Min
    ECS --> Desired
    ECS --> Max
    
    ALB --> Task1
    ALB --> Task2
    ALB --> TaskN
```

## Caching Architecture

```mermaid
graph TB
    User[User Request]
    
    subgraph "Layer 1: CloudFront CDN"
        CF[CloudFront]
        CFHit{Cache Hit?}
    end
    
    subgraph "Layer 2: ElastiCache Redis"
        Redis[Redis Cache]
        RedisHit{Cache Hit?}
    end
    
    subgraph "Layer 3: Application Cache"
        AppCache[Quarkus Cache]
        AppHit{Cache Hit?}
    end
    
    subgraph "Origin"
        API[API Service]
        DB[(DocumentDB)]
    end
    
    User --> CF
    CF --> CFHit
    CFHit -->|Hit| User
    CFHit -->|Miss| Redis
    Redis --> RedisHit
    RedisHit -->|Hit| CF
    RedisHit -->|Miss| AppCache
    AppCache --> AppHit
    AppHit -->|Hit| Redis
    AppHit -->|Miss| API
    API --> DB
    DB --> API
    API --> AppCache
    AppCache --> Redis
    Redis --> CF
    CF --> User
```

## Disaster Recovery Architecture

```mermaid
graph TB
    subgraph "Primary Region: us-east-1"
        subgraph "Production"
            ProdECS[ECS Services]
            ProdDB[(DocumentDB)]
            ProdS3[(S3 Buckets)]
        end
        
        subgraph "Backups"
            DBSnapshots[DocumentDB Snapshots<br/>Daily @ 2 AM UTC]
            S3Replication[S3 Cross-Region<br/>Replication]
        end
    end
    
    subgraph "Secondary Region: us-west-2"
        subgraph "DR Infrastructure"
            DRECS[ECS Services<br/>Standby]
            DRDB[(DocumentDB<br/>Read Replica)]
            DRS3[(S3 Buckets<br/>Replicated)]
        end
    end
    
    ProdDB -->|Automated Snapshots| DBSnapshots
    ProdS3 -->|Cross-Region Replication| DRS3
    DBSnapshots -.->|On Failover| DRDB
    ProdECS -.->|On Failover| DRECS
```

## Security Architecture

```mermaid
graph TB
    User[User]
    
    subgraph "Edge Security"
        WAF[AWS WAF]
        CF[CloudFront]
    end
    
    subgraph "Authentication"
        Cognito[Amazon Cognito]
        APIGW[API Gateway<br/>+ Authorizers]
    end
    
    subgraph "Network Security"
        VPC[VPC]
        SG[Security Groups]
        NACL[Network ACLs]
    end
    
    subgraph "Data Security"
        KMS[AWS KMS]
        Encrypt[Encryption at Rest]
        TLS[TLS in Transit]
    end
    
    subgraph "Monitoring"
        GuardDuty[GuardDuty]
        SecurityHub[Security Hub]
        CloudTrail[CloudTrail]
    end
    
    User --> WAF
    WAF --> CF
    CF --> Cognito
    Cognito --> APIGW
    APIGW --> VPC
    VPC --> SG
    VPC --> NACL
    VPC --> KMS
    KMS --> Encrypt
    VPC --> TLS
    VPC --> GuardDuty
    GuardDuty --> SecurityHub
    VPC --> CloudTrail
```

## Service Integration Patterns

```mermaid
graph LR
    subgraph "Synchronous Communication"
        Client[Client]
        APIGW[API Gateway]
        ALB[ALB]
        Service[Microservice]
    end
    
    subgraph "Asynchronous Communication"
        Service1[Service 1]
        Kafka[MSK Serverless]
        Service2[Service 2]
        Service3[Service 3]
    end
    
    subgraph "Service Discovery"
        ServiceA[Service A]
        CloudMap[AWS Cloud Map]
        ServiceB[Service B]
    end
    
    Client --> APIGW
    APIGW --> ALB
    ALB --> Service
    
    Service1 -->|Publish| Kafka
    Kafka -->|Subscribe| Service2
    Kafka -->|Subscribe| Service3
    
    ServiceA --> CloudMap
    CloudMap --> ServiceB
```

## Observability Architecture

```mermaid
graph TB
    subgraph "Application Layer"
        Services[Microservices]
    end
    
    subgraph "Logging"
        Services -->|Structured Logs| CloudWatch[CloudWatch Logs]
        CloudWatch --> LogGroups[Log Groups<br/>per Service]
    end
    
    subgraph "Metrics"
        Services -->|Custom Metrics| CloudWatchMetrics[CloudWatch Metrics]
        CloudWatchMetrics --> Dashboards[Dashboards]
        CloudWatchMetrics --> Alarms[Alarms]
    end
    
    subgraph "Tracing"
        Services -->|Traces| XRay[X-Ray]
        XRay --> ServiceMap[Service Map]
        XRay --> Traces[Trace Analysis]
    end
    
    subgraph "Alerting"
        Alarms --> SNS[SNS Topics]
        SNS --> Email[Email]
        SNS --> PagerDuty[PagerDuty]
        SNS --> Slack[Slack]
    end
```

