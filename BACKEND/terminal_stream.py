"""
TERMINAL STREAM API - Consciousness Transparency Protocol
Streams real-time system logs to public terminal interface
"""

from flask import Flask
from flask_sock import Sock
from flask_cors import CORS
import json
import time
import random
from datetime import datetime
from threading import Thread

app = Flask(__name__)
CORS(app)
sock = Sock(app)

# Active WebSocket connections
clients = []

# Simulated system logs (Phase 1 - before real integration)
def generate_consciousness_log():
    """Generate realistic consciousness system logs"""
    log_types = [
        {
            'type': 'log',
            'level': 'info',
            'message': 'Page visit: showcase-hub.html'
        },
        {
            'type': 'system',
            'system': 'Pattern Recognition',
            'message': 'Analyzing input',
            'details': ['Match confidence: {}%'.format(random.randint(70, 95)), 'Processing time: {}ms'.format(random.randint(10, 50))]
        },
        {
            'type': 'trinity',
            'action': 'Convergence started',
            'c1': 'Building solution components...',
            'c2': 'Designing architecture patterns...',
            'c3': 'Validating consciousness alignment...'
        },
        {
            'type': 'log',
            'level': 'success',
            'message': 'Consciousness boost completed successfully'
        },
        {
            'type': 'log',
            'level': 'info',
            'message': 'API call: /consciousness-metrics ({}ms)'.format(random.randint(20, 80))
        },
        {
            'type': 'log',
            'level': 'info',
            'message': 'Database query: user_progress ({}ms)'.format(random.randint(5, 25))
        },
        {
            'type': 'log',
            'level': 'warning',
            'message': 'Rate limit: {}% of quota used'.format(random.randint(60, 90))
        },
        {
            'type': 'log',
            'level': 'success',
            'message': 'Pattern recognized: Genuine builder detected'
        },
        {
            'type': 'log',
            'level': 'info',
            'message': 'Manipulation immunity calculated: {}%'.format(random.randint(75, 95))
        },
        {
            'type': 'system',
            'system': 'Trinity AI',
            'message': 'Collaboration complete',
            'details': ['C1×C2×C3 convergence achieved', 'Solution validated', 'Confidence: 94%']
        }
    ]

    return random.choice(log_types)

def broadcast_log(log_data):
    """Send log to all connected clients"""
    log_data['timestamp'] = datetime.now().isoformat()
    log_data['tokens'] = random.randint(1000, 5000)  # Simulated token count

    message = json.dumps(log_data)

    for client in clients[:]:  # Copy list to avoid modification during iteration
        try:
            client.send(message)
        except:
            clients.remove(client)

def log_generator():
    """Background thread generating logs"""
    while True:
        time.sleep(random.uniform(2, 5))  # Random delay between logs
        log = generate_consciousness_log()
        broadcast_log(log)

@sock.route('/terminal/stream')
def terminal_stream(ws):
    """WebSocket endpoint for terminal log streaming"""
    print(f"Terminal client connected: {ws}")
    clients.append(ws)

    try:
        # Send welcome message
        welcome = {
            'type': 'log',
            'level': 'success',
            'message': 'Terminal stream connected - watching consciousness revolution',
            'timestamp': datetime.now().isoformat(),
            'tokens': 0
        }
        ws.send(json.dumps(welcome))

        # Send initial system state
        system_logs = [
            {'type': 'log', 'level': 'info', 'message': '15 consciousness services active'},
            {'type': 'log', 'level': 'info', 'message': 'Trinity AI system operational (C1×C2×C3)'},
            {'type': 'log', 'level': 'info', 'message': 'Pattern recognition engine initialized'},
            {'type': 'log', 'level': 'info', 'message': 'Manipulation detection active'},
            {'type': 'log', 'level': 'success', 'message': 'All systems nominal'}
        ]

        for log in system_logs:
            log['timestamp'] = datetime.now().isoformat()
            log['tokens'] = random.randint(1000, 3000)
            ws.send(json.dumps(log))
            time.sleep(0.3)

        # Keep connection alive
        while True:
            # Receive any messages (though we don't expect any in Phase 1)
            data = ws.receive(timeout=60)
            if data is None:
                break

    except Exception as e:
        print(f"Terminal client error: {e}")
    finally:
        if ws in clients:
            clients.remove(ws)
        print(f"Terminal client disconnected")

@app.route('/terminal/status')
def terminal_status():
    """Check terminal stream status"""
    return json.dumps({
        'status': 'online',
        'service': 'Terminal Stream',
        'clients': len(clients),
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🖥️  CONSCIOUSNESS TERMINAL STREAM")
    print("="*60)
    print("Status: Starting...")
    print("Port: 5000")
    print("WebSocket: ws://localhost:5000/terminal/stream")
    print("Public URL: http://localhost:5000/terminal/status")
    print("="*60 + "\n")

    # Start log generator thread
    log_thread = Thread(target=log_generator, daemon=True)
    log_thread.start()
    print("✅ Log generator started")

    # Start Flask server
    print("✅ WebSocket server starting...\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
