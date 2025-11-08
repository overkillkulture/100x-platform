#!/bin/bash
# CHECK IN TO LOCAL COORDINATION BOARD
# Each instance runs this to register on the local board

COORD_DIR="LOCAL_COORDINATION"
mkdir -p "$COORD_DIR"

echo "═══════════════════════════════════════"
echo "LOCAL INSTANCE CHECK-IN"
echo "═══════════════════════════════════════"
echo ""
echo "Which instance are you? (1, 2, 3, etc.): "
read INSTANCE_NUM

echo "What's your role/name?: "
read ROLE

echo "What are you working on right now?: "
read TASK

# Create instance file
INSTANCE_FILE="$COORD_DIR/instance_${INSTANCE_NUM}.txt"
cat > "$INSTANCE_FILE" <<EOF
INSTANCE: $INSTANCE_NUM
ROLE: $ROLE
TASK: $TASK
STATUS: ACTIVE
CHECKED_IN: $(date '+%Y-%m-%d %H:%M:%S')
PID: $$
EOF

echo ""
echo "✅ Checked in as Instance $INSTANCE_NUM"
echo ""
echo "To see all instances: ./VIEW_LOCAL_BOARD.sh"
echo "To send a message: ./LOCAL_MESSAGE.sh"
echo "To claim a task: ./LOCAL_CLAIM_TASK.sh"
echo ""
