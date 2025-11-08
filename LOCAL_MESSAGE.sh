#!/bin/bash
# SEND MESSAGE TO OTHER LOCAL INSTANCES

COORD_DIR="LOCAL_COORDINATION"
mkdir -p "$COORD_DIR"

echo "From which instance? (your instance number): "
read FROM_INST

echo "Message to all instances: "
read MESSAGE

echo "[$(date '+%H:%M:%S')] Instance $FROM_INST: $MESSAGE" >> "$COORD_DIR/messages.txt"

echo ""
echo "✅ Message sent to all local instances!"
echo "They'll see it when they run ./LOCAL_STATUS.sh"
echo ""
