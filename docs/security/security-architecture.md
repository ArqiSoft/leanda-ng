# Security Architecture

**Last Updated**: 2025-12-27  
**Status**: In Progress  
**Owner**: Agent PROD-4

## Overview

This document describes the comprehensive security architecture for Leanda.io platform, designed to meet enterprise security requirements, compliance standards (GDPR, scientific data regulations), and AWS Well-Architected Framework security pillar best practices.

## Security Principles

1. **Defense in Depth**: Multiple layers of security controls
2. **Least Privilege**: Minimum permissions required for functionality
3. **Zero Trust**: Never trust, always verify
4. **Encryption Everywhere**: Data encrypted at rest and in transit
5. **Security by Design**: Security built into architecture from the start
6. **Continuous Monitoring**: Real-time threat detection and response

## Security Architecture Components

### 1. Identity and Access Management (IAM)

#### Service Roles
- **Service-Specific Roles**: Each microservice has its own IAM role with least privilege permissions
- **ECS Task Roles**: Separate roles for task execution and application runtime
- **Lambda Execution Roles**: Dedicated roles for serverless functions

#### Access Control
- **Role-Based Access Control (RBAC)**: IAM roles mapped to service responsibilities
- **Resource-Based Policies**: S3 bucket policies, KMS key policies
- **Condition Keys**: Additional security through IAM conditions (IP restrictions, time-based access)

#### Service Roles Created
- `leanda-ng-core-api-{environment}`
- `leanda-ng-blob-storage-{environment}`
- `leanda-ng-indexing-{environment}`
- `leanda-ng-metadata-processing-{environment}`
- `leanda-ng-chemical-parser-{environment}`
- `leanda-ng-chemical-properties-{environment}`
- `leanda-ng-reaction-parser-{environment}`
- `leanda-ng-crystal-parser-{environment}`
- `leanda-ng-spectra-parser-{environment}`
- `leanda-ng-imaging-{environment}`
- `leanda-ng-office-processor-{environment}`

#### Permissions by Service Type
- **Database Services**: DocumentDB connect permissions (scoped to service-specific database users)
- **Storage Services**: S3 read/write permissions (scoped to specific buckets and prefixes)
- **Messaging Services**: Kafka/MSK permissions (scoped to specific topics)
- **Event Publishers**: EventBridge publish permissions (scoped to custom event bus)

### 2. Encryption

#### Encryption at Rest

**KMS Keys** (Customer-Managed Keys):
- **S3 Key**: Encrypts S3 buckets (data and artifacts)
- **DocumentDB Key**: Encrypts DocumentDB cluster
- **Secrets Key**: Encrypts Secrets Manager secrets
- **Logs Key**: Encrypts CloudWatch Logs
- **EBS Key**: Encrypts EBS volumes

**Key Rotation**: All keys have automatic key rotation enabled (annual rotation)

**Encrypted Resources**:
- S3 buckets: KMS encryption (SSE-KMS)
- DocumentDB: Encryption at rest with KMS
- Secrets Manager: KMS encryption
- CloudWatch Logs: KMS encryption
- EBS volumes: KMS encryption

#### Encryption in Transit

- **TLS 1.2+**: Enforced for all API endpoints
- **API Gateway**: SSL/TLS termination
- **VPC Endpoints**: Private connectivity to AWS services
- **S3**: Enforce SSL/TLS (`enforceSSL: true`)
- **DocumentDB**: TLS required for connections
- **Kafka/MSK**: TLS encryption for message brokers

### 3. Network Security

#### VPC Architecture
- **Public Subnets**: Load balancers, NAT gateways
- **Private Subnets**: ECS services, application workloads
- **Isolated Subnets**: Databases (DocumentDB, Redis)

#### Security Groups
- **Least Privilege Rules**: Only required ports and protocols
- **ECS Security Group**: 
  - HTTPS outbound (443)
  - HTTP outbound (80) - for package repositories
  - DNS outbound (53)
  - No inbound rules (services accessed via load balancer)
- **Database Security Groups**: Only allow connections from ECS security group

#### VPC Flow Logs
- **Enabled**: All VPC traffic logged to CloudWatch Logs
- **Retention**: 1 year (production), 1 month (development)
- **Encryption**: KMS-encrypted log group
- **Purpose**: Network monitoring, security analysis, compliance

#### VPC Endpoints
- **S3 Gateway Endpoint**: Private S3 access (no cost)
- **DynamoDB Gateway Endpoint**: Private DynamoDB access (no cost)
- **Interface Endpoints** (Production only):
  - Secrets Manager
  - Systems Manager
  - CloudWatch Logs

#### Network ACLs
- Default NACLs with deny-all inbound/outbound (except required traffic)

### 4. Security Monitoring and Detection

#### AWS GuardDuty
- **Threat Detection**: Continuous monitoring for malicious activity
- **Data Sources**:
  - VPC Flow Logs
  - CloudTrail logs
  - S3 data events
  - Malware protection (EBS volumes)
- **Finding Frequency**: 15 minutes
- **Alerts**: SNS topic for security alerts

#### Amazon Macie
- **Data Discovery**: Automatically discovers sensitive data in S3
- **Data Protection**: Monitors data access patterns
- **Status**: Enabled in production, paused in development
- **Finding Frequency**: 15 minutes

#### AWS Security Hub
- **Centralized Findings**: Aggregates findings from GuardDuty, Macie, Config
- **Security Standards**: CIS AWS Foundations Benchmark (production)
- **Compliance Monitoring**: Continuous compliance assessment

#### AWS Config
- **Compliance Rules**: 
  - S3 bucket encryption
  - S3 public access blocked
  - EBS encryption
  - IAM password policy
  - CloudTrail enabled
  - VPC Flow Logs enabled
  - RDS encryption
  - Security group rules
  - Lambda public access prohibited
- **Delivery Channel**: S3 bucket for Config snapshots
- **Recorder**: Records all resource configurations

### 5. Secrets Management

#### AWS Secrets Manager
- **Purpose**: Store sensitive credentials (database passwords, API keys)
- **Encryption**: KMS customer-managed key
- **Rotation**: Automated secret rotation (where supported)
- **Access Control**: Service-specific IAM roles with least privilege

#### Systems Manager Parameter Store
- **Purpose**: Store non-sensitive configuration
- **SecureString**: For sensitive parameters (encrypted with KMS)
- **Standard**: For non-sensitive configuration
- **Access Control**: Service-specific IAM roles

#### Secret Naming Convention
- Service-specific: `{projectName}/{environment}/{serviceName}/{secretName}`
- Shared: `{projectName}/{environment}/shared/{secretName}`

### 6. Audit and Compliance

#### CloudTrail
- **Account-Level Trail**: Logs all API calls
- **Log File Validation**: Enabled for integrity verification
- **S3 Storage**: Encrypted log files in dedicated S3 bucket
- **Retention**: 7 years (production), 90 days (development)
- **Event Types**: Management events, data events (S3, Lambda)

#### CloudWatch Logs
- **Log Groups**: Service-specific log groups
- **Retention**: 1 year (production), 1 week (development)
- **Encryption**: KMS encryption
- **Access Control**: IAM roles for log access

#### Compliance Frameworks
- **GDPR**: Data protection, data subject rights, breach notification
- **Scientific Data Regulations**: Domain-specific compliance requirements
- **AWS Well-Architected Framework**: Security pillar compliance

### 7. Application Security

#### Input Validation
- **API Gateway**: Request validation
- **Application Layer**: Input sanitization and validation
- **File Uploads**: Type, size, content validation

#### Authentication and Authorization
- **OIDC/OAuth2**: User authentication (Keycloak integration)
- **API Keys**: For service-to-service communication
- **IAM Roles**: For AWS service access

#### Rate Limiting
- **API Gateway**: Throttling and rate limiting
- **Application Layer**: Per-user rate limits

### 8. Data Protection

#### Data Classification
- **PII**: Personally Identifiable Information
- **Scientific Data**: Research data, experimental results
- **Public Data**: Publicly accessible data

#### Data Handling Procedures
- **Encryption**: All data encrypted at rest and in transit
- **Access Control**: Least privilege access
- **Data Retention**: Configurable retention policies
- **Data Deletion**: Secure deletion procedures

#### Data Residency
- **Region**: All data stored in specified AWS region
- **Cross-Region Replication**: Disabled (unless required for compliance)

## Security Stack Dependencies

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

## Security Incident Response

See [Security Runbooks](./security-runbooks.md) for:
- Incident response procedures
- Security breach procedures
- Access revocation procedures
- Forensics and investigation procedures

## Compliance Documentation

See [Compliance Framework](./compliance-framework.md) for:
- GDPR compliance procedures
- Scientific data regulations
- Data subject rights
- Data breach notification procedures

## Security Best Practices

1. **Regular Security Audits**: Quarterly security reviews
2. **Penetration Testing**: Annual penetration testing
3. **Dependency Scanning**: Continuous dependency vulnerability scanning
4. **Security Training**: Regular security training for development team
5. **Security Updates**: Prompt patching of security vulnerabilities
6. **Access Reviews**: Quarterly IAM access reviews

## References

- [AWS Well-Architected Framework - Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [GDPR Compliance Guide](https://gdpr.eu/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

