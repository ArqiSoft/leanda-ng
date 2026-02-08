# Leanda.io Comprehensive Modernization and AWS-Native Rewrite Plan

## About Leanda.io

### What is it?

The data is essential for science. Data repositories have existed for decades and have been well-supported by various grants, yet they are merely file stores or highly specialized single-purpose databases.

Leanda.io is an extensible open science data repository. Leanda.io allows users to consume, process, visualize and analyze different data types, formats and data volumes. Its microservice based architecture is designed so that new business domain services can be added without the need to modify the entire system. Currently a large set of modules is implemented providing general content management as well as scientific data handling. Our goal is to address functional, architecture and UX/UX deficiencies of other systems and make Leanda.io the gold standard for the Open Science community. Leanda.io's vision is to be a tool based on open standards for improving data sharing and collaboration with a potential impact across many scientific areas. There is a clear disconnect between domain-specific databases, publishers’ data repositories and semantic web knowledge-bases. Leanda.io provides a basic data processing pipeline. Leanda.io allows real-time data curation and supports ontologies-based properties assignment with subsequent complex searches. Leanda’s deposition pipeline includes a data mining stage which allows text-mining and data conversion on the fly when a new file is deposited. Leanda.io security model supports private, shared and public data. Leanda.io, by incorporating data mining and a curation pipeline on top of integration with multiple data sources, provides a platform for rapid composition of machine learning training data sets for immediate modeling.

### Data Domains and Formats

Leanda.io supports various formats and is able to convert between them seamlessly at time of import or export. At the moment the following data domain services are in place:

- Generic image files such as PNG, GIF, etc
- PDF files
- Office files (MS Office as well as Open Office are supported)
- Tabular data such as CSV and TSV
- Chemical structures (SDF, MOL etc)
- Chemical reactions (RXN)
- Crystals
- Microscopy files
- Machine learning models

### Machine Learning

A machine learning (ML) framework is embedded into Leanda.io and can be used as an API, standalone tool or can be integrated in a new software as an autonomous module. Leanda.io provides a number of pipelines simplifying data science workflows used in research and drug discovery starting from data import and curation and finishing with the predictive models training, evaluation and application. Trained models can be shared with other users or made public.

### Data Curation and Annotation

Leanda.io was designed to support multiple ways of data acquisition, conversion, real-time automated and manual data curation, annotation and analysis. The system can extract the metadata from the raw files automatically. In addition to automatic metadata extraction Leanda.io provides ways to add hierarchical categories to the data, tag, and to assign additional metadata types.

## Executive Summary

This comprehensive plan consolidates analyses of Leanda.io's current state, modernization needs, GitHub repositories, and technology trends as of December 24, 2025. It proposes a complete rewrite to an AWS-native architecture, unifying the polyglot microservices stack, embedding cutting-edge AI/ML capabilities, and optimizing for stability, cost-effectiveness, maintainability, and evolvability. The rewrite addresses technical debt, enhances open science features like real-time curation and ML workflows, and leverages AWS managed services for reduced operational overhead. Estimated timeline: 10-15 months, with 40-60% cost savings through serverless computing and managed infrastructure.

## Current State Analysis

### Modernization Plan Review

The provided modernization plan outlines a 12-month phased approach to mitigate technical debt in Leanda.io's microservices architecture, which uses CQRS/ES patterns with RabbitMQ for communication, MongoDB 3.6/EventStore 4.0.2/Redis 4 for data stores, Angular 9 frontend, and backends in .NET Core 3.1, Java 8/Spring Boot 2.0.0.RC1, and Python.

- **Critical Issues**: Security vulnerabilities from outdated dependencies (e.g., CVEs in Spring Boot RC1, EOL .NET Core 3.1/Angular 9/MongoDB 3.6); obsolescence (Protractor/Travis CI deprecated); inconsistent patterns; limited test coverage.
- **Phased Strategy**:
  - Phase 1 (Months 1-3): Security-focused upgrades (.NET 8, Java 17/Spring Boot 3.1, Angular 17, database LTS versions).
  - Phase 2 (Months 4-5): Testing (Playwright/Cypress) and CI/CD (GitHub Actions; CI/CD postponed until full migration is complete).
  - Phase 3 (Months 6-8): Observability (OpenTelemetry), API enhancements (OpenAPI 3.0), dependency management.
  - Phase 4 (Months 9-10): Performance/scalability optimizations (caching, indexing).
  - Phase 5 (Months 11-12): Developer experience (Docker Compose, documentation).
- **Approach**: Incremental, service-by-service migrations with feature flags, parallel running, backups, and staging tests. Success metrics include zero critical vulnerabilities, <5% performance regression, 99.9% uptime.
- **Limitations**: Retains polyglot stack and self-managed components, limiting adoption of 2025 trends like AI-native infrastructure and serverless. A full rewrite enables unification and AWS optimizations.

### GitHub Organization Analysis (<https://github.com/ArqiSoft>)

The ArqiSoft organization hosts 28 public repositories, confirming the fragmented, polyglot microservices structure with low community engagement (0 stars/forks/issues in most repos). Key insights:

- **Core Repos**: leanda-core (C#, 2021), leanda-ui (JavaScript/Angular, updated Dec 23, 2025), leanda-test (TypeScript, 2019), leanda-cli (Python, 2020).
- **Domain Services**: chemical-file-parser-service (C#, 2020), chemical-properties-service (Java, 2020), spectra-file-parser-service (Java, 2020), crystal-file-parser-service (Java, 2019), reaction-file-parser-service (C#, 2020), office-file-processor-service (Java, 2020), imaging-service (Java, 2020), web-importer-service (Java, 2020), microscopy-metadata-service (Java, 2023), chemical-export-service (Java, 2020).
- **ML and Support**: ml-services/ml-text-mining (Python, 2019), metadata-processing-service/indexing-service/blob-store (C#, 2020-2023), system-java/system-dotnet (Java/C#, 2018-2019), configuration (Shell, 2024).
- **Observations**: Sparse updates (mostly pre-2021), no active PRs/issues, separate repos per service hinder maintenance. Indicates stalled development, underscoring need for consolidation and revival through modernization.

## Technology and Cloud Trends Analysis (as of December 24, 2025)

Based on 2025 trends from AWS re:Invent, Gartner reports, and industry benchmarks:

- **Languages/Frameworks**: .NET 10 LTS, Java 25 LTS, Angular 21 (zoneless, Signal Forms, AI tooling). Microservices favor Quarkus/Spring Boot 3.3+ for efficiency, FastAPI/PyTorch 3.0+ for ML.
- **Databases**: MongoDB 8.2 (vector search), KurrentDB 25 (event sourcing), Redis 8.4. Trends: AI-integrated DBs for semantic queries in scientific data.
- **Technologies**: Kafka over RabbitMQ; Keycloak 26+ for auth; Playwright for testing; GitHub Actions for CI/CD (CI/CD postponed until full migration); OpenTelemetry for observability.
- **Cloud Trends**: AI/ML growth (LLMOps, agentic AI); serverless/edge computing; hybrid/multi-cloud to $723B market; FinOps/sustainability. For repositories: Embedded AI for curation, vector search, MLOps for model sharing.
- **AWS-Specific**: Leads DSML (SageMaker/Bedrock); event-driven with data triggers (EventBridge); data lakes (S3/Glue/Athena); security (GuardDuty/Macie). 2025 updates: Bedrock AgentCore for life sciences, EMR enhancements for scientific computing.

An AWS-native shift aligns with Leanda.io's needs, replacing self-managed tools for managed equivalents, enabling 30-50% cost reductions and AI enhancements.

## Proposed Rewrite Plan

A greenfield rewrite to AWS-native, run parallel to the existing system for gradual migration via feature flags/A/B testing. Unify polyglot stack (reduce to Java/Python), consolidate repos (monorepo for core), embed AI for curation/ML. Timeline: 10-15 months.

### Key Principles

- **Cutting Edge**: Native AI (Bedrock LLMs for annotations, SageMaker for workflows).
- **Stable**: Managed services (99.99% SLAs), multi-AZ resilience.
- **Cost-Effective**: Serverless (pay-per-use), FinOps tools.
- **Easy to Maintain/Evolve**: IaC (CDK), modular plugins, auto-scaling.

### Implementation Phases

1. **Foundation (Months 1-3)**: Redesign with ADRs; rewrite core in Quarkus on Lambda; set up VPC, Cognito, S3/DocumentDB.
2. **ML & Data (Months 4-6)**: Migrate Python ML to SageMaker; integrate Bedrock/Glue for curation/ETL.
3. **Frontend & Domains (Months 7-9)**: Angular 21 on Amplify; domain services as Lambdas.
4. **Optimization & Security (Months 10-11)**: Caching (ElastiCache), GuardDuty; performance testing.
5. **Migration & Deployment (Months 12-15)**: Data migration scripts; parallel run, rollout with 99.9% uptime.

### Risk Mitigation & Benefits

- **Risks**: Vendor lock-in (mitigate with abstractions); downtime (Blue/Green deploys); skills gaps (training).
- **Benefits**: 40-60% ops/cost reduction; AI-driven innovation for open science; easier evolution. Metrics: <500ms responses, zero crit vulns, 25% faster dev cycles.

## Detailed AWS-Native Architecture

Adopts event-driven microservices with CQRS/ES, enhanced by AWS data triggers. Follows AWS Well-Architected Framework 2025.

### Text-Based Architecture Diagram (ASCII Art)

```
[Users/Apps] --> Amazon API Gateway (OIDC/Cognito Auth) --> [Frontend: Amplify/Angular 21 App]
                                                     |
                                                     v
[Data Ingestion] --> AWS Lambda (File Uploads/Parsers) --> Amazon S3 (Raw Storage) --> Amazon EventBridge (Triggers)
                                                     |                                       |
                                                     v                                       v
[ML Pipelines] <-- Amazon SageMaker (Training/Endpoints) <-- Amazon Glue (ETL/Data Mining) --> Amazon Bedrock (GenAI Curation/Annotations)
                                                     |                                       |
                                                     v                                       v
[Data Stores] <-- Amazon DocumentDB (Metadata/NoSQL) <-- Amazon OpenSearch (Vector Search/Queries) --> Amazon Timestream (Event Sourcing)
                                                     |                                       |
                                                     v                                       v
[Microservices] <-- ECS Fargate/App Runner (Domain Services: Chemical, Spectra, etc.) --> Amazon MSK (Kafka for Streaming)
                                                     |
                                                     v
[Observability] <-- Amazon CloudWatch/X-Ray (Monitoring/Tracing) <-- AWS IAM/GuardDuty (Security)
                                                     |
                                                     v
[CI/CD & IaC] <-- AWS CodePipeline/CDK (Deployment) <-- Amazon ECR (Containers)
```

### Components

- **Networking/Security**: Multi-AZ VPC, PrivateLink; Cognito/IAM/KMS; Macie/GuardDuty/WAF.
- **Compute**: Quarkus/Java 25 on Lambda/Fargate; Python 3.13 on SageMaker.
- **Storage/Management**: S3 (tiering), DocumentDB (vectors), Timestream, ElastiCache, OpenSearch, Athena/Glue.
- **ML/AI**: SageMaker Pipelines, Bedrock AgentCore, Comprehend/Rekognition/Textract.
- **Event Processing**: EventBridge/MSK, Step Functions.
- **Frontend/API**: Amplify, API Gateway (OpenAPI).
- **Observability**: CloudWatch/X-Ray/OpenTelemetry.
- **CI/CD/IaC**: CodePipeline, CDK.
- **Scalability/Resilience/Sustainability**: Auto-scaling, Fault Injection, green regions.

This plan revitalizes Leanda.io as a leader in open science, fully leveraging AWS for innovation and efficiency.
