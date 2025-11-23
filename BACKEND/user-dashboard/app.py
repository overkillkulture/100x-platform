#!/usr/bin/env python3
"""
USER DASHBOARD BACKEND API
Provides user management and dashboard data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import jwt
import hashlib

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.getenv('SECRET_KEY', 'user-dashboard-secret-key')
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / 'users.json'
ACTIVITY_FILE = DATA_DIR / 'activity.json'

def init_data():
    if not USERS_FILE.exists():
        USERS_FILE.write_text(json.dumps({'users': []}))
    if not ACTIVITY_FILE.exists():
        ACTIVITY_FILE.write_text(json.dumps({'activities': []}))

init_data()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['email']
    except:
        return None

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'user-dashboard', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name', 'User')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    with open(USERS_FILE, 'r') as f:
        users_data = json.load(f)

    if any(u['email'] == email for u in users_data['users']):
        return jsonify({'error': 'User already exists'}), 400

    new_user = {
        'email': email,
        'password': hash_password(password),
        'name': name,
        'created_at': datetime.utcnow().isoformat(),
        'subscription': 'free',
        'consciousness_level': 85
    }

    users_data['users'].append(new_user)
    with open(USERS_FILE, 'w') as f:
        json.dump(users_data, f, indent=2)

    token = create_token(email)
    return jsonify({'success': True, 'token': token, 'user': {'email': email, 'name': name}})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    with open(USERS_FILE, 'r') as f:
        users_data = json.load(f)

    user = next((u for u in users_data['users'] if u['email'] == email), None)

    if not user or user['password'] != hash_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_token(email)
    return jsonify({'success': True, 'token': token, 'user': {'email': user['email'], 'name': user['name']}})

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Invalid authorization header'}), 401

    token = auth_header.split(' ')[1]
    email = verify_token(token)

    if not email:
        return jsonify({'error': 'Invalid or expired token'}), 401

    with open(USERS_FILE, 'r') as f:
        users_data = json.load(f)

    user = next((u for u in users_data['users'] if u['email'] == email), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'email': user['email'],
        'name': user['name'],
        'subscription': user.get('subscription', 'free'),
        'consciousness_level': user.get('consciousness_level', 85),
        'created_at': user.get('created_at')
    })

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401

    token = auth_header.split(' ')[1]
    email = verify_token(token)
    if not email:
        return jsonify({'error': 'Invalid token'}), 401

    return jsonify({
        'projects_completed': 12,
        'total_tasks': 47,
        'completed_tasks': 39,
        'modules_accessed': 18,
        'streak_days': 7,
        'achievements': ['Platform Explorer', 'First KORPAK', 'Week Streak']
    })

if __name__ == '__main__':
    print("="*70)
    print("USER DASHBOARD BACKEND API")
    print("="*70)
    print("\nEndpoints:")
    print("  GET  /api/health")
    print("  POST /api/auth/register")
    print("  POST /api/auth/login")
    print("  GET  /api/auth/me")
    print("  GET  /api/dashboard/stats")
    print("\nRunning on: http://localhost:3001")
    print("="*70)
    print()
    app.run(host='0.0.0.0', port=3001, debug=True)
