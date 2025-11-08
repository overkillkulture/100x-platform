#!/bin/bash

# SHARE_ABILITY.sh - Share an ability with the network
# Part of the Overkore Network Public Ability License (ONPAL) framework

set -e

ABILITIES_DIR="ABILITIES"
PUBLIC_DIR="PUBLIC_ABILITIES"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}           📤 NETWORK ABILITY SHARING SYSTEM${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if ability name and privacy level provided
if [ $# -lt 2 ]; then
    echo -e "${RED}Usage: $0 <ability_path> <public|private>${NC}"
    echo ""
    echo "Examples:"
    echo "  $0 \"~/dev/Overkore_Deploy_Clean/overkore-ui/app/components/BetaNotice.tsx\" public"
    echo "  $0 \"~/Overcore/runtime/CENTRAL_AI_HUB.js\" private"
    echo ""
    exit 1
fi

ABILITY_PATH="$1"
PRIVACY_LEVEL="$2"

# Validate privacy level
if [[ "$PRIVACY_LEVEL" != "public" && "$PRIVACY_LEVEL" != "private" ]]; then
    echo -e "${RED}❌ Privacy level must be 'public' or 'private'${NC}"
    exit 1
fi

# Check if ability exists
if [ ! -e "$ABILITY_PATH" ]; then
    echo -e "${RED}❌ Ability not found: $ABILITY_PATH${NC}"
    exit 1
fi

ABILITY_NAME=$(basename "$ABILITY_PATH")
ABILITY_TYPE=$(echo "$ABILITY_PATH" | sed 's/.*\.//')

echo -e "${YELLOW}Ability:${NC} $ABILITY_NAME"
echo -e "${YELLOW}Type:${NC} $ABILITY_TYPE"
echo -e "${YELLOW}Privacy:${NC} $PRIVACY_LEVEL"
echo ""

if [ "$PRIVACY_LEVEL" == "public" ]; then
    # Share publicly
    echo -e "${BLUE}📦 Preparing ability for public sharing...${NC}"
    echo ""

    # Create public abilities directory if it doesn't exist
    mkdir -p "$PUBLIC_DIR"

    # Determine category based on path
    CATEGORY="general"
    if [[ "$ABILITY_PATH" == *"component"* ]]; then
        CATEGORY="ui-components"
    elif [[ "$ABILITY_PATH" == *"runtime"* ]]; then
        CATEGORY="runtime-systems"
    elif [[ "$ABILITY_PATH" == *"intelligence"* ]]; then
        CATEGORY="ai-systems"
    elif [[ "$ABILITY_PATH" == *"automation"* ]]; then
        CATEGORY="automation"
    fi

    TARGET_DIR="$PUBLIC_DIR/$CATEGORY"
    mkdir -p "$TARGET_DIR"

    # Copy ability to public directory
    if [ -d "$ABILITY_PATH" ]; then
        # It's a directory
        cp -r "$ABILITY_PATH" "$TARGET_DIR/"
        echo -e "${GREEN}✅ Directory copied to: $TARGET_DIR/$ABILITY_NAME${NC}"
    else
        # It's a file
        cp "$ABILITY_PATH" "$TARGET_DIR/"
        echo -e "${GREEN}✅ File copied to: $TARGET_DIR/$ABILITY_NAME${NC}"
    fi

    # Generate README for the ability
    README_PATH="$TARGET_DIR/${ABILITY_NAME%.${ABILITY_TYPE}}_README.md"

    cat > "$README_PATH" << EOF
# $ABILITY_NAME

**Category:** $CATEGORY
**Privacy:** PUBLIC
**License:** ONPAL (Overkore Network Public Ability License)

## Description

Shared ability from the Overkore Network.

## Usage

\`\`\`
# Copy this ability to your instance:
cp PUBLIC_ABILITIES/$CATEGORY/$ABILITY_NAME <your-destination>
\`\`\`

## Requirements

- Document any dependencies here
- List required packages or services
- Note any configuration needed

## Integration

1. Copy the file to your project
2. Install any dependencies
3. Configure as needed
4. Test the integration

## Improvements

If you improve this ability:
1. Test thoroughly
2. Document changes
3. Push improvements back to network
4. Update this README

## License

ONPAL - Overkore Network Public Ability License

✅ **Allowed:**
- Use in your own projects
- Modify and improve
- Share with other network members

❌ **Not Allowed:**
- Sell to non-network members without permission
- Remove attribution
- Close-source derived works

🔄 **Required:**
- Contribute improvements back to network
- Maintain attribution
- Share derivative works with network

---

*Shared: $(date +%Y-%m-%d)*
*Original Path: $ABILITY_PATH*
EOF

    echo -e "${GREEN}✅ README generated: $README_PATH${NC}"
    echo ""

    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🎯 NEXT STEPS:${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "1. Review the README and customize it"
    echo "2. Add ability documentation"
    echo "3. Update your abilities JSON to include this as public"
    echo "4. Commit and push to GitHub"
    echo ""
    echo -e "${YELLOW}Git commands:${NC}"
    echo "  git add $PUBLIC_DIR"
    echo "  git commit -m \"📤 Shared $ABILITY_NAME as public ability\""
    echo "  git push"
    echo ""

else
    # Private ability
    echo -e "${YELLOW}🔒 Ability marked as PRIVATE${NC}"
    echo ""
    echo "Private abilities are:"
    echo "  ✓ Listed in your abilities.json"
    echo "  ✓ NOT copied to PUBLIC_ABILITIES/"
    echo "  ✓ Require explicit permission to access"
    echo ""
    echo "To share privately:"
    echo "  1. Update your abilities.json to list it as private"
    echo "  2. Document access requirements"
    echo "  3. Respond to access requests on GitHub"
    echo ""
fi

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
