# QA Autonomous Testing Scripts

**Last Updated**: 2025-12-28  
**Agent**: QA-Cloud

## Overview

This directory contains scripts for autonomous testing and troubleshooting. The system can execute tests, analyze failures, find solutions, apply fixes, and iterate until resolution.

## Scripts

### Main Entry Point

- **`qa-autonomous.sh`** - Main orchestrator script
  - Coordinates all components
  - Manages iteration loop
  - Usage: `./qa-autonomous.sh [test-type] [confidence] [max-iterations]`

### Core Components

1. **`qa-autonomous-runner.sh`** - Test execution wrapper
   - Executes tests in Docker
   - Captures results and logs

2. **`qa-result-parser.py`** - Test result parser
   - Parses JUnit XML and Playwright reports
   - Generates structured JSON

3. **`qa-storage.py`** - Result storage system
   - Manages run directories
   - Tracks run history

4. **`qa-problem-analyzer.py`** - Problem analyzer
   - Categorizes failures
   - Calculates confidence scores

5. **`qa-solution-finder.py`** - Solution finder
   - Searches codebase for fixes
   - Generates fix suggestions

6. **`qa-auto-fix.py`** - Auto-fix engine
   - Applies fixes with safeguards
   - Checks protected files
   - Creates backups

7. **`qa-progress-tracker.py`** - Progress tracker
   - Monitors iteration progress
   - Detects no-progress scenarios

8. **`qa-create-pr.sh`** - PR creator
   - Creates git branches
   - Creates PRs for fixes

### Configuration

- **`qa-protected-files.txt`** - List of protected files that should never be modified

## Usage

See [Autonomous Testing Runbook](../../docs/testing/autonomous-testing-runbook.md) for complete documentation.

## Quick Start

```bash
# Run autonomous testing
./qa-autonomous.sh all

# Run with custom settings
./qa-autonomous.sh unit 0.90 5
```

## Output

Results are stored in `docs/testing/autonomous-runs/[run-id]/`

---

**See Also**:
- [Autonomous Testing Runbook](../../docs/testing/autonomous-testing-runbook.md)
- [Testing Strategy](../../docs/testing/testing-strategy.md)

