# 100X Platform - Complete Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Quick Start](#quick-start)
4. [Deployment Commands](#deployment-commands)
5. [Platform-Specific Guides](#platform-specific-guides)
6. [CI/CD Integration](#cicd-integration)
7. [Troubleshooting](#troubleshooting)
8. [Rollback Procedures](#rollback-procedures)
9. [Best Practices](#best-practices)
10. [FAQ](#faq)

---

## Prerequisites

### Required Software

Before deploying the 100X Platform, ensure you have the following installed:

- **Python 3.8+** - Backend services and deployment script
- **Node.js 18+** - Frontend and serverless functions
- **npm or yarn** - Package management
- **Git** - Version control
- **Platform CLI tools** (optional, installed automatically):
  - Vercel CLI
  - Netlify CLI
  - Railway CLI
  - Render CLI

### System Requirements

- **Operating System**: Linux, macOS, or Windows (with WSL2)
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 10GB free space
- **Internet Connection**: Stable connection for deployments

### Required Accounts

Create accounts on your chosen platforms:

1. **Vercel** - https://vercel.com (Frontend hosting)
2. **Netlify** - https://netlify.com (Alternative frontend hosting)
3. **Railway** - https://railway.app (Backend/API hosting)
4. **Render** - https://render.com (Alternative backend hosting)

### API Keys & Services

You'll need API keys for:

- **Anthropic Claude API** (Required)
- **Airtable** (Required)
- **Stripe** (Required for payments)
- **SendGrid** (Email notifications)
- **Twilio** (SMS notifications)
- **OpenAI** (Optional AI features)
- **GitHub** (CI/CD)

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/100x-platform.git
cd 100x-platform
```

### 2. Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `.env` and add your API keys:

```bash
# Required Variables
ANTHROPIC_API_KEY=your_anthropic_api_key_here
AIRTABLE_TOKEN=your_airtable_token_here
AIRTABLE_BASE_ID=your_airtable_base_id_here
STRIPE_SECRET_KEY=your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key_here

# Optional Variables
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
SENDGRID_API_KEY=your_sendgrid_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Install Dependencies

Install all project dependencies:

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Install backend dependencies
pip install -r BACKEND/requirements.txt
```

### 5. Verify Setup

Test your configuration:

```bash
python deploy.py --env development --test-only
```

---

## Quick Start

### Deploy to Development

```bash
python deploy.py --env development
```

### Deploy to Staging

```bash
python deploy.py --env staging --platform netlify
```

### Deploy to Production

```bash
python deploy.py --env production --platform vercel
```

### Dry Run (Test Without Deploying)

```bash
python deploy.py --env production --dry-run
```

---

## Deployment Commands

### Basic Deployment

```bash
# Deploy to specific environment
python deploy.py --env <environment>

# Environments: development, staging, production
```

### Platform-Specific Deployment

```bash
# Deploy to Vercel
python deploy.py --env production --platform vercel

# Deploy to Netlify
python deploy.py --env production --platform netlify

# Deploy to Railway (backend)
python deploy.py --env production --platform railway
```

### Advanced Options

```bash
# Dry run (simulate without deploying)
python deploy.py --env production --dry-run

# Skip tests (not recommended for production)
python deploy.py --env production --skip-tests

# Run tests only
python deploy.py --env production --test-only

# Rollback to previous version
python deploy.py --env production --rollback

# Rollback to specific version
python deploy.py --env production --rollback --version v1.2.3
```

### Combined Commands

```bash
# Full production deployment with all checks
python deploy.py --env production --platform vercel

# Quick staging deploy without tests (development only)
python deploy.py --env staging --skip-tests

# Test production deployment without actually deploying
python deploy.py --env production --dry-run
```

---

## Platform-Specific Guides

### Vercel Deployment

**Best for**: Frontend, serverless functions, static sites

#### 1. Install Vercel CLI

```bash
npm i -g vercel
```

#### 2. Login to Vercel

```bash
vercel login
```

#### 3. Configure Vercel

Create `vercel.json` in project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "*.html",
      "use": "@vercel/static"
    },
    {
      "src": "netlify/functions/*.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ],
  "env": {
    "NODE_ENV": "production"
  }
}
```

#### 4. Deploy

```bash
python deploy.py --env production --platform vercel
```

Or manually:

```bash
vercel --prod
```

#### 5. Set Environment Variables

```bash
vercel env add ANTHROPIC_API_KEY
vercel env add STRIPE_SECRET_KEY
```

---

### Netlify Deployment

**Best for**: Frontend, edge functions, forms

#### 1. Install Netlify CLI

```bash
npm i -g netlify-cli
```

#### 2. Login to Netlify

```bash
netlify login
```

#### 3. Configure Netlify

Create `netlify.toml`:

```toml
[build]
  command = "npm run build"
  publish = "."
  functions = "netlify/functions"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
```

#### 4. Deploy

```bash
python deploy.py --env production --platform netlify
```

Or manually:

```bash
netlify deploy --prod
```

#### 5. Set Environment Variables

```bash
netlify env:set ANTHROPIC_API_KEY "your-key"
netlify env:set STRIPE_SECRET_KEY "your-key"
```

---

### Railway Deployment

**Best for**: Backend APIs, databases, Docker containers

#### 1. Install Railway CLI

```bash
npm i -g @railway/cli
```

#### 2. Login to Railway

```bash
railway login
```

#### 3. Initialize Project

```bash
railway init
```

#### 4. Configure Railway

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python BACKEND/auth_system.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `Procfile`:

```
web: python BACKEND/auth_system.py
```

#### 5. Deploy

```bash
python deploy.py --env production --platform railway
```

Or manually:

```bash
railway up
```

#### 6. Set Environment Variables

```bash
railway variables --set ANTHROPIC_API_KEY=your-key
railway variables --set FLASK_ENV=production
```

---

### Render Deployment

**Best for**: Backend APIs, databases, cron jobs

#### 1. Configure Render

Create `render.yaml`:

```yaml
services:
  - type: web
    name: 100x-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn BACKEND.auth_system:app --workers 4"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: FLASK_ENV
        value: production
    healthCheckPath: /health
    autoDeploy: true

databases:
  - name: 100x-db
    plan: starter
```

#### 2. Connect Repository

1. Go to https://dashboard.render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`

#### 3. Deploy

Deploys automatically on git push, or use:

```bash
python deploy.py --env production --platform render
```

---

## CI/CD Integration

### GitHub Actions

The platform includes automated CI/CD via GitHub Actions. On every push to main:

1. Runs tests
2. Builds the project
3. Deploys to staging (automatically)
4. Awaits approval for production

#### Configuration File

Located at `.github/workflows/deploy.yml`

#### Trigger Manual Deployment

1. Go to Actions tab in GitHub
2. Select "Deploy 100X Platform" workflow
3. Click "Run workflow"
4. Choose environment and platform

#### Set GitHub Secrets

Required secrets in repository settings:

```
ANTHROPIC_API_KEY
AIRTABLE_TOKEN
AIRTABLE_BASE_ID
STRIPE_SECRET_KEY
VERCEL_TOKEN
NETLIFY_AUTH_TOKEN
RAILWAY_TOKEN
```

### Setting Up Secrets

```bash
# Using GitHub CLI
gh secret set ANTHROPIC_API_KEY

# Or via GitHub UI:
# Repository → Settings → Secrets → Actions → New repository secret
```

---

## Troubleshooting

### Common Issues

#### 1. "Module not found" Error

**Problem**: Missing dependencies

**Solution**:
```bash
npm install
pip install -r requirements.txt
```

#### 2. "Environment variable not set" Error

**Problem**: Missing API keys

**Solution**:
```bash
# Check your .env file
cat .env

# Set missing variables
export ANTHROPIC_API_KEY=your_key
```

#### 3. "Deployment failed" Error

**Problem**: Platform authentication issues

**Solution**:
```bash
# Re-login to platform
vercel login
netlify login
railway login
```

#### 4. "Tests failed" Error

**Problem**: Code issues or missing test files

**Solution**:
```bash
# Run tests locally to debug
npm test

# Skip tests temporarily (not recommended)
python deploy.py --env staging --skip-tests
```

#### 5. "Port already in use" Error

**Problem**: Local server running on same port

**Solution**:
```bash
# Kill process on port 5000 (macOS/Linux)
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F
```

### Debug Mode

Enable verbose logging:

```bash
# Set environment variable
export DEBUG=1

# Run deployment with debug info
python deploy.py --env staging --dry-run
```

### Check Deployment Logs

```bash
# View logs directory
ls -la .deployment_logs/

# View latest log
cat .deployment_logs/deploy_production_*.log
```

### Platform-Specific Logs

```bash
# Vercel logs
vercel logs

# Netlify logs
netlify logs

# Railway logs
railway logs
```

---

## Rollback Procedures

### Automatic Rollback

The deployment script includes automatic rollback on failure:

```python
# In deployment_config.json
"rollback": {
  "enabled": true,
  "auto_rollback_on_failure": true
}
```

### Manual Rollback

#### Rollback to Previous Version

```bash
python deploy.py --env production --rollback
```

#### Rollback to Specific Version

```bash
python deploy.py --env production --rollback --version v1.2.3
```

#### Platform-Specific Rollback

**Vercel**:
```bash
vercel rollback
```

**Netlify**:
```bash
# List deployments
netlify deploy:list

# Restore specific deployment
netlify deploy:restore <deploy-id>
```

**Railway**:
```bash
# Railway handles rollback via dashboard
railway open
# Navigate to deployments → Click "Rollback" on desired version
```

### Emergency Rollback Plan

1. **Immediate**: Use automated rollback
   ```bash
   python deploy.py --env production --rollback
   ```

2. **If automated fails**: Use platform dashboard
   - Vercel: Dashboard → Deployments → Click "..." → Redeploy
   - Netlify: Dashboard → Deploys → Click "Publish deploy"

3. **Last resort**: Deploy from backup
   ```bash
   git checkout <previous-commit>
   python deploy.py --env production --skip-tests
   ```

### Post-Rollback Checklist

- [ ] Verify site is accessible
- [ ] Check all critical features work
- [ ] Monitor error logs
- [ ] Notify team of rollback
- [ ] Create incident report
- [ ] Fix issues before next deployment

---

## Best Practices

### Pre-Deployment Checklist

- [ ] All tests passing locally
- [ ] Code reviewed and approved
- [ ] Environment variables configured
- [ ] Database migrations ready (if applicable)
- [ ] Backup created
- [ ] Rollback plan prepared
- [ ] Team notified of deployment

### Deployment Strategy

1. **Always deploy to staging first**
   ```bash
   python deploy.py --env staging
   ```

2. **Test staging thoroughly**
   - Manual testing
   - Automated smoke tests
   - Load testing (if applicable)

3. **Deploy to production during low-traffic hours**

4. **Monitor deployment**
   - Watch logs in real-time
   - Check error rates
   - Verify functionality

### Security Best Practices

1. **Never commit secrets**
   - Use `.env` files (gitignored)
   - Use platform secret management

2. **Enable HTTPS**
   - Enforced in production config
   - SSL certificates auto-renewed

3. **Set security headers**
   - X-Frame-Options
   - Content-Security-Policy
   - X-Content-Type-Options

4. **Rate limiting**
   - Configured in backend APIs
   - Prevents abuse

### Performance Optimization

1. **Enable CDN**
   - Vercel/Netlify CDN enabled by default
   - Edge caching configured

2. **Optimize assets**
   - Compress images
   - Minify CSS/JS
   - Use lazy loading

3. **Database optimization**
   - Index frequently queried fields
   - Use connection pooling

### Monitoring

1. **Set up uptime monitoring**
   - Use platform built-in monitoring
   - Or external: UptimeRobot, Pingdom

2. **Error tracking**
   - Sentry integration (optional)
   - Platform error logs

3. **Performance monitoring**
   - Vercel Analytics
   - Netlify Analytics

---

## FAQ

### General Questions

**Q: How long does a deployment take?**
A: Typically 3-5 minutes for full deployment. Staging is faster (~2 minutes).

**Q: Can I deploy multiple environments simultaneously?**
A: Not recommended. Deploy staging first, verify, then production.

**Q: What happens if deployment fails?**
A: Auto-rollback is triggered (if enabled). Previous version is restored.

**Q: How do I update environment variables?**
A: Update `.env` locally, then sync to platform using their CLI or dashboard.

### Platform Questions

**Q: Which platform should I use?**
A:
- **Frontend**: Vercel (recommended) or Netlify
- **Backend**: Railway (recommended) or Render

**Q: Can I use multiple platforms?**
A: Yes! The system supports multi-platform deployment for redundancy.

**Q: What about costs?**
A:
- **Vercel**: Free tier available, Pro starts at $20/month
- **Netlify**: Free tier available, Pro starts at $19/month
- **Railway**: Usage-based, ~$5-20/month for small projects
- **Render**: Free tier available, Starter at $7/month

### Technical Questions

**Q: How do I add a new module?**
A:
1. Add module to `MODULES/` directory
2. Add to `deployment_config.json` modules list
3. Run `python deploy.py --env staging`

**Q: How do I run local tests?**
A:
```bash
npm test
python -m pytest
```

**Q: Can I customize the deployment process?**
A: Yes! Edit `deploy.py` and `deployment_config.json` to fit your needs.

**Q: How do I enable notifications?**
A: Configure in `deployment_config.json`:
```json
"notifications": {
  "enabled": true,
  "channels": ["email", "sms", "slack"]
}
```

### Troubleshooting Questions

**Q: Deployment is stuck, what do I do?**
A:
1. Check platform status page
2. Review deployment logs
3. Try with `--dry-run` first
4. Contact platform support

**Q: How do I see detailed error messages?**
A:
```bash
# Check deployment logs
cat .deployment_logs/deploy_*.log

# Check platform logs
vercel logs
netlify logs
railway logs
```

**Q: Site is deployed but not working?**
A:
1. Check environment variables are set
2. Verify API endpoints are correct
3. Check browser console for errors
4. Review platform logs

---

## Support & Resources

### Documentation

- [Vercel Docs](https://vercel.com/docs)
- [Netlify Docs](https://docs.netlify.com)
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)

### Community

- GitHub Issues: https://github.com/your-org/100x-platform/issues
- Discord: https://discord.gg/100x-platform
- Email: support@100x-platform.com

### Emergency Contacts

- **Technical Issues**: tech@100x-platform.com
- **Platform Outages**: Check status pages:
  - https://vercel-status.com
  - https://netlifystatus.com
  - https://railway.app/status

---

## Appendix

### Environment Variables Reference

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Yes | Claude API key | - |
| `AIRTABLE_TOKEN` | Yes | Airtable API token | - |
| `AIRTABLE_BASE_ID` | Yes | Airtable base ID | - |
| `STRIPE_SECRET_KEY` | Yes | Stripe secret key | - |
| `STRIPE_PUBLISHABLE_KEY` | Yes | Stripe public key | - |
| `NODE_ENV` | No | Node environment | `development` |
| `FLASK_ENV` | No | Flask environment | `development` |
| `API_URL` | No | Backend API URL | `http://localhost:5000` |

### Port Configuration

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 8888 | Main web interface |
| Backend API | 5000 | REST API server |
| Database | 5432 | PostgreSQL (if used) |

### File Structure

```
100x-platform/
├── deploy.py                 # Master deployment script
├── deployment_config.json    # Deployment configuration
├── DEPLOYMENT_GUIDE.md      # This guide
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD pipeline
├── BACKEND/                 # Backend APIs
├── MODULES/                 # 30 platform modules
├── netlify/                 # Netlify functions
├── .env                     # Environment variables (gitignored)
├── .env.example             # Environment template
├── package.json             # Node.js config
└── requirements.txt         # Python dependencies
```

---

## Changelog

### v1.0.0 - Initial Release
- Complete deployment automation
- Multi-platform support (Vercel, Netlify, Railway, Render)
- Automated testing and smoke tests
- Rollback functionality
- CI/CD integration
- Comprehensive documentation

---

**Made with ⚡ by the 100X Platform Team**

*Last Updated: 2025-11-07*
