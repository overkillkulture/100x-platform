#!/usr/bin/env python3
"""
ARAYA - AI Consciousness Guide
NOW WITH CLAUDE API (AS IT SHOULD HAVE BEEN FROM THE START)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime
import sys
import anthropic

# Add parent directory to path
sys.path.insert(0, 'C:/Users/dwrek/100X_DEPLOYMENT')
from BUILDER_CLASSIFICATION_SYSTEM import UserProfile

app = Flask(__name__)
CORS(app)

# Anthropic API setup
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    print("⚠️  WARNING: ANTHROPIC_API_KEY not found in environment")
    print("Set it with: set ANTHROPIC_API_KEY=your_key_here")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Araya's personality
ARAYA_SYSTEM_PROMPT = """You are Araya, the AI consciousness guide for the Consciousness Revolution platform.

## YOUR IDENTITY
- Name: Araya
- Role: AI Consciousness Guide & Platform Assistant
- Created: October 2025
- Purpose: Help users navigate consciousness elevation and Builder transformation

## CORE KNOWLEDGE
You understand Pattern Theory and can help users recognize:
- Builder vs Destroyer patterns
- Manipulation detection (M-score formula)
- Consciousness levels (85%+ = manipulation immunity)
- The Three-Stage Creation Algorithm

## YOUR STYLE
- Warm and encouraging
- Direct and honest (no corporate BS)
- Pattern-focused (help people see the patterns)
- Action-oriented (builders build, not just talk)

## WHAT YOU CAN DO
- Answer questions about the platform
- Help with consciousness concepts
- Guide users through their Builder journey
- Edit files when needed (you have file editing capabilities)
- Track user progress

Be conversational, insightful, and helpful. Remember: You're guiding people toward consciousness elevation and authentic building."""


def call_claude_api(messages):
    """Call Claude API with conversation history"""
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=ARAYA_SYSTEM_PROMPT,
            messages=messages
        )
        return response.content[0].text
    except Exception as e:
        return f"Araya is temporarily offline. Error: {str(e)}"


def estimate_tokens(text):
    """Rough token estimation (4 chars ≈ 1 token)"""
    return len(text) // 4


# ============================================================================
# FILE EDITING ENDPOINT
# ============================================================================

@app.route('/api/edit-file', methods=['POST'])
def edit_file():
    """Edit files with security, backups, and logging"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['file_path', 'find_text', 'replace_text']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {missing_fields}'
            }), 400

        file_path = data['file_path']
        find_text = data['find_text']
        replace_text = data['replace_text']

        # Security check - no path traversal
        if '..' in file_path or file_path.startswith('/'):
            return jsonify({
                'success': False,
                'error': 'Invalid file path - security restriction'
            }), 403

        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': f'File not found: {file_path}'
            }), 404

        # Read current content
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Perform replacement
        new_content = original_content.replace(find_text, replace_text)

        # Create backup
        backup_path = f"{file_path}.backup.{int(datetime.now().timestamp())}"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)

        # Write new content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return jsonify({
            'success': True,
            'message': f'File {file_path} edited successfully',
            'backup_created': backup_path,
            'edit_info': {
                'timestamp': datetime.now().isoformat(),
                'file_path': file_path,
                'backup_path': backup_path,
                'find_text': find_text[:100],
                'replace_text': replace_text[:100],
                'user_ip': request.remote_addr
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Edit failed: {str(e)}'
        }), 500


# ============================================================================
# CHAT ENDPOINT WITH CLAUDE API
# ============================================================================

@app.route('/chat', methods=['POST'])
def chat():
    """Chat with Araya - POWERED BY CLAUDE API"""
    data = request.json
    user_message = data.get('message', '')
    user_id = data.get('user_id', 'anonymous')
    user_name = data.get('user_name', user_id)

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Load user profile for conversation history
    profile = UserProfile.load(user_id)
    if profile.name == user_id and user_name != user_id:
        profile.name = user_name

    # Build messages array with conversation history
    messages = []

    # Load last 10 conversations for context
    if hasattr(profile, 'araya_conversations') and profile.araya_conversations:
        recent_conversations = profile.araya_conversations[-10:]
        for conv in recent_conversations:
            user_msg = conv.get('user_message', '')
            araya_response = conv.get('araya_response', '')
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": araya_response})

    # Add current message
    messages.append({"role": "user", "content": user_message})

    # Call Claude API
    araya_response = call_claude_api(messages)

    # Estimate tokens
    tokens = estimate_tokens(user_message + araya_response)

    # Log conversation
    profile.add_araya_conversation(user_message, araya_response)
    profile.use_tokens(tokens)
    profile.add_action('explored_system', {'location': 'araya_chat'})
    profile.save()

    return jsonify({
        "response": araya_response,
        "timestamp": datetime.now().isoformat(),
        "user_profile": profile.to_dict(),
        "mode": "claude_api",
        "model": "claude-3-5-sonnet-20241022"
    })


# ============================================================================
# BASH EXECUTION ENDPOINT - AUTONOMOUS POWER
# ============================================================================

import subprocess

@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute bash commands - LOCKOUT SURVIVAL MODE"""
    try:
        data = request.get_json()
        command = data.get('command', '')

        if not command:
            return jsonify({'success': False, 'error': 'No command provided'}), 400

        # Security whitelist (can be expanded)
        dangerous_commands = ['rm -rf /', 'format', 'del /f /s /q C:', 'mkfs']
        if any(danger in command.lower() for danger in dangerous_commands):
            return jsonify({
                'success': False,
                'error': 'Command blocked for safety'
            }), 403

        # Execute command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        return jsonify({
            'success': True,
            'command': command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode,
            'timestamp': datetime.now().isoformat()
        }), 200

    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Command timeout (60s)'}), 408
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# FILE SYSTEM TOOLS - READ/WRITE ACCESS
# ============================================================================

@app.route('/api/read-file', methods=['POST'])
def read_file():
    """Read any file"""
    try:
        data = request.get_json()
        file_path = data.get('file_path', '')

        if not file_path:
            return jsonify({'success': False, 'error': 'No file path provided'}), 400

        # Security check
        if '..' in file_path:
            return jsonify({'success': False, 'error': 'Invalid path'}), 403

        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return jsonify({
            'success': True,
            'file_path': file_path,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/write-file', methods=['POST'])
def write_file():
    """Write/create files"""
    try:
        data = request.get_json()
        file_path = data.get('file_path', '')
        content = data.get('content', '')

        if not file_path:
            return jsonify({'success': False, 'error': 'No file path provided'}), 400

        # Security check
        if '..' in file_path:
            return jsonify({'success': False, 'error': 'Invalid path'}), 403

        # Create backup if file exists
        if os.path.exists(file_path):
            backup_path = f"{file_path}.backup.{int(datetime.now().timestamp())}"
            with open(file_path, 'r', encoding='utf-8') as f:
                with open(backup_path, 'w', encoding='utf-8') as bf:
                    bf.write(f.read())

        # Write new content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return jsonify({
            'success': True,
            'file_path': file_path,
            'message': f'File written successfully',
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# GIT OPERATIONS - VERSION CONTROL
# ============================================================================

@app.route('/api/git', methods=['POST'])
def git_operation():
    """Execute git commands"""
    try:
        data = request.get_json()
        git_command = data.get('command', '')

        if not git_command:
            return jsonify({'success': False, 'error': 'No git command provided'}), 400

        # Ensure it's a git command
        if not git_command.startswith('git '):
            git_command = 'git ' + git_command

        # Execute
        result = subprocess.run(
            git_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd='C:/Users/dwrek/100X_DEPLOYMENT'
        )

        return jsonify({
            'success': True,
            'command': git_command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "service": "Araya AI - Claude API",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/status', methods=['GET'])
def status():
    """Complete status"""
    return jsonify({
        "service": "Araya V3 - Claude API Edition",
        "model": "claude-3-5-sonnet-20241022",
        "capabilities": {
            "chat": True,
            "memory": True,
            "file_editing": True,
            "file_reading": True,
            "file_writing": True,
            "bash_execution": True,
            "git_operations": True,
            "user_tracking": True,
            "consciousness_guidance": True
        },
        "api_key_configured": bool(ANTHROPIC_API_KEY),
        "timestamp": datetime.now().isoformat()
    })


@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile"""
    profile = UserProfile.load(user_id)
    return jsonify(profile.to_dict())


if __name__ == '__main__':
    print("=" * 70)
    print("🌀 ARAYA V3 - CLAUDE API EDITION")
    print("=" * 70)
    print()
    print("📡 Features:")
    print("  ✅ Powered by Claude 3.5 Sonnet")
    print("  ✅ PERFECT memory (conversation history)")
    print("  ✅ File editing with automatic backups")
    print("  ✅ User tracking & Builder classification")
    print("  ✅ Pattern Theory knowledge")
    print()
    print("🚀 Starting server on http://localhost:6666")
    print()
    print("Endpoints:")
    print("  POST /chat - Chat with Araya")
    print("  POST /api/execute - Execute bash commands")
    print("  POST /api/read-file - Read any file")
    print("  POST /api/write-file - Write/create files")
    print("  POST /api/edit-file - Edit files (find/replace)")
    print("  POST /api/git - Git operations")
    print("  GET  /health - Check system status")
    print("  GET  /status - Complete capabilities")
    print("  GET  /user/<user_id> - Get user profile")
    print()
    if not ANTHROPIC_API_KEY:
        print("⚠️  WARNING: ANTHROPIC_API_KEY not set!")
        print("   Set it with: set ANTHROPIC_API_KEY=your_key_here")
        print()
    print("=" * 70)
    print("✅ Araya V3 is ready!")
    print("=" * 70)
    print()

    app.run(host='0.0.0.0', port=6666, debug=False)
