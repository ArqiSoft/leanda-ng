#!/bin/bash
# Service Health Check Script
# Checks health of all services in docker-compose

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
DOCKER_DIR="$REPO_ROOT/docker"

if [ ! -f "$DOCKER_DIR/docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found at $DOCKER_DIR/docker-compose.yml"
    exit 1
fi

echo "=========================================="
echo "Leanda NG Service Health Check"
echo "=========================================="
echo ""

cd "$DOCKER_DIR"

# Check if docker-compose is running
if ! docker-compose ps > /dev/null 2>&1; then
    echo "⚠️  Docker Compose is not running"
    echo "   Start services with: cd docker && docker-compose up -d"
    exit 1
fi

echo "📋 Checking service status..."
echo ""

# Get service list from docker-compose
SERVICES=$(docker-compose config --services 2>/dev/null | grep -v "mongodb\|redis\|redpanda\|opensearch\|minio\|prometheus\|grafana" || true)

if [ -z "$SERVICES" ]; then
    echo "⚠️  No application services found in docker-compose.yml"
    echo "   Infrastructure services may still be running"
    docker-compose ps
    exit 0
fi

# Check each service
ALL_HEALTHY=true

for service in $SERVICES; do
    # Get health status
    STATUS=$(docker-compose ps "$service" 2>/dev/null | tail -n +3 | awk '{print $1}' || echo "not_running")
    
    if [ "$STATUS" = "not_running" ] || [ -z "$STATUS" ]; then
        echo "❌ $service: Not running"
        ALL_HEALTHY=false
    else
        # Try to check health endpoint if it's a web service
        PORT=$(docker-compose port "$service" 8080 2>/dev/null | cut -d: -f2 || echo "")
        if [ -n "$PORT" ]; then
            if curl -sf "http://localhost:$PORT/health/live" > /dev/null 2>&1; then
                echo "✅ $service: Healthy (port $PORT)"
            else
                echo "⚠️  $service: Running but health check failed (port $PORT)"
                ALL_HEALTHY=false
            fi
        else
            echo "✅ $service: Running"
        fi
    fi
done

echo ""

# Check infrastructure services
echo "📋 Infrastructure Services:"
INFRA_SERVICES="mongodb redis redpanda opensearch minio"
for infra in $INFRA_SERVICES; do
    if docker-compose ps "$infra" 2>/dev/null | grep -q "Up"; then
        echo "✅ $infra: Running"
    else
        echo "❌ $infra: Not running"
        ALL_HEALTHY=false
    fi
done

echo ""

if [ "$ALL_HEALTHY" = true ]; then
    echo "=========================================="
    echo "✅ All services are healthy!"
    echo "=========================================="
    exit 0
else
    echo "=========================================="
    echo "⚠️  Some services are not healthy"
    echo "   Check logs with: cd docker && docker-compose logs [service-name]"
    echo "=========================================="
    exit 1
fi

