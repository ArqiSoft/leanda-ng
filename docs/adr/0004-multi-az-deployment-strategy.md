# 0004. Multi-AZ Deployment Strategy

## Status

Accepted

## Context

Leanda.io requires high availability and fault tolerance. We need to design a multi-AZ deployment strategy to ensure service continuity in case of AZ failures.

**Requirements**:
- High availability (99.9% uptime target)
- Automatic failover in case of AZ failure
- No single point of failure
- Minimal performance impact
- Cost-effective deployment

## Decision

Deploy all services and infrastructure across **2+ availability zones** with automatic failover.

**Architecture**:
- **VPC**: Spans 2 availability zones
- **ECS Services**: Tasks distributed across 2+ AZs
- **Application Load Balancer**: Routes traffic across AZs
- **DocumentDB**: Multi-AZ cluster with automatic failover
- **MSK Serverless**: Automatic multi-AZ distribution
- **ElastiCache Redis**: Multi-AZ with automatic failover (production)

## Consequences

### Positive

- ✅ **High Availability**: 99.9% uptime SLA achievable
- ✅ **Automatic Failover**: Services continue operating during AZ failures
- ✅ **No Single Point of Failure**: All components replicated across AZs
- ✅ **Performance**: Low latency within region, no performance impact
- ✅ **Disaster Recovery**: Foundation for multi-region expansion

### Negative

- ⚠️ **Cost**: 2x infrastructure cost (mitigated by using serverless services)
- ⚠️ **Complexity**: More complex networking and configuration
- ⚠️ **Data Consistency**: Requires careful design for eventual consistency

### Mitigations

1. **Cost**: Use serverless services (Fargate, MSK Serverless) that scale automatically
2. **Complexity**: Use managed services with built-in multi-AZ support
3. **Consistency**: Use appropriate consistency models (strong for critical data, eventual for events)

## Implementation Details

### VPC Configuration

```typescript
// 2 availability zones
maxAzs: 2

// Subnets per AZ
- Public subnets (2): For ALB, NAT Gateway
- Private subnets (2): For ECS tasks
- Isolated subnets (2): For databases
```

### ECS Service Configuration

```typescript
// Minimum 2 tasks for high availability
minCapacity: 2

// Task distribution across AZs
taskDefinition: {
  placementConstraints: [
    {
      type: 'distinctInstance', // Distribute across AZs
    },
  ],
}
```

### Application Load Balancer

```typescript
// ALB spans 2 AZs
subnets: [publicSubnet1, publicSubnet2]

// Health checks route traffic only to healthy AZs
healthCheck: {
  healthyThresholdCount: 2,
  unhealthyThresholdCount: 3,
}
```

### DocumentDB Configuration

```typescript
// Multi-AZ cluster
instances: 2 // One per AZ

// Automatic failover
preferredMaintenanceWindow: 'sun:02:00-sun:03:00'
```

## Alternatives Considered

### Single AZ Deployment

**Pros**: Lower cost, simpler configuration  
**Cons**: No fault tolerance, single point of failure  
**Decision**: Rejected - does not meet availability requirements

### 3+ AZ Deployment

**Pros**: Even higher availability, better fault tolerance  
**Cons**: Higher cost, more complexity  
**Decision**: Rejected - 2 AZs sufficient for 99.9% availability target

### Active-Passive Multi-AZ

**Pros**: Lower cost (passive AZ only for failover)  
**Cons**: Slower failover, wasted capacity  
**Decision**: Rejected - active-active provides better performance and faster failover

## Monitoring and Alerting

- **CloudWatch Alarms**: Monitor AZ health and failover events
- **Health Checks**: ALB health checks detect AZ failures
- **Automated Failover**: DocumentDB and ElastiCache automatically failover
- **Alerting**: Notify on-call engineer on AZ failure

## References

- [AWS Multi-AZ Deployment Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-for-high-availability.html)
- [ECS Multi-AZ Deployment](https://docs.aws.amazon.com/ecs/latest/developerguide/service-connect.html)

