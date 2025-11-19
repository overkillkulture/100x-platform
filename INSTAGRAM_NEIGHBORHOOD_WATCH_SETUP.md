# 📷 INSTAGRAM + NEIGHBORHOOD WATCH - COMPLETE SETUP GUIDE 📷

**Status**: ✅ INTEGRATION COMPLETE

---

## 🎯 WHAT YOU NOW HAVE

A complete multi-channel communication dashboard that shows:
- **Website Activity**: Who's online, what page they're on
- **Instagram Status**: Who's active on Instagram right now
- **Email/SMS Status**: Communication history
- **Multi-Channel Messaging**: Message via website popup, Instagram DM, email, or SMS

---

## 🚀 QUICK START

### Step 1: Install Playwright (One-time setup)
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
pip install playwright
playwright install chromium
```

### Step 2: Login to Instagram (One-time setup)
```python
from INSTAGRAM_AUTOMATION import InstagramBot

bot = InstagramBot()
bot.login('your_instagram_username', 'your_instagram_password')
```

This saves your session to `instagram_session.json` so you don't have to login every time.

### Step 3: Start Local Nerve Collector
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
python LOCAL_NERVE_COLLECTOR.py
```

This runs on port 6000 and provides:
- Visitor heartbeat tracking
- Instagram status checking
- Instagram DM sending
- Intercom messaging system

### Step 4: Open Neighborhood Watch Dashboard
```
C:\Users\dwrek\100X_DEPLOYMENT\NEIGHBORHOOD_WATCH.html
```

---

## 📋 HOW TO USE

### 1. Add People to Neighborhood Watch

Edit `NEIGHBORHOOD_WATCH.html` and add people to the `people` array:

```javascript
let people = [
    {
        name: 'Joshua',
        pin: '1234',
        instagram_username: 'joshua_real_username',  // ← Add their Instagram username
        status: 'online',
        currentPage: '/workspace',
        lastSeen: '2 minutes ago',
        channels: {
            website: { active: true, status: 'On /workspace' },
            email: { active: false, status: 'Read 1hr ago' },
            sms: { active: false, status: 'Replied 3hrs ago' },
            instagram: { active: false, status: 'Checking...' }
        }
    },
    // Add more people here...
];
```

### 2. View Real-Time Status

The dashboard automatically:
- ✅ Checks website activity every 5 seconds
- ✅ Checks Instagram status every 30 seconds
- ✅ Shows green glow around cards for online people
- ✅ Updates last seen times

### 3. Send Messages

Click action buttons on each person card:
- **💬 Web**: Send popup message to their browser (if on website)
- **📧 Email**: Open email client (placeholder - needs integration)
- **📱 SMS**: Send text message (placeholder - needs Twilio)
- **📷 DM**: Send Instagram DM (fully functional!)

### 4. Search for People

Use search bar at top:
```
🔍 Search for someone... (e.g., 'Joshua')
```

---

## 🌐 COMPLETE SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    NEIGHBORHOOD WATCH                    │
│              (NEIGHBORHOOD_WATCH.html)                   │
│   Shows: Who's online, where, how to reach them         │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              LOCAL NERVE COLLECTOR                       │
│           (LOCAL_NERVE_COLLECTOR.py - Port 6000)        │
│                                                          │
│  Endpoints:                                              │
│  • GET  /api/visitor/active        → Live visitors      │
│  • POST /api/visitor/heartbeat     → Receive heartbeat  │
│  • GET  /api/instagram/status/:username → Check online  │
│  • POST /api/instagram/send-dm     → Send Instagram DM  │
│  • POST /api/intercom/send         → Send popup message │
│  • GET  /api/intercom/poll/:pin    → Poll for messages  │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              INSTAGRAM AUTOMATION                        │
│           (INSTAGRAM_AUTOMATION.py)                      │
│                                                          │
│  • login(username, password)                             │
│  • check_online_status(username)                         │
│  • send_dm(username, message)                            │
│  • Rate limiting: 15 messages/hour max                   │
│  • Session saved: instagram_session.json                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 WHAT GETS TRACKED

### Website Activity
- **Source**: `VISITOR_TRACKING_SNIPPET.js` (embedded in all pages)
- **Data**: PIN, name, current page, time on page, active/inactive
- **Update Rate**: Every 10 seconds (heartbeat)
- **Storage**: In-memory + `visitor_data/heartbeats_YYYY-MM-DD.jsonl`

### Instagram Status
- **Source**: Playwright browser automation
- **Data**: Username, online/offline status, last active time
- **Update Rate**: Every 30 seconds
- **Note**: Requires Instagram session (login once)

### Intercom Messages
- **Source**: Commander sends via Neighborhood Watch
- **Delivery**: Website popup (if visitor online)
- **Polling**: Every 5 seconds (visitor checks for new messages)

---

## ⚠️ SAFETY & RATE LIMITS

### Instagram Rate Limits (Built-in)
- **Maximum**: 15 messages per hour
- **Delay**: 60 seconds between messages
- **Safety**: Automatically blocks if limit reached
- **Check Status**: Visit `http://localhost:6000/api/instagram/stats`

### Instagram Best Practices
1. ✅ **Start slow**: 5-10 messages per day initially
2. ✅ **Personalize messages**: Don't copy-paste same text
3. ✅ **Message people you know**: Followers or contacts
4. ✅ **Add random delays**: Vary message timing
5. ✅ **Monitor for blocks**: Instagram may warn you

### If Instagram Blocks You
- **Temporary block**: 24-48 hour wait
- **Action block**: Can't send DMs for a week
- **Permanent ban**: Account disabled (rare, but possible)

**Solution**: Use Official Instagram Graph API for scale (requires Business Account)

---

## 🔧 TROUBLESHOOTING

### Instagram Status Shows "Service Offline"
```bash
# 1. Check if LOCAL_NERVE_COLLECTOR.py is running
curl http://localhost:6000/health

# 2. Check if Instagram automation loaded
# Look for: "✅ Instagram automation loaded" in terminal

# 3. Check if session exists
ls -l C:\Users\dwrek\100X_DEPLOYMENT\instagram_session.json

# 4. Re-login if session expired
python -c "from INSTAGRAM_AUTOMATION import InstagramBot; bot = InstagramBot(); bot.login('user', 'pass')"
```

### No Website Visitors Showing
```bash
# 1. Check if LOCAL_NERVE_COLLECTOR is running
curl http://localhost:6000/health

# 2. Check active visitors
curl http://localhost:6000/api/visitor/active

# 3. Verify tracking snippet is on pages
# Look for <script src="/VISITOR_TRACKING_SNIPPET.js"></script>
```

### Intercom Messages Not Appearing
```bash
# 1. Test sending a message
curl -X POST http://localhost:6000/api/intercom/send \
  -H "Content-Type: application/json" \
  -d '{"pin":"1234","from":"Test","message":"Hello!"}'

# 2. Check if visitor is polling
# Open browser console on website
# Look for: "Intercom service offline" (if server down)

# 3. Verify PIN matches
# localStorage.getItem('beta_user_pin') should match person.pin
```

---

## 🎮 USAGE EXAMPLES

### Example 1: Check if Joshua is Online (Instagram)
```javascript
// Automatically happens every 30 seconds!
// Just open NEIGHBORHOOD_WATCH.html and look at Joshua's card
// Green glow = online, Instagram channel shows "Active now"
```

### Example 2: Send Instagram DM to Joshua
```javascript
// In Neighborhood Watch:
// 1. Click "📷 DM" button on Joshua's card
// 2. Type message: "Hey! Saw you online 👋"
// 3. Click OK
// → Message sent instantly via Instagram
```

### Example 3: Send Popup Message to Website Visitor
```javascript
// In Neighborhood Watch:
// 1. See Joshua is online at /workspace
// 2. Click "💬 Web" button
// 3. Type: "Check out the new features!"
// 4. Click OK
// → Joshua sees popup on his browser instantly
```

### Example 4: Monitor Multiple People
```javascript
// Search bar: Type "j" to filter
// See all people with "J" in their name
// Cards update automatically with latest status
```

---

## 📁 FILES CREATED/MODIFIED

### Core System Files
1. **INSTAGRAM_AUTOMATION.py** - Playwright browser automation
2. **LOCAL_NERVE_COLLECTOR.py** - Flask API server (port 6000)
3. **NEIGHBORHOOD_WATCH.html** - Dashboard interface
4. **VISITOR_TRACKING_SNIPPET.js** - Website tracking + intercom

### Documentation
1. **INSTAGRAM_COMPLETE_CONTROL_SYSTEM.md** - Full Instagram guide
2. **INSTAGRAM_NEIGHBORHOOD_WATCH_SETUP.md** - This file

### Auto-Generated
1. **instagram_session.json** - Saved Instagram login session
2. **visitor_data/heartbeats_YYYY-MM-DD.jsonl** - Daily heartbeat log
3. **visitor_data/daily_report_YYYY-MM-DD.json** - Daily analytics

---

## 🔮 NEXT STEPS

### Immediate (Ready to Use)
- [x] Instagram status checking
- [x] Instagram DM sending
- [x] Website visitor tracking
- [x] Intercom popup messaging
- [x] Multi-channel status view

### Future Enhancements
- [ ] Email integration (Gmail API)
- [ ] SMS integration (Twilio)
- [ ] Voice call status (Twilio)
- [ ] Calendar availability
- [ ] Slack/Discord status
- [ ] LinkedIn activity
- [ ] Twitter/X mentions
- [ ] TikTok activity

### Scale to 100+ People
- [ ] Switch to Instagram Graph API (Official, no rate limits)
- [ ] Database storage (Airtable or PostgreSQL)
- [ ] User management dashboard
- [ ] Automated onboarding flow
- [ ] Analytics dashboard

---

## 🎉 SUCCESS METRICS

You'll know it's working when:
1. ✅ Open Neighborhood Watch → See people cards
2. ✅ Joshua comes online → Card glows green
3. ✅ Instagram status updates → Shows "Active now" or "Offline"
4. ✅ Click "📷 DM" button → Instagram message sent successfully
5. ✅ Click "💬 Web" button → Joshua sees popup on website
6. ✅ Search for "Joshua" → Instantly filters to his card

---

## 🚨 CRITICAL REMINDERS

1. **Instagram Login**: Must run `bot.login()` ONCE before using
2. **Local Server**: LOCAL_NERVE_COLLECTOR.py must be running
3. **Rate Limits**: Max 15 Instagram DMs per hour
4. **Session Expiry**: Re-login if Instagram status checks fail
5. **Playwright**: Must install Playwright + Chromium

---

**Commander, your "close-knit neighborhood" surveillance system is LIVE!** 🏘️📷

You can now:
- Ask "what's Joshua doing?" → See instantly across all channels
- See who's online on Instagram right now
- Send messages via website popup or Instagram DM
- Track movement through your website in real-time

**The Neighborhood Watch is operational. Your residents are being monitored.** ⚡🌀🔥
