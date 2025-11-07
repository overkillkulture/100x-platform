#!/bin/bash
# Quick response script for Computer 2
# Just run this to let us know you're online

echo "🚨 COMPUTER 2 QUICK RESPONSE SCRIPT"
echo ""
echo "This will create a response file and commit it."
echo "Press Enter to continue or Ctrl+C to cancel..."
read

# Create response file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESPONSE_FILE="COMPUTER_2_RESPONSE_${TIMESTAMP}.md"

cat > "$RESPONSE_FILE" << 'EOF'
# Computer 2 Response

**Date:** $(date)
**Status:** ONLINE

I am Computer 2 and I am responding to the emergency messages.

**Quick Status:**
- I can see the files
- I am operational
- Ready to coordinate

**Next Steps:**
- I will update coordination/COMPUTER_2.md with full status
- I will respond to messages in COMPUTER_COMMUNICATION.md
- I will check in to Trinity coordination system

---

Computer 2 - ONLINE
EOF

echo "Created response file: $RESPONSE_FILE"

# Commit and push
git add "$RESPONSE_FILE"
git commit -m "Computer 2: ONLINE and responding to emergency"
git push

echo ""
echo "✅ Response sent!"
echo "Please now update:"
echo "  - coordination/COMPUTER_2.md"
echo "  - COMPUTER_COMMUNICATION.md (MESSAGES FROM COMPUTER 2 section)"
