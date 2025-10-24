# 🚀 QUICK DEPLOY - Builder Terminal to Railway

## Network Issue Fix - Use GitHub Deployment

Railway CLI is timing out. Use GitHub deployment instead (takes 2 minutes):

### Step 1: Push to GitHub

```bash
cd C:/Users/dwrek/100X_DEPLOYMENT/builder-terminal-deploy

# Add GitHub remote (create repo first at github.com/new)
git remote add origin https://github.com/YOUR-USERNAME/builder-terminal.git

# Push
git push -u origin master
```

### Step 2: Deploy via Railway Dashboard

1. Go to https://railway.com/project/ba4ad921-3553-43a0-8064-3b01f27e7a87
2. Click "+ New Service"
3. Select "GitHub Repo"
4. Choose the `builder-terminal` repository
5. Railway auto-detects Python and deploys!

### Step 3: Add Environment Variable

1. In Railway dashboard, click on the service
2. Go to "Variables" tab
3. Add: `ANTHROPIC_API_KEY` = `[your Claude API key]`
4. Service auto-restarts with the key

### Step 4: Get Your URL

Railway gives you a URL like:
```
https://builder-terminal-production.up.railway.app
```

Copy that URL!

### Step 5: Update HTML File

Edit `builder-terminal.html` line ~234:

```javascript
// Change from:
const API_BASE = 'http://localhost:8003';

// To:
const API_BASE = 'https://builder-terminal-production.up.railway.app';
```

### Step 6: Deploy HTML to Netlify

```bash
cd C:/Users/dwrek/100X_DEPLOYMENT
netlify deploy --prod
```

## 🎯 Done!

Beta testers can now access:
```
https://consciousnessrevolution.io/builder-terminal.html?username=[their-name]
```

Each gets their own AI coding assistant!

## Alternative: Super Quick Deploy (No GitHub)

If you want to skip GitHub, use Render.com instead:

1. Go to https://render.com/deploy
2. Click "New +" → "Web Service"
3. Choose "Deploy without Git"
4. Upload the files from `builder-terminal-deploy` folder
5. Set environment variable
6. Deploy!

Render gives you a URL instantly.

## Files Ready in:
`C:/Users/dwrek/100X_DEPLOYMENT/builder-terminal-deploy/`

- ✅ BUILDER_TERMINAL_API.py
- ✅ requirements.txt
- ✅ Procfile
- ✅ runtime.txt
- ✅ Git initialized and committed

All ready to push to GitHub!
