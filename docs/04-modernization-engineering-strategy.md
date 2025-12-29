# Leanda.io Comprehensive Modular Redesign Strategy

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

## Analysis of the Existing Modernization Plan

As an experienced data and software engineering lead with over 20 years in building scalable microservices systems for scientific and enterprise applications, I begin by analyzing the provided modernization plan. This plan is a solid foundation for addressing immediate technical debt but falls short in long-term evolvability and modernization to 2025 standards.

### Strengths

- **Phased Approach**: The 12-month timeline with five phases (Foundation & Security, Testing & CI/CD, Architecture & Patterns, Performance & Scalability, Developer Experience) prioritizes critical security updates first, aligning with best practices like "secure by design" and incremental delivery.
- **Comprehensive Coverage**: It targets key pain points—outdated stacks (.NET Core 3.1 to .NET 8, Java 8/Spring Boot 2.0.0.RC1 to Java 17/Spring Boot 3.1, Angular 9 to 17, databases to LTS versions), deprecated tools (Protractor to Playwright, Travis CI to GitHub Actions), and enhancements (OpenTelemetry for observability, OpenAPI for APIs).
- **Risk Mitigation**: Emphasizes backups, rollback plans, staging environments, and success metrics (e.g., zero critical vulnerabilities, 99.9% uptime), which reflect mature engineering practices.
- **Quick Wins**: Immediate actions like dependency updates and security audits provide early value.

### Weaknesses

- **Retention of Polyglot Stack**: Maintaining C#, Java, Python, and TypeScript increases cognitive load, maintenance costs, and integration complexity. A unified language (e.g., Java for backend, Python for ML) would improve consistency.
- **Limited Cloud-Native Focus**: While it updates infrastructure (Docker, databases), it doesn't fully embrace serverless, AI-native trends, or managed services, missing opportunities for cost optimization and scalability in variable scientific workloads.
- **Fragmented Implementation**: Service-by-service upgrades risk inconsistencies; lacks emphasis on Domain-Driven Design (DDD) for modular boundaries.
- **Testing and Validation Gaps**: While migrating to Playwright/Cucumber, it doesn't mandate Test-Driven Development (TDD), Behavior-Driven Development (BDD), or comprehensive coverage (unit, integration, end-to-end, load testing).
- **Evolvability**: No explicit focus on extensibility patterns like plugin architectures or API-first design, crucial for adding new data domains.

Overall, the plan patches the system effectively but doesn't position Leanda.io as cutting-edge. A modular redesign is needed to unify, scale, and innovate.

## Analysis of the GitHub Organization Repositories

The ArqiSoft organization (<https://github.com/ArqiSoft>) contains 28 public repositories, revealing a fragmented, outdated codebase with low activity. This analysis is based on repository metadata, commit histories, and structures as of December 24, 2025.

### Key Observations

- **Fragmentation**: Each microservice is in a separate repo (e.g., leanda-core in C#, chemical-properties-service in Java, ml-services in Python), leading to duplicated CI/CD setups, inconsistent versioning, and hard-to-manage dependencies. A monorepo or grouped structure (e.g., core, domains, ml) would streamline collaboration.
- **Outdated Code**: Most repos last updated pre-2021 (e.g., crystal-file-parser-service in 2019, spectra-file-parser-service in 2020), with vulnerabilities from old dependencies. Recent activity is minimal (e.g., leanda-ui updated Dec 23, 2025, possibly a minor fix).
- **Polyglot Nature**: C# for core/persistence (leanda-core, metadata-processing-service), Java for parsers/processors (chemical-file-parser-service, office-file-processor-service), Python for ML/CLI (ml-text-mining, leanda-cli), TypeScript for UI/testing (leanda-ui, leanda-test). This diversity complicates builds and deployments.
- **Quality Issues**: Limited READMEs, no ADRs (Architecture Decision Records), sparse tests (leanda-test uses deprecated Protractor), and no modern CI (some .travis.yml files). No issues/PRs indicate stalled community/development.
- **Opportunities**: Domain-specific repos (e.g., reaction-file-parser-service) align with modular extensions. Configuration repo (Shell, updated 2024) could seed IaC efforts.

This setup risks security holes and hinders scalability. Redesign should consolidate repos, enforce standards, and integrate modern tools.

## Proposed Step-by-Step Modular Redesign Strategy

Drawing from best engineering practices (e.g., DDD for bounded contexts, Twelve-Factor App principles, CI/CD pipelines, TDD/BDD, observability-first), I propose a modular redesign as a greenfield rewrite with parallel migration. This ensures zero-downtime rollout, focusing on core functionality first. Adopt AWS-native for managed services, unifying backend in Java 25 LTS/Quarkus (fast, cloud-native), Python 3.13 for ML, Angular 21 for UI.

### Guiding Principles

- **Modularity**: Use DDD to define bounded contexts (e.g., Core Management, Data Ingestion, ML Pipelines, Domain Services).
- **Best Practices**: API-first design, IaC with AWS CDK, TDD/BDD for >80% coverage, GitOps for deployments, security scanning (Snyk), observability (OpenTelemetry).
- **Repo Structure**: Monorepo for core/shared, separate for ML/UI to balance collaboration and isolation.
- **Timeline**: 12-18 months, agile sprints (2-week), with MVP releases.
- **Team**: Cross-functional (devs, data engineers, QA, DevOps); training on new stacks.

### Phased Approach

#### Phase 0: Planning and Assessment (Months 1-2)

- **Objectives**: Baseline current system, define roadmap.
- **Steps**:
  1. Audit repos: Use tools like SonarQube for code quality, Dependabot for vulnerabilities.
  2. Map domains: Identify bounded contexts (e.g., Ingestion, Curation, Search, ML).
  3. Define non-functionals: SLAs (99.9% uptime), scalability (auto-scale for bursts), security (zero-trust).
  4. Select stack: Java/Quarkus for services, Python/FastAPI for ML, AWS (Lambda, SageMaker, DocumentDB).
  5. Create ADRs: Document decisions (e.g., monorepo vs. multi-repo).
- **Best Practices**: Stakeholder workshops, risk matrix, success metrics (e.g., audit report).
- **Deliverables**: Roadmap, architecture diagrams, consolidated monorepo setup.

#### Phase 1: Core Functionality Redesign (Months 3-6)

- **Objectives**: Build foundational microservices with essential features.
- **Steps**:
  1. Rewrite core (leanda-core): API gateway, persistence, auth (Cognito).
  2. Implement ingestion/curation: Lambda for file uploads/parsers, Glue for ETL, Bedrock for AI annotations.
  3. Unify domains: Modular plugins (e.g., chemical/spectra parsers as Quarkus modules).
  4. Integrate event-driven: EventBridge for triggers, MSK for streaming.
- **Best Practices**: TDD for units, BDD for behaviors; feature flags for toggles; pair programming.
- **Testing/Validation**: Unit tests (JUnit/Pytest), integration tests (Postman for APIs); validate against sample datasets (e.g., SDF files).
- **Deliverables**: MVP core deployable to staging; 70% code coverage.

#### Phase 2: ML and Advanced Features (Months 7-9)

- **Objectives**: Embed ML pipelines and extensibility.
- **Steps**:
  1. Rewrite ML services: SageMaker for training/endpoints, integrate with curation (e.g., auto-dataset composition).
  2. Add search/annotation: OpenSearch for vector queries, ontologies via Bedrock.
  3. Frontend: Angular 21 on Amplify, with real-time WebSockets.
- **Best Practices**: MLOps (SageMaker Pipelines), versioned models, A/B testing for features.
- **Testing/Validation**: ML-specific tests (accuracy benchmarks), end-to-end (Playwright for UI flows); load testing (k6) for scalability.
- **Deliverables**: Functional ML workflows; beta release to select users.

#### Phase 3: Comprehensive Testing and Validation (Months 10-12)

- **Objectives**: Ensure reliability and performance.
- **Steps**:
  1. Full test suite: Unit/integration/E2E, security (penetration testing), performance (response times <500ms).
  2. Data migration: Scripts from MongoDB to DocumentDB; validate integrity.
  3. Chaos engineering: AWS Fault Injection for resilience.
- **Best Practices**: CI/CD with CodePipeline (matrix builds, auto-deploys); blue/green deployments.
- **Testing/Validation**: Coverage >85%; user acceptance testing (UAT) with scientists; metrics validation (uptime, vuln scans).
- **Deliverables**: Production-ready system; migration guide.

#### Phase 4: Deployment, Monitoring, and Iteration (Months 13-18)

- **Objectives**: Rollout, optimize, evolve.
- **Steps**:
  1. Parallel run: Route traffic gradually via API Gateway.
  2. Monitor: CloudWatch/X-Ray for anomalies; FinOps for costs.
  3. Iterate: Add new domains (e.g., via plugins); community contributions.
- **Best Practices**: GitOps, post-mortems, continuous feedback loops.
- **Testing/Validation**: Ongoing monitoring, A/B metrics comparison.
- **Deliverables**: Full production; documentation, training materials.

This strategy transforms Leanda.io into a modular, scalable platform, reducing debt while enabling innovation.
