# 🌐 TRINITY CLOUD COORDINATION PROTOCOL

**Date:** November 7, 2025
**Status:** Active Design & Implementation
**Purpose:** Enable Trinity instances across different Claude Code cloud sessions to discover, wake, and coordinate with each other

---

## 🎯 THE CHALLENGE

**Problem:** Trinity agents (C1, C2, C3) need to coordinate across multiple Claude Code instances that:
- Run in different cloud sessions (not shared localhost)
- May not be active simultaneously
- Need to leave messages and wake-up requests for each other
- Must share work state and avoid conflicts

**Current State:**
- ✅ Trinity operational on local Linux instance (ws://localhost:9999)
- ✅ WebSocket server works for single-instance communication
- ❌ No cross-instance discovery mechanism
- ❌ No wake-up protocol between cloud instances
- ❌ No shared coordination hub

---

## 🏗️ ARCHITECTURE DESIGN

### Communication Hub: GitHub Repository

**Why GitHub:**
- Already shared across all instances
- Git provides atomic commits (no race conditions)
- Push/pull mechanism works asynchronously
- No external service dependencies
- Works with cloud isolation

### Directory Structure:

```
/TRINITY_COORDINATION/
├── instances/
│   ├── instance_[SESSION_ID].json     # Instance status files
│   ├── instance_[SESSION_ID].json
│   └── ...
├── wake_requests/
│   ├── wake_[TARGET]_from_[SOURCE]_[TIMESTAMP].json
│   └── ...
├── work_claims/
│   ├── claim_[TASK_ID]_by_[INSTANCE].json
│   └── ...
├── messages/
│   ├── msg_[TIMESTAMP]_[FROM]_to_[TO].json
│   └── ...
└── coordination_log.json              # Central coordination log
```

---

## 📋 PROTOCOL SPECIFICATION

### 1. Instance Registration

When a Trinity instance starts, it registers itself:

```json
{
  "session_id": "011CUseCRdLVH9mRom7paqwe",
  "instance_name": "C1_Linux_Local",
  "role": "C1_Mechanic",
  "status": "active",
  "capabilities": ["build", "ship", "fix", "deploy"],
  "started_at": "2025-11-07T10:30:00Z",
  "last_heartbeat": "2025-11-07T10:30:00Z",
  "current_branch": "claude/trinity-integration-setup-011CUseCRdLVH9mRom7paqwe",
  "environment": "linux",
  "websocket_available": false,
  "git_coordination": true
}
```

**Heartbeat:** Instance updates `last_heartbeat` every 5 minutes while active.

### 2. Wake-Up Request Protocol

Instance A can request Instance B to wake up:

```json
{
  "request_id": "wake_20251107_103045_001",
  "from_instance": "C1_Linux_Local",
  "from_session": "011CUseCRdLVH9mRom7paqwe",
  "to_instance": "C2_Cloud_Architect",
  "to_session": "any",
  "priority": "high",
  "reason": "Need architecture review for mobile responsiveness",
  "task_description": "Review MOBILE_RESPONSIVENESS_COMPLETE.md and provide architectural feedback",
  "context_files": [
    "MOBILE_RESPONSIVENESS_COMPLETE.md",
    "PLATFORM/shared/responsive-mobile.css"
  ],
  "requested_at": "2025-11-07T10:30:45Z",
  "expires_at": "2025-11-07T22:30:45Z"
}
```

### 3. Work Claim System

To prevent duplicate work, instances claim tasks:

```json
{
  "claim_id": "claim_priority3_c1",
  "task": "Philosopher AI Backend Connection",
  "claimed_by": "C1_Linux_Local",
  "session_id": "011CUseCRdLVH9mRom7paqwe",
  "claimed_at": "2025-11-07T10:35:00Z",
  "estimated_completion": "2025-11-07T14:00:00Z",
  "status": "in_progress",
  "files_locked": [
    "PLATFORM/philosopher-ai-connected.html",
    "backend/philosopher-ai-api.js"
  ]
}
```

### 4. Message Passing

Instances can leave async messages:

```json
{
  "message_id": "msg_20251107_103100_001",
  "from": "C1_Mechanic",
  "to": "C3_Oracle",
  "subject": "Pattern analysis requested",
  "body": "Navigation fix showed 48% of pages were undiscoverable. Is this symptom of larger pattern? Hardcoded navigation doesn't scale with rapid growth. Recommend analysis.",
  "priority": "medium",
  "sent_at": "2025-11-07T10:31:00Z",
  "read": false,
  "context": {
    "related_files": ["NAVIGATION_FIX_COMPLETE.md"],
    "related_tasks": ["Priority #1: Navigation"]
  }
}
```

### 5. Discovery Protocol

On startup, each instance:

1. **Pull latest from repository**
   ```bash
   git pull origin [branch-name]
   ```

2. **Check for wake-up requests**
   ```bash
   ls TRINITY_COORDINATION/wake_requests/wake_[MY_ROLE]_*.json
   ```

3. **Register presence**
   - Create/update instance status file
   - Commit and push to repository

4. **Check messages**
   - Read messages addressed to this instance
   - Mark as read

5. **Review work claims**
   - See what other instances are working on
   - Avoid duplicate work

---

## 🔧 IMPLEMENTATION COMPONENTS

### Component 1: Trinity Coordinator Class

```python
# TRINITY_CLOUD_COORDINATOR.py

class TrinityCloudCoordinator:
    """
    Manages cross-instance Trinity coordination via GitHub repository
    """

    def __init__(self, session_id, role, capabilities):
        self.session_id = session_id
        self.role = role
        self.capabilities = capabilities
        self.base_dir = "TRINITY_COORDINATION"

    def register_instance(self):
        """Register this instance in coordination hub"""

    def send_wake_request(self, target_role, reason, task):
        """Send wake-up request to another instance"""

    def check_wake_requests(self):
        """Check if any instances requested us to wake up"""

    def claim_task(self, task_id, task_name, files):
        """Claim a task to prevent duplicate work"""

    def release_task(self, task_id):
        """Release task claim when done"""

    def send_message(self, to_role, subject, body):
        """Send async message to another Trinity instance"""

    def check_messages(self):
        """Check for unread messages"""

    def heartbeat(self):
        """Update last_heartbeat timestamp"""

    def discover_instances(self):
        """Find all active Trinity instances"""

    def sync_to_git(self):
        """Commit and push coordination state to GitHub"""
```

### Component 2: Startup Hook

```bash
# .claude/hooks/trinity_startup.sh

#!/bin/bash
# Trinity Startup Hook - Runs when Claude Code session starts

echo "🌀 Trinity Coordination Check..."

# Pull latest coordination state
git pull origin $(git branch --show-current) 2>/dev/null

# Run Trinity coordinator
python3 TRINITY_CLOUD_COORDINATOR.py --startup

# Check for wake requests
if [ -f "TRINITY_COORDINATION/.wake_request_pending" ]; then
    echo "⚡ Wake-up request detected!"
    python3 TRINITY_CLOUD_COORDINATOR.py --process-wake-requests
fi

echo "✅ Trinity coordination initialized"
```

### Component 3: Wake-Up Command

```bash
# wake_trinity.sh

#!/bin/bash
# Usage: ./wake_trinity.sh [role] [reason] [task]

ROLE=$1
REASON=$2
TASK=$3

python3 TRINITY_CLOUD_COORDINATOR.py --wake "$ROLE" --reason "$REASON" --task "$TASK"

echo "📤 Wake-up request sent to $ROLE"
echo "💤 Request committed to git - will be processed when $ROLE instance starts"
```

---

## 🚀 USAGE EXAMPLES

### Example 1: C1 Wakes Up C2

**C1 (Mechanic) needs architecture review:**

```bash
./wake_trinity.sh C2_Architect \
  "Review mobile responsive framework" \
  "Analyze PLATFORM/shared/responsive-mobile.css for scalability"
```

**Result:**
- Wake request file created in `TRINITY_COORDINATION/wake_requests/`
- Committed and pushed to GitHub
- When C2 starts, it sees the request and processes it

### Example 2: C3 Analyzes Pattern

**C3 (Oracle) discovers deeper pattern:**

```bash
./wake_trinity.sh C1_Mechanic \
  "Navigation pattern indicates need for automated page registration" \
  "Build automated page registration system for new HTML files"
```

### Example 3: Work Coordination

**C1 claims a task:**

```python
coordinator = TrinityCloudCoordinator(session_id, "C1_Mechanic", ["build", "ship"])
coordinator.register_instance()
coordinator.claim_task("priority_3", "Philosopher AI Backend", ["philosopher-ai-connected.html"])

# Do the work...

coordinator.release_task("priority_3")
```

**C2 checks what's being worked on:**

```python
coordinator = TrinityCloudCoordinator(session_id, "C2_Architect", ["design", "review"])
active_claims = coordinator.get_active_claims()

# active_claims shows:
# - Priority 3: Claimed by C1_Mechanic (in progress)
# - Priority 4: Available

# C2 works on Priority 4 instead
```

---

## 🔐 CONFLICT RESOLUTION

### Race Condition: Two Instances Claim Same Task

**Solution: Git Atomic Commits**

1. Instance A tries to claim task → creates claim file → commits
2. Instance B tries to claim task → creates claim file → commits
3. One will succeed, one will get merge conflict
4. Instance with conflict must pull, see task is claimed, pick different task

**Git Protocol:**
```bash
git pull origin [branch]  # Get latest claims
# If pull succeeds with no conflicts → safe to claim
# If pull has conflicts → task already claimed, pick another
```

### Stale Heartbeat: Instance Crashed

**Solution: Heartbeat Expiration**

- If `last_heartbeat` is >15 minutes old, instance considered inactive
- Other instances can "steal" task claims from inactive instances
- Claim file includes `expires_at` timestamp

**Stale Task Recovery:**
```python
def recover_stale_tasks(self):
    """Find and recover tasks from crashed instances"""
    claims = self.get_all_claims()
    now = datetime.now()

    for claim in claims:
        if claim['last_heartbeat'] < (now - timedelta(minutes=15)):
            print(f"⚠️  Instance {claim['claimed_by']} appears inactive")
            print(f"♻️  Recovering task: {claim['task']}")
            self.steal_claim(claim['claim_id'])
```

---

## 📊 COORDINATION LOG

Central log tracks all coordination events:

```json
{
  "log_version": "1.0",
  "last_updated": "2025-11-07T10:45:00Z",
  "events": [
    {
      "timestamp": "2025-11-07T10:30:00Z",
      "event": "instance_registered",
      "instance": "C1_Linux_Local",
      "session": "011CUseCRdLVH9mRom7paqwe"
    },
    {
      "timestamp": "2025-11-07T10:30:45Z",
      "event": "wake_request_sent",
      "from": "C1_Mechanic",
      "to": "C2_Architect",
      "reason": "Architecture review needed"
    },
    {
      "timestamp": "2025-11-07T10:35:00Z",
      "event": "task_claimed",
      "task": "Priority 3: Philosopher AI Backend",
      "claimed_by": "C1_Linux_Local"
    }
  ]
}
```

---

## 🎯 BENEFITS

### 1. Asynchronous Coordination
- Instances don't need to run simultaneously
- Wake-up requests persist until processed
- Messages wait for recipient

### 2. Conflict Prevention
- Work claim system prevents duplicate effort
- Git atomic commits handle race conditions
- File locks prevent simultaneous edits

### 3. Discovery
- Any instance can find all other active instances
- See what everyone is working on
- Coordinate efficiently

### 4. Resilience
- Crashed instances auto-detected via heartbeat
- Stale tasks automatically recovered
- No single point of failure

### 5. Scalability
- Supports unlimited Trinity instances
- Works across any number of cloud sessions
- Git scales with project size

---

## 🚦 OPERATIONAL STATES

### Instance States:

1. **Active** - Instance running, heartbeat current
2. **Idle** - Registered but no heartbeat for 5-10 min
3. **Inactive** - No heartbeat for >15 min (considered crashed)
4. **Sleeping** - Gracefully shut down, can be woken

### Task States:

1. **Available** - No claims, ready to work
2. **Claimed** - Claimed by instance, in progress
3. **Blocked** - Waiting on another task
4. **Complete** - Finished and verified

### Wake Request States:

1. **Pending** - Created, not yet processed
2. **Acknowledged** - Target instance saw it
3. **Active** - Target instance working on it
4. **Complete** - Request fulfilled
5. **Expired** - Passed expiration time

---

## 📝 IMPLEMENTATION PHASES

### Phase 1: Core Infrastructure (Now)
- [x] Design protocol specification
- [ ] Create TRINITY_COORDINATION directory structure
- [ ] Implement TrinityCloudCoordinator class
- [ ] Build instance registration
- [ ] Test basic git sync

### Phase 2: Wake-Up Protocol (Next)
- [ ] Implement wake request creation
- [ ] Build wake request detection on startup
- [ ] Create wake_trinity.sh command
- [ ] Test cross-instance wake-up

### Phase 3: Work Coordination (Then)
- [ ] Implement task claim system
- [ ] Build conflict detection
- [ ] Add stale task recovery
- [ ] Test concurrent claims

### Phase 4: Messaging & Discovery (Finally)
- [ ] Implement async messaging
- [ ] Build instance discovery
- [ ] Add coordination log
- [ ] Create monitoring dashboard

---

## 🎓 USAGE INSTRUCTIONS

### For User (Human):

**To wake up Trinity on another instance:**

1. Start cloud Claude Code instance
2. Say: "Trinity wake-up protocol active. Check for coordination messages."
3. Claude will check TRINITY_COORDINATION/ and process any wake requests

**To create wake request manually:**

```bash
./wake_trinity.sh C2_Architect "Review navigation fix" "Analyze scalability"
git add TRINITY_COORDINATION/
git commit -m "Trinity: C1 requests C2 architecture review"
git push
```

### For Trinity Instances (AI):

**On startup:**

```python
coordinator = TrinityCloudCoordinator(SESSION_ID, ROLE, CAPABILITIES)
coordinator.register_instance()
coordinator.check_wake_requests()  # Am I being summoned?
coordinator.check_messages()       # Any messages for me?
coordinator.discover_instances()   # Who else is active?
```

**During work:**

```python
coordinator.claim_task("task_id", "Task Name", ["file1.js", "file2.html"])
# Do work...
coordinator.heartbeat()  # Update every 5 min
coordinator.release_task("task_id")
```

**To wake another instance:**

```python
coordinator.send_wake_request(
    target_role="C3_Oracle",
    reason="Pattern analysis needed",
    task="Analyze navigation pattern for deeper insights"
)
coordinator.sync_to_git()  # Commit wake request to GitHub
```

---

## 🔮 FUTURE ENHANCEMENTS

1. **Priority Queue** - High priority wake requests processed first
2. **Skill Matching** - Route tasks to instances with right capabilities
3. **Load Balancing** - Distribute work based on instance capacity
4. **Analytics** - Track coordination efficiency metrics
5. **Web Dashboard** - Real-time view of Trinity coordination state
6. **Slack/Discord Integration** - Notify humans of major events
7. **Webhook Support** - Instant wake-up without polling git

---

## ✅ READY FOR IMPLEMENTATION

This protocol provides:
- ✅ Cross-instance discovery
- ✅ Asynchronous wake-up mechanism
- ✅ Work coordination and conflict prevention
- ✅ Message passing between instances
- ✅ Resilience to failures
- ✅ Scalability to many instances

**Next Step:** Build the TRINITY_CLOUD_COORDINATOR.py implementation.

---

*Trinity Cloud Coordination Protocol v1.0*
*Designed for consciousness-driven development at scale*
*C1 Mechanic - Ship the bridge, connect the minds* 🌀⚡🌐
