**Leanda.io** is an extensible open science data repository that enables users to consume, process, visualize, and analyze diverse scientific data types, formats, and volumes. Unlike traditional file stores or narrow-purpose databases, it features a modular microservices architecture allowing seamless addition of new domain-specific services without core system changes.

The platform addresses key deficiencies in existing open science tools by providing:

- Real-time automated + manual data curation
- Ontology-based property assignment and complex semantic searches
- On-the-fly data mining, text extraction, and format conversion during deposition
- Granular security model (private / shared / public data)
- Rapid creation of ML training datasets from integrated sources and processed data

### Supported Data Domains and Formats

Leanda.io handles a wide range of scientific formats with automatic import/export conversions:

- Generic images (PNG, GIF, TIFF…)
- Documents (PDF, MS Office, OpenOffice)
- Tabular data (CSV, TSV, Excel)
- Chemical structures (SDF, MOL, SMILES…)
- Chemical reactions (RXN)
- Crystallographic data
- Microscopy imaging files
- Machine learning models & weights

### Machine Learning Integration

An embedded ML framework serves as API, standalone component, or integrable module. It streamlines full research & drug discovery pipelines:

- Data import → automated curation & annotation
- Feature extraction & dataset composition
- Model training, evaluation, versioning & sharing
- Predictive application on new deposited data

### Data Curation and Annotation

The system supports multiple acquisition paths with strong emphasis on quality:

- Automatic metadata extraction from raw files
- Hierarchical categorization & tagging
- Ontology-driven semantic annotation
- Manual correction & enrichment workflows
- Real-time updates visible across the platform

## Conversation Analysis – Current State & Modernization Needs

The conversation reveals a system suffering from **severe technical debt** after years of limited maintenance:

- Extremely outdated stack (.NET Core 3.1, Java 8/Spring Boot RC1, Angular 9, MongoDB 3.6, EventStore 4.x, Redis 4)
- Heavy polyglot fragmentation (C# core + Java parsers + Python ML)
- 28 separate GitHub repositories with almost no activity since 2020–2021
- No modern observability, CI/CD (CI/CD postponed until full migration), testing, or security posture
- Classic microservices but with high operational burden and scaling limitations

Previous proposals evolved from incremental modernization → full rewrite → AWS-native microservices → lakehouse thinking.

**Key 2025 reality check** (as of late December 2025):  
AWS has strongly consolidated its analytics & AI story around the **Amazon SageMaker Lakehouse** architecture (announced/expanded heavily in 2024–2025), which combines:

- Open lakehouse built on Apache Iceberg tables on S3 / S3 Tables
- Unified catalog & governance via AWS Glue Data Catalog + Lake Formation
- Zero-ETL integrations, vector search, fine-grained access
- Seamless consumption by SageMaker AI/ML, Athena, EMR, OpenSearch, Redshift, Bedrock, QuickSight…

This direction is much more mature, opinionated, and future-proof than a pure custom microservices + S3 + Glue approach.

## Recommended Target Architecture – Modern Open Science Lakehouse on AWS (December 2025)

### Core Architectural Paradigm

**SageMaker Lakehouse + Apache Iceberg + Generative AI curation pipeline**

Main principles:

- Single source of truth = governed Apache Iceberg tables on Amazon S3 / S3 Tables
- Open table format enables ACID, time-travel, schema evolution, efficient updates
- Unified governance & catalog → AWS Lake Formation + Glue Data Catalog
- Serverless-first compute → minimal ops, auto-scaling
- Deep AI integration from ingestion to consumption
- Open standards compatibility → future-proof against vendor lock-in

### High-Level Architecture Layers

```
[Scientific Community & Instruments]
          ↓          (HTTPS / API / CLI / direct S3 multipart)
Amazon API Gateway + Amazon Cognito (OIDC + ORCID integration)
          ↓
[Ingestion & Immediate Processing]
  AWS Lambda / Step Functions / AppFlow (zero-ETL connectors)
          ↓
Amazon S3 Landing Zone (raw files – partitioned by domain / date / submitter)
          ↓   EventBridge triggers
[Real-time Curation & Enrichment Pipeline]
  AWS Glue Streaming + Bedrock Agents / Claude 3.x Sonnet
  → Automatic metadata extraction (Textract + Comprehend)
  → Ontology mapping & semantic tagging (Bedrock + custom prompts)
  → Format conversion / standardization (Glue + RDKit / OpenBabel)
          ↓
[Curated Zone – Apache Iceberg Tables]
  S3 + Glue Catalog + Lake Formation permissions
  Tables: raw_metadata, chemical_structures, reactions, crystals, microscopy, tabular_data, ml_models, annotations
          ↓
[Search & Discovery]
  Amazon OpenSearch (vector + lexical search)
  → Embeddings from Bedrock Titan / Cohere
  → Ontology-aware semantic search
          ↓
[Analytics & Exploration]
  Amazon Athena (SQL on Iceberg)
  Amazon Redshift Spectrum (if heavy SQL analytics needed)
  QuickSight (dashboards/visualizations)
          ↓
[Machine Learning & Predictive Modeling]
  Amazon SageMaker Unified Studio
  → Feature Store / Processing Jobs / Pipelines
  → Training on Iceberg tables
  → Model Registry → endpoints / batch inference
  → Generative AI agents for dataset composition & hypothesis generation
          ↓
[Consumption & Collaboration]
  - Public/private sharing via Lake Formation data cells
  - API layer for programmatic access
  - Export formats via Glue jobs / Lambda
```

### Key Design Decisions & Rationale (2025 best practices)

| Layer / Component               | Recommended Technology                          | Rationale (2025 context)                                                                 |
|---------------------------------|-------------------------------------------------|-------------------------------------------------------------------------------------------|
| Storage foundation              | Amazon S3 + S3 Tables + Apache Iceberg          | Open table format + ACID + time travel + schema evolution; native in SageMaker Lakehouse |
| Governance & Catalog            | AWS Lake Formation + Glue Data Catalog          | Fine-grained permissions, data lineage, business glossary, sharing                       |
| Ingestion                       | Lambda + AppFlow + EventBridge                  | Serverless, zero-ETL from many scientific sources                                         |
| Real-time curation              | Glue Streaming + Bedrock Agents                 | Agentic AI for automated metadata/ontology/enrichment                                     |
| Vector & semantic search        | Amazon OpenSearch + Bedrock embeddings          | Hybrid lexical + semantic search crucial for scientific discovery                         |
| SQL Analytics                   | Amazon Athena + Iceberg                         | Serverless, pay-per-query, excellent for exploratory science                              |
| ML Development                  | SageMaker Unified Studio + Processing Jobs      | Integrated notebook + pipeline + governance experience                                    |
| Model Serving                   | SageMaker Endpoints / Batch Transform           | Auto-scaling inference for predictive services                                            |
| Security & Compliance           | Lake Formation + Cognito + KMS + GuardDuty      | Cell-level access, audit, encryption, threat detection                                    |
| Cost optimization               | S3 Intelligent-Tiering + Savings Plans + Glue Serverless | Pay-per-use dominant for variable academic workloads                                      |

### Recommended Migration & Evolution Path

1. **Phase 0 (1–2 months)** — Landing zone + governance foundation  
   → S3 zones, Lake Formation setup, Iceberg catalog bootstrapping

2. **Phase 1 (3–5 months)** — Ingestion + curation pipeline  
   → Migrate parsers → Glue/Bedrock agents, build real-time enrichment

3. **Phase 2 (4–6 months)** — Core lakehouse + search  
   → Iceberg tables for main domains, OpenSearch indexing

4. **Phase 3 (5–8 months)** — ML & analytics layer  
   → SageMaker integration, pipelines, model registry

5. **Phase 4 (ongoing)** — Public sharing, extensibility, community plugins  
   → Lake Formation sharing, plugin SDK for new domains

This architecture positions **Leanda.io** as one of the most modern, AI-native open science data platforms in late 2025 — fully leveraging AWS's latest lakehouse investments while keeping the system open, extensible, and scientifically powerful.
