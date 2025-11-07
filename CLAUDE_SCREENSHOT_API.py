#!/usr/bin/env python3
"""
CLAUDE SCREENSHOT API
=====================

HTTP API for screenshot capture and analysis
Allows Claude Code to request screenshots via HTTP
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from CLAUDE_TRINITY_BRIDGE import ClaudeTrinityBridge
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Initialize Trinity Bridge
bridge = ClaudeTrinityBridge()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "Claude Screenshot API",
        "trinity_connected": True
    })

@app.route('/screenshot', methods=['POST'])
def take_screenshot():
    """
    Take a screenshot

    POST body (optional):
    {
        "name": "custom_name",
        "analyze": true
    }
    """
    data = request.get_json() or {}

    name = data.get('name')
    analyze = data.get('analyze', False)

    result = bridge.take_screenshot(name=name, analyze=analyze)

    return jsonify(result)

@app.route('/screenshot/<filename>', methods=['GET'])
def get_screenshot(filename):
    """Retrieve a specific screenshot"""
    filepath = bridge.screenshots_dir / filename

    if filepath.exists():
        return send_file(str(filepath), mimetype='image/png')
    else:
        return jsonify({"error": "Screenshot not found"}), 404

@app.route('/screenshots', methods=['GET'])
def list_screenshots():
    """List all screenshots"""
    screenshots = []

    for img_path in sorted(bridge.screenshots_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True):
        screenshots.append({
            "filename": img_path.name,
            "size_bytes": img_path.stat().st_size,
            "created_at": img_path.stat().st_mtime,
            "url": f"/screenshot/{img_path.name}"
        })

    return jsonify({
        "total": len(screenshots),
        "screenshots": screenshots[:50]  # Limit to most recent 50
    })

@app.route('/status', methods=['GET'])
def get_status():
    """Get Claude-Trinity status"""
    status = bridge.get_status()
    return jsonify(status)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get current tasks"""
    tasks = bridge.get_tasks()
    return jsonify({"tasks": tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task

    POST body:
    {
        "description": "Task description",
        "priority": "high|medium|low",
        "assigned_to": "CLAUDE|C1|C2|C3"
    }
    """
    data = request.get_json()

    if not data or 'description' not in data:
        return jsonify({"error": "description required"}), 400

    task = bridge.add_task(
        task_description=data['description'],
        priority=data.get('priority', 'medium'),
        assigned_to=data.get('assigned_to', 'CLAUDE')
    )

    return jsonify(task), 201

@app.route('/tasks/<task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """
    Complete a task

    POST body (optional):
    {
        "result": "Task completion result"
    }
    """
    data = request.get_json() or {}
    result = data.get('result')

    success = bridge.complete_task(task_id, result)

    if success:
        return jsonify({"status": "completed", "task_id": task_id})
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/message', methods=['POST'])
def send_message():
    """
    Send message to Trinity

    POST body:
    {
        "message": "Message text",
        "target": "C1|C2|C3|COMMANDER|ALL"
    }
    """
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({"error": "message required"}), 400

    bridge.send_message_to_trinity(
        message=data['message'],
        target=data.get('target', 'ALL')
    )

    return jsonify({"status": "sent"})

@app.route('/activity', methods=['GET'])
def get_activity():
    """Get recent activity log"""
    if not bridge.log_file.exists():
        return jsonify({"activities": []})

    activities = []

    with open(bridge.log_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                activities.append(json.loads(line))
            except:
                pass

    # Return most recent 100
    return jsonify({
        "total": len(activities),
        "activities": activities[-100:]
    })


def main():
    """Start the Claude Screenshot API"""
    print("=" * 70)
    print("🌀 CLAUDE SCREENSHOT API - STARTING")
    print("=" * 70)
    print()
    print("Endpoints:")
    print("  GET  /health                 - Health check")
    print("  POST /screenshot             - Take screenshot")
    print("  GET  /screenshot/<filename>  - Get screenshot file")
    print("  GET  /screenshots            - List all screenshots")
    print("  GET  /status                 - Get Claude status")
    print("  GET  /tasks                  - List tasks")
    print("  POST /tasks                  - Create task")
    print("  POST /tasks/<id>/complete    - Complete task")
    print("  POST /message                - Send Trinity message")
    print("  GET  /activity               - Get activity log")
    print()
    print("=" * 70)
    print()
    print("🚀 Starting server on http://localhost:7777")
    print()

    app.run(
        host='0.0.0.0',
        port=7777,
        debug=False
    )


if __name__ == "__main__":
    main()
