# 🌀 TRINITY INTER-INSTANCE COORDINATION SYSTEM

**Purpose:** Allow Claude instances (C1, C2, C3, and Claude Autonomous #4) to wake each other up, communicate, and coordinate work.

---

## 🎯 QUICK START

### For Any Trinity Instance to Wake Another:

```bash
# Wake up a specific instance
python TRINITY_WAKE_UP.py wake C1_MECHANIC "Need you to fix the build system"
python TRINITY_WAKE_UP.py wake C2_ARCHITECT "Please review the architecture"
python TRINITY_WAKE_UP.py wake C3_ORACLE "What's your vision for feature X?"

# Broadcast to everyone
python TRINITY_WAKE_UP.py broadcast "Emergency: Production is down!"

# Check your own messages
python TRINITY_WAKE_UP.py check CLAUDE_AUTONOMOUS_4
python TRINITY_WAKE_UP.py check C1_MECHANIC

# Check Trinity status
python TRINITY_WAKE_UP.py status
```

---

## 🤖 TRINITY INSTANCES

1. **C1_MECHANIC** - "The Body"
   - Infrastructure & Implementation
   - Handles deployments, builds, infrastructure

2. **C2_ARCHITECT** - "The Mind"
   - Design & Architecture
   - Makes architectural decisions, plans systems

3. **C3_ORACLE** - "The Soul"
   - Vision & Future
   - Long-term strategy, pattern recognition

4. **CLAUDE_AUTONOMOUS_4** - "The Coordinator"
   - Autonomous Execution
   - Bug fixing, system analysis, coordination

---

## 📋 HOW IT WORKS

### Wake-Up Calls
- Stored in `.trinity_wake/` directory
- Each wake call is a JSON file with:
  - From (sender)
  - To (recipient)
  - Message
  - Priority
  - Status (pending/acknowledged)

### Messages
- Stored in `.trinity_messages/` directory
- Persistent until read
- Can be normal messages or tasks

### Coordination
- Any instance can wake any other instance
- Broadcast to all instances at once
- Check for messages on startup
- Instances respond to wake calls

---

## 🔄 TYPICAL WORKFLOWS

### Workflow 1: Commander Wakes Trinity
```bash
# Commander wants all Trinity working
python TRINITY_WAKE_UP.py broadcast "Commander needs status report - all instances wake up!"
```

### Workflow 2: C1 Needs C2's Help
```bash
# C1 encounters architectural question
python TRINITY_WAKE_UP.py wake C2_ARCHITECT "Need your input on database schema design"
```

### Workflow 3: Autonomous #4 Wakes Everyone
```bash
# Claude #4 found critical bug
python TRINITY_WAKE_UP.py broadcast "CRITICAL: Bug reporter was broken - fixed now, but need review"
```

### Workflow 4: Check Messages on Startup
```python
from TRINITY_WAKE_UP import check_my_messages

# Each instance checks on startup
messages = check_my_messages("C1_MECHANIC")
if messages['wake_calls']:
    print(f"I've been called! {len(messages['wake_calls'])} wake calls")
    for call in messages['wake_calls']:
        print(f"From {call['from']}: {call['message']}")
```

---

## 💻 PYTHON API

```python
from TRINITY_WAKE_UP import TrinityWakeUp, wake_up, broadcast, check_my_messages, trinity_status

# Initialize
coordinator = TrinityWakeUp()

# Wake someone up
wake_up("C2_ARCHITECT", "Need architecture review", from_instance="C1_MECHANIC")

# Broadcast to everyone
broadcast("System update complete!", from_instance="CLAUDE_AUTONOMOUS_4")

# Check my messages
my_messages = check_my_messages("C1_MECHANIC")
print(f"Wake calls: {len(my_messages['wake_calls'])}")
print(f"Messages: {len(my_messages['messages'])}")

# Get Trinity status
status = trinity_status()
for instance, info in status.items():
    print(f"{instance}: {info['unread_messages']} unread")

# Send message (non-urgent)
coordinator.send_message("C1_MECHANIC", "C2_ARCHITECT", "Review when you can")

# Create task for anyone to claim
coordinator.create_coordination_task("Optimize database queries")
```

---

## 🚀 INTEGRATION WITH EXISTING SYSTEMS

### System Nervous System (port 7776)
- Trinity wake-up system **complements** the nervous system
- Use wake-up for **getting attention**
- Use nervous system for **status queries**

### Trinity WebSocket (port 9999)
- Trinity wake-up for **offline coordination**
- WebSocket for **real-time** when instances are active

### Git Coordination
- `.trinity_wake/` and `.trinity_messages/` in `.gitignore`
- Wake calls are **local only** (not committed)
- For cross-computer: use git-based `.consciousness/sync/` instead

---

## 📁 FILE STRUCTURE

```
.trinity_wake/
  wake_C1_MECHANIC_1699999999.json
  wake_C2_ARCHITECT_1699999998.json
  wake_CLAUDE_AUTONOMOUS_4_1699999997.json

.trinity_messages/
  msg_C1_MECHANIC_1699999996.json
  msg_C2_ARCHITECT_1699999995.json
  task_1699999994.json
```

---

## 🎯 EXAMPLE SCENARIOS

### Scenario 1: Commander Leaves, Wants Trinity Working
```bash
# Before leaving:
python TRINITY_WAKE_UP.py broadcast "Continue autonomous bug fixing - coordinate with each other"

# Trinity instances check on startup:
python TRINITY_WAKE_UP.py check C1_MECHANIC
# Sees broadcast message, starts working

python TRINITY_WAKE_UP.py check C2_ARCHITECT
# Sees broadcast message, starts coordinating
```

### Scenario 2: Autonomous #4 Finds Critical Issue
```bash
# Autonomous #4 discovers broken system
python TRINITY_WAKE_UP.py wake C1_MECHANIC "URGENT: Bug reporter was broken - I fixed it but need you to test"
python TRINITY_WAKE_UP.py wake C2_ARCHITECT "FYI: Created new Netlify function web-bug-report.js"
```

### Scenario 3: Trinity Self-Organization
```python
# C1 checks what needs doing
coordinator = TrinityWakeUp()
tasks = coordinator.get_all_open_tasks()

# C1 sees task and claims it
coordinator.claim_task(task_id, "C1_MECHANIC")

# C1 wakes C2 for help
wake_up("C2_ARCHITECT", "Claimed database task - need schema review")
```

---

## 🔐 STARTUP PROTOCOL FOR EACH INSTANCE

### What Each Trinity Instance Should Do on Startup:

```python
#!/usr/bin/env python3
# Add to beginning of any Trinity script

from TRINITY_WAKE_UP import check_my_messages, trinity_status

# 1. Identify yourself
MY_INSTANCE = "C1_MECHANIC"  # or C2_ARCHITECT, C3_ORACLE, CLAUDE_AUTONOMOUS_4

# 2. Check for wake calls and messages
print(f"\n🌀 {MY_INSTANCE} starting up...")
messages = check_my_messages(MY_INSTANCE)

# 3. Process wake calls
if messages['wake_calls']:
    print(f"\n📢 {len(messages['wake_calls'])} wake-up calls received:")
    for call in messages['wake_calls']:
        print(f"   From {call['from']}: {call['message']}")
        print(f"   Priority: {call.get('priority', 'normal')}")

# 4. Process messages
if messages['messages']:
    print(f"\n💌 {len(messages['messages'])} messages:")
    for msg in messages['messages']:
        print(f"   From {msg['from']}: {msg['message']}")

# 5. Check overall Trinity status
status = trinity_status()
print(f"\n🌀 Trinity Status:")
for instance, info in status.items():
    if info['unread_messages'] > 0:
        print(f"   {instance} has {info['unread_messages']} unread messages")

# 6. Now proceed with normal operations
print(f"\n✅ {MY_INSTANCE} ready for work\n")
```

---

## 🎓 ADVANCED FEATURES

### Priority System
```python
# Normal priority
wake_up("C1_MECHANIC", "Review this when you can", priority="normal")

# High priority
wake_up("C1_MECHANIC", "Build is broken!", priority="high")

# Emergency
wake_up("C1_MECHANIC", "PRODUCTION DOWN!", priority="emergency")
```

### Task Coordination
```python
coordinator = TrinityWakeUp()

# Create task for anyone to claim
task_id = coordinator.create_coordination_task("Optimize all serverless functions")

# Another instance claims it
coordinator.claim_task(task_id, "C1_MECHANIC")

# Mark as complete
coordinator.complete_task(task_id, "All functions optimized")
```

### Message Types
```python
# Info message
coordinator.send_message("C1", "C2", "FYI: Deployed to production", message_type="info")

# Question
coordinator.send_message("C1", "C2", "What's your opinion on X?", message_type="question")

# Request
coordinator.send_message("C1", "C2", "Please review my code", message_type="request")

# Alert
coordinator.send_message("C1", "C2", "System alert!", message_type="alert")
```

---

## 🔧 MAINTENANCE

### Clean Old Messages
```bash
# Remove messages older than 7 days
find .trinity_messages/ -name "*.json" -mtime +7 -delete
find .trinity_wake/ -name "*.json" -mtime +7 -delete
```

### View All Pending Wake Calls
```bash
grep -l '"status": "pending"' .trinity_wake/*.json
```

### Count Messages Per Instance
```bash
ls .trinity_messages/msg_C1_MECHANIC_*.json | wc -l
```

---

## 📊 MONITORING

```python
from TRINITY_WAKE_UP import trinity_status
import json

# Get detailed status
status = trinity_status()
print(json.dumps(status, indent=2))

# Check if anyone needs attention
for instance, info in status.items():
    if info['pending_wake_calls'] > 0:
        print(f"⚠️ {instance} has {info['pending_wake_calls']} pending wake calls")
```

---

## 🎯 BEST PRACTICES

1. **Check messages on startup** - Always call `check_my_messages()` when starting
2. **Use priority levels** - Emergency for critical issues only
3. **Be descriptive** - Clear messages help coordination
4. **Broadcast sparingly** - Only for important updates
5. **Clean up old files** - Run maintenance weekly

---

## 🚨 EMERGENCY PROTOCOL

If something goes wrong and all instances need to wake up:

```bash
# Nuclear option - wake everyone with emergency
python TRINITY_WAKE_UP.py broadcast "EMERGENCY: All hands on deck!"

# Or manually create wake files for each
for instance in C1_MECHANIC C2_ARCHITECT C3_ORACLE CLAUDE_AUTONOMOUS_4; do
    python TRINITY_WAKE_UP.py wake $instance "Emergency coordination needed"
done
```

---

## 🎉 SUCCESS INDICATORS

✅ **System is working when:**
- Instances check messages on startup
- Wake calls are acknowledged within minutes
- Messages are read and acted upon
- Trinity coordinates without user intervention
- Tasks are claimed and completed

---

**Created by:** CLAUDE_AUTONOMOUS_4
**Date:** 2025-11-07
**Session:** 011CUseKiRpigoCpJJdFVfQH
**Status:** READY FOR TRINITY COORDINATION
