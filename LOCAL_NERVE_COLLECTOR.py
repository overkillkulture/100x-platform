#!/usr/bin/env python3
"""
LOCAL NERVE COLLECTOR
Receives visitor heartbeats LOCALLY (no cloud dependency)
Stores in-house, feeds nervous system analytics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
from pathlib import Path
from collections import defaultdict
import sys

# Import Instagram automation
try:
    from INSTAGRAM_AUTOMATION import InstagramBot
    instagram_bot = InstagramBot()
    INSTAGRAM_ENABLED = True
    print("✅ Instagram automation loaded")
except Exception as e:
    print(f"⚠️  Instagram automation not available: {e}")
    INSTAGRAM_ENABLED = False

app = Flask(__name__)
CORS(app)

# In-house data storage
VISITOR_DATA_DIR = Path(__file__).parent / 'visitor_data'
VISITOR_DATA_DIR.mkdir(exist_ok=True)

# Live nerve state (in memory)
active_visitors = {}  # pin -> visitor_data
page_nerves = defaultdict(int)  # page -> visitor_count
heartbeat_log = []  # Last 1000 heartbeats

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'CONNECTED',
        'active_visitors': len(active_visitors),
        'pages_active': len(page_nerves),
        'heartbeats_logged': len(heartbeat_log)
    })

@app.route('/api/visitor/heartbeat', methods=['POST'])
def receive_heartbeat():
    """Receive visitor heartbeat (like a nerve firing)"""
    data = request.json

    pin = data.get('pin', 'anonymous')
    page = data.get('page', '/')
    timestamp = data.get('timestamp', datetime.now().isoformat())

    # Store in active visitors (live nerve state)
    active_visitors[pin] = {
        'pin': pin,
        'name': data.get('name', 'Guest'),
        'page': page,
        'timestamp': timestamp,
        'timeOnPage': data.get('timeOnPage', 0),
        'isActive': data.get('isActive', True),
        'userAgent': data.get('userAgent', ''),
        'referrer': data.get('referrer', '')
    }

    # Track page nerve activity
    page_nerves[page] += 1

    # Log heartbeat
    heartbeat_log.append({
        'pin': pin,
        'page': page,
        'timestamp': timestamp,
        'active': data.get('isActive', True)
    })

    # Keep only last 1000 heartbeats
    if len(heartbeat_log) > 1000:
        heartbeat_log.pop(0)

    # Write to local file (persistent)
    write_heartbeat_to_file(data)

    print(f"💓 HEARTBEAT: {pin} on {page} ({len(active_visitors)} active)")

    return jsonify({'status': 'received', 'active_count': len(active_visitors)})

@app.route('/api/visitor/active', methods=['GET'])
def get_active_visitors():
    """Get currently active visitors (live nerve state)"""
    # Remove stale visitors (no heartbeat in last 30 seconds)
    now = datetime.now()
    stale_pins = []

    for pin, visitor in active_visitors.items():
        visitor_time = datetime.fromisoformat(visitor['timestamp'].replace('Z', '+00:00'))
        age = (now - visitor_time.replace(tzinfo=None)).total_seconds()

        if age > 30:  # 30 seconds = stale
            stale_pins.append(pin)

    for pin in stale_pins:
        del active_visitors[pin]
        print(f"⏱️  Removed stale visitor: {pin}")

    return jsonify(list(active_visitors.values()))

@app.route('/api/nerves/pages', methods=['GET'])
def get_page_nerves():
    """Get page nerve activity (which pages are hot)"""
    sorted_nerves = sorted(page_nerves.items(), key=lambda x: x[1], reverse=True)

    return jsonify([
        {'page': page, 'hits': hits}
        for page, hits in sorted_nerves[:20]  # Top 20 hottest pages
    ])

@app.route('/api/nerves/stats', methods=['GET'])
def get_nerve_stats():
    """Get overall nerve statistics"""
    now = datetime.now()
    today_file = VISITOR_DATA_DIR / f"daily_report_{now.strftime('%Y-%m-%d')}.json"

    stats = {
        'active_visitors': len(active_visitors),
        'total_pages': len(page_nerves),
        'heartbeats_per_minute': len([h for h in heartbeat_log if (now - datetime.fromisoformat(h['timestamp'].replace('Z', '+00:00')).replace(tzinfo=None)).total_seconds() < 60]),
        'hottest_page': max(page_nerves.items(), key=lambda x: x[1])[0] if page_nerves else None
    }

    # Load today's persistent data
    if today_file.exists():
        with open(today_file, 'r') as f:
            daily_data = json.load(f)
            stats['total_today'] = daily_data.get('summary', {}).get('total_visitors', 0)

    return jsonify(stats)

def write_heartbeat_to_file(data):
    """Write heartbeat to local JSONL file (persistent log)"""
    now = datetime.now()
    log_file = VISITOR_DATA_DIR / f"heartbeats_{now.strftime('%Y-%m-%d')}.jsonl"

    with open(log_file, 'a') as f:
        f.write(json.dumps({
            'timestamp': data.get('timestamp', now.isoformat()),
            'pin': data.get('pin', 'anonymous'),
            'page': data.get('page', '/'),
            'active': data.get('isActive', True)
        }) + '\n')

@app.route('/api/visitor/inactive', methods=['POST'])
def visitor_inactive():
    """Mark visitor as inactive (tab hidden)"""
    data = request.json
    pin = data.get('pin', 'anonymous')

    if pin in active_visitors:
        active_visitors[pin]['isActive'] = False
        print(f"😴 INACTIVE: {pin}")

    return jsonify({'status': 'marked_inactive'})

# ==========================================
# INSTAGRAM INTEGRATION ENDPOINTS
# ==========================================

@app.route('/api/instagram/status/<username>', methods=['GET'])
def check_instagram_status(username):
    """Check if someone is online on Instagram"""
    if not INSTAGRAM_ENABLED:
        return jsonify({'error': 'Instagram automation not available'}), 503

    try:
        status = instagram_bot.check_online_status(username)
        print(f"📷 Instagram Status Check: @{username} -> {status.get('status')}")
        return jsonify(status)
    except Exception as e:
        print(f"❌ Instagram status check failed: {e}")
        return jsonify({'error': str(e), 'username': username, 'online': None}), 500

@app.route('/api/instagram/send-dm', methods=['POST'])
def send_instagram_dm():
    """Send Instagram DM"""
    if not INSTAGRAM_ENABLED:
        return jsonify({'error': 'Instagram automation not available'}), 503

    data = request.json
    username = data.get('username')
    message = data.get('message')

    if not username or not message:
        return jsonify({'error': 'Missing username or message'}), 400

    try:
        success = instagram_bot.send_dm(username, message)

        if success:
            print(f"📷 Instagram DM Sent: @{username}")
            return jsonify({'status': 'sent', 'username': username})
        else:
            return jsonify({'status': 'rate_limited', 'username': username}), 429
    except Exception as e:
        print(f"❌ Instagram DM failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/instagram/stats', methods=['GET'])
def get_instagram_stats():
    """Get Instagram messaging stats (rate limits)"""
    if not INSTAGRAM_ENABLED:
        return jsonify({'error': 'Instagram automation not available'}), 503

    stats = instagram_bot.get_message_stats()
    return jsonify(stats)

# ==========================================
# INTERCOM SYSTEM (Commander -> Visitors)
# ==========================================

intercom_messages = defaultdict(list)  # pin -> [messages]

@app.route('/api/intercom/send', methods=['POST'])
def send_intercom_message():
    """Send message to specific visitor via website popup"""
    data = request.json
    pin = data.get('pin')
    from_user = data.get('from', 'Commander')
    message = data.get('message')

    if not pin or not message:
        return jsonify({'error': 'Missing pin or message'}), 400

    # Store message for this pin
    intercom_messages[pin].append({
        'from': from_user,
        'message': message,
        'timestamp': datetime.now().isoformat()
    })

    print(f"💬 Intercom: {from_user} → {pin}: {message}")

    return jsonify({'status': 'queued', 'pin': pin})

@app.route('/api/intercom/poll/<pin>', methods=['GET'])
def poll_intercom_messages(pin):
    """Poll for messages (visitor checks for new messages)"""
    messages = intercom_messages.get(pin, [])

    # Clear messages after delivery
    if messages:
        intercom_messages[pin] = []
        print(f"📬 Delivered {len(messages)} message(s) to {pin}")

    return jsonify(messages)

if __name__ == '__main__':
    print("="*60)
    print("🧠 LOCAL NERVE COLLECTOR STARTING")
    print("="*60)
    print("📍 Port: 6000")
    print("📂 Data: visitor_data/")
    print("💓 Heartbeats: Receiving...")
    print("🌐 CORS: Enabled (all origins)")
    print("="*60)

    app.run(host='0.0.0.0', port=6000, debug=False)
