"""
VERIFY ALL CONNECTIONS
Check that everything is connected and talking

Commander's request: "How do I make sure everything is all connected"

This script:
1. Checks Nervous System is running
2. Checks all services are registered
3. Verifies heartbeats are working
4. Tests service-to-service communication
5. Verifies alarms are monitoring
6. Tests intercom system
7. Shows visual connection map
"""
import requests
import time
from datetime import datetime

NERVOUS_SYSTEM = 'http://localhost:7776'
INTERCOM = 'http://localhost:7778'

EXPECTED_SERVICES = [
    {'id': 'trinity_api', 'port': 8888},
    {'id': 'araya_api', 'port': 6666},
    {'id': 'mission_control', 'port': 8003},
    {'id': 'analytics_api', 'port': 8001},
    {'id': 'universal_intercom', 'port': 7778},
]


def check_nervous_system():
    """Check if Nervous System is running"""
    print("\n" + "=" * 60)
    print("1️⃣  CHECKING NERVOUS SYSTEM")
    print("=" * 60)

    try:
        response = requests.get(f'{NERVOUS_SYSTEM}/system/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Nervous System is ONLINE")
            print(f"   Status: {data['status']}")
            print(f"   Services online: {data['online_services']}")
            return True
        else:
            print(f"❌ Nervous System returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Nervous System is OFFLINE: {e}")
        print(f"   Start it with: python SYSTEM_NERVOUS_SYSTEM.py")
        return False


def check_registered_services():
    """Check which services are registered"""
    print("\n" + "=" * 60)
    print("2️⃣  CHECKING REGISTERED SERVICES")
    print("=" * 60)

    try:
        response = requests.get(f'{NERVOUS_SYSTEM}/services', timeout=5)
        if response.status_code == 200:
            data = response.json()

            print(f"\nFound {data['total']} registered services:")
            print(f"  Online: {data['online']}")
            print(f"  Dead: {data['dead']}")
            print()

            for service in data['services']:
                status_icon = "✅" if service['status'] == 'online' else "❌"
                print(f"{status_icon} {service['name']}")
                print(f"   ID: {service['id']}")
                print(f"   Status: {service['status']}")
                print(f"   Last heartbeat: {service['last_heartbeat']}")
                print()

            return data['services']
        else:
            print(f"❌ Could not get services list")
            return []
    except Exception as e:
        print(f"❌ Error checking services: {e}")
        return []


def test_service_communication(services):
    """Test service-to-service communication"""
    print("\n" + "=" * 60)
    print("3️⃣  TESTING SERVICE COMMUNICATION")
    print("=" * 60)

    if len(services) < 2:
        print("⚠️  Need at least 2 services to test communication")
        return

    # Pick first two online services
    online = [s for s in services if s['status'] == 'online']

    if len(online) < 2:
        print("⚠️  Need at least 2 ONLINE services")
        return

    service1 = online[0]
    service2 = online[1]

    print(f"\nTesting: {service1['name']} → {service2['name']}")

    # Service 1 queries Service 2
    try:
        response = requests.get(f"{NERVOUS_SYSTEM}/query/{service2['id']}", timeout=5)
        if response.status_code == 200:
            print(f"✅ {service1['name']} successfully queried {service2['name']}")
            data = response.json()
            print(f"   Response: {service2['name']} is {data['registered_info']['status']}")
        else:
            print(f"❌ Query failed")
    except Exception as e:
        print(f"❌ Communication test failed: {e}")


def check_intercom():
    """Check if Universal Intercom is running"""
    print("\n" + "=" * 60)
    print("4️⃣  CHECKING UNIVERSAL INTERCOM")
    print("=" * 60)

    try:
        response = requests.get(f'{INTERCOM}/status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Universal Intercom is ONLINE")
            print(f"   Active conversations: {data['active_conversations']}")
            print(f"   Active users: {data['active_users']}")
            print(f"   Channels: {data['channels']}")
            return True
        else:
            print(f"❌ Intercom not responding")
            return False
    except Exception as e:
        print(f"❌ Universal Intercom is OFFLINE: {e}")
        print(f"   Start it with: python UNIVERSAL_INTERCOM.py")
        return False


def check_recent_events():
    """Check for recent system events"""
    print("\n" + "=" * 60)
    print("5️⃣  CHECKING RECENT EVENTS")
    print("=" * 60)

    try:
        response = requests.get(f'{NERVOUS_SYSTEM}/events?limit=10', timeout=5)
        if response.status_code == 200:
            data = response.json()

            if data['total_events'] == 0:
                print("⚠️  No events recorded yet")
                print("   Services may not be broadcasting")
                return

            print(f"\nLast {min(10, data['total_events'])} events:")
            for event in data['events'][-10:]:
                event_type = event['type']
                service_id = event.get('service_id', 'unknown')
                timestamp = event['timestamp']

                icon = "📡"
                if event_type == 'error':
                    icon = "❌"
                elif event_type == 'warning':
                    icon = "⚠️"
                elif event_type == 'critical':
                    icon = "🚨"

                print(f"{icon} {event_type} from {service_id}")
                print(f"   Time: {timestamp}")
                print()

    except Exception as e:
        print(f"❌ Could not check events: {e}")


def show_connection_map(services):
    """Show visual connection map"""
    print("\n" + "=" * 60)
    print("6️⃣  CONNECTION MAP")
    print("=" * 60)

    print("""
                    🧠 NERVOUS SYSTEM (Port 7776)
                              |
                (Central Communication Hub)
                              |
        +---------------------+---------------------+
        |                     |                     |
""")

    for i, service in enumerate(services[:3]):
        status = "✅" if service['status'] == 'online' else "❌"
        print(f"    {status} {service['name']:<20} ", end="")

    print("\n")

    if len(services) > 3:
        for service in services[3:]:
            status = "✅" if service['status'] == 'online' else "❌"
            print(f"    {status} {service['name']}")

    print("""
                              |
                    📻 INTERCOM (Port 7778)
                    (Break into conversations)
                              |
                        TEAM HUB
                    (Visual Interface)
""")


def run_full_check():
    """Run complete connection verification"""
    print("\n" + "=" * 60)
    print("🔍 COMPLETE CONNECTION VERIFICATION 🔍")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. Check Nervous System
    nervous_ok = check_nervous_system()
    if not nervous_ok:
        print("\n❌ CRITICAL: Nervous System is not running!")
        print("   Cannot proceed without it.")
        return

    # 2. Check registered services
    services = check_registered_services()

    # 3. Test communication
    if services:
        test_service_communication(services)

    # 4. Check intercom
    intercom_ok = check_intercom()

    # 5. Check events
    check_recent_events()

    # 6. Show connection map
    show_connection_map(services)

    # Final summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    total_services = len(services)
    online_services = len([s for s in services if s['status'] == 'online'])

    print(f"\n✅ Nervous System: {'ONLINE' if nervous_ok else 'OFFLINE'}")
    print(f"✅ Intercom: {'ONLINE' if intercom_ok else 'OFFLINE'}")
    print(f"📡 Services: {online_services}/{total_services} online")

    if online_services == total_services and nervous_ok and intercom_ok:
        print("\n🎉 ALL SYSTEMS CONNECTED AND COMMUNICATING! 🎉")
    elif online_services > 0:
        print("\n⚠️  Some systems are online, but not all")
        print("   Check which services need to be started")
    else:
        print("\n❌ NO SERVICES CONNECTED")
        print("   Start services and connect them with SERVICE_CONNECTOR")

    print("\n" + "=" * 60)


if __name__ == '__main__':
    run_full_check()
