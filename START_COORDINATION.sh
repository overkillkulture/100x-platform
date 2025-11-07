#!/bin/bash
# START_COORDINATION.sh - Quick start script for multi-instance coordination

echo "========================================"
echo "🚀 STARTING MULTI-INSTANCE COORDINATION"
echo "========================================"
echo ""

# 1. Start Central Hub
echo "1. Starting Central Hub server..."
python3 TRINITY_CENTRAL_HUB.py &
HUB_PID=$!
echo "   ✅ Hub started (PID: $HUB_PID)"
echo "   📊 Dashboard: http://localhost:8888"
echo ""

sleep 3

# 2. Instructions for instances
echo "2. FOR EACH CLAUDE INSTANCE:"
echo "   Run this in each instance:"
echo ""
echo "   python3 INSTANCE_REPORTER.py"
echo ""
echo "   When prompted:"
echo "   - Instance 1: claude-c1-001 | Role: C1-Mechanic"
echo "   - Instance 2: claude-c2-001 | Role: C2-Architect"
echo "   - Instance 3: claude-c3-001 | Role: C3-Oracle"
echo "   - Instance 4-6: claude-c4-001 | Role: C4-Specialist"
echo ""

echo "3. CLAIM TASKS:"
echo "   View available tasks in dashboard"
echo "   Each instance claims a task and starts working"
echo ""

echo "4. VIEW STATUS:"
echo "   Open: http://localhost:8888"
echo "   See all instances, their tasks, and status"
echo ""

echo "========================================"
echo "✅ COORDINATION HUB RUNNING"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop hub"
echo ""

# Wait for hub process
wait $HUB_PID
