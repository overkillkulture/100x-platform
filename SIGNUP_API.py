#!/usr/bin/env python3
"""
SIGNUP NOTIFICATION API
Simple Flask server that receives signup notifications and sends emails
Run this in background: python SIGNUP_API.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from SIGNUP_NOTIFIER import SignupNotifier
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Allow requests from your website

# Initialize notifier
notifier = SignupNotifier()

# Log file for signups (backup in case email fails)
SIGNUP_LOG = "C:/Users/dwrek/100X_DEPLOYMENT/signups_log.json"

def log_signup(data):
    """Save signup to file as backup"""
    try:
        if os.path.exists(SIGNUP_LOG):
            with open(SIGNUP_LOG, 'r') as f:
                signups = json.load(f)
        else:
            signups = []

        signups.append(data)

        with open(SIGNUP_LOG, 'w') as f:
            json.dump(signups, f, indent=2)

        print(f"✅ Logged signup to {SIGNUP_LOG}")
    except Exception as e:
        print(f"⚠️ Failed to log signup: {e}")

@app.route('/api/notify-signup', methods=['POST'])
def notify_signup():
    """Endpoint that receives signup notifications"""
    try:
        data = request.json

        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n🚀 NEW SIGNUP DETECTED:")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Phone: {phone}")
        print(f"   Time: {timestamp}\n")

        # Log to file first (always works)
        signup_data = {
            'username': username,
            'email': email,
            'phone': phone,
            'timestamp': timestamp
        }
        log_signup(signup_data)

        # Try to send email notification
        email_sent = notifier.send_signup_notification(
            username=username,
            email=email,
            phone=phone,
            timestamp=timestamp
        )

        return jsonify({
            'success': True,
            'email_sent': email_sent,
            'message': f'Signup logged for {username}'
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/get-signups', methods=['GET'])
def get_signups():
    """Get all signups from log file"""
    try:
        if os.path.exists(SIGNUP_LOG):
            with open(SIGNUP_LOG, 'r') as f:
                signups = json.load(f)
            return jsonify({
                'success': True,
                'signups': signups,
                'total': len(signups)
            })
        else:
            return jsonify({
                'success': True,
                'signups': [],
                'total': 0
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'running',
        'service': 'Signup Notification API',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🚀 SIGNUP NOTIFICATION API STARTING")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    print("📡 Listening on: http://localhost:5555")
    print("📧 Email notifications: ENABLED")
    print("💾 Backup logging: ENABLED")
    print("")
    print("🔗 Test with:")
    print("   curl http://localhost:5555/api/health")
    print("")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")

    # Run server
    app.run(host='0.0.0.0', port=5555, debug=False)
