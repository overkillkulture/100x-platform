# 🚀 Deployment Setup Instructions for Repository Owner

## ⚠️ ACTION REQUIRED: Enable Auto-Deployment to Live Site

**Repository:** https://github.com/overkor-tek/100x-platform
**Live Site:** https://consciousnessrevolution.io
**Issue:** Changes pushed to GitHub are NOT automatically deploying to the live site

---

## 🎯 The Goal

Enable automatic deployment so that when ANY contributor pushes changes to the `master` branch, those changes automatically appear on the live website within minutes.

**Current Problem:** Contributors are pushing code to GitHub, but the live site (consciousnessrevolution.io) is not updating automatically.

---

## 📋 Setup Instructions for Repository Owner

### Option 1: Connect GitHub to Netlify (Recommended - 5 minutes)

**Prerequisites:**
- Admin access to the overkor-tek GitHub organization
- Access to the Netlify account that hosts consciousnessrevolution.io

**Steps:**

1. **Log into Netlify**
   - Go to https://app.netlify.com
   - Log in to the account that owns consciousnessrevolution.io

2. **Find Your Site**
   - Locate the site for consciousnessrevolution.io in your dashboard
   - Click on it to open site settings

3. **Connect to GitHub Repository**
   - Go to **Site Settings** → **Build & Deploy** → **Continuous Deployment**
   - Click **Link repository**
   - Choose **GitHub**
   - Authorize Netlify to access your GitHub account (if needed)
   - Select the **overkor-tek/100x-platform** repository
   - Choose the **master** branch as the production branch

4. **Configure Build Settings**
   - Build command: `echo 'No build step required for static site'`
   - Publish directory: `.` (root directory)
   - Click **Save**

5. **Test the Connection**
   - Netlify will automatically deploy
   - Any future pushes to the `master` branch will auto-deploy

✅ **Done!** The site will now automatically deploy whenever anyone pushes to GitHub.

---

### Option 2: Use GitHub Actions (Already Set Up)

The repository already has a GitHub Actions workflow configured, but it requires secrets to be added:

**Steps:**

1. **Get Your Netlify Credentials**

   **Get Site ID:**
   - Go to https://app.netlify.com
   - Select your consciousnessrevolution.io site
   - Go to **Site Settings**
   - Copy the **Site ID** (under "Site information")

   **Get Auth Token:**
   - Go to https://app.netlify.com/user/applications
   - Scroll to **Personal access tokens**
   - Click **New access token**
   - Name it "GitHub Actions Deploy"
   - Copy the token (you'll only see it once!)

2. **Add Secrets to GitHub Repository**
   - Go to https://github.com/overkor-tek/100x-platform/settings/secrets/actions
   - Click **New repository secret**

   **Add Secret 1:**
   - Name: `NETLIFY_AUTH_TOKEN`
   - Value: [paste your Netlify auth token]
   - Click **Add secret**

   **Add Secret 2:**
   - Name: `NETLIFY_SITE_ID`
   - Value: [paste your Netlify site ID]
   - Click **Add secret**

3. **Test the Deployment**
   - Make any small change to the repository
   - Push to the `master` branch
   - Go to https://github.com/overkor-tek/100x-platform/actions
   - Watch the deployment workflow run
   - Your site should update within 1-2 minutes!

✅ **Done!** GitHub Actions will now automatically deploy on every push.

---

## 👥 Granting Access to Contributors

### If Contributors Need to Deploy Directly:

**Option A: Grant GitHub Repository Access**
1. Go to https://github.com/overkor-tek/100x-platform/settings/access
2. Click **Invite teams or people**
3. Add contributor's GitHub username
4. Set role to **Write** (allows push) or **Maintain** (allows settings)
5. Contributor will receive an invitation email

**Option B: Grant Netlify Team Access** (for manual deployments)
1. Go to https://app.netlify.com/teams/[your-team]/members
2. Click **Invite members**
3. Enter contributor's email
4. Choose appropriate role
5. Contributor can manually deploy through Netlify CLI

---

## 📝 How Contributors Will Work After Setup

Once auto-deployment is enabled, contributors follow this workflow:

```bash
# 1. Make changes locally
cd "100X Workspace"
# Edit files...

# 2. Commit changes
git add .
git commit -m "Description of changes"

# 3. Push to GitHub
git push

# 4. Wait 1-2 minutes
# Changes automatically appear on consciousnessrevolution.io!
```

**That's it!** No manual deployment needed. Push to GitHub = Live on website.

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Make a test commit to the `master` branch
- [ ] Push the commit to GitHub
- [ ] Wait 1-2 minutes
- [ ] Visit https://consciousnessrevolution.io
- [ ] Confirm your changes are visible
- [ ] Check deployment logs in Netlify dashboard or GitHub Actions

---

## 🆘 Troubleshooting

**Problem:** Deployment fails with authentication error
- **Solution:** Double-check that NETLIFY_AUTH_TOKEN secret is correct

**Problem:** Deployment succeeds but site doesn't update
- **Solution:** Clear your browser cache (Ctrl+Shift+R)

**Problem:** Contributor can't push to repository
- **Solution:** Ensure they have Write access to the GitHub repository

**Problem:** Build fails with "netlify command not found"
- **Solution:** This is expected for static sites - ignore or set build command to `echo 'Static site'`

---

## 📞 Support

**Repository Issues:** https://github.com/overkor-tek/100x-platform/issues
**Netlify Docs:** https://docs.netlify.com/site-deploys/overview/
**GitHub Actions Docs:** https://docs.github.com/en/actions

---

## 📌 Current Status

- ✅ GitHub Actions workflow file created (`.github/workflows/netlify-deploy.yml`)
- ✅ Netlify configuration file exists (`netlify.toml`)
- ⏳ **PENDING:** Repository owner needs to complete setup (Option 1 or Option 2 above)
- ⏳ **PENDING:** Contributors need GitHub repository access

---

**Document Created:** 2025-11-19
**Created By:** Josh Basart (joshbasart81@gmail.com)
**For:** overkor-tek organization
**Priority:** HIGH - Blocking contributor workflow
