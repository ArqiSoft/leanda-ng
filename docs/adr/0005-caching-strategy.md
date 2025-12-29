# 0005. Multi-Layer Caching Strategy

## Status

Accepted

## Context

Leanda.io requires high-performance API responses and efficient content delivery. We need to design a caching strategy to:
- Reduce database load
- Improve API response times
- Reduce bandwidth costs
- Improve user experience

**Requirements**:
- Cache API responses for frequently accessed data
- Cache static assets (frontend, images)
- Support cache invalidation
- Handle cache misses gracefully
- Cost-effective solution

## Decision

Implement a **three-layer caching strategy**:
1. **CloudFront (CDN)**: Static assets and API responses
2. **ElastiCache Redis**: Application-level caching
3. **Application Cache (Quarkus)**: In-memory caching

## Consequences

### Positive

- ✅ **Performance**: Reduced latency, improved response times
- ✅ **Cost Reduction**: Reduced database load, bandwidth savings
- ✅ **Scalability**: Offloads traffic from origin servers
- ✅ **User Experience**: Faster page loads, better responsiveness

### Negative

- ⚠️ **Complexity**: Multiple cache layers to manage
- ⚠️ **Cache Invalidation**: Requires careful invalidation strategy
- ⚠️ **Cost**: Additional services (CloudFront, ElastiCache)
- ⚠️ **Stale Data**: Risk of serving stale data if invalidation fails

### Mitigations

1. **Complexity**: Use managed services with automatic management
2. **Invalidation**: Implement cache tags and TTL-based invalidation
3. **Cost**: Right-size ElastiCache, use CloudFront free tier
4. **Stale Data**: Use appropriate TTLs, implement cache versioning

## Implementation Details

### Layer 1: CloudFront (CDN)

**Purpose**: Static assets and API responses

**Configuration**:
- **Static Assets**: TTL 1 hour, cache forever with versioned URLs
- **API Responses**: TTL 5 minutes, cache based on query parameters
- **Origin**: S3 for static assets, API Gateway for API responses

**Cache Invalidation**:
- On deployment: Invalidate static assets
- On data updates: Invalidate specific API paths

### Layer 2: ElastiCache Redis

**Purpose**: Application-level caching for API responses

**Configuration**:
- **Instance Type**: cache.t3.micro (dev), cache.t3.small (prod)
- **TTL**: 15 minutes for API responses, 24 hours for sessions
- **Eviction Policy**: LRU (Least Recently Used)

**Cache Keys**:
- API responses: `api:{service}:{endpoint}:{params}`
- User sessions: `session:{userId}`
- Metadata: `metadata:{entityId}`

**Cache Invalidation**:
- On data updates: Delete specific cache keys
- On user logout: Delete session keys
- TTL-based expiration

### Layer 3: Application Cache (Quarkus)

**Purpose**: In-memory caching for frequently accessed data

**Configuration**:
- **Cache Provider**: Caffeine (in-memory cache)
- **Size**: 100MB per service instance
- **TTL**: 5 minutes

**Use Cases**:
- Frequently accessed metadata
- User permissions
- Configuration data

## Cache Invalidation Strategy

### Event-Driven Invalidation

```java
// On data update, invalidate cache
@Incoming("entity-updated")
public void handleEntityUpdate(EntityUpdatedEvent event) {
    cache.invalidate("metadata:" + event.getEntityId());
    cloudFront.invalidate("/api/entities/" + event.getEntityId());
}
```

### TTL-Based Expiration

- **Short TTL**: Frequently changing data (5 minutes)
- **Medium TTL**: Moderately changing data (15 minutes)
- **Long TTL**: Rarely changing data (1 hour)

### Cache Versioning

- Use versioned cache keys: `v1:metadata:{entityId}`
- Increment version on schema changes
- Old versions expire naturally via TTL

## Alternatives Considered

### Single-Layer Caching (Redis Only)

**Pros**: Simpler, lower cost  
**Cons**: No CDN benefits, higher latency for static assets  
**Decision**: Rejected - does not provide optimal performance

### Two-Layer Caching (CloudFront + Redis)

**Pros**: Good performance, simpler than three layers  
**Cons**: No in-memory caching for hot data  
**Decision**: Rejected - in-memory cache provides additional performance boost

### No Caching

**Pros**: Simplest, no cache invalidation complexity  
**Cons**: Poor performance, high database load, high costs  
**Decision**: Rejected - does not meet performance requirements

## Monitoring and Metrics

- **CloudFront**: Cache hit ratio, bandwidth, requests
- **ElastiCache**: Cache hit ratio, memory usage, evictions
- **Application**: Cache hit ratio, cache size, TTL effectiveness

## References

- [AWS CloudFront Best Practices](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/best-practices.html)
- [ElastiCache Best Practices](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/best-practices.html)
- [Quarkus Caching Guide](https://quarkus.io/guides/cache)

