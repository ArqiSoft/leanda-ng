# Specifications Directory

This directory contains specifications extracted from legacy .NET services and validated against legacy code.

**Status**: ✅ **Complete** (2025-12-27). Validated and gaps added 2025-02-02.

## API versioning and base path

All Core API paths are defined relative to **`/api/v1`** (see `servers[0].url` in `api/core-api.yaml`). Legacy controllers use `api/[controller]` (e.g. `api/Users`, `api/Nodes`). New implementations should expose the spec under `/api/v1` for versioning. Paths in the OpenAPI spec are written without the base path (e.g. `/nodes`, `/categories/tree`).

## Directory Structure

```
specs/
├── api/                         # OpenAPI 3.1 specifications
│   └── core-api.yaml           # Core API endpoints (✅ Complete, incl. categories, search, notifications, node collections, category entities)
├── events/                      # AsyncAPI specifications
│   └── domain-events.yaml      # Domain events and commands (✅ Complete)
├── models/                      # JSON Schema specifications
│   ├── User.json               # User entity schema (✅ Complete)
│   ├── File.json               # File entity schema (✅ Complete)
│   ├── Folder.json             # Folder entity schema (✅ Complete)
│   ├── Record.json             # Record entity schema (✅ Complete)
│   ├── Model.json              # ML Model entity schema (✅ Complete)
│   ├── Node.json               # Unified node schema (✅ Complete)
│   ├── CategoryTree.json       # Category tree schema (✅ Complete)
│   └── UserNotification.json   # User notification schema (✅ Complete)
├── implementation/              # Implementation plans
│   └── core-services-plan.md   # .NET to Quarkus mapping (✅ Complete; includes legacy-only events note)
└── tests/                       # Test specifications
    ├── api-tests.md            # API test scenarios (✅ Complete)
    ├── integration-tests.md    # Integration test scenarios (✅ Complete)
    └── test-data.md            # Test data fixtures (✅ Complete)
```

## Legacy validation

Specs were validated against:

- **REST**: `legacy/leanda-core/Sds.Osdr.WebApi/Controllers/*.cs` (CategoryTreesController, SearchResults, UserNotificationsController, NodeCollectionsController, CategoryEntitiesController, NodesController, EntititesController, UsersController, ExportsController, MachineLearningController, etc.)
- **Events**: `legacy/leanda-core/Sds.Osdr.Generic/Domain/Events/*.cs`, `Sds.Osdr.RecordsFile/Domain/Events/*.cs`, and related command/aggregate modules.

Gaps that were added: Categories API, Search API, User Notifications API, Node Collections (bulk PATCH), Category Entities API; model schemas CategoryTree.json, UserNotification.json. Legacy-only domain events (RecordsFile, Pdf, Reactions) are documented in `implementation/core-services-plan.md` for when those backends are migrated.

## Extracted Specifications Summary

### OpenAPI 3.1 (`api/core-api.yaml`)
- **Nodes API**: GET/POST nodes, inner nodes, public nodes, ZIP download, **bulk PATCH (node collection)**
- **Entities API**: CRUD for files, folders, records, models; blobs, images, metadata; **entity categories**
- **Users API**: User management, public info; **notifications (GET/DELETE)**
- **Categories API**: Category tree CRUD, tree node update/delete
- **Search API**: Full-text search (OpenSearch-backed, paginated)
- **Category Entities API**: Add/remove categories on entities; get entities by category
- **Exports API**: File export with format conversion
- **Machine Learning API**: Model training, predictions, feature vectors
- **Health API**: Health checks, readiness, version

### AsyncAPI (`events/domain-events.yaml`)
- **User Events**: CreateUser, UserCreated, UserUpdated, UserPersisted
- **Folder Events**: CreateFolder, FolderCreated, FolderMoved, FolderDeleted
- **File Events**: FileCreated, FileStatusChanged, FileMoved, FileDeleted, ImageAdded
- **Record Events**: RecordCreated, RecordParsed, FieldsUpdated
- **ML Events**: StartTraining, TrainingCompleted, PredictionCreated
- **Processing Events**: ProcessingStarted, ProcessingFinished, ProcessingFailed

### JSON Schemas (`models/*.json`)
- Entities: User, File, Folder, Record, Model, Node, CategoryTree, UserNotification
- Value Objects: AccessPermissions, Image, Blob, KeyValue, Property
- MongoDB indexes defined for each entity (where applicable)

### Implementation Plan (`implementation/core-services-plan.md`)
- Technology mapping: .NET Core 3.1 → Java 21 + Quarkus 3.x
- Framework mapping: MassTransit → SmallRye Reactive Messaging
- Data access: MongoDB.Driver → Quarkus Panache MongoDB
- Authentication: OIDC with Keycloak
- Work breakdown per agent

## Usage

- **Agent 1 (Core API)**: Use `api/core-api.yaml` for REST endpoint implementation
- **Agent 2 (Domain Services)**: Use `events/domain-events.yaml` for event handler implementation
- **Agent 3 (Persistence)**: Use `models/*.json` for data model implementation
- **Agent 4 (Testing)**: Use `tests/*.md` for test scenario implementation
- **Agent 5 (Docker)**: Reference specs for service configuration

## Legacy Source Files Analyzed

- `leanda-core/Sds.Osdr.WebApi/Controllers/*.cs` - REST endpoints
- `leanda-core/Sds.Osdr.Generic/Domain/Commands/*.cs` - Commands
- `leanda-core/Sds.Osdr.Generic/Domain/Events/*.cs` - Events
- `leanda-core/Sds.Osdr.Generic/Domain/Aggregates/*.cs` - Domain models
- `leanda-core/Sds.Osdr.MachineLearning/Domain/Commands/*.cs` - ML commands

## Next Steps

Phase 1 agents can begin implementation using these specifications:
1. **Agent 5**: Set up Docker infrastructure
2. **Agent 1**: Implement REST endpoints from `core-api.yaml`
3. **Agent 2**: Implement event handlers from `domain-events.yaml`
4. **Agent 3**: Implement data models from `models/*.json`
5. **Agent 4**: Implement tests from `tests/*.md`

