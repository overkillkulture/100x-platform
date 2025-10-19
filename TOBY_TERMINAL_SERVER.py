#!/usr/bin/env python3
"""
TOBY'S TERMINAL SERVER - Mac Edition
This creates a WebSocket server that connects to the JARVIS HUD terminal
So we can help Toby remotely from our side!
"""

import asyncio
import websockets
import subprocess
import json
import os

print("""
🌌 TOBY'S TERMINAL SERVER 🌌
===============================
This will let the JARVIS HUD connect to your Mac terminal!
Server running on ws://localhost:8765

READY TO CONNECT!
""")

# Store connected clients
clients = set()

async def handle_terminal(websocket, path):
    """Handle terminal commands from JARVIS HUD"""
    clients.add(websocket)
    print(f"✅ JARVIS HUD connected! ({len(clients)} total connections)")

    try:
        # Send welcome message
        await websocket.send(json.dumps({
            'output': '🎮 TOBY\'S MAC TERMINAL CONNECTED!',
            'cwd': os.getcwd()
        }))

        await websocket.send(json.dumps({
            'output': f'Current directory: {os.getcwd()}',
            'cwd': os.getcwd()
        }))

        await websocket.send(json.dumps({
            'output': '💻 Ready for commands! Type anything...',
            'cwd': os.getcwd()
        }))

        # Handle incoming commands
        async for message in websocket:
            try:
                data = json.loads(message)

                if data.get('action') == 'execute':
                    command = data.get('command', '').strip()

                    if not command:
                        continue

                    print(f"📥 Command received: {command}")

                    # Handle cd command specially
                    if command.startswith('cd '):
                        try:
                            new_dir = command[3:].strip()
                            os.chdir(new_dir)
                            output = f'Changed directory to: {os.getcwd()}'
                        except Exception as e:
                            output = f'Error: {str(e)}'
                    else:
                        # Execute command
                        try:
                            result = subprocess.run(
                                command,
                                shell=True,
                                capture_output=True,
                                text=True,
                                timeout=30,
                                cwd=os.getcwd()
                            )
                            output = result.stdout if result.stdout else result.stderr
                            if not output:
                                output = '✅ Command completed'
                        except subprocess.TimeoutExpired:
                            output = '⏱️ Command timed out (30s limit)'
                        except Exception as e:
                            output = f'❌ Error: {str(e)}'

                    # Send output back
                    await websocket.send(json.dumps({
                        'output': output,
                        'cwd': os.getcwd()
                    }))

                    print(f"📤 Response sent: {output[:100]}...")

            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    'output': '❌ Invalid command format',
                    'cwd': os.getcwd()
                }))
            except Exception as e:
                await websocket.send(json.dumps({
                    'output': f'❌ Error: {str(e)}',
                    'cwd': os.getcwd()
                }))

    except websockets.exceptions.ConnectionClosed:
        print("🔴 JARVIS HUD disconnected")
    finally:
        clients.remove(websocket)
        print(f"Remaining connections: {len(clients)}")

async def main():
    """Start the WebSocket server"""
    server = await websockets.serve(handle_terminal, "0.0.0.0", 8765)
    print("🚀 Server started successfully!")
    print("📡 Listening on ws://0.0.0.0:8765")
    print("\nWaiting for JARVIS HUD to connect...")
    print("(Open the JARVIS HUD and click the Terminal module)")
    print("\n🛑 Press Ctrl+C to stop\n")

    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("Thanks for using Toby's Terminal Server! 🌌")
