# Secrets Management Architecture

**Last Updated**: 2025-12-27  
**Status**: Complete  
**Owner**: Agent PROD-4

## Overview

This document describes the secrets management architecture for Leanda.io platform, using AWS Secrets Manager and Systems Manager Parameter Store for secure credential and configuration management.

## Architecture

### AWS Secrets Manager

**Purpose**: Store sensitive credentials and secrets that require rotation

**Use Cases**:
- Database passwords (DocumentDB, Redis)
- API keys (third-party services)
- OAuth2 client secrets
- TLS certificates and private keys
- Service-to-service authentication tokens

**Features**:
- Automatic secret rotation (where supported)
- KMS encryption (customer-managed keys)
- Versioning and audit trail
- Fine-grained access control via IAM

### Systems Manager Parameter Store

**Purpose**: Store configuration values and non-sensitive parameters

**Use Cases**:
- Application configuration (non-sensitive)
- Feature flags
- Service endpoints
- Environment-specific settings

**Parameter Types**:
- **Standard**: Non-sensitive configuration (free)
- **SecureString**: Sensitive parameters (encrypted with KMS)

## Secret Naming Convention

### Secrets Manager

```
{projectName}/{environment}/{serviceName}/{secretName}
{projectName}/{environment}/shared/{secretName}
```

**Examples**:
- `leanda-ng/production/core-api/database-password`
- `leanda-ng/production/shared/mongodb-admin-password`
- `leanda-ng/development/blob-storage/s3-access-key`

### Parameter Store

```
/{projectName}/{environment}/{serviceName}/{parameterName}
/{projectName}/{environment}/shared/{parameterName}
```

**Examples**:
- `/leanda-ng/production/core-api/mongodb-connection-string`
- `/leanda-ng/production/shared/kafka-bootstrap-servers`
- `/leanda-ng/development/indexing/opensearch-endpoint`

## IAM Access Control

### Service Roles

Each service has an IAM role with permissions to access:
- Service-specific secrets: `{projectName}/{environment}/{serviceName}/*`
- Shared secrets: `{projectName}/{environment}/shared/*`

### Permissions

**Secrets Manager**:
```json
{
  "Effect": "Allow",
  "Action": [
    "secretsmanager:GetSecretValue",
    "secretsmanager:DescribeSecret"
  ],
  "Resource": [
    "arn:aws:secretsmanager:region:account:secret:leanda-ng/environment/service-name/*",
    "arn:aws:secretsmanager:region:account:secret:leanda-ng/environment/shared/*"
  ]
}
```

**Parameter Store**:
```json
{
  "Effect": "Allow",
  "Action": [
    "ssm:GetParameter",
    "ssm:GetParameters",
    "ssm:GetParametersByPath"
  ],
  "Resource": [
    "arn:aws:ssm:region:account:parameter/leanda-ng/environment/service-name/*",
    "arn:aws:ssm:region:account:parameter/leanda-ng/environment/shared/*"
  ]
}
```

**KMS Decrypt** (for encrypted secrets/parameters):
```json
{
  "Effect": "Allow",
  "Action": [
    "kms:Decrypt",
    "kms:DescribeKey"
  ],
  "Resource": "arn:aws:kms:region:account:key/*",
  "Condition": {
    "StringEquals": {
      "kms:ViaService": [
        "secretsmanager.region.amazonaws.com",
        "ssm.region.amazonaws.com"
      ]
    }
  }
}
```

## Secret Rotation

### Supported Services

AWS Secrets Manager supports automatic rotation for:
- RDS databases (DocumentDB, Aurora, RDS)
- Redshift clusters
- Custom Lambda rotation functions

### Rotation Schedule

- **Database Passwords**: Every 30 days
- **API Keys**: Every 90 days (or as required by third-party services)
- **OAuth2 Secrets**: Every 90 days

### Rotation Function

Custom Lambda functions for rotation:
- `leanda-ng-rotate-docdb-password-{environment}`
- `leanda-ng-rotate-api-key-{environment}`

## Application Integration

### Java/Quarkus Services

**Secrets Manager**:
```java
@ConfigProperty(name = "quarkus.mongodb.connection-string")
String connectionString; // Loaded from Secrets Manager via Quarkus extension
```

**Parameter Store**:
```java
@ConfigProperty(name = "kafka.bootstrap.servers")
String kafkaBootstrapServers; // Loaded from Parameter Store
```

### Configuration Properties

Services use Quarkus configuration properties that automatically resolve from:
1. Environment variables
2. Parameter Store (via AWS SDK)
3. Secrets Manager (via AWS SDK)

## Secret Creation and Management

### Creating Secrets

**Using AWS CLI**:
```bash
# Create database password secret
aws secretsmanager create-secret \
  --name leanda-ng/production/core-api/database-password \
  --description "DocumentDB password for core-api service" \
  --secret-string '{"username":"leanda_admin","password":"SecurePassword123!"}' \
  --kms-key-id alias/leanda-ng-secrets-production

# Create shared API key
aws secretsmanager create-secret \
  --name leanda-ng/production/shared/external-api-key \
  --description "External API key for third-party service" \
  --secret-string "api-key-value" \
  --kms-key-id alias/leanda-ng-secrets-production
```

**Using AWS Console**:
1. Navigate to Secrets Manager
2. Click "Store a new secret"
3. Select secret type (credentials, API key, etc.)
4. Enter secret name following naming convention
5. Select KMS key for encryption
6. Configure rotation (if supported)
7. Review and store

### Updating Secrets

**Using AWS CLI**:
```bash
aws secretsmanager update-secret \
  --secret-id leanda-ng/production/core-api/database-password \
  --secret-string '{"username":"leanda_admin","password":"NewSecurePassword123!"}'
```

### Rotating Secrets

**Automatic Rotation**:
- Configured in Secrets Manager console
- Lambda function handles rotation
- Old versions retained for rollback

**Manual Rotation**:
```bash
aws secretsmanager rotate-secret \
  --secret-id leanda-ng/production/core-api/database-password
```

## Security Best Practices

1. **Never Hardcode Secrets**: Always use Secrets Manager or Parameter Store
2. **Use Least Privilege**: Service roles only access required secrets
3. **Enable Rotation**: Automate secret rotation where possible
4. **Monitor Access**: CloudTrail logs all secret access
5. **Version Control**: Never commit secrets to version control
6. **Encryption**: All secrets encrypted with KMS customer-managed keys
7. **Audit Trail**: All secret operations logged in CloudTrail

## Monitoring and Alerting

### CloudWatch Metrics

- `GetSecretValue` API calls
- Secret rotation failures
- Parameter access patterns

### CloudTrail Events

All secret operations logged:
- `CreateSecret`
- `UpdateSecret`
- `GetSecretValue`
- `RotateSecret`
- `DeleteSecret`

### Alerts

- Secret rotation failures
- Unauthorized access attempts
- Secret deletion attempts

## Disaster Recovery

### Backup

- Secrets Manager: Automatic versioning
- Parameter Store: Manual backups (export to S3)

### Recovery

1. Restore from previous version (Secrets Manager)
2. Recreate from backup (Parameter Store)
3. Update application configuration
4. Verify service functionality

## Compliance

### Audit Requirements

- All secret access logged in CloudTrail
- Secret versions retained for audit trail
- Access reviews conducted quarterly

### Data Protection

- Secrets encrypted at rest (KMS)
- Secrets encrypted in transit (TLS)
- Access controlled via IAM
- No secrets in logs or error messages

## References

- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/)
- [AWS Systems Manager Parameter Store Documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [Quarkus AWS Integration](https://quarkus.io/guides/amazon-services)

