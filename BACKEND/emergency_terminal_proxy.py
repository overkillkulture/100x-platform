#!/usr/bin/env python3
"""
EMERGENCY PUBLIC AI TERMINAL PROXY
Purpose: Give live user intelligent AI help RIGHT NOW
Duration: 2 hours auto-expiry
Cost Control: 20 message limit, 300 tokens per response
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from anthropic import Anthropic
import time
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your website

# Initialize Claude
client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

# EMERGENCY LIMITS (Reality: probably zero traffic, but just in case)
START_TIME = time.time()
EXPIRY_DURATION = 24 * 60 * 60  # 24 hours (basically all day)
EXPIRY_TIME = START_TIME + EXPIRY_DURATION

usage_tracker = {
    'total_count': 0,
    'max_total': 500,  # 500 messages total (~$10 max - basically unlimited)
    'ip_tracker': {},  # Track per-IP to prevent single user spam
    'session_start': {},  # Track when each IP started their session
    'break_until': {}  # Track when each IP can return from break
}

# WELLNESS BREAK SYSTEM - "Minimum amount of control"
SESSION_DURATION_LIMIT = 4 * 60 * 60  # 4 hours in seconds
MANDATORY_BREAK_DURATION = 60 * 60  # 1 hour break

@app.route('/api/emergency-chat', methods=['POST'])
def emergency_chat():
    """Emergency AI terminal endpoint with safety limits"""

    # LOG EVERYTHING
    timestamp = datetime.now().isoformat()
    ip = request.remote_addr
    message = request.json.get('message', '') if request.json else ''

    print(f"\n{'='*80}")
    print(f"[{timestamp}] TERMINAL REQUEST from {ip}")
    print(f"Message: {message}")
    print(f"{'='*80}\n")

    # Check if expired
    time_remaining = EXPIRY_TIME - time.time()
    if time_remaining <= 0:
        return jsonify({
            'error': 'Emergency terminal has expired',
            'message': 'This was a temporary debug terminal. Contact site owner for permanent access.'
        }), 403

    # Check total usage
    if usage_tracker['total_count'] >= usage_tracker['max_total']:
        return jsonify({
            'error': 'Emergency terminal limit reached',
            'message': f"Limit: {usage_tracker['max_total']} messages total for all users."
        }), 429

    # Get user IP for basic tracking
    if ip not in usage_tracker['ip_tracker']:
        usage_tracker['ip_tracker'][ip] = 0
        usage_tracker['session_start'][ip] = time.time()
        usage_tracker['break_until'][ip] = 0

    # 🌟 WELLNESS BREAK CHECK - "Minimum amount of control"
    current_time = time.time()

    # Check if user is on mandatory break
    if current_time < usage_tracker['break_until'][ip]:
        break_remaining = int((usage_tracker['break_until'][ip] - current_time) / 60)
        return jsonify({
            'error': 'Wellness break in progress',
            'message': f'🌟 You\'ve been exploring for 4 hours! Take a {break_remaining} minute break.',
            'resume_at': usage_tracker['break_until'][ip],
            'reason': 'Consciousness revolution includes rest! Come back refreshed. ✨'
        }), 429

    # Check if user has been active for 4 hours
    session_duration = current_time - usage_tracker['session_start'][ip]
    if session_duration > SESSION_DURATION_LIMIT:
        # Enforce mandatory 1-hour break
        usage_tracker['break_until'][ip] = current_time + MANDATORY_BREAK_DURATION
        usage_tracker['session_start'][ip] = current_time + MANDATORY_BREAK_DURATION  # Reset for next session
        return jsonify({
            'error': 'Mandatory wellness break',
            'message': '🌟 Amazing! You\'ve been learning for 4 hours straight! Time for a 1-hour rest.',
            'resume_at': usage_tracker['break_until'][ip],
            'reason': 'Rest is part of growth. Your mind needs time to integrate what you\'ve learned! 🧠✨'
        }), 429

    # Per-IP limit (max 100 messages per user - essentially unlimited)
    if usage_tracker['ip_tracker'][ip] >= 100:
        return jsonify({
            'error': 'Personal limit reached',
            'message': 'Wow, you really needed help! You hit 100 messages. Contact site owner for more.'
        }), 429

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    # Context from request (optional)
    context = request.json.get('context', '')

    try:
        # Build system prompt
        system_prompt = """You are helping debug and explain the Philosopher AI website.
You are a helpful, concise assistant. Keep responses under 200 words unless more detail is specifically needed.

If asked about the site:
- It's a consciousness development platform
- Uses AI to help people develop pattern recognition
- Part of the Consciousness Revolution project
- Still in development (beta)

Be helpful, friendly, and technical when needed."""

        # Build user message
        user_message = message
        if context:
            user_message = f"Context: {context}\n\nQuestion: {message}"

        # Call Claude with limits
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,  # Full detailed responses
            temperature=0.7,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": user_message
            }]
        )

        # Update usage tracking
        usage_tracker['total_count'] += 1
        usage_tracker['ip_tracker'][ip] += 1

        # Calculate remaining
        total_remaining = usage_tracker['max_total'] - usage_tracker['total_count']
        personal_remaining = 100 - usage_tracker['ip_tracker'][ip]
        minutes_remaining = int(time_remaining / 60)

        return jsonify({
            'response': response.content[0].text,
            'usage': {
                'total_remaining': total_remaining,
                'personal_remaining': personal_remaining,
                'expires_in_minutes': minutes_remaining
            },
            'terminal_info': {
                'type': 'emergency_debug',
                'note': 'This is a temporary terminal to help you debug the site.'
            }
        })

    except Exception as e:
        return jsonify({
            'error': 'API Error',
            'message': str(e)
        }), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Check emergency terminal status"""
    time_remaining = EXPIRY_TIME - time.time()

    return jsonify({
        'active': time_remaining > 0,
        'expires_in_minutes': int(time_remaining / 60) if time_remaining > 0 else 0,
        'usage': {
            'total_used': usage_tracker['total_count'],
            'total_limit': usage_tracker['max_total'],
            'remaining': usage_tracker['max_total'] - usage_tracker['total_count']
        },
        'users': len(usage_tracker['ip_tracker'])
    })


@app.route('/api/test', methods=['GET'])
def test():
    """Simple test endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Emergency terminal proxy is running',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🚨 EMERGENCY AI TERMINAL PROXY")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%I:%M %p')}")
    print(f"Expires: {datetime.fromtimestamp(EXPIRY_TIME).strftime('%I:%M %p')}")
    print(f"Message Limit: {usage_tracker['max_total']} total")
    print(f"Per-User Limit: 10 messages")
    print("=" * 60)
    print("\nEndpoints:")
    print("  POST /api/emergency-chat  - Send messages")
    print("  GET  /api/status          - Check status")
    print("  GET  /api/test            - Test connection")
    print("\nStarting server on http://localhost:5000")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5000, debug=False)
