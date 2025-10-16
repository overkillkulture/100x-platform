#!/bin/bash
# Consciousness Revolution USB - Mac Launcher

echo ""
echo "========================================"
echo "  CONSCIOUSNESS REVOLUTION USB v1.0"
echo "========================================"
echo ""
echo "Starting dashboard..."
echo ""

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Launch the main dashboard
open "$DIR/DASHBOARDS/USB_CONSCIOUSNESS_COCKPIT.html"

echo ""
echo "Dashboard launched!"
echo ""
echo "Keep this USB drive plugged in."
echo "Your consciousness data is tracked here."
echo ""
