"""
ACTIVE USER DETECTOR
Real-time detection of who's currently using the workspace
Detects stuck users, active sessions, and provides admin control
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime, timedelta
from collections import defaultdict
import time

app = Flask(__name__)
CORS(app)

# Active user tracking
ACTIVE_USERS = {}  # {user_id: {name, last_seen, location, status}}
USER_ACTIONS = defaultdict(list)  # {user_id: [actions]}
WORKSPACE_STATE = {
    'mode': 'normal',  # normal, maintenance, updating
    'message': None,
    'stuck_on': None  # e.g., 'police_accountability'
}

TIMEOUT_SECONDS = 300  # 5 minutes of inactivity = inactive

@app.route('/ping', methods=['POST'])
def user_ping():
    """User sends ping to show they're active"""
    data = request.json
    user_id = data.get('user_id', 'anonymous')
    user_name = data.get('user_name', user_id)
    location = data.get('location', 'unknown')
    action = data.get('action', 'browsing')

    # Update active users
    ACTIVE_USERS[user_id] = {
        'name': user_name,
        'last_seen': datetime.now().isoformat(),
        'location': location,
        'status': 'active',
        'action': action
    }

    # Log action
    USER_ACTIONS[user_id].append({
        'timestamp': datetime.now().isoformat(),
        'location': location,
        'action': action
    })

    # Keep only last 20 actions per user
    USER_ACTIONS[user_id] = USER_ACTIONS[user_id][-20:]

    return jsonify({
        'status': 'received',
        'workspace_state': WORKSPACE_STATE,
        'user_count': len(get_active_users())
    })

@app.route('/users/active', methods=['GET'])
def get_active_users_endpoint():
    """Get list of currently active users"""
    active = get_active_users()
    return jsonify({
        'active_users': active,
        'count': len(active),
        'workspace_state': WORKSPACE_STATE,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/users/stuck', methods=['GET'])
def get_stuck_users():
    """Get users who are stuck (not moving for a while)"""
    stuck = []
    now = datetime.now()

    for user_id, info in ACTIVE_USERS.items():
        last_seen = datetime.fromisoformat(info['last_seen'])
        time_stuck = (now - last_seen).total_seconds()

        # If they've been at same location for > 2 minutes, consider stuck
        if time_stuck > 120:
            stuck.append({
                'user_id': user_id,
                'name': info['name'],
                'location': info['location'],
                'time_stuck_seconds': time_stuck,
                'time_stuck_minutes': time_stuck / 60
            })

    return jsonify({
        'stuck_users': stuck,
        'count': len(stuck),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/workspace/state', methods=['GET', 'POST'])
def workspace_state():
    """Get or set workspace state"""
    global WORKSPACE_STATE

    if request.method == 'POST':
        data = request.json
        WORKSPACE_STATE['mode'] = data.get('mode', WORKSPACE_STATE['mode'])
        WORKSPACE_STATE['message'] = data.get('message', WORKSPACE_STATE['message'])
        WORKSPACE_STATE['stuck_on'] = data.get('stuck_on', WORKSPACE_STATE['stuck_on'])

        return jsonify({
            'status': 'updated',
            'workspace_state': WORKSPACE_STATE
        })

    return jsonify(WORKSPACE_STATE)

@app.route('/workspace/clear-stuck', methods=['POST'])
def clear_stuck_state():
    """Clear stuck state (like police accountability mode)"""
    global WORKSPACE_STATE

    WORKSPACE_STATE['stuck_on'] = None
    WORKSPACE_STATE['mode'] = 'normal'
    WORKSPACE_STATE['message'] = 'Workspace reset - refreshing...'

    return jsonify({
        'status': 'cleared',
        'message': 'Stuck state cleared',
        'workspace_state': WORKSPACE_STATE
    })

@app.route('/broadcast/maintenance', methods=['POST'])
def broadcast_maintenance():
    """Notify all active users of maintenance"""
    data = request.json
    message = data.get('message', 'System maintenance in progress')
    duration = data.get('duration_minutes', 5)

    WORKSPACE_STATE['mode'] = 'maintenance'
    WORKSPACE_STATE['message'] = f"{message} (Est. {duration} min)"

    active = get_active_users()

    return jsonify({
        'status': 'broadcast_sent',
        'message': WORKSPACE_STATE['message'],
        'notified_users': len(active),
        'users': [u['name'] for u in active]
    })

@app.route('/dashboard', methods=['GET'])
def admin_dashboard_data():
    """Data for admin dashboard"""
    active = get_active_users()
    stuck = get_stuck_users().json['stuck_users']

    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'workspace_state': WORKSPACE_STATE,
        'active_users': {
            'count': len(active),
            'users': active
        },
        'stuck_users': {
            'count': len(stuck),
            'users': stuck
        },
        'total_tracked': len(ACTIVE_USERS)
    })

def get_active_users():
    """Get users who are currently active (seen in last 5 min)"""
    active = []
    now = datetime.now()

    for user_id, info in ACTIVE_USERS.items():
        last_seen = datetime.fromisoformat(info['last_seen'])
        seconds_ago = (now - last_seen).total_seconds()

        if seconds_ago < TIMEOUT_SECONDS:
            active.append({
                'user_id': user_id,
                'name': info['name'],
                'location': info['location'],
                'action': info['action'],
                'last_seen': info['last_seen'],
                'seconds_ago': seconds_ago
            })

    return active

def cleanup_inactive_users():
    """Remove users who haven't been seen in a while"""
    to_remove = []
    now = datetime.now()

    for user_id, info in ACTIVE_USERS.items():
        last_seen = datetime.fromisoformat(info['last_seen'])
        if (now - last_seen).total_seconds() > TIMEOUT_SECONDS * 2:
            to_remove.append(user_id)

    for user_id in to_remove:
        del ACTIVE_USERS[user_id]
        if user_id in USER_ACTIONS:
            del USER_ACTIONS[user_id]

if __name__ == '__main__':
    print("\n" + "="*60)
    print("👁️ ACTIVE USER DETECTOR")
    print("="*60)
    print("\n🚀 Starting on http://localhost:7779")
    print("\nEndpoints:")
    print("  POST /ping - User activity ping")
    print("  GET /users/active - Get active users")
    print("  GET /users/stuck - Get stuck users")
    print("  GET /workspace/state - Get workspace state")
    print("  POST /workspace/state - Set workspace state")
    print("  POST /workspace/clear-stuck - Clear stuck state")
    print("  POST /broadcast/maintenance - Notify users")
    print("  GET /dashboard - Admin dashboard data")
    print("\n✅ Active User Detector ready")

    app.run(host='0.0.0.0', port=7779, debug=False)
