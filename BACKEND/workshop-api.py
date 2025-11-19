"""
Builder Workshop API Bridge
Connects the workshop to OpenAI/Grok/DeepSeek APIs
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from browser

# Load all available API keys
load_dotenv('C:/Users/dwrek/.env.openai')
load_dotenv('C:/Users/dwrek/.env.grok')
load_dotenv('C:/Users/dwrek/.env.deepseek')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROK_API_KEY = os.getenv('GROK_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Send message to AI and get response"""
    try:
        data = request.json
        message = data.get('message', '')
        provider = data.get('provider', 'openai')  # openai, grok, or deepseek

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Route to appropriate API
        if provider == 'openai' and OPENAI_API_KEY:
            response = call_openai(message)
        elif provider == 'grok' and GROK_API_KEY:
            response = call_grok(message)
        elif provider == 'deepseek' and DEEPSEEK_API_KEY:
            response = call_deepseek(message)
        else:
            return jsonify({'error': f'Provider {provider} not available'}), 400

        return jsonify({
            'response': response,
            'provider': provider
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def call_openai(message):
    """Call OpenAI API"""
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'gpt-4',
        'messages': [
            {
                'role': 'system',
                'content': '''You are a helpful AI assistant in the 100X Builder Workshop.
                Help users build their ideas. Focus on: community features, Truth Coin crypto,
                news platform, and escaping the 9-5. Be encouraging and practical.'''
            },
            {
                'role': 'user',
                'content': message
            }
        ],
        'temperature': 0.7
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data,
        timeout=30
    )

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")

def call_grok(message):
    """Call Grok API (x.ai)"""
    headers = {
        'Authorization': f'Bearer {GROK_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'grok-beta',
        'messages': [
            {
                'role': 'system',
                'content': '''You are a helpful AI assistant in the 100X Builder Workshop.
                Help users build their ideas. Focus on: community features, Truth Coin crypto,
                news platform, and escaping the 9-5. Be encouraging and practical.'''
            },
            {
                'role': 'user',
                'content': message
            }
        ],
        'temperature': 0.7
    }

    response = requests.post(
        'https://api.x.ai/v1/chat/completions',
        headers=headers,
        json=data,
        timeout=30
    )

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Grok API error: {response.status_code} - {response.text}")

def call_deepseek(message):
    """Call DeepSeek API"""
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'deepseek-chat',
        'messages': [
            {
                'role': 'system',
                'content': '''You are a helpful AI assistant in the 100X Builder Workshop.
                Help users build their ideas. Focus on: community features, Truth Coin crypto,
                news platform, and escaping the 9-5. Be encouraging and practical.'''
            },
            {
                'role': 'user',
                'content': message
            }
        ],
        'temperature': 0.7
    }

    response = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers=headers,
        json=data,
        timeout=30
    )

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"DeepSeek API error: {response.status_code} - {response.text}")

@app.route('/api/health', methods=['GET'])
def health():
    """Check API health and available providers"""
    return jsonify({
        'status': 'healthy',
        'providers': {
            'openai': OPENAI_API_KEY is not None,
            'grok': GROK_API_KEY is not None,
            'deepseek': DEEPSEEK_API_KEY is not None
        }
    })

if __name__ == '__main__':
    print("🚀 Builder Workshop API Starting...")
    print(f"✅ OpenAI: {'Available' if OPENAI_API_KEY else 'Not configured'}")
    print(f"✅ Grok: {'Available' if GROK_API_KEY else 'Not configured'}")
    print(f"✅ DeepSeek: {'Available' if DEEPSEEK_API_KEY else 'Not configured'}")
    print("\n🌐 API running on http://localhost:5100")
    print("🔗 Workshop can now connect to real AI!\n")

    app.run(host='0.0.0.0', port=5100, debug=True)
