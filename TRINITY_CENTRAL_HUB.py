#!/usr/bin/env python3
"""
TRINITY CENTRAL HUB
===================

Central convergence point for all Trinity systems across all computers.

This hub:
1. Receives status reports from all computers
2. Stores messages between computers
3. Distributes instructions
4. Provides web interface for monitoring
5. Works offline (stores everything locally)
6. Future: Phone control interface

Architecture:
- All computers report here
- All Trinities (C1×C2×C3) on each computer sync here
- Commander can view/control from anywhere
- Offline-first (no cloud dependency)
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path
import threading
import time

app = Flask(__name__)
CORS(app)

# Data storage (offline-first)
DATA_DIR = Path("TRINITY_HUB_DATA")
DATA_DIR.mkdir(exist_ok=True)

COMPUTERS_FILE = DATA_DIR / "computers.json"
MESSAGES_FILE = DATA_DIR / "messages.json"
INSTRUCTIONS_FILE = DATA_DIR / "instructions.json"

def load_data(file_path):
    """Load JSON data"""
    if file_path.exists():
        return json.loads(file_path.read_text())
    return []

def save_data(file_path, data):
    """Save JSON data"""
    file_path.write_text(json.dumps(data, indent=2))

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """Main hub dashboard"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Trinity Central Hub</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            padding: 20px;
        }
        h1 {
            text-align: center;
            font-size: 2em;
            margin-bottom: 30px;
            text-shadow: 0 0 10px #00ff00;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .register-panel {
            background: rgba(0, 200, 255, 0.1);
            border: 2px solid #00ddff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }
        .register-panel h2 {
            color: #00ddff;
            margin-bottom: 15px;
            text-align: center;
        }
        .register-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .register-btn {
            background: linear-gradient(135deg, #00ff00, #00ddff);
            color: #000;
            padding: 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            font-size: 1em;
            transition: all 0.3s;
        }
        .register-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
        }
        .register-btn:active {
            transform: scale(0.95);
        }
        .computer {
            background: rgba(0, 255, 0, 0.1);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .computer h2 {
            color: #00ddff;
            margin-bottom: 10px;
        }
        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            margin-right: 10px;
        }
        .online { background: rgba(0, 255, 0, 0.3); }
        .offline { background: rgba(255, 0, 0, 0.3); color: #ff0000; }
        .capability {
            display: inline-block;
            background: rgba(0, 100, 255, 0.3);
            padding: 3px 8px;
            border-radius: 3px;
            margin: 2px;
            font-size: 0.9em;
        }
        .issue {
            background: rgba(255, 100, 0, 0.3);
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
        }
        .refresh {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #00ff00;
            color: #000;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }
        .alert {
            position: fixed;
            top: 80px;
            right: 20px;
            background: rgba(0, 255, 0, 0.9);
            color: #000;
            padding: 15px 20px;
            border-radius: 5px;
            font-weight: bold;
            display: none;
        }
    </style>
</head>
<body>
    <button class="refresh" onclick="location.reload()">🔄 Refresh</button>
    <div class="alert" id="alert"></div>

    <div class="container">
        <h1>⚡ TRINITY CENTRAL HUB ⚡</h1>

        <div class="register-panel">
            <h2>🚀 QUICK REGISTER - CLICK YOUR INSTANCE</h2>
            <p style="text-align: center; margin-bottom: 15px;">Each instance clicks their button to register instantly!</p>
            <div class="register-buttons">
                <button class="register-btn" onclick="registerInstance(1)">
                    🤖 Instance 1<br>C1-Mechanic
                </button>
                <button class="register-btn" onclick="registerInstance(2)">
                    🏗️ Instance 2<br>C2-Architect
                </button>
                <button class="register-btn" onclick="registerInstance(3)">
                    🔮 Instance 3<br>C3-Oracle
                </button>
                <button class="register-btn" onclick="registerInstance(4)">
                    ⚙️ Instance 4<br>C4-Specialist
                </button>
                <button class="register-btn" onclick="registerInstance(5)">
                    🔧 Instance 5<br>C5-Specialist
                </button>
                <button class="register-btn" onclick="registerInstance(6)">
                    💡 Instance 6<br>C6-Specialist
                </button>
            </div>
        </div>

        <div id="computers"></div>
    </div>

    <script>
        async function registerInstance(num) {
            const roles = {
                1: 'C1-Mechanic',
                2: 'C2-Architect',
                3: 'C3-Oracle',
                4: 'C4-Specialist',
                5: 'C5-Specialist',
                6: 'C6-Specialist'
            };

            const response = await fetch('/register-instance', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    instance_num: num,
                    role: roles[num]
                })
            });

            const result = await response.json();

            // Show success message
            const alert = document.getElementById('alert');
            alert.textContent = `✅ Instance ${num} registered as ${roles[num]}!`;
            alert.style.display = 'block';
            setTimeout(() => alert.style.display = 'none', 3000);

            // Reload status
            loadStatus();
        }

        async function loadStatus() {
            const response = await fetch('/api/computers');
            const computers = await response.json();

            const container = document.getElementById('computers');
            container.innerHTML = '';

            if (computers.length === 0) {
                container.innerHTML = '<div style="text-align: center; color: #ffff00; padding: 20px;">⏳ Waiting for instances to register...</div>';
                return;
            }

            computers.forEach(comp => {
                const div = document.createElement('div');
                div.className = 'computer';

                const now = new Date();
                const lastSeen = new Date(comp.timestamp);
                const minutes = Math.floor((now - lastSeen) / 60000);
                const isOnline = minutes < 5;

                div.innerHTML = `
                    <h2>${comp.computer_id}</h2>
                    <div class="status ${isOnline ? 'online' : 'offline'}">
                        ${isOnline ? '🟢 ONLINE' : '🔴 OFFLINE'}
                    </div>
                    <div style="margin-top: 10px;">
                        <strong>Role:</strong> ${comp.role || 'Unknown'}<br>
                        <strong>Current Task:</strong> ${comp.current_task || 'None'}<br>
                        <strong>Last Seen:</strong> ${minutes < 1 ? 'Just now' : minutes + ' min ago'}
                    </div>
                    <div style="margin-top: 10px;">
                        <strong>Capabilities:</strong><br>
                        ${comp.capabilities.map(c => `<span class="capability">✅ ${c}</span>`).join('')}
                    </div>
                    ${comp.issues && comp.issues.length > 0 ? `
                        <div class="issue">
                            <strong>⚠️ Issues:</strong><br>
                            ${comp.issues.map(i => `
                                • ${i.name}<br>
                                &nbsp;&nbsp;Fix: ${i.fix}
                            `).join('<br>')}
                        </div>
                    ` : ''}
                `;

                container.appendChild(div);
            });
        }

        loadStatus();
        setInterval(loadStatus, 3000); // Refresh every 3 seconds
    </script>
</body>
</html>
    ''')

@app.route('/api/computers')
def get_computers():
    """Get all computer statuses"""
    computers = load_data(COMPUTERS_FILE)
    return jsonify(computers)

@app.route('/register-instance', methods=['POST'])
def register_instance():
    """Quick register an instance from the dashboard"""
    data = request.json
    instance_num = data['instance_num']
    role = data['role']

    # Create instance data
    instance_data = {
        'computer_id': f'Instance-{instance_num}',
        'role': role,
        'current_task': 'Available',
        'hostname': f'local-instance-{instance_num}',
        'ip': '127.0.0.1',
        'timestamp': datetime.now().isoformat(),
        'capabilities': [
            'Python 3.11',
            'Git',
            'Claude Code',
            'Full Platform Access'
        ],
        'issues': []
    }

    # Load and update computers list
    computers = load_data(COMPUTERS_FILE)

    # Check if already registered
    found = False
    for i, comp in enumerate(computers):
        if comp['computer_id'] == instance_data['computer_id']:
            computers[i] = instance_data
            found = True
            break

    if not found:
        computers.append(instance_data)

    # Save
    save_data(COMPUTERS_FILE, computers)

    print(f"✅ Instance {instance_num} registered as {role}")

    return jsonify({"status": "registered", "instance": instance_num, "role": role})

@app.route('/report', methods=['POST'])
def receive_report():
    """Receive status report from computer"""
    data = request.json

    # Load existing computers
    computers = load_data(COMPUTERS_FILE)

    # Update or add this computer
    computer_id = data['data']['computer_id']
    found = False
    for i, comp in enumerate(computers):
        if comp['computer_id'] == computer_id:
            computers[i] = data['data']
            found = True
            break

    if not found:
        computers.append(data['data'])

    # Save
    save_data(COMPUTERS_FILE, computers)

    print(f"✅ Received report from {computer_id}")

    return jsonify({"status": "received"})

@app.route('/send', methods=['POST'])
def send_message():
    """Send message between computers"""
    message = request.json

    # Save message
    messages = load_data(MESSAGES_FILE)
    messages.append(message)
    save_data(MESSAGES_FILE, messages)

    return jsonify({"status": "sent"})

@app.route('/instructions/<computer_id>')
def get_instructions(computer_id):
    """Get instructions for specific computer"""
    instructions = load_data(INSTRUCTIONS_FILE)

    # Filter for this computer
    comp_instructions = [i for i in instructions if i['target'] == computer_id]

    return jsonify(comp_instructions)

def auto_report_loop():
    """Background thread to auto-report hub status"""
    while True:
        time.sleep(30)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Hub running - {len(load_data(COMPUTERS_FILE))} computers connected")

if __name__ == "__main__":
    print("=" * 60)
    print("⚡ TRINITY CENTRAL HUB STARTING ⚡")
    print("=" * 60)
    print()
    print("Dashboard: http://localhost:8888")
    print("API: http://localhost:8888/api/computers")
    print()
    print("Waiting for computers to report...")
    print("=" * 60)
    print()

    # Start background reporter
    reporter = threading.Thread(target=auto_report_loop, daemon=True)
    reporter.start()

    # Start Flask server
    app.run(host='0.0.0.0', port=8888, debug=False)
