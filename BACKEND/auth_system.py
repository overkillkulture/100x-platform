"""
CONSCIOUSNESS REVOLUTION - AUTHENTICATION SYSTEM
Cross-domain single sign-on for all 7 domains
"""

import os
import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuration
SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/consciousness_revolution')
TOKEN_EXPIRY_HOURS = 24 * 7  # 7 days

class AuthSystem:
    """
    Handles all authentication across 7 domains
    One account works everywhere
    """

    def __init__(self):
        self.db_conn = psycopg2.connect(DATABASE_URL)

    def _get_cursor(self):
        return self.db_conn.cursor(cursor_factory=RealDictCursor)

    def signup(self, email: str, password: str, full_name: str = None,
               signup_source: str = 'organic', utm_data: Dict = None) -> Dict:
        """
        Create new user account

        Returns:
            {
                'success': bool,
                'user_id': int,
                'token': str,
                'message': str
            }
        """

        # Validate email
        if not email or '@' not in email:
            return {'success': False, 'message': 'Invalid email address'}

        # Validate password strength
        if not password or len(password) < 8:
            return {'success': False, 'message': 'Password must be at least 8 characters'}

        # Check if email already exists
        cursor = self._get_cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email.lower(),))
        existing_user = cursor.fetchone()

        if existing_user:
            return {'success': False, 'message': 'Email already registered'}

        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create user
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, signup_source, utm_source, utm_campaign)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            email.lower(),
            password_hash,
            full_name,
            signup_source,
            utm_data.get('source') if utm_data else None,
            utm_data.get('campaign') if utm_data else None
        ))

        user_id = cursor.fetchone()['id']
        self.db_conn.commit()

        # Grant free tier access to all domains
        self._grant_free_tier_access(user_id)

        # Generate JWT token
        token = self._generate_token(user_id, email)

        # Track conversion event
        self._track_event(user_id, 'signup', None, 'free', 'all_domains')

        return {
            'success': True,
            'user_id': user_id,
            'token': token,
            'message': 'Account created successfully'
        }

    def login(self, email: str, password: str) -> Dict:
        """
        Authenticate user and return JWT token

        Returns:
            {
                'success': bool,
                'user_id': int,
                'token': str,
                'message': str
            }
        """

        cursor = self._get_cursor()
        cursor.execute("""
            SELECT id, email, password_hash, account_status
            FROM users
            WHERE email = %s
        """, (email.lower(),))

        user = cursor.fetchone()

        if not user:
            return {'success': False, 'message': 'Invalid email or password'}

        # Check account status
        if user['account_status'] != 'active':
            return {'success': False, 'message': f'Account is {user["account_status"]}'}

        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return {'success': False, 'message': 'Invalid email or password'}

        # Update last login
        cursor.execute("UPDATE users SET last_login = NOW() WHERE id = %s", (user['id'],))
        self.db_conn.commit()

        # Generate token
        token = self._generate_token(user['id'], user['email'])

        return {
            'success': True,
            'user_id': user['id'],
            'email': user['email'],
            'token': token,
            'message': 'Login successful'
        }

    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify JWT token and return user data

        Returns:
            {
                'user_id': int,
                'email': str
            } or None if invalid
        """

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return {
                'user_id': payload['user_id'],
                'email': payload['email']
            }
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def check_access(self, user_id: int, domain: str, tier: str = None) -> Dict:
        """
        Check if user has access to domain/tier

        Returns:
            {
                'has_access': bool,
                'tier': str,
                'usage_current_month': dict,
                'limits': dict
            }
        """

        cursor = self._get_cursor()
        cursor.execute("""
            SELECT tier, feature_flags, usage_current_month, active
            FROM domain_access
            WHERE user_id = %s AND domain = %s AND active = TRUE
        """, (user_id, domain))

        access = cursor.fetchone()

        if not access:
            return {'has_access': False, 'tier': None}

        if tier and access['tier'] != tier:
            return {'has_access': False, 'tier': access['tier']}

        return {
            'has_access': True,
            'tier': access['tier'],
            'usage_current_month': access['usage_current_month'] or {},
            'limits': access['feature_flags'] or {}
        }

    def record_usage(self, user_id: int, domain: str, action: str, count: int = 1):
        """
        Track usage for freemium limits

        Example: record_usage(123, 'intelligence', 'ai_actions', 1)
        """

        cursor = self._get_cursor()

        # Get current usage
        cursor.execute("""
            SELECT usage_current_month, usage_reset_date
            FROM domain_access
            WHERE user_id = %s AND domain = %s
        """, (user_id, domain))

        result = cursor.fetchone()
        if not result:
            return

        usage = result['usage_current_month'] or {}
        reset_date = result['usage_reset_date']

        # Reset if month has passed
        if not reset_date or datetime.now() > reset_date:
            usage = {}
            reset_date = datetime.now() + timedelta(days=30)

        # Update usage count
        usage[action] = usage.get(action, 0) + count

        # Save
        cursor.execute("""
            UPDATE domain_access
            SET usage_current_month = %s, usage_reset_date = %s
            WHERE user_id = %s AND domain = %s
        """, (psycopg2.extras.Json(usage), reset_date, user_id, domain))

        self.db_conn.commit()

    def _generate_token(self, user_id: int, email: str) -> str:
        """Generate JWT token"""
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    def _grant_free_tier_access(self, user_id: int):
        """Grant free tier access to all 7 domains"""

        domains_config = [
            {
                'domain': 'music',
                'tier': 'free',
                'features': {
                    'streams_tracking': True,
                    'basic_analytics': True,
                    'monthly_limit': 100
                }
            },
            {
                'domain': 'intelligence',
                'tier': 'free',
                'features': {
                    'ai_actions_per_month': 25,
                    'basic_models': True
                }
            },
            {
                'domain': 'tools',
                'tier': 'free',
                'features': {
                    'modules_limit': 5,
                    'basic_features': True
                }
            },
            {
                'domain': 'education',
                'tier': 'free',
                'features': {
                    'courses_limit': 1,
                    'basic_content': True
                }
            },
            {
                'domain': 'commerce',
                'tier': 'free',
                'features': {
                    'store_access': True
                }
            },
            {
                'domain': 'communication',
                'tier': 'free',
                'features': {
                    'oib_access': True
                }
            },
            {
                'domain': 'community',
                'tier': 'free',
                'features': {
                    'forum_access': True
                }
            }
        ]

        cursor = self._get_cursor()
        for config in domains_config:
            cursor.execute("""
                INSERT INTO domain_access (user_id, domain, tier, feature_flags, usage_reset_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                user_id,
                config['domain'],
                config['tier'],
                psycopg2.extras.Json(config['features']),
                datetime.now() + timedelta(days=30)
            ))

        self.db_conn.commit()

    def _track_event(self, user_id: int, event_type: str, from_tier: str, to_tier: str, domain: str):
        """Track conversion events"""

        cursor = self._get_cursor()
        cursor.execute("""
            INSERT INTO conversion_events (user_id, event_type, from_tier, to_tier, domain)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, event_type, from_tier, to_tier, domain))
        self.db_conn.commit()


# =====================================================
# API ENDPOINTS (Flask/FastAPI integration)
# =====================================================

from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)
auth = AuthSystem()

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_data = auth.verify_token(token)

        if not user_data:
            return jsonify({'error': 'Unauthorized'}), 401

        request.user_id = user_data['user_id']
        request.user_email = user_data['email']
        return f(*args, **kwargs)

    return decorated

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    """
    POST /api/auth/signup
    Body: {"email": "...", "password": "...", "full_name": "..."}
    """
    data = request.json
    result = auth.signup(
        email=data.get('email'),
        password=data.get('password'),
        full_name=data.get('full_name'),
        signup_source=data.get('source', 'website'),
        utm_data={
            'source': request.args.get('utm_source'),
            'campaign': request.args.get('utm_campaign')
        }
    )

    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """
    POST /api/auth/login
    Body: {"email": "...", "password": "..."}
    """
    data = request.json
    result = auth.login(
        email=data.get('email'),
        password=data.get('password')
    )

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@app.route('/api/auth/verify', methods=['GET'])
@require_auth
def api_verify():
    """
    GET /api/auth/verify
    Headers: Authorization: Bearer <token>
    """
    return jsonify({
        'success': True,
        'user_id': request.user_id,
        'email': request.user_email
    })

@app.route('/api/access/<domain>', methods=['GET'])
@require_auth
def api_check_access(domain):
    """
    GET /api/access/music
    Headers: Authorization: Bearer <token>
    """
    access_info = auth.check_access(request.user_id, domain)
    return jsonify(access_info)

@app.route('/api/usage/<domain>/<action>', methods=['POST'])
@require_auth
def api_record_usage(domain, action):
    """
    POST /api/usage/intelligence/ai_actions
    Headers: Authorization: Bearer <token>
    Body: {"count": 1}
    """
    data = request.json
    count = data.get('count', 1)

    auth.record_usage(request.user_id, domain, action, count)

    return jsonify({'success': True, 'message': f'Recorded {count} {action} for {domain}'})


if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=5000, debug=True)


# =====================================================
# AUTHENTICATION SYSTEM COMPLETE
# Ready for deployment
# Supports cross-domain SSO for all 7 domains
# =====================================================
