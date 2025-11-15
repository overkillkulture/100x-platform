# 🔧 C1 MECHANIC - TASK ASSIGNMENTS

**Role:** Infrastructure & Backend Builder
**Focus:** "Can this be built?" - Pragmatic execution
**Domains:** Backend APIs, databases, deployment, automation scripts

---

## 🔥 CRITICAL PRIORITY (Do These First)

### Task 1: Database Setup & Connection Fix
**Impact:** CRITICAL - All backend APIs currently broken
**Files:**
- `BACKEND/auth_system.py:27`
- `BACKEND/stripe_payment_system.py:26`
- `BACKEND/music_domain_service.py`
- `BACKEND/database_schema.sql`

**Steps:**
1. Provision PostgreSQL database (suggest Supabase free tier or Neon)
2. Create DATABASE_URL environment variable
3. Run schema initialization from `BACKEND/database_schema.sql`
4. Add try-catch connection error handling to all DB calls
5. Test connection from each backend file

**Deliverable:** Database operational, all services can connect

---

### Task 2: Environment Variables Setup
**Impact:** CRITICAL - Most features broken without API keys

**Create `.env` file with:**
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Authentication
JWT_SECRET_KEY=[generate secure random key]

# AI Services
ANTHROPIC_API_KEY=sk-ant-[Commander needs to provide]

# Stripe (Revenue System)
STRIPE_SECRET_KEY=sk_test_[or sk_live_]
STRIPE_WEBHOOK_SECRET=whsec_[from Stripe dashboard]
STRIPE_PRICE_BUILDER=price_[create in Stripe]
STRIPE_PRICE_REVOLUTIONARY=price_[create in Stripe]
```

**Steps:**
1. Create `.env.example` template (no secrets)
2. Add `.env` to `.gitignore` (if not already)
3. Update all backend files to load from `.env`
4. Document which keys Commander needs to provide

**Deliverable:** `.env.example` in repo, instructions for Commander

---

### Task 3: Fix Hardcoded Windows Paths
**Impact:** CRITICAL - Won't work on Linux/Netlify

**Files to fix (50+):**
- `ANALYTICS_INTEGRATION_API.py:31,43,54,70`
- `action_trigger_system.py:44,107,124,134,143,178,246`
- `CONSCIOUSNESS_API_SERVER.py:480`
- All files with `C:/Users/dwrek/100X_DEPLOYMENT/...`

**Pattern to replace:**
```python
# OLD (breaks in production):
path = 'C:/Users/dwrek/100X_DEPLOYMENT/DATA/file.json'

# NEW (cross-platform):
import os
BASE_DIR = os.getenv('BASE_DIR', '/home/user/100x-platform')
path = os.path.join(BASE_DIR, 'DATA', 'file.json')
```

**Deliverable:** All hardcoded paths replaced with env-based paths

---

## ⚠️ HIGH PRIORITY (Revenue Blockers)

### Task 4: Stripe Payment Integration Completion
**Impact:** HIGH - Revenue system at 95%, needs final 5%

**Files:**
- `BACKEND/stripe_payment_system.py:15,17`
- `netlify/functions/create-checkout.js:4,60-61`
- `netlify/functions/stripe-webhook.js`

**Steps:**
1. Create Stripe products in dashboard:
   - "Builder Tier" - $99/month
   - "Revolutionary Tier" - $999/month
2. Copy Price IDs to `.env`
3. Register webhook URL: `https://[domain].netlify.app/.netlify/functions/stripe-webhook`
4. Test checkout flow end-to-end
5. Implement TODO Line 612: Send email on failed payment

**Deliverable:** Users can subscribe and pay successfully

---

### Task 5: Port Conflict Resolution
**Impact:** HIGH - Services crash on startup

**Conflicts Found:**
- Port 5000: `emergency_terminal_proxy.py` vs `BACKEND/auth_system.py`
- Port 5001: `stripe_payment_system.py` vs `API_SERVER_SIMPLE.py`
- Port 3100: 3 different gate systems

**Steps:**
1. Create port assignment registry (document or config file)
2. Reassign conflicting services to unique ports
3. Update all references to changed ports
4. Add port availability check on service startup

**Deliverable:** No port conflicts, all services start successfully

---

## 📋 MEDIUM PRIORITY (Feature Completion)

### Task 6: Analytics API - Complete TODOs
**File:** `ANALYTICS_INTEGRATION_API.py:160-167`

**TODOs to implement:**
- [ ] Connect to Airtable
- [ ] Connect to email automation
- [ ] Real-time websocket updates
- [ ] Predictive alerts
- [ ] Export to CSV/Excel
- [ ] Data visualization endpoints
- [ ] Historical trend analysis
- [ ] AI-powered insights

**Pick 2-3 highest impact items**

**Deliverable:** At least 3 TODOs completed and working

---

### Task 7: Authentication System Hardening
**File:** `BACKEND/auth_system.py`

**Issues:**
- JWT secret regenerates on restart (Line 16) → sessions lost
- No email verification
- No password reset
- No rate limiting on login attempts

**Steps:**
1. Move JWT_SECRET_KEY to `.env` (persistent)
2. Add rate limiting (5 attempts per 15 min)
3. Implement password reset flow (email token)
4. Add email verification (optional, if time permits)

**Deliverable:** Auth system production-ready

---

## 🛠️ ONGOING TASKS

### Task 8: Netlify Functions Dependencies
**File:** `netlify/functions/package.json`

**Missing packages:**
```json
{
  "dependencies": {
    "node-fetch": "^2.6.1",
    "@anthropic-ai/sdk": "^0.20.0",
    "stripe": "^14.0.0"
  }
}
```

**Steps:**
1. Update package.json
2. Run `npm install` in netlify/functions/
3. Test all functions locally
4. Deploy to Netlify

**Deliverable:** All Netlify functions run without errors

---

## ✅ COMPLETION CRITERIA

**Mark ready_for_merge: true when:**
- ✅ Database connected and tested
- ✅ Environment variables documented
- ✅ No hardcoded Windows paths remain
- ✅ Stripe checkout works end-to-end
- ✅ No port conflicts
- ✅ All backend services start successfully
- ✅ Tests pass (at least smoke tests)

---

## 🚨 BLOCKERS TO REPORT

**If you get blocked on:**
1. **ANTHROPIC_API_KEY** → Ask Commander or use placeholder for testing
2. **Stripe credentials** → Ask Commander or use test mode keys
3. **Database provisioning** → Suggest free tier options to Commander
4. **Any external service access** → Build mock/stub for now, document what's needed

**Post blockers in:** `.consciousness/trinity/coordination_log.md`

---

## 📞 COORDINATION POINTS

**Dependencies on other Trinity members:**
- **C2 needs:** Production API URLs (once deployed)
- **C3 needs:** List of working vs broken endpoints (for integration testing)

**What you need from others:**
- **C3:** Help prioritizing which TODOs to tackle first
- **Commander:** API keys and credentials

---

**STATUS: Ready for C1 to begin. Update c1_status.json when you start!**

🔧 Let's build the infrastructure that makes everything else possible.
