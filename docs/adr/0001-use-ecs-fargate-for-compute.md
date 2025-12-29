# 0001. Use ECS Fargate for Compute

## Status

Accepted

## Context

Leanda.io requires a container orchestration platform to run 11 Java/Quarkus microservices. We need to choose between:
- Amazon ECS Fargate (serverless containers)
- Amazon ECS with EC2 instances (self-managed)
- Amazon EKS (Kubernetes)
- AWS Lambda (serverless functions)

**Requirements**:
- Support Java/Quarkus applications (not suitable for Lambda)
- Auto-scaling based on load
- Multi-AZ deployment for high availability
- Minimal operational overhead
- Cost-effective for variable workloads

## Decision

Use **Amazon ECS Fargate** for all microservices compute.

**Rationale**:
1. **Serverless**: No EC2 instance management, automatic scaling
2. **Java/Quarkus Support**: Full support for containerized Java applications
3. **Multi-AZ**: Built-in support for multi-AZ deployment
4. **Cost-Effective**: Pay only for running tasks, no idle instances
5. **Operational Simplicity**: No cluster management, patching, or capacity planning
6. **Integration**: Seamless integration with ALB, CloudWatch, IAM

## Consequences

### Positive

- ✅ **Reduced Operational Overhead**: No EC2 instance management
- ✅ **Automatic Scaling**: ECS handles scaling based on metrics
- ✅ **Cost Optimization**: Pay-per-use, no idle capacity
- ✅ **Security**: Fargate tasks run in isolated compute environments
- ✅ **Multi-AZ Resilience**: Automatic distribution across availability zones

### Negative

- ⚠️ **Cold Start**: 30-60 second startup time for new tasks (mitigated with min capacity)
- ⚠️ **Cost at Scale**: May be more expensive than EC2 for 24/7 workloads (mitigated with reserved capacity)
- ⚠️ **Limited Control**: Less control over underlying infrastructure compared to EC2

### Mitigations

1. **Cold Start**: Maintain minimum 2 tasks per service to avoid cold starts
2. **Cost**: Use reserved capacity for predictable workloads, right-size tasks
3. **Control**: Use ECS task definitions for fine-grained control over CPU/memory

## Alternatives Considered

### Amazon ECS with EC2

**Pros**: More control, potentially lower cost for 24/7 workloads  
**Cons**: Requires EC2 instance management, patching, capacity planning  
**Decision**: Rejected due to operational overhead

### Amazon EKS (Kubernetes)

**Pros**: Industry standard, extensive ecosystem  
**Cons**: Higher complexity, requires Kubernetes expertise, more expensive  
**Decision**: Rejected due to complexity and cost

### AWS Lambda

**Pros**: True serverless, automatic scaling  
**Cons**: Not suitable for Java/Quarkus long-running services, cold starts  
**Decision**: Rejected - not suitable for microservices architecture

## Implementation Notes

- Use ECS Fargate with Application Load Balancer for traffic distribution
- Configure auto-scaling based on CPU, memory, and custom metrics
- Use ECR for container image storage
- Implement health checks for automatic task replacement
- Use service discovery (Cloud Map) for service-to-service communication

## References

- [AWS ECS Fargate Documentation](https://docs.aws.amazon.com/ecs/latest/developerguide/AWS_Fargate.html)
- [ECS Best Practices](https://docs.aws.amazon.com/ecs/latest/bestpracticesguide/intro.html)

