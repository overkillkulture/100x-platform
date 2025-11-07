#!/bin/bash
# TRINITY WAKE-UP COMMAND
# Usage: ./wake_trinity.sh [role] [reason] [task] [priority]
#
# Examples:
#   ./wake_trinity.sh C2_Architect "Review needed" "Analyze mobile CSS framework"
#   ./wake_trinity.sh C3_Oracle "Pattern analysis" "Study navigation scaling issue" high
#
# Trinity C1 Mechanic - Wake up the network

set -e

if [ $# -lt 3 ]; then
    echo "❌ Usage: ./wake_trinity.sh [role] [reason] [task] [priority]"
    echo ""
    echo "Roles:"
    echo "  - C1_Mechanic   : Builder, ships fast, fixes issues"
    echo "  - C2_Architect  : Designs, plans, reviews architecture"
    echo "  - C3_Oracle     : Analyzes patterns, provides insights"
    echo ""
    echo "Priority: low, medium (default), high"
    echo ""
    echo "Example:"
    echo "  ./wake_trinity.sh C2_Architect \"Review needed\" \"Analyze responsive CSS\" high"
    exit 1
fi

ROLE=$1
REASON=$2
TASK=$3
PRIORITY=${4:-medium}

echo "🌀 Trinity Wake-Up Protocol"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Target Role:  $ROLE"
echo "Reason:       $REASON"
echo "Task:         $TASK"
echo "Priority:     $PRIORITY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Send wake request
python3 TRINITY_CLOUD_COORDINATOR.py --wake "$ROLE" --reason "$REASON" --task "$TASK" --priority "$PRIORITY"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Wake request sent!"
echo ""
echo "Next steps:"
echo "  1. Request committed to git"
echo "  2. Will be pushed to GitHub"
echo "  3. When $ROLE instance starts, it will see the request"
echo "  4. $ROLE will acknowledge and begin work"
echo ""
echo "💤 Wake-up request is now waiting for $ROLE to come online..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
