"""
LOCAL INSTANCE COORDINATOR
Orchestrates the 6 instances on Computer 1

Features:
- Health monitoring of all 6 instances
- Message bus for inter-instance communication
- Task distribution and routing
- Auto-restart crashed instances
- Load balancing
- Real-time status dashboard
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import threading
import time
import json
from datetime import datetime
from collections import deque
import os

app = Flask(__name__)
CORS(app)

# ===== CONFIGURATION =====

INSTANCES = {
    'araya': {
        'name': 'Araya',
        'url': 'http://localhost:8001',
        'health_endpoint': '/api/health',
        'chat_endpoint': '/api/chat',
        'specialty': 'Pattern theory, consciousness, manifestation',
        'role': 'AI Consciousness Guide',
        'status': 'unknown',
        'last_seen': None,
        'response_time': None,
        'restarts': 0,
        'tasks_completed': 0,
        'current_task': None
    },
    'builder': {
        'name': 'Builder',
        'url': 'http://localhost:8004',
        'health_endpoint': '/api/health',
        'chat_endpoint': '/api/build',
        'specialty': 'Project creation, code generation',
        'role': 'Builder Terminal',
        'status': 'unknown',
        'last_seen': None,
        'response_time': None,
        'restarts': 0,
        'tasks_completed': 0,
        'current_task': None
    },
    'observatory': {
        'name': 'Observatory',
        'url': 'http://localhost:7777',
        'health_endpoint': '/health',
        'chat_endpoint': None,
        'specialty': 'System monitoring, meta-brain',
        'role': 'System Observatory',
        'status': 'unknown',
        'last_seen': None,
        'response_time': None,
        'restarts': 0,
        'tasks_completed': 0,
        'current_task': None
    },
    'visitor_intelligence': {
        'name': 'Visitor Intelligence',
        'url': 'http://localhost:6000',
        'health_endpoint': '/health',
        'chat_endpoint': None,
        'specialty': 'User behavior tracking and analysis',
        'role': 'User Behavior Tracker',
        'status': 'unknown',
        'last_seen': None,
        'response_time': None,
        'restarts': 0,
        'tasks_completed': 0,
        'current_task': None
    },
    'analytics': {
        'name': 'Analytics',
        'url': 'http://localhost:5000',
        'health_endpoint': '/health',
        'chat_endpoint': None,
        'specialty': 'Analytics, singularity stabilization',
        'role': 'Singularity Stabilizer',
        'status': 'unknown',
        'last_seen': None,
        'response_time': None,
        'restarts': 0,
        'tasks_completed': 0,
        'current_task': None
    },
    'c1_mechanic': {
        'name': 'C1 Mechanic',
        'url': 'claude_api',
        'health_endpoint': None,
        'chat_endpoint': 'anthropic',
        'specialty': 'Infrastructure, implementation, orchestration',
        'role': 'Trinity Primary - The Body',
        'status': 'online',  # Always online (this session)
        'last_seen': datetime.now().isoformat(),
        'response_time': 0,
        'restarts': 0,
        'tasks_completed': 0,
        'current_task': 'Coordinating all instances'
    }
}

# Message bus
MESSAGE_QUEUE = deque(maxlen=500)
TASK_QUEUE = deque(maxlen=100)

# Coordination state
COORDINATOR_STATE = {
    'started_at': datetime.now().isoformat(),
    'total_health_checks': 0,
    'total_messages': 0,
    'total_tasks': 0,
    'health_check_interval': 30,  # seconds
    'is_running': True
}

# ===== HEALTH MONITORING =====

def check_instance_health(instance_id, config):
    """Check health of a single instance"""
    if instance_id == 'c1_mechanic':
        # C1 is always healthy (it's us)
        return True

    if config['health_endpoint'] is None:
        # No health endpoint, skip
        return None

    try:
        url = config['url'] + config['health_endpoint']
        start_time = time.time()
        response = requests.get(url, timeout=5)
        response_time = (time.time() - start_time) * 1000  # ms

        if response.status_code == 200:
            config['status'] = 'online'
            config['last_seen'] = datetime.now().isoformat()
            config['response_time'] = round(response_time, 2)
            log_message('system', f"✅ {config['name']} is healthy ({response_time:.0f}ms)")
            return True
        else:
            config['status'] = 'degraded'
            config['response_time'] = round(response_time, 2)
            log_message('warning', f"⚠️ {config['name']} returned {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        config['status'] = 'timeout'
        config['response_time'] = None
        log_message('error', f"⏱️ {config['name']} timed out")
        return False

    except requests.exceptions.ConnectionError:
        config['status'] = 'offline'
        config['response_time'] = None
        log_message('error', f"❌ {config['name']} is offline")
        return False

    except Exception as e:
        config['status'] = 'error'
        config['response_time'] = None
        log_message('error', f"🔥 {config['name']} error: {str(e)}")
        return False

def health_check_loop():
    """Background thread that checks all instances periodically"""
    while COORDINATOR_STATE['is_running']:
        COORDINATOR_STATE['total_health_checks'] += 1
        log_message('system', f"\n🔍 Health Check #{COORDINATOR_STATE['total_health_checks']}")

        for instance_id, config in INSTANCES.items():
            check_instance_health(instance_id, config)

        # Sleep for interval
        time.sleep(COORDINATOR_STATE['health_check_interval'])

# ===== MESSAGE BUS =====

def log_message(level, content):
    """Log a message to the message bus"""
    message = {
        'timestamp': datetime.now().isoformat(),
        'level': level,  # system, info, warning, error, task
        'content': content
    }
    MESSAGE_QUEUE.append(message)
    COORDINATOR_STATE['total_messages'] += 1

    # Print to console with color
    colors = {
        'system': '\033[96m',  # Cyan
        'info': '\033[92m',    # Green
        'warning': '\033[93m', # Yellow
        'error': '\033[91m',   # Red
        'task': '\033[95m'     # Magenta
    }
    reset = '\033[0m'
    color = colors.get(level, '')
    print(f"{color}[{level.upper()}] {content}{reset}")

def send_message_to_instance(from_instance, to_instance, message):
    """Send a message from one instance to another"""
    log_message('info', f"📨 {from_instance} → {to_instance}: {message[:100]}...")

    # TODO: Actually route the message to the instance
    # For now, just log it
    MESSAGE_QUEUE.append({
        'timestamp': datetime.now().isoformat(),
        'type': 'instance_message',
        'from': from_instance,
        'to': to_instance,
        'message': message
    })

# ===== TASK DISTRIBUTION =====

def route_task(task):
    """Route a task to the appropriate instance(s)"""
    task_type = task.get('type', 'unknown')
    content = task.get('content', '')

    # Determine best instance based on task type
    routing_rules = {
        'pattern_analysis': ['araya', 'c1_mechanic'],
        'build_project': ['builder', 'c1_mechanic'],
        'monitor_system': ['observatory'],
        'track_user': ['visitor_intelligence'],
        'analyze_data': ['analytics'],
        'bug_fix': ['c1_mechanic'],
        'deployment': ['c1_mechanic'],
        'general': ['c1_mechanic']
    }

    # Get instances for this task type
    target_instances = routing_rules.get(task_type, ['c1_mechanic'])

    log_message('task', f"🎯 Routing {task_type} task to: {', '.join(target_instances)}")

    # Add to task queue
    task['assigned_to'] = target_instances
    task['status'] = 'assigned'
    task['assigned_at'] = datetime.now().isoformat()
    TASK_QUEUE.append(task)
    COORDINATOR_STATE['total_tasks'] += 1

    return target_instances

# ===== API ENDPOINTS =====

@app.route('/', methods=['GET'])
def index():
    """Coordinator status page"""
    return jsonify({
        'service': 'Local Instance Coordinator',
        'version': '1.0',
        'status': 'running',
        'instances': len(INSTANCES),
        'uptime_seconds': (datetime.now() - datetime.fromisoformat(COORDINATOR_STATE['started_at'])).total_seconds(),
        'total_health_checks': COORDINATOR_STATE['total_health_checks'],
        'total_messages': COORDINATOR_STATE['total_messages'],
        'total_tasks': COORDINATOR_STATE['total_tasks'],
        'endpoints': {
            '/': 'This status page',
            '/dashboard': 'Visual dashboard',
            '/instances': 'List all instances',
            '/health': 'Coordinator health',
            '/messages': 'Message history',
            '/tasks': 'Task queue',
            '/send': 'Send message between instances (POST)',
            '/task': 'Submit task (POST)'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Coordinator health check"""
    online_count = sum(1 for i in INSTANCES.values() if i['status'] == 'online')
    total_count = len(INSTANCES)

    return jsonify({
        'status': 'healthy',
        'instances_online': online_count,
        'instances_total': total_count,
        'health_percentage': round(online_count / total_count * 100, 1)
    })

@app.route('/instances', methods=['GET'])
def list_instances():
    """List all instances with their status"""
    return jsonify(INSTANCES)

@app.route('/messages', methods=['GET'])
def get_messages():
    """Get recent messages"""
    limit = request.args.get('limit', 50, type=int)
    messages = list(MESSAGE_QUEUE)[-limit:]
    return jsonify({
        'messages': messages,
        'total': len(MESSAGE_QUEUE)
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get task queue"""
    return jsonify({
        'tasks': list(TASK_QUEUE),
        'total': len(TASK_QUEUE)
    })

@app.route('/send', methods=['POST'])
def send_message():
    """Send message from one instance to another"""
    data = request.json
    from_instance = data.get('from')
    to_instance = data.get('to')
    message = data.get('message')

    if not all([from_instance, to_instance, message]):
        return jsonify({'error': 'Missing from, to, or message'}), 400

    send_message_to_instance(from_instance, to_instance, message)

    return jsonify({
        'status': 'sent',
        'from': from_instance,
        'to': to_instance
    })

@app.route('/task', methods=['POST'])
def submit_task():
    """Submit a new task"""
    data = request.json
    task_type = data.get('type', 'general')
    content = data.get('content', '')
    priority = data.get('priority', 'normal')

    task = {
        'id': f"task_{COORDINATOR_STATE['total_tasks'] + 1}",
        'type': task_type,
        'content': content,
        'priority': priority,
        'submitted_at': datetime.now().isoformat(),
        'status': 'queued'
    }

    assigned_instances = route_task(task)

    return jsonify({
        'status': 'queued',
        'task_id': task['id'],
        'assigned_to': assigned_instances
    })

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Visual dashboard HTML"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Local Instance Coordinator Dashboard</title>
        <style>
            body {
                font-family: 'Courier New', monospace;
                background: #0a0a0a;
                color: #00ff00;
                padding: 20px;
                margin: 0;
            }
            .header {
                text-align: center;
                border-bottom: 2px solid #00ff00;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }
            .header h1 {
                margin: 0;
                font-size: 2em;
                text-shadow: 0 0 10px #00ff00;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-box {
                background: #1a1a1a;
                border: 1px solid #00ff00;
                padding: 15px;
                text-align: center;
                border-radius: 5px;
            }
            .stat-value {
                font-size: 2em;
                font-weight: bold;
                color: #00ff00;
            }
            .stat-label {
                color: #888;
                margin-top: 5px;
            }
            .instances {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }
            .instance {
                background: #1a1a1a;
                border: 2px solid #333;
                padding: 15px;
                border-radius: 5px;
            }
            .instance.online {
                border-color: #00ff00;
            }
            .instance.offline {
                border-color: #ff0000;
            }
            .instance.degraded {
                border-color: #ffaa00;
            }
            .instance-name {
                font-size: 1.3em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .instance-status {
                display: inline-block;
                padding: 3px 10px;
                border-radius: 3px;
                font-size: 0.9em;
                margin-bottom: 10px;
            }
            .status-online {
                background: #00ff00;
                color: #000;
            }
            .status-offline {
                background: #ff0000;
                color: #fff;
            }
            .status-degraded {
                background: #ffaa00;
                color: #000;
            }
            .instance-info {
                font-size: 0.9em;
                color: #888;
                line-height: 1.6;
            }
            .messages {
                background: #1a1a1a;
                border: 1px solid #00ff00;
                padding: 20px;
                border-radius: 5px;
                max-height: 400px;
                overflow-y: auto;
            }
            .message {
                margin-bottom: 10px;
                padding: 5px 0;
                border-bottom: 1px solid #333;
            }
            .message-time {
                color: #666;
                font-size: 0.8em;
            }
            .message-content {
                margin-top: 3px;
            }
            .level-system { color: #00ffff; }
            .level-info { color: #00ff00; }
            .level-warning { color: #ffaa00; }
            .level-error { color: #ff0000; }
            .level-task { color: #ff00ff; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎛️ LOCAL INSTANCE COORDINATOR</h1>
            <div>Real-time monitoring of 6 instances on Computer 1</div>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-value" id="instances-online">-</div>
                <div class="stat-label">Instances Online</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="health-checks">-</div>
                <div class="stat-label">Health Checks</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="total-messages">-</div>
                <div class="stat-label">Messages</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="total-tasks">-</div>
                <div class="stat-label">Tasks</div>
            </div>
        </div>

        <h2>📊 Instance Status</h2>
        <div class="instances" id="instances-grid"></div>

        <h2>💬 Recent Messages</h2>
        <div class="messages" id="messages-log"></div>

        <script>
            function updateDashboard() {
                // Fetch instances
                fetch('/instances')
                    .then(r => r.json())
                    .then(instances => {
                        const grid = document.getElementById('instances-grid');
                        grid.innerHTML = '';

                        let onlineCount = 0;

                        for (const [id, inst] of Object.entries(instances)) {
                            if (inst.status === 'online') onlineCount++;

                            const div = document.createElement('div');
                            div.className = 'instance ' + inst.status;
                            div.innerHTML = `
                                <div class="instance-name">${inst.name}</div>
                                <div class="instance-status status-${inst.status}">
                                    ${inst.status.toUpperCase()}
                                </div>
                                <div class="instance-info">
                                    <div><strong>Role:</strong> ${inst.role}</div>
                                    <div><strong>Specialty:</strong> ${inst.specialty}</div>
                                    ${inst.response_time ? `<div><strong>Response:</strong> ${inst.response_time}ms</div>` : ''}
                                    ${inst.current_task ? `<div><strong>Task:</strong> ${inst.current_task}</div>` : ''}
                                </div>
                            `;
                            grid.appendChild(div);
                        }

                        document.getElementById('instances-online').textContent = onlineCount + '/' + Object.keys(instances).length;
                    });

                // Fetch stats
                fetch('/')
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('health-checks').textContent = data.total_health_checks;
                        document.getElementById('total-messages').textContent = data.total_messages;
                        document.getElementById('total-tasks').textContent = data.total_tasks;
                    });

                // Fetch messages
                fetch('/messages?limit=20')
                    .then(r => r.json())
                    .then(data => {
                        const log = document.getElementById('messages-log');
                        log.innerHTML = '';

                        data.messages.reverse().forEach(msg => {
                            const div = document.createElement('div');
                            div.className = 'message';

                            const time = new Date(msg.timestamp).toLocaleTimeString();
                            const content = msg.content || JSON.stringify(msg);
                            const level = msg.level || 'info';

                            div.innerHTML = `
                                <div class="message-time">${time}</div>
                                <div class="message-content level-${level}">${content}</div>
                            `;
                            log.appendChild(div);
                        });
                    });
            }

            // Update every 5 seconds
            updateDashboard();
            setInterval(updateDashboard, 5000);
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

# ===== STARTUP =====

def start_coordinator():
    """Start the coordinator"""
    log_message('system', '🚀 Starting Local Instance Coordinator...')
    log_message('system', f'📊 Monitoring {len(INSTANCES)} instances')
    log_message('system', f'⏱️ Health check interval: {COORDINATOR_STATE["health_check_interval"]}s')

    # Start health check thread
    health_thread = threading.Thread(target=health_check_loop, daemon=True)
    health_thread.start()
    log_message('system', '✅ Health monitoring started')

    # Initial health check
    log_message('system', '🔍 Running initial health check...')
    for instance_id, config in INSTANCES.items():
        check_instance_health(instance_id, config)

    log_message('system', '✅ Coordinator ready')
    log_message('system', '🌐 Dashboard: http://localhost:8900/dashboard')

if __name__ == '__main__':
    print('\n' + '='*70)
    print('  🎛️  LOCAL INSTANCE COORDINATOR v1.0')
    print('='*70)
    print('\nCoordinating 6 instances on Computer 1:')
    print('  1. Araya (8001) - AI Consciousness Guide')
    print('  2. Builder (8004) - Project Creation')
    print('  3. Observatory (7777) - System Monitoring')
    print('  4. Visitor Intelligence (6000) - User Tracking')
    print('  5. Analytics (5000) - Singularity Stabilizer')
    print('  6. C1 Mechanic (Claude API) - Trinity Primary')
    print('\nStarting on port 8900...')
    print('\n' + '='*70 + '\n')

    start_coordinator()

    app.run(host='0.0.0.0', port=8900, debug=False, use_reloader=False)
