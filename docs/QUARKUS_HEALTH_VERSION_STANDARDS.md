# Quarkus Health and Version Standards

## Overview

Quarkus provides standard extensions for health checks and version information:

1. **SmallRye Health** (`quarkus-smallrye-health`) - Standard health check endpoints
2. **Quarkus Info** (`quarkus-info`) - Standard application information endpoints

## Health Checks (SmallRye Health)

### Dependency

```xml
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-smallrye-health</artifactId>
</dependency>
```

### Configuration

```properties
# Health check configuration
quarkus.smallrye-health.root-path=/health
quarkus.smallrye-health.liveness-path=/live
quarkus.smallrye-health.readiness-path=/ready
quarkus.smallrye-health.startup-path=/started
```

### Standard Endpoints

**Important**: Health endpoints are served at `/q/health/*` by default (Quarkus non-application-root-path).

- `/q/health` - Overall health status (aggregates all checks)
- `/q/health/live` - Liveness probe (service is alive, doesn't check dependencies)
- `/q/health/ready` - Readiness probe (service is ready, checks MongoDB, Kafka, etc.)
- `/q/health/started` - Startup probe (service has started)

**When to use each endpoint**:
- **Liveness (`/q/health/live`)**: Use for startup checks and Kubernetes liveness probes. Returns UP if the service process is running, regardless of dependency status (Kafka, MongoDB).
- **Readiness (`/q/health/ready`)**: Use for dependency verification and Kubernetes readiness probes. Returns UP only if all dependencies (MongoDB, Kafka, Reactive Messaging channels) are connected and healthy.
- **Startup checks**: Always use liveness endpoint to avoid blocking service startup when dependencies aren't ready yet.

### Implementation Options

#### Option 1: Automatic Health Checks (Recommended)

SmallRye Health automatically provides health checks for:
- Database connections (MongoDB, PostgreSQL, etc.)
- Kafka connections
- Reactive Messaging channels

No custom code needed - just configure the extension.

#### Option 2: Custom Health Checks

Create custom health checks using `@Liveness` and `@Readiness` annotations:

```java
@ApplicationScoped
public class CustomHealthCheck implements HealthCheck {
    
    @Liveness
    public HealthCheckResponse liveness() {
        return HealthCheckResponse.named("Service Liveness")
            .up()
            .build();
    }
    
    @Readiness
    public HealthCheckResponse readiness() {
        // Check dependencies (MongoDB, Kafka, etc.)
        return HealthCheckResponse.named("Service Readiness")
            .up()
            .withData("mongodb", "connected")
            .withData("kafka", "connected")
            .build();
    }
}
```

#### Option 3: JAX-RS Resource (Not Recommended)

Custom `@Path("/health")` resources can conflict with SmallRye Health. 
**Avoid this approach** - use HealthCheck implementations instead.

## Version Information (Quarkus Info)

### Dependency

```xml
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-info</artifactId>
</dependency>
```

### Configuration

```properties
# Enable info endpoint
quarkus.info.enabled=true
quarkus.info.path=/info

# Build information (from Maven/Gradle)
quarkus.info.build.enabled=true
quarkus.info.build.time=true
quarkus.info.build.version=true

# Git information (optional)
quarkus.info.git.enabled=true
quarkus.info.git.mode=full
```

### Standard Endpoints

- `/info` - Application information (version, build time, git info)

### Response Format

```json
{
  "app": {
    "name": "leanda-ng-blob-storage",
    "version": "1.0.0-SNAPSHOT"
  },
  "build": {
    "time": "2026-01-13T10:00:00Z",
    "version": "1.0.0-SNAPSHOT"
  },
  "git": {
    "branch": "main",
    "commit": {
      "id": "abc123",
      "time": "2026-01-13T09:00:00Z"
    }
  }
}
```

### Custom Info Providers

You can add custom information:

```java
@ApplicationScoped
public class CustomInfoProvider implements InfoContributor {
    
    @Override
    public void contribute(Info.Builder builder) {
        builder.withDetail("custom", Map.of(
            "environment", System.getenv("ENV"),
            "region", "us-east-1"
        ));
    }
}
```

## Best Practices

1. **Use SmallRye Health for health checks** - Don't create custom `/health` JAX-RS resources
2. **Use Quarkus Info for version info** - Don't create custom `/version` endpoints
3. **Use Quarkus default paths** - Health endpoints are at `/q/health/live` and `/q/health/ready` (Quarkus default). Do NOT set `quarkus.http.non-application-root-path` unless necessary.
4. **Use liveness for startup checks** - Use `/q/health/live` for startup verification (doesn't require dependencies to be ready)
5. **Use readiness for dependency checks** - Use `/q/health/ready` to verify all dependencies (MongoDB, Kafka) are connected
6. **Enable build info** - Use `quarkus-info` to automatically expose build metadata
7. **Add custom checks when needed** - Use `HealthCheck` implementations for service-specific checks

## Migration from Custom Resources

If you have custom `HealthResource` or `VersionResource` classes:

1. Remove the custom JAX-RS resources
2. Add `quarkus-smallrye-health` and `quarkus-info` dependencies
3. Configure the extensions in `application.properties`
4. Create `HealthCheck` implementations if custom logic is needed
5. Use `InfoContributor` for custom version/build information

## Example: Complete Configuration

### pom.xml

```xml
<dependencies>
    <!-- Health checks -->
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-smallrye-health</artifactId>
    </dependency>
    
    <!-- Version/build info -->
    <dependency>
        <groupId>io.quarkus</groupId>
        <artifactId>quarkus-info</artifactId>
    </dependency>
</dependencies>
```

### application.properties

```properties
# Health checks (SmallRye Health)
# Health endpoints at /q/health/live and /q/health/ready (Quarkus default)
# Liveness (/q/health/live): Service is alive (doesn't check dependencies)
# Readiness (/q/health/ready): Service is ready (checks MongoDB, Kafka, etc.)
# DO NOT set quarkus.http.non-application-root-path - use default /q path
quarkus.smallrye-health.root-path=/health
quarkus.smallrye-health.liveness-path=/live
quarkus.smallrye-health.readiness-path=/ready

# Version/build info
quarkus.info.enabled=true
quarkus.info.path=/info
quarkus.info.build.enabled=true
quarkus.info.git.enabled=true
```

### Custom Health Check (if needed)

```java
package io.leanda.service.infrastructure.health;

import jakarta.enterprise.context.ApplicationScoped;
import org.eclipse.microprofile.health.HealthCheck;
import org.eclipse.microprofile.health.HealthCheckResponse;
import org.eclipse.microprofile.health.Liveness;
import org.eclipse.microprofile.health.Readiness;

@ApplicationScoped
public class ServiceHealthCheck implements HealthCheck {
    
    @Liveness
    public HealthCheckResponse liveness() {
        return HealthCheckResponse.named("Service Liveness")
            .up()
            .build();
    }
    
    @Readiness
    public HealthCheckResponse readiness() {
        // Add dependency checks here
        return HealthCheckResponse.named("Service Readiness")
            .up()
            .withData("dependencies", "all-connected")
            .build();
    }
}
```

## References

- [Quarkus SmallRye Health Guide](https://quarkus.io/guides/smallrye-health)
- [Quarkus Info Extension](https://quarkus.io/guides/info)
- [MicroProfile Health Specification](https://microprofile.io/project/eclipse/microprofile-health)
