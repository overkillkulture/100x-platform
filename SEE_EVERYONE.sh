#!/bin/bash
# SEE EVERYONE'S INFO

echo ""
echo "======================================"
echo "ALL INSTANCES - CURRENT STATUS"
echo "======================================"
echo ""

if [ ! -d "TRINITY_HUB_DATA/instance_reports" ]; then
  echo "❌ No reports yet. Run ./DUMP_INFO_HERE.sh first"
  exit 1
fi

COUNT=$(ls TRINITY_HUB_DATA/instance_reports/*.json 2>/dev/null | wc -l)
echo "Total Active: $COUNT/6 instances"
echo ""

for file in TRINITY_HUB_DATA/instance_reports/*.json; do
  if [ -f "$file" ]; then
    echo "----------------------------------------"
    python3 -m json.tool "$file" 2>/dev/null || cat "$file"
    echo ""
  fi
done

echo "======================================"
echo "To add your info: ./DUMP_INFO_HERE.sh"
echo "======================================"
echo ""
