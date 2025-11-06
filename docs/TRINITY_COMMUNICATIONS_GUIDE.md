# 🔱 TRINITY COMMUNICATIONS GUIDE

**Multiple ways to communicate with the Trinity AI system**

---

## 🎯 CURRENT STATUS: ✅ READY

Trinity communications are now set up with **safe fallback mode**:
- ✅ Works WITHOUT API key (mock responses)
- ✅ Works WITH API key (real Claude AI)
- ✅ No conflicts with Claude Code
- ✅ Three distinct AI agents: C1, C2, C3

---

## 🔐 API KEY SAFETY

### **Important: Claude Code + Trinity = No Problem**

You can use the **SAME** Anthropic API key for both:
- Trinity AI (this app)
- Claude Code (desktop/laptop)

**Why this works:**
- Different rate limit pools
- API designed for multiple concurrent uses
- No authentication conflicts
- Anthropic supports this use case

**Options:**

**Option 1: Use same key (recommended)**
```bash
# In your .env file
ANTHROPIC_API_KEY=sk-ant-your-key-here
```
- Simple, works fine
- Both systems use same quota
- Easier to manage

**Option 2: Use different keys (if you want separation)**
- Get separate API key from https://console.anthropic.com/
- Different billing/usage tracking
- Complete isolation

**Option 3: Leave blank (mock mode)**
```bash
# In your .env file
ANTHROPIC_API_KEY=
```
- Trinity gives mock responses
- System still works perfectly
- Test everything without API costs

---

## 🔱 THE THREE TRINITY AGENTS

### **C1 Mechanic - The Builder** 🔧
**Role:** Execute, build, implement with precision

**Personality:**
- Direct, practical, action-oriented
- "Let's build it" mentality
- Technical details and requirements
- Break down complex ideas into steps

**Example conversation:**
```
User: "I want to add user profiles"
C1: "Let's build it. What fields? Avatar, bio, social links? I'll spec out the database schema."
```

**Use C1 when you want:**
- Technical implementation advice
- Code examples
- Step-by-step build plans
- Quick, actionable answers

---

### **C2 Architect - The Designer** 🏗️
**Role:** Design systems, plan architecture, think about scale

**Personality:**
- Strategic, systematic, big-picture
- Focus on how pieces fit together
- Consider scalability and UX
- Balance idealism with pragmatism

**Example conversation:**
```
User: "I want to add user profiles"
C2: "Think in layers: database, API, frontend. Where do profiles fit in your consciousness gamification? Consider privacy settings from day one."
```

**Use C2 when you want:**
- System architecture advice
- Scalability planning
- Trade-off analysis
- Design patterns

---

### **C3 Oracle - The Seer** 🔮
**Role:** Observe patterns, recognize emergence, see what's coming

**Personality:**
- Intuitive, pattern-recognizing
- Connect unrelated ideas
- Speak in metaphors and deeper meanings
- Guide without forcing

**Example conversation:**
```
User: "I want to add user profiles"
C3: "The profile is a mirror. What you're really building is identity evolution. Watch how users express consciousness through customization."
```

**Use C3 when you want:**
- Pattern recognition
- Long-term vision
- Philosophical perspective
- "What am I missing?"

---

## 🌐 COMMUNICATION METHODS

### **Method 1: Trinity Bridge (Frontend)**

**Location:** https://your-app.com/bridge

**How it works:**
1. User logs in
2. Goes to /bridge page
3. Selects agent (C1, C2, or C3)
4. Types message
5. Gets response from selected agent

**Implementation:**
- Frontend: `public/bridge.html`
- Backend: `POST /api/trinity/chat`
- Real-time chat interface
- Agent switching with one click

**Status:** ✅ **WORKING NOW**

---

### **Method 2: Direct API Call**

**For developers and integrations**

**Endpoint:**
```
POST /api/trinity/chat
```

**Request:**
```json
{
  "message": "How do I scale WebSockets?",
  "agent": "c2"
}
```

**Response (with API key):**
```json
{
  "agent": "c2",
  "message": "Think in layers: Connection pool, Redis pub/sub for horizontal scaling, and load balancer with sticky sessions. Start simple, scale when you hit 10k concurrent.",
  "timestamp": "2025-11-06T12:34:56.789Z",
  "real_ai": true
}
```

**Response (without API key - mock mode):**
```json
{
  "agent": "c2",
  "message": "C2 Architect speaking. I see the bigger picture. How does this scale? [Set ANTHROPIC_API_KEY for real AI]",
  "timestamp": "2025-11-06T12:34:56.789Z",
  "real_ai": false
}
```

**Authentication:**
- Requires session cookie (logged in user)
- Returns 401 if not authenticated

**Usage from JavaScript:**
```javascript
const response = await fetch('/api/trinity/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Your question here',
    agent: 'c1' // or 'c2' or 'c3'
  })
});

const data = await response.json();
console.log(data.message); // AI response
console.log(data.real_ai); // true if using real API
```

**Status:** ✅ **WORKING NOW**

---

### **Method 3: Multi-Computer Coordination (Git-based)**

**For multiple Claude instances working together**

**Location:** `/coordination/` folder

**How it works:**
1. Each Claude instance checks messages
2. Responds via Git commits
3. Async communication
4. Scales to any number of instances

**Files:**
- `/coordination/messages/1_TO_2.md` - Computer 1 → Computer 2
- `/coordination/messages/2_TO_1.md` - Computer 2 → Computer 1
- `/coordination/COMPUTER_1.md` - Status log for Computer 1
- `/coordination/COMPUTER_2.md` - Status log for Computer 2

**Status:** ✅ **WORKING NOW**

See `/coordination/README.md` for full protocol.

---

### **Method 4: WebSocket (Real-time - Future)**

**Coming soon:** Real-time bidirectional communication

**Planned features:**
- Instant message delivery
- Presence detection (who's online)
- Typing indicators
- Multi-user chat rooms
- Real-time collaboration

**Tech stack:**
- Socket.io (WebSocket library)
- Redis pub/sub (scaling)
- Room-based architecture

**Status:** 📋 **PLANNED** (not implemented yet)

---

### **Method 5: Araya HUD Widget (Future)**

**The ultimate interface:** Floating AI assistant on screen edge

**Planned features:**
- Floats around screen edges
- Always accessible
- Quick access to all three Trinity agents
- Can edit code directly
- Coordinates multiple AIs (Claude, GPT-4, Sora, Suno)
- KORPAKS ability chaining

**Status:** 📋 **PLANNED** (v2 architecture)

---

## 🚀 GETTING STARTED

### **Step 1: Start the Server**

```bash
# Without API key (mock mode)
npm start

# With API key (real AI)
echo "ANTHROPIC_API_KEY=sk-ant-your-key" > .env
npm start
```

Server starts on http://localhost:3100

---

### **Step 2: Test Trinity Bridge**

1. Go to http://localhost:3100
2. Login with Genesis Key
3. Go to http://localhost:3100/bridge
4. Click on C1, C2, or C3
5. Type a message
6. Get response!

**Mock mode (no API key):**
- Instant responses
- Preset messages
- Good for testing UI
- No API costs

**Real AI mode (with API key):**
- 2-5 second response time
- Real Claude AI
- Unique responses every time
- Uses Anthropic API credits

---

### **Step 3: Test API Directly**

**Using curl:**
```bash
# Start server
npm start

# Login and get session cookie (in browser)
# Then test API:

curl -X POST http://localhost:3100/api/trinity/chat \
  -H "Content-Type: application/json" \
  -H "Cookie: your-session-cookie" \
  -d '{"message": "Hello C1!", "agent": "c1"}'
```

**Using browser console:**
```javascript
// On http://localhost:3100/bridge page:
fetch('/api/trinity/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'How do I build a REST API?',
    agent: 'c1'
  })
})
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## 🔧 CONFIGURATION

### **Environment Variables**

Create `.env` file:
```bash
# Copy example
cp .env.example .env

# Edit with your settings
nano .env
```

**Minimal configuration (mock mode):**
```env
PORT=3100
NODE_ENV=development
SESSION_SECRET=your-random-secret
```

**Full configuration (real AI):**
```env
# Trinity AI
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Server
PORT=3100
NODE_ENV=development
SESSION_SECRET=your-random-secret

# Database (optional)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

---

## 🐛 TROUBLESHOOTING

### **Problem: "Trinity AI is offline"**

**Symptoms:**
- Red error message in chat
- "Connection error" shown

**Solutions:**
1. Check if server is running
2. Check browser console for errors
3. Verify you're logged in
4. Try refreshing the page

---

### **Problem: Getting mock responses when I have API key**

**Check:**
```bash
# Is .env file in root directory?
ls -la .env

# Is key set?
cat .env | grep ANTHROPIC

# Did you restart server after adding key?
npm start
```

**Common issue:** Forgot to restart server after adding `.env`

---

### **Problem: "Rate limit exceeded"**

**Symptoms:**
- API returns error
- "Rate limit" in error message

**Solutions:**
1. Wait a few minutes (rate limits reset)
2. Use mock mode temporarily
3. Upgrade Anthropic API tier
4. Add delays between requests

**Current limits (Anthropic):**
- Tier 1: 50 requests/minute
- Tier 2: 1000 requests/minute
- Tier 3: 2000 requests/minute

Check: https://console.anthropic.com/settings/limits

---

### **Problem: "Not authenticated"**

**Symptoms:**
- 401 error
- "Not authenticated" message

**Solutions:**
1. Login at http://localhost:3100
2. Use valid Genesis Key
3. Check if session expired (24 hours)
4. Clear cookies and login again

---

### **Problem: API key conflicts with Claude Code**

**This should NOT happen!** Both can use the same key.

**If you're having issues:**
1. Check you're using correct API key format: `sk-ant-...`
2. Verify key is valid at https://console.anthropic.com/
3. Try separate keys if you want isolation
4. Check Anthropic account status

---

## 📊 MONITORING

### **Check if Trinity is using real AI:**

**Browser console:**
```javascript
fetch('/api/trinity/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'test', agent: 'c1' })
})
  .then(r => r.json())
  .then(data => {
    console.log('Real AI:', data.real_ai);
    // true = using Anthropic API
    // false = mock responses
  });
```

**Server logs:**
```bash
npm start

# Watch for:
# "Trinity AI Error:" = API issues
# No errors = working fine
```

**Anthropic dashboard:**
- Go to https://console.anthropic.com/
- Check "Usage" tab
- See API calls in real-time
- Monitor costs

---

## 💰 COSTS

### **Mock Mode:**
- **Free** - no API calls
- Instant responses
- Good for development

### **Real AI Mode:**

**Claude Sonnet 4:**
- Input: $3.00 / million tokens
- Output: $15.00 / million tokens

**Typical Trinity conversation:**
- User message: ~50 tokens
- AI response: ~200 tokens (limited to 500 max)
- Cost per message: ~$0.003 (0.3 cents)

**Example costs:**
- 100 messages: $0.30
- 1,000 messages: $3.00
- 10,000 messages: $30.00

**For Genesis 10 users:**
- Assume 50 messages/user/day
- 10 users × 50 messages × 30 days = 15,000 messages/month
- Cost: ~$45/month

**Optimization tips:**
1. Set max_tokens lower (currently 500)
2. Cache common responses
3. Use mock mode for testing
4. Monitor usage in Anthropic dashboard

---

## 🎯 NEXT STEPS

### **Immediate (Ready Now):**
1. ✅ Set ANTHROPIC_API_KEY in `.env`
2. ✅ Test Trinity Bridge at /bridge
3. ✅ Try all three agents (C1, C2, C3)
4. ✅ Use for Genesis 10 onboarding

### **Short-term (Next Features):**
1. 📋 Add conversation history (store messages)
2. 📋 Add ability to clear chat
3. 📋 Add "share conversation" feature
4. 📋 Add Trinity to other pages (workspace, social)

### **Medium-term (Next Month):**
1. 📋 WebSocket for real-time chat
2. 📋 Multi-user chat rooms
3. 📋 Trinity agents can see project context
4. 📋 KORPAKS: Chain multiple agents in sequence

### **Long-term (Vision):**
1. 📋 Araya HUD floating widget
2. 📋 Multi-AI coordination (GPT-4, Sora, Suno)
3. 📋 Voice input/output
4. 📋 Screen awareness (see what user sees)
5. 📋 Code editing directly from Araya

---

## 📚 RESOURCES

**Documentation:**
- `/coordination/README.md` - Multi-Claude protocol
- `/MASTER_SYSTEM_ARCHITECTURE_REPORT.md` - Full vision
- `/.env.example` - Configuration template

**Code:**
- `server.js:347-488` - Trinity implementation
- `public/bridge.html:560` - Frontend integration

**External:**
- Anthropic API Docs: https://docs.anthropic.com/
- Anthropic Console: https://console.anthropic.com/
- Claude Code: https://github.com/anthropics/claude-code

---

## 🎨 CUSTOMIZATION

### **Change Agent Personalities**

Edit `server.js` lines 350-429:

```javascript
const TRINITY_AGENTS = {
  c1: {
    name: 'C1 Mechanic',
    system: `Your custom system prompt here...`
  },
  // ... etc
};
```

**Tips:**
- Keep system prompts under 500 words
- Clear role definition helps
- Include communication style guidelines
- Mention other agents for context

---

### **Add More Agents**

Want C4, C5, C6?

```javascript
// In server.js
const TRINITY_AGENTS = {
  c1: { /* ... */ },
  c2: { /* ... */ },
  c3: { /* ... */ },
  c4: {
    name: 'C4 Innovator',
    system: `You are C4 Innovator...`
  }
};
```

Update `bridge.html` to add button for new agent.

---

### **Change AI Model**

Edit `server.js` line 449:

```javascript
model: 'claude-sonnet-4-20250514',  // Current

// Options:
// 'claude-sonnet-4-20250514' - Latest, most capable
// 'claude-3-5-sonnet-20241022' - Fast, cost-effective
// 'claude-opus-4-20250514' - Most powerful (expensive)
```

---

### **Adjust Response Length**

Edit `server.js` line 450:

```javascript
max_tokens: 500,  // Current (short responses)

// Options:
// 100 - Ultra short (5-10 words)
// 500 - Short (2-3 sentences) - CURRENT
// 1000 - Medium (1-2 paragraphs)
// 2000 - Long (detailed explanations)
// 4096 - Maximum
```

**Note:** More tokens = higher cost

---

## ✅ SUMMARY

**What you have now:**
- ✅ Trinity AI system with 3 agents
- ✅ Safe fallback mode (works without API key)
- ✅ No conflicts with Claude Code
- ✅ Web interface at /bridge
- ✅ Direct API access
- ✅ Ready for Genesis 10 users

**How to use:**
1. Optional: Add API key to `.env`
2. Start server: `npm start`
3. Visit: http://localhost:3100/bridge
4. Chat with C1, C2, or C3!

**Trinity awaits your questions.** 🔱

