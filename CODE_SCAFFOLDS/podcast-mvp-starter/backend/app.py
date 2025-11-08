"""
Podcast MVP - Minimal Flask Backend Starter
============================================

This is a minimal working Flask app to get you started.

To run:
1. pip install flask flask-cors flask-jwt-extended sqlalchemy psycopg2-binary
2. Create PostgreSQL database: createdb podcast_mvp
3. Update DATABASE_URL in this file
4. python app.py
5. Test: curl http://localhost:5000/api/health

Next steps: Add models, authentication, endpoints from MVP_TECHNICAL_SPEC.md
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
import os
from datetime import datetime

# ==================== CONFIG ====================

app = Flask(__name__)
CORS(app)

# CHANGE THESE:
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
DATABASE_URL = 'postgresql://localhost:5432/podcast_mvp'  # Update with your credentials

jwt = JWTManager(app)

# ==================== DATABASE ====================

engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    subscription_tier = Column(String(50), default='free')
    created_at = Column(DateTime, default=datetime.utcnow)

class Podcast(Base):
    __tablename__ = 'podcasts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(2000))
    created_at = Column(DateTime, default=datetime.utcnow)

class Episode(Base):
    __tablename__ = 'episodes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    podcast_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String(255), nullable=False)
    audio_file_path = Column(String(500))
    transcript = Column(String)
    processing_status = Column(String(50), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)

# ==================== ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Podcast MVP API is running'})

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User signup"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name', '')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    session = Session()

    # Check if user exists
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        session.close()
        return jsonify({'error': 'User already exists'}), 400

    # Create user
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        full_name=full_name
    )
    session.add(user)
    session.commit()

    # Generate token
    access_token = create_access_token(identity=str(user.id))

    session.close()

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': str(user.id),
            'email': user.email,
            'full_name': user.full_name
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    session = Session()

    user = session.query(User).filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        session.close()
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))

    session.close()

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': str(user.id),
            'email': user.email,
            'full_name': user.full_name
        }
    }), 200

@app.route('/api/podcasts', methods=['GET'])
@jwt_required()
def get_podcasts():
    """Get user's podcasts"""
    user_id = get_jwt_identity()

    session = Session()
    podcasts = session.query(Podcast).filter_by(user_id=uuid.UUID(user_id)).all()

    result = [{
        'id': str(p.id),
        'title': p.title,
        'description': p.description,
        'created_at': p.created_at.isoformat()
    } for p in podcasts]

    session.close()

    return jsonify(result)

@app.route('/api/podcasts', methods=['POST'])
@jwt_required()
def create_podcast():
    """Create new podcast"""
    user_id = get_jwt_identity()
    data = request.json

    title = data.get('title')
    description = data.get('description', '')

    if not title:
        return jsonify({'error': 'Title required'}), 400

    session = Session()

    podcast = Podcast(
        user_id=uuid.UUID(user_id),
        title=title,
        description=description
    )
    session.add(podcast)
    session.commit()

    result = {
        'id': str(podcast.id),
        'title': podcast.title,
        'description': podcast.description,
        'created_at': podcast.created_at.isoformat()
    }

    session.close()

    return jsonify(result), 201

@app.route('/api/episodes', methods=['POST'])
@jwt_required()
def create_episode():
    """Create new episode"""
    user_id = get_jwt_identity()
    data = request.json

    podcast_id = data.get('podcast_id')
    title = data.get('title')

    if not podcast_id or not title:
        return jsonify({'error': 'podcast_id and title required'}), 400

    session = Session()

    # Verify podcast belongs to user
    podcast = session.query(Podcast).filter_by(
        id=uuid.UUID(podcast_id),
        user_id=uuid.UUID(user_id)
    ).first()

    if not podcast:
        session.close()
        return jsonify({'error': 'Podcast not found'}), 404

    episode = Episode(
        podcast_id=uuid.UUID(podcast_id),
        title=title
    )
    session.add(episode)
    session.commit()

    result = {
        'id': str(episode.id),
        'podcast_id': str(episode.podcast_id),
        'title': episode.title,
        'processing_status': episode.processing_status,
        'created_at': episode.created_at.isoformat()
    }

    session.close()

    return jsonify(result), 201

# ==================== RUN ====================

if __name__ == '__main__':
    print("🎙️ Podcast MVP API Starting...")
    print("📍 Running on http://localhost:5000")
    print("✅ Health check: http://localhost:5000/api/health")
    print("")
    print("📝 Next steps:")
    print("1. Test signup: POST /api/auth/signup")
    print("2. Test login: POST /api/auth/login")
    print("3. Add WebRTC recording (see MVP_TECHNICAL_SPEC.md)")
    print("4. Add S3 upload (see MVP_TECHNICAL_SPEC.md)")
    print("5. Add FFmpeg processing (see MVP_TECHNICAL_SPEC.md)")
    print("")
    app.run(debug=True, port=5000)
