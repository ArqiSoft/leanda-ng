# Deployment Guide

This guide describes how to deploy Leanda.io services to AWS using GitHub Actions CI/CD pipelines. **CI/CD is postponed until full migration is complete.**

## Overview

The deployment process uses:
- **GitHub Actions** for CI/CD automation (postponed until full migration)
- **AWS CDK** for infrastructure as code
- **OIDC** for secure AWS authentication
- **Docker** for containerized services
- **ECS Fargate** for container orchestration

## Environments

### Development
- **Branch**: `develop`
- **Purpose**: Development and testing
- **Auto-deploy**: Yes (on push to `develop`)

### Staging
- **Branch**: `develop` (deploys to staging environment)
- **Purpose**: Pre-production testing
- **Auto-deploy**: Yes (on push to `develop`)

### Production
- **Branch**: `main`
- **Purpose**: Production workloads
- **Auto-deploy**: Yes (on push to `main`, with confirmation required for manual dispatch)

## Deployment Workflows

### 1. Java Services Workflow

**File**: `.github/workflows/java-services.yml`

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

**Actions**:
- Builds all 11 Java services using Maven
- Runs unit tests
- Runs integration tests (if configured)
- Uploads test results as artifacts

**Usage**:
```bash
# Automatic on push/PR
git push origin develop

# Manual trigger
gh workflow run java-services.yml
```

### 2. Frontend Workflow

**File**: `.github/workflows/frontend.yml`

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

**Actions**:
- Lints TypeScript/Angular code
- Runs unit tests with coverage
- Builds production bundle
- Runs E2E tests with Playwright

**Usage**:
```bash
# Automatic on push/PR
git push origin develop

# Manual trigger
gh workflow run frontend.yml
```

### 3. Infrastructure Workflow

**File**: `.github/workflows/infrastructure.yml`

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

**Actions**:
- Validates CDK code
- Synthesizes CDK stacks
- Shows diff (on PRs)

**Usage**:
```bash
# Automatic on push/PR
git push origin develop

# Manual trigger
gh workflow run infrastructure.yml
```

### 4. Staging Deployment

**File**: `.github/workflows/deploy-staging.yml`

**Triggers**:
- Push to `develop` branch
- Manual workflow dispatch (with service selection)

**Actions**:
- Deploys infrastructure (CDK stacks)
- Builds Java services (Docker images)
- Builds frontend (production bundle)
- Deploys to staging environment

**Usage**:
```bash
# Automatic on push to develop
git push origin develop

# Manual trigger (deploy all)
gh workflow run deploy-staging.yml

# Manual trigger (deploy specific service)
gh workflow run deploy-staging.yml -f service=core-api
```

### 5. Production Deployment

**File**: `.github/workflows/deploy-production.yml`

**Triggers**:
- Push to `main` branch
- Manual workflow dispatch (requires confirmation)

**Actions**:
- Runs pre-deployment checks
- Deploys infrastructure (CDK stacks)
- Builds and tests Java services
- Builds and tests frontend
- Deploys to production environment
- Runs post-deployment verification

**Usage**:
```bash
# Automatic on push to main
git push origin main

# Manual trigger (requires confirmation)
gh workflow run deploy-production.yml -f confirm=deploy -f service=all
```

## Manual Deployment Steps

### Deploy Infrastructure

```bash
cd infrastructure

# Install dependencies
npm ci

# Build TypeScript
npm run build

# Configure AWS credentials
export AWS_PROFILE=leanda-staging  # or leanda-production

# Synthesize stacks
npm run synth

# Deploy all stacks
npm run deploy

# Deploy specific stack
cdk deploy leanda-ng-kms-staging
```

### ECR layout

The Compute Stack creates **one ECR repository per environment**: `leanda-ng/<env>` (e.g. `leanda-ng/dev`, `leanda-ng/staging`). Images are tagged by service name and version, not by separate repos. Full image URI format: `{account}.dkr.ecr.{region}.amazonaws.com/leanda-ng/{env}/{service}:{tag}` (e.g. `core-api:minimal`, `core-api:20250202-abc123`).

### Build and push minimal images

The five minimal service images that work on EC2 (core-api, blob-storage, imaging, office-processor, indexing) can be built locally and pushed to ECR using the same Maven order and `Dockerfile.minimal` as the EC2 test runner. Use the script:

```bash
# From repo root. Requires: AWS CLI, Docker, Maven 3.9+, Java 21, Compute Stack deployed for target env.
./scripts/build-and-push-minimal-ecr.sh --env=dev --region=us-east-1 --tag=minimal
```

- **Services**: core-api, blob-storage, imaging, office-processor, indexing.
- **ECR URI**: Resolved from CloudFormation stack output `leanda-ng-compute-<env>` (EcrRepositoryUri), or set `ECR_URI` to override.
- **Options**: `--env=dev|staging|production`, `--region=us-east-1`, `--tag=minimal|YYYYMMDD|sha`. Use an immutable tag (date or git SHA) for releases.

### Deploy a single Java service (manual)

```bash
cd services/core-api

# Build and package
mvn clean package -DskipTests

# Build Docker image (use Dockerfile.minimal for minimal distro; Dockerfile for full)
docker build -t leanda/core-api:minimal -f Dockerfile.minimal .

# Resolve ECR URI (or set ECR_URI); then tag and push to the single repo
ECR_URI=$(aws cloudformation describe-stacks --stack-name leanda-ng-compute-dev --query "Stacks[0].Outputs[?OutputKey=='EcrRepositoryUri'].OutputValue" --output text --region us-east-1)
docker tag leanda/core-api:minimal "$ECR_URI/core-api:minimal"

aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin "${ECR_URI%%/*}"

docker push "$ECR_URI/core-api:minimal"

# Update ECS service (trigger new deployment)
aws ecs update-service \
  --cluster leanda-ng-cluster-dev \
  --service core-api \
  --force-new-deployment
```

### Deploy Frontend

```bash
cd frontend

# Install dependencies
npm ci

# Build production bundle
npm run build:prod

# Deploy to S3/CloudFront (example)
aws s3 sync dist/ s3://leanda-ng-frontend-staging/ --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

## Environment Variables

### Required GitHub Secrets

| Secret Name | Description | Example |
|------------|-------------|---------|
| `AWS_ROLE_TO_ASSUME_STAGING` | IAM role ARN for staging | `arn:aws:iam::123456789012:role/GitHubActionsStagingRole` |
| `AWS_ROLE_TO_ASSUME_PRODUCTION` | IAM role ARN for production | `arn:aws:iam::123456789012:role/GitHubActionsProductionRole` |
| `AWS_ACCOUNT_ID` | AWS account ID | `123456789012` |

### CDK Environment Variables

Set these in GitHub Actions secrets or as environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment name | `development` |
| `CDK_DEFAULT_ACCOUNT` | AWS account ID | Required |
| `CDK_DEFAULT_REGION` | AWS region | `us-east-1` |
| `COST_CENTER` | Cost center tag | `engineering` |
| `OWNER` | Owner email | `leanda-team@example.com` |
| `BUDGET_ALERT_EMAILS` | Budget alert emails (comma-separated) | `leanda-team@example.com` |
| `MONTHLY_BUDGET_AMOUNT` | Monthly budget amount | Optional |

## Deployment Checklist

### Pre-Deployment

- [ ] All tests pass (unit, integration, E2E)
- [ ] Code review approved
- [ ] Infrastructure changes reviewed (CDK diff)
- [ ] Security scan passed
- [ ] Dependencies updated and secure
- [ ] Documentation updated

### Deployment

- [ ] Infrastructure deployed successfully
- [ ] Services built and tested
- [ ] Docker images pushed to ECR
- [ ] ECS services updated
- [ ] Frontend deployed to S3/CloudFront
- [ ] Health checks passing

### Post-Deployment

- [ ] Smoke tests passing
- [ ] Monitoring dashboards showing healthy metrics
- [ ] No error alerts
- [ ] Performance metrics within expected ranges
- [ ] Rollback plan ready (if needed)

## Rollback Procedures

### Rollback Infrastructure

```bash
cd infrastructure

# List previous deployments
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE

# Rollback specific stack
cdk deploy leanda-ng-compute-staging --rollback
```

### Rollback ECS Service

```bash
# List service deployments
aws ecs list-tasks --cluster leanda-ng-staging --service-name core-api

# Rollback to previous task definition
aws ecs update-service \
  --cluster leanda-ng-staging \
  --service core-api \
  --task-definition core-api:previous-version \
  --force-new-deployment
```

### Rollback Frontend

```bash
# Restore previous version from S3 versioning
aws s3 cp s3://leanda-ng-frontend-staging/previous-version/ \
  s3://leanda-ng-frontend-staging/ --recursive

# Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

## Monitoring and Verification

### Check Deployment Status

```bash
# Check ECS service status
aws ecs describe-services \
  --cluster leanda-ng-staging \
  --services core-api

# Check CloudWatch logs
aws logs tail /aws/ecs/leanda-ng-staging/core-api --follow

# Check service health
curl https://api-staging.leanda.io/health
```

### Verify Infrastructure

```bash
# List all stacks
cdk list

# Check stack status
aws cloudformation describe-stacks --stack-name leanda-ng-compute-staging

# View stack resources
aws cloudformation describe-stack-resources --stack-name leanda-ng-compute-staging
```

## Troubleshooting

### Deployment Failures

1. **Check GitHub Actions logs**: Review workflow run logs for errors
2. **Check CloudWatch logs**: Review service logs for runtime errors
3. **Check ECS service events**: Review ECS service deployment events
4. **Check CDK synthesis**: Run `cdk synth` locally to validate

### Common Issues

**Issue**: OIDC authentication fails
- **Solution**: Verify OIDC identity provider and IAM role trust policy

**Issue**: CDK deployment fails
- **Solution**: Check CDK context, verify AWS credentials, review stack events

**Issue**: ECS service fails to start
- **Solution**: Check task definition, verify container image exists in ECR, review CloudWatch logs

**Issue**: Frontend deployment fails
- **Solution**: Verify S3 bucket permissions, check CloudFront distribution status

## Best Practices

1. **Always test in staging first**: Deploy to staging before production
2. **Use feature flags**: Implement feature flags for gradual rollouts
3. **Monitor deployments**: Watch metrics and logs during deployment
4. **Have rollback plan**: Always have a rollback procedure ready
5. **Document changes**: Update documentation with deployment changes
6. **Review CDK diff**: Always review `cdk diff` before deploying infrastructure
7. **Use blue/green deployments**: For zero-downtime deployments
8. **Automate testing**: Run tests automatically before deployment

## References

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [ECS Deployment Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-best-practices.html)
- [OIDC Setup Guide](./oidc-setup.md)

