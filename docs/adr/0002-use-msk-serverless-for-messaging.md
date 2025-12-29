# 0002. Use MSK Serverless for Messaging

## Status

Accepted

## Context

Leanda.io uses an event-driven architecture with Kafka for asynchronous communication between microservices. We need to choose a Kafka solution:
- Amazon MSK Serverless (managed, auto-scaling)
- Amazon MSK Provisioned (managed, fixed capacity)
- Self-managed Kafka on EC2
- Amazon EventBridge (alternative event bus)

**Requirements**:
- Kafka-compatible API (services use SmallRye Reactive Messaging)
- Auto-scaling for variable workloads
- High availability (multi-AZ)
- Minimal operational overhead
- Cost-effective for variable message volumes

## Decision

Use **Amazon MSK Serverless** for all Kafka messaging.

**Rationale**:
1. **Serverless**: Automatic scaling based on throughput, no capacity planning
2. **Kafka-Compatible**: Full Kafka API compatibility, no code changes needed
3. **Multi-AZ**: Built-in multi-AZ deployment for high availability
4. **Operational Simplicity**: No cluster management, automatic patching
5. **Cost-Effective**: Pay-per-use pricing, no idle capacity
6. **Integration**: Seamless integration with VPC, IAM, CloudWatch

## Consequences

### Positive

- ✅ **Automatic Scaling**: Scales automatically based on message throughput
- ✅ **No Capacity Planning**: No need to provision brokers or storage
- ✅ **High Availability**: Multi-AZ deployment with automatic failover
- ✅ **Cost Optimization**: Pay only for actual message throughput
- ✅ **Operational Simplicity**: No cluster management or patching

### Negative

- ⚠️ **Throughput Limits**: 200 MB/s per partition (may require partitioning strategy)
- ⚠️ **Cost at Scale**: May be more expensive than provisioned for high, constant throughput
- ⚠️ **Limited Control**: Less control over broker configuration compared to provisioned

### Mitigations

1. **Throughput Limits**: Partition topics appropriately (10+ partitions per topic)
2. **Cost**: Monitor costs, consider provisioned MSK for high, constant throughput
3. **Control**: Use topic-level configurations for fine-grained control

## Alternatives Considered

### Amazon MSK Provisioned

**Pros**: More control, potentially lower cost for high constant throughput  
**Cons**: Requires capacity planning, manual scaling, cluster management  
**Decision**: Rejected due to operational overhead and variable workload

### Self-Managed Kafka on EC2

**Pros**: Full control, potentially lower cost  
**Cons**: Requires cluster management, patching, monitoring, high operational overhead  
**Decision**: Rejected due to operational complexity

### Amazon EventBridge

**Pros**: True serverless, automatic scaling, lower cost  
**Cons**: Not Kafka-compatible, requires code changes, different API  
**Decision**: Rejected - would require significant code changes

## Implementation Notes

- Use MSK Serverless with VPC integration
- Configure topics with appropriate partition counts (10+ partitions)
- Use IAM for authentication and authorization
- Enable CloudWatch metrics for monitoring
- Implement dead letter queues for failed messages
- Use consumer groups for parallel processing

## References

- [AWS MSK Serverless Documentation](https://docs.aws.amazon.com/msk/latest/developerguide/serverless.html)
- [MSK Best Practices](https://docs.aws.amazon.com/msk/latest/developerguide/best-practices.html)

