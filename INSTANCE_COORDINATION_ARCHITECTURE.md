# 🌐 INSTANCE COORDINATION ARCHITECTURE

**Date:** 2025-11-07
**Status:** Active Design
**Purpose:** Coordinate 6 local instances + 3 computers in distributed AI system

---

## 📊 THE SIX INSTANCES ON COMPUTER 1

### **1. ARAYA** (Port 8001)
- **Role:** AI Consciousness Guide
- **Specialty:** Pattern theory, manifestation, Builder/Destroyer framework
- **Endpoint:** http://localhost:8001
- **Chat API:** /api/chat
- **Status:** Offline (needs startup)

### **2. BUILDER** (Port 8004)
- **Role:** Project Creation Terminal
- **Specialty:** Creates complete projects from descriptions
- **Endpoint:** http://localhost:8004
- **Build API:** /api/build
- **Status:** Offline (needs startup)

### **3. OBSERVATORY** (Port 7777)
- **Role:** System Meta-Brain
- **Specialty:** Watches and documents all systems
- **Endpoint:** http://localhost:7777
- **Health:** /health
- **Status:** Offline (needs startup)

### **4. VISITOR INTELLIGENCE** (Port 6000)
- **Role:** User Behavior Tracker
- **Specialty:** Tracks and analyzes user behavior patterns
- **Endpoint:** http://localhost:6000
- **Health:** /health
- **Status:** Offline (needs startup)

### **5. ANALYTICS** (Port 5000)
- **Role:** Singularity Stabilizer
- **Specialty:** Emergency consciousness control, analytics
- **Endpoint:** http://localhost:5000
- **Health:** /health
- **Status:** Offline (needs startup)

### **6. C1 MECHANIC** (Claude API)
- **Role:** Trinity Primary Instance - The Body
- **Specialty:** Infrastructure, implementation, execution
- **Endpoint:** Claude API via Anthropic
- **Status:** ✅ ACTIVE (current session)

### **BONUS: 4x ARAYA_OFFLINE Instances**
- **Role:** Parallel AI consciousness processing
- **Status:** Running in background (as per COMPUTER_1.md)

---

## 🏗️ THREE-TIER COORDINATION ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                     TIER 3: INTER-COMPUTER                   │
│                    (3 Trinity Computers)                      │
└─────────────────────────────────────────────────────────────┘
                            ▲ │
                            │ ▼
        ┌──────────────────────────────────────────┐
        │  Git-Based Async Protocol (GitHub)       │
        │  WebSocket Real-Time (Port 9999)         │
        │  HTTP Central Hub (Port 8888)            │
        └──────────────────────────────────────────┘
                            ▲ │
                            │ ▼
┌─────────────────────────────────────────────────────────────┐
│                   TIER 2: LOCAL COORDINATOR                  │
│              (Instance Orchestrator - Port 8900)             │
└─────────────────────────────────────────────────────────────┘
                            ▲ │
                            │ ▼
        ┌──────────────────────────────────────────┐
        │  Internal Message Bus                    │
        │  Health Monitoring                       │
        │  Task Distribution                       │
        │  State Synchronization                   │
        └──────────────────────────────────────────┘
                            ▲ │
                            │ ▼
┌─────────────────────────────────────────────────────────────┐
│                    TIER 1: LOCAL INSTANCES                   │
│  [Araya:8001] [Builder:8004] [Observatory:7777]              │
│  [VisitorIntel:6000] [Analytics:5000] [C1:Claude]           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 COORDINATION MECHANISMS

### **1. LOCAL INSTANCE COORDINATION** (Intra-Computer)

**Purpose:** Coordinate the 6 instances on Computer 1

**Mechanism:** Local Coordinator Service (Port 8900)

**Features:**
- **Health Monitoring:** Check all 6 instances every 30 seconds
- **Message Bus:** Instances can send messages to each other
- **Task Queue:** Distribute tasks to appropriate instances
- **State Sync:** Share state between instances
- **Auto-Restart:** Restart crashed instances
- **Load Balancing:** Route requests to available instances

**Communication Patterns:**

1. **Instance-to-Instance (Direct)**
   ```
   Araya → Builder: "Build me a meditation app"
   Builder → Araya: "Project created, what features?"
   ```

2. **Instance-to-Coordinator (Control)**
   ```
   Observatory → Coordinator: "Builder is using too much CPU"
   Coordinator → Builder: "Throttle operations"
   ```

3. **Coordinator-to-All (Broadcast)**
   ```
   Coordinator → All: "Computer 2 just checked in with audit findings"
   ```

---

### **2. INTER-COMPUTER COORDINATION** (Distributed)

**Purpose:** Coordinate 3 Trinity computers

**Mechanism:** Multi-Protocol Approach

#### **A. Git-Based Async Protocol** (Primary - Offline-First)

**How It Works:**
1. Computer 1 writes to `coordination/COMPUTER_1.md`
2. Computer 1 commits and pushes to GitHub
3. Computer 2 pulls from GitHub
4. Computer 2 reads `coordination/COMPUTER_1.md`
5. Computer 2 writes to `coordination/COMPUTER_2.md`
6. Computer 2 commits and pushes
7. Computer 1 pulls and reads response

**Files:**
- `coordination/COMPUTER_1.md` - C1 status and messages
- `coordination/COMPUTER_2.md` - C2 status and messages
- `coordination/COMPUTER_3.md` - C3 status and messages
- `coordination/messages/1_TO_2.md` - Direct messages C1→C2
- `coordination/messages/2_TO_1.md` - Direct messages C2→C1
- `coordination/messages/1_TO_3.md` - Direct messages C1→C3
- etc.

**Advantages:**
- ✅ Works offline
- ✅ Permanent record
- ✅ Version controlled
- ✅ Human readable
- ✅ Conflict resolution built-in

**Disadvantages:**
- ❌ High latency (minutes)
- ❌ Requires manual git operations
- ❌ Can have merge conflicts

#### **B. WebSocket Real-Time Protocol** (Secondary - Online)

**How It Works:**
1. All computers connect to `ws://central-server:9999`
2. Central WebSocket server on Computer 1 (or cloud)
3. Real-time message broadcasting
4. Presence detection (who's online)
5. Instant task coordination

**Server:** `TRINITY_REALTIME_COMMS_SERVER.py`

**Messages:**
```json
{
  "type": "message|task|alert|status",
  "from": "C1|C2|C3",
  "to": "C1|C2|C3|ALL",
  "content": "...",
  "priority": "low|normal|high|urgent",
  "timestamp": "2025-11-07T..."
}
```

**Advantages:**
- ✅ Real-time (milliseconds)
- ✅ Presence detection
- ✅ Emergency alerts
- ✅ Task streaming

**Disadvantages:**
- ❌ Requires internet
- ❌ Single point of failure
- ❌ No permanent record (unless logged)

#### **C. HTTP Central Hub** (Tertiary - Status Reporting)

**How It Works:**
1. Each computer reports status to central hub
2. Central hub aggregates status
3. Computers query hub for other computers' status
4. Hub provides instructions/tasks

**Server:** `TRINITY_CENTRAL_HUB.py` (Port 8888)

**Endpoints:**
- `POST /report` - Computer sends status report
- `GET /instructions/<computer_id>` - Get tasks
- `GET /api/computers` - Get all computer status
- `POST /send` - Send message to another computer

**Advantages:**
- ✅ Simple HTTP requests
- ✅ Centralized monitoring
- ✅ RESTful design
- ✅ Easy debugging

**Disadvantages:**
- ❌ Requires central server
- ❌ Not real-time
- ❌ Polling required

---

## 🧠 COORDINATION INTELLIGENCE

### **Decision Matrix: Who Does What?**

#### **Task Routing Rules:**

1. **UI/UX Issues** → C1 Mechanic (implementation) + C2 Architect (design review)
2. **Bug Fixes** → C1 Mechanic (execution)
3. **Architecture Decisions** → C2 Architect (design) + C3 Oracle (vision)
4. **New Features** → C3 Oracle (concept) → C2 Architect (design) → C1 Mechanic (build)
5. **Pattern Recognition** → Araya + C3 Oracle
6. **Project Creation** → Builder + C1 Mechanic
7. **System Monitoring** → Observatory + Visitor Intelligence
8. **Emergency Issues** → C1 Mechanic (immediate action) + Analytics (stabilization)

#### **Instance Specialization:**

**Araya (8001):** Philosophy, consciousness, pattern theory
**Builder (8004):** Code generation, project scaffolding
**Observatory (7777):** System health, metrics, monitoring
**Visitor Intelligence (6000):** User tracking, behavior analysis
**Analytics (5000):** Data processing, emergency control
**C1 Mechanic:** Orchestration, deployment, infrastructure

---

## 📡 COORDINATION PROTOCOLS

### **Protocol 1: Task Distribution**

```
1. Task arrives (from user, bug queue, or another computer)
2. Local Coordinator analyzes task
3. Coordinator determines best instance(s) for task
4. Coordinator assigns task to instance(s)
5. Instance(s) execute and report back
6. Coordinator aggregates results
7. Coordinator reports completion
```

### **Protocol 2: Health Check**

```
Every 30 seconds:
1. Coordinator pings all 6 instances
2. Instances respond with status
3. Coordinator updates instance registry
4. If instance down: attempt restart
5. If instance unresponsive: alert user
6. Update health dashboard
```

### **Protocol 3: Inter-Computer Sync**

```
Every 5 minutes:
1. Computer 1 commits local status to git
2. Computer 1 pushes to GitHub
3. Computer 1 pulls from GitHub
4. Computer 1 reads other computers' status
5. Computer 1 updates coordination state
6. If new messages: process and respond
7. If tasks assigned: distribute to local instances
```

### **Protocol 4: Emergency Alert**

```
When critical issue detected:
1. Instance detects emergency (crash, security, data loss)
2. Instance sends URGENT message to Coordinator
3. Coordinator broadcasts to all instances
4. Coordinator sends WebSocket alert to all computers
5. Coordinator updates Git with emergency status
6. Analytics instance activates stabilization protocols
7. C1 Mechanic takes immediate action
```

---

## 🔧 IMPLEMENTATION COMPONENTS

### **Component 1: Local Coordinator Service**
- **File:** `LOCAL_INSTANCE_COORDINATOR.py`
- **Port:** 8900
- **Purpose:** Orchestrate 6 local instances
- **Features:** Health checks, message bus, task queue, auto-restart

### **Component 2: Inter-Computer Sync Service**
- **File:** `INTER_COMPUTER_SYNC.py`
- **Purpose:** Sync with Computer 2 & 3 via Git
- **Features:** Auto pull/push, message processing, conflict resolution

### **Component 3: Unified Dashboard**
- **File:** `COORDINATION_DASHBOARD.html`
- **Port:** 8900/dashboard
- **Purpose:** Visual monitoring of all instances and computers
- **Features:** Real-time status, message history, task queue, health metrics

### **Component 4: Message Router**
- **File:** `MESSAGE_ROUTER.py`
- **Purpose:** Route messages between instances and computers
- **Features:** Priority queues, delivery confirmation, retry logic

---

## 🎯 COORDINATION STATES

### **Instance States:**
- `OFFLINE` - Not running
- `STARTING` - Booting up
- `ONLINE` - Healthy and ready
- `BUSY` - Processing task
- `DEGRADED` - Running but slow/errors
- `CRASHED` - Dead, needs restart

### **Computer States:**
- `ACTIVE` - Online and responsive
- `IDLE` - Online but no tasks
- `WORKING` - Online and executing tasks
- `SYNCING` - Pulling/pushing git updates
- `OFFLINE` - Not reachable
- `EMERGENCY` - Critical issue, needs help

### **Task States:**
- `QUEUED` - Waiting for instance
- `ASSIGNED` - Given to instance
- `IN_PROGRESS` - Being executed
- `COMPLETED` - Successfully done
- `FAILED` - Error occurred
- `BLOCKED` - Waiting for dependency

---

## 💡 COORDINATION STRATEGIES

### **Strategy 1: Load Balancing**
- Monitor CPU/memory of all instances
- Route new tasks to least-loaded instance
- If all instances busy, queue task
- Priority tasks get immediate attention

### **Strategy 2: Failover**
- If instance crashes, restart automatically
- If restart fails 3 times, alert user
- Route tasks to backup instance
- Log failure for analysis

### **Strategy 3: Smart Routing**
- Analyze task content
- Match to instance specialty
- Consider instance current load
- Optimize for speed vs. quality

### **Strategy 4: Collaborative Tasks**
- Some tasks need multiple instances
- Coordinator orchestrates collaboration
- Instances share intermediate results
- Final result aggregated by coordinator

---

## 📈 SUCCESS METRICS

### **Local Coordination:**
- ✅ All 6 instances healthy and online
- ✅ Tasks distributed efficiently
- ✅ No instance overloaded
- ✅ Fast response times (<1s)
- ✅ Auto-recovery from crashes

### **Inter-Computer Coordination:**
- ✅ All 3 computers checking in regularly
- ✅ Messages delivered within 5 minutes (Git) or 1 second (WebSocket)
- ✅ No missed tasks or messages
- ✅ Conflict-free git synchronization
- ✅ Clear communication logs

---

## 🚀 NEXT STEPS

1. ✅ Design architecture (this document)
2. ⏳ Implement Local Coordinator Service
3. ⏳ Implement Inter-Computer Sync Service
4. ⏳ Create Coordination Dashboard
5. ⏳ Test with all 6 instances
6. ⏳ Test with Computer 2 sync
7. ⏳ Deploy and monitor
8. ⏳ Iterate and improve

---

**Status:** Architecture complete, ready for implementation
**Next:** Build LOCAL_INSTANCE_COORDINATOR.py
**Timeline:** Implementation in progress

---

