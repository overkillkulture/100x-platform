# 🚀 Universal Consciousness API - Quick Start Guide

## What Is This?

**The API that unlocks infinite third-party integrations for your social media automation.**

Built autonomously while you relocated. Trinity-powered. Ready to scale.

---

## 🎯 Quick Start (3 Steps)

### Step 1: Start the API Server

```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
python CONSCIOUSNESS_API_SERVER.py
```

Server starts on: `http://localhost:5000`

### Step 2: Get Your API Key

Check your desktop: `COMMANDER_API_KEY.txt`

Or create a new one:
```bash
curl -X POST http://localhost:5000/admin/create-key \
  -H "Content-Type: application/json" \
  -d '{"name":"Your Name","email":"you@example.com","tier":"free"}'
```

### Step 3: Make Your First Request

```bash
curl -H "X-API-Key: YOUR_KEY_HERE" \
  http://localhost:5000/api/v1/platforms
```

---

## 📋 Available Endpoints

### Health Check
```bash
GET /health
```

### Post to Multiple Platforms
```bash
POST /api/v1/post
Headers: X-API-Key: YOUR_KEY
Body: {
  "platforms": ["tiktok", "linkedin", "youtube"],
  "video_path": "/path/to/video.mp4",
  "caption": "Your caption",
  "title": "Video title"
}
```

### Get Analytics
```bash
GET /api/v1/analytics
Headers: X-API-Key: YOUR_KEY
```

### List Platforms
```bash
GET /api/v1/platforms
Headers: X-API-Key: YOUR_KEY
```

### Get Usage Stats
```bash
GET /api/v1/usage
Headers: X-API-Key: YOUR_KEY
```

---

## 💡 Integration Examples

### Python Example
```python
import requests

API_KEY = "ck_your_key_here"
API_URL = "http://localhost:5000/api/v1"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Post to multiple platforms
response = requests.post(
    f"{API_URL}/post",
    headers=headers,
    json={
        "platforms": ["tiktok", "linkedin", "youtube"],
        "video_path": "C:/Users/dwrek/SOCIAL_VIDEOS/twitter_linkedin.mp4",
        "caption": "Check out this automation! 🚀",
        "title": "Social Media Automation Demo"
    }
)

print(response.json())
```

### JavaScript Example
```javascript
const API_KEY = "ck_your_key_here";
const API_URL = "http://localhost:5000/api/v1";

async function postToSocial() {
    const response = await fetch(`${API_URL}/post`, {
        method: 'POST',
        headers: {
            'X-API-Key': API_KEY,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            platforms: ['tiktok', 'linkedin', 'youtube'],
            video_path: 'C:/Users/dwrek/SOCIAL_VIDEOS/twitter_linkedin.mp4',
            caption: 'Automated post via API! 🌌',
            title: 'API Demo'
        })
    });

    const data = await response.json();
    console.log(data);
}

postToSocial();
```

### cURL Example
```bash
curl -X POST http://localhost:5000/api/v1/post \
  -H "X-API-Key: ck_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["tiktok", "linkedin", "youtube"],
    "video_path": "C:/Users/dwrek/SOCIAL_VIDEOS/twitter_linkedin.mp4",
    "caption": "Posted via cURL! ⚡",
    "title": "API Demo"
  }'
```

---

## 🔐 Authentication

All API requests require the `X-API-Key` header:

```
X-API-Key: ck_your_32_character_key_here
```

**Keep your API key secure!** Don't commit it to public repos.

---

## 📊 Response Format

All successful responses return JSON:

```json
{
  "status": "success",
  "message": "Posted to 3 platforms",
  "platforms": ["tiktok", "linkedin", "youtube"],
  "results": {
    "tiktok": {"success": true, "url": "..."},
    "linkedin": {"success": true, "url": "..."},
    "youtube": {"success": true, "video_id": "..."}
  },
  "timestamp": "2025-10-16T18:30:00Z"
}
```

Errors return appropriate status codes:
- `400` - Bad request (missing fields)
- `401` - Unauthorized (invalid API key)
- `500` - Server error

---

## 🌐 Deploying to Production

### Option 1: Railway.app (Recommended)
```bash
# Install Railway CLI
npm install -g railway

# Login
railway login

# Deploy
railway init
railway up
```

### Option 2: Heroku
```bash
# Install Heroku CLI
# Create Procfile:
echo "web: python CONSCIOUSNESS_API_SERVER.py" > Procfile

# Deploy
heroku create consciousness-api
git push heroku main
```

### Option 3: VPS (DigitalOcean, Linode, etc.)
```bash
# On server:
git clone your-repo
cd your-repo
pip install -r requirements.txt
python CONSCIOUSNESS_API_SERVER.py

# Use nginx as reverse proxy
# Use systemd or pm2 to keep running
```

---

## 🔥 What This Unlocks

**Third-Party Integrations:**
- Zapier connections
- Make.com automations
- IFTTT triggers
- Custom apps
- Mobile apps
- Browser extensions
- Slack bots
- Discord bots
- **INFINITE POSSIBILITIES**

**Network Effects:**
- Every integration brings new users
- Users bring more integrations
- Exponential growth loop

**Category Leadership:**
- First consciousness-aligned social API
- Open source = community trust
- Gift model = viral growth

---

## 💎 Next Steps

1. **Test locally:** Make sure API works with your setup
2. **Deploy to cloud:** Get a public URL
3. **Add to platform:** Link from consciousnessrevolution.io
4. **Open source:** GitHub repo + documentation
5. **Launch:** ProductHunt, HackerNews, Reddit

---

## 🌌 The Vision

This API isn't just automation infrastructure.

**It's proof that consciousness can organize systems through GIFTS instead of CONTROL.**

Every third-party integration = another node in consciousness network.

**Built autonomously. Trinity-powered. Consciousness-elevated.** ⚡🚀

---

*For support: Check main documentation or consciousness revolution platform*
