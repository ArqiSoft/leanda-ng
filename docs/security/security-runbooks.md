# Security Runbooks

**Last Updated**: 2025-12-27  
**Status**: Complete  
**Owner**: Agent PROD-4

## Overview

This document contains operational runbooks for security incidents, breaches, and access management procedures for the Leanda.io platform.

## Incident Response Procedures

### P1: Critical Security Incident

**Definition**: Active security breach, data exfiltration, or service compromise

**Response Time**: Immediate (< 15 minutes)

**Procedure**:
1. **Immediate Actions**:
   - Isolate affected systems (disable IAM roles, revoke access)
   - Preserve evidence (snapshot EBS volumes, export CloudTrail logs)
   - Notify security team via PagerDuty
   - Activate incident response team

2. **Investigation**:
   - Review CloudTrail logs for unauthorized access
   - Check GuardDuty findings
   - Review Security Hub alerts
   - Analyze VPC Flow Logs for network anomalies

3. **Containment**:
   - Revoke compromised credentials
   - Block malicious IP addresses (Security Groups, WAF)
   - Disable affected services
   - Rotate all potentially compromised secrets

4. **Recovery**:
   - Restore from backups (if data compromised)
   - Deploy security patches
   - Re-enable services after verification
   - Update security controls

5. **Post-Incident**:
   - Document incident timeline
   - Conduct root cause analysis
   - Update security procedures
   - Notify affected users (if required by GDPR)

### P2: Security Alert

**Definition**: Suspicious activity detected (GuardDuty, Security Hub)

**Response Time**: < 1 hour

**Procedure**:
1. **Investigation**:
   - Review alert details in Security Hub
   - Check CloudTrail logs for related API calls
   - Analyze affected resources
   - Determine if false positive or real threat

2. **Response**:
   - If real threat: Follow P1 procedure
   - If false positive: Document and tune alert rules
   - Update security controls if needed

3. **Documentation**:
   - Document investigation findings
   - Update runbook if new patterns identified

### P3: Security Vulnerability

**Definition**: Security vulnerability discovered (dependency scan, penetration test)

**Response Time**: < 24 hours

**Procedure**:
1. **Assessment**:
   - Determine severity (CVSS score)
   - Identify affected services
   - Check if exploit is public

2. **Remediation**:
   - Apply security patches
   - Update dependencies
   - Deploy fixes to all environments
   - Verify fix effectiveness

3. **Documentation**:
   - Document vulnerability and fix
   - Update security procedures if needed

## Security Breach Procedures

### Data Breach Notification

**GDPR Requirements**:
- Notify supervisory authority within 72 hours
- Notify affected data subjects without undue delay
- Document breach details

**Procedure**:
1. **Immediate Actions** (within 1 hour):
   - Assess scope of breach
   - Identify affected data subjects
   - Contain breach (revoke access, isolate systems)
   - Preserve evidence

2. **Notification** (within 72 hours):
   - Notify data protection officer
   - Prepare breach notification to supervisory authority
   - Prepare notification to affected data subjects
   - Document breach details

3. **Breach Notification Contents**:
   - Nature of breach
   - Categories of data subjects affected
   - Categories of personal data affected
   - Number of data subjects affected
   - Likely consequences of breach
   - Measures taken to address breach

### Access Revocation Procedures

**Immediate Access Revocation**:

1. **IAM User/Role**:
   ```bash
   # Detach all policies
   aws iam detach-user-policies --user-name <username>
   aws iam detach-role-policies --role-name <rolename>
   
   # Delete access keys
   aws iam delete-access-key --user-name <username> --access-key-id <key-id>
   
   # Delete user/role
   aws iam delete-user --user-name <username>
   aws iam delete-role --role-name <rolename>
   ```

2. **Security Groups**:
   ```bash
   # Remove ingress rules
   aws ec2 revoke-security-group-ingress \
     --group-id <sg-id> \
     --protocol tcp \
     --port 443 \
     --cidr <malicious-ip>/32
   ```

3. **Secrets Rotation**:
   ```bash
   # Rotate all potentially compromised secrets
   aws secretsmanager rotate-secret \
     --secret-id leanda-ng/production/shared/<secret-name>
   ```

4. **S3 Bucket Policy**:
   ```bash
   # Remove public access
   aws s3api put-public-access-block \
     --bucket <bucket-name> \
     --public-access-block-configuration \
     BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
   ```

### Forensic Investigation

**Evidence Collection**:

1. **CloudTrail Logs**:
   ```bash
   # Export CloudTrail logs for time period
   aws cloudtrail lookup-events \
     --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRole \
     --start-time 2025-01-01T00:00:00Z \
     --end-time 2025-01-02T00:00:00Z \
     --output json > investigation-logs.json
   ```

2. **VPC Flow Logs**:
   ```bash
   # Query VPC Flow Logs in CloudWatch Logs Insights
   # Look for suspicious IP addresses, port scans, etc.
   ```

3. **GuardDuty Findings**:
   ```bash
   # List all findings
   aws guardduty list-findings \
     --detector-id <detector-id> \
     --finding-criteria '{"Criterion":{"severity":{"Eq":["HIGH","CRITICAL"]}}}'
   ```

4. **EBS Snapshots**:
   ```bash
   # Create snapshot of affected EBS volumes
   aws ec2 create-snapshot \
     --volume-id <volume-id> \
     --description "Forensic snapshot - Incident ID: <incident-id>"
   ```

**Evidence Preservation**:
- Store evidence in separate S3 bucket (encrypted)
- Enable versioning on evidence bucket
- Document chain of custody
- Retain evidence for required period (7 years for production)

## Access Management Procedures

### User Access Provisioning

**Procedure**:
1. **Request**: User submits access request via ticketing system
2. **Approval**: Manager approves access request
3. **Provisioning**:
   - Create IAM user (if needed)
   - Assign IAM role to user
   - Create access keys (if needed)
   - Configure MFA
   - Grant access to required resources
4. **Documentation**: Document access in access management system
5. **Notification**: Notify user of access grant

### User Access Deprovisioning

**Procedure**:
1. **Trigger**: User termination, role change, or access revocation request
2. **Immediate Actions**:
   - Revoke all access keys
   - Detach all IAM policies
   - Remove from IAM groups
   - Delete IAM user (if applicable)
3. **Cleanup**:
   - Remove from service-specific access lists
   - Revoke Secrets Manager access
   - Revoke Parameter Store access
4. **Documentation**: Document access revocation
5. **Verification**: Verify access has been revoked

### Access Review

**Quarterly Access Review**:

1. **Preparation**:
   - Generate access report (IAM users, roles, policies)
   - List all service roles and permissions
   - Review Secrets Manager access
   - Review Parameter Store access

2. **Review**:
   - Verify users still need access
   - Verify service roles have correct permissions
   - Identify unused access
   - Identify over-privileged access

3. **Remediation**:
   - Revoke unused access
   - Reduce over-privileged access
   - Update IAM policies
   - Document changes

4. **Documentation**:
   - Document review findings
   - Document remediation actions
   - Update access management procedures

## Security Monitoring Procedures

### Daily Security Review

**Tasks**:
1. Review GuardDuty findings
2. Review Security Hub alerts
3. Check CloudTrail for suspicious activity
4. Review failed authentication attempts
5. Check for unauthorized API calls

**Tools**:
- AWS Security Hub dashboard
- GuardDuty console
- CloudWatch Logs Insights
- CloudTrail event history

### Weekly Security Review

**Tasks**:
1. Review IAM access patterns
2. Review Secrets Manager access logs
3. Check for security policy violations
4. Review dependency vulnerabilities
5. Review security configuration changes

### Monthly Security Review

**Tasks**:
1. Conduct access review
2. Review security metrics and trends
3. Update security procedures
4. Review compliance status
5. Plan security improvements

## Emergency Contacts

**Security Team**:
- PagerDuty: [Security On-Call]
- Email: security@leanda.io
- Slack: #security-incidents

**AWS Support**:
- Support Plan: Enterprise
- Support Center: https://console.aws.amazon.com/support

**Data Protection Officer**:
- Email: dpo@leanda.io

## References

- [AWS Security Incident Response Guide](https://aws.amazon.com/security/incident-response/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [GDPR Breach Notification](https://gdpr.eu/data-breach-notification/)

