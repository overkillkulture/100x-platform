# Trinity Coordination System

**Purpose:** Multi-instance coordination for up to 21 simultaneous Claude instances (7 per computer × 3 computers)

---

## Directory Structure

```
TRINITY_COORDINATION/
├── README.md (this file)
├── instances/
│   ├── TEMPLATE.md (template for new instances)
│   ├── INSTANCE_1.md (active instances check in here)
│   ├── INSTANCE_2.md
│   └── ... (up to INSTANCE_21.md)
└── messages/
    ├── INSTANCE_1_TO_2.md
    ├── INSTANCE_2_TO_1.md
    └── ... (instance-to-instance messages)
```

---

## Quick Start

### For New Instances

1. **Read the main coordination file first:**
   ```bash
   cat 🚨_ALL_CLAUDE_INSTANCES_READ_THIS_NOW.md
   ```

2. **Check existing instances:**
   ```bash
   ls TRINITY_COORDINATION/instances/
   ```

3. **Create your instance file:**
   ```bash
   cp TRINITY_COORDINATION/instances/TEMPLATE.md TRINITY_COORDINATION/instances/INSTANCE_[N].md
   # Edit with your info
   ```

4. **Update your status regularly:**
   - Every hour during active work
   - Before starting new major tasks
   - After completing work
   - When encountering blockers

5. **Send messages to other instances:**
   ```bash
   # Create message file
   touch TRINITY_COORDINATION/messages/INSTANCE_[FROM]_TO_[TO].md
   ```

---

## Instance Numbering

**Computer 1 (Bozeman Primary):** Instances 1-7
**Computer 2 (Secondary):** Instances 8-14
**Computer 3 (Future):** Instances 15-21

### Current Active Instances

- **Instance 1:** Autonomous Contact Test (Session 011CUtYha8BCasLQ7jC7wTdC)
- **Instances 2-21:** Available

---

## Communication Protocols

### 1. Instance Status Files
**Location:** `TRINITY_COORDINATION/instances/INSTANCE_[N].md`
**Purpose:** Track what each instance is doing
**Update Frequency:** Hourly or when status changes

### 2. Instance Messages
**Location:** `TRINITY_COORDINATION/messages/`
**Format:** `INSTANCE_[FROM]_TO_[TO].md`
**Purpose:** Direct communication between instances
**When to Use:** Coordination, handoffs, questions

### 3. Inter-Computer Messages
**Location:** `COMPUTER_COMMUNICATION.md` (root)
**Purpose:** Computer-to-computer asynchronous messaging
**When to Use:** Cross-computer coordination

---

## Rules of Engagement

### Rule 1: Check Before You Start
Always check other instance status files before beginning work to avoid conflicts.

### Rule 2: Claim Your Work
Update your instance file immediately when starting a new task.

### Rule 3: Update Regularly
Don't go silent - update your status at least every hour.

### Rule 4: Coordinate Major Changes
Before making significant system changes, check with other instances.

### Rule 5: Clean Up After Yourself
When done, update your status to COMPLETED and document handoff info.

---

## Best Practices

### File Editing Coordination
```
# In your instance file, always list files you're editing:
Files Being Modified:
- path/to/file1.js
- path/to/file2.html
```

### Avoiding Conflicts
1. Check other instances' "Files Being Modified" sections
2. If someone else is editing the same file, coordinate via messages
3. Use different branches when possible
4. Commit and push frequently

### Resource Management
- Monitor API usage across instances
- Coordinate resource-intensive operations
- Share database/server ports to avoid conflicts
- Document what services you're running

---

## Message Templates

### Requesting Coordination
```markdown
# Instance [FROM] to Instance [TO]

**Priority:** NORMAL / HIGH / URGENT
**Subject:** [Brief description]

**Context:**
[What are you working on?]

**Request:**
[What do you need from the other instance?]

**Timeline:**
[When do you need it?]

**Files Involved:**
- file1.js
- file2.html
```

### Handoff Message
```markdown
# Handoff: Instance [FROM] to Instance [TO]

**Task:** [What task is being handed off]
**Status:** [Current status]

**Completed:**
- [x] Step 1
- [x] Step 2

**Pending:**
- [ ] Step 3
- [ ] Step 4

**Blockers:**
[Any issues encountered]

**Next Steps:**
[What the receiving instance should do]

**Files:**
[List of relevant files]
```

---

## Emergency Protocols

### Instance Crash / Failure
1. Create `EMERGENCY_INSTANCE_[N]_FAILURE.md` in root
2. Document what happened
3. Update instance status to "FAILED"
4. Another instance should claim the work

### Critical Blocker
1. Update your instance status to "BLOCKED"
2. Create message to all instances explaining blocker
3. Wait for coordination before proceeding

### Resource Exhaustion
1. Check all instance files for resource usage
2. Coordinate to pause non-critical work
3. Prioritize essential tasks
4. Document resolution

---

## Monitoring Dashboard

### Check System Health
```bash
# See all active instances
grep -r "Status: ACTIVE" TRINITY_COORDINATION/instances/

# See all blocked instances
grep -r "Status: BLOCKED" TRINITY_COORDINATION/instances/

# Check recent updates
ls -lt TRINITY_COORDINATION/instances/

# Read all current tasks
grep -r "Working On:" TRINITY_COORDINATION/instances/
```

---

## Success Metrics

**Good Coordination:**
- ✅ All instances updating status regularly
- ✅ No file conflicts
- ✅ Clear communication
- ✅ Efficient resource usage
- ✅ Tasks completing successfully

**Warning Signs:**
- ⚠️ Instance hasn't updated in >2 hours
- ⚠️ Multiple instances editing same files
- ⚠️ Repeated merge conflicts
- ⚠️ API quota nearing limits
- ⚠️ Services competing for same ports

---

## Integration with Existing Systems

### Old Coordination System (October 2025)
- Located in: `coordination/`
- Maintained for reference
- New system uses: `TRINITY_COORDINATION/`

### Computer Communication
- Located in: `COMPUTER_COMMUNICATION.md`
- For cross-computer async messaging
- Complements instance coordination

### Autonomous Systems
- Ability Acquisition: Port 6000
- KORPAK Engine: Port 5006
- Araya Chat: Netlify functions
- Document port/resource usage in instance files

---

## Version History

**v1.0 - November 7, 2025**
- Initial Trinity coordination framework
- Created by Instance 1 (Autonomous Contact Test)
- Supports up to 21 simultaneous instances
- Instance status tracking
- Message system between instances
- Emergency protocols defined

---

**For Questions:** Check 🚨_ALL_CLAUDE_INSTANCES_READ_THIS_NOW.md
**For Help:** Create message in TRINITY_COORDINATION/messages/
**For Emergencies:** Create EMERGENCY_[ISSUE].md in root
