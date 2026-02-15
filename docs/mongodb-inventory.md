# MongoDB Usage Inventory (Pre–DynamoDB Migration)

This document recorded all MongoDB usage before removal. Used for DynamoDB migration (see ADR 0012 and docs/dynamodb-model.md).

## Collections and Usage

| Mongo Collection | Used By | Purpose | DynamoDB Table |
|------------------|---------|---------|----------------|
| Nodes | core-api (NodeRepositoryImpl) | Unified tree (users, folders, files, records, models) | Nodes |
| Files | core-api (FileRepositoryImpl, FileCreatedHandler), indexing (FileEventHandler) | File metadata | Files |
| workflow_state | core-api (WorkflowStateEntity, WorkflowStateRepositoryImpl) | Saga workflow state | WorkflowState |

## Code Locations (Pre-Migration)

- **core-api**: WorkflowStateEntity, WorkflowStateRepositoryImpl, NodeRepositoryImpl, FileRepositoryImpl, FileCreatedHandler, MongoClientConfig; application.properties (quarkus.mongodb.*); tests (NodeRepositoryTest, EntitiesResourceTest, NodesResourceTest, SearchResourceTest, WorkflowStateRepositoryImplTest, MongoClientConfigTest).
- **indexing**: FileEventHandler (MongoClient for getFileDocument, isEntityDeleted); application.properties.
- **shared/models**: Node.java, File.java (both @MongoEntity, PanacheMongoEntityBase).
- **Other services**: application.properties only (quarkus.mongodb.connection-string, quarkus.mongodb.database) in blob-storage, office-processor, imaging, chemical-parser, chemical-properties, metadata-processing.

## Config and Infra

- **Docker**: mongodb, mongodb-test, mongodb-integration services; MONGODB_CONNECTION_STRING and depends_on in service definitions.
- **CDK**: DocumentDB in database-stack.ts; KMS documentDbKey; observability DocumentDB alarms; finops DocumentDB budget filter.

All of the above have been removed or replaced per the migration plan.
