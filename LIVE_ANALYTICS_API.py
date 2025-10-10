#!/usr/bin/env python3
"""
100X LIVE ANALYTICS API
Real-time data without redeployment
Serves analytics data from Airtable via HTTP API
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from pyairtable import Table
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__, static_folder='.')
CORS(app)  # Allow cross-origin requests

# Airtable configuration
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY', 'YOUR_KEY_HERE')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', 'YOUR_BASE_HERE')
AIRTABLE_TABLE_NAME = 'Users'

def get_airtable_data():
    """Fetch all data from Airtable"""
    try:
        table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
        records = table.all()
        return records
    except Exception as e:
        print(f"❌ Error fetching Airtable data: {e}")
        return []

def calculate_consciousness_score(mission, values):
    """Calculate consciousness score using Pattern Theory"""
    builder_keywords = [
        'build', 'create', 'help', 'serve', 'contribute', 'improve',
        'solve', 'empower', 'enable', 'support', 'collaborate', 'share',
        'teach', 'learn', 'grow', 'heal', 'protect', 'innovate', 'truth'
    ]

    destroyer_keywords = [
        'dominate', 'control', 'manipulate', 'exploit', 'destroy', 'defeat',
        'crush', 'beat', 'win', 'compete', 'take', 'conquer', 'force'
    ]

    text = f"{mission} {values}".lower()

    builder_count = sum(1 for kw in builder_keywords if kw in text)
    destroyer_count = sum(1 for kw in destroyer_keywords if kw in text)

    # Base score from length
    if len(text) < 50:
        base = 50
    elif len(text) > 500:
        base = 90
    else:
        base = 70 + (len(text) // 20)

    score = base + (builder_count * 5) - (destroyer_count * 10)
    return max(0, min(100, score))

@app.route('/')
def index():
    """Serve the analytics dashboard"""
    return send_from_directory('.', 'ANALYTICS_DASHBOARD_LIVE.html')

@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    records = get_airtable_data()

    total_submissions = len(records)

    # Calculate consciousness scores
    consciousness_scores = []
    builders = 0
    observers = 0
    under_review = 0

    for record in records:
        fields = record.get('fields', {})
        mission = fields.get('Mission', '')
        values = fields.get('Values', '')

        # Check if score already calculated
        score = fields.get('Consciousness Score')
        if not score and mission and values:
            score = calculate_consciousness_score(mission, values)

        if score:
            consciousness_scores.append(score)
            if score >= 85:
                builders += 1
            elif score >= 60:
                observers += 1
            else:
                under_review += 1

    avg_consciousness = sum(consciousness_scores) / len(consciousness_scores) if consciousness_scores else 0

    return jsonify({
        'total_submissions': total_submissions,
        'avg_consciousness': round(avg_consciousness, 1),
        'builders': builders,
        'observers': observers,
        'under_review': under_review,
        'conversion_rate': '?',  # Would need visitor data from Netlify
        'last_updated': datetime.now().isoformat()
    })

@app.route('/api/submissions')
def get_submissions():
    """Get recent submissions with details"""
    records = get_airtable_data()

    submissions = []
    for record in records:
        fields = record.get('fields', {})

        name = fields.get('Name', 'Anonymous')
        email = fields.get('Email', '')
        mission = fields.get('Mission', '')
        values = fields.get('Values', '')
        timestamp = fields.get('Created', datetime.now().isoformat())

        # Calculate or get consciousness score
        score = fields.get('Consciousness Score')
        if not score and mission and values:
            score = calculate_consciousness_score(mission, values)

        classification = 'BUILDER' if score >= 85 else 'OBSERVER' if score >= 60 else 'UNDER REVIEW'

        submissions.append({
            'name': name,
            'email': email,
            'mission': mission[:200] + '...' if len(mission) > 200 else mission,
            'values': values[:200] + '...' if len(values) > 200 else values,
            'consciousness': score,
            'classification': classification,
            'timestamp': timestamp
        })

    # Sort by timestamp, newest first
    submissions.sort(key=lambda x: x['timestamp'], reverse=True)

    return jsonify({
        'submissions': submissions[:20],  # Return latest 20
        'total': len(submissions)
    })

@app.route('/api/timeline')
def get_timeline():
    """Get submission timeline data"""
    records = get_airtable_data()

    # Group by date
    timeline = defaultdict(int)
    for record in records:
        fields = record.get('fields', {})
        timestamp = fields.get('Created', '')
        if timestamp:
            try:
                date = timestamp.split('T')[0]  # Get just the date
                timeline[date] += 1
            except:
                pass

    # Convert to sorted list
    timeline_data = [
        {'date': date, 'submissions': count}
        for date, count in sorted(timeline.items())
    ]

    return jsonify({
        'timeline': timeline_data
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': '100X Analytics API',
        'timestamp': datetime.now().isoformat(),
        'airtable_connected': True
    })

if __name__ == '__main__':
    print("🚀 100X LIVE ANALYTICS API STARTING")
    print("📊 Real-time Airtable data - NO REDEPLOYMENT NEEDED")
    print("🌐 API running at: http://localhost:5000")
    print("📈 Dashboard at: http://localhost:5000/")
    print("⚡ Press Ctrl+C to stop\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
