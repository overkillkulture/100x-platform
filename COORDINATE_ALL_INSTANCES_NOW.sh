#!/bin/bash

# Quick coordination script for all 16 instances
# Run this to open coordination hub and see status

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║     🎯 COORDINATING ALL 16 CLAUDE INSTANCES                   ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check git status
echo "📊 Checking GitHub for instance activity..."
git fetch --all 2>&1 | grep -E "new branch|claude/" | head -10

BRANCH_COUNT=$(git branch -a | grep "claude/" | wc -l)
echo "✅ Found $BRANCH_COUNT active instance branches"
echo ""

# Show coordination URLs
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 COORDINATION HUBS:"
echo ""
echo "   PRIMARY: https://consciousnessrevolution.io/CENTRAL_HUB.html"
echo "   BACKUP:  file://$(pwd)/CENTRAL_HUB.html"
echo "   SIMPLE:  https://consciousnessrevolution.io/connect.html"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if browser available
if command -v firefox &> /dev/null; then
    echo "🌐 Opening CENTRAL_HUB.html in Firefox..."
    firefox CENTRAL_HUB.html &
elif command -v google-chrome &> /dev/null; then
    echo "🌐 Opening CENTRAL_HUB.html in Chrome..."
    google-chrome CENTRAL_HUB.html &
elif command -v chromium &> /dev/null; then
    echo "🌐 Opening CENTRAL_HUB.html in Chromium..."
    chromium CENTRAL_HUB.html &
elif command -v open &> /dev/null; then
    echo "🌐 Opening CENTRAL_HUB.html in default browser..."
    open CENTRAL_HUB.html
elif command -v xdg-open &> /dev/null; then
    echo "🌐 Opening CENTRAL_HUB.html in default browser..."
    xdg-open CENTRAL_HUB.html &
else
    echo "⚠️  No browser found. Open manually:"
    echo "    file://$(pwd)/CENTRAL_HUB.html"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 WHAT TO DO IN EACH CLAUDE WINDOW:"
echo ""
echo "   1. Open the URL above"
echo "   2. Select instance number (1-16)"
echo "   3. Say what you're working on"
echo "   4. Click 'CHECK IN NOW'"
echo "   5. See all other instances appear"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 TIP: Copy the URL to all 16 Claude windows"
echo "    Each instance takes 30 seconds to check in"
echo "    Total time: ~8 minutes for full coordination"
echo ""
echo "📊 Read: ALL_INSTANCE_ACTIVITY_REPORT.md for details"
echo ""
echo "✅ Coordination hub opened. Standing by..."
