# 🚂 RAILWAY AUTOMATIC DEPLOYMENT SETUP

**Goal:** Automatic deployment to Railway on every git push

---

## 🎯 SETUP STEPS

### **Step 1: Connect Railway to GitHub**

1. Go to https://railway.app/
2. Login (or create account if needed)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Authorize Railway to access your GitHub account
6. Select repository: `overkillculture/100x-platform`
7. Select branch: `claude/new-environment-setup-011CUbzCDVryyJUYeqJ4sd9p` (or `main` for production)

**Railway will now auto-detect your Node.js app and configure it automatically.**

---

### **Step 2: Configure Environment Variables**

In Railway dashboard:

1. Click on your project
2. Go to "Variables" tab
3. Add these environment variables:

```env
# Required
NODE_ENV=production
PORT=3100

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://... (Railway will auto-generate)

# Redis (if using)
REDIS_URL=redis://... (Railway will auto-generate)

# Session Secret
SESSION_SECRET=your-super-secret-key-here-change-this

# Anthropic API (for Trinity AI)
ANTHROPIC_API_KEY=your-anthropic-api-key

# Optional: Custom Domain
RAILWAY_PUBLIC_DOMAIN=your-custom-domain.com
```

---

### **Step 3: Configure Build Settings**

Railway should auto-detect these, but verify:

**Build Command:**
```bash
npm install
```

**Start Command:**
```bash
npm start
```

**Root Directory:**
```
/
```

**If you need to customize, go to Settings > Build:**
- Build Command: `npm run build` (if you have a build step)
- Start Command: `node server.js` or `npm start`

---

### **Step 4: Add railway.json (Optional but Recommended)**

Create this file in your repo root:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "npm start",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

This ensures consistent deployment configuration.

---

### **Step 5: Verify Auto-Deploy is Enabled**

In Railway dashboard:

1. Go to your project settings
2. Find "Deployments" section
3. Ensure "Auto-deploy" is toggled **ON**
4. Set trigger: "Deploy on push to branch: [your-branch-name]"

**Now Railway will auto-deploy every time you push to that branch!**

---

## 🔄 HOW IT WORKS

### **Deployment Flow:**
```
1. You run: git push origin claude/new-environment-setup-011CUbzCDVryyJUYeqJ4sd9p
   ↓
2. GitHub webhook notifies Railway
   ↓
3. Railway pulls latest code
   ↓
4. Railway runs: npm install
   ↓
5. Railway runs: npm start
   ↓
6. New version is live at: https://your-app.up.railway.app
   ↓
7. Old version is automatically replaced (zero-downtime deploy)
```

---

## 🚀 TESTING THE AUTO-DEPLOY

### **Test Deployment:**

1. Make a small change to your code:
```bash
# Add a comment to server.js
echo "// Test deploy" >> server.js
```

2. Commit and push:
```bash
git add server.js
git commit -m "Test: Railway auto-deploy"
git push origin claude/new-environment-setup-011CUbzCDVryyJUYeqJ4sd9p
```

3. Watch Railway dashboard:
   - You'll see "Building..." status
   - Then "Deploying..."
   - Then "Active" with new deployment ID

4. Visit your Railway URL to confirm changes are live

---

## 📊 MONITORING DEPLOYMENTS

### **Railway Dashboard Shows:**
- ✅ Deployment status (Building, Active, Failed)
- ✅ Build logs (see what's happening during deploy)
- ✅ Runtime logs (see your app's console.log output)
- ✅ Metrics (CPU, memory, network usage)
- ✅ Deployment history (rollback to any previous version)

### **Accessing Logs:**
1. Click on your project
2. Click "Deployments" tab
3. Click on any deployment to see logs
4. Or use Railway CLI: `railway logs`

---

## 🛠️ RAILWAY CLI (Optional but Powerful)

### **Install Railway CLI:**
```bash
npm i -g @railway/cli
```

### **Login:**
```bash
railway login
```

### **Link to Your Project:**
```bash
cd /path/to/100x-platform
railway link
```

### **Useful CLI Commands:**
```bash
# Deploy manually (bypasses git)
railway up

# View logs in real-time
railway logs

# Open dashboard in browser
railway open

# Run commands in Railway environment
railway run node server.js

# Check deployment status
railway status
```

---

## 🔧 TROUBLESHOOTING

### **Problem: Build Fails**
**Solution:** Check build logs in Railway dashboard
- Common issue: Missing dependencies in package.json
- Fix: Add missing packages and push again

### **Problem: App Crashes After Deploy**
**Solution:** Check runtime logs
- Common issue: Missing environment variables
- Fix: Add missing vars in Railway dashboard

### **Problem: Database Connection Issues**
**Solution:** Railway's DATABASE_URL format might differ
- Check Railway's auto-generated DATABASE_URL
- Update your database connection code if needed

### **Problem: Port Binding Issues**
**Solution:** Railway assigns a random port
```javascript
// server.js - Make sure you use Railway's PORT
const PORT = process.env.PORT || 3100;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### **Problem: Auto-Deploy Not Triggering**
**Solution:**
1. Check Railway webhook status in GitHub repo settings
2. Go to: github.com/overkillculture/100x-platform/settings/hooks
3. Find Railway webhook, ensure it's green (not red)
4. If red, re-authorize Railway's GitHub access

---

## 🎨 CUSTOM DOMAIN (Optional)

### **Add Your Own Domain:**

1. In Railway dashboard, go to Settings
2. Click "Networking" or "Domains"
3. Click "Add Domain"
4. Enter your domain: `platform.yourdomain.com`
5. Railway provides DNS records:
   ```
   Type: CNAME
   Name: platform
   Value: your-app.up.railway.app
   ```
6. Add these records to your domain registrar (GoDaddy, Namecheap, etc.)
7. Wait for DNS propagation (5-60 minutes)
8. Railway will auto-provision SSL certificate (HTTPS)

---

## 💰 PRICING

**Railway Free Tier:**
- $5 free credit per month
- Pay only for usage beyond that
- Typical Node.js app: ~$5-15/month

**What Uses Credits:**
- CPU time
- Memory usage
- Network bandwidth
- Database storage (PostgreSQL/Redis)

**Monitoring Usage:**
Check "Usage" tab in Railway dashboard to avoid surprises.

---

## 🚀 PRODUCTION CHECKLIST

Before going live with Genesis 10 users:

- [ ] Environment variables set (SESSION_SECRET, ANTHROPIC_API_KEY)
- [ ] Database connected (PostgreSQL or file-based)
- [ ] Auto-deploy enabled and tested
- [ ] Custom domain configured (optional but professional)
- [ ] SSL certificate active (Railway auto-provisions)
- [ ] Logs monitored (check for errors)
- [ ] Health check endpoint working (`/api/health` or similar)
- [ ] Error handling in place (don't expose stack traces)
- [ ] Rate limiting configured (prevent abuse)

---

## 🔄 DEPLOYMENT WORKFLOW (Day-to-Day)

### **Normal Development Flow:**

```bash
# 1. Work on your code
vim server.js  # or whatever editor

# 2. Test locally
npm start
# Visit http://localhost:3100

# 3. Commit changes
git add .
git commit -m "Add new feature: XYZ"

# 4. Push to GitHub
git push origin claude/new-environment-setup-011CUbzCDVryyJUYeqJ4sd9p

# 5. Railway automatically deploys!
# Check Railway dashboard to confirm

# 6. Visit production URL to verify
# https://your-app.up.railway.app
```

**That's it! No manual deployment steps needed.**

---

## 📱 RAILWAY MOBILE APP

Railway has a mobile app (iOS/Android) so you can:
- Monitor deployments on the go
- Check logs from your phone
- Get push notifications for deploy status
- Restart services if needed

**Download:** Search "Railway" in App Store or Google Play

---

## 🎯 NEXT STEPS

1. **Connect GitHub to Railway** (5 minutes)
2. **Set environment variables** (2 minutes)
3. **Test auto-deploy with dummy commit** (2 minutes)
4. **Share production URL with Genesis testers** (immediate)

**After setup, every git push = automatic deployment. Set it and forget it!** 🚀

---

**Railway Dashboard:** https://railway.app/dashboard
**Docs:** https://docs.railway.app/
**Support:** https://discord.gg/railway (Railway Discord - very responsive)

---

*This is the deployment pipeline that will support your Genesis 10 onboarding and scale to Genesis 100.* ⚡
