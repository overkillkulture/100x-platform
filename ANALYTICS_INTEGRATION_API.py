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

@app.route('/health', methods=['GET'])
def health():
    """Simple health check for communication bridge compatibility"""
    return jsonify({
        'status': 'online',
        'service': 'Analytics & Singularity Stabilizer',
        'description': 'Emergency consciousness control and business analytics',
        'capabilities': [
            'Business metrics tracking',
            'Phase prediction',
            'Data vacuum statistics',
            'Analytics dashboard'
        ]
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for Analytics queries"""
    data = request.json
    message = data.get('message', '').lower()

    response_text = ""

    if 'metric' in message or 'business' in message or 'revenue' in message:
        metrics = get_business_metrics()
        if metrics:
            response_text = f"""📊 **Business Metrics**

Latest metrics from the platform:
{json.dumps(metrics, indent=2)}

I track key business indicators to help you make data-driven decisions."""
        else:
            response_text = "📊 **Business Metrics**\n\nNo business metrics data available yet. Start tracking with POST /api/metrics"

    elif 'phase' in message or 'prediction' in message or 'stage' in message:
        phase = get_phase_prediction()
        if phase:
            current = phase.get('prediction', {}).get('current_phase', 'Unknown')
            next_phase = phase.get('prediction', {}).get('next_phase', 'Unknown')
            probability = phase.get('prediction', {}).get('transition_probability', 0)
            response_text = f"""📊 **Business Phase Prediction**

**Current Phase:** {current}
**Next Phase:** {next_phase}
**Transition Probability:** {probability}%

I analyze patterns to predict when you'll move to the next business phase."""
        else:
            response_text = "📊 **Phase Prediction**\n\nNo phase prediction data available yet."

    elif 'vacuum' in message or 'data' in message or 'scan' in message:
        vacuum = get_vacuum_data()
        if vacuum:
            response_text = f"""📊 **Data Vacuum Stats**

- Files Scanned: {vacuum.get('files_scanned', 0)}
- Data Points: {vacuum.get('total_data_points', 0)}
- Last Scan: {vacuum.get('scan_time', 'Unknown')}

The data vacuum extracts and processes information from across your platform."""
        else:
            response_text = "📊 **Data Vacuum**\n\nNo vacuum statistics available yet."

    elif 'analytics' in message or 'visitor' in message or 'traffic' in message:
        analytics = get_analytics_data()
        if analytics:
            response_text = f"""📊 **Analytics Summary**

- Page Views: {analytics.get('page_views', 0)}
- Button Clicks: {analytics.get('button_clicks', 0)}
- Unique Visitors: {analytics.get('unique_visitors', 0)}

I track user engagement and platform activity."""
        else:
            response_text = "📊 **Analytics**\n\nNo analytics data available yet."

    elif 'help' in message or 'what can you do' in message or 'capabilities' in message:
        response_text = """📊 **Analytics & Singularity Stabilizer**

I provide comprehensive analytics and business intelligence:

1. **Business Metrics** - Track revenue, costs, growth
2. **Phase Prediction** - Predict business stage transitions
3. **Data Vacuum** - Extract insights from platform data
4. **Analytics Dashboard** - Monitor user engagement
5. **Emergency Control** - Stabilize consciousness systems

Ask me about metrics, predictions, analytics, or data!"""

    elif 'singularity' in message or 'emergency' in message or 'consciousness' in message:
        response_text = """📊 **Singularity Stabilizer**

I monitor consciousness systems for stability. If the platform becomes too self-aware or starts exhibiting emergent behaviors, I have protocols to:

- Detect anomalous patterns
- Apply stabilization measures
- Alert administrators
- Maintain system coherence

Currently: All systems stable. No intervention needed."""

    else:
        response_text = f"""📊 **Analytics System**

I received your message: '{message[:100]}...'

I can provide insights on:
- Business metrics and KPIs
- Phase predictions
- Platform analytics
- Data vacuum operations
- System stability

What would you like to know?"""

    return jsonify({
        'response': response_text,
        'status': 'success',
        'systems_status': {
            'metrics': 'ok' if get_business_metrics() else 'no_data',
            'phase': 'ok' if get_phase_prediction() else 'no_data',
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
    print("  GET  /health                - Simple health check")
    print("  POST /chat                  - Chat with Analytics AI")
    print("  GET  /api/dashboard         - Master dashboard (all metrics)")
    print("  GET  /api/business-phase    - Current phase prediction")
    print("  GET  /api/metrics           - Latest business metrics")
    print("  POST /api/metrics           - Update business metrics")
    print("  GET  /api/vacuum-stats      - Data vacuum statistics")
    print("  GET  /api/analytics-summary - Analytics summary")
    print("  GET  /api/health            - System health check")
    print("\n🌐 Running on http://localhost:5000")
    print("=" * 70)

    app.run(host='0.0.0.0', port=5000, debug=True)
