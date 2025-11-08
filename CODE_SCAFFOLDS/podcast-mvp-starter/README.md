# 🎙️ Podcast MVP - Starter Code

Minimal working code to get you started on the Podcast MVP in 15 minutes.

## ✅ What's Included

**Backend (Flask):**
- ✅ User authentication (signup/login with JWT)
- ✅ Podcast and Episode models (PostgreSQL)
- ✅ CRUD endpoints for podcasts
- ✅ Database setup with SQLAlchemy

**Frontend (React):**
- ✅ Login and Signup forms
- ✅ Dashboard with podcast list
- ✅ Create new podcast form
- ✅ API integration with axios

## 🚀 Quick Start (15 minutes)

### 1. Backend Setup (5 minutes)

```bash
# Install dependencies
pip install flask flask-cors flask-jwt-extended sqlalchemy psycopg2-binary

# Create database
createdb podcast_mvp

# Edit app.py - Update these lines:
# - app.config['JWT_SECRET_KEY'] = 'your-secret-key'
# - DATABASE_URL = 'postgresql://localhost:5432/podcast_mvp'

# Run backend
cd backend
python app.py

# Test health check
curl http://localhost:5000/api/health
```

Expected output: `{"status": "ok", "message": "Podcast MVP API is running"}`

### 2. Frontend Setup (5 minutes)

```bash
# Create React app
npm create vite@latest frontend -- --template react
cd frontend

# Install dependencies
npm install axios react-router-dom

# Copy App.jsx
cp ../frontend/App.jsx src/App.jsx

# Run frontend
npm run dev
```

Open http://localhost:5173

### 3. Test (5 minutes)

1. **Sign up**: Create account with email/password
2. **Create podcast**: Click "New Podcast", enter title
3. **See it in dashboard**: Your podcast appears in the list

**Success!** You now have a working podcast platform starter.

## 📝 What's Next?

This starter gives you auth + basic CRUD. To build the full MVP, add:

### Week 1: Database + Auth ✅ DONE
- [x] User model
- [x] Podcast model
- [x] Episode model
- [x] JWT authentication

### Week 2: Recording (See MVP_TECHNICAL_SPEC.md)
- [ ] WebRTC recording component (lines 550-650)
- [ ] Real-time audio chunks upload
- [ ] S3 integration (lines 400-450)

### Week 3: Processing (See MVP_TECHNICAL_SPEC.md)
- [ ] Celery background tasks (lines 800-850)
- [ ] FFmpeg audio enhancement (lines 850-900)
- [ ] Whisper transcription (lines 900-950)
- [ ] Claude show notes generation (lines 950-1000)

### Week 4: Billing + Launch (See MVP_TECHNICAL_SPEC.md)
- [ ] Stripe integration (lines 450-500)
- [ ] Subscription tiers
- [ ] Usage limits
- [ ] Beta testing + deployment

## 📚 Full Documentation

**Complete 1,200-line technical spec:**
`MODULES/CONTENT/podcast_production/MVP_TECHNICAL_SPEC.md`

**14-day development guide:**
`QUICK_START_GUIDES/PODCAST_QUICKSTART.md`

**Strategic assessment:**
`MODULES/CONTENT/podcast_production/DEPLOYMENT_PACKAGE.md`

## 🔧 Troubleshooting

**Database connection error:**
```bash
# Check PostgreSQL is running
pg_isready

# Create database if it doesn't exist
createdb podcast_mvp
```

**CORS error in frontend:**
- Make sure backend is running on http://localhost:5000
- Check `CORS(app)` is in app.py

**JWT error:**
- Make sure you're sending `Authorization: Bearer <token>` header
- Token is stored in localStorage after login

## 💰 Revenue Potential

With this foundation, you can build to:
- **Month 6:** $29.4K MRR (600 users)
- **Year 1:** $98K MRR (2,000 users)
- **Total Year 1 Revenue:** $466.4K

## 🚀 Ready to Build?

1. Get this starter working (15 minutes)
2. Read `MVP_TECHNICAL_SPEC.md` (30 minutes)
3. Follow `PODCAST_QUICKSTART.md` day-by-day (14 days)
4. Launch! 🎉

---

**Created by:** C1 - The Mechanic
**For:** Fast MVP development start
**Time to first API call:** 15 minutes
