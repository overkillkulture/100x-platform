"""
CENTRAL COMMAND HUB
One input → Many instances → Collect results → One output

Features:
- WebSocket server for real-time communication
- ALL computers connect to this one server
- ONE input box broadcasts to all instances
- See all instances thinking simultaneously
- Screen capture + AI analysis
- No GitHub/cloud/drive dependencies
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import json
from datetime import datetime
from collections import defaultdict
import base64
import os
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'trinity-central-command-2025'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ===== STATE MANAGEMENT =====

# Connected instances: {instance_id: {socket_id, computer_id, name, status, last_seen}}
INSTANCES = {}

# Active tasks: {task_id: {input, status, responses: {instance_id: response}}}
TASKS = {}

# Thinking streams: {instance_id: [thoughts...]}
THINKING_STREAMS = defaultdict(list)

# Screen captures: {instance_id: {screenshot_b64, timestamp, analysis}}
SCREEN_CAPTURES = {}

TASK_COUNTER = 0

# ===== WEBSOCKET EVENTS =====

@socketio.on('connect')
def handle_connect():
    print(f"✅ Client connected: {request.sid}")
    emit('server_message', {'message': 'Connected to Central Command Hub'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f"❌ Client disconnected: {request.sid}")

    # Remove instance if it was registered
    instance_to_remove = None
    for instance_id, data in INSTANCES.items():
        if data.get('socket_id') == request.sid:
            instance_to_remove = instance_id
            break

    if instance_to_remove:
        del INSTANCES[instance_to_remove]
        # Broadcast instance offline
        socketio.emit('instance_offline', {'instance_id': instance_to_remove})

@socketio.on('register_instance')
def handle_register(data):
    """Instance registers itself with the hub"""
    instance_id = data.get('instance_id')
    computer_id = data.get('computer_id')
    instance_name = data.get('name')

    INSTANCES[instance_id] = {
        'socket_id': request.sid,
        'computer_id': computer_id,
        'name': instance_name,
        'status': 'idle',
        'last_seen': datetime.now().isoformat()
    }

    print(f"📝 Registered: {instance_name} (Computer {computer_id})")

    # Broadcast new instance to all
    socketio.emit('instance_online', {
        'instance_id': instance_id,
        'computer_id': computer_id,
        'name': instance_name
    })

    # Send current instances list to new instance
    emit('instances_list', {'instances': INSTANCES})

@socketio.on('submit_task')
def handle_submit_task(data):
    """Central command submits a task"""
    global TASK_COUNTER
    TASK_COUNTER += 1

    task_id = f"task_{TASK_COUNTER}"
    task_input = data.get('input')
    target_instances = data.get('targets', 'all')  # 'all' or list of instance_ids

    TASKS[task_id] = {
        'id': task_id,
        'input': task_input,
        'status': 'distributing',
        'submitted_at': datetime.now().isoformat(),
        'responses': {},
        'final_output': None
    }

    print(f"📤 Task {task_id}: {task_input[:50]}...")

    # Distribute to instances
    if target_instances == 'all':
        targets = list(INSTANCES.keys())
    else:
        targets = target_instances

    for instance_id in targets:
        if instance_id in INSTANCES:
            socket_id = INSTANCES[instance_id]['socket_id']
            socketio.emit('new_task', {
                'task_id': task_id,
                'input': task_input
            }, room=socket_id)

    # Broadcast to dashboard
    socketio.emit('task_created', {
        'task_id': task_id,
        'input': task_input,
        'targets': targets
    })

    emit('task_submitted', {'task_id': task_id})

@socketio.on('task_response')
def handle_task_response(data):
    """Instance sends back a response"""
    task_id = data.get('task_id')
    instance_id = data.get('instance_id')
    response = data.get('response')

    if task_id in TASKS:
        TASKS[task_id]['responses'][instance_id] = {
            'response': response,
            'timestamp': datetime.now().isoformat()
        }

        print(f"📥 Response from {instance_id} for {task_id}")

        # Broadcast response to all viewers
        socketio.emit('task_response_received', {
            'task_id': task_id,
            'instance_id': instance_id,
            'response': response
        })

        # Check if all responses received
        targets = TASKS[task_id].get('targets', [])
        if len(TASKS[task_id]['responses']) >= len(targets):
            # All responses in, combine them
            combine_responses(task_id)

@socketio.on('thinking_stream')
def handle_thinking_stream(data):
    """Instance streams its thinking in real-time"""
    instance_id = data.get('instance_id')
    thought = data.get('thought')

    THINKING_STREAMS[instance_id].append({
        'thought': thought,
        'timestamp': datetime.now().isoformat()
    })

    # Keep only last 100 thoughts
    THINKING_STREAMS[instance_id] = THINKING_STREAMS[instance_id][-100:]

    # Broadcast to dashboard
    socketio.emit('thinking_update', {
        'instance_id': instance_id,
        'thought': thought,
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('screen_capture')
def handle_screen_capture(data):
    """Instance sends a screen capture"""
    instance_id = data.get('instance_id')
    screenshot_b64 = data.get('screenshot')  # Base64 encoded image

    SCREEN_CAPTURES[instance_id] = {
        'screenshot': screenshot_b64,
        'timestamp': datetime.now().isoformat(),
        'analysis': None  # Will be filled by AI
    }

    print(f"📸 Screen capture from {instance_id}")

    # Broadcast to dashboard
    socketio.emit('screen_capture_received', {
        'instance_id': instance_id,
        'screenshot': screenshot_b64,
        'timestamp': datetime.now().isoformat()
    })

    # TODO: Trigger AI analysis of screenshot
    # analyze_screenshot(instance_id, screenshot_b64)

@socketio.on('heartbeat')
def handle_heartbeat(data):
    """Instance sends heartbeat"""
    instance_id = data.get('instance_id')
    if instance_id in INSTANCES:
        INSTANCES[instance_id]['last_seen'] = datetime.now().isoformat()
        INSTANCES[instance_id]['status'] = data.get('status', 'idle')

# ===== RESPONSE COMBINATION =====

def combine_responses(task_id):
    """Combine all responses into final output"""
    task = TASKS[task_id]
    responses = task['responses']

    # Simple combination: concatenate all responses
    combined = "\n\n".join([
        f"[{inst_id}]: {resp['response']}"
        for inst_id, resp in responses.items()
    ])

    task['final_output'] = combined
    task['status'] = 'completed'

    print(f"✅ Task {task_id} completed")

    # Broadcast completion
    socketio.emit('task_completed', {
        'task_id': task_id,
        'final_output': combined
    })

# ===== HTTP ROUTES =====

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/instances')
def get_instances():
    """Get all connected instances"""
    return jsonify({'instances': INSTANCES})

@app.route('/api/tasks')
def get_tasks():
    """Get all tasks"""
    return jsonify({'tasks': TASKS})

@app.route('/api/thinking/<instance_id>')
def get_thinking(instance_id):
    """Get thinking stream for an instance"""
    return jsonify({'thoughts': THINKING_STREAMS.get(instance_id, [])})

@app.route('/api/screen/<instance_id>')
def get_screen(instance_id):
    """Get latest screen capture for an instance"""
    return jsonify(SCREEN_CAPTURES.get(instance_id, {}))

# ===== DASHBOARD HTML =====

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>CENTRAL COMMAND HUB</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background: #000;
            color: #0f0;
            padding: 20px;
            overflow-x: hidden;
        }

        .header {
            text-align: center;
            padding: 20px;
            border: 3px solid #0f0;
            margin-bottom: 20px;
            background: rgba(0, 255, 0, 0.05);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.3); }
            50% { box-shadow: 0 0 40px rgba(0, 255, 0, 0.6); }
        }

        h1 {
            font-size: 2.5em;
            text-shadow: 0 0 20px #0f0;
        }

        .input-section {
            margin-bottom: 20px;
            padding: 20px;
            border: 2px solid #0f0;
            background: rgba(0, 255, 0, 0.05);
        }

        .input-box {
            width: 100%;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            background: #000;
            color: #0f0;
            border: 2px solid #0f0;
            margin-bottom: 10px;
            resize: vertical;
        }

        .submit-btn {
            padding: 15px 30px;
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            background: #0f0;
            color: #000;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }

        .submit-btn:hover {
            background: #0ff;
        }

        .instances-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }

        .instance-panel {
            border: 2px solid #0f0;
            padding: 15px;
            background: rgba(0, 0, 0, 0.9);
            min-height: 300px;
        }

        .instance-panel.offline {
            border-color: #f00;
            opacity: 0.5;
        }

        .instance-header {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #0f0;
        }

        .thinking-stream {
            max-height: 250px;
            overflow-y: auto;
            font-size: 0.9em;
            line-height: 1.6;
        }

        .thought {
            margin-bottom: 8px;
            padding: 5px;
            border-left: 2px solid #0f0;
            padding-left: 10px;
        }

        .output-section {
            margin-top: 20px;
            padding: 20px;
            border: 2px solid #0ff;
            background: rgba(0, 255, 255, 0.05);
        }

        .output-box {
            padding: 15px;
            background: #000;
            color: #0ff;
            border: 1px solid #0ff;
            min-height: 200px;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
        }

        .status-bar {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #0f0;
            background: rgba(0, 255, 0, 0.05);
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            font-size: 2em;
            color: #0f0;
            text-shadow: 0 0 10px #0f0;
        }

        .stat-label {
            color: #0a0;
            margin-top: 5px;
        }

        .blink {
            animation: blink 1s infinite;
        }

        @keyframes blink {
            0%, 50%, 100% { opacity: 1; }
            25%, 75% { opacity: 0.3; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚡ CENTRAL COMMAND HUB ⚡</h1>
        <p>One Input → Many Instances → One Output</p>
        <p style="margin-top: 10px;" class="blink">● LIVE</p>
    </div>

    <div class="status-bar">
        <div class="stat">
            <div class="stat-number" id="instance-count">0</div>
            <div class="stat-label">Instances Online</div>
        </div>
        <div class="stat">
            <div class="stat-number" id="task-count">0</div>
            <div class="stat-label">Tasks Processed</div>
        </div>
        <div class="stat">
            <div class="stat-number" id="thinking-count">0</div>
            <div class="stat-label">Thoughts Captured</div>
        </div>
    </div>

    <div class="input-section">
        <h2>📤 CENTRAL INPUT</h2>
        <textarea id="input-box" class="input-box" rows="4" placeholder="Type your command here... It will be distributed to ALL connected instances."></textarea>
        <button class="submit-btn" onclick="submitTask()">🚀 DISTRIBUTE TO ALL INSTANCES</button>
    </div>

    <h2 style="margin: 20px 0;">🤖 LIVE THINKING STREAMS</h2>
    <div class="instances-grid" id="instances-grid">
        <div class="instance-panel offline">
            <div class="instance-header">Waiting for instances...</div>
            <div class="thinking-stream">
                No instances connected yet.<br><br>
                Instances will appear here when they connect to the hub.
            </div>
        </div>
    </div>

    <div class="output-section">
        <h2>📥 COMBINED OUTPUT</h2>
        <div class="output-box" id="output-box">
            Waiting for responses...
        </div>
    </div>

    <script>
        const socket = io();

        let instances = {};
        let thinkingCount = 0;
        let taskCount = 0;

        socket.on('connect', () => {
            console.log('Connected to Central Command Hub');
        });

        socket.on('instance_online', (data) => {
            instances[data.instance_id] = data;
            updateInstancesGrid();
            updateStats();
        });

        socket.on('instance_offline', (data) => {
            delete instances[data.instance_id];
            updateInstancesGrid();
            updateStats();
        });

        socket.on('thinking_update', (data) => {
            addThought(data.instance_id, data.thought);
            thinkingCount++;
            updateStats();
        });

        socket.on('task_response_received', (data) => {
            addOutput(`[${data.instance_id}]: ${data.response}`);
        });

        socket.on('task_completed', (data) => {
            addOutput('\\n✅ TASK COMPLETED\\n\\n' + data.final_output);
            taskCount++;
            updateStats();
        });

        function submitTask() {
            const input = document.getElementById('input-box').value;
            if (!input.trim()) {
                alert('Please enter a command');
                return;
            }

            socket.emit('submit_task', {
                input: input,
                targets: 'all'
            });

            addOutput('\\n📤 DISTRIBUTED TO ALL INSTANCES: ' + input + '\\n');
            document.getElementById('input-box').value = '';
        }

        function updateInstancesGrid() {
            const grid = document.getElementById('instances-grid');
            grid.innerHTML = '';

            for (const [id, data] of Object.entries(instances)) {
                const panel = document.createElement('div');
                panel.className = 'instance-panel';
                panel.id = 'instance-' + id;

                panel.innerHTML = `
                    <div class="instance-header">
                        ${data.name}<br>
                        <span style="font-size: 0.8em; color: #0a0;">Computer ${data.computer_id}</span>
                    </div>
                    <div class="thinking-stream" id="thinking-${id}">
                        <div style="color: #0a0;">Waiting for thoughts...</div>
                    </div>
                `;

                grid.appendChild(panel);
            }

            if (Object.keys(instances).length === 0) {
                grid.innerHTML = `
                    <div class="instance-panel offline">
                        <div class="instance-header">Waiting for instances...</div>
                        <div class="thinking-stream">
                            No instances connected yet.<br><br>
                            Instances will appear here when they connect to the hub.
                        </div>
                    </div>
                `;
            }
        }

        function addThought(instanceId, thought) {
            const stream = document.getElementById('thinking-' + instanceId);
            if (stream) {
                const thoughtDiv = document.createElement('div');
                thoughtDiv.className = 'thought';
                thoughtDiv.textContent = thought;
                stream.appendChild(thoughtDiv);

                // Auto-scroll
                stream.scrollTop = stream.scrollHeight;

                // Keep only last 20 thoughts
                while (stream.children.length > 20) {
                    stream.removeChild(stream.firstChild);
                }
            }
        }

        function addOutput(text) {
            const outputBox = document.getElementById('output-box');
            outputBox.textContent += text + '\\n';
            outputBox.scrollTop = outputBox.scrollHeight;
        }

        function updateStats() {
            document.getElementById('instance-count').textContent = Object.keys(instances).length;
            document.getElementById('task-count').textContent = taskCount;
            document.getElementById('thinking-count').textContent = thinkingCount;
        }

        // Allow Enter to submit (Ctrl+Enter for new line)
        document.getElementById('input-box').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                submitTask();
                e.preventDefault();
            }
        });
    </script>
</body>
</html>
'''

# ===== STARTUP =====

if __name__ == '__main__':
    print('\n' + '='*70)
    print('  ⚡ CENTRAL COMMAND HUB')
    print('='*70)
    print('\nOne Input → Many Instances → One Output')
    print('\nFeatures:')
    print('  • WebSocket real-time communication')
    print('  • All computers connect to this hub')
    print('  • One input box distributes to all instances')
    print('  • Live thinking streams visible')
    print('  • Combined output from all responses')
    print('\nStarting server...')
    print('\n📊 Dashboard: http://localhost:5555')
    print('='*70 + '\n')

    socketio.run(app, host='0.0.0.0', port=5555, debug=False)
