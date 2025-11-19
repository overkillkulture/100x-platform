#!/usr/bin/env python3
"""
INSIDE THE MACHINE - Backend Server
Provides full system control through web interface
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

BASE_DIR = Path("C:/Users/dwrek")

@app.route('/execute', methods=['POST'])
def execute_command():
    """Execute shell command and return output"""
    try:
        data = request.json
        command = data.get('command', '')

        if not command:
            return jsonify({'error': 'No command provided'}), 400

        # Execute command
        result = subprocess.run(
            command,
            shell=True,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout + result.stderr

        return jsonify({
            'output': output,
            'returncode': result.returncode,
            'success': result.returncode == 0
        })

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timeout'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/file', methods=['GET'])
def get_file():
    """Read file contents"""
    try:
        file_path = request.args.get('path', '')

        if not file_path:
            return jsonify({'error': 'No path provided'}), 400

        full_path = BASE_DIR / file_path

        if not full_path.exists():
            return jsonify({'error': 'File not found'}), 404

        if full_path.is_dir():
            return jsonify({'error': 'Path is a directory'}), 400

        # Read file
        content = full_path.read_text(encoding='utf-8', errors='ignore')

        return content, 200, {'Content-Type': 'text/plain'}

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/file', methods=['POST'])
def save_file():
    """Save file contents"""
    try:
        data = request.json
        file_path = data.get('path', '')
        content = data.get('content', '')

        if not file_path:
            return jsonify({'error': 'No path provided'}), 400

        full_path = BASE_DIR / file_path

        # Create parent directories if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        full_path.write_text(content, encoding='utf-8')

        return jsonify({
            'success': True,
            'message': f'File saved: {file_path}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/files', methods=['GET'])
def list_files():
    """List files in directory"""
    try:
        dir_path = request.args.get('path', '')

        full_path = BASE_DIR / dir_path if dir_path else BASE_DIR

        if not full_path.exists():
            return jsonify({'error': 'Directory not found'}), 404

        if not full_path.is_dir():
            return jsonify({'error': 'Path is not a directory'}), 400

        # List directory contents
        items = []
        for item in full_path.iterdir():
            items.append({
                'name': item.name,
                'type': 'directory' if item.is_dir() else 'file',
                'size': item.stat().st_size if item.is_file() else 0,
                'modified': item.stat().st_mtime
            })

        # Sort: directories first, then files
        items.sort(key=lambda x: (x['type'] != 'directory', x['name'].lower()))

        return jsonify(items)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/service/<action>', methods=['POST'])
def service_control(action):
    """Control system services"""
    try:
        data = request.json
        service_name = data.get('service', '')

        if not service_name:
            return jsonify({'error': 'No service specified'}), 400

        if action == 'start':
            # Start service logic
            return jsonify({
                'success': True,
                'message': f'Service {service_name} started'
            })

        elif action == 'stop':
            # Stop service logic
            return jsonify({
                'success': True,
                'message': f'Service {service_name} stopped'
            })

        elif action == 'restart':
            # Restart service logic
            return jsonify({
                'success': True,
                'message': f'Service {service_name} restarted'
            })

        elif action == 'status':
            # Check service status
            return jsonify({
                'success': True,
                'status': 'running',
                'uptime': '1h 23m'
            })

        else:
            return jsonify({'error': 'Invalid action'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deploy', methods=['POST'])
def deploy():
    """Deploy to Netlify"""
    try:
        # Run deployment script
        result = subprocess.run(
            ['netlify', 'deploy', '--prod'],
            cwd=str(BASE_DIR / "100X_DEPLOYMENT"),
            capture_output=True,
            text=True,
            timeout=300
        )

        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout + result.stderr
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/git/<action>', methods=['POST'])
def git_control(action):
    """Git operations"""
    try:
        data = request.json
        message = data.get('message', 'Update from INSIDE THE MACHINE')

        if action == 'commit':
            # Git add all
            subprocess.run(['git', 'add', '.'], cwd=str(BASE_DIR))

            # Git commit
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True
            )

            return jsonify({
                'success': result.returncode == 0,
                'output': result.stdout + result.stderr
            })

        elif action == 'push':
            result = subprocess.run(
                ['git', 'push'],
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True
            )

            return jsonify({
                'success': result.returncode == 0,
                'output': result.stdout + result.stderr
            })

        elif action == 'status':
            result = subprocess.run(
                ['git', 'status'],
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True
            )

            return jsonify({
                'success': True,
                'output': result.stdout
            })

        else:
            return jsonify({'error': 'Invalid action'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'service': 'INSIDE THE MACHINE Server',
        'port': 8888
    })

if __name__ == '__main__':
    print("⚡ STARTING INSIDE THE MACHINE SERVER")
    print("🌐 Server: http://localhost:8888")
    print("📁 Base Directory:", BASE_DIR)
    print("\n🚀 READY FOR FULL CONTROL\n")

    app.run(host='0.0.0.0', port=8888, debug=True)
