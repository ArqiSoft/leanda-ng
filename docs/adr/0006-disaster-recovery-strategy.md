# 0006. Disaster Recovery Strategy

## Status

Accepted

## Context

Leanda.io requires a disaster recovery strategy to ensure business continuity in case of regional failures, data corruption, or other disasters.

**Requirements**:
- Recovery Time Objective (RTO): 4 hours
- Recovery Point Objective (RPO): 1 hour
- Data protection against regional failures
- Automated backup and restore procedures
- Regular disaster recovery testing

## Decision

Implement a **multi-region backup strategy** with automated backups and point-in-time recovery.

**Strategy**:
- **Primary Region**: us-east-1 (N. Virginia)
- **Secondary Region**: us-west-2 (Oregon) - for backups and future DR
- **Backup Frequency**: Daily automated backups
- **Retention**: 7 days (dev), 30 days (production)
- **Cross-Region Replication**: Enabled for critical data

## Consequences

### Positive

- ✅ **Data Protection**: Protection against regional failures
- ✅ **Point-in-Time Recovery**: Restore to any point within retention period
- ✅ **Automated Backups**: No manual intervention required
- ✅ **Compliance**: Meets data retention and recovery requirements

### Negative

- ⚠️ **Cost**: Additional storage costs for backups and replication
- ⚠️ **Complexity**: More complex backup and restore procedures
- ⚠️ **RPO Limitation**: 1 hour RPO means potential data loss

### Mitigations

1. **Cost**: Use S3 lifecycle policies, Glacier for long-term storage
2. **Complexity**: Automate backup and restore procedures
3. **RPO**: Increase backup frequency if needed (currently daily)

## Implementation Details

### Backup Strategy

#### DocumentDB Backups

```typescript
// Automated daily backups
backupRetentionPeriod: Duration.days(30) // Production
backupRetentionPeriod: Duration.days(7)   // Development

// Backup window: 2 AM UTC
preferredBackupWindow: '02:00-03:00'

// Point-in-time recovery enabled
enablePointInTimeRecovery: true
```

#### S3 Backups

```typescript
// Versioning enabled
versioned: true

// Cross-region replication
replicationConfiguration: {
  role: replicationRole,
  rules: [
    {
      destination: {
        bucket: secondaryRegionBucket,
        storageClass: 'STANDARD_IA',
      },
    },
  ],
}

// Lifecycle policies
lifecycleRules: [
  {
    transitions: [
      { storageClass: 'GLACIER', transitionAfter: Duration.days(90) },
      { storageClass: 'DEEP_ARCHIVE', transitionAfter: Duration.days(365) },
    ],
  },
]
```

#### Application State Backups

- **ECS Task Definitions**: Versioned in ECR
- **Infrastructure**: Versioned in Git, deployed via CDK
- **Configuration**: Stored in Parameter Store / Secrets Manager

### Disaster Recovery Scenarios

#### Scenario 1: Single AZ Failure

**Impact**: Minimal (services in multiple AZs)  
**Recovery**: Automatic failover via ALB  
**RTO**: < 5 minutes  
**RPO**: 0 (no data loss)

**Procedure**:
1. ALB automatically routes traffic to healthy AZ
2. ECS tasks in failed AZ are replaced automatically
3. DocumentDB continues operating in remaining AZ
4. No manual intervention required

#### Scenario 2: Region Failure

**Impact**: Complete service outage  
**Recovery**: Failover to secondary region  
**RTO**: 4 hours  
**RPO**: 1 hour (last backup)

**Procedure**:
1. Activate secondary region infrastructure (CDK deploy)
2. Restore DocumentDB from cross-region snapshot
3. Restore S3 data from cross-region replication
4. Update DNS to point to secondary region
5. Restart services in secondary region
6. Verify service health and functionality

#### Scenario 3: Data Corruption

**Impact**: Data loss or corruption  
**Recovery**: Restore from point-in-time backup  
**RPO**: 1 hour (last backup)  
**RTO**: 2 hours

**Procedure**:
1. Identify corruption time window
2. Restore DocumentDB to point-in-time (before corruption)
3. Restore S3 objects from version history
4. Replay Kafka events from backup (if available)
5. Verify data integrity
6. Resume normal operations

### Disaster Recovery Testing

**Frequency**: Quarterly  
**Procedure**:
1. Test DocumentDB restore from snapshot
2. Test S3 restore from version history
3. Test infrastructure deployment in secondary region
4. Test service startup and health checks
5. Document results and update procedures

## Alternatives Considered

### Single-Region Backup Only

**Pros**: Lower cost, simpler  
**Cons**: No protection against regional failures  
**Decision**: Rejected - does not meet DR requirements

### Active-Active Multi-Region

**Pros**: Zero RTO, zero RPO  
**Cons**: Very high cost, high complexity  
**Decision**: Rejected - not cost-effective for current scale

### No Disaster Recovery

**Pros**: No additional cost  
**Cons**: No protection against disasters  
**Decision**: Rejected - unacceptable risk

## Monitoring and Alerting

- **Backup Status**: CloudWatch alarms for backup failures
- **Replication Status**: S3 replication metrics
- **DR Testing**: Quarterly automated DR tests
- **Alerting**: Notify on-call engineer on backup failures

## References

- [AWS Disaster Recovery Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-for-disaster-recovery.html)
- [DocumentDB Backup and Restore](https://docs.aws.amazon.com/documentdb/latest/developerguide/backup-restore.html)
- [S3 Cross-Region Replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)

