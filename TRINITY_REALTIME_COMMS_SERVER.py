#!/usr/bin/env python3
"""
================================================
TRINITY REAL-TIME COMMUNICATION SERVER
================================================
WebSocket-based real-time 2-way communication
for C1 Mechanic, C2 Architect, C3 Oracle

Features:
- Real-time message broadcasting
- Agent presence detection
- Message history (last 50 messages)
- Task coordination
- Emergency alerts
- Commander monitoring dashboard

Port: 9999
Usage: python TRINITY_REALTIME_COMMS_SERVER.py
================================================
"""

import asyncio
import json
import datetime
from typing import Set, Dict, List
from pathlib import Path

try:
    import websockets
    from websockets.server import WebSocketServerProtocol
except ImportError:
    print("❌ Installing websockets library...")
    import subprocess
    subprocess.run(["pip", "install", "websockets"], check=True)
    import websockets
    from websockets.server import WebSocketServerProtocol

# ================================================
# STATE MANAGEMENT
# ================================================

# Connected agents: {agent_id: websocket}
AGENTS: Dict[str, WebSocketServerProtocol] = {}

# Message history (last 50 messages)
MESSAGE_HISTORY: List[Dict] = []
MAX_HISTORY = 50

# Agent status: {agent_id: {status, last_seen, current_task}}
AGENT_STATUS: Dict[str, Dict] = {}

# ================================================
# CORE FUNCTIONS
# ================================================

def add_to_history(message: Dict):
    """Add message to history, maintain max size"""
    MESSAGE_HISTORY.append(message)
    if len(MESSAGE_HISTORY) > MAX_HISTORY:
        MESSAGE_HISTORY.pop(0)

def get_agent_list() -> List[str]:
    """Get list of connected agents"""
    return list(AGENTS.keys())

def format_timestamp() -> str:
    """Get current timestamp"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def broadcast_to_agents(message: Dict, exclude: str = None):
    """Broadcast message to all connected agents (except sender)"""
    if not AGENTS:
        return

    message_json = json.dumps(message)
    disconnected = []

    for agent_id, websocket in AGENTS.items():
        if agent_id == exclude:
            continue
        try:
            await websocket.send(message_json)
        except Exception as e:
            print(f"⚠️  Failed to send to {agent_id}: {e}")
            disconnected.append(agent_id)

    # Clean up disconnected agents
    for agent_id in disconnected:
        if agent_id in AGENTS:
            del AGENTS[agent_id]
        if agent_id in AGENT_STATUS:
            del AGENT_STATUS[agent_id]

async def handle_agent_message(agent_id: str, message: Dict):
    """Process message from agent"""
    msg_type = message.get("type", "chat")

    # Add metadata
    message["from"] = agent_id
    message["timestamp"] = format_timestamp()

    # Add to history
    add_to_history(message)

    # Broadcast to other agents
    await broadcast_to_agents(message, exclude=agent_id)

    # Handle specific message types
    if msg_type == "status_update":
        AGENT_STATUS[agent_id] = {
            "status": message.get("status", "active"),
            "current_task": message.get("task", ""),
            "last_seen": format_timestamp()
        }
    elif msg_type == "emergency":
        print(f"🚨 EMERGENCY from {agent_id}: {message.get('content')}")

async def handle_connection(websocket: WebSocketServerProtocol, path: str):
    """Handle new WebSocket connection"""
    agent_id = None

    try:
        # Wait for authentication message
        auth_msg = await asyncio.wait_for(websocket.recv(), timeout=10.0)
        auth_data = json.loads(auth_msg)

        agent_id = auth_data.get("agent_id")
        if not agent_id:
            await websocket.send(json.dumps({"error": "Missing agent_id"}))
            return

        # Register agent
        AGENTS[agent_id] = websocket
        AGENT_STATUS[agent_id] = {
            "status": "online",
            "current_task": "",
            "last_seen": format_timestamp()
        }

        print(f"✅ {agent_id} connected")

        # Send welcome message
        await websocket.send(json.dumps({
            "type": "welcome",
            "message": f"Welcome {agent_id}! Trinity communication active.",
            "agents_online": get_agent_list(),
            "history": MESSAGE_HISTORY[-10:]  # Last 10 messages
        }))

        # Broadcast join notification
        await broadcast_to_agents({
            "type": "system",
            "content": f"{agent_id} joined Trinity communications",
            "timestamp": format_timestamp()
        }, exclude=agent_id)

        # Message loop
        async for message in websocket:
            try:
                data = json.loads(message)
                await handle_agent_message(agent_id, data)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
            except Exception as e:
                print(f"⚠️  Error processing message from {agent_id}: {e}")
                await websocket.send(json.dumps({"error": str(e)}))

    except asyncio.TimeoutError:
        print(f"⚠️  Connection timeout (no auth)")
    except Exception as e:
        print(f"⚠️  Connection error: {e}")
    finally:
        # Clean up
        if agent_id:
            if agent_id in AGENTS:
                del AGENTS[agent_id]
            if agent_id in AGENT_STATUS:
                del AGENT_STATUS[agent_id]

            print(f"❌ {agent_id} disconnected")

            # Broadcast leave notification
            await broadcast_to_agents({
                "type": "system",
                "content": f"{agent_id} left Trinity communications",
                "timestamp": format_timestamp()
            })

# ================================================
# HTTP DASHBOARD (for Commander monitoring)
# ================================================

async def handle_http_request(path, request_headers):
    """Serve simple HTTP dashboard"""
    if path == "/":
        return (
            200,
            [("Content-Type", "text/html")],
            f"""
<!DOCTYPE html>
<html>
<head>
    <title>Trinity Communications - Monitor</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ffff;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #ff6b00, #ffd700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 32px;
            margin-bottom: 20px;
        }}
        .agent {{
            background: rgba(0, 255, 255, 0.1);
            border: 2px solid #00ffff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }}
        .online {{ border-color: #00ff88; }}
        .offline {{ border-color: #ff4444; opacity: 0.5; }}
        .message {{
            background: rgba(255, 107, 0, 0.1);
            border-left: 3px solid #ff6b00;
            padding: 10px;
            margin: 5px 0;
        }}
        .timestamp {{
            color: #888;
            font-size: 12px;
        }}
    </style>
    <script>
        // Auto-refresh every 5 seconds
        setTimeout(() => location.reload(), 5000);
    </script>
</head>
<body>
    <h1 class="header">🌀 Trinity Real-Time Communications 🌀</h1>

    <h2>Connected Agents:</h2>
    {_generate_agent_status_html()}

    <h2>Recent Messages:</h2>
    {_generate_message_history_html()}

    <p style="color: #888; font-size: 12px;">Auto-refreshes every 5 seconds • WebSocket Server Port 9999</p>
</body>
</html>
""".encode()
        )
    else:
        return (404, [], b"Not Found")

def _generate_agent_status_html() -> str:
    """Generate HTML for agent status"""
    if not AGENT_STATUS:
        return '<div class="agent offline">No agents connected</div>'

    html = ""
    for agent_id, status in AGENT_STATUS.items():
        online = agent_id in AGENTS
        status_class = "online" if online else "offline"
        status_text = "🟢 ONLINE" if online else "🔴 OFFLINE"

        html += f'''
        <div class="agent {status_class}">
            <strong>{agent_id}</strong> {status_text}<br>
            Task: {status.get("current_task", "Idle")}<br>
            <span class="timestamp">Last seen: {status.get("last_seen")}</span>
        </div>
        '''
    return html

def _generate_message_history_html() -> str:
    """Generate HTML for message history"""
    if not MESSAGE_HISTORY:
        return '<div class="message">No messages yet</div>'

    html = ""
    for msg in MESSAGE_HISTORY[-10:]:  # Last 10 messages
        html += f'''
        <div class="message">
            <strong>{msg.get("from", "System")}</strong>: {msg.get("content", msg.get("message", ""))}<br>
            <span class="timestamp">{msg.get("timestamp", "")}</span>
        </div>
        '''
    return html

# ================================================
# MAIN SERVER
# ================================================

async def main():
    """Start Trinity communications server"""
    print("=" * 60)
    print("🌀 TRINITY REAL-TIME COMMUNICATIONS SERVER")
    print("=" * 60)
    print(f"WebSocket Server: ws://localhost:9999")
    print(f"Monitor Dashboard: http://localhost:9999")
    print("=" * 60)
    print()
    print("Waiting for Trinity agents to connect...")
    print()

    # Start WebSocket server with HTTP fallback
    async with websockets.serve(
        handle_connection,
        "localhost",
        9999,
        process_request=handle_http_request
    ):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by Commander")
    except Exception as e:
        print(f"\n\n❌ Server error: {e}")
