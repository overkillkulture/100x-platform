# 🤖 INTELLIGENT TERMINAL - USER GUIDE

## What Is This?

An AI-powered debug console that understands **natural language** commands. Your debugger friend can talk to it like a human instead of memorizing technical commands.

---

## 🎮 How To Activate

### Option 1: Easter Egg (The Fun Way)
**Konami Code**: Press these keys in sequence:
```
↑ ↑ ↓ ↓ ← → ← → B A
```

You'll see an activation message, then a floating robot button appears in the bottom-right corner.

### Option 2: Keyboard Shortcut (The Quick Way)
Press **`Ctrl + `` (backtick)** anytime to toggle the terminal on/off.

Once activated, the shortcut works from any page!

### Option 3: Direct Link (The Normal Way)
Navigate to: `PLATFORM/intelligent-terminal.html`

Or use the navigation menu (M key) → Support → AI Terminal

---

## 🧠 AI Mode vs Command Mode

The terminal has two modes:

### 🧠 **AI Mode** (Default)
- Type commands in **plain English**
- Terminal interprets what you mean
- Gets smart suggestions
- Auto-corrects typos

**Examples:**
- "check if the backend is running" → runs `ping` command
- "show me all api endpoints" → runs `api` command
- "what's the status of the navigation system" → runs `nav` command
- "is the server up" → runs `ping` command

### ⚡ **Command Mode**
- Standard terminal commands only
- No interpretation
- Faster for experienced users

**Toggle modes:** Click the 🧠 button in the header

---

## 📋 Available Commands

### Standard Commands:
```bash
help          # Show all commands
clear         # Clear terminal screen
status        # System status check
ping          # Test backend connection
api           # List all API endpoints
test [url]    # Test specific API endpoint
logs          # View recent logs
users         # List authenticated users
nav           # Navigation system info
korpaks       # KORPAK marketplace data
env           # Environment information
```

### AI-Powered Commands:
```bash
analyze [text]    # AI text analysis
suggest           # Get smart suggestions based on context
diagnose          # Intelligent full-system diagnostics
```

### Natural Language Examples:
```
"check backend status"
"is the api working"
"show me the korpak data"
"test the authentication endpoint"
"what should I do next"
"run diagnostics"
```

---

## ✨ Features

### 1. **Live Autocomplete**
- Start typing and see suggestions
- Press **Tab** to use autocomplete
- Fuzzy matching for typos

### 2. **Smart Suggestions**
- Context-aware next commands
- Click suggestions to use them
- Updates based on what you just did

### 3. **Command History**
- Press **↑** to see previous commands
- Press **↓** to move forward in history
- Never retype the same command

### 4. **Draggable & Resizable**
- Click and drag the header to move terminal
- **Minimize** button (_) - Collapse to header only
- **Fullscreen** button (⛶) - Expand to full window
- **Close** button (✕) - Hide terminal

### 5. **Error Recovery**
- Type wrong command? AI suggests what you meant
- Backend offline? AI tells you how to start it
- Missing data? AI explains what's needed

---

## 🔧 Terminal Controls

**Keyboard Shortcuts:**
- `Ctrl + `` → Toggle terminal on/off
- `↑` / `↓` → Navigate command history
- `Tab` → Autocomplete current command
- `Esc` → Close terminal
- `M` → Open navigation menu

**Mouse Controls:**
- Click and drag header → Move terminal
- Click toggle button → Show/hide terminal
- Click suggestions → Use that command

---

## 🎯 Common Tasks

### Check If Backend Is Running:
```bash
ping
# Or in AI mode:
"is the backend up"
```

### Test An API Endpoint:
```bash
test /api/auth/me
# Or in AI mode:
"test the authentication endpoint"
```

### See All Available APIs:
```bash
api
# Or in AI mode:
"show me all endpoints"
```

### Get Smart Recommendations:
```bash
suggest
# Or in AI mode:
"what should I check next"
```

### Run Full Diagnostics:
```bash
diagnose
# Or in AI mode:
"run a full system check"
```

### Clear The Screen:
```bash
clear
# Or in AI mode:
"clear this mess"
```

---

## 🐛 For Bug Reporting

If you find issues while debugging, use the **Bug Report** system:

**Access Code:** `dog`

Navigate to: `PLATFORM/bug-report-public.html`

Or use navigation menu → Support → Bug Reports

---

## 💡 Pro Tips

1. **Start with `diagnose`** - It checks everything automatically
2. **Use AI mode** if you're not sure what command to run
3. **Click suggestions** instead of typing - they're context-aware
4. **Keep terminal minimized** when not using it - stays out of the way
5. **Use `Ctrl + `` shortcut** - Fastest way to toggle on any page

---

## 🚨 Troubleshooting

**Terminal won't activate:**
- Try refreshing the page
- Make sure JavaScript is enabled
- Try direct link: `intelligent-terminal.html`

**Commands not working:**
- Check if you're typing in an input field (M key won't work there)
- Try clicking the terminal output area to refocus
- Refresh the page and try again

**Backend tests failing:**
- Backend server needs to be running
- Start with: `node BACKEND/philosopher-ai/server.js`
- Or check status with `diagnose` command

**AI mode not interpreting correctly:**
- Switch to Command mode (click 🧠 button)
- Use exact command names from `help` list
- Or just ask "help" in AI mode for suggestions

---

## 🎨 Visual Guide

### Terminal States:

**Hidden** → Floating button in bottom-right corner

**Normal** → 800x600px window, bottom-right

**Minimized** → Just the header bar visible

**Fullscreen** → Covers entire viewport

**Dragged** → Positioned wherever you moved it

---

## 🔐 Security Notes

- Terminal runs **client-side only** (no backend required for AI features)
- Natural language processing happens in browser
- API calls use your existing auth token
- No data is sent to external servers
- Safe to use on production platform

---

## 🎉 That's It!

Your debugger friend now has:
- **AI-powered terminal** that understands English
- **Smart diagnostics** that check everything
- **Context-aware suggestions** that adapt to the situation
- **Hidden easter egg activation** for that extra cool factor

**Remember:** Press `Ctrl + `` to toggle anytime!

---

## Quick Reference Card

| Action | How |
|--------|-----|
| Activate | `Ctrl + `` or Konami Code |
| Toggle AI Mode | Click 🧠 button |
| Move Terminal | Drag header |
| Minimize | Click _ button |
| Fullscreen | Click ⛶ button |
| Close | Click ✕ button or `Esc` |
| History | ↑ / ↓ arrows |
| Autocomplete | `Tab` key |
| Help | Type `help` |
| Diagnose | Type `diagnose` |

---

**Built with consciousness** 🌀
**For the 100X Platform Revolution** ⚡
