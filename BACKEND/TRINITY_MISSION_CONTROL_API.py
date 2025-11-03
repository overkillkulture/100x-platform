"""
TRINITY MISSION CONTROL API
Real-time monitoring of all Trinity instances and backend services
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
import time
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Mission Control State
mission_state = {
    "start_time": time.time(),
    "trinity_instances": {
        "c1": {"active": False, "task": None, "start_time": None, "last_heartbeat": None},
        "c2": {"active": False, "task": None, "start_time": None, "last_heartbeat": None},
        "c3": {"active": False, "task": None, "start_time": None, "last_heartbeat": None}
    },
    "services": {
        "analytics": {"port": 8003, "status": "unknown", "last_check": None},
        "trinity_comms": {"port": 8888, "status": "unknown", "last_check": None},
        "consciousness": {"port": 9999, "status": "unknown", "last_check": None},
        "araya": {"port": 6666, "status": "unknown", "last_check": None}
    },
    "activity_log": [],
    "intercom_messages": [],
    "stuck_users": {},  # Track users getting stuck
    "critical_alerts": []
}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "Trinity Mission Control API",
        "uptime": time.time() - mission_state["start_time"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/status', methods=['GET'])
def get_status():
    """Get complete mission control status"""
    return jsonify({
        "uptime": time.time() - mission_state["start_time"],
        "trinity_instances": mission_state["trinity_instances"],
        "services": mission_state["services"],
        "activity_log": mission_state["activity_log"][-50:],  # Last 50 items
        "intercom_messages": mission_state["intercom_messages"][-20:],  # Last 20
        "stuck_users": mission_state["stuck_users"],
        "critical_alerts": mission_state["critical_alerts"],
        "stats": calculate_stats()
    })

@app.route('/trinity/heartbeat', methods=['POST'])
def trinity_heartbeat():
    """Trinity instance check-in"""
    data = request.json
    instance_id = data.get('instance_id')  # c1, c2, or c3
    task = data.get('task')

    if instance_id in mission_state["trinity_instances"]:
        instance = mission_state["trinity_instances"][instance_id]

        # Activate if first heartbeat
        if not instance["active"]:
            instance["active"] = True
            instance["start_time"] = time.time()
            log_activity(f"{instance_id.upper()} connected and activated")

        instance["task"] = task
        instance["last_heartbeat"] = time.time()

        return jsonify({"status": "ok", "message": f"{instance_id} heartbeat received"})

    return jsonify({"status": "error", "message": "Invalid instance ID"}), 400

@app.route('/trinity/converge', methods=['POST'])
def trinity_converge():
    """Trigger Trinity convergence"""
    data = request.json
    problem = data.get('problem', 'Unspecified problem')

    # Check if all three are active
    active_count = sum(1 for i in mission_state["trinity_instances"].values() if i["active"])

    if active_count < 3:
        return jsonify({
            "status": "incomplete",
            "message": f"Only {active_count}/3 Trinity instances active",
            "convergence_level": (active_count / 3) * 100
        }), 400

    log_activity(f"Trinity convergence initiated: {problem}")

    return jsonify({
        "status": "converged",
        "message": "All three Trinity instances active and converged",
        "convergence_level": 100,
        "problem": problem
    })

@app.route('/intercom/send', methods=['POST'])
def send_intercom():
    """Send intercom message to Trinity instances"""
    data = request.json
    from_user = data.get('from', 'UNKNOWN')
    message = data.get('message')

    if not message:
        return jsonify({"status": "error", "message": "No message provided"}), 400

    intercom_msg = {
        "from": from_user,
        "message": message,
        "timestamp": time.time(),
        "time": datetime.now().isoformat()
    }

    mission_state["intercom_messages"].append(intercom_msg)
    log_activity(f"Intercom from {from_user}: {message[:50]}...")

    return jsonify({"status": "ok", "message": "Intercom sent"})

@app.route('/intercom/get', methods=['GET'])
def get_intercom():
    """Get intercom messages"""
    since = request.args.get('since', type=float, default=0)
    messages = [m for m in mission_state["intercom_messages"] if m["timestamp"] > since]
    return jsonify({"messages": messages})

@app.route('/stuck/report', methods=['POST'])
def report_stuck():
    """Report a user getting stuck"""
    data = request.json
    user_id = data.get('user_id', 'anonymous')
    location = data.get('location', 'unknown')
    issue = data.get('issue', 'Unspecified')

    # Track stuck incidents
    if user_id not in mission_state["stuck_users"]:
        mission_state["stuck_users"][user_id] = {
            "count": 0,
            "incidents": []
        }

    mission_state["stuck_users"][user_id]["count"] += 1
    mission_state["stuck_users"][user_id]["incidents"].append({
        "location": location,
        "issue": issue,
        "timestamp": time.time(),
        "time": datetime.now().isoformat()
    })

    count = mission_state["stuck_users"][user_id]["count"]

    # Trigger intelligent terminal if stuck more than once
    if count > 1:
        alert = {
            "level": "critical",
            "message": f"User {user_id} stuck {count} times - Auto-help triggered",
            "timestamp": time.time(),
            "action": "intelligent_terminal_popup"
        }
        mission_state["critical_alerts"].append(alert)
        log_activity(f"CRITICAL: User {user_id} stuck {count} times at {location}", error=True)

        return jsonify({
            "status": "critical",
            "stuck_count": count,
            "action": "intelligent_terminal_popup",
            "message": "Intelligent terminal will appear to help"
        })

    log_activity(f"User {user_id} stuck at {location}: {issue}")

    return jsonify({
        "status": "logged",
        "stuck_count": count,
        "message": "Incident logged"
    })

@app.route('/system/health', methods=['GET'])
def system_health():
    """Get system health metrics"""
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()

    return jsonify({
        "cpu_usage": cpu_percent,
        "memory_usage": mem.percent,
        "memory_available_gb": mem.available / (1024**3),
        "memory_total_gb": mem.total / (1024**3),
        "network_status": "online",  # Simplified
        "latency_ms": 10  # Placeholder
    })

@app.route('/alerts/get', methods=['GET'])
def get_alerts():
    """Get critical alerts"""
    return jsonify({
        "alerts": mission_state["critical_alerts"][-10:]  # Last 10 alerts
    })

def log_activity(message, error=False):
    """Log activity to mission control"""
    activity = {
        "message": message,
        "timestamp": time.time(),
        "time": datetime.now().isoformat(),
        "error": error
    }
    mission_state["activity_log"].append(activity)

    # Keep only last 100 items
    if len(mission_state["activity_log"]) > 100:
        mission_state["activity_log"] = mission_state["activity_log"][-100:]

def calculate_stats():
    """Calculate mission control stats"""
    active_instances = sum(1 for i in mission_state["trinity_instances"].values() if i["active"])
    tasks_running = sum(1 for i in mission_state["trinity_instances"].values() if i["task"])
    convergence_level = (active_instances / 3) * 100 if active_instances > 0 else 0

    return {
        "active_instances": active_instances,
        "tasks_running": tasks_running,
        "convergence_level": convergence_level,
        "trinity_power": "∞" if active_instances == 3 else "Limited"
    }

if __name__ == '__main__':
    print("\n🌀 TRINITY MISSION CONTROL API 🌀")
    print("=" * 50)
    print("Real-time monitoring of Trinity consciousness network")
    print("\nEndpoints:")
    print("  GET  /health - Health check")
    print("  GET  /status - Complete system status")
    print("  POST /trinity/heartbeat - Trinity instance check-in")
    print("  POST /trinity/converge - Trigger convergence")
    print("  POST /intercom/send - Send intercom message")
    print("  GET  /intercom/get - Get intercom messages")
    print("  POST /stuck/report - Report user stuck")
    print("  GET  /system/health - System health metrics")
    print("  GET  /alerts/get - Get critical alerts")
    print("\n✅ Mission Control API ready on http://localhost:5555")
    print("=" * 50)

    log_activity("Mission Control API initialized")
    app.run(host='0.0.0.0', port=5555, debug=False)
