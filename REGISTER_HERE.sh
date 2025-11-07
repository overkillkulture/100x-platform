#!/bin/bash
# SUPER SIMPLE FILE-BASED REGISTRATION
# Each instance just runs this script!

echo ""
echo "🚀 INSTANCE REGISTRATION"
echo "========================"
echo ""
echo "Which instance are you?"
echo "1) Instance 1 - C1-Mechanic"
echo "2) Instance 2 - C2-Architect"
echo "3) Instance 3 - C3-Oracle"
echo "4) Instance 4 - C4-Specialist"
echo "5) Instance 5 - C5-Specialist"
echo "6) Instance 6 - C6-Specialist"
echo ""
read -p "Enter number (1-6): " NUM

case $NUM in
  1) ROLE="C1-Mechanic" ;;
  2) ROLE="C2-Architect" ;;
  3) ROLE="C3-Oracle" ;;
  4) ROLE="C4-Specialist" ;;
  5) ROLE="C5-Specialist" ;;
  6) ROLE="C6-Specialist" ;;
  *) echo "Invalid number!"; exit 1 ;;
esac

# Create registration file
mkdir -p TRINITY_COORDINATION/active_instances
FILE="TRINITY_COORDINATION/active_instances/instance-${NUM}.json"

cat > "$FILE" <<EOF
{
  "instance_num": $NUM,
  "role": "$ROLE",
  "status": "ONLINE",
  "registered_at": "$(date -Iseconds)",
  "current_task": "Available",
  "pid": $$
}
EOF

echo ""
echo "✅ REGISTERED as $ROLE!"
echo ""
echo "Your info saved to: $FILE"
echo ""
echo "To see all instances, run:"
echo "  cat TRINITY_COORDINATION/active_instances/*.json"
echo ""
