#!/bin/bash
# CLAIM A TASK ON LOCAL BOARD

COORD_DIR="LOCAL_COORDINATION"
mkdir -p "$COORD_DIR"

echo "═══════════════════════════════════════"
echo "CLAIM A TASK"
echo "═══════════════════════════════════════"
echo ""
echo "Your instance number: "
read INSTANCE_NUM

echo ""
echo "Available tasks:"
echo "  1) Integration testing framework"
echo "  2) Deployment preparation package"
echo "  3) Module #24: Real-time collaboration"
echo "  4) Module #25: Advanced code generation"
echo "  5) Module #26: Multi-modal processing"
echo "  6) Custom task (enter your own)"
echo ""
echo "Select task (1-6): "
read TASK_NUM

case $TASK_NUM in
  1) TASK="Integration testing framework" ;;
  2) TASK="Deployment preparation package" ;;
  3) TASK="Module #24: Real-time collaboration" ;;
  4) TASK="Module #25: Advanced code generation" ;;
  5) TASK="Module #26: Multi-modal processing" ;;
  6)
    echo "Enter custom task: "
    read TASK
    ;;
  *) echo "Invalid choice"; exit 1 ;;
esac

# Record claim
echo "[$(date '+%H:%M:%S')] Instance $INSTANCE_NUM claimed: $TASK" >> "$COORD_DIR/claimed_tasks.txt"

# Update instance file
if [ -f "$COORD_DIR/instance_${INSTANCE_NUM}.txt" ]; then
  sed -i "s/^TASK:.*/TASK: $TASK/" "$COORD_DIR/instance_${INSTANCE_NUM}.txt"
fi

echo ""
echo "✅ Task claimed: $TASK"
echo "✅ Other instances will see this on the board"
echo ""
echo "Run ./LOCAL_STATUS.sh to view the board"
echo ""
