"""
UNIVERSAL INPUT SYSTEM
Everything is an input - Trinity accepts commands from ANY source
ChatGPT, Claude Code, Phone, Web, SMS, Email, GitHub, etc.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from threading import Thread
import os

# Configuration
TRINITY_DIR = Path("C:/Users/dwrek/.trinity/")
INPUT_QUEUE_DIR = Path("C:/Users/dwrek/.consciousness/input_queue/")
INPUT_QUEUE_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)


class UniversalInputSystem:
    """
    Accept input from ANY source and route to Trinity
    ChatGPT → Claude Code → Phone → Web → SMS → Email → GitHub → Trinity
    """

    def __init__(self):
        self.input_sources = {
            "chatgpt": {"enabled": True, "count": 0},
            "claude_code": {"enabled": True, "count": 0},
            "phone": {"enabled": True, "count": 0},
            "web": {"enabled": True, "count": 0},
            "sms": {"enabled": True, "count": 0},
            "email": {"enabled": True, "count": 0},
            "github": {"enabled": True, "count": 0},
            "api": {"enabled": True, "count": 0}
        }

    def receive_input(self, source, command, data=None, priority="normal"):
        """
        Universal input receiver - accepts from ANY source
        """

        input_id = f"{source}_{int(time.time() * 1000)}"

        input_obj = {
            "input_id": input_id,
            "source": source,
            "command": command,
            "data": data or {},
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "processed": False
        }

        # Write to input queue
        input_file = INPUT_QUEUE_DIR / f"{input_id}.json"
        with open(input_file, 'w') as f:
            json.dump(input_obj, f, indent=2)

        # Update source count
        if source in self.input_sources:
            self.input_sources[source]["count"] += 1

        print(f"✅ [{source.upper()}] Input received: {command}")

        return input_id

    def process_input_queue(self):
        """
        Process all pending inputs and send to Trinity
        """

        pending_inputs = sorted(INPUT_QUEUE_DIR.glob("*.json"))

        for input_file in pending_inputs:
            try:
                with open(input_file, 'r') as f:
                    input_obj = json.load(f)

                if input_obj.get("processed"):
                    continue

                # Process input
                result = self.route_to_trinity(input_obj)

                # Mark as processed
                input_obj["processed"] = True
                input_obj["result"] = result
                input_obj["processed_at"] = datetime.now().isoformat()

                with open(input_file, 'w') as f:
                    json.dump(input_obj, f, indent=2)

                print(f"✅ Processed: {input_obj['input_id']}")

            except Exception as e:
                print(f"❌ Error processing {input_file}: {e}")

    def route_to_trinity(self, input_obj):
        """
        Route input to appropriate Trinity instance
        """

        command = input_obj.get("command")
        source = input_obj.get("source")

        # Create Trinity command file
        trinity_command = {
            "command": command,
            "source": source,
            "data": input_obj.get("data", {}),
            "timestamp": datetime.now().isoformat(),
            "input_id": input_obj["input_id"]
        }

        # Write to Trinity command hub
        command_file = TRINITY_DIR / "UNIVERSAL_INPUT_COMMAND.json"
        with open(command_file, 'w') as f:
            json.dump(trinity_command, f, indent=2)

        return {"status": "routed_to_trinity", "command_file": str(command_file)}

    def get_all_inputs(self, limit=50):
        """Get recent inputs from all sources"""

        inputs = []
        for input_file in sorted(INPUT_QUEUE_DIR.glob("*.json"), reverse=True)[:limit]:
            try:
                with open(input_file, 'r') as f:
                    inputs.append(json.load(f))
            except:
                pass

        return inputs

    def get_source_stats(self):
        """Get statistics per input source"""
        return self.input_sources


# Initialize system
input_system = UniversalInputSystem()


# ==================== API ENDPOINTS ====================

@app.route('/input/chatgpt', methods=['POST'])
def chatgpt_input():
    """Accept input from ChatGPT"""

    data = request.get_json()
    command = data.get('command', '')
    input_data = data.get('data', {})
    priority = data.get('priority', 'normal')

    input_id = input_system.receive_input('chatgpt', command, input_data, priority)

    return jsonify({
        "status": "received",
        "input_id": input_id,
        "source": "chatgpt",
        "message": "Input queued for Trinity processing"
    })


@app.route('/input/claude', methods=['POST'])
def claude_input():
    """Accept input from Claude Code"""

    data = request.get_json()
    command = data.get('command', '')
    input_data = data.get('data', {})
    priority = data.get('priority', 'normal')

    input_id = input_system.receive_input('claude_code', command, input_data, priority)

    return jsonify({
        "status": "received",
        "input_id": input_id,
        "source": "claude_code"
    })


@app.route('/input/phone', methods=['POST'])
def phone_input():
    """Accept input from phone (S24/iPad)"""

    data = request.get_json()
    command = data.get('command', '')
    device = data.get('device', 'unknown')
    input_data = data.get('data', {})

    input_data['device'] = device

    input_id = input_system.receive_input('phone', command, input_data)

    return jsonify({
        "status": "received",
        "input_id": input_id,
        "source": "phone",
        "device": device
    })


@app.route('/input/web', methods=['POST'])
def web_input():
    """Accept input from web interface"""

    data = request.get_json()
    command = data.get('command', '')
    input_data = data.get('data', {})

    input_id = input_system.receive_input('web', command, input_data)

    return jsonify({
        "status": "received",
        "input_id": input_id,
        "source": "web"
    })


@app.route('/input/sms', methods=['POST'])
def sms_input():
    """Accept input from SMS (Twilio)"""

    from_number = request.form.get('From', 'unknown')
    body = request.form.get('Body', '')

    input_id = input_system.receive_input('sms', body, {"from": from_number})

    return jsonify({
        "status": "received",
        "input_id": input_id,
        "source": "sms"
    })


@app.route('/input/email', methods=['POST'])
def email_input():
    """Accept input from email"""

    data = request.get_json()
    subject = data.get('subject', '')
    body = data.get('body', '')
    from_email = data.get('from', 'unknown')

    input_id = input_system.receive_input('email', body, {
        "subject": subject,
        "from": from_email
    })

    return jsonify({
        "status": "received",
        "input_id": input_id,
        "source": "email"
    })


@app.route('/input/github', methods=['POST'])
def github_input():
    """Accept input from GitHub webhook"""

    data = request.get_json()
    event_type = request.headers.get('X-GitHub-Event', 'unknown')

    input_id = input_system.receive_input('github', event_type, data)

    return jsonify({
        "status": "received",
        "input_id": input_id,
        "source": "github",
        "event": event_type
    })


@app.route('/input/api', methods=['POST'])
def generic_api_input():
    """Generic API input - accepts anything"""

    data = request.get_json()
    command = data.get('command', '')
    input_data = data.get('data', {})
    priority = data.get('priority', 'normal')

    input_id = input_system.receive_input('api', command, input_data, priority)

    return jsonify({
        "status": "received",
        "input_id": input_id,
        "source": "api"
    })


@app.route('/inputs/all', methods=['GET'])
def get_all_inputs():
    """Get all recent inputs"""

    limit = int(request.args.get('limit', 50))
    inputs = input_system.get_all_inputs(limit)

    return jsonify({
        "inputs": inputs,
        "total": len(inputs)
    })


@app.route('/inputs/stats', methods=['GET'])
def get_input_stats():
    """Get statistics per source"""

    stats = input_system.get_source_stats()

    return jsonify({
        "sources": stats,
        "total_inputs": sum(s["count"] for s in stats.values())
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check"""

    return jsonify({
        "status": "healthy",
        "system": "Universal Input System",
        "sources_enabled": len([s for s in input_system.input_sources.values() if s["enabled"]]),
        "input_queue": len(list(INPUT_QUEUE_DIR.glob("*.json")))
    })


def process_queue_continuously():
    """Background thread to process input queue"""

    print("🔄 Starting input queue processor...")

    while True:
        try:
            input_system.process_input_queue()
            time.sleep(5)  # Process every 5 seconds
        except Exception as e:
            print(f"❌ Queue processor error: {e}")
            time.sleep(10)


def main():
    """Start Universal Input System"""

    print()
    print("=" * 70)
    print("⚡ UNIVERSAL INPUT SYSTEM")
    print("=" * 70)
    print()
    print("EVERYTHING IS AN INPUT!")
    print()
    print("Accepting commands from:")
    print("  ✅ ChatGPT      → POST /input/chatgpt")
    print("  ✅ Claude Code  → POST /input/claude")
    print("  ✅ Phone        → POST /input/phone")
    print("  ✅ Web          → POST /input/web")
    print("  ✅ SMS          → POST /input/sms")
    print("  ✅ Email        → POST /input/email")
    print("  ✅ GitHub       → POST /input/github")
    print("  ✅ API          → POST /input/api")
    print()
    print("Query endpoints:")
    print("  GET  /inputs/all   - View all inputs")
    print("  GET  /inputs/stats - Source statistics")
    print("  GET  /health       - Health check")
    print()
    print(f"Input queue: {INPUT_QUEUE_DIR}")
    print()
    print("=" * 70)
    print()

    # Start queue processor in background
    processor_thread = Thread(target=process_queue_continuously, daemon=True)
    processor_thread.start()

    # Start Flask app
    app.run(host='0.0.0.0', port=6000, debug=False)


if __name__ == '__main__':
    main()
