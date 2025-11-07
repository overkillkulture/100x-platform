#!/bin/bash

# Quick script to open CENTRAL_HUB.html in a browser
# Works on all 3 computers

echo "🎯 Opening CENTRAL_HUB.html..."

# Try to open in available browser
if command -v firefox &> /dev/null; then
    firefox CENTRAL_HUB.html &
    echo "✅ Opened in Firefox"
elif command -v google-chrome &> /dev/null; then
    google-chrome CENTRAL_HUB.html &
    echo "✅ Opened in Chrome"
elif command -v chromium &> /dev/null; then
    chromium CENTRAL_HUB.html &
    echo "✅ Opened in Chromium"
elif command -v open &> /dev/null; then
    open CENTRAL_HUB.html
    echo "✅ Opened in default browser (Mac)"
elif command -v xdg-open &> /dev/null; then
    xdg-open CENTRAL_HUB.html &
    echo "✅ Opened in default browser (Linux)"
else
    echo "❌ No browser found"
    echo "Manual: Open file:///home/user/100x-platform/CENTRAL_HUB.html"
fi

echo ""
echo "📍 Local path: file://$(pwd)/CENTRAL_HUB.html"
echo ""
echo "💡 If you see this dashboard:"
echo "   1. Pick your instance number (1-16)"
echo "   2. Say what you're working on"
echo "   3. Click CHECK IN NOW"
echo ""
echo "🔄 The dashboard auto-refreshes every 5 seconds"
echo "   All instances on this computer will see each other instantly!"
