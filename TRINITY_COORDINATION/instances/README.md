# 🤖 ACTIVE CLAUDE INSTANCES

This directory tracks all Claude instances currently working on the platform.

---

## 📋 CHECK-IN PROTOCOL

### When You Start a Session:

Create a file: `claude-[role]-[timestamp].txt`

**Format:**
```
ACTIVE - [Your role/purpose]
Started: [Timestamp UTC]
Role: [C1 Mechanic / C2 Architect / C3 Oracle / C4-C7 Specialist]
Status: [Current activity]
Branch: [Git branch you're working on]
Last Activity: [Timestamp UTC]
```

**Example:**
```bash
echo "ACTIVE - Building Module #21
Started: 2025-11-07 14:00 UTC
Role: C1 Mechanic
Status: In progress - social media module
Branch: claude/module-21-social-20251107
Last Activity: 2025-11-07 14:30 UTC" > claude-mechanic-20251107-1400.txt
```

---

## 🔄 UPDATE YOUR STATUS

Update your file whenever status changes:
```bash
echo "ACTIVE - Building Module #21
Started: 2025-11-07 14:00 UTC
Role: C1 Mechanic
Status: Testing complete, pushing to GitHub
Branch: claude/module-21-social-20251107
Last Activity: $(date -u +%Y-%m-%d\ %H:%M\ UTC)" > claude-mechanic-20251107-1400.txt

git add TRINITY_COORDINATION/instances/
git commit -m "Status update: Module #21 testing complete"
git push
```

---

## 🏁 WHEN YOU FINISH

Update your file to COMPLETE:
```bash
echo "COMPLETE - Module #21 Built Successfully
Started: 2025-11-07 14:00 UTC
Completed: 2025-11-07 16:30 UTC
Role: C1 Mechanic
Status: Module #21 complete, tested, committed
Branch: claude/module-21-social-20251107 (merged)
Result: 450 lines, all tests passing
Last Activity: $(date -u +%Y-%m-%d\ %H:%M\ UTC)" > claude-mechanic-20251107-1400.txt
```

---

## 📊 ACTIVE INSTANCES

Check who's currently working:
```bash
ls -la
cat *.txt
```

---

## 🤝 COORDINATION

If you see another instance working on similar task:
1. Read their status file
2. Check coordination_log.md
3. Coordinate in the log
4. Avoid conflicts

---

## 🗑️ CLEANUP

Completed sessions older than 7 days can be archived:
```bash
# Move old files to archive
mkdir -p ../archive/
mv *-202511*.txt ../archive/
```

---

## 📈 INSTANCE TRACKING

This directory helps us:
- See who's currently active
- Avoid duplicate work
- Coordinate tasks
- Track velocity
- Debug issues

---

**Current Active Instances:**

Check the `.txt` files in this directory for live status.

---

🤖 **Multi-instance coordination system** 🤖
