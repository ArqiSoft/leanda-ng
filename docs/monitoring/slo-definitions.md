# Service-Level Objectives (SLOs)

This document defines Service-Level Objectives (SLOs) for all services in the Leanda NG platform.

## SLO Overview

SLOs define the reliability and performance targets for each service. Error budgets are calculated as the difference between the SLO target and 100%.

### SLO Targets

| Service | Availability | Latency (p95) | Error Rate |
|---------|-------------|---------------|------------|
| core-api | 99.9% | < 500ms | < 0.1% |
| blob-storage | 99.9% | < 1000ms | < 0.1% |
| indexing | 99.5% | < 2000ms | < 0.5% |
| metadata-processing | 99.5% | < 3000ms | < 0.5% |
| chemical-parser | 99.0% | < 5000ms | < 1.0% |
| chemical-properties | 99.0% | < 5000ms | < 1.0% |
| reaction-parser | 99.0% | < 5000ms | < 1.0% |
| crystal-parser | 99.0% | < 5000ms | < 1.0% |
| spectra-parser | 99.0% | < 5000ms | < 1.0% |
| imaging | 99.0% | < 5000ms | < 1.0% |
| office-processor | 99.0% | < 5000ms | < 1.0% |

### Error Budgets

Error budgets represent the acceptable amount of unreliability:

**Example for core-api (99.9% availability)**:
- **Error Budget**: 0.1% (43 minutes per month)
- **50% Budget Alert**: 21.5 minutes consumed
- **80% Budget Alert**: 34.4 minutes consumed

---

## Service-Specific SLOs

### core-api

**Availability**: 99.9%  
**Target**: Less than 43 minutes of downtime per month

**Latency (p95)**: < 500ms  
**Target**: 95% of requests complete within 500ms

**Error Rate**: < 0.1%  
**Target**: Less than 0.1% of requests result in 5xx errors

**Measurement**:
- Availability: `(total_requests - 5xx_errors) / total_requests * 100`
- Latency: 95th percentile of response times
- Error Rate: `5xx_errors / total_requests * 100`

**Error Budget Tracking**:
- Alert when error budget consumed > 50% (21.5 minutes)
- Alert when error budget consumed > 80% (34.4 minutes)

---

### blob-storage

**Availability**: 99.9%  
**Target**: Less than 43 minutes of downtime per month

**Latency (p95)**: < 1000ms  
**Target**: 95% of file operations complete within 1000ms

**Error Rate**: < 0.1%  
**Target**: Less than 0.1% of operations result in errors

**Measurement**:
- Availability: `(total_operations - errors) / total_operations * 100`
- Latency: 95th percentile of operation times
- Error Rate: `errors / total_operations * 100`

---

### indexing

**Availability**: 99.5%  
**Target**: Less than 3.6 hours of downtime per month

**Latency (p95)**: < 2000ms  
**Target**: 95% of indexing operations complete within 2000ms

**Error Rate**: < 0.5%  
**Target**: Less than 0.5% of indexing operations result in errors

**Measurement**:
- Availability: `(total_operations - errors) / total_operations * 100`
- Latency: 95th percentile of indexing times
- Error Rate: `errors / total_operations * 100`

---

### metadata-processing

**Availability**: 99.5%  
**Target**: Less than 3.6 hours of downtime per month

**Latency (p95)**: < 3000ms  
**Target**: 95% of processing operations complete within 3000ms

**Error Rate**: < 0.5%  
**Target**: Less than 0.5% of processing operations result in errors

**Measurement**:
- Availability: `(total_operations - errors) / total_operations * 100`
- Latency: 95th percentile of processing times
- Error Rate: `errors / total_operations * 100`

---

### Parser Services (chemical-parser, chemical-properties, reaction-parser, crystal-parser, spectra-parser, imaging, office-processor)

**Availability**: 99.0%  
**Target**: Less than 7.2 hours of downtime per month

**Latency (p95)**: < 5000ms  
**Target**: 95% of parsing operations complete within 5000ms

**Error Rate**: < 1.0%  
**Target**: Less than 1.0% of parsing operations result in errors

**Measurement**:
- Availability: `(total_operations - errors) / total_operations * 100`
- Latency: 95th percentile of parsing times
- Error Rate: `errors / total_operations * 100`

**Note**: Parser services have lower SLOs due to the complexity and variability of parsing operations.

---

## Error Budget Calculation

Error budgets are calculated monthly:

```
Error Budget = 100% - SLO Target
Consumed Budget = (Actual Error Rate / Error Budget) * 100
```

**Example for core-api**:
- SLO Target: 99.9% availability
- Error Budget: 0.1% (43 minutes per month)
- If 21.5 minutes consumed: 50% budget consumed
- If 34.4 minutes consumed: 80% budget consumed

---

## Error Budget Alerts

### 50% Budget Alert

**Severity**: P2 (Warning)  
**Action**: Review error patterns and plan remediation

**Response**:
1. Review error logs and patterns
2. Identify root causes
3. Plan fixes for next sprint
4. Monitor closely for further degradation

### 80% Budget Alert

**Severity**: P1 (Critical)  
**Action**: Immediate remediation required

**Response**:
1. Immediate investigation of root causes
2. Implement hotfixes if possible
3. Consider temporary service degradation (feature flags)
4. Escalate to team lead

---

## SLO Monitoring

### CloudWatch Metrics

SLO metrics are tracked in CloudWatch:
- **Namespace**: `LeandaNG/SLO`
- **Metrics**: 
  - `Availability`: Service availability percentage
  - `ErrorBudgetConsumed`: Percentage of error budget consumed
  - `LatencyP95`: 95th percentile latency
  - `ErrorRate`: Error rate percentage

### Dashboards

SLO dashboards are available in CloudWatch:
- **Location**: CloudWatch → Dashboards → `leanda-ng-slo-{environment}`
- **Widgets**: 
  - Error budget consumption over time
  - Availability trends
  - Latency percentiles
  - Error rate trends

---

## SLO Review Process

### Monthly Review

1. **Review Error Budgets**: Check error budget consumption for all services
2. **Identify Trends**: Identify services with consistent budget consumption
3. **Plan Improvements**: Plan SLO improvements for services exceeding targets
4. **Update SLOs**: Adjust SLOs if targets are consistently unmet or too conservative

### Quarterly Review

1. **SLO Effectiveness**: Review whether SLOs are driving the right behaviors
2. **Error Budget Usage**: Analyze how error budgets are being used
3. **Service Prioritization**: Prioritize SLO improvements based on business impact
4. **Documentation Updates**: Update SLO definitions based on learnings

---

## SLO Violation Response

### When SLO is Violated

1. **Immediate**: 
   - Acknowledge violation
   - Check error budget consumption
   - Review recent changes

2. **Short-term**: 
   - Investigate root causes
   - Implement fixes
   - Monitor recovery

3. **Long-term**: 
   - Review SLO targets
   - Plan improvements
   - Update runbooks

---

## Best Practices

### SLO Design

1. **User-Focused**: Define SLOs based on user experience
2. **Measurable**: Use metrics that can be reliably measured
3. **Achievable**: Set targets that are challenging but achievable
4. **Review Regularly**: Review and adjust SLOs based on actual performance

### Error Budget Management

1. **Track Consumption**: Monitor error budget consumption regularly
2. **Plan Usage**: Plan error budget usage for deployments and experiments
3. **Learn from Violations**: Use SLO violations as learning opportunities
4. **Balance**: Balance reliability with feature velocity

---

## Additional Resources

- [Alerting Runbook](./alerting-runbook.md)
- [Monitoring Guide](./monitoring-guide.md)
- [Google SRE Book - SLOs](https://sre.google/workbook/slo-document/)

---

**Last Updated**: 2025-01-15

