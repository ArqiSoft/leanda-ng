# Leanda.io - Open Science Data Repository Platform

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Leanda.io** is an extensible open science data repository that enables researchers to consume, process, visualize, and analyze diverse scientific data types, formats, and volumes. Unlike traditional file stores or narrow-purpose databases, it features a modular microservices architecture designed for seamless extension with new domain-specific services.

## What is Leanda.io?

Leanda.io addresses key deficiencies in existing open science tools by providing:

- **Real-time automated + manual data curation** with AI-powered metadata extraction
- **Ontology-based property assignment** and complex semantic searches
- **On-the-fly data mining**, text extraction, and format conversion during deposition
- **Granular security model** supporting private, shared, and public data
- **Rapid ML training dataset composition** from integrated sources and processed data
- **Embedded ML framework** for research and drug discovery pipelines

### Supported Data Domains and Formats

Leanda.io handles a wide range of scientific formats with automatic import/export conversions:

- Generic images (PNG, GIF, TIFF, BMP)
- Documents (PDF, MS Office, OpenOffice)
- Tabular data (CSV, TSV, Excel)
- Chemical structures (SDF, MOL, SMILES, CDX)
- Chemical reactions (RXN)
- Crystallographic data (CIF)
- Spectra (JDX)
- Microscopy imaging files
- Machine learning models & weights

## Current Phase

**⚠️ IMPORTANT: This project is currently in the planning/design phase. NOTHING is runnable yet.**

Infrastructure is designed, documentation is comprehensive, and contracts are defined, but **NO code is implemented or runnable yet**. The ~92% completion refers to design/planning work, not implementation.

See [Project Summary Report](./docs/journey/01-journey-week-1-report.md) for detailed progress.

## Quick Start

**⚠️ NOTHING is runnable yet - this is a planning/design phase.**

This project is currently in the planning and design phase. Infrastructure is designed, documentation is comprehensive, and contracts are defined, but **no code is implemented or runnable yet**. Implementation will begin after the design phase is complete.

### Prerequisites (For Future Implementation)

When implementation begins, you will need:

- **Java 21 LTS** (for backend services)
- **Python 3.12+** (for ML services)
- **Node.js 20+** (for frontend and CDK)
- **Docker & Docker Compose** (for local development)
- **AWS CLI v2** (for infrastructure deployment)

### Current Status

- ✅ Infrastructure design complete (AWS CDK stacks designed)
- ✅ Documentation complete (architecture, ADRs, security, deployment guides)
- ✅ API contracts defined (OpenAPI/AsyncAPI specifications)
- ⏳ Service implementation (not started)
- ⏳ Frontend implementation (not started)
- ⏳ ML services implementation (not started)

See the [Development Journey](./docs/journey/01-journey-week-1.md) for progress updates.

## Technology Stack

| Layer | Technology | Description |
|-------|------------|-------------|
| **Frontend** | Angular 21 | Zoneless architecture, Signal Forms |
| **Backend** | Java 21, Quarkus 3.17+ | Cloud-native microservices |
| **ML Services** | Python 3.12+, FastAPI | ML pipelines and inference |
| **Database** | MongoDB 7.0 | DocumentDB compatible |
| **Cache** | Redis 7.2 | Session and data caching |
| **Messaging** | Redpanda | Kafka-compatible streaming |
| **Search** | OpenSearch 2.11 | Full-text and vector search |
| **Storage** | MinIO | S3-compatible object storage |
| **Infrastructure** | AWS CDK | Infrastructure as Code |
| **Monitoring** | Prometheus, Grafana | Metrics and dashboards |

## Documentation

- **[Architecture Overview](./docs/architecture.md)** - Project structure and design
- **[Modernization Plan](./docs/02-modernization-plan.md)** - Migration strategy
- **[Engineering Strategy](./docs/04-modernization-engineering-strategy.md)** - Lakehouse approach
- **[Development Journey](./docs/journey/01-journey-week-1.md)** - Progress logs
- **[Phase Documentation](./docs/phases/)** - Migration phase details

## Planned Services Overview

**Note**: These services are planned but not yet implemented. See API contracts in `shared/contracts/` and `shared/specs/` for specifications.

| Service | Port | Description | Status |
|---------|------|-------------|--------|
| core-api | 8080 | User management, events, WebSocket | ⏳ Planned |
| blob-storage | 8084 | File storage and retrieval | ⏳ Planned |
| chemical-parser | 8083 | Parse SDF, MOL files | ⏳ Planned |
| chemical-properties | 8086 | Calculate molecular properties | ⏳ Planned |
| reaction-parser | 8087 | Parse RXN files | ⏳ Planned |
| crystal-parser | 8089 | Parse CIF files | ⏳ Planned |
| spectra-parser | 8090 | Parse JDX files | ⏳ Planned |
| imaging | 8091 | Image processing | ⏳ Planned |
| office-processor | 8088 | Office document conversion | ⏳ Planned |
| metadata-processing | 8098 | Metadata extraction | ⏳ Planned |
| indexing | 8099 | OpenSearch indexing | ⏳ Planned |

## Project Status

### Phase 0: Foundation & Design (Current)

- ✅ **Infrastructure Design**: AWS CDK stacks designed (9 stacks)
- ✅ **Documentation**: Comprehensive architecture, ADRs, security, deployment guides
- ✅ **API Contracts**: OpenAPI/AsyncAPI specifications defined
- ✅ **Architecture Decisions**: 7 ADRs documented
- ✅ **Planning**: Multi-agent coordination framework designed

### Implementation Phase (Next)

- ⏳ **Phase 1**: Core services implementation (not started)
- ⏳ **Phase 2**: Domain parsers implementation (not started)
- ⏳ **Phase 3**: ML services implementation (not started)
- ⏳ **Phase 4**: Frontend implementation (not started)
- ⏳ **Phase 5**: Infrastructure deployment and testing (not started)

**Note**: The project is currently in planning/design phase. The ~92% completion refers to design/planning work, not code implementation. See [Development Journey](./docs/journey/01-journey-week-1-report.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see:

- [Architecture Documentation](./docs/architecture.md) - Project structure
- [Development Guidelines](./docs/04-modernization-engineering-strategy.md) - Coding standards

## Acknowledgments

Leanda.io was originally developed by the ArqiSoft team and before that by Science Data Software team. This modernization effort aims to revitalize the platform for the open science community using modern AWS-native technologies and best practices.

---

**Built with care for the open science community**
