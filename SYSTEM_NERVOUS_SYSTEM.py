"""
SYSTEM NERVOUS SYSTEM
Central communication hub - everything talks to everything

This is the "tap on the shoulder" system Commander requested.
Every service registers here, sends heartbeats, broadcasts events, and can query other services.
"""
import json
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import requests

app = Flask(__name__)
CORS(app)

# Data storage
DATA_DIR = Path(__file__).parent / 'SYSTEM_NERVOUS_SYSTEM_DATA'
DATA_DIR.mkdir(exist_ok=True)

# In-memory state (fast access)
SERVICES = {}  # {service_id: {name, url, last_heartbeat, status, metadata}}
EVENTS = []    # Recent events (last 100)
MESSAGES = {}  # {service_id: [messages]}

# Configuration
MAX_EVENTS = 100
HEARTBEAT_TIMEOUT = 60  # seconds


def save_state():
    """Save current state to disk"""
    state = {
        'services': SERVICES,
        'events': EVENTS[-50:],  # Save last 50 events
        'timestamp': datetime.now().isoformat()
    }
    with open(DATA_DIR / 'state.json', 'w') as f:
        json.dump(state, f, indent=2)


def load_state():
    """Load state from disk"""
    global SERVICES, EVENTS
    state_file = DATA_DIR / 'state.json'
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
            SERVICES = state.get('services', {})
            EVENTS = state.get('events', [])


def add_event(event_type, service_id, data):
    """Add event to feed"""
    event = {
        'type': event_type,
        'service_id': service_id,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    EVENTS.append(event)

    # Keep only recent events
    if len(EVENTS) > MAX_EVENTS:
        EVENTS.pop(0)

    # Auto-save on important events
    if event_type in ['service_registered', 'service_dead', 'error']:
        save_state()


def check_heartbeats():
    """Background thread to check service heartbeats"""
    while True:
        time.sleep(10)  # Check every 10 seconds

        now = time.time()
        for service_id, service in SERVICES.items():
            last_heartbeat = service.get('last_heartbeat_time', 0)

            if now - last_heartbeat > HEARTBEAT_TIMEOUT:
                if service.get('status') != 'dead':
                    service['status'] = 'dead'
                    add_event('service_dead', service_id, {
                        'name': service.get('name'),
                        'last_seen': service.get('last_heartbeat')
                    })


# Start heartbeat checker
threading.Thread(target=check_heartbeats, daemon=True).start()


@app.route('/register', methods=['POST'])
def register_service():
    """Register a service with the nervous system"""
    data = request.json
    service_id = data.get('service_id')

    SERVICES[service_id] = {
        'name': data.get('name'),
        'url': data.get('url'),
        'port': data.get('port'),
        'type': data.get('type', 'unknown'),
        'capabilities': data.get('capabilities', []),
        'status': 'online',
        'last_heartbeat': datetime.now().isoformat(),
        'last_heartbeat_time': time.time(),
        'metadata': data.get('metadata', {})
    }

    add_event('service_registered', service_id, {
        'name': data.get('name'),
        'type': data.get('type')
    })

    return jsonify({
        'status': 'registered',
        'service_id': service_id,
        'total_services': len(SERVICES)
    })


@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    """Service sends heartbeat to show it's alive"""
    data = request.json
    service_id = data.get('service_id')

    if service_id in SERVICES:
        SERVICES[service_id]['last_heartbeat'] = datetime.now().isoformat()
        SERVICES[service_id]['last_heartbeat_time'] = time.time()
        SERVICES[service_id]['status'] = 'online'

        # Update metadata if provided
        if 'metadata' in data:
            SERVICES[service_id]['metadata'].update(data['metadata'])

        return jsonify({'status': 'ok', 'service_id': service_id})
    else:
        return jsonify({'status': 'error', 'message': 'Service not registered'}), 404


@app.route('/broadcast', methods=['POST'])
def broadcast_event():
    """Broadcast an event to all listening services"""
    data = request.json
    service_id = data.get('service_id')
    event_type = data.get('event_type')
    event_data = data.get('data', {})

    add_event(event_type, service_id, event_data)

    # If event has targets, send directly to them
    targets = data.get('targets', [])
    if targets:
        for target_id in targets:
            if target_id in MESSAGES:
                MESSAGES[target_id].append({
                    'from': service_id,
                    'type': event_type,
                    'data': event_data,
                    'timestamp': datetime.now().isoformat()
                })
            else:
                MESSAGES[target_id] = [{
                    'from': service_id,
                    'type': event_type,
                    'data': event_data,
                    'timestamp': datetime.now().isoformat()
                }]

    return jsonify({
        'status': 'broadcasted',
        'event_type': event_type,
        'listeners': len(SERVICES)
    })


@app.route('/query/<service_id>', methods=['GET'])
def query_service(service_id):
    """'Tap on the shoulder' - Query what a service is doing"""

    if service_id not in SERVICES:
        return jsonify({
            'status': 'error',
            'message': f'Service {service_id} not found'
        }), 404

    service = SERVICES[service_id]

    # Try to get live status from the service
    service_url = service.get('url')
    live_status = None

    if service_url:
        try:
            response = requests.get(f"{service_url}/status", timeout=2)
            if response.status_code == 200:
                live_status = response.json()
        except:
            pass  # Service might not have /status endpoint

    return jsonify({
        'service_id': service_id,
        'registered_info': service,
        'live_status': live_status,
        'queried_at': datetime.now().isoformat()
    })


@app.route('/ask/<service_id>', methods=['POST'])
def ask_service(service_id):
    """Ask a service to do something or answer a question"""

    if service_id not in SERVICES:
        return jsonify({
            'status': 'error',
            'message': f'Service {service_id} not found'
        }), 404

    service = SERVICES[service_id]
    data = request.json

    # Send request to service
    service_url = service.get('url')
    if not service_url:
        return jsonify({
            'status': 'error',
            'message': 'Service has no URL registered'
        }), 400

    try:
        # Forward the request to the service
        endpoint = data.get('endpoint', '/process')
        response = requests.post(f"{service_url}{endpoint}", json=data, timeout=5)

        return jsonify({
            'status': 'success',
            'service_id': service_id,
            'response': response.json() if response.status_code == 200 else None,
            'status_code': response.status_code
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/services', methods=['GET'])
def list_services():
    """List all registered services"""

    services_list = []
    for service_id, service in SERVICES.items():
        services_list.append({
            'id': service_id,
            'name': service.get('name'),
            'type': service.get('type'),
            'status': service.get('status'),
            'last_heartbeat': service.get('last_heartbeat'),
            'url': service.get('url'),
            'capabilities': service.get('capabilities', [])
        })

    return jsonify({
        'services': services_list,
        'total': len(services_list),
        'online': len([s for s in services_list if s['status'] == 'online']),
        'dead': len([s for s in services_list if s['status'] == 'dead'])
    })


@app.route('/events', methods=['GET'])
def get_events():
    """Get recent events"""
    limit = request.args.get('limit', 50, type=int)

    return jsonify({
        'events': EVENTS[-limit:],
        'total_events': len(EVENTS)
    })


@app.route('/messages/<service_id>', methods=['GET'])
def get_messages(service_id):
    """Get messages for a service"""

    messages = MESSAGES.get(service_id, [])

    # Mark as read (clear after retrieval)
    if service_id in MESSAGES:
        MESSAGES[service_id] = []

    return jsonify({
        'service_id': service_id,
        'messages': messages,
        'count': len(messages)
    })


@app.route('/system/status', methods=['GET'])
def system_status():
    """Get overall system status"""

    online_services = [s for s in SERVICES.values() if s['status'] == 'online']
    dead_services = [s for s in SERVICES.values() if s['status'] == 'dead']

    return jsonify({
        'total_services': len(SERVICES),
        'online': len(online_services),
        'dead': len(dead_services),
        'recent_events': EVENTS[-10:],
        'services': {
            'online': [s['name'] for s in online_services],
            'dead': [s['name'] for s in dead_services]
        },
        'system_health': 'healthy' if len(online_services) > 0 else 'critical',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/system/health', methods=['GET'])
def system_health():
    """Quick health check endpoint"""

    online_count = len([s for s in SERVICES.values() if s['status'] == 'online'])

    return jsonify({
        'status': 'healthy' if online_count > 0 else 'critical',
        'online_services': online_count,
        'total_services': len(SERVICES)
    })


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🧠 SYSTEM NERVOUS SYSTEM - CENTRAL COMMUNICATION HUB 🧠")
    print("=" * 60)
    print("\nThis is the 'tap on shoulder' system.")
    print("All services register here and communicate through here.")
    print("\nEndpoints:")
    print("  POST /register        - Service registers itself")
    print("  POST /heartbeat       - Service sends heartbeat")
    print("  POST /broadcast       - Broadcast event to all services")
    print("  GET  /query/<id>      - Query what a service is doing")
    print("  POST /ask/<id>        - Ask service to do something")
    print("  GET  /services        - List all services")
    print("  GET  /events          - Get recent events")
    print("  GET  /messages/<id>   - Get messages for service")
    print("  GET  /system/status   - Overall system status")
    print("  GET  /system/health   - Quick health check")
    print("\n" + "=" * 60)
    print("Starting on http://localhost:7777")
    print("=" * 60 + "\n")

    # Load previous state
    load_state()

    app.run(host='0.0.0.0', port=7776, debug=False)
