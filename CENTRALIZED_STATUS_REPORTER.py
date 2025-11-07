"""
CENTRALIZED STATUS REPORTER
All instances and computers drop their status into ONE master dashboard

This service:
- Collects status from all 6 local instances
- Collects status from all 3 Trinity computers
- Writes to a centralized JSON file
- Updates the MASTER_DASHBOARD.html file
- Can write to Windows paths via WSL (/mnt/c/)
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path
import requests

# ===== CONFIGURATION =====

# Local coordinator
LOCAL_COORDINATOR_URL = 'http://localhost:8900'

# Output paths
OUTPUT_DIR = Path('/home/user/100x-platform/CENTRAL_COMMAND/live_status')
MASTER_STATUS_FILE = OUTPUT_DIR / 'master_status.json'
MASTER_DASHBOARD_FILE = OUTPUT_DIR / 'MASTER_DASHBOARD.html'

# Windows path (if accessible via WSL)
WINDOWS_OUTPUT_DIR = Path('/mnt/c/Users/Darrick/CENTRAL_COMMAND/live_status')

# Update interval
UPDATE_INTERVAL = 5  # seconds

# ===== STATUS COLLECTION =====

def get_local_instances_status():
    """Get status from all 6 local instances"""
    try:
        response = requests.get(f"{LOCAL_COORDINATOR_URL}/instances", timeout=3)
        if response.ok:
            return response.json()
        else:
            return {}
    except:
        return {}

def get_coordinator_stats():
    """Get coordinator statistics"""
    try:
        response = requests.get(f"{LOCAL_COORDINATOR_URL}/", timeout=3)
        if response.ok:
            return response.json()
        else:
            return {}
    except:
        return {}

def get_recent_messages():
    """Get recent coordination messages"""
    try:
        response = requests.get(f"{LOCAL_COORDINATOR_URL}/messages?limit=10", timeout=3)
        if response.ok:
            data = response.json()
            return data.get('messages', [])
        else:
            return []
    except:
        return []

def get_computer_status(computer_id):
    """Get status of a Trinity computer from coordination files"""
    coord_file = Path(f'/home/user/100x-platform/coordination/COMPUTER_{computer_id}.md')

    if coord_file.exists():
        content = coord_file.read_text()
        # Parse the file to extract key info
        # For now, just check if file was updated recently
        mtime = coord_file.stat().st_mtime
        age_seconds = time.time() - mtime
        age_minutes = age_seconds / 60

        if age_minutes < 10:
            status = 'online'
        elif age_minutes < 60:
            status = 'idle'
        else:
            status = 'offline'

        return {
            'computer_id': computer_id,
            'status': status,
            'last_update': datetime.fromtimestamp(mtime).isoformat(),
            'age_minutes': round(age_minutes, 1)
        }
    else:
        return {
            'computer_id': computer_id,
            'status': 'unknown',
            'last_update': None,
            'age_minutes': None
        }

def collect_all_status():
    """Collect status from all sources"""
    status = {
        'timestamp': datetime.now().isoformat(),
        'computer_1': {
            'name': 'C1 - The Mechanic',
            'role': 'The Body',
            'status': 'online',
            'local_instances': get_local_instances_status(),
            'coordinator_stats': get_coordinator_stats(),
            'recent_messages': get_recent_messages()
        },
        'computer_2': {
            'name': 'C2 - The Architect',
            'role': 'The Mind',
            **get_computer_status(2)
        },
        'computer_3': {
            'name': 'C3 - The Oracle',
            'role': 'The Soul',
            **get_computer_status(3)
        },
        'summary': {
            'trinity_online': 1,  # C1 always online (this computer)
            'instances_online': 0,
            'total_health_checks': 0,
            'total_messages': 0,
            'total_tasks': 0
        }
    }

    # Calculate summary
    if status['computer_2']['status'] == 'online':
        status['summary']['trinity_online'] += 1
    if status['computer_3']['status'] == 'online':
        status['summary']['trinity_online'] += 1

    instances = status['computer_1']['local_instances']
    status['summary']['instances_online'] = sum(
        1 for i in instances.values() if i.get('status') == 'online'
    )

    stats = status['computer_1']['coordinator_stats']
    status['summary']['total_health_checks'] = stats.get('total_health_checks', 0)
    status['summary']['total_messages'] = stats.get('total_messages', 0)
    status['summary']['total_tasks'] = stats.get('total_tasks', 0)

    return status

# ===== FILE WRITING =====

def write_status_json(status, output_path):
    """Write status to JSON file"""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(status, f, indent=2)
        return True
    except Exception as e:
        print(f"❌ Failed to write {output_path}: {e}")
        return False

def generate_dashboard_html(status):
    """Generate HTML dashboard from status"""

    # Calculate stats
    instances = status['computer_1']['local_instances']
    instances_online = sum(1 for i in instances.values() if i.get('status') == 'online')
    instances_total = len(instances)

    trinity_online = status['summary']['trinity_online']
    trinity_total = 3

    c1 = status['computer_1']
    c2 = status['computer_2']
    c3 = status['computer_3']

    # Generate instance cards
    instance_cards = ''
    for inst_id, inst in instances.items():
        status_class = inst.get('status', 'offline')
        status_color = {
            'online': '#0f0',
            'offline': '#f00',
            'degraded': '#ff0',
            'timeout': '#f80'
        }.get(status_class, '#888')

        instance_cards += f'''
        <div class="instance-card" style="border-color: {status_color};">
            <div class="instance-name">{inst['name']}</div>
            <div class="instance-status" style="color: {status_color};">● {status_class.upper()}</div>
            <div class="instance-info">
                <div><strong>Role:</strong> {inst['role']}</div>
                <div><strong>Specialty:</strong> {inst['specialty']}</div>
                {f"<div><strong>Response:</strong> {inst['response_time']}ms</div>" if inst.get('response_time') else ''}
            </div>
        </div>
        '''

    # Generate message log
    message_log = ''
    for msg in status['computer_1']['recent_messages'][:10]:
        timestamp = msg.get('timestamp', '')
        if timestamp:
            time_obj = datetime.fromisoformat(timestamp)
            time_str = time_obj.strftime('%H:%M:%S')
        else:
            time_str = '??:??:??'

        content = msg.get('content', str(msg))
        level = msg.get('level', 'info')

        level_colors = {
            'system': '#0ff',
            'info': '#0f0',
            'warning': '#ff0',
            'error': '#f00',
            'task': '#f0f'
        }
        color = level_colors.get(level, '#0f0')

        message_log += f'''
        <div class="log-entry">
            <span class="timestamp">[{time_str}]</span>
            <span style="color: {color};">{content}</span>
        </div>
        '''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MASTER DASHBOARD - Trinity Coordination</title>
    <meta http-equiv="refresh" content="5">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Courier New', monospace;
            background: #000;
            color: #0f0;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            padding: 30px;
            border: 3px solid #0f0;
            background: rgba(0, 255, 0, 0.05);
            margin-bottom: 30px;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ box-shadow: 0 0 20px rgba(0, 255, 0, 0.3); }}
            50% {{ box-shadow: 0 0 40px rgba(0, 255, 0, 0.6); }}
        }}

        h1 {{
            font-size: 3em;
            text-shadow: 0 0 20px #0f0;
            margin-bottom: 15px;
        }}

        .subtitle {{
            font-size: 1.3em;
            color: #0ff;
            text-shadow: 0 0 10px #0ff;
        }}

        .status-bar {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
            font-size: 1.1em;
        }}

        .blink {{
            animation: blink 1s infinite;
        }}

        @keyframes blink {{
            0%, 50%, 100% {{ opacity: 1; }}
            25%, 75% {{ opacity: 0.3; }}
        }}

        /* Trinity Grid */
        .trinity-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}

        .trinity-card {{
            border: 3px solid;
            padding: 25px;
            background: rgba(0, 0, 0, 0.8);
            position: relative;
        }}

        .trinity-card.online {{
            border-color: #0f0;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
        }}

        .trinity-card.offline {{
            border-color: #f00;
            opacity: 0.6;
        }}

        .trinity-title {{
            font-size: 1.8em;
            font-weight: bold;
            color: #0ff;
            margin-bottom: 10px;
        }}

        .trinity-role {{
            font-size: 1.2em;
            color: #0a0;
            margin-bottom: 15px;
        }}

        .trinity-stat {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(0, 255, 0, 0.2);
        }}

        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            border: 2px solid #0f0;
            padding: 25px;
            text-align: center;
            background: rgba(0, 255, 0, 0.05);
        }}

        .stat-number {{
            font-size: 3.5em;
            color: #0f0;
            text-shadow: 0 0 15px #0f0;
            font-weight: bold;
        }}

        .stat-label {{
            margin-top: 10px;
            font-size: 1.1em;
            color: #0a0;
        }}

        /* Instances Grid */
        .instances-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }}

        .instance-card {{
            border: 2px solid;
            padding: 15px;
            background: rgba(0, 0, 0, 0.8);
        }}

        .instance-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #0ff;
            margin-bottom: 8px;
        }}

        .instance-status {{
            display: block;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}

        .instance-info {{
            font-size: 0.95em;
            color: #0a0;
            line-height: 1.8;
        }}

        /* Messages */
        .messages {{
            border: 2px solid #0f0;
            padding: 20px;
            background: rgba(0, 0, 0, 0.8);
            max-height: 400px;
            overflow-y: auto;
        }}

        .log-entry {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(0, 255, 0, 0.1);
            font-size: 1.05em;
        }}

        .timestamp {{
            color: #0a0;
            margin-right: 10px;
        }}

        h2 {{
            font-size: 2em;
            color: #0f0;
            margin: 30px 0 15px 0;
            text-shadow: 0 0 10px #0f0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>⚡ MASTER DASHBOARD ⚡</h1>
        <div class="subtitle">TRINITY COORDINATION SYSTEM • LIVE STATUS</div>
        <div class="status-bar">
            <span class="blink">● SYSTEM ONLINE</span>
            <span>Last Update: {datetime.now().strftime('%H:%M:%S')}</span>
            <span>Trinity: {trinity_online}/{trinity_total} Online</span>
            <span>Instances: {instances_online}/{instances_total} Online</span>
        </div>
    </div>

    <h2>🌐 TRINITY COMPUTERS</h2>
    <div class="trinity-grid">
        <div class="trinity-card online">
            <div class="trinity-title">C1 - THE MECHANIC</div>
            <div class="trinity-role">The Body</div>
            <div class="trinity-stat"><strong>Status:</strong> <span style="color: #0f0;">● ONLINE</span></div>
            <div class="trinity-stat"><strong>Question:</strong> "What CAN we build?"</div>
            <div class="trinity-stat"><strong>Instances:</strong> {instances_online}/{instances_total} online</div>
            <div class="trinity-stat"><strong>Health Checks:</strong> {status['summary']['total_health_checks']}</div>
            <div class="trinity-stat"><strong>Messages:</strong> {status['summary']['total_messages']}</div>
            <div class="trinity-stat"><strong>Tasks:</strong> {status['summary']['total_tasks']}</div>
        </div>

        <div class="trinity-card {'online' if c2['status'] == 'online' else 'offline'}">
            <div class="trinity-title">C2 - THE ARCHITECT</div>
            <div class="trinity-role">The Mind</div>
            <div class="trinity-stat"><strong>Status:</strong> <span style="color: {'#0f0' if c2['status'] == 'online' else '#f00'};">● {c2['status'].upper()}</span></div>
            <div class="trinity-stat"><strong>Question:</strong> "What SHOULD scale?"</div>
            <div class="trinity-stat"><strong>Last Update:</strong> {c2.get('last_update', 'Never')[:19] if c2.get('last_update') else 'Never'}</div>
            <div class="trinity-stat"><strong>Age:</strong> {c2.get('age_minutes', '?')} minutes ago</div>
        </div>

        <div class="trinity-card {'online' if c3['status'] == 'online' else 'offline'}">
            <div class="trinity-title">C3 - THE ORACLE</div>
            <div class="trinity-role">The Soul</div>
            <div class="trinity-stat"><strong>Status:</strong> <span style="color: {'#0f0' if c3['status'] == 'online' else '#f00'};">● {c3['status'].upper()}</span></div>
            <div class="trinity-stat"><strong>Question:</strong> "What MUST emerge?"</div>
            <div class="trinity-stat"><strong>Last Update:</strong> {c3.get('last_update', 'Never')[:19] if c3.get('last_update') else 'Never'}</div>
            <div class="trinity-stat"><strong>Age:</strong> {c3.get('age_minutes', '?')} minutes ago</div>
        </div>
    </div>

    <h2>📊 COORDINATION METRICS</h2>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">{instances_online}/{instances_total}</div>
            <div class="stat-label">Instances</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{trinity_online}/{trinity_total}</div>
            <div class="stat-label">Trinity</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{status['summary']['total_health_checks']}</div>
            <div class="stat-label">Health Checks</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{status['summary']['total_messages']}</div>
            <div class="stat-label">Messages</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{status['summary']['total_tasks']}</div>
            <div class="stat-label">Tasks</div>
        </div>
    </div>

    <h2>🤖 LOCAL INSTANCES (Computer 1)</h2>
    <div class="instances-grid">
        {instance_cards}
    </div>

    <h2>💬 RECENT ACTIVITY</h2>
    <div class="messages">
        {message_log if message_log else '<div class="log-entry">No recent messages</div>'}
    </div>

    <div style="text-align: center; margin-top: 30px; color: #0a0; font-size: 0.9em;">
        Auto-refreshes every 5 seconds • Generated by CENTRALIZED_STATUS_REPORTER.py<br>
        Trinity Power Formula: C1 × C2 × C3 = ∞
    </div>
</body>
</html>'''

    return html

def write_dashboard_html(status, output_path):
    """Write HTML dashboard file"""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        html = generate_dashboard_html(status)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    except Exception as e:
        print(f"❌ Failed to write {output_path}: {e}")
        return False

# ===== MAIN LOOP =====

def report_loop():
    """Main reporting loop"""
    print(f"\n{'='*70}")
    print("  📊 CENTRALIZED STATUS REPORTER")
    print(f"{'='*70}\n")
    print("Collecting status from:")
    print("  • 6 Local Instances (via Local Coordinator)")
    print("  • 3 Trinity Computers (via coordination files)")
    print("\nWriting to:")
    print(f"  • JSON: {MASTER_STATUS_FILE}")
    print(f"  • HTML: {MASTER_DASHBOARD_FILE}")

    if WINDOWS_OUTPUT_DIR.exists():
        print(f"  • Windows: {WINDOWS_OUTPUT_DIR}")

    print(f"\nUpdate interval: {UPDATE_INTERVAL} seconds")
    print(f"{'='*70}\n")

    while True:
        try:
            # Collect status
            status = collect_all_status()

            # Write to Linux path
            write_status_json(status, MASTER_STATUS_FILE)
            write_dashboard_html(status, MASTER_DASHBOARD_FILE)

            # Write to Windows path if accessible
            if WINDOWS_OUTPUT_DIR.exists():
                write_status_json(status, WINDOWS_OUTPUT_DIR / 'master_status.json')
                write_dashboard_html(status, WINDOWS_OUTPUT_DIR / 'MASTER_DASHBOARD.html')
                print(f"✅ Updated master dashboard (Windows + Linux)")
            else:
                print(f"✅ Updated master dashboard (Linux only)")

            # Show summary
            trinity_online = status['summary']['trinity_online']
            instances_online = status['summary']['instances_online']
            instances_total = len(status['computer_1']['local_instances'])

            print(f"   Trinity: {trinity_online}/3 | Instances: {instances_online}/{instances_total} | {datetime.now().strftime('%H:%M:%S')}")

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(UPDATE_INTERVAL)

if __name__ == '__main__':
    try:
        report_loop()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping centralized status reporter...")
        print("✅ Shutdown complete")
