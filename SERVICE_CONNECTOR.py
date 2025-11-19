"""
SERVICE CONNECTOR
Add this to any service to connect it to the Nervous System

Usage:
    from SERVICE_CONNECTOR import ServiceConnector

    connector = ServiceConnector(
        service_id='araya_api',
        name='Araya Intelligent Terminal',
        url='http://localhost:6666',
        port=6666,
        capabilities=['chat', 'computer_control', 'file_operations']
    )

    connector.start()  # Starts heartbeat and registration

    # Broadcast events
    connector.broadcast('user_message', {'user': 'Commander', 'message': 'Hello'})

    # Query other services
    status = connector.query('trinity_api')

    # Ask other services to do things
    response = connector.ask('c1_mechanic', '/build', {'task': 'Fix bug'})
"""
import requests
import threading
import time
from datetime import datetime


class ServiceConnector:
    def __init__(self, service_id, name, url, port, service_type='general', capabilities=None, metadata=None):
        self.service_id = service_id
        self.name = name
        self.url = url
        self.port = port
        self.service_type = service_type
        self.capabilities = capabilities or []
        self.metadata = metadata or {}

        self.nervous_system_url = 'http://localhost:7776'
        self.heartbeat_interval = 30  # seconds
        self.running = False
        self.heartbeat_thread = None

    def register(self):
        """Register with the nervous system"""
        try:
            response = requests.post(f'{self.nervous_system_url}/register', json={
                'service_id': self.service_id,
                'name': self.name,
                'url': self.url,
                'port': self.port,
                'type': self.service_type,
                'capabilities': self.capabilities,
                'metadata': self.metadata
            }, timeout=5)

            if response.status_code == 200:
                print(f"✅ {self.name} registered with Nervous System")
                return True
            else:
                print(f"❌ Failed to register {self.name}")
                return False
        except Exception as e:
            print(f"❌ Could not connect to Nervous System: {e}")
            return False

    def heartbeat(self):
        """Send heartbeat to nervous system"""
        try:
            response = requests.post(f'{self.nervous_system_url}/heartbeat', json={
                'service_id': self.service_id,
                'metadata': self.metadata  # Updated metadata
            }, timeout=5)

            return response.status_code == 200
        except:
            return False

    def heartbeat_loop(self):
        """Background thread that sends heartbeats"""
        while self.running:
            self.heartbeat()
            time.sleep(self.heartbeat_interval)

    def start(self):
        """Start the connector (register + heartbeat)"""
        if self.register():
            self.running = True
            self.heartbeat_thread = threading.Thread(target=self.heartbeat_loop, daemon=True)
            self.heartbeat_thread.start()
            print(f"🧠 {self.name} connected to Nervous System")
            return True
        return False

    def stop(self):
        """Stop the connector"""
        self.running = False
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=2)
        print(f"🔌 {self.name} disconnected from Nervous System")

    def broadcast(self, event_type, data, targets=None):
        """Broadcast an event to the nervous system"""
        try:
            response = requests.post(f'{self.nervous_system_url}/broadcast', json={
                'service_id': self.service_id,
                'event_type': event_type,
                'data': data,
                'targets': targets  # Optional: specific services to notify
            }, timeout=5)

            return response.status_code == 200
        except:
            return False

    def query(self, target_service_id):
        """Query what another service is doing"""
        try:
            response = requests.get(f'{self.nervous_system_url}/query/{target_service_id}', timeout=5)

            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def ask(self, target_service_id, endpoint='/process', data=None):
        """Ask another service to do something"""
        try:
            response = requests.post(f'{self.nervous_system_url}/ask/{target_service_id}', json={
                'endpoint': endpoint,
                'data': data or {},
                'from': self.service_id
            }, timeout=10)

            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def get_messages(self):
        """Get messages sent to this service"""
        try:
            response = requests.get(f'{self.nervous_system_url}/messages/{self.service_id}', timeout=5)

            if response.status_code == 200:
                return response.json().get('messages', [])
            return []
        except:
            return []

    def update_metadata(self, **kwargs):
        """Update service metadata"""
        self.metadata.update(kwargs)

    def list_services(self):
        """Get list of all services in the system"""
        try:
            response = requests.get(f'{self.nervous_system_url}/services', timeout=5)

            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None


# Example usage
if __name__ == '__main__':
    print("\n🧠 SERVICE CONNECTOR TEST 🧠\n")

    # Create connector
    connector = ServiceConnector(
        service_id='test_service',
        name='Test Service',
        url='http://localhost:9999',
        port=9999,
        capabilities=['testing', 'demo']
    )

    # Start (register + heartbeat)
    if connector.start():
        print("\n✅ Connector started!")

        # Update metadata
        connector.update_metadata(users=0, requests=0)

        # Broadcast event
        connector.broadcast('test_event', {'message': 'Hello from test service!'})

        # List all services
        services = connector.list_services()
        print(f"\n📋 Found {services['total']} services in system")

        # Keep running for 30 seconds to show heartbeat
        print("\n⏳ Running for 30 seconds to demonstrate heartbeat...")
        time.sleep(30)

        # Stop
        connector.stop()
        print("\n✅ Connector test complete!")
    else:
        print("\n❌ Could not start connector - is Nervous System running on port 7777?")
