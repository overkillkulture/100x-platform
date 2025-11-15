"""
100X PLATFORM - UNIFIED AUTHENTICATION SERVER
Single entry point using existing auth_system.py
"""

import os
import sys
from flask import Flask, request, jsonify, send_file, redirect
from flask_cors import CORS
from functools import wraps

# Import existing auth system
sys.path.append(os.path.dirname(__file__))
from BACKEND.auth_system import AuthSystem, require_auth

app = Flask(__name__)
CORS(app)

# Initialize auth system
try:
    auth = AuthSystem()
    print("✅ Auth system initialized successfully")
except Exception as e:
    print(f"⚠️  Warning: Auth system initialization failed: {e}")
    print("   Make sure DATABASE_URL is set correctly")
    auth = None


# =====================================================
# STATIC FILE SERVING
# =====================================================

@app.route('/')
def home():
    """Serve the start.html entry point"""
    return send_file('start.html')


@app.route('/workspace')
def workspace():
    """Serve the workspace (protected route)"""
    # In production, this should verify the JWT token
    # For now, we'll serve the file and let client-side handle auth
    return send_file('workspace.html')


# =====================================================
# AUTHENTICATION ENDPOINTS
# =====================================================

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    """
    POST /api/auth/signup
    Body: {"email": "...", "password": "...", "full_name": "..."}
    """
    if not auth:
        return jsonify({
            'success': False,
            'message': 'Auth system not available. Check database connection.'
        }), 500

    try:
        data = request.json
        result = auth.signup(
            email=data.get('email'),
            password=data.get('password'),
            full_name=data.get('full_name'),
            signup_source=data.get('source', 'platform'),
            utm_data={
                'source': request.args.get('utm_source'),
                'campaign': request.args.get('utm_campaign')
            }
        )

        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """
    POST /api/auth/login
    Body: {"email": "...", "password": "..."}
    """
    if not auth:
        return jsonify({
            'success': False,
            'message': 'Auth system not available. Check database connection.'
        }), 500

    try:
        data = request.json
        result = auth.login(
            email=data.get('email'),
            password=data.get('password')
        )

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/auth/verify', methods=['GET'])
def api_verify():
    """
    GET /api/auth/verify
    Headers: Authorization: Bearer <token>
    """
    if not auth:
        return jsonify({'success': False, 'message': 'Auth system not available'}), 500

    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_data = auth.verify_token(token)

        if user_data:
            return jsonify({
                'success': True,
                'user_id': user_data['user_id'],
                'email': user_data['email']
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/access/<domain>', methods=['GET'])
def api_check_access(domain):
    """
    GET /api/access/music
    Headers: Authorization: Bearer <token>
    """
    if not auth:
        return jsonify({'success': False, 'message': 'Auth system not available'}), 500

    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_data = auth.verify_token(token)

        if not user_data:
            return jsonify({'error': 'Unauthorized'}), 401

        access_info = auth.check_access(user_data['user_id'], domain)
        return jsonify(access_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/usage/<domain>/<action>', methods=['POST'])
def api_record_usage(domain, action):
    """
    POST /api/usage/intelligence/ai_actions
    Headers: Authorization: Bearer <token>
    Body: {"count": 1}
    """
    if not auth:
        return jsonify({'success': False, 'message': 'Auth system not available'}), 500

    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_data = auth.verify_token(token)

        if not user_data:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.json
        count = data.get('count', 1)

        auth.record_usage(user_data['user_id'], domain, action, count)

        return jsonify({
            'success': True,
            'message': f'Recorded {count} {action} for {domain}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =====================================================
# HEALTH CHECK
# =====================================================

@app.route('/health')
def health():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'auth_system': 'connected' if auth else 'disconnected',
        'database': 'connected' if auth else 'disconnected'
    }

    if auth:
        return jsonify(status), 200
    else:
        status['status'] = 'degraded'
        return jsonify(status), 503


# =====================================================
# ERROR HANDLERS
# =====================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# =====================================================
# STARTUP
# =====================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 100X PLATFORM - UNIFIED AUTH SERVER")
    print("=" * 60)
    print()
    print("📍 Entry Point:  http://localhost:5000")
    print("🔐 Auth API:     http://localhost:5000/api/auth/*")
    print("🏠 Workspace:    http://localhost:5000/workspace")
    print()

    if auth:
        print("✅ Authentication System: READY")
        print("✅ Database Connection:   CONNECTED")
    else:
        print("⚠️  Authentication System: NOT AVAILABLE")
        print("⚠️  Database Connection:   FAILED")
        print()
        print("To fix:")
        print("  1. Set DATABASE_URL environment variable")
        print("  2. Ensure PostgreSQL is running")
        print("  3. Run database migrations if needed")

    print()
    print("=" * 60)
    print()

    # Start server
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
