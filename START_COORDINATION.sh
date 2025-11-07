#!/bin/bash

# START_COORDINATION.sh
# Launches the complete Trinity coordination system

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎛️  TRINITY COORDINATION SYSTEM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Starting multi-tier coordination:"
echo "  • 6 Local Instances"
echo "  • Local Instance Coordinator"
echo "  • Inter-Computer Synchronization"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd /home/user/100x-platform

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

# Check if required files exist
if [ ! -f "MASTER_COORDINATOR.py" ]; then
    echo "❌ MASTER_COORDINATOR.py not found!"
    exit 1
fi

if [ ! -f "LOCAL_INSTANCE_COORDINATOR.py" ]; then
    echo "❌ LOCAL_INSTANCE_COORDINATOR.py not found!"
    exit 1
fi

if [ ! -f "INTER_COMPUTER_SYNC.py" ]; then
    echo "❌ INTER_COMPUTER_SYNC.py not found!"
    exit 1
fi

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo "⚠️  Warning: Not in a git repository!"
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip3 install -q flask flask-cors requests 2>/dev/null || echo "⚠️  Flask/requests may not be installed"

echo ""
echo "🚀 Launching Master Coordinator..."
echo ""

# Run the master coordinator
python3 MASTER_COORDINATOR.py
