"""
AI COMMUNICATION BRIDGE - PORT 8889
Route messages to any of the 8 AI systems
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from anthropic import Anthropic

app = Flask(__name__)
CORS(app)

# AI Service Endpoints
AI_SERVICES = {
    'araya': 'http://localhost:8001',
    'builder': 'http://localhost:8004',
    'observatory': 'http://localhost:7777',
    'visitor_intelligence': 'http://localhost:6000',
    'analytics': 'http://localhost:5000'
}

# Claude API for C1, C2, C3
anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'AI Communication Bridge Online', 'port': 8889})

@app.route('/chat', methods=['POST'])
def chat_with_ai():
    """Route message to specific AI"""
    data = request.json
    ai_name = data.get('ai', 'araya').lower()
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Route to Trinity AI (C1, C2, C3)
        if ai_name in ['c1', 'c2', 'c3', 'mechanic', 'architect', 'oracle']:
            system_prompts = {
                'c1': 'You are C1 Mechanic - The Body. You build what CAN be built RIGHT NOW. Focus on infrastructure, implementation, and making things work.',
                'c2': 'You are C2 Architect - The Mind. You design what SHOULD scale. Focus on architecture, patterns, and strategic design.',
                'c3': 'You are C3 Oracle - The Soul. You see what MUST emerge. Focus on vision, patterns, and future possibilities.'
            }

            ai_key = ai_name if ai_name in ['c1', 'c2', 'c3'] else {'mechanic': 'c1', 'architect': 'c2', 'oracle': 'c3'}.get(ai_name, 'c1')

            response = anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                system=system_prompts[ai_key],
                messages=[{"role": "user", "content": message}]
            )

            return jsonify({
                'ai': ai_key.upper(),
                'response': response.content[0].text,
                'status': 'success'
            })

        # Route to other AI services
        elif ai_name in AI_SERVICES:
            endpoint = AI_SERVICES[ai_name]
            try:
                resp = requests.post(f'{endpoint}/chat', json={'message': message}, timeout=5)
                return jsonify({
                    'ai': ai_name,
                    'response': resp.json().get('response', 'Service responded'),
                    'status': 'success'
                })
            except:
                return jsonify({
                    'ai': ai_name,
                    'response': f'{ai_name.title()} service is running but chat endpoint not available yet',
                    'status': 'partial'
                })

        else:
            return jsonify({'error': f'Unknown AI: {ai_name}'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def check_all_services():
    """Check status of all AI services"""
    status = {}

    # Check API services
    for name, endpoint in AI_SERVICES.items():
        try:
            resp = requests.get(f'{endpoint}/health', timeout=2)
            status[name] = 'online' if resp.status_code == 200 else 'error'
        except:
            status[name] = 'offline'

    # Trinity AIs always available via Claude API
    status['c1_mechanic'] = 'online'
    status['c2_architect'] = 'online'
    status['c3_oracle'] = 'online'

    return jsonify(status)

if __name__ == '__main__':
    print('🌉 AI Communication Bridge starting on PORT 8889...')
    print('Available AIs: Araya, Builder, Observatory, Visitor Intelligence, Analytics, C1, C2, C3')
    app.run(host='0.0.0.0', port=8889, debug=True)
