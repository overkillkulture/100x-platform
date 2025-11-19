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
    </style>
</head>
<body>
    <button class="refresh" onclick="location.reload()">🔄 Refresh</button>

    <div class="container">
        <h1>⚡ TRINITY CENTRAL HUB ⚡</h1>

        <div id="computers"></div>
    </div>

    <script>
        async function loadStatus() {
            const response = await fetch('/api/computers');
            const computers = await response.json();

            const container = document.getElementById('computers');
            container.innerHTML = '';

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
                        <strong>Hostname:</strong> ${comp.hostname}<br>
                        <strong>IP:</strong> ${comp.ip}<br>
                        <strong>Last Seen:</strong> ${minutes} min ago
                    </div>
                    <div style="margin-top: 10px;">
                        <strong>Capabilities:</strong><br>
                        ${comp.capabilities.map(c => `<span class="capability">✅ ${c}</span>`).join('')}
                    </div>
                    ${comp.issues.length > 0 ? `
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
        setInterval(loadStatus, 5000); // Refresh every 5 seconds
    </script>
</body>
</html>
    ''')

@app.route('/api/computers')
def get_computers():
    """Get all computer statuses"""
    computers = load_data(COMPUTERS_FILE)
    return jsonify(computers)

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
