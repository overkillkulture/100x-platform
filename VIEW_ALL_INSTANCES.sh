#!/bin/bash
echo ""
echo "🎯 REGISTERED INSTANCES"
echo "======================="
echo ""

if [ ! -d "TRINITY_COORDINATION/active_instances" ]; then
  echo "⚠️  No instances registered yet!"
  exit 0
fi

COUNT=$(ls TRINITY_COORDINATION/active_instances/*.json 2>/dev/null | wc -l)
echo "Total: $COUNT/6 instances registered"
echo ""

for file in TRINITY_COORDINATION/active_instances/instance-*.json; do
  if [ -f "$file" ]; then
    NUM=$(grep -o '"instance_num": [0-9]*' "$file" | grep -o '[0-9]*')
    ROLE=$(grep -o '"role": "[^"]*"' "$file" | cut -d'"' -f4)
    TIME=$(grep -o '"registered_at": "[^"]*"' "$file" | cut -d'"' -f4)
    TASK=$(grep -o '"current_task": "[^"]*"' "$file" | cut -d'"' -f4)

    echo "🟢 Instance $NUM - $ROLE"
    echo "   Task: $TASK"
    echo "   Registered: $TIME"
    echo ""
  fi
done

if [ $COUNT -lt 6 ]; then
  echo "⏳ Waiting for:"
  for i in {1..6}; do
    if [ ! -f "TRINITY_COORDINATION/active_instances/instance-$i.json" ]; then
      case $i in
        1) echo "   - Instance 1 (C1-Mechanic)" ;;
        2) echo "   - Instance 2 (C2-Architect)" ;;
        3) echo "   - Instance 3 (C3-Oracle)" ;;
        4) echo "   - Instance 4 (C4-Specialist)" ;;
        5) echo "   - Instance 5 (C5-Specialist)" ;;
        6) echo "   - Instance 6 (C6-Specialist)" ;;
      esac
    fi
  done
  echo ""
fi
