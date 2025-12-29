# OIDC Setup for GitHub Actions

This document describes how to configure OpenID Connect (OIDC) for GitHub Actions to authenticate with AWS without storing long-lived credentials.

## Overview

OIDC allows GitHub Actions to assume AWS IAM roles using short-lived tokens, eliminating the need to store AWS access keys as secrets. This is more secure and follows AWS best practices.

## Prerequisites

- AWS Account with appropriate permissions
- GitHub repository
- AWS CLI configured (for setup commands)

## Setup Steps

### 1. Create OIDC Identity Provider in AWS

Run the following AWS CLI command to create the OIDC identity provider:

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1 \
  --tags Key=Project,Value=leanda-ng Key=ManagedBy,Value=CDK
```

**Note**: The thumbprint may change. Verify the current thumbprint at:
https://github.com/orgs/community/discussions/25381

### 2. Create IAM Roles for Each Environment

Create separate IAM roles for staging and production environments.

#### Staging Role

```bash
# Create trust policy for staging
cat > staging-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:YOUR_ORG/leanda:*"
        }
      }
    }
  ]
}
EOF

# Create role
aws iam create-role \
  --role-name GitHubActionsStagingRole \
  --assume-role-policy-document file://staging-trust-policy.json \
  --tags Key=Project,Value=leanda-ng Key=Environment,Value=staging
```

#### Production Role

```bash
# Create trust policy for production (more restrictive)
cat > production-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:YOUR_ORG/leanda:ref:refs/heads/main"
        }
      }
    }
  ]
}
EOF

# Create role
aws iam create-role \
  --role-name GitHubActionsProductionRole \
  --assume-role-policy-document file://production-trust-policy.json \
  --tags Key=Project,Value=leanda-ng Key=Environment,Value=production
```

### 3. Attach Policies to Roles

Attach the necessary policies to each role. For CDK deployments, you'll need:

```bash
# Attach CDK deployment policy (or create custom policy)
aws iam attach-role-policy \
  --role-name GitHubActionsStagingRole \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess

# For production, use more restrictive policies
aws iam attach-role-policy \
  --role-name GitHubActionsProductionRole \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess
```

**Note**: In production, create custom IAM policies with least-privilege permissions instead of PowerUserAccess.

### 4. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:

| Secret Name | Value | Description |
|------------|-------|-------------|
| `AWS_ROLE_TO_ASSUME_STAGING` | `arn:aws:iam::ACCOUNT_ID:role/GitHubActionsStagingRole` | IAM role ARN for staging |
| `AWS_ROLE_TO_ASSUME_PRODUCTION` | `arn:aws:iam::ACCOUNT_ID:role/GitHubActionsProductionRole` | IAM role ARN for production |
| `AWS_ACCOUNT_ID` | `123456789012` | Your AWS account ID |

### 5. Update Workflow Files

The workflow files are already configured to use OIDC. They use the `aws-actions/configure-aws-credentials@v4` action with the `role-to-assume` parameter.

Example from `.github/workflows/infrastructure.yml`:

```yaml
- name: Configure AWS credentials (OIDC)
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME_STAGING }}
    aws-region: us-east-1
```

## Verification

### Test OIDC Authentication

1. Push a commit to the `develop` branch
2. Check the GitHub Actions workflow run
3. Verify that the "Configure AWS credentials (OIDC)" step succeeds
4. Check CloudTrail logs to confirm the role assumption

### Verify Role Permissions

```bash
# Test role assumption
aws sts assume-role-with-web-identity \
  --role-arn arn:aws:iam::ACCOUNT_ID:role/GitHubActionsStagingRole \
  --role-session-name test-session \
  --web-identity-token $(gh auth token)
```

## Security Best Practices

1. **Separate Roles**: Use different IAM roles for staging and production
2. **Least Privilege**: Grant only the minimum permissions required
3. **Branch Restrictions**: Restrict production role to `main` branch only
4. **Audit Logging**: Enable CloudTrail to audit all role assumptions
5. **Regular Review**: Periodically review and rotate role permissions

## Troubleshooting

### Error: "Not authorized to perform sts:AssumeRoleWithWebIdentity"

- Verify the OIDC identity provider is created correctly
- Check the trust policy conditions match your repository
- Ensure the role ARN in GitHub secrets is correct

### Error: "The request signature we calculated does not match"

- Verify the OIDC provider thumbprint is correct
- Check that the identity provider URL is exactly: `https://token.actions.githubusercontent.com`

### Error: "Access Denied"

- Verify the IAM role has the necessary permissions
- Check that the branch condition in the trust policy matches your workflow trigger

## References

- [GitHub Actions OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [AWS IAM OIDC Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
- [AWS CDK Deployment Guide](https://docs.aws.amazon.com/cdk/v2/guide/cli.html)

