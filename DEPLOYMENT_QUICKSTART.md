# 100X Platform - Deployment Quick Start

## 🚀 One-Command Deployment

### Prerequisites Checklist
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env and add your API keys
nano .env  # or use your preferred editor

# 3. Install dependencies
npm install
pip install -r requirements.txt
```

### Deploy Commands

#### Local Development
```bash
python deploy.py --env development
```

#### Staging Environment
```bash
python deploy.py --env staging --platform netlify
```

#### Production Environment
```bash
python deploy.py --env production --platform vercel
```

### Common Options

| Command | Description |
|---------|-------------|
| `--dry-run` | Test deployment without changes |
| `--skip-tests` | Skip running tests (not recommended) |
| `--test-only` | Only run tests, don't deploy |
| `--rollback` | Rollback to previous version |

### Quick Examples

```bash
# Test production deployment without deploying
python deploy.py --env production --dry-run

# Deploy to staging without tests (dev only)
python deploy.py --env staging --skip-tests

# Run tests only
python deploy.py --env production --test-only

# Rollback production
python deploy.py --env production --rollback
```

### Platform-Specific Quick Deploy

#### Vercel (Frontend)
```bash
npm i -g vercel
vercel login
vercel --prod
```

#### Netlify (Frontend)
```bash
npm i -g netlify-cli
netlify login
netlify deploy --prod
```

#### Railway (Backend)
```bash
npm i -g @railway/cli
railway login
railway up
```

### CI/CD Quick Setup

1. Add secrets to GitHub repository:
   - `ANTHROPIC_API_KEY`
   - `AIRTABLE_TOKEN`
   - `STRIPE_SECRET_KEY`
   - `VERCEL_TOKEN`
   - `NETLIFY_AUTH_TOKEN`
   - `RAILWAY_TOKEN`

2. Push to main branch - automatic deployment!

3. Manual deployment:
   - Go to GitHub Actions
   - Select "Deploy 100X Platform"
   - Click "Run workflow"
   - Choose environment and platform

### Troubleshooting One-Liners

```bash
# Check deployment logs
cat .deployment_logs/deploy_*.log | tail -50

# Verify environment variables
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Keys loaded:', bool(os.getenv('ANTHROPIC_API_KEY')))"

# Test API connectivity
curl -f https://api.100x-platform.com/health

# View platform logs
vercel logs      # Vercel
netlify logs     # Netlify
railway logs     # Railway
```

### Emergency Rollback

```bash
# Quick rollback
python deploy.py --env production --rollback

# Rollback to specific version
python deploy.py --env production --rollback --version v1.2.3
```

### Help & Documentation

```bash
# Show all options
python deploy.py --help

# Read full guide
cat DEPLOYMENT_GUIDE.md

# View configuration
cat deployment_config.json | jq
```

### Support

- 📖 Full Guide: `DEPLOYMENT_GUIDE.md`
- 🐛 Issues: https://github.com/your-org/100x-platform/issues
- 💬 Discord: https://discord.gg/100x-platform
- 📧 Email: support@100x-platform.com

---

**Made with ⚡ by the 100X Platform Team**
