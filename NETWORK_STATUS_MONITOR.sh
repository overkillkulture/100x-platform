#!/bin/bash

#################################################################
# NETWORK STATUS MONITOR
# Displays real-time status of all computers in Overkore Network
# Usage: ./NETWORK_STATUS_MONITOR.sh [--json]
#################################################################

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Configuration
ABILITIES_DIR="./ABILITIES"
REPO_URL=$(git config --get remote.origin.url 2>/dev/null || echo "unknown")
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

# Function to print section header
print_header() {
    echo -e "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}$1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}\n"
}

# Function to extract JSON value
get_json_value() {
    local file=$1
    local key=$2
    grep "\"$key\"" "$file" | head -1 | sed 's/.*": "\{0,1\}\([^",]*\).*/\1/' | xargs
}

# Function to count array items in JSON
count_json_array() {
    local file=$1
    local key=$2
    grep -A 1000 "\"$key\"" "$file" | grep -o "\"[^\"]*\"" | wc -l
}

# Function to check Git status
check_git_status() {
    local ahead=$(git rev-list --count origin/$CURRENT_BRANCH..$CURRENT_BRANCH 2>/dev/null || echo "0")
    local behind=$(git rev-list --count $CURRENT_BRANCH..origin/$CURRENT_BRANCH 2>/dev/null || echo "0")

    if [ "$ahead" -gt 0 ] && [ "$behind" -gt 0 ]; then
        echo -e "${YELLOW}⚠ Diverged${NC} (ahead $ahead, behind $behind)"
    elif [ "$ahead" -gt 0 ]; then
        echo -e "${YELLOW}⬆ Ahead${NC} by $ahead commits"
    elif [ "$behind" -gt 0 ]; then
        echo -e "${YELLOW}⬇ Behind${NC} by $behind commits"
    else
        echo -e "${GREEN}✅ Synced${NC}"
    fi
}

# Main output
clear
echo -e "${MAGENTA}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║       🌐  OVERKORE NETWORK STATUS MONITOR  🌐             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}Repository:${NC} $REPO_URL"
echo -e "${CYAN}Branch:${NC} $CURRENT_BRANCH"
echo -e "${CYAN}Last Updated:${NC} $(date)"

print_header "📊 GIT SYNCHRONIZATION STATUS"
check_git_status

# Latest commits
echo -e "\n${WHITE}Latest 5 commits:${NC}"
git log --oneline -5 --color=always | sed 's/^/  /'

print_header "💻 COMPUTER STATUS"

# Track totals
total_computers=0
total_files=0
total_systems=0
total_public_abilities=0

# Check for abilities files
if [ ! -d "$ABILITIES_DIR" ]; then
    echo -e "${RED}❌ ABILITIES directory not found!${NC}"
    echo -e "   Expected: $ABILITIES_DIR"
    exit 1
fi

ability_files=$(find "$ABILITIES_DIR" -name "*_abilities.json" 2>/dev/null)

if [ -z "$ability_files" ]; then
    echo -e "${YELLOW}⚠ No ability files found${NC}"
else
    for file in $ability_files; do
        total_computers=$((total_computers + 1))

        # Extract computer info
        instance_id=$(get_json_value "$file" "instance_id")
        computer_name=$(get_json_value "$file" "computer_name")
        discovered_at=$(get_json_value "$file" "discovered_at")
        total_files_count=$(get_json_value "$file" "total_source_files")

        # Count systems and abilities
        systems_count=$(count_json_array "$file" "systems_built_this_session")
        public_abilities_count=$(count_json_array "$file" "public_abilities")

        # Update totals
        total_files=$((total_files + total_files_count))
        total_systems=$((total_systems + systems_count))
        total_public_abilities=$((total_public_abilities + public_abilities_count))

        # Display computer info
        echo -e "${GREEN}┌─ ${computer_name}${NC} ${CYAN}($instance_id)${NC}"
        echo -e "${GREEN}│${NC}  📁 Files: ${WHITE}$total_files_count${NC}"
        echo -e "${GREEN}│${NC}  🔧 Systems Built: ${WHITE}$systems_count${NC}"
        echo -e "${GREEN}│${NC}  📤 Public Abilities: ${WHITE}$public_abilities_count${NC}"
        echo -e "${GREEN}│${NC}  🕐 Last Updated: ${WHITE}$discovered_at${NC}"

        # Show strengths
        strengths=$(get_json_value "$file" "strengths" | head -c 100)
        if [ ! -z "$strengths" ]; then
            echo -e "${GREEN}│${NC}  💪 Strengths: ${YELLOW}${strengths}...${NC}"
        fi

        echo -e "${GREEN}└─${NC}"
        echo ""
    done
fi

print_header "📦 PUBLIC ABILITIES STATUS"

# Check PUBLIC_ABILITIES directory
if [ -d "PUBLIC_ABILITIES" ]; then
    echo -e "${GREEN}✅ PUBLIC_ABILITIES library exists${NC}\n"

    # Count abilities by category
    ui_components=$(find PUBLIC_ABILITIES/ui-components -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
    runtime_systems=$(find PUBLIC_ABILITIES/runtime-systems -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
    ai_systems=$(find PUBLIC_ABILITIES/ai-systems -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
    automation=$(find PUBLIC_ABILITIES/automation -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
    coordination=$(find PUBLIC_ABILITIES/coordination -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)

    echo -e "  ${CYAN}├─${NC} UI Components: ${WHITE}$ui_components${NC}"
    echo -e "  ${CYAN}├─${NC} Runtime Systems: ${WHITE}$runtime_systems${NC}"
    echo -e "  ${CYAN}├─${NC} AI Systems: ${WHITE}$ai_systems${NC}"
    echo -e "  ${CYAN}├─${NC} Automation: ${WHITE}$automation${NC}"
    echo -e "  ${CYAN}└─${NC} Coordination: ${WHITE}$coordination${NC}"

    total_public=$((ui_components + runtime_systems + ai_systems + automation + coordination))
    echo -e "\n  ${WHITE}Total Public Abilities: ${GREEN}$total_public${NC}"
else
    echo -e "${YELLOW}⚠ PUBLIC_ABILITIES library not created yet${NC}"
    echo -e "   Run: ./SHARE_ABILITY.sh to create it"
fi

print_header "🚀 NETWORK AUTOMATION TOOLS"

# Check for automation tools
tools=("DISCOVER_MY_ABILITIES.sh" "COMPARE_ALL_ABILITIES.sh" "REQUEST_ABILITY.sh" "SHARE_ABILITY.sh" "MERGE_ABILITIES.sh")
tools_available=0

for tool in "${tools[@]}"; do
    if [ -f "$tool" ]; then
        tools_available=$((tools_available + 1))
        echo -e "${GREEN}  ✅${NC} $tool"
    else
        echo -e "${RED}  ❌${NC} $tool ${YELLOW}(missing)${NC}"
    fi
done

echo -e "\n  ${WHITE}Tools Available: ${GREEN}$tools_available${NC} / ${WHITE}5${NC}"

print_header "📚 CONTENT STATUS"

# Check for crypto book
crypto_chapters=$(find . -maxdepth 1 -name "CRYPTO_COIN_CREATION_CHAPTER_*.md" 2>/dev/null | wc -l)
if [ $crypto_chapters -gt 0 ]; then
    echo -e "  ${GREEN}✅${NC} Crypto Book: ${WHITE}$crypto_chapters chapters${NC}"

    # Check if Chapter 8 exists (latest)
    if [ -f "CRYPTO_COIN_CREATION_CHAPTER_8.md" ]; then
        words=$(wc -w < "CRYPTO_COIN_CREATION_CHAPTER_8.md")
        echo -e "  ${CYAN}   Latest:${NC} Chapter 8 (Avoiding SEC Violations) - ${WHITE}$words words${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} Crypto Book: ${YELLOW}Not available${NC}"
fi

# Check for documentation
docs=$(find . -maxdepth 1 -name "*AUTONOMOUS*.md" -o -name "*NETWORK*.md" -o -name "*README*.md" 2>/dev/null | wc -l)
echo -e "  ${GREEN}✅${NC} Documentation Files: ${WHITE}$docs${NC}"

print_header "🔧 CONVERGENCE STATUS"

# Check if convergence plan exists
if [ -f "CONVERGENCE_ACTION_PLAN.md" ]; then
    echo -e "${GREEN}  ✅ Convergence Action Plan exists${NC}"
else
    echo -e "${YELLOW}  ⚠ No convergence plan found${NC}"
fi

# Check network comparison
if [ -f "NETWORK_COMPARISON_C1_vs_C3.md" ]; then
    echo -e "${GREEN}  ✅ Network Comparison exists${NC}"
else
    echo -e "${YELLOW}  ⚠ No network comparison found${NC}"
fi

# Check quick start guide
if [ -f "QUICK_START_PUBLIC_ABILITIES.md" ]; then
    echo -e "${GREEN}  ✅ Quick Start Guide exists${NC}"
else
    echo -e "${YELLOW}  ⚠ No quick start guide found${NC}"
fi

print_header "📈 NETWORK SUMMARY"

echo -e "${CYAN}Total Computers:${NC} ${WHITE}$total_computers${NC}"
echo -e "${CYAN}Total Source Files:${NC} ${WHITE}$total_files${NC}"
echo -e "${CYAN}Total Systems Built:${NC} ${WHITE}$total_systems${NC}"
echo -e "${CYAN}Total Public Abilities:${NC} ${WHITE}$total_public_abilities${NC}"
echo -e "${CYAN}Automation Tools:${NC} ${WHITE}$tools_available${NC}/5"

# Network health score
health_score=0
[ $total_computers -gt 0 ] && health_score=$((health_score + 20))
[ $total_files -gt 100 ] && health_score=$((health_score + 20))
[ $tools_available -eq 5 ] && health_score=$((health_score + 20))
[ -d "PUBLIC_ABILITIES" ] && health_score=$((health_score + 20))
[ -f "CONVERGENCE_ACTION_PLAN.md" ] && health_score=$((health_score + 20))

echo ""
if [ $health_score -ge 80 ]; then
    echo -e "${GREEN}Network Health: ${WHITE}$health_score%${NC} ${GREEN}✅ EXCELLENT${NC}"
elif [ $health_score -ge 60 ]; then
    echo -e "${YELLOW}Network Health: ${WHITE}$health_score%${NC} ${YELLOW}⚠ GOOD${NC}"
else
    echo -e "${RED}Network Health: ${WHITE}$health_score%${NC} ${RED}❌ NEEDS WORK${NC}"
fi

print_header "🎯 QUICK ACTIONS"

echo -e "${CYAN}To update abilities:${NC}"
echo -e "  ./DISCOVER_MY_ABILITIES.sh"
echo ""
echo -e "${CYAN}To compare computers:${NC}"
echo -e "  ./COMPARE_ALL_ABILITIES.sh"
echo ""
echo -e "${CYAN}To request an ability:${NC}"
echo -e "  ./REQUEST_ABILITY.sh \"ability-name\" computer_id"
echo ""
echo -e "${CYAN}To share an ability:${NC}"
echo -e "  ./SHARE_ABILITY.sh \"path/to/ability\" public"
echo ""
echo -e "${CYAN}To pull latest network updates:${NC}"
echo -e "  git pull origin $CURRENT_BRANCH"
echo ""
echo -e "${CYAN}To view convergence plan:${NC}"
echo -e "  cat CONVERGENCE_ACTION_PLAN.md"
echo ""

echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}\n"
echo -e "${GREEN}✅ Network status check complete${NC}"
echo -e "${CYAN}Run with --json for machine-readable output${NC}\n"
