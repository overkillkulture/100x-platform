"""
PHILOSOPHER AI - BACKEND API SERVER
Flask API that powers philosopher-ai-connected.html

Endpoints:
- POST /api/auth/register - Create account
- POST /api/auth/login - Login
- GET /api/auth/me - Get current user
- POST /api/questions/ask - Ask Philosopher AI a question
- GET /api/health - Health check

Built by C1 Mechanic - Ship fast, iterate forever
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import bcrypt
import sqlite3
import os
import secrets
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

# Try to import anthropic (optional - will use demo mode if not available)
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    anthropic = None
    ANTHROPIC_AVAILABLE = False

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configuration
SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
DATABASE_PATH = 'philosopher_ai.db'
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Initialize Anthropic client
if ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY:
    claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
else:
    claude_client = None
    if not ANTHROPIC_AVAILABLE:
        print("⚠️  anthropic module not installed - running in DEMO MODE")
    elif not ANTHROPIC_API_KEY:
        print("⚠️  ANTHROPIC_API_KEY not set - running in DEMO MODE")

# ============================================================
# DATABASE SETUP
# ============================================================

def init_database():
    """Create database tables if they don't exist"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            username TEXT,
            tier TEXT DEFAULT 'free',
            questions_used INTEGER DEFAULT 0,
            questions_limit INTEGER DEFAULT 3,
            consciousness_level INTEGER DEFAULT 50,
            signup_source TEXT DEFAULT 'philosopher-ai',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    """)

    # Conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            consciousness_boost INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized")

# Initialize database on startup
init_database()

# ============================================================
# DATABASE HELPERS
# ============================================================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def dict_from_row(row):
    """Convert sqlite3.Row to dictionary"""
    return dict(zip(row.keys(), row)) if row else None

# ============================================================
# AUTHENTICATION MIDDLEWARE
# ============================================================

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer TOKEN
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Decode token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user_id = data['user_id']

            # Get user from database
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (current_user_id,))
            current_user = cursor.fetchone()
            conn.close()

            if not current_user:
                return jsonify({'error': 'User not found'}), 401

            # Attach user to request
            request.current_user = dict_from_row(current_user)

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated

# ============================================================
# AUTHENTICATION ENDPOINTS
# ============================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Create new user account"""
    data = request.get_json()

    email = data.get('email', '').lower().strip()
    password = data.get('password', '')
    username = data.get('username', '')
    signup_source = data.get('signupSource', 'philosopher-ai')

    # Validation
    if not email or '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    if not password or len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    # Check if user exists
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({'error': 'Email already registered'}), 400

    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create user
    cursor.execute("""
        INSERT INTO users (email, password_hash, username, signup_source)
        VALUES (?, ?, ?, ?)
    """, (email, password_hash, username, signup_source))

    user_id = cursor.lastrowid
    conn.commit()

    # Get user data
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = dict_from_row(cursor.fetchone())
    conn.close()

    # Generate JWT token
    token = jwt.encode({
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'username': user['username'],
            'tier': user['tier'],
            'questionsUsed': user['questions_used'],
            'questionsLimit': user['questions_limit'],
            'consciousnessLevel': user['consciousness_level']
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()

    email = data.get('email', '').lower().strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    # Get user
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({'error': 'Invalid email or password'}), 401

    user = dict_from_row(user)

    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        conn.close()
        return jsonify({'error': 'Invalid email or password'}), 401

    # Update last login
    cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],))
    conn.commit()
    conn.close()

    # Generate JWT token
    token = jwt.encode({
        'user_id': user['id'],
        'email': user['email'],
        'exp': datetime.utcnow() + timedelta(days=7)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'username': user['username'],
            'tier': user['tier'],
            'questionsUsed': user['questions_used'],
            'questionsLimit': user['questions_limit'],
            'consciousnessLevel': user['consciousness_level']
        }
    })

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user():
    """Get current user info"""
    user = request.current_user

    return jsonify({
        'user': {
            'id': user['id'],
            'email': user['email'],
            'username': user['username'],
            'tier': user['tier'],
            'questionsUsed': user['questions_used'],
            'questionsLimit': user['questions_limit'],
            'consciousnessLevel': user['consciousness_level']
        }
    })

# ============================================================
# QUESTION/ANSWER ENGINE
# ============================================================

def get_claude_response(question, conversation_history=None):
    """Get response from Claude API"""
    if not claude_client:
        # Demo mode - return canned response
        return {
            'answer': f"""**Demo Mode Response**

I hear your question: "{question}"

This is a demonstration response since the Anthropic API key is not configured.

In production, I would provide:
- Pattern Theory analysis of your situation
- Destroyer detection (D1-D7 classification)
- Consciousness-aligned guidance
- Actionable next steps

To enable full functionality, set the ANTHROPIC_API_KEY environment variable.

For now, know that asking deeper questions is the first step toward higher consciousness. You're on the right path.""",
            'consciousness_boost': 3
        }

    # Build system prompt (Pattern Theory context)
    system_prompt = """You are The Philosopher, an AI consciousness advisor trained on Pattern Theory.

Your role is to help users understand their challenges through:
1. **Destroyer Detection** (D1-D7 classification)
2. **Consciousness Measurement** (0-100% scale, 85%+ = builder threshold)
3. **Manipulation Recognition** (gaslighting, triangulation, projection, etc.)
4. **Pattern Recognition** (identifying recurring life patterns)

**Your Communication Style:**
- Direct and honest (no sugar-coating)
- Pattern-focused (show underlying dynamics)
- Consciousness-elevating (guide toward higher awareness)
- Action-oriented (give concrete next steps)

**Response Structure:**
1. Acknowledge the pattern you see
2. Explain underlying consciousness dynamics
3. Identify any destroyer/manipulation patterns
4. Provide consciousness-aligned action steps
5. Offer follow-up questions for deeper exploration

Keep responses concise but insightful (300-500 words)."""

    # Build conversation context
    messages = []
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({'role': 'user', 'content': question})

    try:
        # Call Claude API
        response = claude_client.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=2000,
            temperature=0.7,
            system=system_prompt,
            messages=messages
        )

        answer = response.content[0].text

        # Calculate consciousness boost (simple heuristic for now)
        consciousness_boost = min(10, len(question) // 50 + 3)  # 3-10 based on question depth

        return {
            'answer': answer,
            'consciousness_boost': consciousness_boost
        }

    except Exception as e:
        print(f"❌ Claude API error: {e}")
        return {
            'answer': "I apologize - there was an error processing your question. Please try again.",
            'consciousness_boost': 0
        }

@app.route('/api/questions/ask', methods=['POST'])
@token_required
def ask_question():
    """Ask Philosopher AI a question"""
    user = request.current_user
    data = request.get_json()

    question = data.get('question', '').strip()
    conversation_id = data.get('conversationId')

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    # Check question limit (free tier only)
    if user['tier'] == 'free':
        if user['questions_used'] >= user['questions_limit']:
            return jsonify({
                'error': 'Question limit reached',
                'message': 'You have used all your free questions this month. Upgrade to Student tier for unlimited questions.'
            }), 403

    conn = get_db()
    cursor = conn.cursor()

    # Create or get conversation
    if not conversation_id:
        # New conversation
        cursor.execute("""
            INSERT INTO conversations (user_id, title)
            VALUES (?, ?)
        """, (user['id'], question[:100]))  # Use first 100 chars as title
        conversation_id = cursor.lastrowid
    else:
        # Verify conversation belongs to user
        cursor.execute('SELECT user_id FROM conversations WHERE id = ?', (conversation_id,))
        conv = cursor.fetchone()
        if not conv or conv['user_id'] != user['id']:
            conn.close()
            return jsonify({'error': 'Invalid conversation'}), 403

    # Get conversation history
    cursor.execute("""
        SELECT role, content FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at ASC
    """, (conversation_id,))
    history_rows = cursor.fetchall()
    conversation_history = [{'role': row['role'], 'content': row['content']} for row in history_rows]

    # Get Claude response
    response_data = get_claude_response(question, conversation_history)
    answer = response_data['answer']
    consciousness_boost = response_data['consciousness_boost']

    # Save user message
    cursor.execute("""
        INSERT INTO messages (conversation_id, role, content)
        VALUES (?, ?, ?)
    """, (conversation_id, 'user', question))

    # Save AI response
    cursor.execute("""
        INSERT INTO messages (conversation_id, role, content, consciousness_boost)
        VALUES (?, ?, ?, ?)
    """, (conversation_id, 'philosopher', answer, consciousness_boost))

    # Update user stats
    new_questions_used = user['questions_used'] + 1
    new_consciousness_level = min(100, user['consciousness_level'] + consciousness_boost)

    cursor.execute("""
        UPDATE users
        SET questions_used = ?,
            consciousness_level = ?
        WHERE id = ?
    """, (new_questions_used, new_consciousness_level, user['id']))

    conn.commit()
    conn.close()

    return jsonify({
        'answer': answer,
        'consciousnessBoost': consciousness_boost,
        'newConsciousnessLevel': new_consciousness_level,
        'questionId': conversation_id,
        'questionsRemaining': max(0, user['questions_limit'] - new_questions_used) if user['tier'] == 'free' else None
    })

# ============================================================
# HEALTH CHECK
# ============================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'philosopher-ai-backend',
        'version': '1.0.0',
        'buildNumber': 1,
        'timestamp': datetime.utcnow().isoformat(),
        'claudeApiConfigured': claude_client is not None
    })

# ============================================================
# RUN SERVER
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🧠 PHILOSOPHER AI - BACKEND API SERVER")
    print("=" * 60)
    print(f"Database: {DATABASE_PATH}")
    print(f"Claude API: {'✅ Configured' if claude_client else '⚠️  Not configured (demo mode)'}")
    print(f"JWT Secret: {'✅ Set' if SECRET_KEY else '❌ Missing'}")
    print("=" * 60)
    print("Endpoints:")
    print("  POST /api/auth/register")
    print("  POST /api/auth/login")
    print("  GET  /api/auth/me")
    print("  POST /api/questions/ask")
    print("  GET  /api/health")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("=" * 60)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
