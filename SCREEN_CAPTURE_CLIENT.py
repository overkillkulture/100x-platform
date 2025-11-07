"""
SCREEN CAPTURE CLIENT
Captures screenshots and sends to Central Command Hub for AI analysis

Works on any computer - captures screen every N seconds and streams to the cyclotron.
"""

import socketio
import time
import base64
import io
from datetime import datetime
from PIL import ImageGrab
import sys

# ===== CONFIGURATION =====

HUB_URL = 'http://localhost:5555'
INSTANCE_ID = None
CAPTURE_INTERVAL = 5  # seconds

# ===== SOCKET.IO CLIENT =====

sio = socketio.Client()

# ===== SCREEN CAPTURE =====

def capture_screen():
    """Capture the screen and return as base64 string"""
    try:
        # Capture screen
        screenshot = ImageGrab.grab()

        # Resize to reduce bandwidth (optional)
        screenshot = screenshot.resize((1280, 720))

        # Convert to base64
        buffer = io.BytesIO()
        screenshot.save(buffer, format='PNG')
        img_b64 = base64.b64encode(buffer.getvalue()).decode()

        return img_b64

    except Exception as e:
        print(f"❌ Screen capture error: {e}")
        return None

def capture_loop():
    """Main capture loop"""
    print(f"📸 Starting screen capture (every {CAPTURE_INTERVAL}s)...")

    while True:
        try:
            # Capture screen
            img_b64 = capture_screen()

            if img_b64 and sio.connected:
                # Send to hub
                sio.emit('screen_capture', {
                    'instance_id': INSTANCE_ID,
                    'screenshot': img_b64
                })

                print(f"📸 Screen captured and sent ({datetime.now().strftime('%H:%M:%S')})")

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(CAPTURE_INTERVAL)

# ===== EVENT HANDLERS =====

@sio.on('connect')
def on_connect():
    print(f"✅ Connected to Central Command Hub")

    # Register
    sio.emit('register_instance', {
        'instance_id': INSTANCE_ID,
        'computer_id': 'screen_capture',
        'name': f'Screen Capture ({INSTANCE_ID})'
    })

@sio.on('disconnect')
def on_disconnect():
    print(f"❌ Disconnected from hub")

# ===== MAIN =====

def main(hub_url, instance_id, capture_interval=5):
    global HUB_URL, INSTANCE_ID, CAPTURE_INTERVAL

    HUB_URL = hub_url
    INSTANCE_ID = instance_id
    CAPTURE_INTERVAL = capture_interval

    print('\n' + '='*70)
    print('  📸 SCREEN CAPTURE CLIENT')
    print('='*70)
    print(f'\nInstance: {INSTANCE_ID}')
    print(f'Hub: {HUB_URL}')
    print(f'Interval: {CAPTURE_INTERVAL}s')
    print('\nConnecting to hub...')
    print('='*70 + '\n')

    try:
        # Connect to hub
        sio.connect(HUB_URL)

        print("✅ Connected")
        print("📸 Capturing screen... Press Ctrl+C to stop\n")

        # Start capture loop
        capture_loop()

    except KeyboardInterrupt:
        print("\n\n🛑 Stopping...")
        sio.disconnect()
        print("✅ Stopped")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: Make sure Pillow is installed:")
        print("  pip3 install Pillow python-socketio")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 SCREEN_CAPTURE_CLIENT.py <hub_url> <instance_id> [interval]")
        print("\nExample:")
        print("  python3 SCREEN_CAPTURE_CLIENT.py http://192.168.1.100:5555 computer1 5")
        sys.exit(1)

    hub_url = sys.argv[1]
    instance_id = sys.argv[2]
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    main(hub_url, instance_id, interval)
