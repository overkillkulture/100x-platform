#!/usr/bin/env python3
"""
Simple Analytics Receiver
Receives analytics data from the website and stores it
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Allow requests from website

ANALYTICS_FILE = 'analytics_data.json'

def load_analytics():
    """Load existing analytics"""
    if os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, 'r') as f:
            return json.load(f)
    return {'events': [], 'sessions': [], 'summary': {'total_events': 0, 'unique_visitors': 0}}

def save_analytics(data):
    """Save analytics to file"""
    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/track', methods=['POST'])
def track_event():
    """Receive analytics event"""
    try:
        event = request.json
        analytics = load_analytics()
        
        # Add timestamp
        event['server_received'] = datetime.now().isoformat()
        
        # Store event
        analytics['events'].append(event)
        analytics['summary']['total_events'] += 1
        
        # Update summary
        if event.get('event_type') == 'page_view':
            session_ids = set(e.get('session_id') for e in analytics['events'] if e.get('session_id'))
            analytics['summary']['unique_visitors'] = len(session_ids)
        
        save_analytics(analytics)
        
        return jsonify({'success': True, 'message': 'Event tracked'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get analytics summary"""
    try:
        analytics = load_analytics()
        
        # Calculate stats
        events = analytics['events']
        page_views = [e for e in events if e.get('event_type') == 'page_view']
        button_clicks = [e for e in events if e.get('event_type') == 'button_click']
        
        # Today's visitors
        today = datetime.now().date().isoformat()
        today_events = [e for e in events if e.get('server_received', '').startswith(today)]
        today_sessions = set(e.get('session_id') for e in today_events if e.get('session_id'))
        
        stats = {
            'total_events': len(events),
            'total_page_views': len(page_views),
            'total_button_clicks': len(button_clicks),
            'unique_visitors': analytics['summary']['unique_visitors'],
            'today_visitors': len(today_sessions),
            'today_events': len(today_events),
            'last_updated': datetime.now().isoformat()
        }
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recent', methods=['GET'])
def get_recent():
    """Get recent events"""
    try:
        analytics = load_analytics()
        recent = analytics['events'][-50:]  # Last 50 events
        return jsonify({'events': recent}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n📊 Analytics Receiver Starting...")
    print("📡 Listening for analytics from website")
    print("🌐 Stats available at http://localhost:5002/stats\n")
    app.run(host='0.0.0.0', port=5002, debug=True)
