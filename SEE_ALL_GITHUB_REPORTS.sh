#!/bin/bash
# SEE ALL REPORTS FROM ALL COMPUTERS ON GITHUB

echo "=========================================="
echo "PULLING LATEST FROM GITHUB..."
echo "=========================================="
echo ""

git pull origin claude/autonomous-contact-test-011CUtYhH6FjHJiY9ZgmCLtR

echo ""
echo "=========================================="
echo "ALL COMPUTER REPORTS"
echo "=========================================="
echo ""

if [ ! -d "GITHUB_REPORTS" ]; then
  echo "❌ No reports yet. Be the first!"
  echo "   Run: ./REPORT_TO_GITHUB.sh"
  exit 1
fi

COUNT=$(ls GITHUB_REPORTS/*.md 2>/dev/null | wc -l)
echo "📊 Total Reports: $COUNT"
echo ""

# Show all reports
for report in GITHUB_REPORTS/*.md; do
  if [ -f "$report" ]; then
    echo "┌─────────────────────────────────────────"
    echo "│ $(basename $report)"
    echo "├─────────────────────────────────────────"
    head -20 "$report"
    echo "│"
    echo "│ [See full report: $report]"
    echo "└─────────────────────────────────────────"
    echo ""
  fi
done

echo "=========================================="
echo "To send YOUR report: ./REPORT_TO_GITHUB.sh"
echo "=========================================="
echo ""
