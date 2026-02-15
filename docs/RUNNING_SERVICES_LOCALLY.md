# Running All Leanda Services Locally

This guide explains how to run all Leanda application services locally in JVM while keeping infrastructure services (MongoDB, Kafka, OpenSearch) in Docker.

## Quick Start

```bash
# Start all services (infrastructure in Docker, applications in JVM)
./scripts/start-all-services-local.sh
```

This script will:
1. Start infrastructure services in Docker (MongoDB, Redpanda/Kafka, OpenSearch)
2. Start all application services locally using `mvn quarkus:dev`
3. Wait for all services to be healthy
4. Display service URLs and health check endpoints

## Service Ports

### Infrastructure (Docker)
- **MongoDB**: `localhost:27019` (container: 27017)
- **Redpanda/Kafka**: `localhost:19093` (container: 19093)
- **OpenSearch**: `localhost:9202` (container: 9200)

### Application Services (Local JVM)
- **blob-storage**: `http://localhost:8080`
- **core-api**: `http://localhost:8081` (configured to avoid conflict with blob-storage)
- **chemical-parser**: `http://localhost:8083`
- **chemical-properties**: `http://localhost:8086`
- **reaction-parser**: `http://localhost:8087`
- **crystal-parser**: `http://localhost:8088`
- **spectra-parser**: `http://localhost:8089`
- **imaging**: `http://localhost:8090`
- **office-processor**: `http://localhost:8091`
- **metadata-processing**: `http://localhost:8098`
- **indexing**: `http://localhost:8099`

## Port Conflict Resolution

Both `blob-storage` and `core-api` default to port `8080`. When running locally:
- `blob-storage` uses port `8080` (from `application.properties`)
- `core-api` is configured to use port `8081` via `-Dquarkus.http.port=8081`

## Manual Service Startup

If you prefer to start services manually:

### 1. Start Infrastructure

```bash
cd docker
docker compose -f docker-compose.yml --profile integration up -d mongodb-integration redpanda-integration opensearch-integration
```

### 2. Start Application Services

Each service can be started individually:

```bash
# Set infrastructure connection strings
export MONGODB_CONNECTION_STRING="mongodb://admin:admin123@localhost:27019/leanda-ng?authSource=admin"
export KAFKA_BOOTSTRAP_SERVERS="localhost:19093"
export BLOB_STORAGE_URL="http://localhost:8080"

# Start blob-storage
cd services/blob-storage
mvn quarkus:dev -Dquarkus.http.port=8080

# Start core-api (in another terminal)
cd services/core-api
mvn quarkus:dev -Dquarkus.http.port=8081

# Start other services similarly...
```

## Health Checks

Verify services are healthy:

```bash
# Infrastructure
curl http://localhost:27019  # MongoDB (via mongosh)
curl http://localhost:9202/_cluster/health  # OpenSearch

# Application services
curl http://localhost:8080/health/live  # blob-storage
curl http://localhost:8081/health/live  # core-api
curl http://localhost:8083/health/live  # chemical-parser
# ... etc
```

## Viewing Logs

Service logs are written to `/tmp/leanda-<service-name>.log`:

```bash
# View all service logs
tail -f /tmp/leanda-*.log

# View specific service log
tail -f /tmp/leanda-blob-storage.log
tail -f /tmp/leanda-core-api.log
```

## Stopping Services

The startup script handles cleanup automatically when you press `Ctrl+C`. To stop manually:

```bash
# Stop all application services
pkill -f "quarkus:dev"

# Stop infrastructure
cd docker
docker compose -f docker-compose.yml --profile integration down
```

## Configuration

### Environment Variables

Services automatically use these connection strings when running locally:
- `MONGODB_CONNECTION_STRING`: `mongodb://admin:admin123@localhost:27019/leanda-ng?authSource=admin`
- `KAFKA_BOOTSTRAP_SERVERS`: `localhost:19093`
- `BLOB_STORAGE_URL`: `http://localhost:8080` (for services that need it)

### Service-Specific Configuration

Each service's `application.properties` can be overridden via system properties:

```bash
mvn quarkus:dev \
  -Dquarkus.http.port=8081 \
  -DMONGODB_CONNECTION_STRING="mongodb://..." \
  -DKAFKA_BOOTSTRAP_SERVERS="localhost:19093"
```

## Troubleshooting

### Port Already in Use

If you get "port already in use" errors:
1. Check what's using the port: `lsof -i :8080`
2. Stop the conflicting service
3. Or change the port in the startup command

### Services Not Starting

1. Check service logs: `tail -f /tmp/leanda-<service>.log`
2. Verify infrastructure is running: `docker ps`
3. Check MongoDB connection: `mongosh "mongodb://admin:admin123@localhost:27019/leanda-ng?authSource=admin"`
4. Check Kafka connection: `kafka-console-producer --bootstrap-server localhost:19093 --topic test`

### Health Checks Failing

1. Wait longer - services may take 30-60 seconds to start
2. Check service logs for errors
3. Verify infrastructure services are healthy
4. Check firewall/network settings

## Benefits of Local Execution

✅ **Faster startup**: No Docker image builds/pulls  
✅ **Easier debugging**: Attach debugger directly to JVM  
✅ **Hot reload**: Quarkus dev mode supports live code reload  
✅ **Lower resource usage**: No Docker overhead for application services  
✅ **Better IDE integration**: See logs directly in console, easier to set breakpoints  
✅ **Faster iteration**: Code changes reflect immediately (with hot reload)

## Integration with Tests

To run integration tests with local services:

```bash
export SERVICES_MODE=local
./scripts/run-system-integration-tests.sh
```

This will use the locally running services instead of starting them in Docker.

## See Also

- [LOCAL_SERVICE_MODE.md](../tests/integration/LOCAL_SERVICE_MODE.md) - Detailed local mode documentation for tests
- [README.md](../tests/integration/README.md) - Integration test documentation
