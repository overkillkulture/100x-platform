# 🗂️ QUICK FILE REFERENCE - 100X PLATFORM

## CRITICAL FILES YOU NEED TO KNOW

### Frontend Foundation
```
/workspace-v3.html                          Main workspace UI (modify this)
/consciousness-workspace.html                Claude-like interface
/poker-table-workspace-v3.html              Collaborative gaming interface
/PLATFORM/index.html                         Main platform entry point
/frontend/consciousness-sdk.js               Frontend SDK utilities
```

### Backend Core
```
/BACKEND/database_schema.sql                PostgreSQL schema (16 tables)
/BACKEND/auth_system.py                     User auth & JWT tokens
/BACKEND/TRINITY_MISSION_CONTROL_API.py     AI coordination API
/netlify/functions/araya-chat.js            Chat endpoint
/netlify/functions/araya-api.mjs            Main AI API
```

### AI Systems
```
/araya.html                                 Araya AI Assistant
/TRINITY_COMMAND_CENTER.html                Trinity control hub
/TRINITY_COLLABORATION_INTERFACE.html       C1/C2/C3 interface
/PLATFORM/trinity-cockpit.html              Trinity cockpit
```

### Module System
```
/MODULES/AUTOMATION/jarvis_assistant/       Voice automation
/MODULES/CONTENT/                           Content creation modules
/MODULES/KNOWLEDGE/                         Knowledge management
/MODULES/ADVANCED/ai_code_sandbox/          Code execution
```

### Domain Pages
```
/domain-intelligence.html                   AI/Intelligence domain
/domain-music.html                          Music production domain
/domain-commerce.html                       Commerce/Marketplace domain
/domain-consciousness.html                  Core consciousness domain
(13 domains total - see CODEBASE_ARCHITECTURE_MAP.md)
```

### Key Configuration
```
/package.json                               Dependencies
/.env.example                               Environment variables
/.netlify/functions/package.json            Netlify deps
/netlify.toml                              Netlify config (if exists)
/.gitignore                                Git config
```

### Documentation & Planning
```
/CODEBASE_ARCHITECTURE_MAP.md               Full architecture analysis
/COLLABORATION_WORKSPACE_ROADMAP.md         4-phase implementation plan
/DOCS/                                     20+ blueprint files
/.consciousness/SYNC_PROTOCOL.md            Inter-computer sync
```

---

## FILES TO MODIFY FOR COLLABORATION

### Week 1-2: Real-Time Foundation
- `/workspace-v3.html` → Add Socket.IO integration
- `/frontend/consciousness-sdk.js` → Add real-time methods
- Create: `/frontend/workspace-realtime.js` → New WebSocket client

### Week 3-4: Collaborative Editing
- `/frontend/` → Add Yjs library integration
- Create: `/frontend/collaborative-editor.js` → CRDT editor
- Create: `/BACKEND/workspace_service.py` → Conflict resolution

### Week 5-6: Workspace Management
- Create: `/netlify/functions/workspace-api.mjs` → CRUD operations
- Create: `/frontend/workspace-manager.js` → Workspace lifecycle
- `/BACKEND/database_schema.sql` → Add 3 workspace tables

### Week 7-8: AI Integration
- Create: `/BACKEND/trinity-workspace-agent.py` → AI for workspaces
- Create: `/frontend/ai-collaboration.js` → AI presence
- Enhance: `/BACKEND/TRINITY_MISSION_CONTROL_API.py` → Workspace coordination

---

## DIRECTORY STRUCTURE CHEAT SHEET

```
/100x-platform/
├── /netlify/functions/          API endpoints (26 functions)
├── /BACKEND/                    Python services
├── /frontend/                   Frontend components
├── /MODULES/                    15+ automation modules
├── /DOCS/                       20+ documentation files
├── /PLATFORM/                   Main platform files
│   └── /shared/                 Reusable JS components
├── /4bot_projects/              4-bot projects
├── /coordination/               Inter-computer sync
├── /.consciousness/             GitHub sync protocol
├── /domain-*.html               7+ domain pages
├── /workspace-*.html            Workspace variants
├── /araya*.html                 Araya AI interfaces
├── /TRINITY_*.html              Trinity interfaces
├── /hud-*.html                  HUD interfaces
├── /DATA/                       JSON data files
├── /api/                        API data (stats, submissions)
├── package.json                 Main dependencies
├── .env.example                 Env template
└── CODEBASE_ARCHITECTURE_MAP.md THIS ANALYSIS
```

---

## KEY TABLES IN DATABASE

### User & Auth
- `users` - User accounts
- `subscriptions` - Domain subscriptions
- `domain_access` - Per-domain permissions

### Workspace (TO ADD)
- `workspaces` - Workspace records
- `workspace_members` - User access to workspaces
- `workspace_content` - Shared content/edits

### Commerce
- `transactions` - Payments
- `marketplace_items` - Creator economy items
- `creator_payouts` - Creator earnings

### Analytics
- `revenue_snapshots` - Financial metrics
- `conversion_events` - Funnel tracking
- `system_alerts` - Automated alerts

### Domain Specific
- `musik_profiles` - Music streaming integration
- `korpaks` - Autonomous work units
- `keystone_allies` - Customer acquisition

---

## ENVIRONMENT VARIABLES YOU NEED

### Critical (Must Have)
```
ANTHROPIC_API_KEY                # Claude API
STRIPE_SECRET_KEY                # Stripe payments
DATABASE_URL                     # PostgreSQL connection
```

### Important (Recommended)
```
AIRTABLE_TOKEN                   # AI memory/brain
TWILIO_ACCOUNT_SID               # SMS
SENDGRID_API_KEY                 # Email
```

### Optional
```
OPENAI_API_KEY
GITHUB_TOKEN
TWITTER_API_KEY
INSTAGRAM_ACCESS_TOKEN
```

---

## COMMON PATTERNS IN CODEBASE

### API Endpoint Pattern (Netlify)
```javascript
// /netlify/functions/example.js
const handler = async (event) => {
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: { 'Access-Control-Allow-Origin': '*' }
    };
  }
  
  try {
    const { data } = JSON.parse(event.body);
    // Process request
    return {
      statusCode: 200,
      body: JSON.stringify({ success: true })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};

module.exports = { handler };
```

### Python Service Pattern
```python
# /BACKEND/service.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/endpoint', methods=['POST'])
def handle_request():
    data = request.get_json()
    # Process data
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
```

### Frontend Real-Time Pattern (TO ADD)
```javascript
// Will be in /frontend/workspace-realtime.js
const socket = io('wss://your-server.com');

socket.on('connect', () => {
  socket.emit('join-workspace', workspaceId);
});

socket.on('user-joined', (user) => {
  // Handle user presence
});

socket.on('content-changed', (change) => {
  // Apply remote change
});
```

---

## DEPLOYMENT CHECKLIST

- [ ] Database schema migrated to PostgreSQL
- [ ] Environment variables set
- [ ] Netlify functions deployed
- [ ] Backend server running (Railway/Render)
- [ ] WebSocket server deployed
- [ ] DNS pointing to correct domain
- [ ] SSL/HTTPS enabled
- [ ] Rate limiting configured
- [ ] Backup system in place
- [ ] Monitoring/alerts set up

---

## QUICK ANSWERS

**Q: Where is the workspace?**
A: `/workspace-v3.html` - This is where you add real-time collaboration

**Q: How are users authenticated?**
A: JWT tokens from `/BACKEND/auth_system.py` - Uses bcrypt hashing

**Q: How is AI integrated?**
A: Araya (Claude API) via `/netlify/functions/araya-chat.js` - Trinity system in `/BACKEND/TRINITY_MISSION_CONTROL_API.py`

**Q: Where's the database schema?**
A: `/BACKEND/database_schema.sql` - 16 tables, PostgreSQL ready

**Q: What's missing?**
A: Real-time WebSocket server for multi-user collaboration - That's what you need to build!

**Q: How long to add collaboration?**
A: 2 weeks for basic real-time, 8 weeks for full featured system with AI

**Q: What's the architecture?**
A: Netlify frontend + Express.js backend + PostgreSQL database + Socket.IO for real-time

---

## HELPFUL COMMANDS

```bash
# Check Node dependencies
npm list @anthropic-ai/sdk

# List all Netlify functions
ls -la netlify/functions/

# Count files by type
find . -name "*.html" | wc -l
find . -name "*.js" | wc -l
find . -name "*.py" | wc -l

# Search for specific pattern
grep -r "websocket\|socket" --include="*.js" .

# Check git status
git status

# View recent commits
git log --oneline -10
```

---

**This is your roadmap. Start with the files listed in "Week 1-2" section and follow the COLLABORATION_WORKSPACE_ROADMAP.md for detailed implementation steps.**
