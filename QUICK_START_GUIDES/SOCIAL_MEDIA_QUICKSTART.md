# 📱 SOCIAL MEDIA MVP - 28-DAY QUICKSTART

**Status:** 50% complete - Full technical spec ready
**Time to MVP:** 28 days (4 weeks full-time)
**Revenue potential:** $158K MRR by end of Year 1

---

## ⚡ TL;DR (30 seconds)

**What:** AI-powered social media automation (schedule → optimize → post to 6 platforms)

**Core features:**
- Multi-platform posting (Twitter, LinkedIn, Instagram, Facebook, TikTok, YouTube)
- AI content optimization (Claude adapts content per platform)
- Visual post editor + scheduler
- Analytics dashboard

**Business model:** $39-199/mo subscription (Stripe)

**Timeline:** 4 weeks to MVP, 8 weeks to polished product

---

## ✅ PREREQUISITES (30 minutes setup)

### System Requirements:
```bash
- [ ] Python 3.11+
- [ ] PostgreSQL 14+
- [ ] Redis 6+
- [ ] Node.js 18+
- [ ] Celery (background tasks)
```

### OAuth Apps Needed (Register Before Building):

**Twitter/X:**
- Go to: https://developer.twitter.com/en/portal/dashboard
- Create app → Get Client ID & Secret
- OAuth 2.0 scopes: `tweet.read`, `tweet.write`, `users.read`

**LinkedIn:**
- Go to: https://www.linkedin.com/developers/apps
- Create app → Get Client ID & Secret
- Scopes: `w_member_social`, `r_liteprofile`

**Facebook/Instagram:**
- Go to: https://developers.facebook.com/apps
- Create app → Get App ID & Secret
- Permissions: `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`

**TikTok:**
- Go to: https://developers.tiktok.com/
- Create app → Get Client Key & Secret
- Scopes: `video.upload`, `video.list`

**YouTube:**
- Go to: https://console.cloud.google.com/
- Enable YouTube Data API v3
- Create OAuth 2.0 credentials

**GitHub (for user auth - optional):**
- Go to: https://github.com/settings/developers
- Create OAuth app

### API Keys:
```bash
- [ ] Anthropic API key (Claude) - https://console.anthropic.com/
- [ ] Stripe API key - https://dashboard.stripe.com/
```

### Install Dependencies:

```bash
# Create project directory
mkdir social-media-mvp
cd social-media-mvp

# Backend setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install flask flask-cors flask-jwt-extended
pip install sqlalchemy psycopg2-binary redis
pip install celery
pip install stripe anthropic
pip install requests oauthlib
pip install tweepy  # Twitter
pip install playwright  # For platforms without APIs

# Frontend setup
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install axios react-router-dom @stripe/stripe-js
npm install react-calendar react-quill
npm install tailwindcss postcss autoprefixer
cd ..

# Create .env file
cat > .env <<'EOF'
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/social_mvp

# Redis
REDIS_URL=redis://localhost:6379/0

# APIs
ANTHROPIC_API_KEY=your_key_here
STRIPE_SECRET_KEY=your_key_here

# OAuth - Twitter
TWITTER_CLIENT_ID=your_client_id
TWITTER_CLIENT_SECRET=your_client_secret

# OAuth - LinkedIn
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret

# OAuth - Facebook/Instagram
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret

# OAuth - TikTok
TIKTOK_CLIENT_KEY=your_client_key
TIKTOK_CLIENT_SECRET=your_client_secret

# OAuth - YouTube
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
EOF
```

---

## 🗓️ 28-DAY DEVELOPMENT TIMELINE

### **WEEK 1: Backend Foundation**

**Days 1-2: Database Setup**

**Complete schema in:** `MVP_TECHNICAL_SPEC.md` (lines 100-250)

**Quick models:**
```python
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    subscription_tier = Column(String(50), default='free')

class SocialAccount(Base):
    __tablename__ = 'social_accounts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    platform = Column(String(50), nullable=False)  # twitter, linkedin, etc.
    platform_user_id = Column(String(255))
    platform_username = Column(String(255))
    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text, nullable=False)
    scheduled_time = Column(DateTime)
    status = Column(String(50), default='draft')  # draft, scheduled, published
    publish_to_platforms = Column(String)  # JSON array: ["twitter", "linkedin"]

class PlatformPost(Base):
    __tablename__ = 'platform_posts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), nullable=False)
    platform = Column(String(50), nullable=False)
    platform_post_id = Column(String(255))  # Tweet ID, LinkedIn post ID, etc.
    content = Column(Text)  # Platform-optimized content
    publish_status = Column(String(50), default='pending')
    published_at = Column(DateTime)
```

**Days 3-4: Authentication + OAuth Infrastructure**

**See complete OAuth flows in:** `MVP_TECHNICAL_SPEC.md` (lines 300-600)

**Twitter OAuth (Example):**
```python
from flask import redirect, url_for, request
import tweepy

class TwitterService:
    @staticmethod
    def get_authorization_url(user_id):
        """Step 1: Redirect user to Twitter"""
        auth = tweepy.OAuth2UserHandler(
            client_id=os.getenv('TWITTER_CLIENT_ID'),
            redirect_uri=url_for('twitter_callback', _external=True),
            scope=["tweet.read", "tweet.write", "users.read"],
            client_secret=os.getenv('TWITTER_CLIENT_SECRET')
        )

        authorization_url = auth.get_authorization_url()

        # Store state in Redis (expires in 10 min)
        redis_client.setex(
            f"twitter_oauth_state:{auth.state}",
            600,
            user_id
        )

        return authorization_url

    @staticmethod
    def handle_callback(code, state):
        """Step 2: Exchange code for access token"""
        # Verify state
        user_id = redis_client.get(f"twitter_oauth_state:{state}")
        if not user_id:
            raise ValueError("Invalid or expired state")

        auth = tweepy.OAuth2UserHandler(
            client_id=os.getenv('TWITTER_CLIENT_ID'),
            redirect_uri=url_for('twitter_callback', _external=True),
            client_secret=os.getenv('TWITTER_CLIENT_SECRET')
        )

        # Get access token
        auth.fetch_token(code)

        # Get user info
        api = tweepy.API(auth)
        twitter_user = api.verify_credentials()

        # Save to database
        social_account = SocialAccount(
            user_id=user_id,
            platform='twitter',
            platform_user_id=str(twitter_user.id),
            platform_username=twitter_user.screen_name,
            access_token=auth.access_token,
            refresh_token=auth.refresh_token,
            token_expires_at=datetime.now() + timedelta(seconds=auth.expires_in)
        )
        db.session.add(social_account)
        db.session.commit()

        return social_account

@app.route('/api/oauth/twitter/authorize')
@jwt_required()
def twitter_authorize():
    user_id = get_jwt_identity()
    auth_url = TwitterService.get_authorization_url(user_id)
    return jsonify({'auth_url': auth_url})

@app.route('/api/oauth/twitter/callback')
def twitter_callback():
    code = request.args.get('code')
    state = request.args.get('state')

    try:
        social_account = TwitterService.handle_callback(code, state)
        # Redirect to frontend success page
        return redirect('http://localhost:3000/settings/connections?success=twitter')
    except Exception as e:
        return redirect('http://localhost:3000/settings/connections?error=twitter')
```

**Days 5-7: Core Post API**

```python
@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.json

    post = Post(
        user_id=user_id,
        content=data['content'],
        scheduled_time=data.get('scheduled_time'),
        status='draft' if data.get('scheduled_time') else 'published',
        publish_to_platforms=json.dumps(data['platforms'])
    )

    db.session.add(post)
    db.session.commit()

    # If immediate publish
    if post.status == 'published':
        # Queue Celery task
        publish_post.delay(str(post.id))

    return jsonify({'post_id': str(post.id)}), 201

@app.route('/api/posts', methods=['GET'])
@jwt_required()
def get_posts():
    user_id = get_jwt_identity()
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()

    return jsonify([{
        'id': str(p.id),
        'content': p.content,
        'status': p.status,
        'scheduled_time': p.scheduled_time.isoformat() if p.scheduled_time else None,
        'platforms': json.loads(p.publish_to_platforms)
    } for p in posts])
```

---

### **WEEK 2: Platform Integrations**

**Days 8-10: Twitter + LinkedIn Publishing**

**Complete publishing logic in:** `MVP_TECHNICAL_SPEC.md` (lines 650-850)

**Celery task for publishing:**
```python
from celery import Celery
from anthropic import Anthropic

celery = Celery('tasks', broker=os.getenv('REDIS_URL'))

@celery.task
def publish_post(post_id):
    """Publish to all selected platforms"""
    post = Post.query.get(post_id)
    platforms = json.loads(post.publish_to_platforms)

    for platform in platforms:
        # Create platform-specific post
        platform_post = PlatformPost(
            post_id=post.id,
            platform=platform,
            publish_status='pending'
        )
        db.session.add(platform_post)
        db.session.commit()

        # Optimize content for platform using Claude
        optimized_content = optimize_content_for_platform(
            post.content,
            platform
        )
        platform_post.content = optimized_content
        db.session.commit()

        # Publish to platform
        if platform == 'twitter':
            publish_to_twitter.delay(str(platform_post.id))
        elif platform == 'linkedin':
            publish_to_linkedin.delay(str(platform_post.id))
        # ... other platforms

@celery.task
def publish_to_twitter(platform_post_id):
    """Publish to Twitter"""
    platform_post = PlatformPost.query.get(platform_post_id)
    post = Post.query.get(platform_post.post_id)

    # Get user's Twitter account
    social_account = SocialAccount.query.filter_by(
        user_id=post.user_id,
        platform='twitter',
        is_active=True
    ).first()

    if not social_account:
        platform_post.publish_status = 'failed'
        platform_post.error_message = 'No Twitter account connected'
        db.session.commit()
        return

    # Publish tweet
    auth = tweepy.OAuth2UserHandler(
        client_id=os.getenv('TWITTER_CLIENT_ID'),
        client_secret=os.getenv('TWITTER_CLIENT_SECRET')
    )
    auth.access_token = social_account.access_token

    api = tweepy.API(auth)

    try:
        tweet = api.update_status(status=platform_post.content)

        platform_post.platform_post_id = str(tweet.id)
        platform_post.publish_status = 'published'
        platform_post.published_at = datetime.now()
        db.session.commit()

    except Exception as e:
        platform_post.publish_status = 'failed'
        platform_post.error_message = str(e)
        db.session.commit()

def optimize_content_for_platform(content, platform):
    """Use Claude to optimize content for specific platform"""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    platform_guidelines = {
        'twitter': {'char_limit': 280, 'style': 'concise, punchy, hashtags'},
        'linkedin': {'char_limit': 3000, 'style': 'professional, thought leadership'},
        'instagram': {'char_limit': 2200, 'style': 'visual, storytelling, emojis'},
        'facebook': {'char_limit': 63206, 'style': 'conversational, engaging'},
    }

    guidelines = platform_guidelines.get(platform, {})

    prompt = f"""Optimize this social media post for {platform}:

Original post:
{content}

Platform: {platform}
Character limit: {guidelines.get('char_limit', 'no limit')}
Style: {guidelines.get('style', 'engaging')}

Rules:
- Keep the core message
- Adapt tone for platform
- Stay within character limit
- Add platform-appropriate formatting (hashtags, emojis if appropriate)

Return ONLY the optimized post content, nothing else."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()
```

**Days 11-14: Instagram, Facebook, TikTok, YouTube**

Similar OAuth + publishing flows for remaining platforms.

**See complete implementations in:** `MVP_TECHNICAL_SPEC.md`

---

### **WEEK 3: Frontend**

**Days 15-17: Post Editor + Scheduler**

**React post editor:**
```javascript
import { useState } from 'react';
import axios from 'axios';

export default function PostEditor() {
  const [content, setContent] = useState('');
  const [platforms, setPlatforms] = useState([]);
  const [scheduledTime, setScheduledTime] = useState(null);

  const handlePublish = async () => {
    try {
      await axios.post('/api/posts', {
        content,
        platforms,
        scheduled_time: scheduledTime
      }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });

      alert(scheduledTime ? 'Post scheduled!' : 'Post published!');
      setContent('');
      setPlatforms([]);
      setScheduledTime(null);
    } catch (error) {
      alert('Failed to publish');
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Create Post</h2>

      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="What's on your mind?"
        className="w-full h-40 p-4 border rounded-lg mb-4"
      />

      <div className="mb-4">
        <h3 className="font-semibold mb-2">Publish to:</h3>
        {['twitter', 'linkedin', 'instagram', 'facebook'].map(platform => (
          <label key={platform} className="inline-flex items-center mr-4">
            <input
              type="checkbox"
              checked={platforms.includes(platform)}
              onChange={(e) => {
                if (e.target.checked) {
                  setPlatforms([...platforms, platform]);
                } else {
                  setPlatforms(platforms.filter(p => p !== platform));
                }
              }}
              className="mr-2"
            />
            {platform.charAt(0).toUpperCase() + platform.slice(1)}
          </label>
        ))}
      </div>

      <div className="mb-4">
        <label className="block font-semibold mb-2">Schedule (optional):</label>
        <input
          type="datetime-local"
          value={scheduledTime || ''}
          onChange={(e) => setScheduledTime(e.target.value)}
          className="border rounded px-3 py-2"
        />
      </div>

      <button
        onClick={handlePublish}
        className="bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold"
        disabled={!content || platforms.length === 0}
      >
        {scheduledTime ? 'Schedule Post' : 'Publish Now'}
      </button>
    </div>
  );
}
```

**Days 18-21: Platform Connections Page + Queue Management**

OAuth connection UI + post queue/calendar view

---

### **WEEK 4: Billing + Launch**

**Days 22-23: Stripe Integration**

**See complete Stripe setup in:** `MVP_TECHNICAL_SPEC.md` (lines 450-550)

**Quick Stripe:**
```python
@app.route('/api/billing/create-checkout', methods=['POST'])
@jwt_required()
def create_checkout():
    user_id = get_jwt_identity()
    tier = request.json.get('tier', 'pro')

    price_ids = {
        'starter': 'price_starter_39',
        'pro': 'price_pro_79',
        'business': 'price_business_199'
    }

    session = stripe.checkout.Session.create(
        customer_email=User.query.get(user_id).email,
        payment_method_types=['card'],
        line_items=[{'price': price_ids[tier], 'quantity': 1}],
        mode='subscription',
        success_url='http://localhost:3000/billing/success',
        cancel_url='http://localhost:3000/billing/cancel',
    )

    return jsonify({'checkout_url': session.url})
```

**Days 24-26: Testing + Bug Fixes**

**Days 27-28: Deploy + Beta Launch**

```bash
# Deploy backend to Railway
railway init
railway up

# Deploy frontend to Vercel
npm run build
vercel --prod

# Set environment variables in Railway dashboard
```

---

## 🚀 LAUNCH CHECKLIST

**Platform Integrations:**
- [ ] Twitter OAuth working
- [ ] LinkedIn OAuth working
- [ ] Instagram OAuth working
- [ ] Facebook OAuth working
- [ ] TikTok OAuth working (optional for MVP)
- [ ] YouTube OAuth working (optional for MVP)

**Core Features:**
- [ ] Post creation working
- [ ] Content optimization (Claude) working
- [ ] Scheduling working
- [ ] Multi-platform posting working
- [ ] Queue management working

**Business:**
- [ ] Stripe billing working
- [ ] Pricing tiers defined ($39-199/mo)
- [ ] Landing page deployed
- [ ] 10+ beta testers recruited

**Deploy:**
- [ ] Backend deployed (Railway)
- [ ] Frontend deployed (Vercel)
- [ ] Database hosted (Railway PostgreSQL)
- [ ] Redis hosted (Railway Redis)
- [ ] Celery workers running
- [ ] Environment variables set

---

## 📊 SUCCESS METRICS (WEEK 1)

**Minimum viable launch:**
- ✅ 20+ paid users ($800+ MRR)
- ✅ 500+ posts published across platforms
- ✅ 4+ platforms actively used
- ✅ < 5% post failure rate

---

## 💰 REVENUE TIMELINE

**Month 1:** $4.7K MRR (60 users @ $79 avg)
**Month 3:** $11.9K MRR (150 users)
**Month 6:** $55.3K MRR (700 users)
**Month 12:** $158K MRR (2,000 users)

**Year 1 Total Revenue:** $808.2K

---

## 🔗 FULL DOCUMENTATION

**Complete technical spec (900 lines):**
`MODULES/AUTOMATION/social_media_automation/MVP_TECHNICAL_SPEC.md`

**Includes:**
- Complete database schemas (11 tables)
- OAuth flows for all 6 platforms
- Full API documentation
- React component library
- Celery task queue implementation
- Claude content optimization
- Deployment guides

**Strategic assessment:**
`MODULES/AUTOMATION/social_media_automation/DEPLOYMENT_PACKAGE.md`

---

## ⚠️ COMMON CHALLENGES

**OAuth is complex:**
- Test each platform individually
- Use Postman to debug OAuth flows
- Handle token refresh properly

**Rate limits:**
- Twitter: 50 tweets/day (user limit)
- LinkedIn: Varies by account type
- Build retry logic with exponential backoff

**Platform API changes:**
- Monitor developer forums
- Version your API calls
- Have fallback strategies

---

**Prepared by:** C1 - The Mechanic
**For:** 28-day MVP development sprint
**Difficulty:** Hard (complex OAuth, multiple APIs)

**Ready to build? Start with Week 1 database + OAuth setup using the technical spec.**
