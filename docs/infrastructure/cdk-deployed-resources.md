# CDK-Deployed Resources (Leanda NG)

This document lists all AWS resources and services deployed by the CDK app (`infrastructure/bin/leanda-ng.ts`), per stack. **Terraform is not used for the main platform** — only legacy `legacy/leanda-ui/terraform/` exists for the old UI.

**Environment**: `ENVIRONMENT` (default `development`). Stack IDs use prefix `leanda-ng-<stack>-<env>`.

---

## Stack dependency order

1. **KMS** (no deps)
2. **IAM** (no deps)
3. **Networking** (depends on KMS for Flow Logs key)
4. **Database** (Networking, KMS)
5. **Messaging** (Networking)
6. **Compute** (Networking, IAM)
7. **Observability** (Compute, Database, Messaging)
8. **Security** (Networking)
9. **FinOps** (no deps)
10. **Saga Orchestration** (optional: `DEPLOY_SAGA_ORCHESTRATION=true`, depends on Messaging)
11. **Test Runner** (optional: `DEPLOY_TEST_RUNNER=true`, standalone)

---

## 1. KMS Stack (`leanda-ng-kms-<env>`)

| Resource | Type | Purpose |
|----------|------|---------|
| S3Key | KMS Key | S3 bucket encryption |
| DynamoDbKey | KMS Key | DynamoDB encryption |
| SecretsKey | KMS Key | Secrets Manager encryption |
| LogsKey | KMS Key | CloudWatch Logs encryption |
| EbsKey | KMS Key | EBS volume encryption |

- All keys: key rotation enabled, alias `leanda-ng-<usage>-<env>`.
- Outputs: ARNs for each key (exported for cross-stack).

---

## 2. IAM Stack (`leanda-ng-iam-<env>`)

| Resource | Type | Purpose |
|----------|------|---------|
| EcsExecutionRole | IAM Role | ECS task execution (pull images, logs) |
| EcsTaskRole | IAM Role | ECS task runtime (base) |
| LambdaExecutionRole | IAM Role | Lambda (VPC + logs) |
| core-api Role | IAM Role | core-api service |
| blob-storage Role | IAM Role | blob-storage service |
| indexing Role | IAM Role | indexing service |
| metadata-processing Role | IAM Role | metadata-processing service |
| chemical-parser Role | IAM Role | chemical-parser service |
| chemical-properties Role | IAM Role | chemical-properties service |
| reaction-parser Role | IAM Role | reaction-parser service |
| crystal-parser Role | IAM Role | crystal-parser service |
| spectra-parser Role | IAM Role | spectra-parser service |
| imaging Role | IAM Role | imaging service |
| office-processor Role | IAM Role | office-processor service |

- Each service role: Secrets Manager, SSM Parameter Store, KMS decrypt; DB/S3/MSK/EventBridge/OpenSearch/X-Ray as needed.
- Outputs: EcsTaskRoleArn, EcsExecutionRoleArn, LambdaExecutionRoleArn.

---

## 3. Networking Stack (`leanda-ng-networking-<env>`)

| Resource | Type | Purpose |
|----------|------|---------|
| Vpc | VPC | `leanda-ng-vpc-<env>`, 2 AZs, public/private/isolated subnets |
| EcsSecurityGroup | Security Group | ECS Fargate (egress: 443, 80, 53) |
| VpcFlowLogs | Flow Log | All traffic → CloudWatch Logs |
| VpcFlowLogsLogGroup | Log Group | `/aws/vpc/flowlogs/leanda-ng-<env>` |
| S3Endpoint | VPC Gateway Endpoint | S3 (private/isolated) |
| DynamoDbEndpoint | VPC Gateway Endpoint | DynamoDB (private/isolated) |
| SecretsManagerEndpoint | Interface Endpoint | Secrets Manager (prod only) |
| SsmEndpoint | Interface Endpoint | SSM (prod only) |
| CloudWatchLogsEndpoint | Interface Endpoint | CloudWatch Logs (prod only) |

- Outputs: VpcId, EcsSecurityGroupId, VpcFlowLogsId.

---

## 4. Database Stack (`leanda-ng-database-<env>`)

| Resource | Type | Purpose |
|----------|------|---------|
| DataBucket | S3 Bucket | `leanda-ng-data-<env>-<account>`, versioned, KMS, lifecycle (Intelligent Tiering, Glacier, multipart expiry) |
| ArtifactsBucket | S3 Bucket | `leanda-ng-artifacts-<env>-<account>`, KMS |
| NodesTable | DynamoDB Table | `leanda-ng-<env>-nodes`, GSIs: parentId-createdDateTime, type-ownedBy-createdDateTime |
| FilesTable | DynamoDB Table | `leanda-ng-<env>-files`, GSIs: parentId-createdDateTime, ownedBy-createdDateTime, blobId |
| WorkflowStateTable | DynamoDB Table | `leanda-ng-<env>-workflow-state`, GSI: workflowType-createdAt |
| CategoryTreesTable | DynamoDB Table | `leanda-ng-<env>-category-trees` |
| RedisCluster | ElastiCache (CfnCacheCluster) | `leanda-ng-redis-<env>`, cache.t3.micro, 1 node |
| RedisSecurityGroup | Security Group | Redis (ingress 6379 from ECS SG) |
| RedisSubnetGroup | ElastiCache Subnet Group | Private subnets |

- Outputs: table names, RedisEndpoint, RedisPort, RedisSecurityGroupId, DataBucketName.

---

## 5. Messaging Stack (`leanda-ng-messaging-<env>`)

| Resource | Type | Purpose |
|----------|------|---------|
| EventBus | EventBridge Event Bus | `leanda-ng-<env>` |
| MskCluster | MSK Serverless Cluster | `leanda-ng-msk-<env>`, IAM auth, in VPC private subnets (requires 2 AZs) |

- Outputs: EventBusArn, EventBusName, MskClusterArn.

---

## 6. Compute Stack (`leanda-ng-compute-<env>`)

| Resource | Type | Purpose |
|----------|------|---------|
| EcrRepository | ECR Repository | `leanda-ng/<env>`, scan on push, lifecycle (5/10 images) |
| EcsCluster | ECS Cluster | `leanda-ng-cluster-<env>`, Container Insights |
| LogGroup | CloudWatch Log Group | `/ecs/leanda-ng-<env>` |

- Outputs: ClusterName, EcrRepositoryUri, LogGroupName.

---

## 7. Observability Stack (`leanda-ng-observability-<env>`)

**Services monitored**: core-api, blob-storage, indexing, metadata-processing, chemical-parser, chemical-properties, reaction-parser, crystal-parser, spectra-parser, imaging, office-processor.

| Resource | Type | Purpose |
|----------|------|---------|
| CriticalAlertsTopic | SNS Topic | P1 alerts |
| WarningAlertsTopic | SNS Topic | P2 alerts |
| InfoAlertsTopic | SNS Topic | P3 alerts |
| XRayErrorSamplingRule | X-Ray Sampling Rule | 100% for errors |
| XRaySuccessSamplingRule | X-Ray Sampling Rule | 10% for success |
| XRayServiceGroup | X-Ray Group | Service map filter |
| ServiceLogGroup | Log Group | `/aws/leanda-ng/services/<env>` |
| Per-service Log Groups | Log Groups | `/aws/leanda-ng/services/<service>/<env>` |
| ECS alarms (per service) | CloudWatch Alarm | CPU/Memory (P2), 5xx error rate (P1) |
| DynamoDbUserErrorsAlarm | CloudWatch Alarm | DynamoDB user errors (P2) |
| RedisMemoryAlarm, RedisEvictionsAlarm | CloudWatch Alarm | Redis (P2) |
| MskConsumerLagAlarm | CloudWatch Alarm | MSK lag (P2) |
| EventBridgeDlqAlarm | CloudWatch Alarm | EventBridge DLQ (P1) |
| S3BucketSizeAlarm, S3RequestErrorsAlarm | CloudWatch Alarm | S3 (P3/P2) |
| EventErrorRateAlarm | CloudWatch Alarm | Event error rate (P2) |
| MainDashboard | CloudWatch Dashboard | `leanda-ng-main-<env>` |
| Per-service dashboards | CloudWatch Dashboard | `leanda-ng-<service>-<env>` |
| BusinessMetricsDashboard | CloudWatch Dashboard | `leanda-ng-business-metrics-<env>` |
| PerformanceDashboard | CloudWatch Dashboard | `leanda-ng-performance-<env>` |
| EventObservabilityDashboard | CloudWatch Dashboard | `leanda-ng-events-<env>` |

- Outputs: MainDashboardName, CriticalAlertsTopicArn, WarningAlertsTopicArn, InfoAlertsTopicArn, ApplicationSignalsServices.

---

## 8. Security Stack (`leanda-ng-security-<env>`)

| Resource | Type | Purpose |
|----------|------|---------|
| SecurityAlertsTopic | SNS Topic | Security alerts |
| ConfigBucket | S3 Bucket | `leanda-ng-config-<env>-<account>`, AWS Config delivery |
| SecurityLogGroup | Log Group | `/aws/leanda-ng/security/<env>` |
| GuardDutyDetector | GuardDuty Detector | Threat detection, S3/Kubernetes/Malware config |
| GuardDutySNSRole | IAM Role | GuardDuty → SNS |
| MacieSession | Macie Session | ENABLED (prod) / PAUSED (non-prod) |
| SecurityHub | Security Hub | CfnHub |
| ConfigRole | IAM Role | AWS Config |
| ConfigDeliveryChannel | Config Delivery Channel | S3, 24h frequency |
| ConfigRecorder | Config Recorder | All supported + global |
| Config Rules | Managed Rules | S3 encryption, S3 public read/write, EBS encryption, IAM password, CloudTrail, VPC Flow Logs, RDS encryption, SG ingress, Lambda public access |

- Outputs: SecurityAlertsTopicArn, GuardDutyDetectorId, SecurityHubArn, ConfigBucketName.

---

## 9. FinOps Stack (`leanda-ng-finops-<env>`)

| Resource | Type | Purpose |
|----------|------|---------|
| BudgetTopic | SNS Topic | Budget alerts |
| CostAnomalyTopic | SNS Topic | Cost anomaly alerts |
| TotalCostBudget | AWS Budget | By Project/Environment, 50/80/100% and forecast |
| ServiceCostBudget | AWS Budget | ECS, DynamoDB, S3, MSK, ElastiCache, CloudWatch, KMS |
| BillingAlarmRole | IAM Role | Placeholder (billing alarm manual in us-east-1) |
| CostDashboard | CloudWatch Dashboard | `leanda-ng-cost-<env>` |

- Outputs: BudgetTopicArn, CostAnomalyTopicArn, TotalCostBudgetName, CostDashboardName, CostAnomalyDetectionNote.

---

## 10. Saga Orchestration Stack (optional) (`leanda-ng-saga-orchestration-<env>`)

**Enabled**: `DEPLOY_SAGA_ORCHESTRATION=true`

| Resource | Type | Purpose |
|----------|------|---------|
| WorkflowStateTable | DynamoDB Table | `leanda-ng-saga-state-<env>` |
| ParseFileHandler | Lambda | saga-handlers/parse-file |
| GenerateMetadataHandler | Lambda | saga-handlers/generate-metadata |
| IndexDocumentHandler | Lambda | saga-handlers/index-document |
| OptimizeTrainingHandler | Lambda | saga-handlers/optimize-training |
| TrainModelHandler | Lambda | saga-handlers/train-model |
| FileProcessingWorkflow | Step Functions State Machine | File processing saga |
| MlTrainingWorkflow | Step Functions State Machine | ML training saga |
| FileProcessingStartedRule | EventBridge Rule | EventBridge → FileProcessing state machine |

- Outputs: FileProcessingStateMachineArn, MlTrainingStateMachineArn.

---

## 11. Test Runner Stack (optional) (`leanda-ng-test-runner-<env>`)

**Enabled**: `DEPLOY_TEST_RUNNER=true`

| Resource | Type | Purpose |
|----------|------|---------|
| TestRunnerInstance | EC2 Instance | t4g.xlarge, ARM64, Amazon Linux 2023, spot (default), default VPC public subnet |
| TestRunnerSecurityGroup | Security Group | Optional SSH; SSM access |
| TestRunnerRole | IAM Role | SSM, CloudWatch Agent, ECR pull, S3 test-data read |
| AutoStopNotificationTopic | SNS Topic | Optional, if TEST_RUNNER_ADMIN_EMAIL set |
| AutoStopLambdaRole | IAM Role | Lambda for auto-stop |
| AutoStopFunction | Lambda | Python 3.12, ARM64, every 15 min (EventBridge), stops instance after inactivity |
| AutoStopLambdaLogGroup | Log Group | Lambda logs |
| AutoStopScheduleRule | EventBridge Rule | Rate 15 minutes → Lambda |

- User data: Docker, Docker Compose, ECR helper, Java 21, Maven, `/opt/test-runner`.
- Outputs: TestRunnerInstanceId, TestRunnerRoleArn, AutoStopLambdaArn, NotificationTopicArn (if set), SSMConnectCommand, StartInstanceCommand, optional SSH/PublicIP.

---

## Summary: services and resources

| Category | Services / Resources |
|----------|----------------------|
| **Application services (IAM + Observability)** | core-api, blob-storage, indexing, metadata-processing, chemical-parser, chemical-properties, reaction-parser, crystal-parser, spectra-parser, imaging, office-processor |
| **Compute** | ECS cluster, ECR repo, CloudWatch log group |
| **Data** | DynamoDB (nodes, files, workflow-state, category-trees), ElastiCache Redis, S3 (data, artifacts) |
| **Messaging** | EventBridge bus, MSK Serverless |
| **Security & compliance** | KMS (5 keys), GuardDuty, Macie, Security Hub, AWS Config + rules |
| **Observability** | CloudWatch dashboards/alarms/log groups, X-Ray, SNS alert topics |
| **FinOps** | Budgets, SNS topics, cost dashboard |
| **Optional** | Saga orchestration (Step Functions + Lambdas), Test Runner (EC2 + Lambda) |

To list what is actually deployed in an account/region, use:

```bash
cd infrastructure && npx cdk list
```

To compare code vs deployed state:

```bash
cd infrastructure && npx cdk diff
```
