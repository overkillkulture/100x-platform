# Netlify Auto-Deployment Setup Guide

## Overview
Your repository is now configured to automatically deploy to Netlify whenever you push changes to GitHub.

## Current Status
✅ GitHub Actions workflow created (`.github/workflows/netlify-deploy.yml`)
✅ Workflow pushed to GitHub repository
⏳ Pending: Add Netlify secrets to GitHub

## Setup Instructions

### Step 1: Get Your Netlify Site ID

1. Go to [Netlify Dashboard](https://app.netlify.com)
2. Select your site (consciousnessrevolution.io or 100x-platform)
3. Go to **Site Settings**
4. Under **Site Information**, copy the **Site ID** (looks like: `abc12345-6789-def0-1234-56789abcdef0`)

### Step 2: Get Your Netlify Auth Token

1. Go to [Netlify User Settings](https://app.netlify.com/user/applications)
2. Scroll down to **Personal access tokens**
3. Click **New access token**
4. Give it a name like "GitHub Actions Deploy"
5. Copy the generated token (you'll only see it once!)

### Step 3: Add Secrets to GitHub

1. Go to: https://github.com/overkor-tek/100x-platform/settings/secrets/actions
2. Click **New repository secret**
3. Add two secrets:

   **Secret 1:**
   - Name: `NETLIFY_AUTH_TOKEN`
   - Value: [paste your Netlify personal access token]

   **Secret 2:**
   - Name: `NETLIFY_SITE_ID`
   - Value: [paste your Netlify site ID]

### Step 4: Test the Deployment

After adding the secrets, make any small change and push it:

```bash
cd "100X Workspace"
echo "# Test deployment" >> README.md
git add README.md
git commit -m "Test auto-deployment"
git push
```

The GitHub Action will automatically trigger and deploy your site to Netlify!

## How It Works

1. **You push code** to the `master` or `main` branch
2. **GitHub Actions triggers** the workflow automatically
3. **Workflow deploys** your site to Netlify
4. **Netlify publishes** the changes live
5. **Your site updates** at consciousnessrevolution.io

## Monitoring Deployments

- **GitHub Actions**: https://github.com/overkor-tek/100x-platform/actions
- **Netlify Dashboard**: https://app.netlify.com

## Troubleshooting

If deployment fails:
1. Check GitHub Actions logs for errors
2. Verify secrets are correctly set
3. Ensure Netlify site is properly configured
4. Check Netlify build logs

## Benefits

✅ Automatic deployment on every push
✅ No manual Netlify CLI commands needed
✅ Preview deployments for pull requests
✅ Deployment status in GitHub commits
✅ Faster iteration and updates

---

**Created:** 2025-11-19
**Status:** Ready for secret configuration
