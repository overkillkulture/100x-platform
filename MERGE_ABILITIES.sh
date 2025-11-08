#!/bin/bash

# MERGE_ABILITIES.sh - Merge abilities from multiple computers
# Part of the Overkore Network Public Ability License (ONPAL) framework

set -e

ABILITIES_DIR="ABILITIES"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}           🔄 NETWORK ABILITY MERGE SYSTEM${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if ability name provided
if [ $# -lt 1 ]; then
    echo -e "${RED}Usage: $0 <ability_name> [computer1] [computer2] ...${NC}"
    echo ""
    echo "Examples:"
    echo "  $0 \"Beta Testing Framework\"  # Shows all implementations"
    echo "  $0 \"Revenue Automation\" computer_1 computer_2  # Compare specific computers"
    echo ""
    exit 1
fi

ABILITY_NAME="$1"
shift  # Remove first argument, rest are computer IDs

echo -e "${YELLOW}Ability:${NC} $ABILITY_NAME"
echo ""

# If no specific computers provided, search all
if [ $# -eq 0 ]; then
    echo -e "${BLUE}🔍 Searching all computers for implementations...${NC}"
    echo ""

    FOUND_COUNT=0
    COMPUTERS_WITH_ABILITY=()

    # Search all abilities files
    for abilities_file in "$ABILITIES_DIR"/*.json; do
        if [ -f "$abilities_file" ]; then
            computer_id=$(basename "$abilities_file" .json | sed 's/_abilities//')

            # Search in public_abilities array
            if grep -q "\"$ABILITY_NAME\"" "$abilities_file"; then
                FOUND_COUNT=$((FOUND_COUNT + 1))
                COMPUTERS_WITH_ABILITY+=("$computer_id")

                computer_name=$(grep '"computer_name"' "$abilities_file" | sed 's/.*: "//;s/".*//')

                echo -e "${GREEN}✅ Found on: $computer_name ($computer_id)${NC}"

                # Check if public or private
                if grep -A 10 '"public_abilities"' "$abilities_file" | grep -q "$ABILITY_NAME"; then
                    echo -e "   ${GREEN}Status: PUBLIC${NC}"
                else
                    echo -e "   ${YELLOW}Status: PRIVATE${NC}"
                fi

                # Show version/details if available
                discovered_at=$(grep '"discovered_at"' "$abilities_file" | sed 's/.*: "//;s/".*//')
                echo -e "   Last Updated: $discovered_at"
                echo ""
            fi
        fi
    done

    if [ $FOUND_COUNT -eq 0 ]; then
        echo -e "${RED}❌ No computers found with '$ABILITY_NAME'${NC}"
        echo ""
        echo "Available abilities:"
        echo ""
        for abilities_file in "$ABILITIES_DIR"/*.json; do
            if [ -f "$abilities_file" ]; then
                computer_id=$(basename "$abilities_file" .json | sed 's/_abilities//')
                echo -e "${CYAN}$computer_id:${NC}"
                grep -A 20 '"public_abilities"' "$abilities_file" | grep '"' | grep -v 'public_abilities' | sed 's/.*"//;s/".*//' | sed 's/^/  ✓ /'
                echo ""
            fi
        done
        exit 1
    fi

    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}📊 MERGE DECISION MATRIX${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""

    echo -e "${YELLOW}Found $FOUND_COUNT implementation(s) of '$ABILITY_NAME'${NC}"
    echo ""

    if [ $FOUND_COUNT -eq 1 ]; then
        echo -e "${GREEN}✅ Only one implementation exists${NC}"
        echo -e "${GREEN}   → Use: ${COMPUTERS_WITH_ABILITY[0]}${NC}"
        echo ""
        echo "No merge needed - single source of truth"
    else
        echo -e "${YELLOW}⚠️  Multiple implementations detected${NC}"
        echo ""
        echo -e "${BLUE}RECOMMENDED MERGE STRATEGY:${NC}"
        echo ""
        echo "1. ${CYAN}COMPARE:${NC} Review each implementation"
        echo "   - Check feature completeness"
        echo "   - Compare code quality"
        echo "   - Evaluate documentation"
        echo ""
        echo "2. ${CYAN}DECIDE:${NC} Choose merge approach"
        echo "   a) Use best single implementation"
        echo "   b) Merge features from multiple"
        echo "   c) Keep both as variations"
        echo ""
        echo "3. ${CYAN}MERGE:${NC} Create canonical version"
        echo "   \$ git cherry-pick <commit-hash>  # For single impl"
        echo "   # OR manually merge best features"
        echo ""
        echo "4. ${CYAN}BROADCAST:${NC} Share with network"
        echo "   \$ git commit -m \"Merged $ABILITY_NAME - best of all implementations\""
        echo "   \$ git push"
        echo ""

        echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
        echo -e "${CYAN}🎯 DETAILED COMPARISON${NC}"
        echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
        echo ""

        for computer_id in "${COMPUTERS_WITH_ABILITY[@]}"; do
            abilities_file="$ABILITIES_DIR/${computer_id}_abilities.json"
            computer_name=$(grep '"computer_name"' "$abilities_file" | sed 's/.*: "//;s/".*//')

            echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
            echo -e "${CYAN}║ $computer_name ($computer_id)${NC}"
            echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"

            # Extract relevant stats
            total_files=$(grep '"total_source_files"' "$abilities_file" | grep -o '[0-9]*')
            discovered_at=$(grep '"discovered_at"' "$abilities_file" | sed 's/.*: "//;s/".*//')

            echo "Total Source Files: $total_files"
            echo "Last Updated: $discovered_at"

            # Show unique systems
            echo ""
            echo "Unique Systems:"
            grep '"unique_systems"' "$abilities_file" | sed 's/.*: "//;s/".*//' | tr ',' '\n' | sed 's/^/  ✓ /'

            echo ""
            echo ""
        done

        echo -e "${YELLOW}📋 Next: Manually review implementations and choose merge strategy${NC}"
    fi

else
    # Specific computers provided - compare them
    echo -e "${BLUE}🔍 Comparing implementations across specified computers...${NC}"
    echo ""

    for computer_id in "$@"; do
        abilities_file="$ABILITIES_DIR/${computer_id}_abilities.json"

        if [ ! -f "$abilities_file" ]; then
            echo -e "${RED}❌ Computer not found: $computer_id${NC}"
            continue
        fi

        computer_name=$(grep '"computer_name"' "$abilities_file" | sed 's/.*: "//;s/".*//')

        echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${CYAN}$computer_name ($computer_id)${NC}"
        echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"

        # Check if has ability
        if grep -q "$ABILITY_NAME" "$abilities_file"; then
            echo -e "${GREEN}✅ HAS '$ABILITY_NAME'${NC}"

            # Check privacy
            if grep -A 10 '"public_abilities"' "$abilities_file" | grep -q "$ABILITY_NAME"; then
                echo -e "   Status: ${GREEN}PUBLIC${NC}"
            else
                echo -e "   Status: ${YELLOW}PRIVATE${NC}"
            fi

        else
            echo -e "${RED}❌ MISSING '$ABILITY_NAME'${NC}"
        fi

        echo ""
    done
fi

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
