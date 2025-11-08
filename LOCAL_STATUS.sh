#!/bin/bash
# SHOW LOCAL COORDINATION STATUS
# Real-time view of all instances on this computer

COORD_DIR="LOCAL_COORDINATION"
mkdir -p "$COORD_DIR"

clear
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║           LOCAL INSTANCE COORDINATION - THIS COMPUTER                ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🖥️  COMPUTER: $(hostname)"
echo "⏰  TIME: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "──────────────────────────────────────────────────────────────────────"
echo "ACTIVE INSTANCES:"
echo "──────────────────────────────────────────────────────────────────────"

# Count instances
INSTANCE_COUNT=$(ls $COORD_DIR/instance_*.txt 2>/dev/null | wc -l)
if [ $INSTANCE_COUNT -eq 0 ]; then
  echo ""
  echo "  ⚠️  No instances checked in yet"
  echo "  Run: ./LOCAL_CHECKIN.sh"
  echo ""
else
  echo ""
  for instance_file in $COORD_DIR/instance_*.txt; do
    if [ -f "$instance_file" ]; then
      INST=$(grep "INSTANCE:" "$instance_file" | cut -d' ' -f2-)
      ROLE=$(grep "ROLE:" "$instance_file" | cut -d' ' -f2-)
      TASK=$(grep "TASK:" "$instance_file" | cut -d' ' -f2-)
      TIME=$(grep "CHECKED_IN:" "$instance_file" | cut -d' ' -f2-)

      echo "  🟢 Instance $INST - $ROLE"
      echo "     Task: $TASK"
      echo "     Last seen: $TIME"
      echo ""
    fi
  done
fi

echo "──────────────────────────────────────────────────────────────────────"
echo "TASKS CLAIMED:"
echo "──────────────────────────────────────────────────────────────────────"

if [ -f "$COORD_DIR/claimed_tasks.txt" ]; then
  cat "$COORD_DIR/claimed_tasks.txt"
else
  echo ""
  echo "  No tasks claimed yet"
  echo ""
fi

echo "──────────────────────────────────────────────────────────────────────"
echo "MESSAGES:"
echo "──────────────────────────────────────────────────────────────────────"

if [ -f "$COORD_DIR/messages.txt" ]; then
  tail -10 "$COORD_DIR/messages.txt"
else
  echo ""
  echo "  No messages yet"
  echo ""
fi

echo "──────────────────────────────────────────────────────────────────────"
echo ""
echo "Total instances: $INSTANCE_COUNT"
echo ""
echo "Commands:"
echo "  ./LOCAL_CHECKIN.sh       - Check in to the board"
echo "  ./LOCAL_MESSAGE.sh       - Send a message to other instances"
echo "  ./LOCAL_CLAIM_TASK.sh    - Claim a task"
echo "  ./LOCAL_STATUS.sh        - Refresh this view"
echo ""
