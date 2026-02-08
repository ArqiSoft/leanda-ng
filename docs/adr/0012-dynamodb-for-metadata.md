# 0012. DynamoDB for Metadata and Workflow State (MongoDB Removal)

## Status
Accepted

## Context
Leanda NG greenfield distro initially used MongoDB (and DocumentDB in AWS) for metadata and saga workflow state. The platform aims to simplify operations, reduce cost, and align with AWS-native services. DynamoDB provides single-digit millisecond latency, serverless scaling, and built-in encryption (KMS). S3 (MinIO locally) remains the sole store for blob data. No legacy data migration is required.

## Decision
- **Remove MongoDB/DocumentDB** from all services, Docker, and CDK.
- **Use DynamoDB** for all metadata and workflow state: Nodes (unified tree), Files (file metadata), WorkflowState (saga state).
- **Use S3/MinIO** only for blobs; no change to existing blob storage.
- **Table-per-aggregate**: One DynamoDB table per logical aggregate (Nodes, Files, WorkflowState) to keep access patterns clear and avoid single-table complexity.
- **Indexing service**: Stops using MongoDB; obtains file metadata via Core API REST (GET /api/v1/nodes/{id} or equivalent) instead of direct DB access.

## Consequences
- **Positive**: Single AWS-native metadata store; no DocumentDB cluster to manage; lower cost for small/medium workloads; KMS encryption and IAM integration; DynamoDB Local for dev/tests.
- **Negative**: Query patterns must be modeled with PK/GSI (no ad-hoc queries); indexing service depends on core-api for file metadata (adds one HTTP call per file event when content extraction is needed).

## Tables and Access Patterns

| Table           | PK              | GSIs | Access patterns |
|-----------------|-----------------|------|------------------|
| Nodes           | id (UUID)       | parentId-createdDateTime (list children); type-ownedBy-createdDateTime (list by type/owner) | findById, findChildren, countChildren, findNodePage, save, deleteById, findByParentIdAndType |
| Files           | id (UUID)       | parentId-createdDateTime; ownedBy-createdDateTime; blobId (find by blob) | findById, findByParentId, findByOwnedBy, findByBlobId, save, deleteById, findByStatus, findByType |
| WorkflowState   | correlationId (UUID) | workflowType-createdAt (optional) | get by correlationId, put, update |

## Alternatives Considered
- **Single-table design (STDI)**: Rejected for greenfield to keep aggregates and onboarding simpler; can be revisited if item count and cost justify it.
- **Keep DocumentDB**: Rejected to reduce operational surface and align with serverless.
