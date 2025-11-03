# PRODUCTION HOSTING SETUP - NETLIFY + RAILWAY

**Status:** Ready to deploy
**Frontend:** Netlify (static hosting)
**Backend:** Railway (API/services)

---

## NETLIFY CONFIGURATION (Frontend)

### Files Already Configured:
- `netlify.toml` (already exists)
- `_redirects` (already exists)
- `netlify/functions/` (serverless functions)

### Deployment Steps:
```bash
# 1. Install Netlify CLI (if not already installed)
npm install -g netlify-cli

# 2. Login to Netlify
netlify login

# 3. Link this project to Netlify site
netlify link

# 4. Deploy to production
netlify deploy --prod
```

### Netlify Sites Already Configured:
- **Main Site:** verdant-tulumba-fa2a5a.netlify.app
- **Custom Domain:** conciousnessrevolution.io (DNS already configured)

### Environment Variables (Netlify):
```bash
# Set via Netlify dashboard or CLI:
netlify env:set ANTHROPIC_API_KEY "your-key-here"
netlify env:set GITHUB_TOKEN "your-token-here"
netlify env:set AIRTABLE_TOKEN "your-token-here"
```

---

## RAILWAY CONFIGURATION (Backend APIs)

### What Goes on Railway:
1. Python backend APIs (Flask/FastAPI)
2. Database (PostgreSQL)
3. Background workers
4. Scheduled jobs

### Railway Setup:

#### 1. Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 2. Create `Procfile`:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4
worker: python background_worker.py
```

#### 3. Create `runtime.txt`:
```
python-3.11
```

#### 4. Create `requirements.txt`:
```
flask==3.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
anthropic==0.8.0
requests==2.31.0
python-dotenv==1.0.0
```

### Railway Deployment:
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Link to project
railway link

# 5. Add PostgreSQL database
railway add --database postgresql

# 6. Set environment variables
railway variables set ANTHROPIC_API_KEY="your-key"
railway variables set DATABASE_URL="auto-generated-by-railway"

# 7. Deploy
railway up
```

---

## ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  NETLIFY (Frontend)                          │
│  • Static HTML/CSS/JS                                        │
│  • Serverless Functions (lightweight API proxies)            │
│  • CDN (global edge network)                                 │
│  • Custom domain: conciousnessrevolution.io                  │
└────────────┬────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│                  RAILWAY (Backend)                           │
│  • Python Flask/FastAPI API                                  │
│  • PostgreSQL Database                                       │
│  • Background Workers                                        │
│  • Scheduled Jobs (cron)                                     │
│  • Environment: Production                                   │
└────────────┬────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│              EXTERNAL SERVICES                               │
│  • Anthropic API (Claude)                                    │
│  • GitHub API                                                │
│  • Airtable API                                              │
│  • Social Media APIs (Instagram, TikTok, YouTube)            │
│  • Stripe API (payments)                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## COST BREAKDOWN

### Netlify:
- **Free Tier:** 100GB bandwidth, 300 build minutes/month
- **Pro Tier:** $19/month (1TB bandwidth, 400 build minutes)
- **Recommendation:** Start with Free, upgrade at 50+ users

### Railway:
- **Free Tier:** $5 credit/month, egress fees
- **Hobby Plan:** $5/month base + usage
- **Pro Plan:** $20/month base + usage
- **Recommendation:** Hobby plan ($10-20/month total)

### Total Estimated Cost:
- **Month 1:** $0-5 (free tiers)
- **Month 3:** $20-30 (Netlify Free + Railway Hobby)
- **Month 6:** $40-60 (Netlify Pro + Railway Pro)

---

## DEPLOYMENT CHECKLIST

### Netlify (Frontend):
- [x] netlify.toml configured
- [x] _redirects configured
- [x] Serverless functions in netlify/functions/
- [x] Custom domain DNS configured
- [ ] Environment variables set
- [ ] Deploy to production
- [ ] Verify custom domain working
- [ ] Test all pages load correctly

### Railway (Backend):
- [ ] Create Railway project
- [ ] Add PostgreSQL database
- [ ] Configure environment variables
- [ ] Deploy API service
- [ ] Configure custom domain (api.conciousnessrevolution.io)
- [ ] Test health endpoint (/health)
- [ ] Test API endpoints
- [ ] Setup monitoring/logs

---

## QUICK DEPLOY COMMANDS

### Deploy Everything:
```bash
# Frontend (Netlify)
cd /c/Users/dwrek/100X_DEPLOYMENT
netlify deploy --prod

# Backend (Railway) - coming after backend API is built
railway up
```

### Rollback if Needed:
```bash
# Netlify - rollback to previous deploy
netlify rollback

# Railway - rollback to previous deploy
railway rollback
```

---

## MONITORING & HEALTH CHECKS

### Netlify:
- **Dashboard:** https://app.netlify.com
- **Build logs:** Real-time in dashboard
- **Analytics:** Built-in (requests, bandwidth, forms)

### Railway:
- **Dashboard:** https://railway.app
- **Logs:** Real-time in dashboard
- **Metrics:** CPU, memory, network usage
- **Health endpoint:** api.conciousnessrevolution.io/health

### Uptime Monitoring (Recommended):
- **UptimeRobot** (free, 50 monitors)
- Check every 5 minutes
- Alert via email/SMS if down

---

## SECURITY BEST PRACTICES

1. **Environment Variables:**
   - NEVER commit API keys to git
   - Use Netlify/Railway dashboard to set secrets
   - Rotate keys every 90 days

2. **HTTPS:**
   - Netlify: Auto-enabled (Let's Encrypt)
   - Railway: Auto-enabled

3. **CORS:**
   - Configure allowed origins
   - Don't use wildcard (*) in production

4. **Rate Limiting:**
   - Netlify Functions: 125k requests/month free
   - Railway: Add rate limiting middleware

---

## CUSTOM DOMAIN SETUP

### conciousnessrevolution.io (Frontend):
Already configured in Namecheap DNS:
```
A Record: @ → 75.2.60.5 (Netlify)
CNAME: www → verdant-tulumba-fa2a5a.netlify.app
```

### api.conciousnessrevolution.io (Backend):
Add to Namecheap DNS after Railway deployment:
```
CNAME: api → [railway-generated-url]
```

---

## NEXT STEPS

1. **Immediate (5 min):**
   - Verify Netlify site is still deployed
   - Check DNS is resolving

2. **After Backend Built (1 hour):**
   - Deploy backend to Railway
   - Configure api subdomain
   - Test end-to-end flow

3. **Week 2 (Before Launch):**
   - Setup monitoring
   - Configure backups
   - Load testing
   - Security audit

---

**Status:** ✅ Configuration complete, ready for deployment
**Next Task:** Deploy frontend to Netlify (after Commander unblocks with environment variables)
