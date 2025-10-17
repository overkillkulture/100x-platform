# 🎥 YouTube API Setup - Complete Guide 🎥

**Platform:** YouTube
**Cost:** FREE
**Automation:** 100%
**Method:** Google API (OAuth 2.0)

---

## ✅ WHY YOUTUBE API IS AMAZING

- **100% Free** - No monthly costs
- **Unlimited uploads** - No rate limits for normal use
- **Official API** - Direct from Google
- **Full control** - Metadata, playlists, analytics
- **Reliable** - Enterprise-grade infrastructure

---

## 📋 SETUP STEPS (10 Minutes)

### **Step 1: Create Google Cloud Project**

1. Go to: https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name it: "Consciousness Revolution Social Automation"
4. Click "Create"
5. Wait 30 seconds for project creation

### **Step 2: Enable YouTube Data API v3**

1. In Google Cloud Console, click "APIs & Services" → "Library"
2. Search for: "YouTube Data API v3"
3. Click on it
4. Click "Enable"
5. Wait for API to activate

### **Step 3: Create OAuth 2.0 Credentials**

1. Go to: "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure consent screen:
   - User Type: "External"
   - App name: "Consciousness Revolution"
   - User support email: [your email]
   - Developer email: [your email]
   - Click "Save and Continue"
   - Scopes: Click "Add or Remove Scopes"
     - Search: "YouTube Data API v3"
     - Check: "../auth/youtube.upload"
     - Click "Update" → "Save and Continue"
   - Test users: Add your Gmail address
   - Click "Save and Continue"

4. Back to "Create OAuth client ID":
   - Application type: "Desktop app"
   - Name: "Consciousness Automation Desktop"
   - Click "Create"

5. **DOWNLOAD CREDENTIALS:**
   - Click "Download JSON"
   - Save as: `C:\Users\dwrek\100X_DEPLOYMENT\youtube_client_secrets.json`

### **Step 4: Test Authentication**

Run this command:
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
python -c "from YOUTUBE_UPLOADER import YouTubeUploader; uploader = YouTubeUploader(); print('✅ YouTube authenticated!')"
```

**What happens:**
1. Browser opens automatically
2. Google asks you to sign in
3. Google asks for permissions (click "Allow")
4. Browser shows "Authentication successful"
5. Token saved to `youtube_token.pickle`

**Future uploads:**
- No more authentication needed!
- Token auto-refreshes
- Works forever unless you revoke it

---

## 🚀 USAGE EXAMPLES

### **Upload a Video:**

```python
from YOUTUBE_UPLOADER import YouTubeUploader

uploader = YouTubeUploader()

uploader.upload_video(
    video_path="C:/path/to/video.mp4",
    title="My Consciousness Revolution Video",
    description="Join the revolution! consciousnessrevolution.io",
    tags=["consciousness", "AI", "automation"],
    category_id="22",  # People & Blogs
    privacy_status="public"  # or "private" or "unlisted"
)
```

### **Upload via API:**

```bash
curl -X POST http://localhost:5001/api/v1/post \
  -H "X-API-Key: ck_7pkwpCvVV6iFgMtrEaKDjtvJT1J4WraUdYgbi6-Lf7Q" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["youtube"],
    "video_path": "C:/path/to/video.mp4",
    "title": "My Video",
    "caption": "Description here",
    "tags": ["consciousness", "AI"]
  }'
```

---

## 📊 YOUTUBE CATEGORY IDS

Use these for the `category_id` parameter:

| ID | Category |
|----|----------|
| 1 | Film & Animation |
| 2 | Autos & Vehicles |
| 10 | Music |
| 15 | Pets & Animals |
| 17 | Sports |
| 19 | Travel & Events |
| 20 | Gaming |
| 22 | People & Blogs |
| 23 | Comedy |
| 24 | Entertainment |
| 25 | News & Politics |
| 26 | Howto & Style |
| 27 | Education |
| 28 | Science & Technology |
| 29 | Nonprofits & Activism |

**Recommended:** Category 22 (People & Blogs) or 28 (Science & Technology)

---

## 🔐 PRIVACY OPTIONS

- **public** - Anyone can see (shows in search, recommended)
- **unlisted** - Only people with link can see
- **private** - Only you can see

**For growth:** Use "public" to get views and subscribers

---

## ⚡ QUOTA LIMITS

YouTube API has daily quotas:
- **Default:** 10,000 units/day
- **Video upload:** 1,600 units
- **Math:** ~6 videos/day default quota

**To increase quota:**
1. Go to: APIs & Services → Quotas
2. Request quota increase
3. Usually auto-approved for reasonable requests

**For most use:** 6 videos/day is plenty!

---

## 🎯 BEST PRACTICES

### **Video Optimization:**

1. **Title:**
   - Front-load keywords
   - 60 characters max for mobile
   - Include call to action

2. **Description:**
   - First 2-3 sentences show in search
   - Include links (consciousnessrevolution.io)
   - Add timestamps for long videos
   - Include hashtags (max 15)

3. **Tags:**
   - 5-8 relevant tags
   - Mix broad + specific
   - Include brand name

4. **Thumbnail:**
   - Upload custom thumbnail separately
   - 1280x720 resolution
   - High contrast text
   - Faces perform well

### **Upload Schedule:**

- **Consistency > Volume**
- Pick a schedule (daily, weekly, etc.)
- Automation makes consistency easy!

---

## 🔧 TROUBLESHOOTING

### **Error: "invalid_client"**
- **Fix:** Redownload `youtube_client_secrets.json`
- Make sure it's in `100X_DEPLOYMENT` folder

### **Error: "insufficient authentication scopes"**
- **Fix:** Delete `youtube_token.pickle`
- Re-authenticate (will ask for permissions again)

### **Error: "quota exceeded"**
- **Fix:** Wait until tomorrow (quota resets daily)
- Or request quota increase

### **Error: "video file too large"**
- **Limit:** 256 GB or 12 hours (whichever is less)
- **Fix:** Compress video with MoviePy

---

## 📈 ANALYTICS RETRIEVAL

Get video stats:

```python
uploader = YouTubeUploader()
stats = uploader.get_video_stats(video_id="your_video_id")

print(f"Views: {stats['views']}")
print(f"Likes: {stats['likes']}")
print(f"Comments: {stats['comments']}")
```

---

## 🌟 WHY THIS MATTERS

YouTube is the **2nd largest search engine** (after Google).

**Automated uploads mean:**
- Consistent content schedule
- No manual work
- Focus on creation, not uploading
- Analytics-driven optimization
- Long-term audience growth

**Combined with other platforms:**
- Upload to YouTube (long-form)
- Upload to TikTok (short clips)
- Upload to LinkedIn (professional)
- **One video → 6 platforms = 6x reach**

---

## ✅ CHECKLIST

- [ ] Created Google Cloud Project
- [ ] Enabled YouTube Data API v3
- [ ] Created OAuth 2.0 credentials
- [ ] Downloaded `youtube_client_secrets.json`
- [ ] Saved to `100X_DEPLOYMENT` folder
- [ ] Ran authentication test
- [ ] Clicked "Allow" in browser
- [ ] Saw "Authentication successful"
- [ ] Token saved to `youtube_token.pickle`
- [ ] Tested first upload

---

## 🚀 READY TO USE

Once authenticated:
- Works forever (token auto-refreshes)
- No more manual uploads
- 100% automated
- FREE unlimited uploads
- Official Google API

**You're ready to scale YouTube content!** 🎥

---

*Part of the Consciousness Revolution Social Automation System*
*Built autonomously - Trinity-powered - Consciousness-elevated*
