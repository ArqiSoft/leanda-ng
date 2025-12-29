#!/bin/bash
# Agent Status Check Script
# Shows current status of all agents from COORDINATION.md

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
COORDINATION_FILE="$REPO_ROOT/docs/agents/COORDINATION.md"

if [ ! -f "$COORDINATION_FILE" ]; then
    echo "❌ Error: COORDINATION.md not found at $COORDINATION_FILE"
    exit 1
fi

echo "=========================================="
echo "Leanda NG Agent Status"
echo "=========================================="
echo ""

# Show quick status table
echo "📊 Quick Status:"
grep -A 10 "## Quick Status" "$COORDINATION_FILE" | head -12
echo ""

# Show active agents
echo "🟢 Active Agents:"
if grep -q "🟢 In Progress" "$COORDINATION_FILE"; then
    grep -B 2 "🟢 In Progress" "$COORDINATION_FILE" | grep "###" | sed 's/### //' | sed 's/^/  /'
else
    echo "  None"
fi
echo ""

# Show blocked agents
echo "🟡 Blocked Agents:"
if grep -q "🟡 Blocked" "$COORDINATION_FILE"; then
    grep -B 2 "🟡 Blocked" "$COORDINATION_FILE" | grep "###" | sed 's/### //' | sed 's/^/  /'
else
    echo "  None"
fi
echo ""

# Show completed agents (last 5)
echo "✅ Recently Completed:"
grep -B 2 "✅ Complete" "$COORDINATION_FILE" | grep "###" | sed 's/### //' | head -5 | sed 's/^/  /'
echo ""

# Show pending agents
echo "⏳ Pending Agents:"
grep -B 2 "⏳ Pending" "$COORDINATION_FILE" | grep "###" | sed 's/### //' | head -5 | sed 's/^/  /'
echo ""

echo "=========================================="
echo "For full details, see: docs/agents/COORDINATION.md"
echo "=========================================="
