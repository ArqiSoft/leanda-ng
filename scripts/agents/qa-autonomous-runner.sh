#!/bin/bash

# Autonomous Test Execution Runner
# Wraps docker/run-tests.sh and extracts results for autonomous processing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCKER_DIR="$REPO_ROOT/docker"
OUTPUT_DIR="${1:-$REPO_ROOT/docs/testing/autonomous-runs/temp}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[TEST RUNNER]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[TEST RUNNER]${NC} $1"
}

print_error() {
    echo -e "${RED}[TEST RUNNER]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[TEST RUNNER]${NC} $1"
}

# Parse arguments
TEST_TYPE="${2:-all}"
TIMEOUT="${3:-3600}"  # Default 1 hour timeout

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Create run metadata
RUN_ID="$(date +%Y%m%d-%H%M%S)-$$"
RUN_DIR="$OUTPUT_DIR/$RUN_ID"
mkdir -p "$RUN_DIR"

print_info "Starting autonomous test execution"
print_info "Run ID: $RUN_ID"
print_info "Test Type: $TEST_TYPE"
print_info "Output Directory: $RUN_DIR"

# Create execution log
EXEC_LOG="$RUN_DIR/execution.log"
{
    echo "=== Test Execution Log ==="
    echo "Run ID: $RUN_ID"
    echo "Test Type: $TEST_TYPE"
    echo "Start Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "Timeout: ${TIMEOUT}s"
    echo ""
} > "$EXEC_LOG"

# Function to extract test results from Docker volume
extract_results() {
    local extract_dir="$RUN_DIR/results"
    
    print_info "Extracting test results..."
    mkdir -p "$extract_dir"
    
    # First, try to get results from docker/test-results (where run-tests.sh puts them)
    if [ -d "$DOCKER_DIR/test-results" ]; then
        print_info "Copying results from docker/test-results..."
        cp -r "$DOCKER_DIR/test-results"/* "$extract_dir/" 2>/dev/null || true
        
        # Check if we got any results
        if [ "$(ls -A "$extract_dir" 2>/dev/null)" ]; then
            print_success "Results extracted to $extract_dir"
            return 0
        fi
    fi
    
    # Also try Docker volume (if it exists)
    local volume_name="leanda-ng-test-results"
    if docker volume inspect "$volume_name" > /dev/null 2>&1; then
        print_info "Copying results from Docker volume..."
        docker run --rm \
            -v "$volume_name:/source:ro" \
            -v "$extract_dir:/dest" \
            alpine sh -c "cp -r /source/* /dest/ 2>/dev/null || true" || {
            print_warn "Failed to extract some results from volume"
        }
    fi
    
    # Check if we got any results
    if [ "$(ls -A "$extract_dir" 2>/dev/null)" ]; then
        print_success "Results extracted to $extract_dir"
        return 0
    else
        print_warn "No test results found. Tests may not have produced results."
        return 1
    fi
}

# Function to run tests with timeout
run_tests_with_timeout() {
    local test_type=$1
    local timeout=$2
    
    print_info "Executing tests with timeout of ${timeout}s..."
    
    cd "$DOCKER_DIR"
    
    # Run tests with timeout (macOS compatible)
    if command -v timeout > /dev/null 2>&1; then
        # Linux timeout command
        if timeout "$timeout" ./run-tests.sh "$test_type" >> "$EXEC_LOG" 2>&1; then
            local exit_code=$?
            echo "Exit Code: $exit_code" >> "$EXEC_LOG"
            return $exit_code
        else
            local exit_code=$?
            echo "Exit Code: $exit_code (timeout or error)" >> "$EXEC_LOG"
            print_warn "Test execution timed out or failed"
            return $exit_code
        fi
    else
        # macOS - run without timeout (Docker will handle timeouts)
        if ./run-tests.sh "$test_type" >> "$EXEC_LOG" 2>&1; then
            local exit_code=$?
            echo "Exit Code: $exit_code" >> "$EXEC_LOG"
            return $exit_code
        else
            local exit_code=$?
            echo "Exit Code: $exit_code (error)" >> "$EXEC_LOG"
            print_warn "Test execution failed"
            return $exit_code
        fi
    fi
}

# Function to capture Docker container logs
capture_logs() {
    local logs_dir="$RUN_DIR/logs"
    mkdir -p "$logs_dir"
    
    print_info "Capturing Docker container logs..."
    
    # Get logs from test containers
    cd "$DOCKER_DIR"
    
    # Capture logs from all test-related containers
    for container in $(docker-compose -f docker-compose.test.yml ps -q 2>/dev/null || true); do
        if [ -n "$container" ]; then
            local container_name=$(docker inspect --format='{{.Name}}' "$container" | sed 's/^\///')
            docker logs "$container" > "$logs_dir/${container_name}.log" 2>&1 || true
        fi
    done
    
    print_success "Logs captured to $logs_dir"
}

# Main execution
START_TIME=$(date +%s)

print_info "Changing to Docker directory: $DOCKER_DIR"
cd "$DOCKER_DIR"

# Run tests
if run_tests_with_timeout "$TEST_TYPE" "$TIMEOUT"; then
    TEST_EXIT_CODE=0
    print_success "Tests completed successfully"
else
    TEST_EXIT_CODE=$?
    print_warn "Tests completed with exit code: $TEST_EXIT_CODE"
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Capture logs
capture_logs

# Extract results
extract_results || true

# Create execution summary
{
    echo ""
    echo "=== Execution Summary ==="
    echo "End Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "Duration: ${DURATION}s"
    echo "Exit Code: $TEST_EXIT_CODE"
    echo "Test Type: $TEST_TYPE"
} >> "$EXEC_LOG"

# Create metadata JSON
cat > "$RUN_DIR/metadata.json" <<EOF
{
  "runId": "$RUN_ID",
  "testType": "$TEST_TYPE",
  "startTime": "$(date -u -r $START_TIME +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)",
  "endTime": "$(date -u -r $END_TIME +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)",
  "duration": $DURATION,
  "exitCode": $TEST_EXIT_CODE,
  "resultsPath": "$RUN_DIR/results",
  "logsPath": "$RUN_DIR/logs",
  "executionLog": "$EXEC_LOG"
}
EOF

print_success "Test execution complete"
print_info "Results available in: $RUN_DIR"
print_info "Run ID: $RUN_ID"

# Output run directory for next step (to stdout, without colors)
# All other output goes to stderr via print_* functions
echo "$RUN_DIR" >&1

exit $TEST_EXIT_CODE

