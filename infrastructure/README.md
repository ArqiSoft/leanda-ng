# Leanda NG Infrastructure

AWS CDK infrastructure for Leanda NG platform.

## Prerequisites

- Node.js 20+
- AWS CLI configured
- AWS CDK CLI installed (`npm install -g aws-cdk`)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Bootstrap CDK (first time only):
```bash
npx cdk bootstrap
```

3. Synthesize CloudFormation templates:
```bash
npm run synth
```

4. Deploy all stacks:
```bash
ENVIRONMENT=development npm run deploy
```

## Stacks

### Core Infrastructure Stacks

- **KMS Stack** - Customer-managed encryption keys for S3, DocumentDB, Secrets Manager, CloudWatch Logs, EBS
- **IAM Stack** - IAM roles and policies with least privilege for all services
- **Networking Stack** - VPC, subnets, security groups, VPC Flow Logs, VPC endpoints
- **Database Stack** - DocumentDB (encrypted), ElastiCache Redis, S3 buckets (KMS-encrypted)
- **Messaging Stack** - EventBridge, MSK Serverless
- **Compute Stack** - ECS cluster, ECR repository
- **Observability Stack** - CloudWatch dashboards and log groups

### Security Stacks

- **Security Stack** - GuardDuty, Macie, Security Hub, AWS Config with compliance rules

### FinOps Stacks

- **FinOps Stack** - AWS Budgets, cost monitoring, SNS topics for budget alerts

## Security Architecture

This infrastructure implements comprehensive security controls following AWS Well-Architected Framework security pillar best practices:

### Encryption

- **At Rest**: All data encrypted with KMS customer-managed keys
  - S3 buckets: SSE-KMS
  - DocumentDB: Encryption at rest with KMS
  - Secrets Manager: KMS encryption
  - CloudWatch Logs: KMS encryption
  - EBS volumes: KMS encryption

- **In Transit**: TLS 1.2+ enforced everywhere
  - API Gateway: SSL/TLS termination
  - S3: Enforce SSL (`enforceSSL: true`)
  - DocumentDB: TLS required
  - VPC endpoints: Private connectivity

### Identity and Access Management

- **Service-Specific Roles**: Each microservice has its own IAM role with least privilege permissions
- **Least Privilege**: Minimum permissions required for functionality
- **Resource-Based Policies**: S3 bucket policies, KMS key policies
- **Condition Keys**: Additional security through IAM conditions

### Network Security

- **VPC Architecture**: Public, private, and isolated subnets
- **Security Groups**: Least privilege rules (only required ports)
- **VPC Flow Logs**: All network traffic logged to CloudWatch Logs (KMS-encrypted)
- **VPC Endpoints**: Private connectivity to AWS services (reduces NAT Gateway costs)

### Security Monitoring

- **GuardDuty**: Continuous threat detection
- **Macie**: Data discovery and protection (production only)
- **Security Hub**: Centralized security findings (CIS AWS Foundations Benchmark)
- **AWS Config**: Compliance monitoring with automated rules

### Secrets Management

- **AWS Secrets Manager**: Sensitive credentials with automatic rotation
- **Systems Manager Parameter Store**: Non-sensitive configuration
- **KMS Encryption**: All secrets encrypted with customer-managed keys
- **Access Control**: Service-specific IAM roles with least privilege

### Audit and Compliance

- **CloudTrail**: Comprehensive audit logging (see `docs/security/cloudtrail-configuration.md`)
- **Compliance**: GDPR, scientific data regulations (see `docs/security/compliance-framework.md`)
- **Access Reviews**: Quarterly IAM access reviews

## Security Documentation

Comprehensive security documentation is available in `docs/security/`:

- **[Security Architecture](../docs/security/security-architecture.md)** - Complete security architecture overview
- **[Secrets Management](../docs/security/secrets-management.md)** - Secrets Manager and Parameter Store usage
- **[CloudTrail Configuration](../docs/security/cloudtrail-configuration.md)** - Audit logging setup
- **[Security Runbooks](../docs/security/security-runbooks.md)** - Incident response and breach procedures
- **[Compliance Framework](../docs/security/compliance-framework.md)** - GDPR and scientific data compliance

## Stack Dependencies

```
KMS Stack (encryption keys)
  ↓
IAM Stack (roles and policies)
  ↓
Networking Stack (VPC, security groups, Flow Logs)
  ↓
Database Stack (encrypted databases)
  ↓
Security Stack (GuardDuty, Macie, Security Hub, Config)
```

## Environment Variables

### Required

- `ENVIRONMENT` - Environment name (development, staging, production)
- `CDK_DEFAULT_ACCOUNT` - AWS account ID
- `CDK_DEFAULT_REGION` - AWS region (default: us-east-1)

### Optional (Cost Allocation)

- `COST_CENTER` - Cost center for cost allocation (default: engineering)
- `OWNER` - Owner email or team identifier (default: leanda-team@example.com)
- `BUDGET_ALERT_EMAILS` - Comma-separated list of email addresses for budget alerts (default: leanda-team@example.com)
- `MONTHLY_BUDGET_AMOUNT` - Monthly budget amount in USD (default: 1000 for dev, 5000 for staging, 10000 for production)

## Deployment Order

Stacks must be deployed in dependency order:

1. KMS Stack (encryption keys)
2. IAM Stack (roles and policies)
3. Networking Stack (VPC infrastructure)
4. Database Stack (databases and storage)
5. Messaging Stack (event bus and Kafka)
6. Compute Stack (ECS and ECR)
7. Observability Stack (monitoring)
8. Security Stack (security tooling)
9. FinOps Stack (cost management) - Can be deployed independently

## Useful Commands

- `npm run build` - Compile TypeScript
- `npm run watch` - Watch for changes and compile
- `npm run cdk` - CDK CLI
- `npm run deploy` - Deploy all stacks
- `npm run diff` - Compare deployed stack with current state
- `npm run synth` - Synthesize CloudFormation templates

## Security Best Practices

1. **Never commit secrets** - Use Secrets Manager or Parameter Store
2. **Use least privilege** - Service roles have minimum required permissions
3. **Enable encryption** - All data encrypted at rest and in transit
4. **Monitor security** - Review GuardDuty and Security Hub findings regularly
5. **Review access** - Conduct quarterly IAM access reviews
6. **Update regularly** - Keep dependencies and security patches up to date

## Cost Optimization

This infrastructure implements comprehensive cost optimization strategies following AWS Well-Architected Framework cost optimization pillar.

### Cost Allocation Tags

All resources are automatically tagged with cost allocation tags:
- `Project`: leanda-ng
- `Environment`: dev | staging | prod
- `Service`: service-name (e.g., core-api, blob-storage)
- `CostCenter`: department/budget code
- `Owner`: team/individual email

Tags are applied via the tagging utility (`lib/utils/tagging.ts`) and enable cost allocation reports in AWS Cost Explorer.

### AWS Budgets

Budgets are configured in the FinOps stack (`lib/stacks/finops-stack.ts`):
- **Development**: $1,000/month
- **Staging**: $5,000/month
- **Production**: $10,000/month

Budget alerts are configured at 50%, 80%, and 100% thresholds via SNS notifications.

### Cost Optimization Strategies

1. **S3 Storage Optimization**:
   - Intelligent-Tiering for automatic cost optimization
   - Lifecycle policies: Glacier (90 days), Deep Archive (180 days)
   - Automatic cleanup of incomplete multipart uploads

2. **Compute Optimization**:
   - ECS Fargate with auto-scaling (target CPU 70%, Memory 80%)
   - Right-sizing based on actual usage
   - Scheduled scaling for non-production environments

3. **Database Optimization**:
   - DocumentDB with multi-AZ (production only)
   - ElastiCache Redis with right-sizing
   - Reserved Instances for predictable workloads (recommended after 3 months)

4. **Network Optimization**:
   - VPC endpoints to reduce NAT Gateway costs
   - CloudFront for content delivery (caching reduces origin requests)

### Cost Monitoring

- **AWS Cost Explorer**: Cost analysis and reporting
- **AWS Budgets**: Budget tracking and alerts
- **Cost Anomaly Detection**: Automated cost spike detection (manual setup required)
- **CloudWatch Cost Dashboard**: Cost monitoring dashboard (placeholder)

### Cost Review Process

- **Monthly**: Review cost reports, identify optimization opportunities
- **Quarterly**: Evaluate Reserved Instance opportunities, review Savings Plans

See [FinOps Documentation](../docs/finops/README.md) for detailed cost optimization procedures.

### Cost Considerations

**Security Services**:
- **GuardDuty**: ~$2.00 per GB of data analyzed
- **Macie**: ~$0.10 per GB scanned (first 50GB free)
- **Security Hub**: ~$0.0010 per security check per resource
- **Config**: ~$0.003 per configuration item recorded
- **VPC Flow Logs**: ~$0.50 per GB ingested

**Core Services** (estimated monthly costs for production):
- **ECS Fargate**: ~$200-500 (depending on usage)
- **DocumentDB**: ~$300-600 (db.t3.medium, multi-AZ)
- **S3 Storage**: Variable (depends on data volume, lifecycle policies)
- **MSK Serverless**: ~$50-200 (depending on throughput)
- **ElastiCache Redis**: ~$15-50 (cache.t3.small)
- **CloudWatch**: ~$50-100 (logs, metrics, dashboards)

See [AWS Pricing](https://aws.amazon.com/pricing/) for current pricing.

## References

- [AWS Well-Architected Framework - Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [Security Documentation](../docs/security/)

