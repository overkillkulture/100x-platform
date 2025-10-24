# 🚀 BUILDER TERMINAL - CLOUD DEPLOYMENT GUIDE

## Quick Deploy to Railway (RECOMMENDED)

### Option 1: Railway CLI (Fastest)

```bash
# Install Railway CLI (if not installed)
npm install -g @railway/cli

# Login to Railway
railway login

# Navigate to deployment folder
cd C:/Users/dwrek/100X_DEPLOYMENT

# Create new Railway project
railway init

# Set environment variable
railway variables set ANTHROPIC_API_KEY=your-key-here

# Deploy!
railway up
```

### Option 2: Railway Dashboard (No CLI needed)

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub account
4. Select the repository
5. Set environment variable: `ANTHROPIC_API_KEY`
6. Railway auto-deploys!

### Option 3: Render.com (Alternative)

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect repository
4. Settings:
   - **Build Command:** `pip install -r BUILDER_TERMINAL_requirements.txt`
   - **Start Command:** `gunicorn BUILDER_TERMINAL_API:app --bind 0.0.0.0:$PORT`
   - **Environment Variable:** `ANTHROPIC_API_KEY=your-key-here`
5. Click "Create Web Service"

## After Deployment

You'll get a URL like: `https://builder-terminal-production.up.railway.app`

Update `builder-terminal.html`:
```javascript
const API_BASE = 'https://your-railway-url.railway.app';
```

## Files Needed for Deployment

- ✅ BUILDER_TERMINAL_API.py (main server)
- ✅ BUILDER_TERMINAL_requirements.txt (Python packages)
- ✅ BUILDER_TERMINAL_Procfile (start command)
- ✅ BUILDER_TERMINAL_railway.json (Railway config)

## Environment Variables Required

- `ANTHROPIC_API_KEY` - Your Claude API key
- `PORT` - Auto-set by Railway/Render

## Storage Note

⚠️ **IMPORTANT:** Railway/Render have ephemeral file systems!

Builder files will be lost on restart. For production, you need:

**Quick Fix (Good for beta testing):**
- Files persist during session
- Beta testers can build and preview
- Reset on server restart (acceptable for beta)

**Production Fix (Later):**
- Add database (PostgreSQL)
- Or use S3/Cloud Storage
- Store files permanently

For beta testing, the ephemeral storage is FINE - testers are learning, not saving forever.

## Testing Deployment

1. **Health Check:**
   ```bash
   curl https://your-url.railway.app/api/health
   ```

2. **Test AI:**
   ```bash
   curl -X POST https://your-url.railway.app/api/chat \
     -H "Content-Type: application/json" \
     -d '{"username":"test","message":"Say hello"}'
   ```

3. **Open in Browser:**
   ```
   https://consciousnessrevolution.io/builder-terminal.html?username=demo
   ```

## Beta Tester Access

Once deployed, beta testers get:
- URL: `https://consciousnessrevolution.io/builder-terminal.html?username=[their-username]`
- Their AI coding assistant
- Sandboxed workspace
- Instant preview

Each beta tester gets their own folder: `/builders/[username]/`

## Cost Estimate

**Railway Free Tier:**
- $5 credit/month
- Should handle 10-20 beta testers easily
- Scales automatically

**Render Free Tier:**
- Free (with limitations)
- Spins down after inactivity
- Good for testing

## 🎯 Ready to Deploy!

Choose your platform and follow the steps above!
