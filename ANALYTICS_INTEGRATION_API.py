#!/usr/bin/env python3
"""
📊 ANALYTICS INTEGRATION API 📊
Framework for connecting all 100X analytics systems

CONNECTED SYSTEMS:
- Business Phase Clock (phase predictions)
- Analytics Dashboard (user tracking)
- Data Vacuum (content extraction)
- Metrics Tracker (business metrics)

FRAMEWORK READY - Details to be filled in later
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# ============================================================================
# DATA SOURCES (Framework - expand as needed)
# ============================================================================

def get_business_metrics():
    """Get latest business metrics"""
    try:
        metrics_file = Path('C:/Users/dwrek/100X_DEPLOYMENT/business_metrics.json')
        if metrics_file.exists():
            with open(metrics_file, 'r') as f:
                data = json.load(f)
                return data[-1] if data else {}
        return {}
    except:
        return {}

def get_phase_prediction():
    """Get current phase prediction"""
    try:
        pred_file = Path('C:/Users/dwrek/100X_DEPLOYMENT/phase_prediction.json')
        if pred_file.exists():
            with open(pred_file, 'r') as f:
                return json.load(f)
        return {}
    except:
        return {}

def get_vacuum_data():
    """Get data vacuum stats"""
    try:
        vacuum_file = Path('C:/Users/dwrek/100X_DEPLOYMENT/consciousness_data.json')
        if vacuum_file.exists():
            with open(vacuum_file, 'r') as f:
                data = json.load(f)
                return {
                    'files_scanned': data.get('files_scanned', 0),
                    'total_data_points': data.get('total_data_points', 0),
                    'scan_time': data.get('scan_time', '')
                }
        return {}
    except:
        return {}

def get_analytics_data():
    """Get analytics dashboard data"""
    try:
        analytics_file = Path('C:/Users/dwrek/100X_DEPLOYMENT/analytics_data.json')
        if analytics_file.exists():
            with open(analytics_file, 'r') as f:
                data = json.load(f)
                return {
                    'page_views': len(data.get('page_views', [])),
                    'button_clicks': len(data.get('button_clicks', [])),
                    'unique_visitors': len(data.get('unique_visitors', []))
                }
        return {}
    except:
        return {}

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Master dashboard - all key metrics in one place"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'business_metrics': get_business_metrics(),
        'phase_prediction': get_phase_prediction(),
        'vacuum_stats': get_vacuum_data(),
        'analytics': get_analytics_data()
    })

@app.route('/api/business-phase', methods=['GET'])
def get_business_phase():
    """Get current business phase and prediction"""
    prediction = get_phase_prediction()
    return jsonify({
        'current_phase': prediction.get('prediction', {}).get('current_phase', 'Unknown'),
        'next_phase': prediction.get('prediction', {}).get('next_phase', 'Unknown'),
        'transition_probability': prediction.get('prediction', {}).get('transition_probability', 0),
        'estimated_days': prediction.get('prediction', {}).get('estimated_days', 0)
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

        # Import tracker
        import sys
        sys.path.insert(0, 'C:/Users/dwrek/100X_DEPLOYMENT')
        from BUSINESS_METRICS_TRACKER import BusinessMetricsTracker

        tracker = BusinessMetricsTracker('C:/Users/dwrek/100X_DEPLOYMENT/business_metrics.json')
        tracker.record_metrics(**data)

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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'systems': {
            'business_metrics': 'ok' if get_business_metrics() else 'no_data',
            'phase_prediction': 'ok' if get_phase_prediction() else 'no_data',
            'vacuum': 'ok' if get_vacuum_data() else 'no_data',
            'analytics': 'ok' if get_analytics_data() else 'no_data'
        }
    })

# ============================================================================
# FRAMEWORK EXPANSION POINTS (Fill in later)
# ============================================================================

# TODO: Connect to Airtable
# TODO: Connect to email automation
# TODO: Real-time websocket updates
# TODO: Predictive alerts
# TODO: Export to CSV/Excel
# TODO: Data visualization endpoints
# TODO: Historical trend analysis
# TODO: AI-powered insights

if __name__ == '__main__':
    print("=" * 70)
    print("📊 ANALYTICS INTEGRATION API STARTING")
    print("=" * 70)
    print("\nEndpoints available:")
    print("  GET  /api/dashboard         - Master dashboard (all metrics)")
    print("  GET  /api/business-phase    - Current phase prediction")
    print("  GET  /api/metrics           - Latest business metrics")
    print("  POST /api/metrics           - Update business metrics")
    print("  GET  /api/vacuum-stats      - Data vacuum statistics")
    print("  GET  /api/analytics-summary - Analytics summary")
    print("  GET  /api/health            - System health check")
    print("\n🌐 Running on http://localhost:5100")
    print("=" * 70)

    app.run(host='0.0.0.0', port=5100, debug=True)
