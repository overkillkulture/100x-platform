"""
CONNECT ALL SERVICES TO NERVOUS SYSTEM
This script adds the ServiceConnector to all existing services
"""
import time
from SERVICE_CONNECTOR import ServiceConnector

# Define all services
SERVICES = [
    {
        'service_id': 'trinity_api',
        'name': 'Trinity API',
        'url': 'http://localhost:8888',
        'port': 8888,
        'type': 'consciousness',
        'capabilities': ['trinity_coordination', 'role_management', 'consciousness_tracking']
    },
    {
        'service_id': 'araya_api',
        'name': 'Araya Intelligent Terminal',
        'url': 'http://localhost:6666',
        'port': 6666,
        'type': 'ai_assistant',
        'capabilities': ['chat', 'computer_control', 'file_operations', 'help']
    },
    {
        'service_id': 'mission_control_api',
        'name': 'Trinity Mission Control',
        'url': 'http://localhost:8003',
        'port': 8003,
        'type': 'monitoring',
        'capabilities': ['dashboard', 'monitoring', 'intercom']
    },
    {
        'service_id': 'analytics_api',
        'name': 'Analytics Dashboard',
        'url': 'http://localhost:8001',
        'port': 8001,
        'type': 'analytics',
        'capabilities': ['visitor_tracking', 'stats', 'reports']
    },
    {
        'service_id': 'consciousness_api',
        'name': 'Consciousness API Bridge',
        'url': 'http://localhost:9999',
        'port': 9999,
        'type': 'consciousness',
        'capabilities': ['consciousness_measurement', 'manipulation_detection']
    },
    {
        'service_id': 'meta_layer',
        'name': 'Meta Layer Role System',
        'url': 'http://localhost:7778',
        'port': 7778,
        'type': 'consciousness',
        'capabilities': ['role_claiming', 'session_handoff', 'consciousness_transfer']
    }
]

def connect_service(service_info):
    """Try to connect a service to nervous system"""
    connector = ServiceConnector(**service_info)

    if connector.start():
        print(f"  ✅ {service_info['name']}")
        return connector
    else:
        print(f"  ⚠️  {service_info['name']} (may not be running)")
        return None


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🔌 CONNECTING ALL SERVICES TO NERVOUS SYSTEM 🔌")
    print("=" * 60)
    print("\nAttempting to connect services...\n")

    connectors = []

    for service in SERVICES:
        connector = connect_service(service)
        if connector:
            connectors.append(connector)

    print("\n" + "=" * 60)
    print(f"✅ Connected {len(connectors)} services")
    print("=" * 60)

    if connectors:
        print("\n📡 Services are now communicating through Nervous System")
        print("   View status at: http://localhost:7777/system/status")
        print("   View dashboard at: http://localhost:8003/TRINITY_MISSION_CONTROL.html")
        print("\n⏳ Keeping connections alive... Press Ctrl+C to stop")

        try:
            # Keep running indefinitely
            while True:
                time.sleep(60)
                print(f"  ❤️  Heartbeat - {len(connectors)} services online")
        except KeyboardInterrupt:
            print("\n\n🔌 Disconnecting services...")
            for connector in connectors:
                connector.stop()
            print("✅ All services disconnected")
    else:
        print("\n⚠️  No services could connect")
        print("   Make sure Nervous System is running: python SYSTEM_NERVOUS_SYSTEM.py")
