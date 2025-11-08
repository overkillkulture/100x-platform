# 📱 SOCIAL MEDIA AUTOMATION MVP - TECHNICAL SPECIFICATION

**Target Launch:** December 9, 2025 (4 weeks)
**Development Time:** 4 weeks
**Complexity:** Medium-High
**Priority:** CRITICAL ("DOMINO 1")

---

## 🎯 MVP SCOPE

### **INCLUDED in 4-Week MVP:**
✅ Web dashboard (upload, post, schedule)
✅ Multi-platform posting (6 platforms: Twitter, Instagram, TikTok, LinkedIn, Facebook, YouTube)
✅ AI content optimization (Claude AI adapts content per platform)
✅ Basic scheduling (date/time picker)
✅ Simple queue system
✅ User authentication (JWT)
✅ Stripe billing (3 tiers: Starter/Pro/Business)
✅ Basic analytics (follower count, post history)
✅ Platform account connections (OAuth)
✅ Content library (save drafts)

### **EXCLUDED from MVP (Add in v2.0):**
❌ Growth automation (likes, comments, follows) (v2.0 - Week 5-6)
❌ Advanced analytics (drop-off, engagement rate) (v2.1 - Week 7-8)
❌ Optimal time detection (AI analyzes best times) (v2.2 - Week 9)
❌ Bulk CSV upload (v2.3 - Week 10)
❌ Team collaboration (v2.4 - Week 11)
❌ White-label reports (v2.5 - Week 12)
❌ API access (v2.6 - Week 13+)

---

## 🗄️ DATABASE SCHEMA

### **PostgreSQL Schema:**

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    email_verified BOOLEAN DEFAULT FALSE,
    stripe_customer_id VARCHAR(255),
    subscription_tier VARCHAR(50) DEFAULT 'free', -- free, starter, pro, business
    subscription_status VARCHAR(50) DEFAULT 'inactive', -- active, inactive, cancelled, past_due
    subscription_end_date TIMESTAMP,
    posts_this_month INTEGER DEFAULT 0,
    posts_limit_per_month INTEGER DEFAULT 10, -- Free tier limit
    connected_accounts_count INTEGER DEFAULT 0,
    INDEX idx_email (email),
    INDEX idx_stripe_customer (stripe_customer_id)
);

-- Social Accounts table (user's connected platforms)
CREATE TABLE social_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- twitter, instagram, tiktok, linkedin, facebook, youtube
    platform_user_id VARCHAR(255),
    platform_username VARCHAR(255),
    platform_display_name VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    last_synced_at TIMESTAMP,
    follower_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, platform, platform_user_id),
    INDEX idx_user (user_id),
    INDEX idx_platform (platform),
    INDEX idx_active (is_active)
);

-- Posts table
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    content TEXT NOT NULL,
    media_urls TEXT[], -- Array of media file URLs (images, videos)
    media_types VARCHAR(50)[], -- Array of media types (image, video)
    platforms VARCHAR(50)[] NOT NULL, -- Array of target platforms
    status VARCHAR(50) DEFAULT 'draft', -- draft, scheduled, publishing, published, failed
    scheduled_for TIMESTAMP,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_scheduled (scheduled_for),
    INDEX idx_published (published_at)
);

-- Platform Posts table (individual posts per platform)
CREATE TABLE platform_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    social_account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    content TEXT NOT NULL, -- Platform-optimized content
    media_urls TEXT[],
    status VARCHAR(50) DEFAULT 'pending', -- pending, publishing, published, failed
    platform_post_id VARCHAR(255), -- ID from platform API
    platform_url TEXT, -- URL to published post
    error_message TEXT,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_post (post_id),
    INDEX idx_platform (platform),
    INDEX idx_status (status)
);

-- Analytics table (basic stats per platform post)
CREATE TABLE post_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform_post_id UUID REFERENCES platform_posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50),
    impressions INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2) DEFAULT 0.00,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_platform_post (platform_post_id),
    INDEX idx_user (user_id),
    INDEX idx_platform (platform)
);

-- Content Library (saved drafts, templates)
CREATE TABLE content_library (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    content TEXT NOT NULL,
    media_urls TEXT[],
    tags VARCHAR(100)[],
    is_template BOOLEAN DEFAULT FALSE,
    template_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_template (is_template)
);

-- Subscription Plans table
CREATE TABLE subscription_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    price_monthly INTEGER NOT NULL, -- In cents
    price_yearly INTEGER,
    stripe_price_id VARCHAR(255),
    posts_per_month INTEGER, -- -1 = unlimited
    connected_accounts_limit INTEGER,
    features JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default plans
INSERT INTO subscription_plans (name, slug, price_monthly, posts_per_month, connected_accounts_limit, features) VALUES
('Free', 'free', 0, 10, 2, '["basic_posting", "2_platforms", "manual_scheduling"]'),
('Starter', 'starter', 2900, 30, 3, '["basic_posting", "3_platforms", "scheduling", "ai_optimization", "email_support"]'),
('Pro', 'pro', 7900, -1, 10, '["unlimited_posts", "10_platforms", "scheduling", "ai_optimization", "analytics", "priority_support"]'),
('Business', 'business', 19900, -1, 25, '["unlimited_posts", "25_platforms", "scheduling", "ai_optimization", "advanced_analytics", "team_collaboration", "dedicated_support"]');

-- Stripe Webhook Logs
CREATE TABLE stripe_webhook_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100),
    event_data JSONB,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_processed (processed)
);

-- Queue/Scheduler table
CREATE TABLE scheduled_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    scheduled_for TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
    celery_task_id VARCHAR(255),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_scheduled (scheduled_for),
    INDEX idx_status (status)
);

-- Usage tracking
CREATE TABLE usage_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100), -- post_created, post_published, ai_optimization
    platform VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_created (created_at)
);
```

---

## 🏗️ BACKEND ARCHITECTURE

### **Tech Stack:**

```
Framework: Flask (Python 3.11+) or FastAPI
Database: PostgreSQL 14+
Cache: Redis 7+
Task Queue: Celery with Redis broker
File Storage: AWS S3
API: RESTful JSON API
Auth: JWT (PyJWT)
Payment: Stripe Python SDK
AI: Anthropic Claude API (content optimization)
Social Media APIs:
  - Twitter: Tweepy
  - Instagram: Instagram Graph API
  - TikTok: TikTok API (or Playwright)
  - LinkedIn: LinkedIn API
  - Facebook: Facebook Graph API
  - YouTube: YouTube Data API
```

### **Project Structure:**

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── user.py
│   │   ├── social_account.py
│   │   ├── post.py
│   │   ├── platform_post.py
│   │   └── subscription.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── social_accounts.py
│   │   ├── posts.py
│   │   ├── analytics.py
│   │   ├── billing.py
│   │   └── webhooks.py
│   ├── services/
│   │   ├── content_optimizer.py (Claude AI)
│   │   ├── twitter_service.py
│   │   ├── instagram_service.py
│   │   ├── tiktok_service.py
│   │   ├── linkedin_service.py
│   │   ├── facebook_service.py
│   │   ├── youtube_service.py
│   │   ├── s3_service.py
│   │   └── stripe_service.py
│   ├── tasks/
│   │   ├── posting_tasks.py
│   │   └── analytics_tasks.py
│   └── utils/
│       ├── auth.py
│       └── validators.py
├── requirements.txt
└── wsgi.py
```

---

## 🎨 FRONTEND ARCHITECTURE

### **Tech Stack:**

```
Framework: React 18
State: Redux Toolkit
Routing: React Router v6
Styling: Tailwind CSS
UI Components: Headless UI
HTTP Client: Axios
Build: Vite
```

### **Project Structure:**

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   ├── layout/
│   │   ├── auth/
│   │   ├── posts/
│   │   │   ├── PostCreate.jsx
│   │   │   ├── PostList.jsx
│   │   │   ├── PostEditor.jsx
│   │   │   └── MediaUpload.jsx
│   │   ├── scheduling/
│   │   │   ├── Calendar.jsx
│   │   │   └── Queue.jsx
│   │   ├── platforms/
│   │   │   ├── PlatformConnect.jsx
│   │   │   └── PlatformList.jsx
│   │   ├── analytics/
│   │   │   ├── Dashboard.jsx
│   │   │   └── Charts.jsx
│   │   └── billing/
│   │       ├── PricingPlans.jsx
│   │       └── Checkout.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── Posts.jsx
│   │   ├── Schedule.jsx
│   │   ├── Analytics.jsx
│   │   ├── Platforms.jsx
│   │   ├── Settings.jsx
│   │   └── Billing.jsx
│   ├── store/
│   │   ├── slices/
│   │   │   ├── authSlice.js
│   │   │   ├── postsSlice.js
│   │   │   ├── platformsSlice.js
│   │   │   └── analyticsSlice.js
│   │   └── api.js
│   └── App.jsx
└── package.json
```

---

## 🔌 API ENDPOINTS

### **Authentication:**
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/refresh
GET    /api/auth/me
```

### **Social Accounts (Platform Connections):**
```
GET    /api/social-accounts              - List user's connected accounts
POST   /api/social-accounts/connect      - Initiate OAuth flow
GET    /api/social-accounts/callback     - OAuth callback
DELETE /api/social-accounts/:id          - Disconnect account
POST   /api/social-accounts/:id/refresh  - Refresh access token
GET    /api/social-accounts/:id/stats    - Get platform stats
```

### **Posts:**
```
GET    /api/posts                  - List user's posts
POST   /api/posts                  - Create new post
GET    /api/posts/:id              - Get post details
PUT    /api/posts/:id              - Update post
DELETE /api/posts/:id              - Delete post
POST   /api/posts/:id/publish      - Publish now
POST   /api/posts/:id/schedule     - Schedule for later
POST   /api/posts/:id/optimize     - AI optimize content
POST   /api/posts/upload-media     - Upload image/video
```

### **Analytics:**
```
GET    /api/analytics/overview     - Dashboard stats
GET    /api/analytics/posts/:id    - Post-specific analytics
GET    /api/analytics/platforms    - Platform breakdown
```

### **Billing:**
```
GET    /api/billing/plans          - Get subscription plans
POST   /api/billing/checkout       - Create checkout session
POST   /api/billing/portal         - Customer portal link
GET    /api/billing/subscription   - Get subscription status
POST   /api/webhooks/stripe        - Stripe webhooks
```

---

## 🔐 OAUTH FLOW (Platform Connections)

### **Twitter OAuth 2.0:**
```
1. User clicks "Connect Twitter"
   ↓
2. Backend generates OAuth URL with state token
   ↓
3. User redirects to Twitter authorization page
   ↓
4. User approves
   ↓
5. Twitter redirects to callback URL with code
   ↓
6. Backend exchanges code for access token
   ↓
7. Backend saves token to social_accounts table
   ↓
8. Redirect user back to dashboard
```

### **Implementation:**

```python
# services/twitter_service.py

import tweepy
from flask import current_app, url_for

class TwitterService:

    @staticmethod
    def get_authorization_url(user_id):
        """Generate Twitter OAuth URL"""

        auth = tweepy.OAuth2UserHandler(
            client_id=current_app.config['TWITTER_CLIENT_ID'],
            redirect_uri=url_for('api.twitter_callback', _external=True),
            scope=["tweet.read", "tweet.write", "users.read"],
            client_secret=current_app.config['TWITTER_CLIENT_SECRET']
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
        """Handle OAuth callback"""

        # Verify state
        user_id = redis_client.get(f"twitter_oauth_state:{state}")
        if not user_id:
            raise ValueError("Invalid state")

        # Exchange code for token
        auth = tweepy.OAuth2UserHandler(
            client_id=current_app.config['TWITTER_CLIENT_ID'],
            redirect_uri=url_for('api.twitter_callback', _external=True),
            scope=["tweet.read", "tweet.write", "users.read"],
            client_secret=current_app.config['TWITTER_CLIENT_SECRET']
        )

        access_token = auth.fetch_token(code)

        # Get user info
        client = tweepy.Client(bearer_token=access_token['access_token'])
        me = client.get_me()

        # Save to database
        social_account = SocialAccount(
            user_id=user_id,
            platform='twitter',
            platform_user_id=me.data.id,
            platform_username=me.data.username,
            platform_display_name=me.data.name,
            access_token=access_token['access_token'],
            refresh_token=access_token.get('refresh_token'),
            token_expires_at=access_token.get('expires_at')
        )
        social_account.save()

        return social_account

    @staticmethod
    def post_tweet(social_account_id, content, media_ids=None):
        """Post tweet"""

        account = SocialAccount.query.get(social_account_id)
        if not account:
            raise ValueError("Account not found")

        client = tweepy.Client(bearer_token=account.access_token)

        response = client.create_tweet(
            text=content,
            media_ids=media_ids
        )

        return {
            'platform_post_id': response.data['id'],
            'platform_url': f"https://twitter.com/{account.platform_username}/status/{response.data['id']}"
        }
```

---

## 📝 POSTING FLOW

### **Create & Publish Post:**

```
1. User creates post in dashboard
   - Enters content
   - Uploads media (optional)
   - Selects platforms (Twitter, Instagram, etc)
   ↓
2. Frontend sends POST /api/posts
   ↓
3. Backend creates post record (status='draft')
   ↓
4. User clicks "Optimize with AI"
   ↓
5. POST /api/posts/:id/optimize
   ↓
6. Claude AI optimizes content for each platform:
   - Twitter: 280 chars, punchy, hashtags
   - Instagram: Longer caption, emojis, 30 hashtags
   - LinkedIn: Professional tone, 3000 chars
   - TikTok: Short, trending hashtags
   ↓
7. Frontend displays optimized versions
   ↓
8. User reviews and edits (optional)
   ↓
9. User clicks "Publish Now" or "Schedule"
   ↓
10. Backend creates Celery task: publish_post(post_id)
   ↓
11. Celery worker publishes to each platform in parallel
   ↓
12. Each platform_post record created with status
   ↓
13. User sees real-time status updates (via polling or websocket)
```

### **Celery Task:**

```python
# tasks/posting_tasks.py

from celery import shared_task, group
from app.services.twitter_service import TwitterService
from app.services.instagram_service import InstagramService
# ... other services
from app.models.post import Post, PlatformPost

@shared_task
def publish_post(post_id):
    """Publish post to all selected platforms"""

    post = Post.query.get(post_id)
    if not post:
        return {"error": "Post not found"}

    post.status = 'publishing'
    post.save()

    # Create subtasks for each platform
    platform_tasks = []

    for platform in post.platforms:
        platform_tasks.append(
            publish_to_platform.s(post_id, platform)
        )

    # Execute all platform tasks in parallel
    job = group(platform_tasks)
    result = job.apply_async()

    return {"status": "publishing", "task_id": result.id}


@shared_task
def publish_to_platform(post_id, platform):
    """Publish to specific platform"""

    post = Post.query.get(post_id)
    if not post:
        return {"error": "Post not found"}

    # Get user's connected account for this platform
    social_account = SocialAccount.query.filter_by(
        user_id=post.user_id,
        platform=platform,
        is_active=True
    ).first()

    if not social_account:
        return {"error": f"No connected {platform} account"}

    # Get platform-optimized content
    platform_post = PlatformPost.query.filter_by(
        post_id=post_id,
        platform=platform
    ).first()

    if not platform_post:
        # Create platform post if doesn't exist
        platform_post = PlatformPost(
            post_id=post_id,
            user_id=post.user_id,
            social_account_id=social_account.id,
            platform=platform,
            content=post.content,  # Will be optimized
            media_urls=post.media_urls
        )
        platform_post.save()

    try:
        # Publish based on platform
        if platform == 'twitter':
            result = TwitterService.post_tweet(
                social_account.id,
                platform_post.content,
                media_ids=platform_post.media_urls
            )
        elif platform == 'instagram':
            result = InstagramService.post(
                social_account.id,
                platform_post.content,
                media_urls=platform_post.media_urls
            )
        # ... other platforms

        # Update platform_post record
        platform_post.status = 'published'
        platform_post.platform_post_id = result['platform_post_id']
        platform_post.platform_url = result['platform_url']
        platform_post.published_at = datetime.utcnow()
        platform_post.save()

        return {"status": "success", "platform": platform, "url": result['platform_url']}

    except Exception as e:
        platform_post.status = 'failed'
        platform_post.error_message = str(e)
        platform_post.save()

        return {"status": "failed", "platform": platform, "error": str(e)}
```

---

## 🤖 AI CONTENT OPTIMIZATION

```python
# services/content_optimizer.py

import anthropic
from flask import current_app

class ContentOptimizer:

    def __init__(self):
        self.claude = anthropic.Anthropic(
            api_key=current_app.config['ANTHROPIC_API_KEY']
        )

    def optimize_for_platform(self, content, platform, media_count=0):
        """Optimize content for specific platform"""

        platform_guidelines = {
            'twitter': {
                'char_limit': 280,
                'style': 'Short, punchy, use hashtags sparingly (2-3), engage with questions',
                'hashtags': True
            },
            'instagram': {
                'char_limit': 2200,
                'style': 'Engaging caption, storytelling, use emojis, call-to-action, 20-30 hashtags',
                'hashtags': True
            },
            'tiktok': {
                'char_limit': 150,
                'style': 'Very short, attention-grabbing, trending hashtags, challenges',
                'hashtags': True
            },
            'linkedin': {
                'char_limit': 3000,
                'style': 'Professional, insightful, business value, storytelling, thought leadership',
                'hashtags': True
            },
            'facebook': {
                'char_limit': 63206,
                'style': 'Conversational, engaging, ask questions, community-focused',
                'hashtags': False
            },
            'youtube': {
                'char_limit': 5000,
                'style': 'SEO-optimized title and description, keywords, timestamps',
                'hashtags': False
            }
        }

        guideline = platform_guidelines.get(platform, {})
        char_limit = guideline.get('char_limit', 280)
        style = guideline.get('style', '')

        prompt = f"""Optimize this social media post for {platform}:

Original content:
{content}

Platform: {platform}
Character limit: {char_limit}
Style guidelines: {style}
Media attached: {media_count} file(s)

IMPORTANT:
- Adapt the tone and style for {platform}
- Stay within {char_limit} characters
- Make it engaging and platform-appropriate
- Include relevant hashtags if appropriate for {platform}
- Preserve the core message

Return ONLY the optimized post content, nothing else."""

        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        optimized_content = response.content[0].text.strip()

        # Ensure character limit
        if len(optimized_content) > char_limit:
            optimized_content = optimized_content[:char_limit-3] + "..."

        return optimized_content
```

---

## ⏱️ 4-WEEK DEVELOPMENT TIMELINE

### **Week 1: Backend Foundation**
**Day 1-2:** Database & Models
- PostgreSQL setup
- Create all tables
- SQLAlchemy models
- Migrations

**Day 3-4:** Authentication
- JWT implementation
- Registration/login
- Email verification
- Password reset

**Day 5-7:** Core API Endpoints
- Posts CRUD
- Social accounts CRUD
- Media upload (S3)
- Basic tests

### **Week 2: Platform Integrations**
**Day 8-9:** OAuth Implementation
- Twitter OAuth
- LinkedIn OAuth
- Facebook OAuth
- Token storage/refresh

**Day 10-11:** Posting Services
- Twitter posting
- Instagram posting (Graph API)
- TikTok posting
- LinkedIn posting

**Day 12-14:** AI & Testing
- Claude AI content optimizer
- Celery task queue
- Platform posting tasks
- Integration tests

### **Week 3: Frontend Dashboard**
**Day 15-16:** Core UI
- React app setup
- Login/signup pages
- Dashboard layout
- Navigation

**Day 17-18:** Post Creation
- Post editor component
- Media upload
- Platform selection
- Preview

**Day 19-21:** Scheduling & Queue
- Calendar component
- Schedule picker
- Queue management
- Real-time status updates

### **Week 4: Polish & Launch**
**Day 22-23:** Analytics & Billing
- Basic analytics dashboard
- Stripe checkout
- Subscription management
- Usage tracking

**Day 24-25:** Polish
- Responsive design
- Error handling
- Loading states
- Toasts/notifications

**Day 26-28:** Testing & Launch
- Beta testing (10 users)
- Bug fixes
- Performance optimization
- Deploy to production
- Launch!

---

## 💰 PRICING & TIERS

```
STARTER: $29/month
- 3 connected accounts
- 30 posts per month
- AI content optimization
- Basic scheduling
- Email support

PRO: $79/month ⭐ MOST POPULAR
- 10 connected accounts
- Unlimited posts
- AI content optimization
- Advanced scheduling
- Basic analytics
- Priority support

BUSINESS: $199/month
- 25 connected accounts
- Unlimited posts
- AI content optimization
- Advanced scheduling
- Advanced analytics
- Team collaboration (3 seats)
- API access
- Dedicated support
```

---

## 🧪 TESTING CHECKLIST

### **Backend:**
- [ ] User authentication
- [ ] OAuth flows (all platforms)
- [ ] Post creation/editing
- [ ] AI content optimization
- [ ] Platform posting (all 6 platforms)
- [ ] Scheduling tasks
- [ ] Stripe billing
- [ ] Analytics collection

### **Frontend:**
- [ ] Login/signup flow
- [ ] Platform connections
- [ ] Post creation
- [ ] Media upload
- [ ] Scheduling interface
- [ ] Queue management
- [ ] Analytics display
- [ ] Billing/pricing
- [ ] Responsive design

---

## 🚀 DEPLOYMENT

```
Backend: DigitalOcean App Platform (Docker)
Database: DigitalOcean Managed PostgreSQL
Redis: DigitalOcean Managed Redis
Storage: AWS S3
Frontend: Vercel
CDN: CloudFront

Estimated Monthly Cost (1000 users):
- Infrastructure: $150/mo
- API costs (Claude): $500/mo
- Total: $650/mo

Revenue (1000 users, 50% Pro):
- 500 Pro × $79 = $39,500/mo
- Profit: $38,850/mo (98% margin)
```

---

**Technical Spec Prepared by:** C1 - The Mechanic
**Date:** November 8, 2025
**Status:** ✅ READY FOR DEVELOPMENT

**Next Step:** Start Week 1 development on Monday, November 18, 2025

📱⚡🚀
```
