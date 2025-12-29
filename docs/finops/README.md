# Leanda.io FinOps and Cost Optimization

This directory contains FinOps (Financial Operations) documentation, strategies, and procedures for cost optimization on AWS.

## Table of Contents

1. [Cost Optimization Strategy](#cost-optimization-strategy)
2. [Cost Allocation and Tagging](#cost-allocation-and-tagging)
3. [AWS Budgets and Monitoring](#aws-budgets-and-monitoring)
4. [Right-Sizing Procedures](#right-sizing-procedures)
5. [Cost Review Procedures](#cost-review-procedures)
6. [Cost Optimization Playbook](#cost-optimization-playbook)

---

## Cost Optimization Strategy

See [ADR-0007: Cost Optimization Strategy](../adr/0007-cost-optimization-strategy.md) for the comprehensive cost optimization strategy.

**Key Principles**:
- **Cost Visibility**: Tag all resources for cost allocation
- **Proactive Management**: Budget alerts prevent cost overruns
- **Automated Optimization**: Use AWS services that optimize automatically (S3 Intelligent-Tiering)
- **Right-Sizing**: Regular reviews ensure resources match actual usage
- **Reserved Capacity**: Use Reserved Instances/Savings Plans for predictable workloads

---

## Cost Allocation and Tagging

### Mandatory Tags

All AWS resources must be tagged with the following mandatory tags:

| Tag | Value | Example |
|-----|-------|---------|
| `Project` | leanda-ng | leanda-ng |
| `Environment` | dev \| staging \| prod | production |
| `Service` | service-name | core-api, blob-storage |
| `CostCenter` | department/budget code | engineering |
| `Owner` | team/individual email | leanda-team@example.com |

### Tagging Implementation

Tags are automatically applied to all resources via CDK:

```typescript
// All stacks use the tagging utility
import { applyCostAllocationTags } from '../lib/utils/tagging';

applyCostAllocationTags(resource, {
  Project: 'leanda-ng',
  Environment: environment,
  Service: 'service-name',
  CostCenter: costCenter,
  Owner: owner,
});
```

### Cost Allocation Reports

Generate cost allocation reports in AWS Cost Explorer:

1. Navigate to **AWS Cost Explorer**
2. Select **Cost allocation tags**
3. Enable tags: `Project`, `Environment`, `Service`, `CostCenter`, `Owner`
4. Generate reports by tag

**Report Types**:
- Cost by service
- Cost by environment
- Cost by team (CostCenter)
- Cost by service owner

---

## AWS Budgets and Monitoring

### Budget Configuration

Budgets are configured in the FinOps CDK stack (`infrastructure/lib/stacks/finops-stack.ts`):

**Total Cost Budget**:
- Development: $1,000/month
- Staging: $5,000/month
- Production: $10,000/month

**Service Cost Budget**:
- 80% of total budget for core services (ECS, DocumentDB, S3, MSK, ElastiCache, CloudWatch, KMS)

### Budget Alerts

Alerts are configured at the following thresholds:
- **50%**: Early warning
- **80%**: Approaching budget limit
- **100%**: Budget exceeded
- **Forecasted 100%**: Projected to exceed budget

**Alert Channels**:
- Email notifications
- SNS topic: `leanda-ng-budget-alerts-{environment}`

### Cost Monitoring

**AWS Cost Explorer**:
- Daily cost tracking
- Cost by service, environment, tag
- Cost trends and forecasts
- Custom cost reports

**CloudWatch Cost Dashboard**:
- Placeholder dashboard created in FinOps stack
- Manual setup required (cost metrics not available via CloudWatch Metrics API)

**Cost Anomaly Detection**:
- Must be enabled manually in AWS Cost Management Console
- Alerts on unexpected cost spikes
- SNS topic: `leanda-ng-cost-anomaly-alerts-{environment}`

### Billing Alarms

**Important**: Billing alarms must be created manually in the AWS Console (us-east-1 region only) and cannot be automated via CDK.

**Setup Steps**:
1. Navigate to **CloudWatch** → **Alarms** → **Create alarm**
2. Select **Billing** metric
3. Set threshold (e.g., $500 for development)
4. Configure SNS notification
5. Create alarm

---

## Right-Sizing Procedures

### ECS Fargate Tasks

**Initial Sizing**:
- Start with 0.25 vCPU / 512MB memory
- Monitor CPU and memory utilization

**Right-Sizing Process**:
1. Review CloudWatch metrics (CPU, memory utilization)
2. Identify underutilized or overutilized tasks
3. Adjust task size based on p95 metrics
4. Test changes in development/staging first
5. Deploy to production during maintenance window

**Auto-Scaling**:
- Target CPU utilization: 70%
- Target memory utilization: 80%
- Min capacity: 2 tasks (production), 1 task (dev/staging)
- Max capacity: 20 tasks (production), 5 tasks (dev/staging)

### DocumentDB Instances

**Initial Sizing**:
- Development: db.t3.medium (1 instance)
- Staging: db.t3.medium (1 instance)
- Production: db.t3.medium (2 instances, multi-AZ)

**Right-Sizing Process**:
1. Review Performance Insights (CPU, memory, I/O)
2. Identify slow queries and optimization opportunities
3. Consider read replicas for read-heavy workloads
4. Scale instance size during maintenance window
5. Monitor for 1 week after scaling

**Reserved Instances**:
- Evaluate after 3 months of stable usage
- 1-year or 3-year commitments for predictable workloads
- Up to 72% cost savings

### S3 Storage

**Storage Classes**:
- **Standard**: Hot data (frequent access)
- **Intelligent-Tiering**: Automatic optimization (recommended)
- **Glacier**: Cold data (90+ days, 12-hour retrieval)
- **Deep Archive**: Archival data (180+ days, 12-hour retrieval)

**Lifecycle Policies**:
- Automatic transition to Intelligent-Tiering (immediate)
- Transition to Glacier after 90 days
- Transition to Deep Archive after 180 days
- Expire incomplete multipart uploads after 7 days

**Optimization**:
- Review S3 Storage Lens for optimization opportunities
- Enable S3 request metrics to identify expensive operations
- Use S3 Select for querying without full object retrieval

### ElastiCache Redis

**Initial Sizing**:
- Development: cache.t3.micro (1 node)
- Staging: cache.t3.micro (1 node)
- Production: cache.t3.small (1 node, scale as needed)

**Right-Sizing Process**:
1. Review CloudWatch metrics (CPU, memory, cache hits/misses)
2. Identify cache hit rate (target: >80%)
3. Scale instance size or add nodes if needed
4. Consider Reserved Capacity for predictable workloads

---

## Cost Review Procedures

### Monthly Cost Review

**Schedule**: First Monday of each month

**Participants**: Engineering team lead, FinOps lead

**Agenda**:
1. Review AWS Cost Explorer reports
   - Total cost by environment
   - Cost by service
   - Cost by tag (CostCenter, Owner)
   - Cost trends (month-over-month)
2. Review budget alerts
   - Identify any budget threshold breaches
   - Analyze root causes
3. Identify optimization opportunities
   - Underutilized resources
   - Overutilized resources
   - Unused resources
4. Document findings and action items

**Output**: Monthly cost review report

### Quarterly Cost Review

**Schedule**: First Monday of each quarter

**Participants**: Engineering team, Finance, Leadership

**Agenda**:
1. Review quarterly cost trends
2. Evaluate Reserved Instance opportunities
   - Identify steady-state workloads
   - Calculate potential savings
   - Make Reserved Instance purchases
3. Review Savings Plans coverage
   - Evaluate Compute Savings Plans
   - Evaluate EC2 Instance Savings Plans
4. Analyze unit economics
   - Cost per user
   - Cost per data volume
   - Cost per API call
5. Review and adjust budgets
6. Document cost optimization decisions

**Output**: Quarterly cost review report and ADR updates

### Cost Anomaly Response

**When**: Cost anomaly alert received

**Steps**:
1. **Immediate**: Review AWS Cost Explorer for cost spike
2. **Identify**: Determine which service/resource caused the spike
3. **Investigate**: Review CloudWatch metrics, logs, and recent changes
4. **Mitigate**: Take immediate action if needed (scale down, stop unused resources)
5. **Document**: Document root cause and prevention measures
6. **Follow-up**: Review in next monthly cost review

---

## Cost Optimization Playbook

### Scenario 1: Budget Alert at 80%

**Symptoms**: Budget alert received at 80% threshold

**Actions**:
1. Review AWS Cost Explorer to identify cost drivers
2. Check for any recent deployments or changes
3. Review CloudWatch metrics for resource utilization
4. Identify optimization opportunities:
   - Scale down underutilized resources
   - Stop unused resources
   - Review S3 storage classes
5. Document findings and action items
6. Monitor cost trends daily until next budget cycle

### Scenario 2: Unexpected Cost Spike

**Symptoms**: Cost anomaly alert or sudden cost increase

**Actions**:
1. **Immediate**: Review AWS Cost Explorer for cost spike source
2. **Identify**: Determine which service/resource caused the spike
3. **Investigate**:
   - Review CloudWatch metrics (CPU, memory, requests)
   - Check for auto-scaling events
   - Review recent deployments
   - Check for data transfer spikes
4. **Mitigate**:
   - Scale down if over-provisioned
   - Stop unused resources
   - Review and fix any misconfigurations
5. **Document**: Root cause analysis and prevention measures
6. **Follow-up**: Review in next monthly cost review

### Scenario 3: Right-Sizing Resources

**Symptoms**: Resources consistently underutilized or overutilized

**Actions**:
1. **Analyze**: Review CloudWatch metrics for 2 weeks
   - CPU utilization (target: 40-70%)
   - Memory utilization (target: 50-80%)
   - Request count and latency
2. **Plan**: Create right-sizing plan
   - Identify resources to resize
   - Calculate new sizes
   - Plan deployment schedule
3. **Test**: Test changes in development/staging
4. **Deploy**: Deploy to production during maintenance window
5. **Monitor**: Monitor for 1 week after deployment
6. **Document**: Document right-sizing decisions and results

### Scenario 4: Reserved Instance Purchase

**Symptoms**: Steady-state workload identified (3+ months stable usage)

**Actions**:
1. **Analyze**: Review resource usage for 3 months
   - Identify steady-state workloads
   - Calculate potential savings
2. **Evaluate**: Compare Reserved Instance options
   - 1-year vs 3-year commitments
   - Standard vs Convertible Reserved Instances
   - Calculate break-even point
3. **Purchase**: Make Reserved Instance purchase
   - Document purchase decision
   - Update cost allocation tags
4. **Monitor**: Monitor Reserved Instance utilization
5. **Review**: Review in quarterly cost review

---

## Cost Optimization Checklist

### Monthly

- [ ] Review AWS Cost Explorer reports
- [ ] Review budget alerts
- [ ] Identify optimization opportunities
- [ ] Document findings and action items
- [ ] Update cost allocation tags if needed

### Quarterly

- [ ] Review quarterly cost trends
- [ ] Evaluate Reserved Instance opportunities
- [ ] Review Savings Plans coverage
- [ ] Analyze unit economics
- [ ] Review and adjust budgets
- [ ] Document cost optimization decisions

### As Needed

- [ ] Respond to cost anomaly alerts
- [ ] Right-size resources
- [ ] Review and optimize S3 storage classes
- [ ] Review and optimize auto-scaling policies
- [ ] Review and optimize database instances

---

## References

- [ADR-0007: Cost Optimization Strategy](../adr/0007-cost-optimization-strategy.md)
- [AWS Well-Architected Framework - Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
- [AWS Cost Management Best Practices](https://docs.aws.amazon.com/cost-management/latest/userguide/best-practices.html)
- [FinOps Workspace Rules](../../.cursor/rules/13-aws-finops-cost.mdc)
- [Infrastructure README](../../infrastructure/README.md)

