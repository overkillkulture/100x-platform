#!/bin/bash

# REQUEST_ABILITY.sh - Request an ability from another computer in the network
# Part of the Overkore Network Public Ability License (ONPAL) framework

set -e

ABILITIES_DIR="ABILITIES"
GITHUB_REPO="overkillkulture/100x-platform"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}           🔍 NETWORK ABILITY REQUEST SYSTEM${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if ability name and computer ID provided
if [ $# -lt 2 ]; then
    echo -e "${RED}Usage: $0 <ability_name> <computer_id>${NC}"
    echo ""
    echo "Example: $0 \"Beta Testing Framework\" computer_3_DESKTOP-MSMCFH2"
    echo ""
    echo "Available computers:"
    ls -1 "$ABILITIES_DIR"/*.json 2>/dev/null | xargs -n 1 basename | sed 's/_abilities.json//' | sed 's/^/  - /'
    exit 1
fi

ABILITY_NAME="$1"
COMPUTER_ID="$2"
ABILITIES_FILE="$ABILITIES_DIR/${COMPUTER_ID}_abilities.json"

echo -e "${YELLOW}Ability Requested:${NC} $ABILITY_NAME"
echo -e "${YELLOW}From Computer:${NC} $COMPUTER_ID"
echo ""

# Check if computer exists
if [ ! -f "$ABILITIES_FILE" ]; then
    echo -e "${RED}❌ Computer not found: $COMPUTER_ID${NC}"
    echo ""
    echo "Available computers:"
    ls -1 "$ABILITIES_DIR"/*.json 2>/dev/null | xargs -n 1 basename | sed 's/_abilities.json//' | sed 's/^/  - /'
    exit 1
fi

# Check if ability is public
echo -e "${BLUE}📊 Checking ability availability...${NC}"
echo ""

# Extract public abilities from the JSON
PUBLIC_ABILITIES=$(grep -A 20 '"public_abilities"' "$ABILITIES_FILE" | grep -v '"public_abilities"' | grep '"' | sed 's/.*"//;s/".*//')

# Check if requested ability is in public list
IS_PUBLIC=0
while IFS= read -r ability; do
    if [[ "$ability" == *"$ABILITY_NAME"* ]]; then
        IS_PUBLIC=1
        break
    fi
done <<< "$PUBLIC_ABILITIES"

if [ $IS_PUBLIC -eq 1 ]; then
    echo -e "${GREEN}✅ Ability is PUBLIC - available for network use!${NC}"
    echo ""
    echo -e "${GREEN}📦 ABILITY DETAILS:${NC}"
    echo ""

    # Show computer info
    COMPUTER_NAME=$(grep '"computer_name"' "$ABILITIES_FILE" | sed 's/.*: "//;s/".*//')
    echo -e "${YELLOW}Computer:${NC} $COMPUTER_NAME ($COMPUTER_ID)"

    # Show what they can share
    echo ""
    echo -e "${GREEN}Public Abilities Available:${NC}"
    echo "$PUBLIC_ABILITIES" | sed 's/^/  ✓ /'

    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🎯 NEXT STEPS:${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "1. Review the ability documentation in the repository"
    echo "2. Check NETWORK_ABILITY_SHARING.md for usage terms (ONPAL)"
    echo "3. Integrate the ability into your instance"
    echo "4. Contribute improvements back to the network"
    echo ""
    echo -e "${YELLOW}📄 Documentation:${NC} Check repo for README or docs"
    echo -e "${YELLOW}📜 License:${NC} ONPAL - improvements must be shared back"
    echo -e "${YELLOW}🔗 Repository:${NC} https://github.com/$GITHUB_REPO"
    echo ""

else
    echo -e "${YELLOW}⚠️  Ability is PRIVATE - requires permission${NC}"
    echo ""
    echo "This ability is marked as private. You need to:"
    echo ""
    echo "1. Open a GitHub issue requesting access"
    echo "2. Explain your use case"
    echo "3. Propose value exchange (what you can offer)"
    echo "4. Wait for approval from computer owner"
    echo ""
    echo -e "${BLUE}Create request:${NC}"
    echo "  gh issue create --repo $GITHUB_REPO \\"
    echo "    --title \"Request: $ABILITY_NAME from $COMPUTER_ID\" \\"
    echo "    --body \"I would like to request access to '$ABILITY_NAME' from $COMPUTER_ID..."
    echo ""
fi

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
