#!/bin/bash
# Compare All Abilities
# Shows what each instance can do and highlights differences

echo "═══════════════════════════════════════════════════════════════"
echo "  🔄 ABILITIES COMPARISON - Level Out All Instances"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Pull latest
echo "Pulling latest abilities from GitHub..."
git pull
echo ""

# Check if abilities exist
if [ ! -d "ABILITIES" ] || [ -z "$(ls -A ABILITIES 2>/dev/null)" ]; then
    echo "❌ No abilities found yet."
    echo ""
    echo "Run ./DISCOVER_MY_ABILITIES.sh on each instance first."
    exit 1
fi

# Count instances
INSTANCE_COUNT=$(ls ABILITIES/*.json 2>/dev/null | wc -l)
echo "Found $INSTANCE_COUNT instances with abilities:"
echo ""

# Show each instance
for file in ABILITIES/*.json; do
    if [ -f "$file" ]; then
        INSTANCE=$(basename "$file" _abilities.json)
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "  Instance: $INSTANCE"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        # Extract key info using jq if available, otherwise use grep
        if command -v jq &> /dev/null; then
            echo "Unique Systems: $(jq -r '.unique_systems' "$file")"
            echo "Deployed: $(jq -r '.deployed' "$file")"
            echo "APIs: $(jq -r '.apis_configured' "$file")"
            echo "Version: $(jq -r '.codebase_version' "$file")"
            echo "Strengths: $(jq -r '.strengths' "$file")"
            echo "Files: $(jq -r '.files.html' "$file") HTML, $(jq -r '.files.python' "$file") Python, $(jq -r '.files.javascript' "$file") JS"
        else
            # Fallback without jq
            cat "$file"
        fi
        echo ""
    fi
done

echo "═══════════════════════════════════════════════════════════════"
echo "  🎯 NEXT STEPS"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "1. IDENTIFY UNIQUE ABILITIES:"
echo "   - What exists on one instance but not others?"
echo "   - Which version is most complete?"
echo ""
echo "2. OPEN LIVE SYNC CHAT:"
echo "   https://conciousnessrevolution.io/live-sync-chat.html"
echo "   - Discuss which abilities to merge"
echo "   - Decide canonical version"
echo ""
echo "3. MERGE PROCESS:"
echo "   - Choose base instance (probably most complete)"
echo "   - Copy unique abilities from other instances"
echo "   - Test merged version"
echo "   - Push to main branch"
echo "   - All instances pull merged version"
echo ""
echo "4. VERIFY:"
echo "   - All instances now have ALL abilities"
echo "   - Nothing lost in merge"
echo "   - Everyone on same version"
echo ""
echo "═══════════════════════════════════════════════════════════════"
