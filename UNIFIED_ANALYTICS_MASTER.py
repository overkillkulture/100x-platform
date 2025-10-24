#!/usr/bin/env python3
"""
UNIFIED ANALYTICS MASTER - ALL ANALYTICS IN ONE PLACE
Consolidates ALL scattered analytics into unified real-time tracking

Features:
- Real-time "Who's Online Now" tracking
- Full user session journeys (every page, every click)
- Time tracking (how long on each page)
- Live activity feed (what's happening RIGHT NOW)
- User identification (who is testosterone tiger?)
- Path analysis (where are they going?)
- Machine learning ready data format
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime, timedelta
from collections import defaultdict
import json
import os
from pathlib import Path
import hashlib

app = Flask(__name__)
CORS(app)

# Data storage
DATA_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/unified_analytics")
DATA_DIR.mkdir(exist_ok=True)

# In-memory session tracking (for real-time)
ACTIVE_SESSIONS = {}  # session_id -> session data
USER_PROFILES = {}     # user_id -> profile data
LIVE_ACTIVITY = []     # Recent activity (last 100 events)

class UnifiedAnalytics:
    def __init__(self):
        self.sessions_file = DATA_DIR / "all_sessions.jsonl"
        self.events_file = DATA_DIR / "all_events.jsonl"
        self.users_file = DATA_DIR / "all_users.json"

    def get_session_id(self, request):
        """Generate or retrieve session ID"""
        # Use IP + User-Agent hash as session ID
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get('User-Agent', '')
        session_id = hashlib.md5(f"{ip}:{user_agent}".encode()).hexdigest()[:16]
        return session_id

    def track_page_view(self, session_id, page, data=None):
        """Track page view with full context"""
        timestamp = datetime.now()

        # Update active session
        if session_id not in ACTIVE_SESSIONS:
            ACTIVE_SESSIONS[session_id] = {
                'session_id': session_id,
                'started': timestamp.isoformat(),
                'last_seen': timestamp.isoformat(),
                'pages_viewed': [],
                'total_time': 0,
                'user_name': data.get('user_name', 'Anonymous'),
                'ip': data.get('ip', 'Unknown'),
                'user_agent': data.get('user_agent', 'Unknown')
            }

        session = ACTIVE_SESSIONS[session_id]
        session['last_seen'] = timestamp.isoformat()
        session['pages_viewed'].append({
            'page': page,
            'timestamp': timestamp.isoformat(),
            'data': data or {}
        })

        # Add to live activity feed
        LIVE_ACTIVITY.append({
            'timestamp': timestamp.isoformat(),
            'session_id': session_id,
            'user_name': session['user_name'],
            'action': 'page_view',
            'page': page,
            'data': data
        })

        # Keep only last 100 events
        if len(LIVE_ACTIVITY) > 100:
            LIVE_ACTIVITY.pop(0)

        # Log to permanent storage
        with open(self.events_file, 'a') as f:
            f.write(json.dumps({
                'timestamp': timestamp.isoformat(),
                'session_id': session_id,
                'event_type': 'page_view',
                'page': page,
                'data': data
            }) + '\n')

        return session

    def get_online_now(self):
        """Get all users online in last 5 minutes"""
        cutoff = datetime.now() - timedelta(minutes=5)

        online = []
        for session_id, session in ACTIVE_SESSIONS.items():
            last_seen = datetime.fromisoformat(session['last_seen'])
            if last_seen > cutoff:
                # Calculate time on site
                started = datetime.fromisoformat(session['started'])
                time_on_site = (datetime.now() - started).total_seconds()

                online.append({
                    'session_id': session_id,
                    'user_name': session['user_name'],
                    'current_page': session['pages_viewed'][-1]['page'] if session['pages_viewed'] else 'Unknown',
                    'time_on_site': int(time_on_site),
                    'pages_viewed': len(session['pages_viewed']),
                    'last_seen': session['last_seen'],
                    'started': session['started']
                })

        return sorted(online, key=lambda x: x['last_seen'], reverse=True)

    def get_session_journey(self, session_id):
        """Get complete user journey for a session"""
        if session_id not in ACTIVE_SESSIONS:
            return None

        session = ACTIVE_SESSIONS[session_id]

        # Calculate time on each page
        pages_with_duration = []
        for i, page_view in enumerate(session['pages_viewed']):
            start_time = datetime.fromisoformat(page_view['timestamp'])

            # If there's a next page, calculate duration
            if i + 1 < len(session['pages_viewed']):
                end_time = datetime.fromisoformat(session['pages_viewed'][i + 1]['timestamp'])
                duration = (end_time - start_time).total_seconds()
            else:
                # Current page - calculate from now
                duration = (datetime.now() - start_time).total_seconds()

            pages_with_duration.append({
                'page': page_view['page'],
                'timestamp': page_view['timestamp'],
                'duration_seconds': int(duration),
                'data': page_view.get('data', {})
            })

        return {
            'session_id': session_id,
            'user_name': session['user_name'],
            'started': session['started'],
            'last_seen': session['last_seen'],
            'journey': pages_with_duration
        }

analytics = UnifiedAnalytics()

# ==================== API ENDPOINTS ====================

@app.route('/track', methods=['POST'])
def track_event():
    """Track any event from any page"""
    data = request.json
    session_id = analytics.get_session_id(request)

    # Add request context
    data['ip'] = request.headers.get('X-Forwarded-For', request.remote_addr)
    data['user_agent'] = request.headers.get('User-Agent', '')

    page = data.get('page', 'unknown')
    session = analytics.track_page_view(session_id, page, data)

    return jsonify({
        'success': True,
        'session_id': session_id,
        'session': session
    })

@app.route('/online', methods=['GET'])
def get_online():
    """Get all users currently online"""
    online = analytics.get_online_now()
    return jsonify({
        'count': len(online),
        'users': online,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get complete journey for a session"""
    journey = analytics.get_session_journey(session_id)
    if not journey:
        return jsonify({'error': 'Session not found'}), 404
    return jsonify(journey)

@app.route('/live-feed', methods=['GET'])
def get_live_feed():
    """Get live activity feed (last 100 events)"""
    return jsonify({
        'events': LIVE_ACTIVITY,
        'count': len(LIVE_ACTIVITY)
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    online = analytics.get_online_now()

    return jsonify({
        'currently_online': len(online),
        'total_sessions': len(ACTIVE_SESSIONS),
        'total_events': len(LIVE_ACTIVITY),
        'online_users': online
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Unified Analytics ONLINE', 'active_sessions': len(ACTIVE_SESSIONS)})

@app.route('/', methods=['GET'])
def dashboard():
    """Unified Analytics Dashboard"""
    return render_template_string(DASHBOARD_HTML)

# ==================== DASHBOARD HTML ====================

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>UNIFIED ANALYTICS - Real-Time Command Center</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: #000;
            color: #00ff00;
            padding: 20px;
        }
        h1 {
            text-align: center;
            font-size: 48px;
            color: #ff6b00;
            text-shadow: 0 0 20px #ff6b00;
            margin-bottom: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(0, 255, 0, 0.1);
            border: 2px solid #00ff00;
            padding: 20px;
            border-radius: 10px;
        }
        .stat-label {
            font-size: 14px;
            color: #00ddff;
            margin-bottom: 5px;
        }
        .stat-value {
            font-size: 36px;
            font-weight: bold;
        }
        .section {
            background: rgba(0, 0, 0, 0.8);
            border: 3px solid #00ff00;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
        }
        .section h2 {
            color: #00ddff;
            margin-bottom: 15px;
        }
        .user-card {
            background: rgba(255, 107, 0, 0.1);
            border: 2px solid #ff6b00;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .user-name {
            font-size: 20px;
            color: #ff6b00;
            font-weight: bold;
        }
        .user-page {
            color: #00ddff;
            margin: 5px 0;
        }
        .user-time {
            color: #00ff00;
            font-size: 12px;
        }
        .journey-step {
            background: rgba(0, 221, 255, 0.1);
            border-left: 4px solid #00ddff;
            padding: 10px;
            margin: 5px 0;
        }
        .live-event {
            padding: 10px;
            border-bottom: 1px solid #00ff00;
            animation: flash 0.5s;
        }
        @keyframes flash {
            from { background: rgba(0, 255, 0, 0.3); }
            to { background: transparent; }
        }
    </style>
</head>
<body>
    <h1>🔴 UNIFIED ANALYTICS - LIVE</h1>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">CURRENTLY ONLINE</div>
            <div class="stat-value" id="online-count">0</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">TOTAL SESSIONS</div>
            <div class="stat-value" id="total-sessions">0</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">LIVE EVENTS</div>
            <div class="stat-value" id="live-events">0</div>
        </div>
    </div>

    <div class="section">
        <h2>👥 WHO'S ONLINE NOW</h2>
        <div id="online-users"></div>
    </div>

    <div class="section">
        <h2>📊 LIVE ACTIVITY FEED</h2>
        <div id="live-feed"></div>
    </div>

    <script>
        async function refresh() {
            // Get stats
            const statsRes = await fetch('/stats');
            const stats = await statsRes.json();

            document.getElementById('online-count').textContent = stats.currently_online;
            document.getElementById('total-sessions').textContent = stats.total_sessions;

            // Get live feed
            const feedRes = await fetch('/live-feed');
            const feed = await feedRes.json();

            document.getElementById('live-events').textContent = feed.count;

            // Display online users
            const usersHTML = stats.online_users.map(user => `
                <div class="user-card">
                    <div class="user-name">${user.user_name}</div>
                    <div class="user-page">📄 Current: ${user.current_page}</div>
                    <div class="user-page">🔢 Pages viewed: ${user.pages_viewed}</div>
                    <div class="user-time">⏱️ Time on site: ${Math.floor(user.time_on_site / 60)}m ${user.time_on_site % 60}s</div>
                    <div class="user-time">👁️ Last seen: ${new Date(user.last_seen).toLocaleTimeString()}</div>
                </div>
            `).join('');

            document.getElementById('online-users').innerHTML = usersHTML || '<p>No users currently online</p>';

            // Display live feed
            const feedHTML = feed.events.slice().reverse().slice(0, 20).map(event => `
                <div class="live-event">
                    <strong>${event.user_name}</strong> viewed <strong>${event.page}</strong>
                    <span style="float: right; color: #666;">${new Date(event.timestamp).toLocaleTimeString()}</span>
                </div>
            `).join('');

            document.getElementById('live-feed').innerHTML = feedHTML || '<p>No recent activity</p>';
        }

        // Refresh every 2 seconds
        setInterval(refresh, 2000);
        refresh();
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print('🚀 UNIFIED ANALYTICS MASTER starting on port 9000...')
    print('📊 Dashboard: http://localhost:9000')
    print('🔴 Real-time tracking ENABLED')
    app.run(host='0.0.0.0', port=9000, debug=True)
