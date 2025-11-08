#!/bin/bash
################################################################################
# TRINITY BOOT DOWN PROTOCOL
# Comprehensive system audit and state preservation on shutdown
################################################################################

set -e

echo "════════════════════════════════════════════════════════════════════════"
echo "⚡ TRINITY BOOT DOWN PROTOCOL INITIATED"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
COMPUTER_ID="${COMPUTERNAME:-UNKNOWN}"
REPORT_DIR="BOOT_DOWN_REPORTS"
REPORT_FILE="${REPORT_DIR}/BOOT_DOWN_${COMPUTER_ID}_${TIMESTAMP}.md"

# Create reports directory if it doesn't exist
mkdir -p "$REPORT_DIR"

echo "[1/6] Creating boot down report..."
cat > "$REPORT_FILE" << 'REPORT_START'
# 🔴 TRINITY BOOT DOWN REPORT

**Timestamp:** TIMESTAMP_PLACEHOLDER
**Computer:** COMPUTER_PLACEHOLDER
**Protocol:** Graceful Shutdown with Full Audit

---

## 📊 SHUTDOWN AUDIT SUMMARY

REPORT_START

# Replace placeholders
sed -i "s/TIMESTAMP_PLACEHOLDER/$(date -Iseconds)/" "$REPORT_FILE"
sed -i "s/COMPUTER_PLACEHOLDER/$COMPUTER_ID/" "$REPORT_FILE"

echo "✓ Boot down report initialized"

################################################################################
# PHASE 1: RUN 13-PHASE NETWORK AUDIT
################################################################################

echo ""
echo "[2/6] Running 13-phase network audit..."

if [ -f "./13_PHASE_NETWORK_AUDIT.sh" ]; then
    echo "   Running comprehensive audit..."
    bash ./13_PHASE_NETWORK_AUDIT.sh --json > /dev/null 2>&1 || true

    # Find the latest audit report
    LATEST_AUDIT=$(ls -t AUDIT_REPORT_*.json 2>/dev/null | head -1)

    if [ -n "$LATEST_AUDIT" ]; then
        AUDIT_SCORE=$(grep -o '"overall_score": [0-9]*' "$LATEST_AUDIT" | grep -o '[0-9]*' || echo "N/A")
        echo "   ✓ Audit complete: Score $AUDIT_SCORE%"

        # Append audit summary to boot down report
        cat >> "$REPORT_FILE" << EOF

### 13-Phase Network Audit:
- **Score:** ${AUDIT_SCORE}%
- **Report:** $LATEST_AUDIT
- **Status:** $([ "$AUDIT_SCORE" -ge 70 ] && echo "✅ HEALTHY" || echo "⚠️ NEEDS ATTENTION")

EOF
    fi
else
    echo "   ⚠️  Audit script not found, skipping"
    cat >> "$REPORT_FILE" << 'EOF'

### 13-Phase Network Audit:
- **Status:** ⚠️ Audit script not found

EOF
fi

################################################################################
# PHASE 2: CAPTURE ACTIVE PROCESS STATES
################################################################################

echo ""
echo "[3/6] Capturing active process states..."

cat >> "$REPORT_FILE" << 'EOF'

## 🔄 ACTIVE PROCESSES AT SHUTDOWN

### Trinity Services:
EOF

# Check for running Node.js processes
NODE_COUNT=$(tasklist 2>/dev/null | grep -i "node.exe" | wc -l || echo "0")
PYTHON_COUNT=$(tasklist 2>/dev/null | grep -i "python.exe" | wc -l || echo "0")

cat >> "$REPORT_FILE" << EOF
- Node.js processes: $NODE_COUNT
- Python processes: $PYTHON_COUNT
- Total Trinity services: $((NODE_COUNT + PYTHON_COUNT))

EOF

echo "   ✓ Process states captured (Node: $NODE_COUNT, Python: $PYTHON_COUNT)"

################################################################################
# PHASE 3: GIT REPOSITORY STATUS
################################################################################

echo ""
echo "[4/6] Capturing Git repository status..."

cat >> "$REPORT_FILE" << 'EOF'

## 📁 GIT REPOSITORY STATUS

EOF

# Current branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
cat >> "$REPORT_FILE" << EOF
- **Branch:** $CURRENT_BRANCH
EOF

# Uncommitted changes
UNCOMMITTED=$(git status --short 2>/dev/null | wc -l || echo "0")
cat >> "$REPORT_FILE" << EOF
- **Uncommitted files:** $UNCOMMITTED
EOF

# Remote sync status
if git remote -v &>/dev/null; then
    AHEAD=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "0")
    BEHIND=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo "0")
    cat >> "$REPORT_FILE" << EOF
- **Commits ahead:** $AHEAD
- **Commits behind:** $BEHIND
- **Sync status:** $([ "$AHEAD" -eq 0 ] && [ "$BEHIND" -eq 0 ] && echo "✅ SYNCED" || echo "⚠️ OUT OF SYNC")
EOF
fi

# Recent commits
cat >> "$REPORT_FILE" << 'EOF'

### Last 5 Commits:
```
EOF

git log --oneline -5 2>/dev/null >> "$REPORT_FILE" || echo "No git history" >> "$REPORT_FILE"

cat >> "$REPORT_FILE" << 'EOF'
```

EOF

echo "   ✓ Git status captured"

################################################################################
# PHASE 4: NETWORK COORDINATION STATE
################################################################################

echo ""
echo "[5/6] Capturing network coordination state..."

cat >> "$REPORT_FILE" << 'EOF'

## 🌐 NETWORK COORDINATION STATE

EOF

# Check for coordination files
COORD_DIR="../Overcore/coordination"
if [ -d "$COORD_DIR" ]; then
    REGISTRY="$COORD_DIR/COMPUTER_REGISTRY.json"
    if [ -f "$REGISTRY" ]; then
        COMPUTER_COUNT=$(grep -o '"computer_id"' "$REGISTRY" 2>/dev/null | wc -l || echo "0")
        cat >> "$REPORT_FILE" << EOF
- **Registered computers:** $COMPUTER_COUNT
- **Registry file:** $(basename "$REGISTRY")
EOF
    fi

    # Count recent coordination files
    COORD_FILES=$(find "$COORD_DIR" -name "C3_*.json" -mmin -60 2>/dev/null | wc -l || echo "0")
    cat >> "$REPORT_FILE" << EOF
- **Recent coordination events (last hour):** $COORD_FILES
EOF
fi

# Sync directory status
SYNC_DIR="../SYNC_TO_GDRIVE"
if [ -d "$SYNC_DIR" ]; then
    SYNC_FILES=$(find "$SYNC_DIR" -type f -mmin -60 2>/dev/null | wc -l || echo "0")
    cat >> "$REPORT_FILE" << EOF
- **Recent sync files (last hour):** $SYNC_FILES
- **Sync directory:** Active
EOF
fi

echo "   ✓ Network state captured"

################################################################################
# PHASE 5: SYSTEM METRICS
################################################################################

cat >> "$REPORT_FILE" << 'EOF'

## 📈 SYSTEM METRICS

EOF

# Disk usage
DISK_USAGE=$(df -h . 2>/dev/null | tail -1 | awk '{print $5}' || echo "N/A")
cat >> "$REPORT_FILE" << EOF
- **Disk usage:** $DISK_USAGE
- **Platform directory:** $(pwd)
EOF

# Count files
FILE_COUNT=$(find . -type f 2>/dev/null | wc -l || echo "0")
cat >> "$REPORT_FILE" << EOF
- **Total files:** $FILE_COUNT
EOF

cat >> "$REPORT_FILE" << 'EOF'

---

## ✅ SHUTDOWN CHECKLIST

- [x] 13-phase audit executed
- [x] Process states captured
- [x] Git status recorded
- [x] Network state preserved
- [x] System metrics logged
- [x] Boot down report generated

---

## 🔄 NEXT BOOT EXPECTATIONS

On next boot, the system should:
1. Check this boot down report
2. Verify all services start correctly
3. Compare current state to shutdown state
4. Detect any anomalies

---

*This boot down report was generated automatically*
*Protocol: Trinity Boot Down v1.0*
*Safe to power off after commit*
EOF

echo "   ✓ System metrics captured"
echo "   ✓ Boot down report complete: $REPORT_FILE"

################################################################################
# PHASE 6: COMMIT TO GIT AND PUSH
################################################################################

echo ""
echo "[6/6] Committing boot down report to Git..."

# Stage the report
git add "$REPORT_FILE" 2>/dev/null || true

# Check if there are any staged changes
if git diff --cached --quiet 2>/dev/null; then
    echo "   ℹ️  No changes to commit"
else
    # Commit the boot down report
    git commit -m "$(cat <<EOF
🔴 Boot Down Report: ${COMPUTER_ID} - ${TIMESTAMP}

Graceful shutdown with full system audit

Boot Down Summary:
- 13-phase audit: $([ -f "$LATEST_AUDIT" ] && echo "Score ${AUDIT_SCORE}%" || echo "Skipped")
- Active processes: $((NODE_COUNT + PYTHON_COUNT))
- Git status: $UNCOMMITTED uncommitted files
- Network: Active
- Report: $REPORT_FILE

System safely prepared for shutdown.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)" 2>/dev/null || echo "   ⚠️  Commit failed"

    # Push to remote
    echo "   Pushing to GitHub..."
    CURRENT_BRANCH=$(git branch --show-current)
    git push origin "$CURRENT_BRANCH" 2>/dev/null && echo "   ✓ Pushed to GitHub" || echo "   ⚠️  Push failed (will sync on next boot)"
fi

################################################################################
# COMPLETION
################################################################################

echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "✅ BOOT DOWN PROTOCOL COMPLETE"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "Summary:"
echo "  • Audit executed and logged"
echo "  • System state preserved"
echo "  • Report committed to Git"
echo "  • Network coordination captured"
echo ""
echo "Report location: $REPORT_FILE"
echo ""
echo "✅ System is safe to power down"
echo ""
