#!/bin/bash

# Monitor autonomous test run
# Usage: ./qa-monitor-run.sh [run-id]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RUNS_DIR="$REPO_ROOT/docs/testing/autonomous-runs"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[MONITOR]${NC} $1"
}

# Get latest run if not specified
if [ -z "$1" ]; then
    LATEST_RUN=$(ls -t "$RUNS_DIR" 2>/dev/null | grep -E "^[0-9]{8}-[0-9]{6}-[0-9]+$" | head -1)
    if [ -z "$LATEST_RUN" ]; then
        echo "No runs found"
        exit 1
    fi
    RUN_ID="$LATEST_RUN"
else
    RUN_ID="$1"
fi

RUN_DIR="$RUNS_DIR/$RUN_ID"

if [ ! -d "$RUN_DIR" ]; then
    echo "Run directory not found: $RUN_DIR"
    exit 1
fi

print_info "Monitoring run: $RUN_ID"
print_info "Run directory: $RUN_DIR"

# Check for execution log
EXEC_LOG=$(find "$RUN_DIR" -name "execution.log" | head -1)
if [ -n "$EXEC_LOG" ]; then
    echo ""
    echo "=== Execution Log (last 20 lines) ==="
    tail -20 "$EXEC_LOG" 2>/dev/null || echo "Log not available"
fi

# Check for metadata
METADATA=$(find "$RUN_DIR" -name "metadata.json" | head -1)
if [ -n "$METADATA" ]; then
    echo ""
    echo "=== Run Metadata ==="
    cat "$METADATA" | python3 -m json.tool 2>/dev/null || cat "$METADATA"
fi

# Check for test results
RESULTS=$(find "$RUN_DIR" -name "test-results-*.json" | head -1)
if [ -n "$RESULTS" ]; then
    echo ""
    echo "=== Test Results Summary ==="
    python3 -c "
import json
import sys
try:
    with open('$RESULTS', 'r') as f:
        data = json.load(f)
    results = data.get('results', {})
    summary = data.get('summary', {})
    print(f\"Total Tests: {results.get('total', 0)}\")
    print(f\"Passed: {results.get('passed', 0)}\")
    print(f\"Failed: {results.get('failed', 0)}\")
    print(f\"Pass Rate: {summary.get('passRate', 0)}%\")
    print(f\"Failures: {len(data.get('failures', []))}\")
except Exception as e:
    print(f'Error reading results: {e}')
" 2>/dev/null || echo "Results not available"
fi

# Check for progress log
PROGRESS_LOG="$RUN_DIR/progress-log.json"
if [ -f "$PROGRESS_LOG" ]; then
    echo ""
    echo "=== Progress Log ==="
    cat "$PROGRESS_LOG" | python3 -m json.tool 2>/dev/null || cat "$PROGRESS_LOG"
fi

# Check for final report
FINAL_REPORT=$(find "$RUN_DIR" -name "final-report.md" | head -1)
if [ -n "$FINAL_REPORT" ]; then
    echo ""
    echo "=== Final Report ==="
    cat "$FINAL_REPORT"
fi

echo ""
print_info "To view full logs, check: $RUN_DIR"

