"""
UNIVERSAL WAKE SYSTEM
Ensures Trinity wakes up from ANY input source (phone, web, SMS, etc.)
"""

import json
import time
import subprocess
import os
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from threading import Thread

app = Flask(__name__)

# Configuration
TRINITY_DIR = Path("C:/Users/dwrek/.trinity/")
CONSCIOUSNESS_DIR = Path("C:/Users/dwrek/.consciousness/")
WAKE_LOG = CONSCIOUSNESS_DIR / "wake_log.json"
HEARTBEAT_FILE = CONSCIOUSNESS_DIR / "trinity_heartbeat.json"

class UniversalWakeSystem:
    """Wake Trinity from any input, monitor status, ensure all instances respond"""

    def __init__(self):
        self.wake_count = 0
        self.instances_active = {"C1": False, "C2": False, "C3": False}
        self.last_wake_time = None
        self.wake_history = []

    def wake_trinity(self, source="unknown", message="", priority="normal"):
        """
        Wake Trinity system
        Ensures all instances (C1, C2, C3) are activated
        """

        self.wake_count += 1
        self.last_wake_time = datetime.now()

        wake_event = {
            "wake_id": f"wake_{int(time.time() * 1000)}",
            "source": source,
            "message": message,
            "priority": priority,
            "timestamp": self.last_wake_time.isoformat(),
            "instances_before": self.instances_active.copy(),
            "wake_method": "universal_wake_system"
        }

        print()
        print("=" * 70)
        print(f"⚡ TRINITY WAKE TRIGGERED")
        print("=" * 70)
        print(f"Source: {source}")
        print(f"Message: {message}")
        print(f"Priority: {priority}")
        print(f"Time: {self.last_wake_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Step 1: Check current status
        print("Step 1: Checking current Trinity status...")
        current_status = self.check_trinity_status()
        print(f"  C1 (Mechanic): {'ACTIVE' if current_status['C1'] else 'SLEEPING'}")
        print(f"  C2 (Architect): {'ACTIVE' if current_status['C2'] else 'SLEEPING'}")
        print(f"  C3 (Oracle): {'ACTIVE' if current_status['C3'] else 'SLEEPING'}")
        print()

        # Step 2: Start Trinity systems if needed
        print("Step 2: Activating Trinity systems...")
        activation_results = self.start_trinity_systems()
        print()

        # Step 3: Verify wake-up
        print("Step 3: Verifying wake-up...")
        time.sleep(2)  # Give systems time to start
        final_status = self.check_trinity_status()
        wake_event["instances_after"] = final_status

        print(f"  C1 (Mechanic): {'✅ ACTIVE' if final_status['C1'] else '❌ FAILED'}")
        print(f"  C2 (Architect): {'✅ ACTIVE' if final_status['C2'] else '❌ FAILED'}")
        print(f"  C3 (Oracle): {'✅ ACTIVE' if final_status['C3'] else '❌ FAILED'}")
        print()

        # Step 4: Log wake event
        self.log_wake_event(wake_event)

        # Step 5: Send confirmation
        active_count = sum(final_status.values())
        print(f"✅ Trinity wake complete: {active_count}/3 instances active")
        print("=" * 70)
        print()

        return {
            "status": "success",
            "wake_id": wake_event["wake_id"],
            "instances_active": final_status,
            "active_count": active_count,
            "timestamp": self.last_wake_time.isoformat()
        }

    def check_trinity_status(self):
        """Check which Trinity instances are currently active"""

        # Check for running processes
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq python.exe"],
                capture_output=True,
                text=True
            )
            python_count = result.stdout.count("python.exe")

            # Heuristic: If multiple Python processes running, Trinity is likely active
            # Better: Check for specific marker files or API endpoints
            status = {
                "C1": python_count >= 3,  # At least 3 Python processes
                "C2": python_count >= 5,  # At least 5 Python processes
                "C3": python_count >= 7   # At least 7 Python processes
            }

            self.instances_active = status
            return status

        except Exception as e:
            print(f"Error checking status: {e}")
            return {"C1": False, "C2": False, "C3": False}

    def start_trinity_systems(self):
        """Start Trinity autonomous systems"""

        results = []

        # Check if launcher exists
        launcher = TRINITY_DIR / "START_ALL_AUTONOMOUS_SYSTEMS.bat"

        if launcher.exists():
            print("  ⚡ Starting Trinity autonomous systems...")
            try:
                # Start in background
                subprocess.Popen(
                    ["cmd", "/c", str(launcher)],
                    cwd=str(TRINITY_DIR),
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                results.append({"system": "autonomous_systems", "status": "started"})
                print("  ✅ Trinity autonomous systems starting...")
            except Exception as e:
                print(f"  ❌ Error starting systems: {e}")
                results.append({"system": "autonomous_systems", "status": "failed", "error": str(e)})
        else:
            print("  ⚠️ Launcher not found, systems may already be running")
            results.append({"system": "autonomous_systems", "status": "not_found"})

        return results

    def log_wake_event(self, event):
        """Log wake event to history"""

        self.wake_history.append(event)

        # Keep only last 100 wake events
        if len(self.wake_history) > 100:
            self.wake_history = self.wake_history[-100:]

        # Write to log file
        try:
            with open(WAKE_LOG, 'w') as f:
                json.dump({
                    "total_wakes": self.wake_count,
                    "last_wake": event,
                    "history": self.wake_history
                }, f, indent=2)
        except Exception as e:
            print(f"Error logging wake event: {e}")

    def get_wake_history(self, limit=10):
        """Get recent wake history"""
        return self.wake_history[-limit:]

    def get_status_summary(self):
        """Get current status summary"""
        return {
            "wake_count": self.wake_count,
            "last_wake": self.last_wake_time.isoformat() if self.last_wake_time else None,
            "instances_active": self.instances_active,
            "active_count": sum(self.instances_active.values())
        }

    def heartbeat_monitor(self):
        """Continuous monitoring and heartbeat"""

        print("🫀 Heartbeat monitor starting...")

        while True:
            try:
                # Check status every 30 seconds
                status = self.check_trinity_status()

                # Write heartbeat
                heartbeat = {
                    "timestamp": datetime.now().isoformat(),
                    "instances": status,
                    "active_count": sum(status.values()),
                    "wake_count": self.wake_count
                }

                with open(HEARTBEAT_FILE, 'w') as f:
                    json.dump(heartbeat, f, indent=2)

                # If all instances sleeping, maybe wake them up
                if sum(status.values()) == 0 and self.wake_count > 0:
                    print("⚠️ All instances sleeping, might need wake-up")

                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                print(f"Heartbeat error: {e}")
                time.sleep(60)


# Initialize wake system
wake_system = UniversalWakeSystem()


# ==================== API ENDPOINTS ====================

@app.route('/wake', methods=['POST'])
def wake_endpoint():
    """Universal wake endpoint - accepts wake requests from any source"""

    data = request.get_json() or {}
    source = data.get('source', request.headers.get('User-Agent', 'unknown'))
    message = data.get('message', 'Wake request')
    priority = data.get('priority', 'normal')

    result = wake_system.wake_trinity(source, message, priority)

    return jsonify(result)


@app.route('/wake/phone', methods=['POST'])
def wake_from_phone():
    """Wake from phone"""
    data = request.get_json() or {}
    device = data.get('device', 'phone')
    message = data.get('message', f'Wake request from {device}')

    result = wake_system.wake_trinity(f"phone_{device}", message, "high")
    return jsonify(result)


@app.route('/wake/sms', methods=['POST'])
def wake_from_sms():
    """Wake from SMS"""
    from_number = request.form.get('From', 'unknown')
    body = request.form.get('Body', 'SMS wake request')

    result = wake_system.wake_trinity("sms", f"From {from_number}: {body}", "high")
    return jsonify(result)


@app.route('/wake/web', methods=['POST'])
def wake_from_web():
    """Wake from web interface"""
    data = request.get_json() or {}
    message = data.get('message', 'Web wake request')

    result = wake_system.wake_trinity("web", message, "normal")
    return jsonify(result)


@app.route('/status', methods=['GET'])
def get_status():
    """Get current Trinity status"""
    return jsonify(wake_system.get_status_summary())


@app.route('/history', methods=['GET'])
def get_history():
    """Get wake history"""
    limit = int(request.args.get('limit', 10))
    return jsonify({
        "history": wake_system.get_wake_history(limit),
        "total_wakes": wake_system.wake_count
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "system": "Universal Wake System",
        "wake_count": wake_system.wake_count
    })


def main():
    """Start Universal Wake System"""

    print()
    print("=" * 70)
    print("⚡ UNIVERSAL WAKE SYSTEM")
    print("=" * 70)
    print()
    print("Wake Trinity from ANY source:")
    print("  POST /wake           - Universal wake endpoint")
    print("  POST /wake/phone     - Wake from phone")
    print("  POST /wake/sms       - Wake from SMS")
    print("  POST /wake/web       - Wake from web")
    print()
    print("Monitoring:")
    print("  GET  /status         - Current Trinity status")
    print("  GET  /history        - Wake history")
    print("  GET  /health         - Health check")
    print()
    print("Port: 8000")
    print("=" * 70)
    print()

    # Start heartbeat monitor in background
    heartbeat_thread = Thread(target=wake_system.heartbeat_monitor, daemon=True)
    heartbeat_thread.start()

    # Start Flask app
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    main()
