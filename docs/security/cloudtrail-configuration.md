# CloudTrail Configuration

**Last Updated**: 2025-12-27  
**Status**: Complete  
**Owner**: Agent PROD-4

## Overview

This document describes the CloudTrail configuration for Leanda.io platform, providing comprehensive audit logging of all AWS API calls for security, compliance, and operational monitoring.

## Architecture

### Account-Level Trail

**Purpose**: Log all API calls across the AWS account

**Configuration**:
- **Trail Name**: `leanda-ng-account-trail-{environment}`
- **Multi-Region**: Enabled (logs from all regions)
- **Global Services**: Enabled (logs IAM, CloudFront, Route 53)
- **Log File Validation**: Enabled (integrity verification)
- **S3 Bucket**: `leanda-ng-cloudtrail-{environment}-{account-id}`
- **SNS Topic**: `leanda-ng-cloudtrail-alerts-{environment}`

### Event Types

#### Management Events

**Log All Management Events**:
- **Read Events**: API calls that read resources (e.g., `DescribeInstances`)
- **Write Events**: API calls that modify resources (e.g., `CreateInstance`, `DeleteBucket`)

**Examples**:
- EC2: `RunInstances`, `TerminateInstances`, `DescribeInstances`
- S3: `CreateBucket`, `DeleteBucket`, `PutObject`, `GetObject`
- IAM: `CreateUser`, `DeleteUser`, `AttachUserPolicy`
- Lambda: `CreateFunction`, `UpdateFunction`, `InvokeFunction`
- ECS: `CreateService`, `UpdateService`, `RunTask`

#### Data Events

**S3 Data Events**:
- **Read Events**: `GetObject`, `HeadObject`
- **Write Events**: `PutObject`, `DeleteObject`
- **Resources**: All S3 buckets in account
- **Note**: Data events generate high volume - enable selectively

**Lambda Data Events**:
- **Invoke Events**: `InvokeFunction`
- **Resources**: All Lambda functions in account

### Log File Storage

#### S3 Bucket Configuration

**Bucket Name**: `leanda-ng-cloudtrail-{environment}-{account-id}`

**Properties**:
- **Encryption**: SSE-KMS (customer-managed key)
- **Versioning**: Enabled
- **Lifecycle Rules**:
  - Transition to Standard-IA after 30 days
  - Transition to Glacier after 90 days
  - Transition to Deep Archive after 1 year
  - Delete after 7 years (production), 90 days (development)
- **Public Access**: Blocked
- **Bucket Policy**: Only CloudTrail service can write

**Bucket Policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSCloudTrailAclCheck",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::leanda-ng-cloudtrail-{environment}-{account-id}"
    },
    {
      "Sid": "AWSCloudTrailWrite",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::leanda-ng-cloudtrail-{environment}-{account-id}/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "bucket-owner-full-control"
        }
      }
    }
  ]
}
```

### Log File Validation

**Purpose**: Detect tampering or deletion of log files

**Configuration**:
- **Enabled**: Yes
- **Method**: SHA-256 hash of log file
- **Validation File**: `.digest` file in S3 bucket
- **Verification**: Use `aws cloudtrail validate-logs` command

### SNS Notifications

**Topic**: `leanda-ng-cloudtrail-alerts-{environment}`

**Notifications**:
- Trail creation/update/deletion
- Log file delivery failures
- Configuration changes

**Subscribers**:
- Security team email
- PagerDuty (for critical alerts)
- Slack channel (for operational alerts)

## Event Logging Details

### Logged Information

Each log entry contains:
- **Event Time**: Timestamp of API call
- **User Identity**: IAM user, role, or service
- **Event Source**: AWS service (e.g., `ec2.amazonaws.com`)
- **Event Name**: API action (e.g., `RunInstances`)
- **AWS Region**: Region where API call was made
- **Source IP**: IP address of caller
- **User Agent**: Client application
- **Request Parameters**: API request parameters
- **Response Elements**: API response (if applicable)
- **Resources**: AWS resources affected

### Sensitive Data

**Redacted Fields**:
- Passwords in `CreateUser`, `ChangePassword`
- Secret access keys in `CreateAccessKey`
- Database passwords in RDS API calls
- Private keys in certificate operations

**Note**: Sensitive data is automatically redacted by CloudTrail

## Monitoring and Alerting

### CloudWatch Metrics

**Metrics**:
- `CloudTrailEventCount`: Number of events logged
- `CloudTrailInsightEventCount`: Number of insight events

**Alarms**:
- High API call volume (potential attack)
- Failed API calls (unauthorized access attempts)
- Log file delivery failures

### CloudWatch Logs Insights

**Queries**:
```sql
-- Find all S3 bucket deletions
fields @timestamp, userIdentity.arn, eventName, requestParameters.bucketName
| filter eventName = "DeleteBucket"
| sort @timestamp desc

-- Find all IAM policy changes
fields @timestamp, userIdentity.arn, eventName, requestParameters
| filter eventName like /Put.*Policy/ or eventName like /Attach.*Policy/
| sort @timestamp desc

-- Find all failed API calls
fields @timestamp, userIdentity.arn, eventName, errorCode, errorMessage
| filter errorCode != ""
| sort @timestamp desc
```

### Security Hub Integration

CloudTrail findings automatically sent to Security Hub:
- Unauthorized API calls
- Privilege escalation attempts
- Resource deletion attempts
- Configuration changes

## Compliance and Audit

### Compliance Requirements

**GDPR**:
- Log all data access operations
- Retain logs for required period
- Enable log file validation

**Scientific Data Regulations**:
- Log all data processing operations
- Audit trail for data access
- Data retention policies

**AWS Well-Architected Framework**:
- Comprehensive audit logging
- Log integrity verification
- Centralized log storage

### Audit Trail

**Retention**:
- **Production**: 7 years
- **Development**: 90 days

**Access**:
- Security team: Full access
- Compliance team: Read-only access
- Developers: No access (except via CloudWatch Logs Insights)

### Log Analysis

**Tools**:
- CloudWatch Logs Insights
- AWS Athena (query S3 logs)
- Third-party SIEM tools (Splunk, Datadog)

**Reports**:
- Monthly security audit reports
- Quarterly compliance reports
- Annual audit reports

## Best Practices

1. **Enable Multi-Region**: Log events from all regions
2. **Enable Global Services**: Log IAM, CloudFront, Route 53 events
3. **Enable Log File Validation**: Detect tampering
4. **Encrypt Log Files**: Use KMS customer-managed keys
5. **Monitor Log Delivery**: Alert on delivery failures
6. **Regular Reviews**: Review logs for suspicious activity
7. **Access Control**: Limit access to CloudTrail logs
8. **Lifecycle Management**: Archive old logs to reduce costs

## Cost Optimization

### Data Events

**Recommendation**: Enable data events selectively
- High volume (can generate millions of events)
- High cost (charged per event)
- Enable only for critical buckets/functions

### Lifecycle Policies

**S3 Lifecycle**:
- Move to Standard-IA after 30 days
- Move to Glacier after 90 days
- Move to Deep Archive after 1 year
- Delete after retention period

**Cost Savings**: 60-80% reduction in storage costs

## Troubleshooting

### Log File Delivery Failures

**Common Causes**:
- S3 bucket permissions incorrect
- S3 bucket doesn't exist
- KMS key permissions incorrect

**Resolution**:
1. Check S3 bucket policy
2. Verify CloudTrail service role
3. Check KMS key policy
4. Review CloudTrail event history

### Missing Events

**Common Causes**:
- Trail not enabled in region
- Data events not enabled
- Global services not enabled

**Resolution**:
1. Verify trail configuration
2. Check event selectors
3. Review CloudTrail event history

## References

- [AWS CloudTrail Documentation](https://docs.aws.amazon.com/cloudtrail/)
- [CloudTrail Best Practices](https://docs.aws.amazon.com/cloudtrail/latest/userguide/cloudtrail-best-practices.html)
- [CloudTrail Log File Validation](https://docs.aws.amazon.com/cloudtrail/latest/userguide/cloudtrail-log-file-validation.html)

