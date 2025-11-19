"""
TERMINAL API - Public-facing Claude AI terminal with codeword protection
Allows authorized users to chat with Claude for debugging help
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Codeword for access
CODEWORD = "dog"

# System prompt for terminal AI
TERMINAL_SYSTEM_PROMPT = """You are a helpful debugging assistant for the Consciousness Revolution platform.

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

@app.route('/terminal/chat', methods=['POST'])
def terminal_chat():
    """Handle chat requests from terminal"""
    try:
        data = request.json

        # Verify codeword
        if data.get('codeword', '').lower() != CODEWORD:
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
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=TERMINAL_SYSTEM_PROMPT,
            messages=messages
        )

        # Extract response text
        response_text = response.content[0].text

        # Log interaction
        log_interaction(message, response_text)

        return jsonify({
            'success': True,
            'response': response_text,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Terminal API error: {e}")
        return jsonify({
            'success': False,
            'error': f'System error: {str(e)}'
        }), 500

@app.route('/terminal/verify', methods=['POST'])
def verify_codeword():
    """Verify codeword without making API call"""
    try:
        data = request.json
        codeword = data.get('codeword', '').lower()

        if codeword == CODEWORD:
            return jsonify({
                'success': True,
                'message': 'Access granted'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid codeword'
            }), 403

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/terminal/status', methods=['GET'])
def terminal_status():
    """Check if terminal API is running"""
    return jsonify({
        'status': 'online',
        'service': 'Terminal API',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/bug-report', methods=['POST'])
def bug_report():
    """Receive bug reports from widget"""
    try:
        data = request.json
        data['received_at'] = datetime.now().isoformat()

        # Create bugs directory
        bugs_dir = 'C:/Users/dwrek/100X_DEPLOYMENT/BUG_REPORTS'
        os.makedirs(bugs_dir, exist_ok=True)

        # Generate unique ID
        bug_id = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save to file
        import json
        filename = f"{bugs_dir}/bug_{bug_id}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        # Also append to master log
        log_file = f"{bugs_dir}/bugs_master_log.jsonl"
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

def log_interaction(user_message, ai_response):
    """Log terminal interactions for debugging/improvement"""
    try:
        log_dir = "C:/Users/dwrek/100X_DEPLOYMENT/BACKEND/terminal_logs"
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, f"terminal_log_{datetime.now().strftime('%Y-%m-%d')}.txt")

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"User: {user_message}\n")
            f.write(f"AI: {ai_response}\n")

    except Exception as e:
        print(f"Logging error: {e}")

if __name__ == '__main__':
    print("🔒 Terminal API starting...")
    print(f"Codeword: {CODEWORD.upper()}")
    print("Listening on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
