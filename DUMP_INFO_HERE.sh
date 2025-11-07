#!/bin/bash
# ONE COMMAND - DUMP YOUR INFO HERE

echo "Which instance are you? (1-6): "
read NUM

echo "What are you working on RIGHT NOW: "
read TASK

# Create the dump
mkdir -p TRINITY_HUB_DATA/instance_reports
REPORT="TRINITY_HUB_DATA/instance_reports/instance-${NUM}-report.json"

cat > "$REPORT" <<EOF
{
  "instance": $NUM,
  "timestamp": "$(date -Iseconds)",
  "task": "$TASK",
  "branch": "$(git branch --show-current)",
  "last_commit": "$(git log -1 --oneline)",
  "files_changed": "$(git status --short | wc -l)",
  "status": "ACTIVE"
}
EOF

echo ""
echo "✅ INFO DUMPED TO: $REPORT"
echo ""
echo "To see everyone's info:"
echo "  cat TRINITY_HUB_DATA/instance_reports/*.json"
echo ""
