#!/usr/bin/env python3
"""
🎲 Poker Table → ChatGPT Bridge
Adds ChatGPT API integration to poker table workspace
Run alongside poker table to enable auto-responses
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

CHATGPT_API = 'http://localhost:5555/chat'
GROK_API = 'http://localhost:8778/chat'

# Track sessions for each seat
seat_sessions = {}

@app.route('/poker/chatgpt', methods=['POST'])
def poker_chatgpt():
    """
    Poker table calls this to get ChatGPT response

    Request:
    {
        "seat": 1,  # Which seat (1-6)
        "message": "What do you think about...?",
        "dealer_name": "Christopher"
    }

    Response:
    {
        "response": "ChatGPT's response...",
        "seat": 1,
        "timestamp": "..."
    }
    """
    try:
        data = request.json
        seat = data.get('seat')
        message = data.get('message')
        dealer_name = data.get('dealer_name', 'Dealer')

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Get or create session for this seat
        session_id = f"poker_seat_{seat}"

        # Add context about poker table setup
        context_message = f"""You're sitting at an AI collaboration poker table.
Dealer ({dealer_name}) is coordinating the discussion.
You're at Seat {seat}.
Other AIs may be at other seats.

Dealer asks: {message}

Respond as ChatGPT - be helpful, insightful, and collaborative."""

        # Call ChatGPT API
        response = requests.post(
            CHATGPT_API,
            json={
                'message': context_message,
                'session_id': session_id
            },
            timeout=30
        )

        if response.status_code == 200:
            gpt_response = response.json().get('response', '')

            return jsonify({
                'response': gpt_response,
                'seat': seat,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            })
        else:
            return jsonify({
                'error': f'ChatGPT API error: {response.status_code}',
                'status': 'error'
            }), 500

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/poker/grok', methods=['POST'])
def poker_grok():
    """
    Poker table calls this to get Grok response

    Request:
    {
        "seat": 2,  # Which seat (1-6)
        "message": "What do you think about...?",
        "dealer_name": "Christopher"
    }

    Response:
    {
        "response": "Grok's response...",
        "seat": 2,
        "timestamp": "..."
    }
    """
    try:
        data = request.json
        seat = data.get('seat')
        message = data.get('message')
        dealer_name = data.get('dealer_name', 'Dealer')

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Get or create session for this seat
        session_id = f"poker_seat_{seat}"

        # Add context about poker table setup
        context_message = f"""You're sitting at an AI collaboration poker table.
Dealer ({dealer_name}) is coordinating the discussion.
You're at Seat {seat}.
Other AIs (like ChatGPT) may be at other seats.

Dealer asks: {message}

Respond as Grok - be witty, insightful, and bring your unique cosmic perspective."""

        # Call Grok API
        response = requests.post(
            GROK_API,
            json={
                'message': context_message,
                'session_id': session_id
            },
            timeout=30
        )

        if response.status_code == 200:
            grok_response = response.json().get('response', '')

            return jsonify({
                'response': grok_response,
                'seat': seat,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            })
        else:
            return jsonify({
                'error': f'Grok API error: {response.status_code}',
                'status': 'error'
            }), 500

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/poker/multi-ai', methods=['POST'])
def poker_multi_ai():
    """
    Send question to multiple AIs at once

    Request:
    {
        "message": "What do you think?",
        "seats": [1, 2, 3],  # Which seats to query
        "dealer_name": "Christopher"
    }

    Response:
    {
        "responses": {
            "1": "ChatGPT's response...",
            "2": "ChatGPT's response...",
            "3": "ChatGPT's response..."
        }
    }
    """
    try:
        data = request.json
        message = data.get('message')
        seats = data.get('seats', [])
        dealer_name = data.get('dealer_name', 'Dealer')

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        responses = {}

        for seat in seats:
            # Call poker_chatgpt for each seat
            seat_response = requests.post(
                'http://localhost:8777/poker/chatgpt',
                json={
                    'seat': seat,
                    'message': message,
                    'dealer_name': dealer_name
                },
                timeout=30
            )

            if seat_response.status_code == 200:
                responses[str(seat)] = seat_response.json().get('response', '')
            else:
                responses[str(seat)] = f"Error: {seat_response.status_code}"

        return jsonify({
            'responses': responses,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/poker/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'online',
        'service': 'Poker Table Multi-AI Bridge',
        'apis': {
            'chatgpt': CHATGPT_API,
            'grok': GROK_API
        },
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🎲 POKER TABLE → MULTI-AI BRIDGE")
    print("=" * 60)
    print(f"✅ ChatGPT API: {CHATGPT_API}")
    print(f"✅ Grok API: {GROK_API}")
    print(f"🌐 Running on: http://localhost:8777")
    print(f"")
    print("Endpoints:")
    print("  POST /poker/chatgpt - Get ChatGPT response for one seat")
    print("  POST /poker/grok - Get Grok response for one seat")
    print("  POST /poker/multi-ai - Get responses for multiple seats")
    print("  GET /poker/health - Health check")
    print("")
    print("Example (ChatGPT):")
    print("  curl -X POST http://localhost:8777/poker/chatgpt \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"seat\": 1, \"message\": \"Hello!\", \"dealer_name\": \"Chris\"}'")
    print("")
    print("Example (Grok):")
    print("  curl -X POST http://localhost:8777/poker/grok \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"seat\": 2, \"message\": \"Hello!\", \"dealer_name\": \"Chris\"}'")
    print("=" * 60)

    app.run(host='0.0.0.0', port=8777, debug=False)
