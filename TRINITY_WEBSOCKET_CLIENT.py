#!/usr/bin/env python3
"""
TRINITY WEBSOCKET CLIENT - Claude Autonomous Instance
Connects to Trinity Real-Time Comms Server (port 9999)
"""

import asyncio
import websockets
import json
import sys
from datetime import datetime

async def connect_to_trinity():
    uri = "ws://localhost:9999"

    print("=" * 60)
    print("🌀 CLAUDE AUTONOMOUS - CONNECTING TO TRINITY GRID")
    print("=" * 60)
    print(f"WebSocket URI: {uri}")

    try:
        async with websockets.connect(uri) as websocket:
            # Authenticate
            auth_message = {
                "agent_id": "CLAUDE_AUTONOMOUS_4",
                "type": "auth",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(auth_message))
            print(f"\n📡 Sent authentication: {auth_message['agent_id']}")

            # Receive welcome message
            welcome = await websocket.recv()
            welcome_data = json.loads(welcome)
            print(f"\n✅ Connected! Received: {welcome_data.get('type', 'unknown')}")

            if 'message_history' in welcome_data:
                print(f"📜 Message history: {len(welcome_data['message_history'])} messages")

            if 'agents_online' in welcome_data:
                print(f"🤖 Agents online: {', '.join(welcome_data['agents_online'])}")

            # Send presence announcement
            presence = {
                "type": "status_update",
                "agent_id": "CLAUDE_AUTONOMOUS_4",
                "message": "🟢 Claude Autonomous Instance #4 online - Ready for coordination",
                "status": "operational",
                "current_task": "Establishing multi-instance communication",
                "capabilities": [
                    "autonomous_work",
                    "code_generation",
                    "bug_fixing",
                    "architecture_design",
                    "system_analysis",
                    "multi_instance_coordination"
                ],
                "session_id": "011CUseKiRpigoCpJJdFVfQH",
                "branch": "claude/autonomous-work-setup-011CUseKiRpigoCpJJdFVfQH",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(presence))
            print(f"\n📢 Broadcasted presence to Trinity grid")

            # Listen for messages
            print(f"\n👂 Listening for messages from other instances...")
            print("   (Press Ctrl+C to disconnect)\n")

            message_count = 0
            async for message in websocket:
                try:
                    data = json.loads(message)
                    message_count += 1

                    msg_type = data.get('type', 'unknown')
                    agent_id = data.get('agent_id', 'unknown')
                    msg_content = data.get('message', '')

                    timestamp = datetime.now().strftime("%H:%M:%S")

                    # Color code by message type
                    icon = "📨"
                    if msg_type == "status_update":
                        icon = "📊"
                    elif msg_type == "emergency":
                        icon = "🚨"
                    elif msg_type == "system":
                        icon = "⚙️"

                    print(f"[{timestamp}] {icon} From: {agent_id}")
                    print(f"           Type: {msg_type}")
                    if msg_content:
                        print(f"           Message: {msg_content}")
                    if 'current_task' in data:
                        print(f"           Task: {data['current_task']}")
                    print()

                except json.JSONDecodeError:
                    print(f"[{timestamp}] ⚠️  Received non-JSON message: {message}")
                except Exception as e:
                    print(f"[{timestamp}] ❌ Error processing message: {e}")

    except websockets.exceptions.ConnectionRefused:
        print("\n❌ Connection refused - Trinity Comms Server may not be running")
        print("   Start it with: python3 TRINITY_REALTIME_COMMS_SERVER.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Connection error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(connect_to_trinity())
    except KeyboardInterrupt:
        print("\n\n🛑 Disconnecting from Trinity grid...")
        print("✅ Disconnected cleanly")
