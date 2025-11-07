"""
MASTER COORDINATOR
Launches and manages both local and inter-computer coordination

Features:
- Starts Local Instance Coordinator (port 8900)
- Starts Inter-Computer Sync service
- Provides unified dashboard
- Monitors all coordination services
- Handles graceful shutdown
"""

import subprocess
import threading
import time
import signal
import sys
from pathlib import Path

# Processes
PROCESSES = []

def start_service(name, script_path, description):
    """Start a coordination service"""
    print(f"\n🚀 Starting {name}...")
    print(f"   {description}")

    try:
        process = subprocess.Popen(
            ['python3', script_path],
            cwd='/home/user/100x-platform',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        PROCESSES.append({
            'name': name,
            'process': process,
            'script': script_path
        })

        print(f"✅ {name} started (PID: {process.pid})")
        return process

    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def monitor_process_output(process_info):
    """Monitor and print process output"""
    name = process_info['name']
    process = process_info['process']

    # Print stdout
    for line in process.stdout:
        print(f"[{name}] {line.rstrip()}")

def shutdown_all():
    """Gracefully shutdown all services"""
    print("\n\n🛑 Shutting down all coordination services...")

    for proc_info in PROCESSES:
        try:
            print(f"   Stopping {proc_info['name']}...")
            proc_info['process'].terminate()
            proc_info['process'].wait(timeout=10)
            print(f"   ✅ {proc_info['name']} stopped")
        except:
            print(f"   ⚠️ Force killing {proc_info['name']}...")
            proc_info['process'].kill()

    print("\n✅ All services stopped")
    sys.exit(0)

def signal_handler(sig, frame):
    """Handle Ctrl+C"""
    shutdown_all()

if __name__ == '__main__':
    print('\n' + '='*70)
    print('  🎛️  MASTER COORDINATOR - TRINITY SYSTEM')
    print('='*70)
    print('\n🌐 Multi-Tier Coordination Architecture:')
    print('\n  TIER 1: Local Instances (6 instances on this computer)')
    print('    • Araya (8001) - AI Consciousness Guide')
    print('    • Builder (8004) - Project Creation')
    print('    • Observatory (7777) - System Monitoring')
    print('    • Visitor Intelligence (6000) - User Tracking')
    print('    • Analytics (5000) - Singularity Stabilizer')
    print('    • C1 Mechanic (Claude) - Trinity Primary')
    print('\n  TIER 2: Local Coordinator (Instance orchestration)')
    print('    • LOCAL_INSTANCE_COORDINATOR.py')
    print('    • Port: 8900')
    print('    • Dashboard: http://localhost:8900/dashboard')
    print('\n  TIER 3: Inter-Computer Sync (Trinity coordination)')
    print('    • INTER_COMPUTER_SYNC.py')
    print('    • Syncs with Computer 2 (C2 Architect)')
    print('    • Syncs with Computer 3 (C3 Oracle)')
    print('    • Protocol: Git-based async (every 5 min)')
    print('\n' + '='*70)

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    print('\n🔧 Launching coordination services...\n')

    # Start Local Instance Coordinator
    local_coord = start_service(
        'Local Coordinator',
        '/home/user/100x-platform/LOCAL_INSTANCE_COORDINATOR.py',
        'Monitors and coordinates 6 local instances'
    )

    if local_coord:
        # Start output monitoring in background
        threading.Thread(
            target=monitor_process_output,
            args=({'name': 'Local Coordinator', 'process': local_coord},),
            daemon=True
        ).start()

    # Give it a moment to start
    time.sleep(2)

    # Start Inter-Computer Sync
    inter_sync = start_service(
        'Inter-Computer Sync',
        '/home/user/100x-platform/INTER_COMPUTER_SYNC.py',
        'Syncs with Computer 2 & 3 via Git'
    )

    if inter_sync:
        # Start output monitoring in background
        threading.Thread(
            target=monitor_process_output,
            args=({'name': 'Inter-Computer Sync', 'process': inter_sync},),
            daemon=True
        ).start()

    print('\n' + '='*70)
    print('  ✅ ALL COORDINATION SERVICES RUNNING')
    print('='*70)
    print('\n📊 Dashboards & Endpoints:')
    print('  • Local Dashboard: http://localhost:8900/dashboard')
    print('  • Instance Status: http://localhost:8900/instances')
    print('  • Messages: http://localhost:8900/messages')
    print('  • Tasks: http://localhost:8900/tasks')
    print('\n💡 Tips:')
    print('  • Press Ctrl+C to stop all services')
    print('  • Check dashboard for real-time instance status')
    print('  • Git syncs happen every 5 minutes automatically')
    print('  • Messages from Computer 2 & 3 will appear in dashboard')
    print('\n' + '='*70)
    print('\n⏳ Coordination system running... (Press Ctrl+C to stop)\n')

    # Keep running until interrupted
    try:
        while True:
            # Check if processes are still alive
            for proc_info in PROCESSES:
                if proc_info['process'].poll() is not None:
                    print(f"⚠️ {proc_info['name']} has stopped unexpectedly!")

            time.sleep(10)

    except KeyboardInterrupt:
        shutdown_all()
