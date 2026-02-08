# AWS Cost Overview (Leanda NG)

This doc describes **which services are typically most expensive** for this project and **how to see actual costs** in your account.

## Expected cost drivers (by typical impact)

From the CDK stacks and FinOps budget filters, these are the services that usually drive most of the bill (order is approximate; actual order depends on usage):

| Rank | Service | Why it’s often expensive |
|------|---------|--------------------------|
| 1 | **Amazon Managed Streaming for Apache Kafka (MSK)** | MSK Serverless: pay per data in/out and per partition-hour; cluster name `leanda-ng-msk-<env>`. |
| 2 | **Amazon Elastic Container Service (ECS)** | Fargate (or EC2) compute: vCPU + memory 24/7 if services run continuously. |
| 3 | **Amazon CloudWatch** | Logs ingestion & storage, custom metrics, dashboards, alarms; grows with log volume. |
| 4 | **NAT Gateway** (in Networking stack) | Hourly charge per NAT Gateway + data processing; can exceed compute if traffic is high. |
| 5 | **Amazon DynamoDB** | Pay-per-request (or provisioned) + storage; 4 tables + GSIs. |
| 6 | **Amazon ElastiCache** | Redis (cache.t3.micro) runs 24/7. |
| 7 | **AWS Key Management Service (KMS)** | ~$1/month per key + per API call; 5 keys in KMS stack. |
| 8 | **Amazon S3** | Storage + requests; data bucket has lifecycle (Intelligent Tiering, Glacier). |
| 9 | **VPC / other** | NAT Gateway (hourly + $0.045/GB); interface endpoints (ECR, Logs, Secrets, SSM) in all envs to reduce NAT data. |

**Optional stacks:**

- **Test Runner** (`DEPLOY_TEST_RUNNER=true`): EC2 t4g.xlarge (spot) + EBS + Lambda + EventBridge. Can be a large share if the instance is left running.
- **Saga Orchestration**: Step Functions + Lambdas; cost depends on workflow invocations.

## How to see actual costs

Actual costs depend on usage and region. Use one of the methods below.

### 1. AWS Cost Explorer (console)

1. **Billing** → **Cost Explorer**.
2. Set time range (e.g. “Last 6 months” or “This month”).
3. **Group by** → **Service**.
4. Optional: add **Filter** → **Tag** → `Project` = `leanda-ng` (and/or `Environment` = `development`) **after** [activating those tags](https://docs.aws.amazon.com/cost-management/latest/userguide/activate-built-in-tags.html) for cost allocation.

This shows which services are actually most expensive for the selected scope (account or tag).

### 2. AWS CLI – cost by service (this month)

Uses Cost Explorer API; no tag activation required. Run from a shell with AWS credentials and appropriate permissions (`ce:GetCostAndUsage`).

```bash
# First day of current month to today
START=$(date -u +%Y-%m-01)
END=$(date -u +%Y-%m-%d)

aws ce get-cost-and-usage \
  --time-period Start="$START",End="$END" \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --output table
```

To get a compact list of services sorted by cost (requires `jq`):

```bash
START=$(date -u +%Y-%m-01)
END=$(date -u +%Y-%m-%d)

aws ce get-cost-and-usage \
  --time-period Start="$START",End="$END" \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --output json \
  | jq -r '.ResultsByTime[0].Groups | sort_by(-.Metrics.UnblendedCost.Amount | tonumber) | .[] | "\(.Metrics.UnblendedCost.Amount) \(.Keys[0])"'
```

### 3. Filter by project tag (Leanda NG only)

**Leanda resources are tagged** by CDK: `Project=leanda-ng`, `Environment=<env>`, `CostCenter`, `Owner`, `ManagedBy=CDK`. VPC, NAT Gateway, subnets, and interface endpoints in the Networking stack receive these tags, so you can attribute VPC (and other) cost to Leanda after activating cost allocation tags.

**To see Leanda-only costs (including VPC):**

1. **Activate cost allocation tags**: **Billing** → **Cost allocation tags** → select **Project** and **Environment** → **Activate**. Wait up to 24 hours for tags to appear in Cost Explorer.
2. In **Cost Explorer**, add **Filter** → **Tag** → **Project** → **leanda-ng** (and optionally **Environment** → **development**).
3. Group by **Service** to see which services are most expensive for Leanda only.

**CLI (after activating tags):**

```bash
START=$(date -u +%Y-%m-01)
END=$(date -u +%Y-%m-%d)

aws ce get-cost-and-usage \
  --time-period Start="$START",End="$END" \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --filter '{"Tags":{"Key":"Project","Values":["leanda-ng"]}}' \
  --output table
```

### 4. Budgets and alerts

The **FinOps stack** defines:

- **Total cost budget** filtered by `Project=leanda-ng` and `Environment=<env>` (defaults: $1000 dev, $5000 staging, $10000 prod).
- **Service-level budget** for ECS, DynamoDB, S3, MSK, ElastiCache, CloudWatch, KMS (80% of total).
- Alerts at 50%, 80%, 100% actual and 100% forecasted.

Check **Billing** → **Budgets** for current usage vs. these budgets.

## Quick answer: “What’s most expensive right now?”

1. Open **AWS Console** → **Billing** → **Cost Explorer**.
2. Time range: **This month** (or **Last 6 months**).
3. **Group by**: **Service**.
4. Look at the top 5–10 services in the chart/table.

That list is the actual “most expensive services running” for the selected scope (account or tag).

## VPC cost reduction (Leanda)

- **AZs**: **2 AZs** in all envs (required for MSK Serverless: at least 2 subnets per VPC). Cluster name: `leanda-ng-msk-<env>` in Leanda VPC.
- **Networking stack** uses 1 NAT Gateway in dev, 2 in prod. To reduce NAT data processing cost:
  - **Gateway endpoints** (free): S3, DynamoDB.
  - **Interface endpoints** (all envs): ECR API, ECR Docker, CloudWatch Logs, Secrets Manager, SSM — so ECS image pulls and AWS API calls avoid NAT. See `infrastructure/lib/stacks/networking-stack.ts`.

## References

- FinOps stack: `infrastructure/lib/stacks/finops-stack.ts` (budget filters, alert emails).
- Cost allocation tags: `infrastructure/lib/utils/tagging.ts` (Project, Environment, CostCenter, Owner).
- Networking (VPC, endpoints): `infrastructure/lib/stacks/networking-stack.ts`.
- FinOps skill: `.cursor/skills/aws-finops-cost/SKILL.md`.
