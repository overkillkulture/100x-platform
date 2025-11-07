#!/bin/bash

# START_CENTRAL_HUB.sh
# Starts the Central Command Hub (The Cyclotron)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ⚡ CENTRAL COMMAND HUB - THE CYCLOTRON"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "One Input → Many Instances → One Output"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd /home/user/100x-platform

# Check dependencies
echo "📦 Checking dependencies..."
pip3 install -q flask flask-socketio flask-cors python-socketio 2>/dev/null || echo "⚠️  Dependencies may not be installed"

echo ""
echo "🚀 Starting Central Command Hub..."
echo ""
echo "📊 Dashboard will be at:"
echo "   http://localhost:5555"
echo "   http://$(hostname -I | awk '{print $1}'):5555"
echo ""
echo "💡 All computers should connect to this hub"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 CENTRAL_COMMAND_HUB.py
