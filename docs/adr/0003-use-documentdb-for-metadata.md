# 0003. Use DocumentDB for Metadata Storage

## Status

Accepted

## Context

Leanda.io requires a NoSQL database for metadata storage. Services currently use MongoDB-compatible APIs. We need to choose:
- Amazon DocumentDB (MongoDB-compatible, managed)
- Self-managed MongoDB on EC2
- Amazon DynamoDB (NoSQL, serverless)
- Amazon RDS (relational, managed)

**Requirements**:
- MongoDB-compatible API (services use Quarkus MongoDB Panache)
- High availability (multi-AZ)
- Automatic backups and point-in-time recovery
- Minimal operational overhead
- Scalable for growing data volumes

## Decision

Use **Amazon DocumentDB** for all metadata storage.

**Rationale**:
1. **MongoDB-Compatible**: Full MongoDB 5.0 API compatibility, no code changes needed
2. **Managed Service**: Automatic backups, patching, monitoring
3. **High Availability**: Multi-AZ deployment with automatic failover
4. **Scalability**: Read replicas for read-heavy workloads, vertical scaling
5. **Security**: Encryption at rest and in transit, VPC integration
6. **Point-in-Time Recovery**: Automatic backups with 35-day retention

## Consequences

### Positive

- ✅ **Zero Code Changes**: Full MongoDB API compatibility
- ✅ **High Availability**: Multi-AZ with automatic failover (RTO < 60 seconds)
- ✅ **Automatic Backups**: Daily automated snapshots, point-in-time recovery
- ✅ **Scalability**: Read replicas for read scaling, vertical scaling for write scaling
- ✅ **Security**: Encryption, VPC isolation, IAM integration
- ✅ **Operational Simplicity**: No cluster management, automatic patching

### Negative

- ⚠️ **Cost**: More expensive than self-managed MongoDB (mitigated by operational savings)
- ⚠️ **Limited MongoDB Features**: Some advanced MongoDB features not supported
- ⚠️ **Vendor Lock-in**: AWS-specific service (mitigated by MongoDB compatibility)

### Mitigations

1. **Cost**: Right-size instances, use reserved capacity, optimize queries
2. **Features**: DocumentDB supports all features needed by Leanda.io
3. **Lock-in**: MongoDB compatibility provides migration path if needed

## Alternatives Considered

### Self-Managed MongoDB on EC2

**Pros**: Full MongoDB features, potentially lower cost  
**Cons**: Requires cluster management, patching, backups, high operational overhead  
**Decision**: Rejected due to operational complexity

### Amazon DynamoDB

**Pros**: True serverless, automatic scaling, pay-per-use  
**Cons**: Not MongoDB-compatible, requires significant code changes  
**Decision**: Rejected - would require complete rewrite of data access layer

### Amazon RDS

**Pros**: Managed service, high availability  
**Cons**: Relational database, not suitable for document storage  
**Decision**: Rejected - not suitable for document-based data model

## Implementation Notes

- Use DocumentDB cluster with 2+ instances for production (multi-AZ)
- Configure automated backups (daily at 2 AM UTC)
- Enable encryption at rest and in transit
- Use VPC security groups for network isolation
- Configure read replicas for read-heavy workloads
- Monitor performance metrics (CPU, memory, connections)

## References

- [AWS DocumentDB Documentation](https://docs.aws.amazon.com/documentdb/)
- [DocumentDB Best Practices](https://docs.aws.amazon.com/documentdb/latest/developerguide/best-practices.html)

