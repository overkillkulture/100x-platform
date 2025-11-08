#!/bin/bash
# Abilities Discovery Script
# Inventories what THIS instance can do

echo "═══════════════════════════════════════════════════════════════"
echo "  🔍 ABILITIES DISCOVERY - What Can This Instance Do?"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Create abilities directory
mkdir -p ABILITIES

# Get instance ID
read -p "Instance ID (e.g., computer_1, bozeman, rog, mobile): " INSTANCE_ID
echo ""

# Discover abilities
echo "Scanning this instance..."
echo ""

# Create abilities file
ABILITIES_FILE="ABILITIES/${INSTANCE_ID}_abilities.json"

# Count files
HTML_COUNT=$(find . -name "*.html" 2>/dev/null | wc -l)
PY_COUNT=$(find . -name "*.py" 2>/dev/null | wc -l)
JS_COUNT=$(find . -name "*.js" 2>/dev/null | wc -l)

echo "Found:"
echo "  - $HTML_COUNT HTML files"
echo "  - $PY_COUNT Python files"
echo "  - $JS_COUNT JavaScript files"
echo ""

# Ask specific questions
echo "CUSTOM ABILITIES:"
echo ""

read -p "1. What unique systems exist here? (e.g., Legal Arsenal, Voice System): " UNIQUE_SYSTEMS
echo ""

read -p "2. What's deployed/running? (e.g., Netlify functions, Railway services): " DEPLOYED
echo ""

read -p "3. What APIs are configured? (e.g., Stripe, Airtable, Instagram): " APIS
echo ""

read -p "4. What's the codebase version/fork? (e.g., main, trinity-branch, custom): " VERSION
echo ""

read -p "5. What works REALLY WELL here? (e.g., automation, specific features): " STRENGTHS
echo ""

read -p "6. What's broken or needs work? (e.g., bugs, incomplete features): " NEEDS_WORK
echo ""

# Create JSON
cat > "$ABILITIES_FILE" << EOF
{
  "instance_id": "$INSTANCE_ID",
  "discovered_at": "$(date -Iseconds)",
  "files": {
    "html": $HTML_COUNT,
    "python": $PY_COUNT,
    "javascript": $JS_COUNT
  },
  "unique_systems": "$UNIQUE_SYSTEMS",
  "deployed": "$DEPLOYED",
  "apis_configured": "$APIS",
  "codebase_version": "$VERSION",
  "strengths": "$STRENGTHS",
  "needs_work": "$NEEDS_WORK",
  "directory_size": "$(du -sh . 2>/dev/null | cut -f1)"
}
EOF

echo ""
echo "✅ Abilities discovered and saved to: $ABILITIES_FILE"
echo ""

# Show what was saved
echo "Summary:"
cat "$ABILITIES_FILE"
echo ""

# Offer to push
read -p "Push to GitHub so others can see? (y/n): " PUSH
if [ "$PUSH" = "y" ]; then
    git add ABILITIES/
    git commit -m "📊 Abilities discovery: $INSTANCE_ID"
    git push
    echo "✅ Pushed to GitHub"
else
    echo "Not pushed. Run 'git add ABILITIES/ && git commit && git push' when ready."
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Next: Run ./COMPARE_ALL_ABILITIES.sh to see everyone's abilities"
echo "═══════════════════════════════════════════════════════════════"
