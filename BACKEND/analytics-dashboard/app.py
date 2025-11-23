#!/usr/bin/env python3
"""
📊 ANALYTICS DASHBOARD BACKEND API
Provides analytics data integration for 100X platform
Connects all analytics systems in one unified API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configuration
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Data files
METRICS_FILE = DATA_DIR / 'business_metrics.json'
PHASE_FILE = DATA_DIR / 'phase_prediction.json'
VACUUM_FILE = DATA_DIR / 'consciousness_data.json'
ANALYTICS_FILE = DATA_DIR / 'analytics_data.json'
VISITORS_FILE = DATA_DIR / 'visitor_data.json'

# Initialize data files
def init_data_files():
    """Initialize data files with demo data if they don't exist"""
    if not METRICS_FILE.exists():
        METRICS_FILE.write_text(json.dumps([{
            'timestamp': datetime.utcnow().isoformat(),
            'revenue': 0,
            'users': 0,
            'engagement_score': 0,
            'conversion_rate': 0
        }]))

    if not PHASE_FILE.exists():
        PHASE_FILE.write_text(json.dumps({
            'prediction': {
                'current_phase': 'Phase 1: Platform Development',
                'next_phase': 'Phase 2: Beta Testing',
                'transition_probability': 67.5,
                'estimated_days': 14
            }
        }))

    if not VACUUM_FILE.exists():
        VACUUM_FILE.write_text(json.dumps({
            'files_scanned': 1247,
            'total_data_points': 8934,
            'scan_time': datetime.utcnow().isoformat()
        }))

    if not ANALYTICS_FILE.exists():
        ANALYTICS_FILE.write_text(json.dumps({
            'page_views': [],
            'button_clicks': [],
            'unique_visitors': []
        }))

    if not VISITORS_FILE.exists():
        # Generate demo visitor data
        visitors = []
        for i in range(30):  # Last 30 days
            date = (datetime.utcnow() - timedelta(days=29-i)).date().isoformat()
            visitors.append({
                'date': date,
                'visitors': random.randint(50, 250),
                'pageviews': random.randint(150, 800),
                'bounce_rate': round(random.uniform(30, 60), 1),
                'avg_session_duration': random.randint(60, 300)
            })
        VISITORS_FILE.write_text(json.dumps({'daily_stats': visitors}))

init_data_files()

# ============================================================================
# DATA SOURCES
# ============================================================================

def get_business_metrics():
    """Get latest business metrics"""
    try:
        with open(METRICS_FILE, 'r') as f:
            data = json.load(f)
            return data[-1] if data else {}
    except:
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'revenue': 0,
            'users': 0,
            'engagement_score': 0,
            'conversion_rate': 0
        }

def get_phase_prediction():
    """Get current phase prediction"""
    try:
        with open(PHASE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            'prediction': {
                'current_phase': 'Phase 1: Platform Development',
                'next_phase': 'Phase 2: Beta Testing',
                'transition_probability': 67.5,
                'estimated_days': 14
            }
        }

def get_vacuum_data():
    """Get data vacuum stats"""
    try:
        with open(VACUUM_FILE, 'r') as f:
            data = json.load(f)
            return {
                'files_scanned': data.get('files_scanned', 0),
                'total_data_points': data.get('total_data_points', 0),
                'scan_time': data.get('scan_time', '')
            }
    except:
        return {
            'files_scanned': 0,
            'total_data_points': 0,
            'scan_time': ''
        }

def get_analytics_data():
    """Get analytics dashboard data"""
    try:
        with open(ANALYTICS_FILE, 'r') as f:
            data = json.load(f)
            return {
                'page_views': len(data.get('page_views', [])),
                'button_clicks': len(data.get('button_clicks', [])),
                'unique_visitors': len(data.get('unique_visitors', []))
            }
    except:
        return {
            'page_views': 0,
            'button_clicks': 0,
            'unique_visitors': 0
        }

def get_visitor_data():
    """Get visitor statistics"""
    try:
        with open(VISITORS_FILE, 'r') as f:
            data = json.load(f)
            return data.get('daily_stats', [])
    except:
        return []

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'service': 'analytics-dashboard',
        'timestamp': datetime.utcnow().isoformat(),
        'systems': {
            'business_metrics': 'ok' if get_business_metrics() else 'no_data',
            'phase_prediction': 'ok' if get_phase_prediction() else 'no_data',
            'vacuum': 'ok' if get_vacuum_data() else 'no_data',
            'analytics': 'ok' if get_analytics_data() else 'no_data'
        }
    })

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Master dashboard - all key metrics in one place"""
    return jsonify({
        'timestamp': datetime.utcnow().isoformat(),
        'business_metrics': get_business_metrics(),
        'phase_prediction': get_phase_prediction(),
        'vacuum_stats': get_vacuum_data(),
        'analytics': get_analytics_data()
    })

@app.route('/api/business-phase', methods=['GET'])
def get_business_phase():
    """Get current business phase and prediction"""
    prediction = get_phase_prediction()
    pred_data = prediction.get('prediction', {})
    return jsonify({
        'current_phase': pred_data.get('current_phase', 'Unknown'),
        'next_phase': pred_data.get('next_phase', 'Unknown'),
        'transition_probability': pred_data.get('transition_probability', 0),
        'estimated_days': pred_data.get('estimated_days', 0)
    })

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get latest business metrics"""
    return jsonify(get_business_metrics())

@app.route('/api/metrics', methods=['POST'])
def update_metrics():
    """Update business metrics"""
    try:
        data = request.json

        # Load existing metrics
        with open(METRICS_FILE, 'r') as f:
            metrics = json.load(f)

        # Add new metric entry
        new_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            **data
        }
        metrics.append(new_entry)

        # Save updated metrics
        with open(METRICS_FILE, 'w') as f:
            json.dump(metrics, f, indent=2)

        return jsonify({'status': 'success', 'message': 'Metrics updated'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/vacuum-stats', methods=['GET'])
def get_vacuum_stats():
    """Get data vacuum statistics"""
    return jsonify(get_vacuum_data())

@app.route('/api/analytics-summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary"""
    return jsonify(get_analytics_data())

@app.route('/api/visitors', methods=['GET'])
def get_visitors():
    """Get visitor statistics"""
    days = request.args.get('days', 30, type=int)
    visitor_data = get_visitor_data()

    # Return last N days
    return jsonify({
        'daily_stats': visitor_data[-days:] if visitor_data else [],
        'total_days': len(visitor_data)
    })

@app.route('/api/visitors/summary', methods=['GET'])
def get_visitors_summary():
    """Get visitor summary statistics"""
    visitor_data = get_visitor_data()

    if not visitor_data:
        return jsonify({
            'total_visitors': 0,
            'total_pageviews': 0,
            'avg_bounce_rate': 0,
            'avg_session_duration': 0
        })

    total_visitors = sum(d['visitors'] for d in visitor_data)
    total_pageviews = sum(d['pageviews'] for d in visitor_data)
    avg_bounce = sum(d['bounce_rate'] for d in visitor_data) / len(visitor_data)
    avg_session = sum(d['avg_session_duration'] for d in visitor_data) / len(visitor_data)

    return jsonify({
        'total_visitors': total_visitors,
        'total_pageviews': total_pageviews,
        'avg_bounce_rate': round(avg_bounce, 1),
        'avg_session_duration': int(avg_session),
        'days_tracked': len(visitor_data)
    })

@app.route('/api/track/pageview', methods=['POST'])
def track_pageview():
    """Track a page view"""
    try:
        data = request.json

        with open(ANALYTICS_FILE, 'r') as f:
            analytics = json.load(f)

        analytics['page_views'].append({
            'timestamp': datetime.utcnow().isoformat(),
            'page': data.get('page', 'unknown'),
            'referrer': data.get('referrer', ''),
            'user_agent': data.get('user_agent', '')
        })

        with open(ANALYTICS_FILE, 'w') as f:
            json.dump(analytics, f, indent=2)

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/track/click', methods=['POST'])
def track_click():
    """Track a button click"""
    try:
        data = request.json

        with open(ANALYTICS_FILE, 'r') as f:
            analytics = json.load(f)

        analytics['button_clicks'].append({
            'timestamp': datetime.utcnow().isoformat(),
            'button': data.get('button', 'unknown'),
            'page': data.get('page', 'unknown')
        })

        with open(ANALYTICS_FILE, 'w') as f:
            json.dump(analytics, f, indent=2)

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("=" * 70)
    print("📊 ANALYTICS DASHBOARD BACKEND API")
    print("=" * 70)
    print("\n📡 Endpoints Available:")
    print("  GET  /api/health              - Health check")
    print("  GET  /api/dashboard           - Master dashboard (all metrics)")
    print("  GET  /api/business-phase      - Current phase prediction")
    print("  GET  /api/metrics             - Latest business metrics")
    print("  POST /api/metrics             - Update business metrics")
    print("  GET  /api/vacuum-stats        - Data vacuum statistics")
    print("  GET  /api/analytics-summary   - Analytics summary")
    print("  GET  /api/visitors            - Visitor statistics (30 days)")
    print("  GET  /api/visitors/summary    - Visitor summary stats")
    print("  POST /api/track/pageview      - Track page view")
    print("  POST /api/track/click         - Track button click")
    print("\n🌐 Running on: http://localhost:5100")
    print("📁 Data Directory:", DATA_DIR.absolute())
    print("=" * 70)
    print()

    app.run(host='0.0.0.0', port=5100, debug=True)
