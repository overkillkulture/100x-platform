"""
COMMUNICATION DEMO
Shows all the ways services can talk to each other

Commander's request: "tap that other API on the shoulder and say what's going on over there dude"

This demonstrates:
1. Service registration with Nervous System
2. Heartbeat monitoring
3. Event broadcasting
4. Service querying ("tap on shoulder")
5. Service-to-service requests
6. Alarm triggering
7. Multi-channel logging
"""
import time
from SERVICE_CONNECTOR import ServiceConnector
from COMMUNICATION_CHANNELS import CommunicationHub

print("\n" + "=" * 60)
print("🔊 COMPLETE COMMUNICATION SYSTEM DEMO 🔊")
print("=" * 60)

# Create 3 mock services
print("\n📡 Creating 3 services...")

service1 = ServiceConnector(
    service_id='demo_api_1',
    name='Demo API 1',
    url='http://localhost:9001',
    port=9001,
    capabilities=['data_processing', 'analytics']
)

service2 = ServiceConnector(
    service_id='demo_api_2',
    name='Demo API 2',
    url='http://localhost:9002',
    port=9002,
    capabilities=['user_management', 'authentication']
)

service3 = ServiceConnector(
    service_id='demo_api_3',
    name='Demo API 3',
    url='http://localhost:9003',
    port=9003,
    capabilities=['file_storage', 'backup']
)

# Start services (register + heartbeat)
print("\n🚀 Starting services...")
service1.start()
service2.start()
service3.start()

# Create communication hub for Service 1
comm = CommunicationHub('demo_api_1', 'Demo API 1')

print("\n" + "=" * 60)
print("✅ All services registered with Nervous System")
print("=" * 60)

# Wait a moment
time.sleep(2)

# --- DEMO 1: LIST ALL SERVICES ---
print("\n\n1️⃣  LISTING ALL SERVICES")
print("-" * 60)
services = service1.list_services()
print(f"Found {services['total']} services:")
for svc in services['services']:
    print(f"  • {svc['name']} ({svc['id']}) - {svc['status']}")

# --- DEMO 2: TAP ON SHOULDER (Query Service) ---
print("\n\n2️⃣  TAP ON SHOULDER - Query what Service 2 is doing")
print("-" * 60)
print("Service 1: Hey Service 2, what's going on over there?")

status = service1.query('demo_api_2')
print(f"\nService 2 responded:")
print(f"  Name: {status['registered_info']['name']}")
print(f"  Status: {status['registered_info']['status']}")
print(f"  Capabilities: {', '.join(status['registered_info']['capabilities'])}")
print(f"  Last heartbeat: {status['registered_info']['last_heartbeat']}")

# --- DEMO 3: BROADCAST EVENT ---
print("\n\n3️⃣  BROADCASTING EVENT")
print("-" * 60)
print("Service 1 broadcasting: 'Hey everyone, I just processed 100 records!'")

service1.broadcast('data_processed', {
    'records': 100,
    'duration': 2.5,
    'timestamp': time.time()
})

print("✅ Event broadcasted to all services!")

# --- DEMO 4: DIRECT MESSAGE ---
print("\n\n4️⃣  SENDING DIRECT MESSAGE")
print("-" * 60)
print("Service 1 sending private message to Service 3...")

service1.broadcast('backup_request', {
    'data': 'important_file.json',
    'priority': 'high'
}, targets=['demo_api_3'])  # Only Service 3 gets this

print("✅ Message sent directly to Service 3!")

# Check if Service 3 received it
messages = service3.get_messages()
if messages:
    print(f"\nService 3 received {len(messages)} messages:")
    for msg in messages:
        print(f"  From: {msg['from']}")
        print(f"  Type: {msg['type']}")
        print(f"  Data: {msg['data']}")

# --- DEMO 5: MULTI-CHANNEL LOGGING ---
print("\n\n5️⃣  MULTI-CHANNEL LOGGING")
print("-" * 60)

comm.info("Normal operation - processing requests")
comm.warning("API rate limit at 80%")
comm.error("Database connection timeout")
comm.critical("DISK SPACE BELOW 5%!")

print("✅ Messages logged to console, file, and Nervous System!")

# --- DEMO 6: STUCK USER ALERT ---
print("\n\n6️⃣  STUCK USER ALERT (Triggers Alarm)")
print("-" * 60)

comm.stuck_user('user_789', '/dashboard', 'Page not refreshing')
comm.stuck_user('user_790', '/dashboard', 'Page not refreshing')
comm.stuck_user('user_791', '/dashboard', 'Page not refreshing')

print("✅ 3 stuck users reported - Alarm System will detect this!")

# --- DEMO 7: HEARTBEAT MONITORING ---
print("\n\n7️⃣  HEARTBEAT MONITORING")
print("-" * 60)
print("Services are sending heartbeats every 30 seconds...")
print("If a service stops, Nervous System marks it as DEAD")
print("\nLet's simulate Service 3 dying...")

service3.stop()
print("❌ Service 3 stopped sending heartbeats")

print("\nWaiting 65 seconds for Nervous System to detect it's dead...")
print("(In real usage, you'd see this in the Alarm System)")

# --- DEMO 8: SERVICE-TO-SERVICE ASK ---
print("\n\n8️⃣  SERVICE-TO-SERVICE REQUEST")
print("-" * 60)
print("Service 1 asking Service 2: 'Hey, can you authenticate this user?'")

# Note: This would work if Service 2 actually had a /process endpoint
# For now, we're just demonstrating the communication path
result = comm.ask_service('demo_api_2', '/authenticate', {
    'user_id': 'user_123',
    'token': 'abc123'
})

if result:
    print("✅ Request sent successfully!")
else:
    print("⚠️  Service 2 doesn't have /authenticate endpoint (expected for demo)")

# --- FINAL STATUS ---
print("\n\n" + "=" * 60)
print("📊 FINAL STATUS")
print("=" * 60)

services = service1.list_services()
print(f"\nTotal services: {services['total']}")
print(f"Online: {services['online']}")
print(f"Dead: {services['dead']}")

print("\n✅ DEMO COMPLETE!")
print("\nWhat we demonstrated:")
print("  1️⃣  Service discovery")
print("  2️⃣  'Tap on shoulder' queries")
print("  3️⃣  Event broadcasting")
print("  4️⃣  Direct messaging")
print("  5️⃣  Multi-channel logging")
print("  6️⃣  Stuck user alerts")
print("  7️⃣  Heartbeat monitoring")
print("  8️⃣  Service-to-service requests")

print("\n🧠 The Nervous System connects everything!")
print("   View status: http://localhost:7776/system/status")
print("   View events: http://localhost:7776/events")
print("   Query service: http://localhost:7776/query/<service_id>")

# Clean up
print("\n🔌 Stopping services...")
service1.stop()
service2.stop()
# service3 already stopped

print("\n" + "=" * 60)
