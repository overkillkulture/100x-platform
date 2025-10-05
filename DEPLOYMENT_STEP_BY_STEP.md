# 🚀 100X PLATFORM - PRODUCTION DEPLOYMENT GUIDE

**"From localhost to live in under 1 hour"**

---

## 🎯 DEPLOYMENT STRATEGY

**Recommended: Railway.app (Fastest Path to Production)**

Why Railway:
- One-click deployment from GitHub
- Automatic SSL/HTTPS
- Built-in PostgreSQL/MongoDB
- $5/month base + usage
- Zero DevOps required

**Alternative Options:**
- Vercel (frontend) + Railway (backend) - $0-20/month
- DigitalOcean App Platform - $5-12/month
- Heroku - $7-25/month
- AWS/GCP - Complex, overkill for MVP

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### **1. Security Hardening** ✅
```bash
npm install bcrypt express-rate-limit helmet cors dotenv
```

### **2. Environment Variables**
Create `.env` file:
```
PORT=3100
SESSION_SECRET=your-super-secret-key-change-this
DATABASE_URL=mongodb://localhost:27017/100x
NODE_ENV=production
ALLOWED_ORIGINS=https://100x.app,https://www.100x.app
```

### **3. Database Migration**
Replace `db.json` with MongoDB:
```bash
npm install mongodb mongoose
```

### **4. Git Repository**
```bash
git init
git add .
git commit -m "Initial 100X Platform deployment"
git remote add origin https://github.com/yourusername/100x-platform.git
git push -u origin main
```

---

## 🔒 SECURITY UPDATES

### **Update server.js with Production Security:**

```javascript
// Add at top
require('dotenv').config();
const bcrypt = require('bcrypt');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const cors = require('cors');

// Security middleware
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", "data:", "https:"],
        }
    }
}));

app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3100',
    credentials: true
}));

// Rate limiting
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 attempts
    message: 'Too many login attempts, try again later'
});

app.post('/api/login', loginLimiter, async (req, res) => {
    // Existing login logic with bcrypt
});

// Session with secure settings
app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: process.env.NODE_ENV === 'production', // HTTPS only in prod
        httpOnly: true,
        maxAge: 1000 * 60 * 60 * 24 * 7 // 1 week
    }
}));
```

---

## 🗄️ DATABASE MIGRATION (MongoDB)

### **Install MongoDB:**
```bash
npm install mongoose
```

### **Create models/User.js:**
```javascript
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    consciousness_level: { type: Number, default: 0 },
    layer: { type: Number, default: 1 },
    xp: { type: Number, default: 0 },
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('User', userSchema);
```

### **Create models/Project.js:**
```javascript
const mongoose = require('mongoose');

const projectSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    name: { type: String, required: true },
    category: String,
    status: { type: String, default: 'blueprint' },
    revenue: { type: Number, default: 0 },
    description: String,
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Project', projectSchema);
```

### **Update server.js to use MongoDB:**
```javascript
const mongoose = require('mongoose');
const User = require('./models/User');
const Project = require('./models/Project');

// Connect to MongoDB
mongoose.connect(process.env.DATABASE_URL || 'mongodb://localhost:27017/100x')
    .then(() => console.log('✅ Connected to MongoDB'))
    .catch(err => console.error('❌ MongoDB connection error:', err));

// Replace all db.get/set with Mongoose operations
// Example: Register user
app.post('/api/register', async (req, res) => {
    const { username, email, password } = req.body;

    const hashedPassword = await bcrypt.hash(password, 10);

    const user = new User({
        username,
        email,
        password: hashedPassword
    });

    await user.save();
    res.json({ success: true });
});
```

---

## ☁️ RAILWAY.APP DEPLOYMENT

### **Step 1: Prepare for Railway**

Create `railway.json`:
```json
{
    "$schema": "https://railway.app/railway.schema.json",
    "build": {
        "builder": "NIXPACKS"
    },
    "deploy": {
        "startCommand": "node server.js",
        "restartPolicyType": "ON_FAILURE",
        "restartPolicyMaxRetries": 10
    }
}
```

Create `Procfile`:
```
web: node server.js
```

Update `package.json`:
```json
{
    "scripts": {
        "start": "node server.js",
        "dev": "nodemon server.js"
    },
    "engines": {
        "node": "18.x"
    }
}
```

### **Step 2: Deploy to Railway**

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your 100X Platform repo
5. Railway auto-detects Node.js and deploys

### **Step 3: Add MongoDB on Railway**

1. In your Railway project, click "New" → "Database" → "MongoDB"
2. Copy the `MONGO_URL` connection string
3. Go to project Variables, add:
   - `DATABASE_URL` = (paste MongoDB URL)
   - `SESSION_SECRET` = (generate random 32-char string)
   - `NODE_ENV` = `production`
   - `ALLOWED_ORIGINS` = `https://yourapp.up.railway.app`

### **Step 4: Custom Domain (Optional)**

1. In Railway settings, go to "Domains"
2. Click "Generate Domain" (gets you `*.up.railway.app`)
3. OR add custom domain:
   - Add your domain (e.g., `100x.app`)
   - Add CNAME record in your DNS:
     - Name: `@` or `www`
     - Value: `yourapp.up.railway.app`

---

## 🔐 ENVIRONMENT VARIABLES

**Required Variables:**

```bash
# Railway Dashboard → Variables → Add
PORT=3100
SESSION_SECRET=super-secret-key-min-32-chars-change-this-immediately
DATABASE_URL=mongodb://username:password@host:port/100x
NODE_ENV=production
ALLOWED_ORIGINS=https://100x.app,https://www.100x.app
```

**Generate Strong SESSION_SECRET:**
```javascript
// Run this once in Node.js console
require('crypto').randomBytes(32).toString('hex')
```

---

## 📊 MONITORING & BACKUPS

### **Railway Built-in Monitoring:**
- View logs in Railway dashboard
- Metrics tab shows CPU/RAM usage
- Deployments tab shows history

### **MongoDB Backups:**
```javascript
// Add to server.js for daily backups
const cron = require('node-cron');

cron.schedule('0 0 * * *', async () => {
    // Backup database daily at midnight
    const users = await User.find({});
    const projects = await Project.find({});

    fs.writeFileSync(`backups/backup-${Date.now()}.json`, JSON.stringify({
        users,
        projects
    }));
});
```

### **Error Tracking (Optional):**
```bash
npm install @sentry/node
```

---

## 🚦 GO-LIVE CHECKLIST

**Before Launch:**

```
Security:
  ✅ Passwords hashed with bcrypt
  ✅ Rate limiting on login/register
  ✅ Helmet.js security headers
  ✅ CORS configured
  ✅ Session cookies secure (httpOnly, secure in prod)
  ✅ Input validation on all endpoints
  ✅ SQL injection protection (using Mongoose)

Database:
  ✅ MongoDB connected
  ✅ Indexes on username/email for performance
  ✅ Daily backups configured
  ✅ Connection pooling enabled

Performance:
  ✅ Gzip compression enabled
  ✅ Static files served efficiently
  ✅ Database queries optimized
  ✅ Rate limiting prevents abuse

Legal/Compliance:
  ✅ Terms of Service page
  ✅ Privacy Policy page
  ✅ Cookie consent (if EU users)
  ✅ GDPR compliance basics

Functionality:
  ✅ All features tested in production mode
  ✅ Login/register works
  ✅ Dashboard loads correctly
  ✅ Projects CRUD works
  ✅ The Bridge renders
  ✅ Blueprint tool generates plans
```

---

## 💰 COST BREAKDOWN

**Railway.app (Recommended):**
- Hobby Plan: $5/month (500 hours)
- MongoDB Plugin: $5/month (512MB storage)
- **Total: $10/month for MVP**

**Scaling Costs:**
- 1,000 users: ~$20/month
- 10,000 users: ~$50-100/month
- 100,000 users: ~$500/month (time to raise funding)

**Alternative (Budget Option):**
- Vercel (Frontend): $0/month (free tier)
- Railway (Backend + DB): $10/month
- **Total: $10/month**

---

## 🎯 DEPLOYMENT TIMELINE

**Fastest Path (1 hour):**

```
00:00 - Security updates (15 min)
00:15 - MongoDB migration (20 min)
00:35 - Git setup & push (10 min)
00:45 - Railway deployment (10 min)
00:55 - Test production (5 min)
01:00 - LIVE! 🚀
```

**Recommended Path (4 hours):**

```
Hour 1: Security hardening + testing
Hour 2: Database migration + data validation
Hour 3: Git setup + Railway deployment
Hour 4: Production testing + monitoring setup
```

---

## 🔧 QUICK COMMANDS

**Local Testing:**
```bash
NODE_ENV=production node server.js
```

**Railway CLI Deploy:**
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

**MongoDB Local to Cloud Migration:**
```bash
mongodump --db 100x
mongorestore --uri "mongodb+srv://..." --db 100x dump/100x
```

---

## 🚨 TROUBLESHOOTING

**Issue: "Cannot connect to MongoDB"**
- Check DATABASE_URL format: `mongodb://user:pass@host:port/db`
- Verify MongoDB plugin is running in Railway
- Check IP whitelist (Railway IPs change, use 0.0.0.0/0 for now)

**Issue: "Session not persisting"**
- Set `cookie.secure: false` for testing (http)
- Set `cookie.secure: true` for production (https)
- Verify SESSION_SECRET is set

**Issue: "Rate limiting too strict"**
- Adjust windowMs and max in loginLimiter
- Test with: `curl -X POST http://localhost:3100/api/login` (repeat 6 times)

**Issue: "CORS errors"**
- Add your domain to ALLOWED_ORIGINS
- Check preflight OPTIONS requests
- Verify credentials: true in cors config

---

## ✅ POST-DEPLOYMENT

**After going live:**

1. **Test with Genesis Recruit #1** tomorrow
2. **Monitor Railway logs** for errors
3. **Backup database** before adding more users
4. **Set up alerts** for downtime (UptimeRobot.com - free)
5. **Prepare for feedback** and rapid iteration

**You're ready to give Genesis Recruit #1 her login tomorrow** 🎯

---

**Commander, this is your deployment blueprint. Railway.app = fastest path to production. Want me to start the security updates to server.js?** 🚀
