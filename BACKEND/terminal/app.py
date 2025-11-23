#!/usr/bin/env python3
"""
💻 INTELLIGENT TERMINAL BACKEND API
Provides Claude AI-powered debugging assistance through terminal interface
Includes codeword protection and conversation history
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from pathlib import Path
from datetime import datetime
import anthropic

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
CODEWORD = os.getenv('TERMINAL_CODEWORD', 'dog')
DATA_DIR = Path(__file__).parent / 'data'
LOGS_DIR = DATA_DIR / 'logs'
BUGS_DIR = DATA_DIR / 'bugs'

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
BUGS_DIR.mkdir(exist_ok=True)

# System prompt for terminal AI
TERMINAL_SYSTEM_PROMPT = """You are a helpful debugging assistant for the 100X Consciousness Revolution platform.

Users accessing you through a terminal interface are authorized employees or helpers trying to:
- Debug website issues
- Get help with platform navigation
- Report bugs or problems
- Ask technical questions

Your responses should be:
- Concise and terminal-friendly (short paragraphs)
- Technical but friendly
- Include actionable debugging steps when relevant
- Reassuring - you're here to help solve problems

Format responses for terminal display (avoid markdown, use plain text).
Keep responses under 200 words unless explaining complex technical issues.
"""


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'service': 'intelligent-terminal',
        'timestamp': datetime.utcnow().isoformat(),
        'anthropic_configured': bool(ANTHROPIC_API_KEY),
        'codeword_enabled': True
    })


@app.route('/terminal/status', methods=['GET'])
def terminal_status():
    """Check if terminal API is running"""
    return jsonify({
        'status': 'online',
        'service': 'Terminal API',
        'version': '1.0',
        'timestamp': datetime.utcnow().isoformat(),
        'codeword_required': True
    })


@app.route('/terminal/verify', methods=['POST'])
def verify_codeword():
    """Verify codeword without making API call"""
    try:
        data = request.json
        codeword = data.get('codeword', '').lower()

        if codeword == CODEWORD.lower():
            return jsonify({
                'success': True,
                'message': 'Access granted - terminal unlocked'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid codeword - access denied'
            }), 403

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/terminal/chat', methods=['POST'])
def terminal_chat():
    """Handle chat requests from terminal"""
    try:
        data = request.json

        # Verify codeword
        if data.get('codeword', '').lower() != CODEWORD.lower():
            return jsonify({
                'success': False,
                'error': 'Invalid codeword - access denied'
            }), 403

        # Get user message
        message = data.get('message', '').strip()
        if not message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400

        # Check if Anthropic API is configured
        if not ANTHROPIC_API_KEY:
            # Fallback response when API key not configured
            response_text = f"""Terminal AI (Demo Mode):

Your query: "{message}"

This is a demo response. To enable AI-powered debugging assistance:
1. Get an API key from https://console.anthropic.com/
2. Set ANTHROPIC_API_KEY in your .env file
3. Restart the terminal backend

Demo capabilities active. Real AI requires API key configuration."""

            log_interaction(message, response_text, demo_mode=True)

            return jsonify({
                'success': True,
                'response': response_text,
                'demo_mode': True,
                'timestamp': datetime.utcnow().isoformat()
            })

        # Get conversation history (optional)
        history = data.get('history', [])

        # Build messages for Claude
        messages = []
        for msg in history[-10:]:  # Keep last 10 messages for context
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })

        # Call Claude API
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=TERMINAL_SYSTEM_PROMPT,
            messages=messages
        )

        # Extract response text
        response_text = response.content[0].text

        # Log interaction
        log_interaction(message, response_text, demo_mode=False)

        return jsonify({
            'success': True,
            'response': response_text,
            'demo_mode': False,
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        print(f"Terminal API error: {e}")
        return jsonify({
            'success': False,
            'error': f'System error: {str(e)}'
        }), 500


@app.route('/api/bug-report', methods=['POST'])
def bug_report():
    """Receive bug reports from widget"""
    try:
        data = request.json
        data['received_at'] = datetime.utcnow().isoformat()

        # Generate unique ID
        bug_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S')

        # Save to individual file
        filename = BUGS_DIR / f"bug_{bug_id}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        # Also append to master log
        log_file = BUGS_DIR / "bugs_master_log.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(data) + '\n')

        # Print to console
        print("\n" + "="*80)
        print(f"🐛 NEW BUG REPORT - {bug_id}")
        print("="*80)
        print(f"Page: {data.get('page', 'Unknown')}")
        print(f"Description: {data.get('description', 'No description')}")
        print(f"Email: {data.get('email', 'Not provided')}")
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


def log_interaction(user_message, ai_response, demo_mode=False):
    """Log terminal interactions for debugging/improvement"""
    try:
        log_file = LOGS_DIR / f"terminal_log_{datetime.utcnow().strftime('%Y-%m-%d')}.txt"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Timestamp: {datetime.utcnow().isoformat()}\n")
            f.write(f"Mode: {'DEMO' if demo_mode else 'AI'}\n")
            f.write(f"User: {user_message}\n")
            f.write(f"AI: {ai_response}\n")

    except Exception as e:
        print(f"Logging error: {e}")


if __name__ == '__main__':
    print("=" * 70)
    print("💻 INTELLIGENT TERMINAL BACKEND API")
    print("=" * 70)
    print(f"\n🔒 Codeword Protection: ENABLED")
    print(f"📝 Codeword: {CODEWORD.upper()}")
    print(f"🤖 Anthropic API: {'✅ Configured' if ANTHROPIC_API_KEY else '⚠️  Not configured (demo mode)'}")
    print(f"\n📡 Endpoints Available:")
    print(f"  GET  /api/health           - Health check")
    print(f"  GET  /terminal/status      - Terminal status")
    print(f"  POST /terminal/verify      - Verify codeword")
    print(f"  POST /terminal/chat        - Chat with AI assistant")
    print(f"  POST /api/bug-report       - Submit bug report")
    print(f"\n🌐 Running on: http://localhost:5002")
    print(f"📁 Data Directory: {DATA_DIR.absolute()}")
    print(f"📁 Logs Directory: {LOGS_DIR.absolute()}")
    print(f"📁 Bugs Directory: {BUGS_DIR.absolute()}")
    print("=" * 70)
    print()

    app.run(host='0.0.0.0', port=5002, debug=True)
