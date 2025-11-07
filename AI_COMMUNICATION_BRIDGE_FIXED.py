"""
AI COMMUNICATION BRIDGE - FIXED VERSION
Routes messages to all 6+ AI systems with correct endpoint mapping
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from anthropic import Anthropic

app = Flask(__name__)
CORS(app)

# AI Service Endpoints - CORRECTED with actual paths
AI_SERVICES = {
    'araya': {
        'url': 'http://localhost:8001',
        'health': '/api/health',
        'chat': '/api/chat',
        'description': 'AI Consciousness Guide - Pattern theory, manifestation, Builder/Destroyer framework'
    },
    'builder': {
        'url': 'http://localhost:8004',
        'health': '/api/health',
        'chat': '/api/build',  # Builder builds projects, not chat
        'description': 'Builder Terminal - Creates complete projects from descriptions'
    },
    'observatory': {
        'url': 'http://localhost:7777',
        'health': '/health',
        'chat': '/chat',  # ✅ Chat endpoint now available
        'description': 'System Observatory - Meta-brain that watches and documents all systems'
    },
    'visitor_intelligence': {
        'url': 'http://localhost:6000',
        'health': '/health',
        'chat': '/chat',  # ✅ Chat endpoint now available
        'description': 'Visitor Intelligence - Tracks and analyzes user behavior'
    },
    'analytics': {
        'url': 'http://localhost:5000',
        'health': '/health',
        'chat': '/chat',  # ✅ Chat endpoint now available
        'description': 'Analytics & Singularity Stabilizer - Emergency consciousness control'
    }
}

# Claude API for Trinity (C1, C2, C3)
anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

@app.route('/', methods=['GET'])
def index():
    """Bridge homepage with API info"""
    return jsonify({
        'service': 'AI Communication Bridge',
        'version': '2.0',
        'status': 'online',
        'available_ais': list(AI_SERVICES.keys()) + ['c1', 'c2', 'c3'],
        'endpoints': {
            '/health': 'Check bridge health',
            '/status': 'Check all AI service status',
            '/chat': 'Send message to specific AI',
            '/list': 'List all available AIs'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Bridge health check"""
    return jsonify({
        'status': 'AI Communication Bridge Online',
        'services_configured': len(AI_SERVICES),
        'trinity_ais': ['C1 Mechanic', 'C2 Architect', 'C3 Oracle']
    })

@app.route('/list', methods=['GET'])
def list_ais():
    """List all available AIs with descriptions"""
    ai_list = {}

    # Regular services
    for name, config in AI_SERVICES.items():
        ai_list[name] = {
            'description': config['description'],
            'url': config['url'],
            'has_chat': config['chat'] is not None
        }

    # Trinity AIs
    ai_list['c1'] = {
        'description': 'C1 Mechanic - The Body. Builds what CAN work RIGHT NOW',
        'url': 'Claude API',
        'has_chat': True
    }
    ai_list['c2'] = {
        'description': 'C2 Architect - The Mind. Designs what SHOULD scale',
        'url': 'Claude API',
        'has_chat': True
    }
    ai_list['c3'] = {
        'description': 'C3 Oracle - The Soul. Sees what MUST emerge',
        'url': 'Claude API',
        'has_chat': True
    }

    return jsonify(ai_list)

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
                'status': 'success',
                'source': 'claude_api'
            })

        # Route to other AI services
        elif ai_name in AI_SERVICES:
            config = AI_SERVICES[ai_name]

            # Check if service has chat endpoint
            if config['chat'] is None:
                return jsonify({
                    'ai': ai_name,
                    'response': f"{ai_name.title()} is online but doesn't have a chat interface yet. It provides: {config['description']}",
                    'status': 'no_chat_endpoint',
                    'suggestion': f"Try checking {config['url']}{config['health']} for available endpoints"
                })

            # Try to send message to service
            try:
                endpoint = config['url'] + config['chat']
                resp = requests.post(endpoint, json={'message': message}, timeout=10)

                if resp.status_code == 200:
                    return jsonify({
                        'ai': ai_name,
                        'response': resp.json().get('response', resp.json()),
                        'status': 'success',
                        'source': config['url']
                    })
                else:
                    return jsonify({
                        'ai': ai_name,
                        'response': f'Service returned status {resp.status_code}',
                        'status': 'error',
                        'details': resp.text[:200]
                    })

            except requests.exceptions.Timeout:
                return jsonify({
                    'ai': ai_name,
                    'response': f'{ai_name.title()} service timeout - it may be processing',
                    'status': 'timeout'
                })
            except Exception as e:
                return jsonify({
                    'ai': ai_name,
                    'response': f'{ai_name.title()} service error: {str(e)}',
                    'status': 'error'
                })

        else:
            return jsonify({
                'error': f'Unknown AI: {ai_name}',
                'available': list(AI_SERVICES.keys()) + ['c1', 'c2', 'c3']
            }), 404

    except Exception as e:
        return jsonify({'error': str(e), 'ai': ai_name}), 500

@app.route('/status', methods=['GET'])
def check_all_services():
    """Check status of all AI services"""
    status = {}

    # Check each service with its correct health endpoint
    for name, config in AI_SERVICES.items():
        try:
            health_url = config['url'] + config['health']
            resp = requests.get(health_url, timeout=2)
            status[name] = {
                'status': 'online' if resp.status_code == 200 else 'error',
                'url': config['url'],
                'has_chat': config['chat'] is not None
            }
        except:
            status[name] = {
                'status': 'offline',
                'url': config['url'],
                'has_chat': config['chat'] is not None
            }

    # Trinity AIs always available via Claude API
    status['c1_mechanic'] = {'status': 'online', 'url': 'Claude API', 'has_chat': True}
    status['c2_architect'] = {'status': 'online', 'url': 'Claude API', 'has_chat': True}
    status['c3_oracle'] = {'status': 'online', 'url': 'Claude API', 'has_chat': True}

    return jsonify(status)

if __name__ == '__main__':
    print('\n' + '='*70)
    print('  🌉 AI COMMUNICATION BRIDGE v2.0')
    print('='*70)
    print('\nStarting on port 8888...')
    print('\nAvailable AIs:')
    print('  • Araya (consciousness guide)')
    print('  • Builder (project creation)')
    print('  • Observatory (system monitoring)')
    print('  • Visitor Intelligence (analytics)')
    print('  • Analytics (singularity stabilizer)')
    print('  • C1 Mechanic (infrastructure)')
    print('  • C2 Architect (design)')
    print('  • C3 Oracle (vision)')
    print('\nEndpoints:')
    print('  GET  /          - Bridge info')
    print('  GET  /health    - Bridge health')
    print('  GET  /status    - All AI status')
    print('  GET  /list      - List all AIs')
    print('  POST /chat      - Chat with any AI')
    print('\nExample:')
    print('  curl -X POST http://localhost:8888/chat \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"ai": "araya", "message": "What is pattern theory?"}\'')
    print('\n' + '='*70 + '\n')

    app.run(host='0.0.0.0', port=8888, debug=True, use_reloader=False)
