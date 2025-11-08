# 🎙️ PODCAST PRODUCTION MVP - TECHNICAL SPECIFICATION

**Target Launch:** November 25, 2025 (2 weeks)
**Development Time:** 2 weeks
**Complexity:** Medium
**Priority:** HIGH ("EASY WIN")

---

## 🎯 MVP SCOPE

### **INCLUDED in 2-Week MVP:**
✅ Browser-based recording (single-track)
✅ Upload existing audio files
✅ AI audio processing (noise removal, loudness, silences)
✅ AI transcription (Whisper API)
✅ AI show notes (Claude AI)
✅ RSS feed generation
✅ User authentication (JWT)
✅ Stripe billing (3 tiers)
✅ Basic web dashboard
✅ Episode management

### **EXCLUDED from MVP (Add in v2.0):**
❌ Multi-track recording (v2.0 - Week 3)
❌ Remote guest links (v2.0 - Week 3)
❌ Platform API integrations (Spotify, Apple, etc) (v2.1 - Week 4-5)
❌ Video podcast support (v2.2 - Week 6-8)
❌ Analytics dashboard (v2.3 - Week 9)
❌ Guest management system (v2.4 - Week 10)

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
    subscription_tier VARCHAR(50) DEFAULT 'free', -- free, creator, pro, network
    subscription_status VARCHAR(50) DEFAULT 'inactive', -- active, inactive, cancelled, past_due
    subscription_end_date TIMESTAMP,
    storage_used_gb DECIMAL(10,2) DEFAULT 0,
    recording_minutes_used INTEGER DEFAULT 0,
    recording_minutes_limit INTEGER DEFAULT 120, -- 2 hours for free tier
    INDEX idx_email (email),
    INDEX idx_stripe_customer (stripe_customer_id)
);

-- Podcasts table
CREATE TABLE podcasts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    author VARCHAR(255),
    category VARCHAR(100),
    language VARCHAR(10) DEFAULT 'en',
    artwork_url TEXT,
    website_url TEXT,
    rss_url TEXT,
    is_explicit BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'draft', -- draft, published, archived
    INDEX idx_user (user_id),
    INDEX idx_status (status)
);

-- Episodes table
CREATE TABLE episodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    podcast_id UUID REFERENCES podcasts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    episode_number INTEGER,
    season_number INTEGER,
    audio_file_path TEXT,
    audio_file_size_bytes BIGINT,
    audio_file_url TEXT,
    duration_seconds INTEGER,
    transcript TEXT,
    transcript_json JSONB, -- Full transcript with timestamps
    show_notes TEXT,
    show_notes_json JSONB, -- Structured show notes
    artwork_url TEXT,
    published_at TIMESTAMP,
    scheduled_for TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'draft', -- draft, processing, published, scheduled
    processing_status VARCHAR(50), -- uploading, transcribing, editing, complete, error
    processing_error TEXT,
    INDEX idx_podcast (podcast_id),
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_published (published_at),
    INDEX idx_scheduled (scheduled_for)
);

-- Audio Processing Jobs table
CREATE TABLE audio_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    episode_id UUID REFERENCES episodes(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_type VARCHAR(50) NOT NULL, -- upload, transcribe, edit, export
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, complete, failed
    input_file_path TEXT,
    output_file_path TEXT,
    processing_options JSONB, -- {remove_noise: true, remove_silences: true, etc}
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    celery_task_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_episode (episode_id),
    INDEX idx_status (status),
    INDEX idx_celery_task (celery_task_id)
);

-- Subscription Plans table
CREATE TABLE subscription_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL, -- Free, Creator, Pro, Network
    slug VARCHAR(50) UNIQUE NOT NULL,
    price_monthly INTEGER NOT NULL, -- In cents (1900 = $19.00)
    price_yearly INTEGER, -- In cents, if yearly option
    stripe_price_id VARCHAR(255),
    recording_minutes_per_month INTEGER,
    storage_gb INTEGER,
    max_podcasts INTEGER,
    features JSONB, -- Array of feature flags
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default plans
INSERT INTO subscription_plans (name, slug, price_monthly, recording_minutes_per_month, storage_gb, max_podcasts, features) VALUES
('Free', 'free', 0, 120, 3, 1, '["basic_editing", "ai_transcription", "rss_feed"]'),
('Creator', 'creator', 1900, 600, 50, 1, '["basic_editing", "ai_transcription", "ai_show_notes", "rss_feed", "email_support"]'),
('Pro', 'pro', 4900, -1, 200, 3, '["basic_editing", "advanced_editing", "ai_transcription", "ai_show_notes", "rss_feed", "priority_support", "api_access"]'),
('Network', 'network', 9900, -1, 1000, -1, '["all_features", "team_collaboration", "white_label", "dedicated_support"]');

-- Stripe Webhooks Log table (for debugging)
CREATE TABLE stripe_webhook_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100),
    event_data JSONB,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_type (event_type),
    INDEX idx_processed (processed)
);

-- Usage Tracking table
CREATE TABLE usage_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    episode_id UUID REFERENCES episodes(id) ON DELETE CASCADE,
    action VARCHAR(100), -- record, upload, transcribe, edit
    minutes_recorded INTEGER,
    storage_added_gb DECIMAL(10,2),
    api_calls_made INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_created (created_at)
);
```

---

## 🏗️ BACKEND ARCHITECTURE

### **Tech Stack:**

```
Framework: Flask (Python 3.11+)
Database: PostgreSQL 14+
Cache: Redis 7+
Task Queue: Celery with Redis broker
File Storage: AWS S3
API: RESTful JSON API
Auth: JWT (PyJWT)
Payment: Stripe Python SDK
AI: OpenAI Whisper API, Anthropic Claude API
Audio: FFmpeg
```

### **Project Structure:**

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── podcast.py
│   │   ├── episode.py
│   │   └── subscription.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── podcasts.py
│   │   ├── episodes.py
│   │   ├── recording.py
│   │   ├── billing.py
│   │   └── webhooks.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── audio_processor.py
│   │   ├── transcriber.py
│   │   ├── show_notes_generator.py
│   │   ├── rss_generator.py
│   │   ├── s3_service.py
│   │   └── stripe_service.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── audio_tasks.py
│   │   └── transcription_tasks.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── validators.py
│   └── extensions.py
├── migrations/
├── tests/
├── requirements.txt
├── wsgi.py
└── celery_worker.py
```

---

## 🎨 FRONTEND ARCHITECTURE

### **Tech Stack:**

```
Framework: React 18
State: Redux Toolkit
Routing: React Router v6
Styling: Tailwind CSS
Audio Recording: MediaRecorder API
Audio Player: WaveSurfer.js
HTTP Client: Axios
Build: Vite
```

### **Project Structure:**

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Modal.jsx
│   │   │   └── Spinner.jsx
│   │   ├── layout/
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── Layout.jsx
│   │   ├── auth/
│   │   │   ├── Login.jsx
│   │   │   ├── Signup.jsx
│   │   │   └── ForgotPassword.jsx
│   │   ├── podcast/
│   │   │   ├── PodcastList.jsx
│   │   │   ├── PodcastCreate.jsx
│   │   │   └── PodcastEdit.jsx
│   │   ├── episode/
│   │   │   ├── EpisodeList.jsx
│   │   │   ├── EpisodeCreate.jsx
│   │   │   ├── EpisodeEdit.jsx
│   │   │   └── EpisodePlayer.jsx
│   │   ├── recording/
│   │   │   ├── Recorder.jsx
│   │   │   ├── Uploader.jsx
│   │   │   └── ProcessingStatus.jsx
│   │   └── billing/
│   │       ├── PricingPlans.jsx
│   │       ├── Checkout.jsx
│   │       └── BillingSettings.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   ├── Podcasts.jsx
│   │   ├── Episodes.jsx
│   │   ├── Record.jsx
│   │   ├── Settings.jsx
│   │   └── Billing.jsx
│   ├── store/
│   │   ├── index.js
│   │   ├── slices/
│   │   │   ├── authSlice.js
│   │   │   ├── podcastSlice.js
│   │   │   ├── episodeSlice.js
│   │   │   └── billingSlice.js
│   │   └── api.js
│   ├── utils/
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── recorder.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── package.json
└── vite.config.js
```

---

## 🔌 API ENDPOINTS

### **Authentication:**

```
POST   /api/auth/register          - Register new user
POST   /api/auth/login             - Login user
POST   /api/auth/logout            - Logout user
POST   /api/auth/refresh           - Refresh JWT token
POST   /api/auth/forgot-password   - Request password reset
POST   /api/auth/reset-password    - Reset password
GET    /api/auth/me                - Get current user
```

### **Podcasts:**

```
GET    /api/podcasts               - List user's podcasts
POST   /api/podcasts               - Create new podcast
GET    /api/podcasts/:id           - Get podcast details
PUT    /api/podcasts/:id           - Update podcast
DELETE /api/podcasts/:id           - Delete podcast
GET    /api/podcasts/:id/rss       - Get podcast RSS feed
```

### **Episodes:**

```
GET    /api/podcasts/:id/episodes  - List podcast episodes
POST   /api/podcasts/:id/episodes  - Create new episode
GET    /api/episodes/:id           - Get episode details
PUT    /api/episodes/:id           - Update episode
DELETE /api/episodes/:id           - Delete episode
POST   /api/episodes/:id/publish   - Publish episode
```

### **Recording:**

```
POST   /api/recording/start        - Start recording session
POST   /api/recording/upload       - Upload audio chunk (WebRTC)
POST   /api/recording/finish       - Finalize recording
POST   /api/upload                 - Upload existing audio file
```

### **Audio Processing:**

```
POST   /api/episodes/:id/process   - Start AI processing
GET    /api/episodes/:id/status    - Get processing status
POST   /api/episodes/:id/transcribe - Request transcription
POST   /api/episodes/:id/show-notes - Generate show notes
```

### **Billing:**

```
GET    /api/billing/plans          - Get subscription plans
POST   /api/billing/checkout       - Create Stripe checkout session
POST   /api/billing/portal         - Create Stripe customer portal link
GET    /api/billing/subscription   - Get user's subscription
POST   /api/billing/cancel         - Cancel subscription
POST   /api/webhooks/stripe        - Stripe webhook handler
```

---

## 🔐 AUTHENTICATION FLOW

```
1. User signs up with email/password
   ↓
2. Backend creates user in database
   ↓
3. Backend sends verification email
   ↓
4. User clicks verification link
   ↓
5. User logs in
   ↓
6. Backend generates JWT access token (30 min expiry)
   ↓
7. Backend generates JWT refresh token (7 day expiry)
   ↓
8. Frontend stores tokens in localStorage
   ↓
9. Frontend includes access token in Authorization header
   ↓
10. When access token expires, use refresh token to get new one
```

---

## 🎙️ RECORDING FLOW (WebRTC)

```
1. User clicks "Record" in dashboard
   ↓
2. Frontend requests microphone permission
   ↓
3. MediaRecorder starts capturing audio
   ↓
4. Audio chunks sent to backend every 10 seconds (real-time backup)
   ↓
5. Backend saves chunks to S3
   ↓
6. User clicks "Stop"
   ↓
7. Frontend sends finalize request
   ↓
8. Backend concatenates chunks into single MP3
   ↓
9. Backend creates episode record in database
   ↓
10. Backend triggers Celery task for processing
```

### **WebRTC Implementation:**

```javascript
// Frontend: recorder.js

let mediaRecorder;
let audioChunks = [];

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

  mediaRecorder = new MediaRecorder(stream, {
    mimeType: 'audio/webm',
    audioBitsPerSecond: 128000
  });

  mediaRecorder.ondataavailable = async (event) => {
    if (event.data.size > 0) {
      audioChunks.push(event.data);

      // Upload chunk to backend (every 10 seconds)
      await uploadChunk(event.data);
    }
  };

  mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    await finalizeRecording(audioBlob);
  };

  mediaRecorder.start(10000); // Capture in 10-second chunks
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
  }
}

async function uploadChunk(chunk) {
  const formData = new FormData();
  formData.append('chunk', chunk);

  await axios.post('/api/recording/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
}

async function finalizeRecording(audioBlob) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');

  const response = await axios.post('/api/recording/finish', formData);
  return response.data; // Returns episode ID
}
```

---

## 🤖 AUDIO PROCESSING FLOW (Celery)

```
1. Episode created with audio file
   ↓
2. Celery task triggered: process_episode(episode_id)
   ↓
3. Task 1: Noise Removal (FFmpeg afftdn filter)
   - Input: raw_audio.mp3
   - Output: denoised_audio.mp3
   ↓
4. Task 2: Silence Removal (FFmpeg silenceremove)
   - Input: denoised_audio.mp3
   - Output: trimmed_audio.mp3
   ↓
5. Task 3: Loudness Normalization (FFmpeg loudnorm -16 LUFS)
   - Input: trimmed_audio.mp3
   - Output: normalized_audio.mp3
   ↓
6. Task 4: Transcription (Whisper API)
   - Input: normalized_audio.mp3
   - Output: transcript.json (with timestamps)
   ↓
7. Task 5: Show Notes Generation (Claude AI)
   - Input: transcript.json
   - Output: show_notes.json
   ↓
8. Task 6: Update Episode in Database
   - Save processed audio URL
   - Save transcript
   - Save show notes
   - Set status to 'complete'
   ↓
9. Notify user (email/websocket)
```

### **Celery Task:**

```python
# tasks/audio_tasks.py

from celery import shared_task
from app.services.audio_processor import AudioProcessor
from app.services.transcriber import Transcriber
from app.services.show_notes_generator import ShowNotesGenerator
from app.models.episode import Episode
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_episode(self, episode_id):
    """Process episode: denoise, trim, normalize, transcribe, generate show notes"""

    try:
        episode = Episode.query.get(episode_id)
        if not episode:
            logger.error(f"Episode {episode_id} not found")
            return

        episode.processing_status = 'processing'
        episode.save()

        processor = AudioProcessor()
        transcriber = Transcriber()
        show_notes_gen = ShowNotesGenerator()

        # Step 1: Download audio from S3
        input_file = processor.download_from_s3(episode.audio_file_path)

        # Step 2: Noise removal
        denoised_file = processor.remove_noise(input_file)

        # Step 3: Silence removal
        trimmed_file = processor.remove_silences(denoised_file)

        # Step 4: Loudness normalization
        normalized_file = processor.normalize_loudness(trimmed_file, target_lufs=-16.0)

        # Step 5: Upload processed audio to S3
        processed_url = processor.upload_to_s3(normalized_file, f"processed/{episode_id}.mp3")

        # Step 6: Transcribe
        transcript = transcriber.transcribe(normalized_file)

        # Step 7: Generate show notes
        show_notes = show_notes_gen.generate(transcript, episode.title)

        # Step 8: Update episode
        episode.audio_file_url = processed_url
        episode.transcript = transcript['text']
        episode.transcript_json = transcript
        episode.show_notes = show_notes['raw']
        episode.show_notes_json = show_notes
        episode.processing_status = 'complete'
        episode.save()

        logger.info(f"Episode {episode_id} processed successfully")

        # Cleanup temp files
        processor.cleanup([input_file, denoised_file, trimmed_file, normalized_file])

        return {"status": "success", "episode_id": episode_id}

    except Exception as e:
        logger.error(f"Error processing episode {episode_id}: {str(e)}")
        episode.processing_status = 'error'
        episode.processing_error = str(e)
        episode.save()

        # Retry task
        raise self.retry(exc=e, countdown=60)  # Retry after 60 seconds
```

---

## 💳 STRIPE BILLING FLOW

```
1. User clicks "Upgrade to Pro"
   ↓
2. Frontend requests checkout session from backend
   ↓
3. Backend creates Stripe checkout session
   ↓
4. Backend returns session URL
   ↓
5. Frontend redirects to Stripe checkout page
   ↓
6. User enters payment details
   ↓
7. Stripe processes payment
   ↓
8. Stripe redirects to success URL
   ↓
9. Stripe sends webhook to backend
   ↓
10. Backend updates user subscription in database
   ↓
11. User sees upgraded features in dashboard
```

### **Stripe Integration:**

```python
# services/stripe_service.py

import stripe
from flask import current_app

stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

class StripeService:

    @staticmethod
    def create_checkout_session(user, plan_slug):
        """Create Stripe checkout session for subscription"""

        plan = SubscriptionPlan.query.filter_by(slug=plan_slug).first()
        if not plan:
            raise ValueError("Plan not found")

        session = stripe.checkout.Session.create(
            customer_email=user.email,
            payment_method_types=['card'],
            line_items=[{
                'price': plan.stripe_price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f"{current_app.config['FRONTEND_URL']}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{current_app.config['FRONTEND_URL']}/billing",
            metadata={
                'user_id': str(user.id),
                'plan_slug': plan_slug
            }
        )

        return session.url

    @staticmethod
    def handle_webhook(event_type, event_data):
        """Handle Stripe webhook events"""

        if event_type == 'checkout.session.completed':
            # Subscription created
            session = event_data['object']
            user_id = session['metadata']['user_id']
            plan_slug = session['metadata']['plan_slug']
            customer_id = session['customer']
            subscription_id = session['subscription']

            user = User.query.get(user_id)
            plan = SubscriptionPlan.query.filter_by(slug=plan_slug).first()

            user.stripe_customer_id = customer_id
            user.subscription_tier = plan_slug
            user.subscription_status = 'active'
            user.recording_minutes_limit = plan.recording_minutes_per_month
            user.save()

        elif event_type == 'customer.subscription.deleted':
            # Subscription cancelled
            subscription = event_data['object']
            customer_id = subscription['customer']

            user = User.query.filter_by(stripe_customer_id=customer_id).first()
            if user:
                user.subscription_tier = 'free'
                user.subscription_status = 'cancelled'
                user.recording_minutes_limit = 120
                user.save()

        elif event_type == 'invoice.payment_failed':
            # Payment failed
            invoice = event_data['object']
            customer_id = invoice['customer']

            user = User.query.filter_by(stripe_customer_id=customer_id).first()
            if user:
                user.subscription_status = 'past_due'
                user.save()
```

---

## 📱 MVP USER FLOWS

### **Flow 1: Sign Up & Create First Podcast**

```
1. User visits landing page
2. Clicks "Get Started"
3. Enters email/password
4. Receives verification email
5. Clicks verification link
6. Logs in
7. Dashboard shows "Create Your First Podcast"
8. Clicks "Create Podcast"
9. Enters: Title, Description, Author, Category
10. Uploads artwork
11. Clicks "Create"
12. Podcast created!
13. Dashboard shows "Record Your First Episode"
```

### **Flow 2: Record First Episode**

```
1. From podcast page, click "New Episode"
2. Enter episode title
3. Click "Record"
4. Browser requests microphone permission
5. Click "Allow"
6. Recording starts (shows timer, waveform)
7. Talk into microphone
8. Click "Stop"
9. Processing starts (shows progress: Uploading → Processing → Transcribing → Generating Show Notes)
10. Processing complete! (2-3 minutes)
11. Episode page shows:
    - Processed audio player
    - Full transcript
    - AI-generated show notes
12. Click "Publish"
13. Episode published to RSS feed!
```

### **Flow 3: Upload Existing Audio**

```
1. From podcast page, click "New Episode"
2. Enter episode title
3. Click "Upload Existing Audio"
4. Select MP3 file from computer
5. File uploads (shows progress bar)
6. Processing starts automatically
7. 2-3 minutes later, processing complete
8. Review transcript and show notes
9. Edit if needed
10. Click "Publish"
11. Episode published!
```

### **Flow 4: Upgrade to Pro**

```
1. User hits free tier limit (2 hours recorded)
2. Dashboard shows "Upgrade to record more"
3. Click "View Plans"
4. Pricing page shows 3 tiers
5. Click "Upgrade to Pro - $49/month"
6. Redirects to Stripe checkout
7. Enter payment details
8. Click "Subscribe"
9. Payment processes
10. Redirects to dashboard
11. Dashboard shows "Pro" badge
12. Limits updated (unlimited recording)
```

---

## ⏱️ 2-WEEK DEVELOPMENT TIMELINE

### **Week 1: Backend + Database**

**Day 1-2: Database & Models**
- Set up PostgreSQL
- Create all tables (users, podcasts, episodes, etc)
- Implement SQLAlchemy models
- Write database migrations

**Day 3-4: Authentication & User Management**
- Implement JWT auth
- Registration/login endpoints
- Email verification
- Password reset

**Day 5-7: Core API Endpoints**
- Podcast CRUD endpoints
- Episode CRUD endpoints
- File upload endpoint (S3 integration)
- Basic tests

### **Week 2: Frontend + Processing + Billing**

**Day 8-9: Frontend Dashboard**
- React app setup (Vite + Tailwind)
- Login/signup pages
- Dashboard layout
- Podcast list/create pages
- Episode list/create pages

**Day 10-11: Recording & Upload**
- WebRTC recording component
- File upload component
- Audio player component
- Processing status display

**Day 12-13: Audio Processing & AI**
- Celery task setup
- FFmpeg integration (noise, silence, loudness)
- Whisper API integration
- Claude AI show notes
- RSS feed generation

**Day 14: Stripe Billing**
- Stripe checkout integration
- Webhook handler
- Subscription limits enforcement
- Testing & launch prep

---

## 🧪 TESTING STRATEGY

### **Backend Tests:**
```
tests/
├── test_auth.py          - Authentication tests
├── test_podcasts.py      - Podcast CRUD tests
├── test_episodes.py      - Episode CRUD tests
├── test_audio.py         - Audio processing tests
├── test_billing.py       - Stripe integration tests
└── test_tasks.py         - Celery task tests
```

### **Frontend Tests:**
```
- Jest + React Testing Library
- Test authentication flows
- Test recording component
- Test file upload
- Test payment flow
```

---

## 🚀 DEPLOYMENT

### **Infrastructure:**

```
Production:
- Backend: DigitalOcean App Platform (Docker)
- Database: DigitalOcean Managed PostgreSQL
- Redis: DigitalOcean Managed Redis
- File Storage: AWS S3
- CDN: CloudFront (for audio delivery)
- Frontend: Vercel or Netlify

Staging:
- Same as production but separate resources
```

### **Environment Variables:**

```env
# Backend
FLASK_ENV=production
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
JWT_SECRET_KEY=...
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=...
FRONTEND_URL=https://app.podcastpro.com
```

---

## 💰 COST ESTIMATES (Monthly)

### **Infrastructure:**
```
DigitalOcean App Platform (backend): $12/mo
PostgreSQL (1GB): $15/mo
Redis (1GB): $15/mo
AWS S3 (100GB storage): $2.30/mo
CloudFront (1TB transfer): $85/mo
TOTAL INFRASTRUCTURE: ~$130/mo
```

### **APIs (per 1000 users):**
```
Whisper API: $0.006/min × 60 min avg × 1000 users = $360/mo
Claude API: $0.015/request × 100 requests × 1000 users = $1,500/mo
TOTAL API COSTS: ~$1,860/mo
```

### **Total Monthly Costs (1000 users):**
```
Infrastructure: $130
APIs: $1,860
TOTAL: $1,990/mo
```

### **Revenue (1000 users, 50% Pro tier):**
```
500 Pro users × $49/mo = $24,500/mo
Profit Margin: ($24,500 - $1,990) / $24,500 = 92%
```

---

## ✅ MVP COMPLETION CHECKLIST

### **Backend:**
- [ ] PostgreSQL database setup
- [ ] All models implemented
- [ ] JWT authentication working
- [ ] User registration/login
- [ ] Podcast CRUD endpoints
- [ ] Episode CRUD endpoints
- [ ] S3 file upload
- [ ] Celery tasks configured
- [ ] Audio processing pipeline (FFmpeg)
- [ ] Whisper API integration
- [ ] Claude AI show notes
- [ ] RSS feed generation
- [ ] Stripe checkout integration
- [ ] Stripe webhook handler
- [ ] Tests passing

### **Frontend:**
- [ ] React app initialized
- [ ] Login/signup pages
- [ ] Dashboard layout
- [ ] Podcast management
- [ ] Episode management
- [ ] WebRTC recording
- [ ] File upload
- [ ] Audio player
- [ ] Processing status display
- [ ] Billing/pricing page
- [ ] Responsive design
- [ ] Error handling

### **DevOps:**
- [ ] Backend deployed to DigitalOcean
- [ ] Database deployed
- [ ] Redis deployed
- [ ] S3 bucket configured
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set
- [ ] SSL certificates
- [ ] Domain configured

### **Launch:**
- [ ] Landing page live
- [ ] Documentation complete
- [ ] Pricing page published
- [ ] Stripe products created
- [ ] Email templates ready
- [ ] Support email configured
- [ ] 10 beta users tested
- [ ] Launch announcement ready

---

## 🎯 SUCCESS METRICS (Week 1)

- 50 signups
- 10 paid subscriptions
- 100 episodes created
- 500 minutes recorded
- <1% error rate on audio processing
- <5 minute avg processing time
- 95% uptime

---

**Technical Spec Prepared by:** C1 - The Mechanic
**Date:** November 8, 2025
**Status:** ✅ READY FOR DEVELOPMENT

**Next Step:** Start Week 1 development on Monday, November 11, 2025

🎙️⚡🚀
```
