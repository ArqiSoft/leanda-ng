# Alerting Runbook

This runbook provides procedures for responding to common alerts in the Leanda NG platform.

## Alert Severity Levels

- **P1 (Critical)**: Immediate response required (service down, data loss, security breach)
- **P2 (Warning)**: Response within 1 hour (degraded performance, high error rates)
- **P3 (Info)**: Response within 24 hours (minor issues, capacity warnings)

## Escalation Procedures

1. **P1 Alerts**: 
   - Immediate notification via PagerDuty (if configured) or critical alerts SNS topic
   - On-call engineer must acknowledge within 5 minutes
   - Escalate to team lead if not resolved within 30 minutes

2. **P2 Alerts**:
   - Notification via warning alerts SNS topic
   - Response required within 1 hour
   - Escalate to P1 if service degradation worsens

3. **P3 Alerts**:
   - Notification via info alerts SNS topic
   - Response required within 24 hours
   - Review during next team meeting

---

## ECS Service Alarms

### CPU High (`cpu-high`)

**Alarm**: `{project-name}-{service}-cpu-high-{environment}`  
**Severity**: P2 (Warning)  
**Threshold**: CPU utilization > 80% for 10 minutes

**Symptoms**:
- High CPU utilization in CloudWatch metrics
- Slow response times
- Request timeouts

**Investigation Steps**:
1. Check CloudWatch dashboard for the service
2. Review recent deployments or configuration changes
3. Check application logs for errors or long-running operations
4. Review Container Insights for task-level CPU metrics

**Resolution Steps**:
1. **Immediate**: Scale out the service (increase desired task count)
2. **Short-term**: Review and optimize CPU-intensive operations
3. **Long-term**: Right-size task CPU allocation or optimize code

**Prevention**:
- Set up auto-scaling based on CPU utilization
- Monitor CPU trends and plan capacity
- Optimize application code for CPU efficiency

---

### Memory High (`memory-high`)

**Alarm**: `{project-name}-{service}-memory-high-{environment}`  
**Severity**: P2 (Warning)  
**Threshold**: Memory utilization > 80% for 10 minutes

**Symptoms**:
- High memory utilization in CloudWatch metrics
- Out of memory errors in logs
- Task restarts

**Investigation Steps**:
1. Check CloudWatch dashboard for memory metrics
2. Review application logs for memory-related errors
3. Check for memory leaks (gradual increase over time)
4. Review Container Insights for task-level memory metrics

**Resolution Steps**:
1. **Immediate**: Scale out the service (increase desired task count)
2. **Short-term**: Increase task memory allocation
3. **Long-term**: Optimize memory usage (reduce object retention, fix leaks)

**Prevention**:
- Set up auto-scaling based on memory utilization
- Monitor memory trends
- Use memory profiling tools to identify leaks

---

### Error Rate High (`error-rate-high`)

**Alarm**: `{project-name}-{service}-error-rate-high-{environment}`  
**Severity**: P1 (Critical)  
**Threshold**: 5xx errors > 5 in 5 minutes

**Symptoms**:
- High 5xx error rate in ALB metrics
- User-reported errors
- Service unavailable responses

**Investigation Steps**:
1. Check CloudWatch logs for error patterns
2. Review X-Ray traces for failed requests
3. Check database connectivity and health
4. Review recent deployments or configuration changes
5. Check downstream service dependencies

**Resolution Steps**:
1. **Immediate**: 
   - Check service health endpoints
   - Review error logs for root cause
   - Restart unhealthy tasks if needed
2. **Short-term**: 
   - Fix application bugs
   - Restore database connectivity
   - Fix configuration issues
3. **Long-term**: 
   - Improve error handling
   - Add circuit breakers for downstream services
   - Improve monitoring and alerting

**Prevention**:
- Comprehensive error handling in code
- Health checks and automatic task replacement
- Circuit breakers for external dependencies
- Regular load testing

---

## Database Alarms

### DocumentDB CPU High (`docdb-cpu-high`)

**Alarm**: `{project-name}-docdb-cpu-high-{environment}`  
**Severity**: P2 (Warning)  
**Threshold**: CPU utilization > 80% for 10 minutes

**Investigation Steps**:
1. Check CloudWatch metrics for CPU trends
2. Review slow query logs
3. Check for long-running queries
4. Review connection pool usage

**Resolution Steps**:
1. **Immediate**: Scale up DocumentDB instance size
2. **Short-term**: Optimize slow queries
3. **Long-term**: Add read replicas for read-heavy workloads

---

### DocumentDB Connections High (`docdb-connections-high`)

**Alarm**: `{project-name}-docdb-connections-high-{environment}`  
**Severity**: P2 (Warning)  
**Threshold**: Connection count > 80% of max

**Investigation Steps**:
1. Check connection count metrics
2. Review connection pool configuration
3. Check for connection leaks

**Resolution Steps**:
1. **Immediate**: Scale up DocumentDB instance (more max connections)
2. **Short-term**: Optimize connection pool settings
3. **Long-term**: Fix connection leaks in application code

---

### Redis Memory High (`redis-memory-high`)

**Alarm**: `{project-name}-redis-memory-high-{environment}`  
**Severity**: P2 (Warning)  
**Threshold**: Memory utilization > 80% for 10 minutes

**Investigation Steps**:
1. Check memory usage metrics
2. Review cache key patterns
3. Check for memory leaks

**Resolution Steps**:
1. **Immediate**: Scale up ElastiCache instance size
2. **Short-term**: Implement cache eviction policies
3. **Long-term**: Optimize cache key design and TTLs

---

### Redis Evictions High (`redis-evictions-high`)

**Alarm**: `{project-name}-redis-evictions-high-{environment}`  
**Severity**: P2 (Warning)  
**Threshold**: Evictions > 0

**Investigation Steps**:
1. Check eviction metrics
2. Review cache size and memory limits
3. Review cache key patterns

**Resolution Steps**:
1. **Immediate**: Scale up ElastiCache instance size
2. **Short-term**: Implement cache eviction policies
3. **Long-term**: Optimize cache usage and key design

---

## Messaging Alarms

### MSK Consumer Lag High (`msk-consumer-lag-high`)

**Alarm**: `{project-name}-msk-consumer-lag-high-{environment}`  
**Severity**: P2 (Warning)  
**Threshold**: Consumer lag > 1000 messages for 10 minutes

**Investigation Steps**:
1. Check consumer lag metrics
2. Review consumer group status
3. Check consumer service health
4. Review message processing times

**Resolution Steps**:
1. **Immediate**: Scale out consumer service tasks
2. **Short-term**: Optimize message processing logic
3. **Long-term**: Optimize partition strategy and consumer configuration

---

### EventBridge Dead Letter Queue (`eventbridge-dlq`)

**Alarm**: `{project-name}-eventbridge-dlq-messages-{environment}`  
**Severity**: P1 (Critical)  
**Threshold**: Any messages in DLQ

**Investigation Steps**:
1. Check DLQ message count
2. Review DLQ message content
3. Check event rule targets
4. Review target service health

**Resolution Steps**:
1. **Immediate**: 
   - Review DLQ messages for patterns
   - Check target service availability
   - Manually reprocess messages if needed
2. **Short-term**: 
   - Fix target service issues
   - Update event rules if needed
3. **Long-term**: 
   - Improve error handling in targets
   - Add retry logic with exponential backoff

---

## Storage Alarms

### S3 Bucket Size High (`s3-bucket-size-high`)

**Alarm**: `{project-name}-s3-bucket-size-high-{environment}`  
**Severity**: P3 (Info)  
**Threshold**: Bucket size > 1TB

**Investigation Steps**:
1. Check bucket size metrics
2. Review S3 lifecycle policies
3. Check for unnecessary data retention

**Resolution Steps**:
1. **Short-term**: Review and clean up unnecessary data
2. **Long-term**: Optimize S3 lifecycle policies (transition to Glacier, delete old data)

---

### S3 Request Errors (`s3-request-errors`)

**Alarm**: `{project-name}-s3-request-errors-{environment}`  
**Severity**: P2 (Warning)  
**Threshold**: 4xx errors > 10 in 5 minutes

**Investigation Steps**:
1. Check S3 access logs
2. Review IAM permissions
3. Check for bucket policy issues
4. Review application code for S3 access patterns

**Resolution Steps**:
1. **Immediate**: Check IAM permissions and bucket policies
2. **Short-term**: Fix application code issues
3. **Long-term**: Improve error handling and retry logic

---

## Maintenance Windows

During scheduled maintenance windows, alerts can be suppressed:

1. **Manual Suppression**: Use CloudWatch alarm actions to temporarily disable SNS notifications
2. **Scheduled Suppression**: Configure SNS filter policies to suppress alerts during maintenance
3. **Documentation**: Document maintenance windows in team calendar

---

## Contact Information

- **On-Call Engineer**: Check PagerDuty rotation
- **Team Lead**: [team-lead@example.com]
- **Slack Channel**: #leanda-alerts

---

## Runbook Updates

This runbook should be updated whenever:
- New alarms are added
- Alert thresholds are changed
- New services are deployed
- Resolution procedures are improved

**Last Updated**: 2025-01-15

