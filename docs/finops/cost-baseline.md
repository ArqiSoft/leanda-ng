# Leanda.io Cost Baseline and Optimization Recommendations

**Last Updated**: 2025-12-27  
**Status**: Initial Baseline  
**Environment**: Development, Staging, Production

## Executive Summary

This document provides a cost baseline for the Leanda.io platform and optimization recommendations. Costs are estimated based on AWS pricing as of December 2025 and assume typical usage patterns for an open science data repository platform.

**Key Findings**:
- Estimated monthly costs: $1,000 (dev), $5,000 (staging), $10,000 (production)
- Primary cost drivers: ECS Fargate, DocumentDB, S3 storage
- Optimization opportunities: S3 Intelligent-Tiering, Reserved Instances, right-sizing

---

## Cost Baseline by Environment

### Development Environment

**Estimated Monthly Cost**: $1,000

| Service | Resource | Configuration | Estimated Cost |
|---------|----------|---------------|---------------|
| ECS Fargate | 11 services | 0.25 vCPU / 512MB, 1 task each | $150 |
| DocumentDB | 1 instance | db.t3.medium | $100 |
| S3 Storage | Data bucket | 100 GB Standard | $25 |
| MSK Serverless | Kafka cluster | Low throughput | $30 |
| ElastiCache | Redis | cache.t3.micro | $15 |
| CloudWatch | Logs, metrics | Standard retention | $20 |
| VPC | NAT Gateway | 1 NAT Gateway | $32 |
| Security | GuardDuty, Config | Basic monitoring | $50 |
| **Total** | | | **~$422** |

**Budget**: $1,000/month (includes buffer for growth and testing)

### Staging Environment

**Estimated Monthly Cost**: $5,000

| Service | Resource | Configuration | Estimated Cost |
|---------|----------|---------------|---------------|
| ECS Fargate | 11 services | 0.5 vCPU / 1GB, 2 tasks each | $600 |
| DocumentDB | 1 instance | db.t3.medium | $100 |
| S3 Storage | Data bucket | 500 GB Standard | $125 |
| MSK Serverless | Kafka cluster | Medium throughput | $100 |
| ElastiCache | Redis | cache.t3.small | $30 |
| CloudWatch | Logs, metrics | Extended retention | $50 |
| VPC | NAT Gateway | 1 NAT Gateway | $32 |
| Security | GuardDuty, Config, Security Hub | Full monitoring | $150 |
| **Total** | | | **~$1,187** |

**Budget**: $5,000/month (includes buffer for load testing and staging deployments)

### Production Environment

**Estimated Monthly Cost**: $10,000

| Service | Resource | Configuration | Estimated Cost |
|---------|----------|---------------|---------------|
| ECS Fargate | 11 services | 0.5-1 vCPU / 1-2GB, 2-10 tasks each | $2,000 |
| DocumentDB | 2 instances | db.t3.medium, multi-AZ | $400 |
| S3 Storage | Data bucket | 5 TB (with lifecycle policies) | $500 |
| MSK Serverless | Kafka cluster | High throughput | $300 |
| ElastiCache | Redis | cache.t3.small | $50 |
| CloudWatch | Logs, metrics | 1-year retention | $200 |
| VPC | NAT Gateway | 2 NAT Gateways (multi-AZ) | $64 |
| Security | GuardDuty, Config, Security Hub, Macie | Full security monitoring | $300 |
| API Gateway | API requests | 1M requests/month | $50 |
| CloudFront | CDN | 100 GB transfer | $10 |
| **Total** | | | **~$3,824** |

**Budget**: $10,000/month (includes buffer for growth, peak usage, and reserved capacity)

**Note**: Production costs are conservative estimates. Actual costs will vary based on:
- Data volume and access patterns
- API request volume
- Auto-scaling behavior
- Reserved Instance purchases

---

## Cost Optimization Opportunities

### Immediate (No Cost)

1. **S3 Intelligent-Tiering**
   - **Impact**: Automatic cost optimization for unpredictable access patterns
   - **Savings**: 10-40% on storage costs
   - **Implementation**: Already configured in CDK

2. **S3 Lifecycle Policies**
   - **Impact**: Automatic transition to lower-cost storage classes
   - **Savings**: 50-70% on archival data (Glacier, Deep Archive)
   - **Implementation**: Already configured in CDK

3. **Auto-Scaling**
   - **Impact**: Scale down during low usage periods
   - **Savings**: 20-40% on compute costs
   - **Implementation**: Configured in ECS service definitions

4. **Cost Allocation Tags**
   - **Impact**: Enable cost visibility and allocation
   - **Savings**: Enables optimization decisions
   - **Implementation**: Already configured in CDK

### Short-Term (1-3 Months)

1. **Right-Sizing Resources**
   - **Impact**: Match resources to actual usage
   - **Savings**: 20-30% on compute and database costs
   - **Process**: Review CloudWatch metrics, adjust resource sizes

2. **Scheduled Scaling**
   - **Impact**: Scale down non-production during off-hours
   - **Savings**: 30-50% on development/staging costs
   - **Implementation**: EventBridge Scheduler + ECS auto-scaling

3. **S3 Storage Optimization**
   - **Impact**: Optimize storage classes based on access patterns
   - **Savings**: 20-40% on storage costs
   - **Process**: Review S3 Storage Lens, adjust lifecycle policies

### Medium-Term (3-6 Months)

1. **Reserved Instances**
   - **Impact**: Significant savings for predictable workloads
   - **Savings**: 30-72% on DocumentDB and ElastiCache
   - **Process**: Evaluate after 3 months of stable usage

2. **Savings Plans**
   - **Impact**: Flexible savings for compute usage
   - **Savings**: 20-40% on ECS Fargate
   - **Process**: Evaluate Compute Savings Plans after usage patterns stabilize

3. **Graviton (ARM) Instances**
   - **Impact**: Better performance and cost efficiency
   - **Savings**: 20-40% on compute costs
   - **Implementation**: Migrate ECS tasks to ARM64 architecture

### Long-Term (6-12 Months)

1. **Multi-Region Optimization**
   - **Impact**: Optimize data transfer and storage costs
   - **Savings**: 10-20% on data transfer costs
   - **Process**: Evaluate multi-region architecture

2. **Advanced Caching**
   - **Impact**: Reduce database and API costs
   - **Savings**: 20-30% on database costs
   - **Process**: Implement CloudFront, optimize ElastiCache usage

---

## Cost Monitoring and Alerts

### Budget Alerts

Configured in FinOps stack:
- **50% threshold**: Early warning
- **80% threshold**: Approaching budget limit
- **100% threshold**: Budget exceeded
- **Forecasted 100%**: Projected to exceed budget

### Cost Anomaly Detection

**Setup Required**: Manual setup in AWS Cost Management Console

**Configuration**:
- Monitor total cost
- Alert on 20% increase from baseline
- SNS topic: `leanda-ng-cost-anomaly-alerts-{environment}`

### Monthly Cost Review

**Schedule**: First Monday of each month

**Review Items**:
- Total cost by environment
- Cost by service
- Cost by tag (CostCenter, Owner)
- Cost trends (month-over-month)
- Budget alerts
- Optimization opportunities

---

## Cost Optimization Roadmap

### Q1 2025

- [x] Implement cost allocation tags
- [x] Configure AWS Budgets
- [x] Implement S3 lifecycle policies
- [ ] Enable Cost Anomaly Detection (manual setup)
- [ ] Create billing alarms (manual setup)
- [ ] First monthly cost review

### Q2 2025

- [ ] Right-size ECS tasks based on metrics
- [ ] Right-size DocumentDB instances
- [ ] Implement scheduled scaling for non-production
- [ ] Review and optimize S3 storage classes
- [ ] Evaluate Reserved Instance opportunities

### Q3 2025

- [ ] Purchase Reserved Instances (if applicable)
- [ ] Evaluate Savings Plans
- [ ] Migrate to Graviton (ARM) instances
- [ ] Implement advanced caching strategies
- [ ] Quarterly cost review

### Q4 2025

- [ ] Evaluate multi-region optimization
- [ ] Review and optimize data transfer costs
- [ ] Annual cost review and planning
- [ ] Update budgets for next year

---

## Cost Allocation by Service

### Estimated Monthly Costs (Production)

| Service | Estimated Cost | % of Total | Optimization Priority |
|---------|----------------|------------|------------------------|
| ECS Fargate | $2,000 | 52% | High (right-sizing, Graviton) |
| DocumentDB | $400 | 10% | Medium (Reserved Instances) |
| S3 Storage | $500 | 13% | Medium (lifecycle policies) |
| MSK Serverless | $300 | 8% | Low (auto-scaling) |
| Security Services | $300 | 8% | Low (required) |
| CloudWatch | $200 | 5% | Low (required) |
| ElastiCache | $50 | 1% | Low (right-sizing) |
| Other | $74 | 2% | Low |
| **Total** | **$3,824** | **100%** | |

---

## Recommendations

### Immediate Actions

1. **Enable Cost Anomaly Detection** (manual setup required)
2. **Create billing alarms** (manual setup required)
3. **Review S3 Storage Lens** for optimization opportunities
4. **Monitor CloudWatch metrics** for right-sizing opportunities

### Short-Term Actions (1-3 Months)

1. **Right-size ECS tasks** based on actual usage
2. **Implement scheduled scaling** for non-production environments
3. **Review and optimize S3 storage classes**
4. **Conduct first monthly cost review**

### Medium-Term Actions (3-6 Months)

1. **Evaluate Reserved Instance opportunities** for DocumentDB
2. **Evaluate Savings Plans** for ECS Fargate
3. **Migrate to Graviton (ARM) instances** for 20-40% savings
4. **Conduct quarterly cost review**

### Long-Term Actions (6-12 Months)

1. **Evaluate multi-region optimization**
2. **Implement advanced caching strategies**
3. **Annual cost review and planning**

---

## References

- [ADR-0007: Cost Optimization Strategy](../adr/0007-cost-optimization-strategy.md)
- [FinOps Playbook](./README.md)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Cost Management Best Practices](https://docs.aws.amazon.com/cost-management/latest/userguide/best-practices.html)

