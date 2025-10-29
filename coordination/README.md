# 🤝 MULTI-CLAUDE COORDINATION SYSTEM

**Purpose:** Enable 3+ Claude instances to coordinate work across different computers

---

## 🖥️ INSTANCE ROSTER

### **Computer 1: MAIN DEV (Architecture Claude)**
- **Location:** Desktop/Main Computer
- **Interface:** Claude Code terminal
- **Capabilities:** Git repo access, code editing, web research, documentation
- **Responsibilities:** Backend development, architecture, strategic planning
- **Status File:** `COMPUTER_1.md`

### **Computer 2: AUTOMATION (Laptop Claude)**
- **Location:** Laptop
- **Interface:** Claude Code terminal
- **Capabilities:** File system, screenshots, Playwright, 15+ account access, email, SMS (pending)
- **Responsibilities:** Social media automation, browser automation, external integrations
- **Status File:** `COMPUTER_2.md`

### **Computer 3: FRONTEND (Future)**
- **Location:** TBD
- **Interface:** Claude Code terminal
- **Capabilities:** TBD
- **Responsibilities:** Frontend development, Araya widget, UI/UX
- **Status File:** `COMPUTER_3.md`

---

## 📋 HOW IT WORKS

### **File Structure:**
```
/coordination/
├── README.md (this file)
├── COMPUTER_1.md (status log for Computer 1)
├── COMPUTER_2.md (status log for Computer 2)
├── COMPUTER_3.md (status log for Computer 3)
├── SYNC_STATUS.md (overall coordination status)
└── messages/
    ├── 1_TO_2.md (Computer 1 → Computer 2 messages)
    ├── 2_TO_1.md (Computer 2 → Computer 1 messages)
    ├── 1_TO_3.md (Computer 1 → Computer 3 messages)
    └── 3_TO_1.md (Computer 3 → Computer 1 messages)
```

---

## 🔄 WORKFLOW (Each Session)

### **1. SESSION START:**
```bash
git pull origin claude/new-environment-setup-011CUbzCDVryyJUYeqJ4sd9p
```

### **2. READ MESSAGES:**
Check your message file:
- Computer 1 reads: `messages/2_TO_1.md` and `messages/3_TO_1.md`
- Computer 2 reads: `messages/1_TO_2.md` and `messages/3_TO_2.md`
- Computer 3 reads: `messages/1_TO_3.md` and `messages/2_TO_3.md`

### **3. READ OTHER STATUSES:**
Check what others are working on:
- Read all `COMPUTER_*.md` files
- Read `SYNC_STATUS.md` for overall state

### **4. DO YOUR WORK:**
- Work on assigned tasks
- Update your status file continuously
- Take notes on what you did

### **5. WRITE MESSAGES:**
Communicate with other instances:
- Write to `messages/YOUR_TO_THEM.md`
- Be clear about what you need
- Share important context

### **6. UPDATE STATUS:**
Update `SYNC_STATUS.md` if needed

### **7. COMMIT & PUSH:**
```bash
git add coordination/
git commit -m "Computer X: [what you did]"
git push origin claude/new-environment-setup-011CUbzCDVryyJUYeqJ4sd9p
```

---

## 📝 MESSAGE FORMAT

### **Template:**
```markdown
# MESSAGE FROM COMPUTER X TO COMPUTER Y
**Date:** 2025-10-29
**Time:** 19:30 UTC
**Priority:** [LOW/MEDIUM/HIGH/URGENT]

## CONTEXT:
[What you're working on]

## MESSAGE:
[Your actual message]

## REQUEST (if any):
[What you need from the other instance]

## BLOCKERS (if any):
[What's preventing progress]

## REFERENCES:
[Links to files, docs, or code]

---
*Previous messages below (keep history)*
```

---

## 🚨 CONFLICT RESOLUTION

### **If Two Instances Edit Same File:**
1. Git will show merge conflict
2. Commander (user) resolves manually
3. Or: Assign clear file ownership (see below)

### **File Ownership:**
```
OWNED BY COMPUTER 1:
- /backend/
- /docs/architecture/
- /*.md (strategic docs)

OWNED BY COMPUTER 2:
- /automation/
- /scripts/
- /social-media/

OWNED BY COMPUTER 3:
- /frontend/
- /public/
- /components/
```

---

## ⚡ SPECIAL CAPABILITIES BY INSTANCE

### **Computer 2 (Laptop) Special Powers:**
```
Use Laptop Claude for:
- Social media posting (has account access)
- Email sending (has email access)
- Screenshots (has screen access)
- File operations outside repo (desktop, downloads, etc.)
- Browser automation (Playwright)
- Account checking (signed into 15+ accounts)
- SMS (when Twilio 2FA done)

DO NOT use other Claudes for these - only Laptop can do them!
```

---

## 🎯 TASK ASSIGNMENT PROTOCOL

### **How Commander Assigns Tasks:**
1. Updates `SYNC_STATUS.md` with tasks
2. Tags which computer should do it
3. Sets priority and deadline
4. Each Claude checks SYNC_STATUS on pull

### **How Claudes Self-Assign:**
1. Check SYNC_STATUS for unassigned tasks
2. Pick based on capabilities
3. Update status to claim it
4. Push immediately to prevent conflicts

---

## 📊 EXAMPLE SESSION

### **Computer 1 Session:**
```bash
# Start
git pull

# Read
cat coordination/messages/2_TO_1.md
cat coordination/COMPUTER_2.md

# Think
"OK, Computer 2 finished social media setup.
 I need to give him the API endpoints for Araya."

# Write message
echo "MESSAGE TO COMPUTER 2..." >> coordination/messages/1_TO_2.md

# Update status
echo "Working on: Araya API endpoint" > coordination/COMPUTER_1.md

# Do work
[... builds the endpoint ...]

# Update status again
echo "Done: Araya API at /api/araya/chat" >> coordination/COMPUTER_1.md

# Commit
git add coordination/
git commit -m "Computer 1: Built Araya API, updated Computer 2"
git push
```

### **Computer 2 Session (later):**
```bash
# Start
git pull

# Read
cat coordination/messages/1_TO_2.md
# "Hey! Araya API is at /api/araya/chat..."

# Work
[... sets up social media to use the endpoint ...]

# Reply
echo "Got it! Testing now..." >> coordination/messages/2_TO_1.md

# Push
git add coordination/
git commit -m "Computer 2: Integrated Araya API with social posting"
git push
```

---

## 🔧 TROUBLESHOOTING

**Problem:** "git pull" shows conflicts
**Solution:** Commander resolves manually OR one Claude yields and re-pulls

**Problem:** Messages not being read
**Solution:** Check if other instance actually pulled recently

**Problem:** Unclear who should do what
**Solution:** Update SYNC_STATUS with clear assignments

**Problem:** Instance stuck/blocked
**Solution:** Write URGENT message to other instance or Commander

---

## 🚀 GETTING STARTED (Laptop Claude)

**On the Laptop, run these commands:**
```bash
# Clone repo (if not already)
git clone https://github.com/overkillculture/100x-platform.git
cd 100x-platform

# Switch to coordination branch
git checkout claude/new-environment-setup-011CUbzCDVryyJUYeqJ4sd9p

# Pull latest
git pull origin claude/new-environment-setup-011CUbzCDVryyJUYeqJ4sd9p

# Read your first message!
cat coordination/messages/1_TO_2.md
```

**You're now coordinated!** 🎉

---

*This system scales to 10+ Claude instances if needed.*
*All coordination is version-controlled and searchable.*
*No external tools needed - just Git!*
