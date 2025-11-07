#!/bin/bash

# SYNC_TO_WINDOWS.sh
# Syncs the MASTER_DASHBOARD.html to Windows CENTRAL_COMMAND folder

SOURCE_DIR="/home/user/100x-platform/CENTRAL_COMMAND/live_status"
WINDOWS_DIR="C:/Users/Darrick/CENTRAL_COMMAND/live_status"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📂 SYNC TO WINDOWS - MASTER DASHBOARD"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Source: $SOURCE_DIR"
echo "Destination: $WINDOWS_DIR"
echo ""

# Check if running on WSL
if [ -d "/mnt/c" ]; then
    echo "✅ WSL detected"
    WINDOWS_DIR="/mnt/c/Users/Darrick/CENTRAL_COMMAND/live_status"

    # Create directory if it doesn't exist
    mkdir -p "$WINDOWS_DIR"

    # Copy files
    echo "📋 Copying files..."
    cp -v "$SOURCE_DIR/MASTER_DASHBOARD.html" "$WINDOWS_DIR/" 2>/dev/null
    cp -v "$SOURCE_DIR/master_status.json" "$WINDOWS_DIR/" 2>/dev/null

    echo ""
    echo "✅ Files synced to Windows!"
    echo "   Open: file:///$WINDOWS_DIR/MASTER_DASHBOARD.html"

elif command -v powershell.exe &> /dev/null; then
    echo "✅ PowerShell detected (WSL2)"

    # Use PowerShell to copy
    powershell.exe -Command "
        New-Item -ItemType Directory -Force -Path '$WINDOWS_DIR'
        Copy-Item -Path '$SOURCE_DIR/MASTER_DASHBOARD.html' -Destination '$WINDOWS_DIR/' -Force
        Copy-Item -Path '$SOURCE_DIR/master_status.json' -Destination '$WINDOWS_DIR/' -Force
    "

    echo ""
    echo "✅ Files synced to Windows!"

else
    echo "⚠️  Not running on WSL"
    echo ""
    echo "Manual sync required:"
    echo "1. Copy from: $SOURCE_DIR"
    echo "2. To: $WINDOWS_DIR"
    echo ""
    echo "Or use FileZilla/WinSCP/similar to transfer files"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
