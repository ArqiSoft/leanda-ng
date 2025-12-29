#!/bin/bash
# Agent Initialization Script
# Helps agents get started by reading COORDINATION.md and checking dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
COORDINATION_FILE="$REPO_ROOT/docs/agents/COORDINATION.md"

echo "=========================================="
echo "Leanda NG Agent Initialization"
echo "=========================================="
echo ""

if [ ! -f "$COORDINATION_FILE" ]; then
    echo "❌ Error: COORDINATION.md not found at $COORDINATION_FILE"
    exit 1
fi

echo "📋 Reading coordination file: $COORDINATION_FILE"
echo ""

# Extract current status
echo "Current Project Status:"
grep -A 5 "## Quick Status" "$COORDINATION_FILE" | head -10
echo ""

# Show active agents
echo "Active Agents:"
if grep -q "🟢 In Progress" "$COORDINATION_FILE"; then
    grep -B 2 "🟢 In Progress" "$COORDINATION_FILE" | grep "###" | sed 's/### //' || echo "  None"
else
    echo "  None"
fi
echo ""

# Show next agents to start
echo "Next Agents to Start:"
grep -A 10 "### Currently Active Agents" "$COORDINATION_FILE" | grep -A 5 "### Next Agents" | head -10 || echo "  Check COORDINATION.md"
echo ""

echo "=========================================="
echo "Next Steps:"
echo "1. Read docs/agents/COORDINATION.md"
echo "2. Read docs/agents/AGENT_PROMPTS.md for your agent"
echo "3. Update your status in COORDINATION.md"
echo "4. Begin work!"
echo "=========================================="
