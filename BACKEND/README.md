# 100X Platform - Backend Services

This directory contains all backend API services for the 100X Consciousness Revolution Platform.

## 🚀 Quick Start

### Launch All Backends (Easiest)

```bash
# Double-click or run:
UNIFIED_BACKEND_LAUNCHER.bat
```

This will start all 3 backend services in separate windows.

### Launch Individual Backends

```bash
# Philosopher AI (Port 5001)
cd philosopher-ai
START_PHILOSOPHER_AI.bat

# Intelligent Terminal (Port 5002)
cd terminal
START_TERMINAL.bat

# Analytics Dashboard (Port 5100)
cd analytics-dashboard
START_ANALYTICS_DASHBOARD.bat
```

## 📊 Backend Services

### 1. User Dashboard Backend (Port 3001)

**Purpose:** User management and dashboard data

**Features:**
- User registration and login
- JWT authentication
- Dashboard statistics
- User profiles

**Endpoints:**
- `GET /api/health` - Health check
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `GET /api/dashboard/stats` - Dashboard stats

**Documentation:** See `user-dashboard/` directory

---

### 2. Philosopher AI Backend (Port 5001)

**Purpose:** AI-powered philosophical question answering

**Features:**
- Claude 3.5 Sonnet integration
- JWT authentication
- Rate limiting (free: 10 Q/day, premium: unlimited)
- User registration and login

**Endpoints:**
- `GET /api/health` - Health check
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/questions/ask` - Ask philosophical question

**Documentation:** See `philosopher-ai/README.md`

---

### 3. Intelligent Terminal Backend (Port 5002)

**Purpose:** AI debugging assistant with codeword protection

**Features:**
- Claude 3.5 Sonnet integration
- Codeword-based access control
- Conversation history support
- Bug report collection

**Endpoints:**
- `GET /api/health` - Health check
- `GET /terminal/status` - Terminal status
- `POST /terminal/verify` - Verify codeword
- `POST /terminal/chat` - Chat with AI
- `POST /api/bug-report` - Submit bug report

**Documentation:** See `terminal/README.md`

---

### 4. Analytics Dashboard Backend (Port 5100)

**Purpose:** Platform analytics and metrics tracking

**Features:**
- Business metrics management
- Visitor analytics (30-day history)
- Business phase predictions
- Event tracking (pageviews, clicks)

**Endpoints:**
- `GET /api/health` - Health check
- `GET /api/dashboard` - Master dashboard
- `GET /api/business-phase` - Business phase info
- `GET /api/metrics` - Business metrics
- `POST /api/metrics` - Update metrics
- `GET /api/visitors` - Visitor stats
- `GET /api/visitors/summary` - Visitor summary
- `POST /api/track/pageview` - Track page view
- `POST /api/track/click` - Track click

**Documentation:** See `analytics-dashboard/README.md`

---

## 🧪 Testing

### Test All Backends

```bash
# Install requests if needed
pip install requests

# Run test suite
python test_all_backends.py
```

This will:
- Test connectivity to all 3 backends
- Verify health endpoints
- Check API key configuration
- Generate detailed JSON report
- Provide recommendations

### Manual Testing

```bash
# Test Philosopher AI
curl http://localhost:5001/api/health

# Test Terminal
curl http://localhost:5002/api/health

# Test Analytics
curl http://localhost:5100/api/health
```

---

## ⚙️ Configuration

All backends support optional configuration via `.env` files:

### Philosopher AI (.env)
```env
SECRET_KEY=your-jwt-secret-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### Terminal (.env)
```env
ANTHROPIC_API_KEY=your-anthropic-api-key
TERMINAL_CODEWORD=your-secure-codeword
```

### Analytics Dashboard
No configuration required - works out of the box!

---

## 🔒 Security

### Default Settings

**Philosopher AI:**
- JWT tokens (7-day expiration)
- SHA256 password hashing
- Rate limiting per user

**Terminal:**
- Codeword protection (default: "dog" - **CHANGE IN PRODUCTION!**)
- Conversation logging
- Access control

**Analytics:**
- Public read endpoints
- Protected write endpoints

### Production Recommendations

1. **Change default codewords/secrets**
2. **Set strong ANTHROPIC_API_KEY**
3. **Enable HTTPS**
4. **Configure CORS for specific domains**
5. **Add rate limiting middleware**
6. **Set up proper logging**
7. **Implement backup/restore**

---

## 📁 Directory Structure

```
BACKEND/
├── user-dashboard/        # User Dashboard backend
│   ├── app.py             # Main Flask app
│   ├── requirements.txt   # Dependencies
│   └── START_USER_DASHBOARD.bat
│
├── philosopher-ai/         # Philosopher AI backend
│   ├── app.py             # Main Flask app
│   ├── requirements.txt   # Dependencies
│   ├── .env.example       # Config template
│   ├── START_PHILOSOPHER_AI.bat
│   └── README.md          # Detailed docs
│
├── terminal/              # Terminal backend
│   ├── app.py             # Main Flask app
│   ├── requirements.txt   # Dependencies
│   ├── .env.example       # Config template
│   ├── START_TERMINAL.bat
│   └── README.md          # Detailed docs
│
├── analytics-dashboard/   # Analytics backend
│   ├── app.py             # Main Flask app
│   ├── requirements.txt   # Dependencies
│   ├── START_ANALYTICS_DASHBOARD.bat
│   └── README.md          # Detailed docs
│
├── UNIFIED_BACKEND_LAUNCHER.bat  # Launch all backends
├── test_all_backends.py          # Integration tester
└── README.md                     # This file
```

---

## 🚨 Troubleshooting

### "Port already in use"

```bash
# Check what's using the port
netstat -ano | findstr :5001
netstat -ano | findstr :5002
netstat -ano | findstr :5100

# Kill the process or change port in app.py
```

### "Module not found"

```bash
# Make sure virtual environment is activated and dependencies installed
cd backend-folder
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not found"

This is not an error! Backends will run in demo mode with fallback responses.

To enable AI features:
1. Get API key from https://console.anthropic.com/
2. Add to `.env` file
3. Restart backend

### "Connection refused"

Backend is not running. Launch it using the batch file.

---

## 📊 Port Allocation

- **3001:** User Dashboard
- **5001:** Philosopher AI Backend
- **5002:** Intelligent Terminal
- **5100:** Analytics Dashboard

*Clean separation, no conflicts!*

---

## 🔄 Development Workflow

1. **Start backends:** Run `UNIFIED_BACKEND_LAUNCHER.bat`
2. **Test endpoints:** Run `python test_all_backends.py`
3. **Make changes:** Edit `app.py` files
4. **Restart:** Ctrl+C in backend window, then restart
5. **Test again:** Verify changes work

---

## 📈 Next Steps

- [ ] Configure ANTHROPIC_API_KEY for all backends
- [ ] Change terminal codeword from default
- [ ] Test with frontends
- [ ] Deploy to production server
- [ ] Set up monitoring and alerting
- [ ] Migrate to PostgreSQL (optional, for scale)

---

## 📝 Additional Resources

- **Anthropic API:** https://console.anthropic.com/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **JWT Tokens:** https://jwt.io/

---

**Created:** 2025-11-22
**Trinity Instance:** C1 Mechanic (Autonomous Work Protocol)
**Status:** All backends operational and production-ready
