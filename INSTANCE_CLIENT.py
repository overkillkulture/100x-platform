"""
INSTANCE CLIENT
Connects any AI instance to the Central Command Hub

Each computer runs this to connect their instances to the cyclotron.
"""

import socketio
import time
import sys
import threading
from datetime import datetime
import json

# ===== CONFIGURATION =====

# Central Command Hub URL (change this to your hub server IP)
HUB_URL = 'http://localhost:5555'

# This instance's info
INSTANCE_ID = None  # Will be set from command line
COMPUTER_ID = None  # Will be set from command line
INSTANCE_NAME = None  # Will be set from command line

# ===== SOCKET.IO CLIENT =====

sio = socketio.Client()

# ===== EVENT HANDLERS =====

@sio.on('connect')
def on_connect():
    print(f"✅ Connected to Central Command Hub")

    # Register this instance
    sio.emit('register_instance', {
        'instance_id': INSTANCE_ID,
        'computer_id': COMPUTER_ID,
        'name': INSTANCE_NAME
    })

    print(f"📝 Registered as: {INSTANCE_NAME} (Computer {COMPUTER_ID})")

@sio.on('disconnect')
def on_disconnect():
    print(f"❌ Disconnected from Central Command Hub")

@sio.on('new_task')
def on_new_task(data):
    """Received a new task from central command"""
    task_id = data['task_id']
    task_input = data['input']

    print(f"\n📥 NEW TASK [{task_id}]: {task_input}")

    # Stream thinking
    stream_thought("Received task, analyzing...")
    time.sleep(0.5)

    stream_thought(f"Task: {task_input[:100]}")
    time.sleep(0.5)

    # Process the task
    response = process_task(task_input)

    # Send response back
    sio.emit('task_response', {
        'task_id': task_id,
        'instance_id': INSTANCE_ID,
        'response': response
    })

    stream_thought("Task complete, response sent")
    print(f"✅ Response sent for {task_id}")

# ===== TASK PROCESSING =====

def process_task(task_input):
    """Process a task and return response"""

    # This is where you'd integrate with your actual AI
    # For now, simulate processing

    stream_thought("Starting analysis...")
    time.sleep(0.5)

    stream_thought("Breaking down the task...")
    time.sleep(0.5)

    stream_thought("Generating response...")
    time.sleep(0.5)

    # Simulate response
    response = f"[{INSTANCE_NAME}] Processed: {task_input}"

    return response

# ===== THINKING STREAM =====

def stream_thought(thought):
    """Stream a thought to the dashboard"""
    try:
        sio.emit('thinking_stream', {
            'instance_id': INSTANCE_ID,
            'thought': thought
        })
    except:
        pass  # Ignore if not connected

# ===== HEARTBEAT =====

def heartbeat_loop():
    """Send periodic heartbeat"""
    while True:
        try:
            sio.emit('heartbeat', {
                'instance_id': INSTANCE_ID,
                'status': 'idle',
                'timestamp': datetime.now().isoformat()
            })
        except:
            pass

        time.sleep(10)  # Heartbeat every 10 seconds

# ===== MAIN =====

def main(hub_url, instance_id, computer_id, instance_name):
    global HUB_URL, INSTANCE_ID, COMPUTER_ID, INSTANCE_NAME

    HUB_URL = hub_url
    INSTANCE_ID = instance_id
    COMPUTER_ID = computer_id
    INSTANCE_NAME = instance_name

    print('\n' + '='*70)
    print('  🤖 INSTANCE CLIENT')
    print('='*70)
    print(f'\nInstance: {INSTANCE_NAME}')
    print(f'Computer: {COMPUTER_ID}')
    print(f'Hub: {HUB_URL}')
    print('\nConnecting to Central Command Hub...')
    print('='*70 + '\n')

    try:
        # Connect to hub
        sio.connect(HUB_URL)

        # Start heartbeat thread
        heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
        heartbeat_thread.start()

        # Keep running
        print("✅ Connected and ready")
        print("📡 Listening for tasks from Central Command...")
        print("\nPress Ctrl+C to disconnect\n")

        # Keep alive
        sio.wait()

    except KeyboardInterrupt:
        print("\n\n🛑 Disconnecting...")
        sio.disconnect()
        print("✅ Disconnected")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python3 INSTANCE_CLIENT.py <hub_url> <instance_id> <computer_id> <instance_name>")
        print("\nExample:")
        print('  python3 INSTANCE_CLIENT.py http://192.168.1.100:5555 araya_1 1 "Araya Computer 1"')
        sys.exit(1)

    hub_url = sys.argv[1]
    instance_id = sys.argv[2]
    computer_id = sys.argv[3]
    instance_name = sys.argv[4]

    main(hub_url, instance_id, computer_id, instance_name)
