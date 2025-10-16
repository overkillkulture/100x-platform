#!/usr/bin/env python3
"""
SIMPLE BUG REPORT RECEIVER

Receives bug reports from the widget and logs them.
Can forward to Airtable, email, or just save to file.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Create bugs directory if it doesn't exist
BUGS_DIR = 'C:/Users/dwrek/100X_DEPLOYMENT/BUG_REPORTS'
os.makedirs(BUGS_DIR, exist_ok=True)

@app.route('/api/bug-report', methods=['POST'])
def bug_report():
    """Receive and log bug reports"""

    try:
        data = request.json

        # Add server timestamp
        data['received_at'] = datetime.now().isoformat()

        # Generate unique ID
        bug_id = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save to file
        filename = f"{BUGS_DIR}/bug_{bug_id}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        # Also append to master log
        log_file = f"{BUGS_DIR}/bugs_master_log.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(data) + '\n')

        # Print to console for immediate visibility
        print("\n" + "="*80)
        print(f"🐛 NEW BUG REPORT - {bug_id}")
        print("="*80)
        print(f"Page: {data.get('page', 'Unknown')}")
        print(f"Description: {data.get('description', 'No description')}")
        print(f"Email: {data.get('email', 'Not provided')}")
        print(f"Timestamp: {data.get('timestamp', 'Unknown')}")
        print("="*80 + "\n")

        return jsonify({
            'success': True,
            'bug_id': bug_id,
            'message': 'Bug report received. Thank you!'
        })

    except Exception as e:
        print(f"Error receiving bug report: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/bugs/list', methods=['GET'])
def list_bugs():
    """List all bug reports (for Commander to review)"""

    try:
        bugs = []
        for filename in sorted(os.listdir(BUGS_DIR)):
            if filename.startswith('bug_') and filename.endswith('.json'):
                filepath = os.path.join(BUGS_DIR, filename)
                with open(filepath, 'r') as f:
                    bug_data = json.load(f)
                    bugs.append({
                        'id': filename.replace('bug_', '').replace('.json', ''),
                        'page': bug_data.get('page', 'Unknown'),
                        'description': bug_data.get('description', '')[:100] + '...' if len(bug_data.get('description', '')) > 100 else bug_data.get('description', ''),
                        'timestamp': bug_data.get('timestamp', 'Unknown')
                    })

        return jsonify({
            'bugs': bugs,
            'total': len(bugs)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/bugs/<bug_id>', methods=['GET'])
def get_bug(bug_id):
    """Get full details of a specific bug"""

    try:
        filename = f"{BUGS_DIR}/bug_{bug_id}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return jsonify(json.load(f))
        else:
            return jsonify({'error': 'Bug not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🐛 BUG REPORT RECEIVER")
    print("=" * 60)
    print(f"Saving reports to: {BUGS_DIR}")
    print(f"Listening on: http://localhost:5001")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5001, debug=False)
