"""
Social Media MVP - Minimal Flask Backend Starter with OAuth
============================================================

This is a minimal working Flask app with Twitter OAuth to get you started.

To run:
1. pip install flask flask-cors flask-jwt-extended sqlalchemy psycopg2-binary tweepy redis
2. Create PostgreSQL database: createdb social_mvp
3. Register Twitter app: https://developer.twitter.com/en/portal/dashboard
4. Update config in this file (DATABASE_URL, TWITTER_CLIENT_ID, etc.)
5. python app.py
6. Test: curl http://localhost:5000/api/health

Next steps: Add LinkedIn/Instagram/Facebook OAuth from MVP_TECHNICAL_SPEC.md
"""

from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
import os
import json
from datetime import datetime, timedelta
import tweepy
import redis

# ==================== CONFIG ====================

app = Flask(__name__)
CORS(app)

# CHANGE THESE:
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
DATABASE_URL = 'postgresql://localhost:5432/social_mvp'  # Update with your credentials

# Twitter OAuth (get from https://developer.twitter.com/)
TWITTER_CLIENT_ID = 'your_twitter_client_id'
TWITTER_CLIENT_SECRET = 'your_twitter_client_secret'
TWITTER_REDIRECT_URI = 'http://localhost:5000/api/oauth/twitter/callback'

jwt = JWTManager(app)

# Redis for temporary OAuth state storage
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# ==================== DATABASE ====================

engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    subscription_tier = Column(String(50), default='free')
    created_at = Column(DateTime, default=datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text, nullable=False)
    scheduled_time = Column(DateTime)
    status = Column(String(50), default='draft')  # draft, scheduled, published
    publish_to_platforms = Column(Text)  # JSON array
    created_at = Column(DateTime, default=datetime.utcnow)

class PlatformPost(Base):
    __tablename__ = 'platform_posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), nullable=False)
    platform = Column(String(50), nullable=False)
    platform_post_id = Column(String(255))  # Tweet ID, etc.
    content = Column(Text)
    publish_status = Column(String(50), default='pending')
    error_message = Column(Text)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)

# ==================== AUTH ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Social Media MVP API is running'})

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User signup"""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    session = Session()

    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        session.close()
        return jsonify({'error': 'User already exists'}), 400

    user = User(
        email=email,
        password_hash=generate_password_hash(password)
    )
    session.add(user)
    session.commit()

    access_token = create_access_token(identity=str(user.id))

    session.close()

    return jsonify({
        'access_token': access_token,
        'user': {'id': str(user.id), 'email': user.email}
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    session = Session()

    user = session.query(User).filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        session.close()
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))

    session.close()

    return jsonify({
        'access_token': access_token,
        'user': {'id': str(user.id), 'email': user.email}
    }), 200

# ==================== TWITTER OAUTH ====================

@app.route('/api/oauth/twitter/authorize', methods=['POST'])
@jwt_required()
def twitter_authorize():
    """Step 1: Get Twitter authorization URL"""
    user_id = get_jwt_identity()

    # Create OAuth handler
    auth = tweepy.OAuth2UserHandler(
        client_id=TWITTER_CLIENT_ID,
        redirect_uri=TWITTER_REDIRECT_URI,
        scope=["tweet.read", "tweet.write", "users.read"],
        client_secret=TWITTER_CLIENT_SECRET
    )

    # Get authorization URL
    auth_url = auth.get_authorization_url()

    # Store state temporarily (expires in 10 minutes)
    state = auth.state
    redis_client.setex(f"twitter_oauth_state:{state}", 600, user_id)

    return jsonify({'auth_url': auth_url})

@app.route('/api/oauth/twitter/callback')
def twitter_callback():
    """Step 2: Handle Twitter OAuth callback"""
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')

    if error:
        return redirect(f'http://localhost:3000/settings/connections?error=twitter_{error}')

    # Verify state
    user_id = redis_client.get(f"twitter_oauth_state:{state}")
    if not user_id:
        return redirect('http://localhost:3000/settings/connections?error=twitter_invalid_state')

    # Delete state from Redis
    redis_client.delete(f"twitter_oauth_state:{state}")

    # Exchange code for access token
    auth = tweepy.OAuth2UserHandler(
        client_id=TWITTER_CLIENT_ID,
        redirect_uri=TWITTER_REDIRECT_URI,
        client_secret=TWITTER_CLIENT_SECRET
    )

    try:
        auth.fetch_token(code)

        # Get user info
        client = tweepy.Client(auth.access_token)
        twitter_user = client.get_me()

        # Save to database
        session = Session()

        # Check if account already exists
        existing_account = session.query(SocialAccount).filter_by(
            user_id=uuid.UUID(user_id),
            platform='twitter',
            platform_user_id=str(twitter_user.data.id)
        ).first()

        if existing_account:
            # Update tokens
            existing_account.access_token = auth.access_token
            existing_account.refresh_token = auth.refresh_token if hasattr(auth, 'refresh_token') else None
            existing_account.token_expires_at = datetime.now() + timedelta(seconds=auth.expires_in) if hasattr(auth, 'expires_in') else None
            existing_account.is_active = True
        else:
            # Create new account
            social_account = SocialAccount(
                user_id=uuid.UUID(user_id),
                platform='twitter',
                platform_user_id=str(twitter_user.data.id),
                platform_username=twitter_user.data.username,
                access_token=auth.access_token,
                refresh_token=auth.refresh_token if hasattr(auth, 'refresh_token') else None,
                token_expires_at=datetime.now() + timedelta(seconds=auth.expires_in) if hasattr(auth, 'expires_in') else None
            )
            session.add(social_account)

        session.commit()
        session.close()

        return redirect('http://localhost:3000/settings/connections?success=twitter')

    except Exception as e:
        print(f"Twitter OAuth error: {e}")
        return redirect(f'http://localhost:3000/settings/connections?error=twitter_exchange_failed')

# ==================== SOCIAL ACCOUNTS ====================

@app.route('/api/social-accounts', methods=['GET'])
@jwt_required()
def get_social_accounts():
    """Get user's connected social accounts"""
    user_id = get_jwt_identity()

    session = Session()
    accounts = session.query(SocialAccount).filter_by(
        user_id=uuid.UUID(user_id),
        is_active=True
    ).all()

    result = [{
        'id': str(a.id),
        'platform': a.platform,
        'username': a.platform_username,
        'connected_at': a.created_at.isoformat()
    } for a in accounts]

    session.close()

    return jsonify(result)

@app.route('/api/social-accounts/<account_id>', methods=['DELETE'])
@jwt_required()
def disconnect_account(account_id):
    """Disconnect social account"""
    user_id = get_jwt_identity()

    session = Session()

    account = session.query(SocialAccount).filter_by(
        id=uuid.UUID(account_id),
        user_id=uuid.UUID(user_id)
    ).first()

    if not account:
        session.close()
        return jsonify({'error': 'Account not found'}), 404

    account.is_active = False
    session.commit()
    session.close()

    return jsonify({'message': 'Account disconnected'}), 200

# ==================== POSTS ====================

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    """Create new post"""
    user_id = get_jwt_identity()
    data = request.json

    content = data.get('content')
    platforms = data.get('platforms', [])
    scheduled_time = data.get('scheduled_time')

    if not content:
        return jsonify({'error': 'Content required'}), 400

    if not platforms:
        return jsonify({'error': 'At least one platform required'}), 400

    session = Session()

    # Create post
    post = Post(
        user_id=uuid.UUID(user_id),
        content=content,
        scheduled_time=datetime.fromisoformat(scheduled_time) if scheduled_time else None,
        status='scheduled' if scheduled_time else 'published',
        publish_to_platforms=json.dumps(platforms)
    )
    session.add(post)
    session.commit()

    result = {
        'id': str(post.id),
        'content': post.content,
        'status': post.status,
        'platforms': platforms
    }

    session.close()

    # TODO: If immediate publish, queue Celery task here
    # publish_post.delay(str(post.id))

    return jsonify(result), 201

@app.route('/api/posts', methods=['GET'])
@jwt_required()
def get_posts():
    """Get user's posts"""
    user_id = get_jwt_identity()

    session = Session()
    posts = session.query(Post).filter_by(user_id=uuid.UUID(user_id)).order_by(Post.created_at.desc()).all()

    result = [{
        'id': str(p.id),
        'content': p.content,
        'status': p.status,
        'scheduled_time': p.scheduled_time.isoformat() if p.scheduled_time else None,
        'platforms': json.loads(p.publish_to_platforms),
        'created_at': p.created_at.isoformat()
    } for p in posts]

    session.close()

    return jsonify(result)

# ==================== RUN ====================

if __name__ == '__main__':
    print("📱 Social Media MVP API Starting...")
    print("📍 Running on http://localhost:5000")
    print("✅ Health check: http://localhost:5000/api/health")
    print("")
    print("🔑 Twitter OAuth:")
    print(f"   Redirect URI: {TWITTER_REDIRECT_URI}")
    print("   Make sure this matches your Twitter app settings!")
    print("")
    print("📝 Next steps:")
    print("1. Test signup: POST /api/auth/signup")
    print("2. Test Twitter OAuth: POST /api/oauth/twitter/authorize (with JWT)")
    print("3. Add LinkedIn OAuth (see MVP_TECHNICAL_SPEC.md)")
    print("4. Add Instagram/Facebook OAuth (see MVP_TECHNICAL_SPEC.md)")
    print("5. Add Celery for publishing (see MVP_TECHNICAL_SPEC.md)")
    print("6. Add Claude content optimization (see MVP_TECHNICAL_SPEC.md)")
    print("")
    app.run(debug=True, port=5000)
