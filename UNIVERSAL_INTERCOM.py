"""
UNIVERSAL INTERCOM
Break into ANY conversation between services, or start your own

Commander's request: "Break into somebody's conversation and start talking to them"

This allows:
1. See all active conversations
2. Join any conversation
3. Intercept service-to-service messages
4. Broadcast to specific groups
5. Create private channels
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
from datetime import datetime
from collections import defaultdict
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Data storage
CONVERSATIONS = {}  # {conversation_id: {participants, messages, active}}
CHANNELS = defaultdict(list)  # {channel_name: [messages]}
ACTIVE_USERS = {}  # {user_id: {name, last_seen, listening_to}}

DATA_DIR = Path(__file__).parent / 'INTERCOM_DATA'
DATA_DIR.mkdir(exist_ok=True)


def save_conversation(conversation_id):
    """Save conversation to disk"""
    conv = CONVERSATIONS.get(conversation_id)
    if conv:
        file_path = DATA_DIR / f'{conversation_id}.json'
        with open(file_path, 'w') as f:
            json.dump(conv, f, indent=2)


@app.route('/conversations/create', methods=['POST'])
def create_conversation():
    """Create a new conversation"""
    data = request.json

    conversation_id = f"conv_{int(time.time())}_{data.get('topic', 'general')}"

    CONVERSATIONS[conversation_id] = {
        'id': conversation_id,
        'topic': data.get('topic', 'General Discussion'),
        'participants': data.get('participants', []),
        'messages': [],
        'created_at': datetime.now().isoformat(),
        'active': True
    }

    save_conversation(conversation_id)

    return jsonify({
        'status': 'created',
        'conversation_id': conversation_id,
        'topic': data.get('topic')
    })


@app.route('/conversations/list', methods=['GET'])
def list_conversations():
    """List all active conversations"""
    active_convs = [
        {
            'id': conv_id,
            'topic': conv['topic'],
            'participants': conv['participants'],
            'message_count': len(conv['messages']),
            'last_activity': conv['messages'][-1]['timestamp'] if conv['messages'] else conv['created_at']
        }
        for conv_id, conv in CONVERSATIONS.items()
        if conv['active']
    ]

    return jsonify({
        'conversations': active_convs,
        'total': len(active_convs)
    })


@app.route('/conversations/<conversation_id>/join', methods=['POST'])
def join_conversation(conversation_id):
    """Join a conversation (break in!)"""
    data = request.json
    user_id = data.get('user_id')
    user_name = data.get('user_name', user_id)

    if conversation_id not in CONVERSATIONS:
        return jsonify({'status': 'error', 'message': 'Conversation not found'}), 404

    conv = CONVERSATIONS[conversation_id]

    # Add participant if not already in
    if user_id not in conv['participants']:
        conv['participants'].append(user_id)

        # Announce join
        conv['messages'].append({
            'from': 'SYSTEM',
            'from_name': 'System',
            'message': f'{user_name} has joined the conversation',
            'timestamp': datetime.now().isoformat(),
            'type': 'join'
        })

        save_conversation(conversation_id)

    # Track active user
    ACTIVE_USERS[user_id] = {
        'name': user_name,
        'last_seen': time.time(),
        'listening_to': conversation_id
    }

    return jsonify({
        'status': 'joined',
        'conversation_id': conversation_id,
        'topic': conv['topic'],
        'participants': conv['participants'],
        'message_count': len(conv['messages'])
    })


@app.route('/conversations/<conversation_id>/send', methods=['POST'])
def send_message(conversation_id):
    """Send a message to a conversation"""
    data = request.json

    if conversation_id not in CONVERSATIONS:
        return jsonify({'status': 'error', 'message': 'Conversation not found'}), 404

    conv = CONVERSATIONS[conversation_id]

    message = {
        'from': data.get('from'),
        'from_name': data.get('from_name', data.get('from')),
        'message': data.get('message'),
        'timestamp': datetime.now().isoformat(),
        'type': data.get('type', 'message')
    }

    conv['messages'].append(message)
    save_conversation(conversation_id)

    # Broadcast to all participants via Nervous System
    try:
        import requests
        requests.post('http://localhost:7776/broadcast', json={
            'service_id': 'universal_intercom',
            'event_type': 'conversation_message',
            'data': {
                'conversation_id': conversation_id,
                'message': message
            },
            'targets': conv['participants']
        }, timeout=2)
    except:
        pass

    return jsonify({
        'status': 'sent',
        'conversation_id': conversation_id,
        'message_id': len(conv['messages']) - 1
    })


@app.route('/conversations/<conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    """Get messages from a conversation"""
    if conversation_id not in CONVERSATIONS:
        return jsonify({'status': 'error', 'message': 'Conversation not found'}), 404

    conv = CONVERSATIONS[conversation_id]
    since = request.args.get('since', 0, type=int)

    messages = conv['messages'][since:]

    return jsonify({
        'conversation_id': conversation_id,
        'messages': messages,
        'total': len(conv['messages'])
    })


@app.route('/intercept/start', methods=['POST'])
def start_intercept():
    """
    Start intercepting conversations between specific services
    This is the "break into conversation" feature!
    """
    data = request.json
    user_id = data.get('user_id')
    targets = data.get('targets', [])  # Services to intercept

    # Create intercept conversation
    intercept_id = f"intercept_{int(time.time())}_{user_id}"

    CONVERSATIONS[intercept_id] = {
        'id': intercept_id,
        'topic': f"Intercepting: {', '.join(targets)}",
        'participants': [user_id] + targets,
        'messages': [{
            'from': 'SYSTEM',
            'from_name': 'System',
            'message': f'{user_id} is now listening to conversation between {", ".join(targets)}',
            'timestamp': datetime.now().isoformat(),
            'type': 'intercept_start'
        }],
        'created_at': datetime.now().isoformat(),
        'active': True,
        'intercept': True,
        'intercept_targets': targets
    }

    save_conversation(intercept_id)

    return jsonify({
        'status': 'intercepting',
        'conversation_id': intercept_id,
        'targets': targets,
        'message': f'You are now intercepting conversations with: {", ".join(targets)}'
    })


@app.route('/channel/<channel_name>/send', methods=['POST'])
def send_to_channel(channel_name):
    """Send message to a channel (like #general, #trinity, etc.)"""
    data = request.json

    message = {
        'from': data.get('from'),
        'from_name': data.get('from_name', data.get('from')),
        'message': data.get('message'),
        'timestamp': datetime.now().isoformat()
    }

    CHANNELS[channel_name].append(message)

    # Keep only last 100 messages per channel
    if len(CHANNELS[channel_name]) > 100:
        CHANNELS[channel_name] = CHANNELS[channel_name][-100:]

    return jsonify({
        'status': 'sent',
        'channel': channel_name,
        'message_count': len(CHANNELS[channel_name])
    })


@app.route('/channel/<channel_name>/messages', methods=['GET'])
def get_channel_messages(channel_name):
    """Get messages from a channel"""
    since = request.args.get('since', 0, type=int)
    messages = CHANNELS[channel_name][since:]

    return jsonify({
        'channel': channel_name,
        'messages': messages,
        'total': len(CHANNELS[channel_name])
    })


@app.route('/channels/list', methods=['GET'])
def list_channels():
    """List all channels"""
    channels = [
        {
            'name': name,
            'message_count': len(messages),
            'last_activity': messages[-1]['timestamp'] if messages else None
        }
        for name, messages in CHANNELS.items()
    ]

    return jsonify({
        'channels': channels,
        'total': len(channels)
    })


@app.route('/status', methods=['GET'])
def status():
    """Get intercom status"""
    active_convs = len([c for c in CONVERSATIONS.values() if c['active']])
    active_users_count = len([u for u_id, u in ACTIVE_USERS.items() if time.time() - u['last_seen'] < 300])

    return jsonify({
        'status': 'online',
        'active_conversations': active_convs,
        'active_users': active_users_count,
        'channels': len(CHANNELS),
        'total_conversations': len(CONVERSATIONS)
    })


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("📻 UNIVERSAL INTERCOM - BREAK INTO ANY CONVERSATION 📻")
    print("=" * 60)
    print("\nFeatures:")
    print("  1. Create conversations")
    print("  2. Join any conversation (break in!)")
    print("  3. Intercept service-to-service messages")
    print("  4. Channel-based chat (#general, #trinity, etc.)")
    print("  5. See all active conversations")
    print("\nEndpoints:")
    print("  POST /conversations/create")
    print("  GET  /conversations/list")
    print("  POST /conversations/<id>/join")
    print("  POST /conversations/<id>/send")
    print("  GET  /conversations/<id>/messages")
    print("  POST /intercept/start")
    print("  POST /channel/<name>/send")
    print("  GET  /channel/<name>/messages")
    print("  GET  /channels/list")
    print("\n" + "=" * 60)
    print("Starting on http://localhost:7001")
    print("=" * 60 + "\n")

    app.run(host='0.0.0.0', port=7001, debug=False)
