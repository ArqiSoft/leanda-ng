# Secrets Management Guide

This guide describes how to manage secrets and sensitive configuration for Leanda.io deployments.

## Overview

Leanda.io uses a multi-layered approach to secrets management:
- **GitHub Secrets** for CI/CD pipeline secrets
- **AWS Secrets Manager** for runtime secrets
- **AWS Systems Manager Parameter Store** for configuration parameters
- **Environment Variables** for non-sensitive configuration

## Principles

1. **Never commit secrets**: Secrets must never be committed to version control
2. **Least privilege**: Grant minimum permissions required
3. **Rotation**: Rotate secrets regularly
4. **Encryption**: Encrypt secrets at rest and in transit
5. **Audit**: Log all secret access

## GitHub Secrets

### Required Secrets

Configure these in **Settings** → **Secrets and variables** → **Actions**:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `AWS_ROLE_TO_ASSUME_STAGING` | IAM role ARN for staging deployments | `arn:aws:iam::123456789012:role/GitHubActionsStagingRole` |
| `AWS_ROLE_TO_ASSUME_PRODUCTION` | IAM role ARN for production deployments | `arn:aws:iam::123456789012:role/GitHubActionsProductionRole` |
| `AWS_ACCOUNT_ID` | AWS account ID | `123456789012` |

### Optional Secrets

| Secret Name | Description | When to Use |
|------------|-------------|-------------|
| `DOCKER_HUB_USERNAME` | Docker Hub username | If using Docker Hub |
| `DOCKER_HUB_TOKEN` | Docker Hub access token | If using Docker Hub |
| `NPM_TOKEN` | NPM access token | If using private NPM packages |
| `SONAR_TOKEN` | SonarQube token | If using SonarQube |

### Adding Secrets

```bash
# Using GitHub CLI
gh secret set AWS_ROLE_TO_ASSUME_STAGING \
  --body "arn:aws:iam::123456789012:role/GitHubActionsStagingRole"

# Using GitHub Web UI
# 1. Go to repository Settings
# 2. Navigate to Secrets and variables → Actions
# 3. Click "New repository secret"
# 4. Enter name and value
# 5. Click "Add secret"
```

## AWS Secrets Manager

### Storing Secrets

Use AWS Secrets Manager for runtime secrets (database passwords, API keys, etc.):

```bash
# Create a secret
aws secretsmanager create-secret \
  --name leanda-ng/staging/documentdb-password \
  --description "DocumentDB master password for staging" \
  --secret-string "MySecurePassword123!" \
  --tags Key=Environment,Value=staging Key=Project,Value=leanda-ng

# Update a secret
aws secretsmanager update-secret \
  --secret-id leanda-ng/staging/documentdb-password \
  --secret-string "NewSecurePassword456!"

# Rotate a secret
aws secretsmanager rotate-secret \
  --secret-id leanda-ng/staging/documentdb-password \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:rotate-documentdb-password
```

### Retrieving Secrets in CDK

```typescript
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';

// Reference existing secret
const dbPassword = secretsmanager.Secret.fromSecretNameV2(
  this,
  'DocumentDBPassword',
  'leanda-ng/staging/documentdb-password'
);

// Use in RDS/DocumentDB configuration
new docdb.DatabaseCluster(this, 'Database', {
  masterUser: {
    username: 'admin',
    password: dbPassword.secretValue,
  },
  // ...
});
```

### Retrieving Secrets in Application Code

**Java (Quarkus)**:

```java
@ConfigProperty(name = "quarkus.aws.secretsmanager.secret-name")
String secretName;

@Inject
SecretsManagerClient secretsManager;

public String getSecret() {
    GetSecretValueRequest request = GetSecretValueRequest.builder()
        .secretId(secretName)
        .build();
    
    GetSecretValueResponse response = secretsManager.getSecretValue(request);
    return response.secretString();
}
```

**Configuration** (`application.properties`):

```properties
quarkus.aws.secretsmanager.secret-name=leanda-ng/staging/documentdb-password
quarkus.aws.region=us-east-1
```

## AWS Systems Manager Parameter Store

### Storing Parameters

Use Parameter Store for configuration parameters (non-sensitive):

```bash
# Store a String parameter
aws ssm put-parameter \
  --name /leanda-ng/staging/api-version \
  --value "v2" \
  --type String \
  --tags Key=Environment,Value=staging Key=Project,Value=leanda-ng

# Store a SecureString parameter (encrypted)
aws ssm put-parameter \
  --name /leanda-ng/staging/api-key \
  --value "sk-1234567890abcdef" \
  --type SecureString \
  --key-id alias/aws/ssm \
  --tags Key=Environment,Value=staging Key=Project,Value=leanda-ng
```

### Retrieving Parameters in Application Code

**Java (Quarkus)**:

```java
@ConfigProperty(name = "quarkus.aws.ssm.parameter-name")
String parameterName;

@Inject
SsmClient ssmClient;

public String getParameter() {
    GetParameterRequest request = GetParameterRequest.builder()
        .name(parameterName)
        .withDecryption(true)  // For SecureString
        .build();
    
    GetParameterResponse response = ssmClient.getParameter(request);
    return response.parameter().value();
}
```

## Environment Variables

### Non-Sensitive Configuration

Use environment variables for non-sensitive configuration:

```bash
# In docker-compose.yml
environment:
  - ENVIRONMENT=staging
  - AWS_REGION=us-east-1
  - LOG_LEVEL=INFO

# In ECS task definition (CDK)
taskDefinition.addContainer('app', {
  environment: [
    { name: 'ENVIRONMENT', value: 'staging' },
    { name: 'AWS_REGION', value: 'us-east-1' },
    { name: 'LOG_LEVEL', value: 'INFO' },
  ],
});
```

## Secret Rotation

### Automated Rotation

Set up automatic secret rotation using AWS Secrets Manager:

```bash
# Create rotation function (Lambda)
aws lambda create-function \
  --function-name rotate-documentdb-password \
  --runtime python3.11 \
  --handler index.handler \
  --role arn:aws:iam::123456789012:role/SecretsManagerRotationRole \
  --zip-file fileb://rotation-function.zip

# Enable rotation
aws secretsmanager rotate-secret \
  --secret-id leanda-ng/staging/documentdb-password \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:rotate-documentdb-password \
  --rotation-rules AutomaticallyAfterDays=30
```

### Manual Rotation

1. **Generate new secret**: Create a new password/key
2. **Update secret**: Update in AWS Secrets Manager
3. **Update application**: Restart services to pick up new secret
4. **Verify**: Confirm services are working with new secret
5. **Cleanup**: Remove old secret (after verification period)

## Security Best Practices

### 1. Least Privilege IAM Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:leanda-ng/staging/*"
    }
  ]
}
```

### 2. Encrypt Secrets

- Use KMS keys for encryption
- Enable encryption at rest
- Use TLS for secrets in transit

### 3. Audit Secret Access

```bash
# Enable CloudTrail logging
aws cloudtrail create-trail \
  --name leanda-ng-secrets-trail \
  --s3-bucket-name leanda-ng-audit-logs

# Monitor secret access
aws cloudwatch put-metric-alarm \
  --alarm-name secret-access-alert \
  --metric-name SecretAccessCount \
  --namespace AWS/SecretsManager \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold
```

### 4. Regular Rotation

- Rotate secrets every 30-90 days
- Use automated rotation when possible
- Document rotation procedures

### 5. Secret Naming Convention

Use hierarchical naming:

```
leanda-ng/{environment}/{service}/{secret-name}
```

Examples:
- `leanda-ng/staging/documentdb-password`
- `leanda-ng/production/api-key`
- `leanda-ng/staging/kafka-broker-url`

## Troubleshooting

### Secret Not Found

```bash
# Check if secret exists
aws secretsmanager describe-secret \
  --secret-id leanda-ng/staging/documentdb-password

# Verify IAM permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/ECS-Task-Role \
  --action-names secretsmanager:GetSecretValue \
  --resource-arns arn:aws:secretsmanager:us-east-1:123456789012:secret:leanda-ng/staging/documentdb-password
```

### Access Denied

1. Check IAM role permissions
2. Verify secret ARN is correct
3. Check KMS key permissions (for encrypted secrets)
4. Review CloudTrail logs for denied requests

### Secret Rotation Failed

1. Check Lambda function logs
2. Verify rotation function has correct permissions
3. Check database connectivity (for database password rotation)
4. Review Secrets Manager rotation logs

## References

- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/)
- [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Quarkus AWS Integration](https://quarkus.io/guides/amazon-services)

