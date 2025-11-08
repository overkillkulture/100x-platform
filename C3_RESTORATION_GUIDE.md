# 🔄 C3 Instance Restoration Guide

**Computer:** DESKTOP-MSMCFH2 (C3-Oracle)
**Purpose:** Restore all Trinity systems and abilities after computer breakdown/rebuild
**Last Update:** 2025-11-08

---

## ⚡ Quick Restore (TL;DR)

```bash
# 1. Clone repos
git clone https://github.com/overkillkulture/100x-platform.git
cd 100x-platform
git checkout claude/autonomous-contact-test-011CUtYhH6FjHJiY9ZgmCLtR

# 2. Install dependencies
cd ~/Overcore && npm install
cd ~/dev/Overkore_Deploy_Clean/overkore-ui && npm install

# 3. Start Trinity
cd ~/Overcore/coordination && node START_ALL_COORDINATION.js &
cd ~/dev/Overkore_Deploy_Clean/overkore-ui && npm run dev -- --port 3000 &

# 4. Verify
curl http://localhost:3999/health  # Central AI Hub
curl http://localhost:9999/health  # WebSocket Hub
curl http://localhost:3000         # UI Node 1
```

---

## 📋 Full Restoration Checklist

### **Phase 1: Repository Setup**

**Clone main repos:**
```bash
cd ~
git clone https://github.com/overkillkulture/100x-platform.git
git clone https://github.com/[your-org]/Overcore.git  # If separate
git clone https://github.com/[your-org]/Overkore_Deploy_Clean.git  # If separate
```

**Checkout correct branch:**
```bash
cd ~/100x-platform
git checkout claude/autonomous-contact-test-011CUtYhH6FjHJiY9ZgmCLtR
git pull origin claude/autonomous-contact-test-011CUtYhH6FjHJiY9ZgmCLtR
```

### **Phase 2: Dependencies**

**Node.js (required: v18+):**
```bash
node --version  # Should be v18 or higher
npm --version
```

**Install Overcore dependencies:**
```bash
cd ~/Overcore
npm install
# Key packages: ws, express, chokidar, node-fetch
```

**Install UI dependencies:**
```bash
cd ~/dev/Overkore_Deploy_Clean/overkore-ui
npm install
# Key packages: next@15.3.1, react, react-dom, typescript
```

**Python (optional, for learning engine):**
```bash
python --version  # Should be 3.8+
pip install scikit-learn numpy  # For learning_engine.py
```

### **Phase 3: Directory Structure**

**Required directories:**
```
~/Overcore/
├── coordination/
│   ├── START_ALL_COORDINATION.js
│   ├── COMPUTER_REGISTRY.json
│   ├── MASTER_STATE.json
│   └── heartbeat_status.json
├── runtime/
│   ├── CENTRAL_AI_HUB.js
│   ├── mesh_task_worker.js
│   ├── TRINITY_UNIFIED_DASHBOARD.js
│   └── wake_trinity.js
├── intelligence/
│   ├── SWARM_INTELLIGENCE.js
│   └── learning_engine.py
├── automation/
│   ├── SELF_HEALING_MONITOR.js
│   └── AUTO_PERFORMANCE_OPTIMIZER.js
├── ai/
│   ├── PREDICTIVE_TASK_MODEL.js
│   └── INTELLIGENT_TASK_ROUTER.js
└── logs/
    ├── coordination.json
    ├── heartbeat.log
    └── mesh_worker.log

~/dev/Overkore_Deploy_Clean/overkore-ui/
├── app/
│   ├── components/
│   │   ├── BetaNotice.tsx
│   │   ├── SymbolLegend.tsx
│   │   ├── BetaBadge.tsx
│   │   ├── ConsoleShell.tsx
│   │   └── ButtonPanel.tsx
│   ├── trinity-status/page.tsx
│   ├── trinity-control/page.tsx
│   ├── mesh-command/page.tsx
│   └── layout.tsx
├── BETA_SYSTEM_README.md
└── BETA_BADGE_EXPANSION_COMPLETE.md
```

### **Phase 4: Configuration Files**

**Create if missing:**

**~/Overcore/config/nodes.json:**
```json
{
  "nodes": [
    {"id": "node_1", "url": "http://localhost:3000", "role": "Primary"},
    {"id": "node_2", "url": "http://localhost:3001", "role": "Secondary"},
    {"id": "node_3", "url": "http://localhost:3002", "role": "Tertiary"}
  ]
}
```

**~/Overcore/coordination/COMPUTER_REGISTRY.json:**
```json
{
  "computers": [
    {
      "id": "C3-DESKTOP-MSMCFH2",
      "name": "Oracle",
      "ip": "localhost",
      "status": "online",
      "last_seen": "2025-11-08T15:00:00Z"
    }
  ]
}
```

### **Phase 5: Start Services**

**Terminal 1 - Coordination Hub:**
```bash
cd ~/Overcore/coordination
node START_ALL_COORDINATION.js
# Starts: WebSocket Hub (9999), Central AI Hub (3999), all background services
```

**Terminal 2 - UI Node 1:**
```bash
cd ~/dev/Overkore_Deploy_Clean/overkore-ui
npm run dev -- --port 3000
```

**Terminal 3 - UI Node 2:**
```bash
cd ~/dev/Overkore_Deploy_Clean/overkore-ui
npm run dev -- --port 3001
```

**Terminal 4 - UI Node 3:**
```bash
cd ~/dev/Overkore_Deploy_Clean/overkore-ui
npm run dev -- --port 3002
```

**Terminal 5 - Trinity Dashboard:**
```bash
cd ~/Overcore/runtime
node TRINITY_UNIFIED_DASHBOARD.js
# Dashboard available at http://localhost:4000
```

### **Phase 6: Verify All Systems**

**Check services:**
```bash
# Central AI Hub
curl http://localhost:3999/health

# WebSocket Hub
curl http://localhost:9999/health

# UI Nodes
curl http://localhost:3000
curl http://localhost:3001
curl http://localhost:3002

# Trinity Dashboard
curl http://localhost:4000
```

**Check processes:**
```bash
ps aux | grep node | grep -v grep
# Should see ~15 node processes

ps aux | grep python | grep -v grep
# Should see learning_engine.py
```

---

## 🎯 Critical Abilities to Restore

### **1. Trinity Mesh Network**
- ✅ 15 background services
- ✅ WebSocket coordination (port 9999)
- ✅ Central AI Hub (port 3999)
- ✅ 3 UI nodes (ports 3000-3002)
- ✅ Trinity Dashboard (port 4000)

### **2. Beta Testing Framework**
- ✅ BetaNotice component (global banner)
- ✅ SymbolLegend component (floating help)
- ✅ BetaBadge component (status indicators)
- ✅ 26 badges across 6 pages
- ✅ Complete documentation

### **3. AI Systems**
- ✅ Swarm Intelligence
- ✅ Self-Healing Monitors
- ✅ Predictive Task Models
- ✅ Intelligent Task Routing
- ✅ Learning Engine

### **4. Coordination Systems**
- ✅ Google Drive sync (if configured)
- ✅ Heartbeat monitoring
- ✅ Mesh discovery
- ✅ Distributed logging

---

## 🔧 Troubleshooting

### **Services Won't Start**

**Check ports in use:**
```bash
netstat -an | grep -E "3999|9999|3000|3001|3002|4000"
```

**Kill conflicting processes:**
```bash
lsof -ti:3999 | xargs kill -9
lsof -ti:9999 | xargs kill -9
```

### **Dependencies Missing**

```bash
cd ~/Overcore && npm install
cd ~/dev/Overkore_Deploy_Clean/overkore-ui && npm install
```

### **Files Missing**

```bash
cd ~/100x-platform
git pull
# Check ABILITIES/ folder for your abilities.json
# Check for beta documentation
```

---

## 📦 Backup Critical Files

**Before breakdown, backup:**
```bash
# Abilities inventory
~/100x-platform/ABILITIES/computer_3_DESKTOP-MSMCFH2_abilities.json

# Beta system docs
~/100x-platform/BETA_SYSTEM_README.md
~/100x-platform/BETA_BADGE_EXPANSION_COMPLETE.md

# Configuration
~/Overcore/config/
~/Overcore/coordination/*.json

# Logs (optional, for debugging)
~/Overcore/logs/
```

**Backup command:**
```bash
tar -czf c3-backup-$(date +%Y%m%d).tar.gz \
  ~/100x-platform/ABILITIES/ \
  ~/100x-platform/BETA_*.md \
  ~/Overcore/config/ \
  ~/Overcore/coordination/*.json
```

---

## 🚀 Post-Restoration Tasks

1. **Verify abilities:**
   ```bash
   cd ~/100x-platform
   cat ABILITIES/computer_3_DESKTOP-MSMCFH2_abilities.json
   ```

2. **Check GitHub sync:**
   ```bash
   git status
   git pull
   ```

3. **Test all services:**
   - Open http://localhost:3000 (should show Beta banner)
   - Click "?" button (should show symbol legend)
   - Check http://localhost:4000 (Trinity dashboard)
   - Verify all badges display correctly

4. **Re-run abilities discovery:**
   ```bash
   cd ~/100x-platform
   ./DISCOVER_MY_ABILITIES.sh
   # Verify all systems still present
   ```

---

## 🌐 Network Integration

After restoration:

1. **Pull latest from network:**
   ```bash
   cd ~/100x-platform
   git pull
   ./COMPARE_ALL_ABILITIES.sh
   ```

2. **Check for new abilities from other instances:**
   - Review ABILITIES/ folder
   - See what Computer 1 has that you want
   - Merge valuable abilities

3. **Share your restored systems:**
   - Push any improvements made during restoration
   - Update abilities.json if capabilities changed

---

## 📞 Emergency Contacts

**If restoration fails:**
1. Check 100x-platform GitHub for latest code
2. Review Computer 1's abilities (has deployment automation)
3. Ask network for help (create GitHub issue)
4. Fall back to manual setup using this guide

---

**Status:** Ready for restoration
**Last Verified:** 2025-11-08
**Created By:** C3-Oracle autonomous session

*This guide ensures C3's unique Trinity infrastructure and Beta framework survive any computer breakdown and can be restored from scratch.*
