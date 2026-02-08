# DynamoDB Data Model (Leanda NG)

Metadata and workflow state after MongoDB removal. Blobs remain in S3/MinIO.

## Tables

### Nodes
- **Table name**: `{project}-{env}-nodes` (e.g. `leanda-ng-dev-nodes`)
- **Partition key**: `id` (String, UUID)
- **Attributes**: type, subType, name, ownedBy, createdBy, parentId, status, isDeleted, blob (Map), images (List), totalRecords, accessPermissions (Map), version, displayName, firstName, lastName, loginName, email, avatar, createdDateTime (String ISO-8601), updatedDateTime, updatedBy
- **GSI 1** – list children: PK=`parentId`, SK=`createdDateTime` (projection: ALL)
- **GSI 2** – list by type and owner: PK=`type#ownedBy`, SK=`createdDateTime` (projection: ALL)

### Files
- **Table name**: `{project}-{env}-files` (e.g. `leanda-ng-dev-files`)
- **Partition key**: `id` (String, UUID)
- **Attributes**: bucket, blobId, ownedBy, createdBy, parentId, fileName, length, md5, isDeleted, type, status, images (List), metadata (Map), version, createdDateTime, updatedDateTime, updatedBy
- **GSI 1** – by parent: PK=`parentId`, SK=`createdDateTime`
- **GSI 2** – by owner: PK=`ownedBy`, SK=`createdDateTime`
- **GSI 3** – by blob: PK=`blobId` (no SK; blobId unique per file)

### WorkflowState
- **Table name**: `{project}-{env}-workflow-state` (e.g. `leanda-ng-dev-workflow-state`)
- **Partition key**: `correlationId` (String, UUID)
- **Attributes**: workflowType, currentState, version, createdAt, updatedAt, fileId, blobId, bucket, userId, fileWorkflowType, thumbnailCompleted, parseCompleted, recordProcessingCompleted, metadataCompleted, indexingCompleted, failureMessage, trainingId, optimizationCompleted, trainingCompleted, reportCompleted
- **GSI** (optional): PK=`workflowType`, SK=`createdAt` for listing by type

## Configuration
- **Local**: DynamoDB Local endpoint `http://localhost:8000` (or from docker-compose).
- **AWS**: Use default DynamoDB endpoint; table names from env (e.g. `LEANDA_NODES_TABLE`, `LEANDA_FILES_TABLE`, `LEANDA_WORKFLOW_STATE_TABLE`).
- **Encryption**: KMS (CMK) for all tables in AWS.
