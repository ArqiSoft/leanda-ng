#!/bin/bash

# Script to run all tests locally in Docker
# Usage: ./run-tests.sh [unit|integration|e2e|all]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.test.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to cleanup
cleanup() {
    print_info "Cleaning up test containers..."
    cd "$SCRIPT_DIR"
    docker-compose -f docker-compose.test.yml down --volumes 2>/dev/null || true
}

# Trap to cleanup on exit
trap cleanup EXIT

# Parse arguments
TEST_TYPE="${1:-all}"

case "$TEST_TYPE" in
    unit)
        PROFILE="unit-tests"
        SERVICE="unit-tests-runner"
        ;;
    integration)
        PROFILE="integration-tests"
        SERVICE="integration-tests-runner"
        ;;
    e2e)
        PROFILE="e2e-tests"
        SERVICE="e2e-tests-runner"
        ;;
    all)
        PROFILE="all-tests"
        SERVICE="all-tests-runner"
        ;;
    *)
        print_error "Invalid test type: $TEST_TYPE"
        echo "Usage: $0 [unit|integration|e2e|all]"
        exit 1
        ;;
esac

print_info "Running $TEST_TYPE tests in Docker..."
print_info "Using compose file: $COMPOSE_FILE"

# Check Docker
check_docker

# Change to script directory
cd "$SCRIPT_DIR"

# Start infrastructure services
print_info "Starting infrastructure services..."
docker-compose -f docker-compose.test.yml up -d mongodb-test kafka-test zookeeper-test opensearch-test

# Wait for services to be healthy
print_info "Waiting for services to be healthy..."
timeout=60
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if docker-compose -f docker-compose.test.yml ps | grep -q "healthy"; then
        break
    fi
    sleep 2
    elapsed=$((elapsed + 2))
done

# Start service containers if needed (for integration/E2E tests)
if [[ "$TEST_TYPE" == "integration" || "$TEST_TYPE" == "e2e" || "$TEST_TYPE" == "all" ]]; then
    print_info "Starting service containers..."
    docker-compose -f docker-compose.test.yml --profile "$PROFILE" up -d core-api-test blob-storage-test 2>/dev/null || true
    
    # Wait for services to be healthy
    print_info "Waiting for services to be ready..."
    sleep 10
fi

# Run tests
print_info "Running $TEST_TYPE tests..."
if docker-compose -f docker-compose.test.yml --profile "$PROFILE" run --rm "$SERVICE"; then
    print_info "Tests completed successfully!"
    
    # Extract test results
    print_info "Extracting test results..."
    RESULTS_DIR="${SCRIPT_DIR}/test-results"
    mkdir -p "$RESULTS_DIR"
    
    # Copy results from Docker volume
    VOLUME_NAME="docker_test-results"
    if docker volume inspect "$VOLUME_NAME" > /dev/null 2>&1; then
        print_info "Copying results from Docker volume..."
        docker run --rm \
            -v "$VOLUME_NAME:/source:ro" \
            -v "$RESULTS_DIR:/dest" \
            alpine sh -c "cp -r /source/* /dest/ 2>/dev/null || true" || {
            print_warn "Failed to copy some results from volume"
        }
    fi
    
    # Also try to copy from container if it still exists
    CONTAINER_ID=$(docker-compose -f docker-compose.test.yml --profile "$PROFILE" ps -q "$SERVICE" 2>/dev/null | head -1)
    if [ -n "$CONTAINER_ID" ] && docker ps -a --format '{{.ID}}' | grep -q "$CONTAINER_ID"; then
        print_info "Copying results from container..."
        docker cp "${CONTAINER_ID}:/workspace/test-results" "$RESULTS_DIR" 2>/dev/null || true
    fi
    
    print_info "Test results available in: $RESULTS_DIR"
else
    print_error "Tests failed!"
    exit 1
fi

