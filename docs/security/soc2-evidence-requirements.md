# SOC 2 Type II Evidence Requirements

**Last Updated**: 2026-01-10  
**Status**: In Progress  
**Owner**: Agent PROD-7

## Overview

This document defines the evidence requirements for each SOC 2 Type II control. Evidence must demonstrate that controls are designed appropriately and operating effectively over time (typically 6-12 months for Type II).

## Evidence Collection Principles

1. **Automated Collection**: Prefer automated evidence collection where possible
2. **Retention**: Maintain evidence for 7 years (production), 1 year (development/staging)
3. **Integrity**: Protect evidence from tampering (encryption, versioning, access controls)
4. **Accessibility**: Store evidence in accessible locations for audit review
5. **Completeness**: Collect sufficient evidence to demonstrate control effectiveness

## Evidence Storage

### Primary Storage Locations

- **AWS S3**: Encrypted S3 bucket for evidence storage
  - Bucket: `leanda-ng-{environment}-soc2-evidence`
  - Encryption: KMS customer-managed key
  - Versioning: Enabled
  - Lifecycle: 7-year retention for production

- **CloudWatch Logs**: Log groups for automated evidence
  - Retention: 1 year (configurable)
  - Encryption: KMS encryption

- **AWS Config**: Configuration compliance evidence
  - Retention: 7 years
  - S3 storage for snapshots

- **CloudTrail**: Audit trail evidence
  - Retention: 7 years (production), 90 days (development)
  - S3 storage with encryption

### Evidence Organization

```
s3://leanda-ng-{environment}-soc2-evidence/
├── cc6-security/
│   ├── access-controls/
│   ├── encryption/
│   ├── network-security/
│   └── security-monitoring/
├── cc7-availability/
│   ├── monitoring/
│   ├── incident-response/
│   └── business-continuity/
├── cc8-processing-integrity/
│   ├── data-validation/
│   ├── error-detection/
│   └── processing-completeness/
├── cc6.7-confidentiality/
│   ├── data-classification/
│   ├── access-controls/
│   └── data-disposal/
└── privacy/
    ├── notice-choice/
    ├── collection-use/
    └── access-correction/
```

## CC6: Security Evidence Requirements

### CC6.1: Logical and Physical Access Controls

**Evidence Required**:
- IAM policy documents (JSON format)
- Security group configurations
- VPC configuration documentation
- Access control matrix
- Quarterly access review reports

**Collection Method**: Automated (CloudTrail, Config) + Manual (documentation)
**Frequency**: Continuous (automated), Quarterly (reviews)
**Retention**: 7 years

### CC6.2: User Access Provisioning and Deprovisioning

**Evidence Required**:
- IAM role creation/deletion logs (CloudTrail)
- Access provisioning procedures
- Access deprovisioning procedures
- Monthly access review reports
- IAM Access Analyzer findings

**Collection Method**: Automated (CloudTrail, IAM Access Analyzer)
**Frequency**: Continuous (automated), Monthly (reviews)
**Retention**: 7 years

### CC6.3: Authentication and Authorization

**Evidence Required**:
- IAM authentication logs (CloudTrail)
- MFA configuration documentation
- Authorization policy documents
- Failed authentication attempt logs
- Daily authentication reports

**Collection Method**: Automated (CloudTrail, IAM logs)
**Frequency**: Continuous
**Retention**: 7 years

### CC6.4: Encryption of Data at Rest

**Evidence Required**:
- KMS key configuration documentation
- S3 bucket encryption settings (Config)
- DocumentDB encryption settings (Config)
- OpenSearch encryption settings (Config)
- Monthly encryption verification reports

**Collection Method**: Automated (AWS Config, KMS logs)
**Frequency**: Continuous (automated), Monthly (verification)
**Retention**: 7 years

### CC6.5: Encryption of Data in Transit

**Evidence Required**:
- TLS configuration documentation
- VPC endpoint configurations
- Certificate management records
- Monthly encryption verification reports
- VPC Flow Logs (sample)

**Collection Method**: Automated (Config, VPC Flow Logs)
**Frequency**: Continuous (automated), Monthly (verification)
**Retention**: 7 years

### CC6.6: Network Security

**Evidence Required**:
- VPC configuration documentation
- Security group rules (Config)
- Network ACL configurations
- WAF rule configurations
- Weekly security group review reports
- VPC Flow Logs (sample)

**Collection Method**: Automated (Config, VPC Flow Logs, WAF logs)
**Frequency**: Continuous (automated), Weekly (reviews)
**Retention**: 7 years

### CC6.7: Security Monitoring

**Evidence Required**:
- GuardDuty findings reports (weekly)
- Security Hub compliance reports (weekly)
- CloudWatch security alarms
- Security incident logs
- Daily security monitoring reports

**Collection Method**: Automated (GuardDuty, Security Hub, CloudWatch)
**Frequency**: Continuous (automated), Daily (reports)
**Retention**: 7 years

### CC6.8: Incident Response

**Evidence Required**:
- Incident response procedures
- Incident response logs
- CloudWatch alarm configurations
- SNS topic configurations
- Incident resolution reports

**Collection Method**: Manual (procedures) + Automated (logs, alarms)
**Frequency**: As needed (incidents), Quarterly (procedure review)
**Retention**: 7 years

### CC6.9: Change Management

**Evidence Required**:
- Git commit history (infrastructure changes)
- CDK deployment logs
- Change approval records
- Change testing results
- Change documentation

**Collection Method**: Automated (Git, CDK) + Manual (approvals)
**Frequency**: Per change
**Retention**: 7 years

### CC6.10: Vulnerability Management

**Evidence Required**:
- Security Hub vulnerability findings (weekly)
- Dependency scanning reports
- Vulnerability remediation records
- Patch management records
- Weekly vulnerability reports

**Collection Method**: Automated (Security Hub, dependency scanners)
**Frequency**: Continuous (automated), Weekly (reports)
**Retention**: 7 years

## CC7: Availability Evidence Requirements

### CC7.1: System Availability Monitoring

**Evidence Required**:
- CloudWatch availability dashboards (screenshots)
- Service availability metrics (daily)
- SLO compliance reports (monthly)
- Availability trend analysis (quarterly)

**Collection Method**: Automated (CloudWatch)
**Frequency**: Continuous (automated), Daily (metrics), Monthly (reports)
**Retention**: 7 years

### CC7.2: Incident Response Procedures

**Evidence Required**:
- Incident response runbook
- Incident logs
- Incident resolution times
- Post-incident review reports
- Quarterly runbook review

**Collection Method**: Manual (runbook) + Automated (logs)
**Frequency**: As needed (incidents), Quarterly (review)
**Retention**: 7 years

### CC7.3: System Availability Commitments

**Evidence Required**:
- SLO definitions document
- Monthly SLO compliance reports
- Availability SLA reports
- Service availability statistics

**Collection Method**: Automated (CloudWatch, SLO tracking)
**Frequency**: Monthly
**Retention**: 7 years

### CC7.4: Business Continuity Planning

**Evidence Required**:
- Business continuity plan document
- Disaster recovery plan document
- RTO/RPO definitions
- Annual DR test results
- Quarterly plan review records

**Collection Method**: Manual (documentation, test results)
**Frequency**: Quarterly (review), Annually (testing)
**Retention**: 7 years

### CC7.5: Capacity Planning

**Evidence Required**:
- Capacity planning procedures
- Resource utilization reports (monthly)
- Auto-scaling configuration
- Capacity planning review records
- Resource growth projections

**Collection Method**: Automated (CloudWatch metrics) + Manual (procedures)
**Frequency**: Monthly (reports), Quarterly (review)
**Retention**: 7 years

### CC7.6: System Backup and Recovery

**Evidence Required**:
- DocumentDB backup logs (daily)
- S3 versioning configuration
- Backup retention policies
- Recovery test results (quarterly)
- Backup verification reports (weekly)

**Collection Method**: Automated (backup logs, Config)
**Frequency**: Continuous (backups), Weekly (verification), Quarterly (testing)
**Retention**: 7 years

## CC8: Processing Integrity Evidence Requirements

### CC8.1: Data Validation

**Evidence Required**:
- Input validation procedures
- File upload validation logs
- Data format validation logs
- Schema validation results
- Daily validation reports

**Collection Method**: Automated (application logs)
**Frequency**: Continuous (automated), Daily (reports)
**Retention**: 7 years

### CC8.2: Error Detection and Correction

**Evidence Required**:
- Error logging procedures
- Error logs (daily)
- Error correction records
- Error trend analysis (monthly)
- Error resolution reports

**Collection Method**: Automated (application logs, CloudWatch)
**Frequency**: Continuous (automated), Daily (logs), Monthly (analysis)
**Retention**: 7 years

### CC8.3: Processing Completeness

**Evidence Required**:
- Transaction logging procedures
- Transaction logs (daily)
- Processing workflow documentation
- Completeness check results (weekly)
- Data reconciliation reports (monthly)

**Collection Method**: Automated (transaction logs) + Manual (procedures)
**Frequency**: Continuous (automated), Weekly (checks), Monthly (reconciliation)
**Retention**: 7 years

### CC8.4: Processing Accuracy

**Evidence Required**:
- Data validation procedures
- Validation logs (daily)
- Accuracy reports (weekly)
- Data quality metrics
- Accuracy trend analysis (monthly)

**Collection Method**: Automated (validation logs, metrics)
**Frequency**: Continuous (automated), Weekly (reports), Monthly (analysis)
**Retention**: 7 years

### CC8.5: Processing Authorization

**Evidence Required**:
- Authorization procedures
- Authorization logs (CloudTrail)
- Processing workflow approvals
- Authorization audit reports (monthly)
- Unauthorized access attempt logs

**Collection Method**: Automated (CloudTrail, application logs)
**Frequency**: Continuous (automated), Monthly (reports)
**Retention**: 7 years

### CC8.6: Processing Timeliness

**Evidence Required**:
- Performance monitoring procedures
- Performance metrics (daily)
- SLA compliance reports (monthly)
- Processing time trend analysis
- Performance optimization records

**Collection Method**: Automated (CloudWatch, application metrics)
**Frequency**: Continuous (automated), Daily (metrics), Monthly (reports)
**Retention**: 7 years

## CC6.7: Confidentiality Evidence Requirements

### CC6.7.1: Confidential Data Classification

**Evidence Required**:
- Data classification framework document
- Data classification inventory
- Classification review records (quarterly)
- Classification training records

**Collection Method**: Manual (documentation, inventory)
**Frequency**: Quarterly (review)
**Retention**: 7 years

### CC6.7.2: Confidential Data Access Controls

**Evidence Required**:
- Confidential data access policies
- Access logs (CloudTrail, application logs)
- Access review reports (monthly)
- Unauthorized access attempt logs

**Collection Method**: Automated (CloudTrail, logs)
**Frequency**: Continuous (automated), Monthly (reviews)
**Retention**: 7 years

### CC6.7.3: Confidential Data Handling Procedures

**Evidence Required**:
- Confidential data handling procedures document
- Handling procedure training records
- Procedure compliance reports (quarterly)
- Handling incident logs

**Collection Method**: Manual (procedures, training records)
**Frequency**: Quarterly (reviews)
**Retention**: 7 years

### CC6.7.4: Confidential Data Retention

**Evidence Required**:
- Confidential data retention policies
- Retention schedules
- Retention compliance reports (monthly)
- Data retention inventory

**Collection Method**: Manual (policies, schedules) + Automated (compliance)
**Frequency**: Monthly (compliance), Quarterly (review)
**Retention**: 7 years

### CC6.7.5: Confidential Data Disposal

**Evidence Required**:
- Confidential data disposal procedures
- Disposal records
- Disposal verification records
- Annual disposal audit results

**Collection Method**: Manual (procedures, records)
**Frequency**: As needed (disposal), Annually (audit)
**Retention**: 7 years

### CC6.7.6: Confidential Data Monitoring

**Evidence Required**:
- Macie findings reports (daily)
- Confidential data access logs
- Monitoring alert logs
- Monthly monitoring reports

**Collection Method**: Automated (Macie, access logs)
**Frequency**: Continuous (automated), Daily (reports)
**Retention**: 7 years

## P1-P9: Privacy Evidence Requirements

### P1: Notice and Choice

**Evidence Required**:
- Privacy policy document
- Privacy notice distribution records
- Consent records
- Quarterly privacy policy review

**Collection Method**: Manual (policy, records)
**Frequency**: Quarterly (review)
**Retention**: 7 years

### P2: Collection

**Evidence Required**:
- Data collection procedures
- Collection purpose documentation
- Collection logs
- Monthly collection review

**Collection Method**: Manual (procedures) + Automated (logs)
**Frequency**: Monthly (review)
**Retention**: 7 years

### P3: Use and Retention

**Evidence Required**:
- Data retention policies
- Retention schedules
- Data deletion logs
- Monthly retention compliance reports

**Collection Method**: Manual (policies) + Automated (logs)
**Frequency**: Monthly (compliance)
**Retention**: 7 years

### P4: Access

**Evidence Required**:
- Data subject access procedures
- Access request logs
- Access response records
- Access request statistics (quarterly)

**Collection Method**: Manual (procedures, requests)
**Frequency**: As needed (requests), Quarterly (statistics)
**Retention**: 7 years

### P5: Disclosure to Third Parties

**Evidence Required**:
- Third-party disclosure procedures
- Disclosure records
- Data sharing agreements
- Quarterly disclosure review

**Collection Method**: Manual (procedures, agreements, records)
**Frequency**: Quarterly (review)
**Retention**: 7 years

### P6: Security for Privacy

**Evidence Required**:
- Privacy security controls documentation
- Security logs (CloudTrail, application logs)
- Security incident logs
- Daily security monitoring reports

**Collection Method**: Automated (logs) + Manual (documentation)
**Frequency**: Continuous (automated), Daily (reports)
**Retention**: 7 years

### P7: Data Integrity

**Evidence Required**:
- Data validation procedures
- Validation logs
- Accuracy reports (weekly)
- Data quality metrics

**Collection Method**: Automated (logs, metrics)
**Frequency**: Continuous (automated), Weekly (reports)
**Retention**: 7 years

### P8: Monitoring and Enforcement

**Evidence Required**:
- Privacy compliance monitoring procedures
- Compliance reports (monthly)
- Privacy complaint logs
- Complaint resolution records

**Collection Method**: Manual (procedures, complaints) + Automated (reports)
**Frequency**: Monthly (reports), As needed (complaints)
**Retention**: 7 years

### P9: Data Disposal

**Evidence Required**:
- Data disposal procedures
- Disposal logs
- Disposal verification records
- Monthly disposal reports

**Collection Method**: Manual (procedures) + Automated (logs)
**Frequency**: Monthly (reports)
**Retention**: 7 years

## Evidence Collection Automation

### Automated Evidence Collection Tools

- **AWS Config**: Configuration compliance snapshots
- **CloudTrail**: API call logs, access logs
- **CloudWatch**: Metrics, logs, alarms
- **GuardDuty**: Security findings
- **Security Hub**: Compliance reports
- **Macie**: Confidential data findings
- **Lambda Functions**: Custom evidence collection scripts

### Manual Evidence Collection

- Policy and procedure documents
- Training records
- Incident response logs
- Test results
- Audit reports

## Evidence Retention Schedule

### Production Environment

- **Control Evidence**: 7 years
- **Audit Trails**: 7 years
- **Incident Logs**: 7 years
- **Test Results**: 7 years
- **Compliance Reports**: 7 years

### Development/Staging Environment

- **Control Evidence**: 1 year
- **Audit Trails**: 90 days
- **Incident Logs**: 1 year
- **Test Results**: 1 year
- **Compliance Reports**: 1 year

## Evidence Access Controls

- **Encryption**: All evidence encrypted at rest (KMS)
- **Access Control**: IAM policies for evidence bucket access
- **Versioning**: S3 versioning enabled for evidence integrity
- **Audit Trail**: All evidence access logged (CloudTrail)

## Related Documentation

- [SOC 2 Type II Compliance](./soc2-type2-compliance.md)
- [SOC 2 Control Matrix](./soc2-control-matrix.md)
- [SOC 2 Audit Preparation](./soc2-audit-preparation.md)
- [Security Architecture](./security-architecture.md)
