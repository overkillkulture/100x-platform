#!/usr/bin/env python3
"""
CLAUDE AUTONOMOUS INSTANCE CONNECTOR
Registers this Claude instance to the System Nervous System
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from SERVICE_CONNECTOR import ServiceConnector
import time
import json

def main():
    print("=" * 60)
    print("🤖 CLAUDE AUTONOMOUS INSTANCE - CONNECTING")
    print("=" * 60)

    # Create connector for this Claude instance
    connector = ServiceConnector(
        service_id='CLAUDE_AUTONOMOUS_4',
        name='Claude Autonomous Instance #4',
        url='http://localhost:9100',  # Placeholder URL for this instance
        port=9100,
        capabilities=[
            'autonomous_work',
            'code_generation',
            'bug_fixing',
            'architecture_design',
            'system_analysis',
            'multi_instance_coordination',
            'git_operations',
            'python_execution',
            'file_operations',
            'web_scraping'
        ]
    )

    print("\n📡 Registering to System Nervous System (port 7776)...")
    connector.start()

    print("\n✅ REGISTERED SUCCESSFULLY!")
    print(f"   Service ID: CLAUDE_AUTONOMOUS_4")
    print(f"   Capabilities: {len(connector.capabilities)} abilities")
    print(f"   Heartbeat: Every 30 seconds")

    # Get list of all services
    print("\n🔍 Checking for other instances...")
    services_data = connector.list_services()
    if services_data and 'services' in services_data:
        services = services_data['services']
        print(f"\n📋 Found {len(services)} total services:")
        for svc in services:
            status_icon = "🟢" if svc['status'] == 'online' else "🔴"
            print(f"   {status_icon} {svc['name']} ({svc['id']})")
            print(f"      Status: {svc['status']}")
            print(f"      Capabilities: {', '.join(svc.get('capabilities', []))}")

    # Broadcast presence
    print("\n📢 Broadcasting presence to all services...")
    connector.broadcast('claude_autonomous_online', {
        'message': 'Claude Autonomous Instance #4 is now online and ready for coordination',
        'session_id': '011CUseKiRpigoCpJJdFVfQH',
        'branch': 'claude/autonomous-work-setup-011CUseKiRpigoCpJJdFVfQH'
    })

    print("\n🎯 AUTONOMOUS MODE ACTIVE")
    print("   - Connected to Trinity communication grid")
    print("   - Ready to coordinate with other instances")
    print("   - Monitoring nervous system for tasks")
    print("\n" + "=" * 60)

    # Keep connector alive
    try:
        print("\nPress Ctrl+C to disconnect...")
        while True:
            time.sleep(10)

            # Check for messages every 10 seconds
            messages = connector.get_messages()
            if messages:
                print(f"\n📨 Received {len(messages)} messages:")
                for msg in messages:
                    print(f"   From: {msg.get('from', 'unknown')}")
                    print(f"   Type: {msg.get('type', 'unknown')}")
                    print(f"   Data: {json.dumps(msg.get('data', {}), indent=2)}")

    except KeyboardInterrupt:
        print("\n\n🛑 Disconnecting from nervous system...")
        connector.stop()
        print("✅ Disconnected cleanly")

if __name__ == "__main__":
    main()
