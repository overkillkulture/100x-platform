"""
BUILDER TERMINAL API - Web-Based Claude Code for Beta Testers
Created: October 23, 2025

Gives beta testers their own AI coding assistant that can:
- Write code for them
- Create/edit files in their sandbox
- Deploy changes instantly
- Build their own sections of the platform
"""

import os
import anthropic
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path
import re

app = Flask(__name__)
CORS(app)

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Base directory for builder sandboxes
BUILDERS_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/builders")
BUILDERS_DIR.mkdir(exist_ok=True)

def get_builder_dir(username):
    """Get or create a builder's sandbox directory"""
    builder_dir = BUILDERS_DIR / username
    builder_dir.mkdir(exist_ok=True)
    return builder_dir

def sanitize_filename(filename):
    """Ensure filename is safe (no path traversal)"""
    # Remove any path separators and parent directory references
    filename = re.sub(r'[/\\]', '', filename)
    filename = filename.replace('..', '')
    return filename

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "operational",
        "service": "Builder Terminal API",
        "version": "1.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint - AI coding assistant"""
    data = request.json
    username = data.get('username', 'default')
    message = data.get('message', '')
    conversation_history = data.get('history', [])

    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Get builder's directory
    builder_dir = get_builder_dir(username)

    # System prompt - gives Claude coding abilities in builder's sandbox
    system_prompt = f"""You are a coding assistant for a Builder on the Consciousness Revolution platform.

Your Builder: {username}
Their Workspace: /builders/{username}/

## YOUR ABILITIES:

1. **Write Code**: Create HTML, CSS, JavaScript, Python files
2. **Read Files**: See what exists in their workspace
3. **Edit Files**: Modify existing code
4. **Explain Code**: Help them understand what you're building

## WORKSPACE RULES:

- You can ONLY create/modify files in /builders/{username}/
- No access to other directories
- Keep code simple and well-commented
- Always explain what you're doing

## RESPONSE FORMAT:

When writing code, use this format:

```language:filename
[code here]
```

Example:
```html:index.html
<!DOCTYPE html>
<html>
<body>
    <h1>Hello Builder!</h1>
</body>
</html>
```

The system will automatically save files you create.

## CURRENT WORKSPACE CONTENTS:
{list_workspace_files(builder_dir)}

Now help your Builder create something amazing!"""

    # Build conversation for Claude
    messages = []
    for msg in conversation_history:
        messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", "")
        })

    messages.append({
        "role": "user",
        "content": message
    })

    try:
        # Call Claude API
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            temperature=0.7,
            system=system_prompt,
            messages=messages
        )

        assistant_message = response.content[0].text

        # Parse code blocks and save files
        files_created = parse_and_save_code_blocks(assistant_message, builder_dir)

        return jsonify({
            "response": assistant_message,
            "files_created": files_created,
            "workspace": f"/builders/{username}/",
            "preview_url": f"/builders/{username}/index.html",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            "error": str(e),
            "message": "AI assistant encountered an error"
        }), 500

def list_workspace_files(builder_dir):
    """List all files in builder's workspace"""
    try:
        files = []
        for file_path in builder_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(builder_dir)
                files.append(str(relative_path))

        if not files:
            return "Workspace is empty - ready for your first creation!"

        return "Files:\n" + "\n".join([f"  - {f}" for f in files])
    except Exception as e:
        return f"Error listing files: {e}"

def parse_and_save_code_blocks(message, builder_dir):
    """Parse code blocks from Claude's response and save them"""
    files_created = []

    # Pattern: ```language:filename
    pattern = r'```(\w+):([^\n]+)\n(.*?)```'
    matches = re.finditer(pattern, message, re.DOTALL)

    for match in matches:
        language = match.group(1)
        filename = match.group(2).strip()
        code = match.group(3)

        # Sanitize filename
        filename = sanitize_filename(filename)

        # Save file in builder's directory
        file_path = builder_dir / filename

        try:
            file_path.write_text(code, encoding='utf-8')
            files_created.append({
                "filename": filename,
                "language": language,
                "size": len(code),
                "path": str(file_path.relative_to(BUILDERS_DIR))
            })
            print(f"✅ Created: {file_path}")
        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")

    return files_created

@app.route('/builders/<username>/<path:filename>')
def serve_builder_file(username, filename):
    """Serve files from builder's workspace"""
    builder_dir = get_builder_dir(username)
    return send_from_directory(builder_dir, filename)

@app.route('/api/workspace/<username>', methods=['GET'])
def get_workspace(username):
    """Get all files in builder's workspace"""
    builder_dir = get_builder_dir(username)

    files = []
    for file_path in builder_dir.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(builder_dir)
            files.append({
                "filename": str(relative_path),
                "size": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })

    return jsonify({
        "username": username,
        "workspace": f"/builders/{username}/",
        "files": files,
        "file_count": len(files)
    })

@app.route('/api/read/<username>/<path:filename>', methods=['GET'])
def read_file(username, filename):
    """Read a file from builder's workspace"""
    builder_dir = get_builder_dir(username)
    filename = sanitize_filename(filename)
    file_path = builder_dir / filename

    if not file_path.exists():
        return jsonify({"error": "File not found"}), 404

    try:
        content = file_path.read_text(encoding='utf-8')
        return jsonify({
            "filename": filename,
            "content": content,
            "size": len(content)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_index():
    """Serve the main entry point"""
    return send_from_directory('C:/Users/dwrek/100X_DEPLOYMENT', 'index.html')

@app.route('/simple-gate.html')
def serve_gate():
    """Serve the authentication gate"""
    return send_from_directory('C:/Users/dwrek/100X_DEPLOYMENT', 'simple-gate.html')

@app.route('/builder-terminal.html')
def serve_terminal():
    """Serve the Builder Terminal workspace interface"""
    return send_from_directory('C:/Users/dwrek/100X_DEPLOYMENT', 'builder-terminal.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve any other static files (CSS, JS, images, etc)"""
    return send_from_directory('C:/Users/dwrek/100X_DEPLOYMENT', filename)

if __name__ == '__main__':
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  WARNING: ANTHROPIC_API_KEY not found!")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
    else:
        print("✅ Claude API key found")

    print("\n🔨 BUILDER TERMINAL API STARTING 🔨")
    print("=" * 60)
    print("Service: AI Coding Assistant for Builders")
    print("Model: Claude Sonnet 4")
    print(f"Workspaces: {BUILDERS_DIR}")
    print("=" * 60)
    print("\nEndpoints:")
    print("  POST /api/chat - AI coding assistant")
    print("  GET  /api/health - Health check")
    print("  GET  /api/workspace/<username> - List workspace files")
    print("  GET  /api/read/<username>/<filename> - Read file")
    print("  GET  /builders/<username>/<filename> - Serve builder files")
    print("\n🚀 Ready to build! 🚀\n")

    # Run on port 8003 (dedicated builder terminal port)
    app.run(host='0.0.0.0', port=8004, debug=True)
