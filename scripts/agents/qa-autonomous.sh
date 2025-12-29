#!/bin/bash

# Main Orchestrator for Autonomous Testing
# Coordinates all components: execution, parsing, analysis, fixing, iteration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[AUTONOMOUS]${NC} $1"; }
print_success() { echo -e "${GREEN}[AUTONOMOUS]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[AUTONOMOUS]${NC} $1"; }
print_error() { echo -e "${RED}[AUTONOMOUS]${NC} $1"; }

# Parse arguments
TEST_TYPE="${1:-all}"
CONFIDENCE_THRESHOLD="${2:-0.90}"
MAX_ITERATIONS="${3:-10}"

# Generate run ID
RUN_ID="$(date +%Y%m%d-%H%M%S)-$$"
RUN_DIR="$REPO_ROOT/docs/testing/autonomous-runs/$RUN_ID"
mkdir -p "$RUN_DIR"

print_info "Starting autonomous test run"
print_info "Run ID: $RUN_ID"
print_info "Test Type: $TEST_TYPE"
print_info "Confidence Threshold: $CONFIDENCE_THRESHOLD"
print_info "Max Iterations: $MAX_ITERATIONS"

# Initialize storage
python3 "$SCRIPT_DIR/qa-storage.py" create "$RUN_ID" > /dev/null 2>&1 || true

# Initialize progress tracker
ITERATION=0
PROGRESS_LOG="$RUN_DIR/progress-log.json"
echo '{"iterations": []}' > "$PROGRESS_LOG"

# Main loop
while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    ITERATION=$((ITERATION + 1))
    print_info "=== Iteration $ITERATION ==="
    
    # Step 1: Execute tests
    print_info "Step 1: Executing tests..."
    # Capture stderr for logging, stdout for directory path only
    RUN_OUTPUT_DIR=$("$SCRIPT_DIR/qa-autonomous-runner.sh" "$RUN_DIR" "$TEST_TYPE" 3600 2>&1 | tee "$RUN_DIR/runner-output.log" | tail -1)
    RUNNER_EXIT_CODE=${PIPESTATUS[0]}
    if [ $RUNNER_EXIT_CODE -ne 0 ] && [ $ITERATION -eq 1 ]; then
        print_error "Initial test execution failed"
        exit 1
    fi
    
    # Validate the output directory
    if [ ! -d "$RUN_OUTPUT_DIR" ]; then
        print_warn "Output directory not found: $RUN_OUTPUT_DIR, using default"
        RUN_OUTPUT_DIR="$RUN_DIR/$(ls -t "$RUN_DIR" 2>/dev/null | grep -E '^[0-9]{8}-[0-9]{6}-[0-9]+$' | head -1)"
    fi
    
    # Step 2: Parse results
    print_info "Step 2: Parsing test results..."
    RESULTS_DIR="$RUN_OUTPUT_DIR/results"
    
    # Check if results directory exists
    if [ ! -d "$RESULTS_DIR" ]; then
        print_warn "Results directory not found: $RESULTS_DIR"
        # Try alternative locations
        RESULTS_DIR="$RUN_OUTPUT_DIR"
        if [ ! -d "$RESULTS_DIR" ]; then
            print_warn "No results found, skipping parsing"
            # Create empty results file
            echo '{"testRun": {"timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'", "type": "'$TEST_TYPE'", "resultsDirectory": "'$RESULTS_DIR'"}, "results": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0}, "failures": [], "summary": {"passRate": 0.0, "failureRate": 0.0, "status": "no_results", "failureCount": 0}}' > "$RUN_DIR/test-results-iter-$ITERATION.json"
            FAILURE_COUNT=0
        fi
    fi
    
    if [ -d "$RESULTS_DIR" ]; then
        python3 "$SCRIPT_DIR/qa-result-parser.py" "$RESULTS_DIR" "$RUN_DIR/test-results-iter-$ITERATION.json" || {
            print_error "Failed to parse results"
            break
        }
    fi
    
    # Store results
    python3 "$SCRIPT_DIR/qa-storage.py" store "$RUN_ID" "$RUN_DIR/test-results-iter-$ITERATION.json" > /dev/null 2>&1 || true
    
    # Load results
    TEST_RESULTS=$(cat "$RUN_DIR/test-results-iter-$ITERATION.json")
    FAILURE_COUNT=$(echo "$TEST_RESULTS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(len(d.get('failures', [])))")
    TOTAL_TESTS=$(echo "$TEST_RESULTS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('results', {}).get('total', 0))")
    STATUS=$(echo "$TEST_RESULTS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('summary', {}).get('status', 'unknown'))")
    
    print_info "Failures found: $FAILURE_COUNT"
    print_info "Total tests: $TOTAL_TESTS"
    print_info "Status: $STATUS"
    
    # Check if all tests passed (but only if we actually ran tests)
    if [ "$FAILURE_COUNT" -eq 0 ] && [ "$TOTAL_TESTS" -gt 0 ]; then
        print_success "All tests passed!"
        break
    fi
    
    # If no tests ran but we have compilation errors, continue fixing
    if [ "$TOTAL_TESTS" -eq 0 ] && [ "$FAILURE_COUNT" -eq 0 ]; then
        # Check execution log for build failures
        if [ -f "$RUN_OUTPUT_DIR/execution.log" ]; then
            if grep -q "BUILD FAILURE\|compilation\|cannot find symbol\|package.*does not exist" "$RUN_OUTPUT_DIR/execution.log" 2>/dev/null; then
                print_warn "Build failures detected but not parsed. Re-parsing execution log..."
                # Re-parse with execution log
                python3 "$SCRIPT_DIR/qa-result-parser.py" "$RUN_OUTPUT_DIR" "$RUN_DIR/test-results-iter-$ITERATION.json" || {
                    print_error "Failed to re-parse results"
                    break
                }
                # Reload results
                TEST_RESULTS=$(cat "$RUN_DIR/test-results-iter-$ITERATION.json")
                FAILURE_COUNT=$(echo "$TEST_RESULTS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(len(d.get('failures', [])))")
                TOTAL_TESTS=$(echo "$TEST_RESULTS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('results', {}).get('total', 0))")
                print_info "After re-parsing: Failures: $FAILURE_COUNT, Total: $TOTAL_TESTS"
                
                if [ "$FAILURE_COUNT" -eq 0 ]; then
                    print_warn "No failures detected after re-parsing. Stopping."
                    break
                fi
            else
                print_warn "No tests ran and no build failures detected. Stopping."
                break
            fi
        else
            print_warn "No tests ran and no execution log found. Stopping."
            break
        fi
    fi
    
    # Step 3: Analyze problems
    print_info "Step 3: Analyzing problems..."
    python3 "$SCRIPT_DIR/qa-problem-analyzer.py" "$RUN_DIR/test-results-iter-$ITERATION.json" "$RUN_DIR/failures-analysis-iter-$ITERATION.json" || {
        print_error "Failed to analyze problems"
        break
    }
    
    # Step 4: Find solutions
    print_info "Step 4: Finding solutions..."
    python3 "$SCRIPT_DIR/qa-solution-finder.py" "$RUN_DIR/failures-analysis-iter-$ITERATION.json" "$RUN_DIR/solutions-iter-$ITERATION.json" || {
        print_error "Failed to find solutions"
        break
    }
    
    # Step 5: Apply fixes
    print_info "Step 5: Applying fixes..."
    python3 "$SCRIPT_DIR/qa-auto-fix.py" "$RUN_DIR/solutions-iter-$ITERATION.json" "$RUN_DIR/fixes-iter-$ITERATION.json" "$CONFIDENCE_THRESHOLD" || {
        print_warn "Some fixes failed to apply"
    }
    
    # Track progress
    PROGRESS_DATA=$(cat <<EOF
{
  "failureCount": $FAILURE_COUNT,
  "fixesApplied": $(cat "$RUN_DIR/fixes-iter-$ITERATION.json" 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('summary', {}).get('applied', 0))" 2>/dev/null || echo 0)
}
EOF
)
    
    PROGRESS_RESULT=$(echo "$PROGRESS_DATA" | python3 "$SCRIPT_DIR/qa-progress-tracker.py" add - 2>&1)
    echo "$PROGRESS_RESULT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(json.dumps(d, indent=2))" > "$RUN_DIR/progress-iter-$ITERATION.json" 2>/dev/null || true
    
    # Check if should continue
    SHOULD_CONTINUE=$(echo "$PROGRESS_RESULT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('shouldContinue', False))" 2>/dev/null || echo "true")
    
    # Always continue if we have failures, even if fixes were skipped
    if [ "$FAILURE_COUNT" -gt 0 ]; then
        SHOULD_CONTINUE="true"
        print_info "Failures still present - continuing to next iteration"
    fi
    
    if [ "$SHOULD_CONTINUE" != "True" ] && [ "$SHOULD_CONTINUE" != "true" ]; then
        print_warn "Progress tracker indicates we should stop"
        break
    fi
    
    # Update progress log
    python3 -c "
import json
with open('$PROGRESS_LOG', 'r') as f:
    data = json.load(f)
data['iterations'].append($PROGRESS_DATA)
with open('$PROGRESS_LOG', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null || true
    
    sleep 2  # Brief pause between iterations
done

# Generate final report
print_info "Generating final report..."
python3 -c "
import json
from datetime import datetime

# Load all data
try:
    with open('$RUN_DIR/test-results-iter-$ITERATION.json', 'r') as f:
        results = json.load(f)
    with open('$RUN_DIR/failures-analysis-iter-$ITERATION.json', 'r') as f:
        analysis = json.load(f)
    with open('$RUN_DIR/fixes-iter-$ITERATION.json', 'r') as f:
        fixes = json.load(f)
except:
    results = {'failures': []}
    analysis = {'statistics': {}}
    fixes = {'summary': {}}

report = f'''# Autonomous Test Run Report

**Run ID**: $RUN_ID
**Test Type**: $TEST_TYPE
**Iterations**: $ITERATION
**Date**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Summary

- **Total Failures**: {len(results.get('failures', []))}
- **Fixes Applied**: {fixes.get('summary', {}).get('applied', 0)}
- **Fixes Skipped**: {fixes.get('summary', {}).get('skipped', 0)}
- **Pass Rate**: {results.get('summary', {}).get('passRate', 0)}%

## Failures

{len(results.get('failures', []))} test failures identified.

## Fixes Applied

{fixes.get('summary', {}).get('applied', 0)} fixes were automatically applied.

## Next Steps

Review the fixes and test results in this directory.
'''

with open('$RUN_DIR/final-report.md', 'w') as f:
    f.write(report)
" 2>/dev/null || true

# Create PR if fixes were applied
FIXES_APPLIED=$(cat "$RUN_DIR/fixes-iter-$ITERATION.json" 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('summary', {}).get('applied', 0))" 2>/dev/null || echo 0)

if [ "$FIXES_APPLIED" -gt 0 ]; then
    print_info "Creating PR for applied fixes..."
    "$SCRIPT_DIR/qa-create-pr.sh" "$RUN_ID" "$RUN_DIR/final-report.md" || {
        print_warn "PR creation failed or skipped"
    }
fi

print_success "Autonomous test run complete"
print_info "Results in: $RUN_DIR"
print_info "Run ID: $RUN_ID"

