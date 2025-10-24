"""
COMMUNICATION CHANNELS
All the ways services can talk to each other and alert humans

Channels:
1. Nervous System Events (service-to-service)
2. Alarm System (automated monitoring)
3. Dashboard Updates (visual feedback)
4. Browser Notifications (user alerts)
5. Console Logging (debug info)
6. File Logging (permanent record)
7. Email Alerts (critical issues) - TODO
8. SMS Alerts (emergency) - TODO
"""
import json
import requests
from datetime import datetime
from pathlib import Path

# Logs directory
LOGS_DIR = Path('C:/Users/dwrek/100X_DEPLOYMENT/COMMUNICATION_LOGS')
LOGS_DIR.mkdir(exist_ok=True)


class CommunicationHub:
    """Central hub for all communication"""

    def __init__(self, service_id, service_name):
        self.service_id = service_id
        self.service_name = service_name
        self.nervous_system = 'http://localhost:7776'

    def log_to_file(self, channel, level, message, data=None):
        """Log message to file"""
        log_file = LOGS_DIR / f'{self.service_id}_{datetime.now().strftime("%Y%m%d")}.log'

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'service_id': self.service_id,
            'service_name': self.service_name,
            'channel': channel,
            'level': level,
            'message': message,
            'data': data
        }

        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def send_to_nervous_system(self, event_type, data):
        """Send event to nervous system"""
        try:
            requests.post(f'{self.nervous_system}/broadcast', json={
                'service_id': self.service_id,
                'event_type': event_type,
                'data': data
            }, timeout=2)
            return True
        except:
            return False

    def log(self, level, message, data=None, channels=None):
        """
        Log message to multiple channels

        Args:
            level: 'debug', 'info', 'warning', 'error', 'critical'
            message: Log message
            data: Additional data
            channels: List of channels to use (default: all)
        """
        channels = channels or ['console', 'file', 'nervous_system']

        # Console output
        if 'console' in channels:
            level_icons = {
                'debug': '🔍',
                'info': 'ℹ️',
                'warning': '⚠️',
                'error': '❌',
                'critical': '🚨'
            }
            icon = level_icons.get(level, '📝')
            print(f"{icon} [{self.service_name}] {message}")

        # File logging
        if 'file' in channels:
            self.log_to_file('file', level, message, data)

        # Nervous system event
        if 'nervous_system' in channels:
            self.send_to_nervous_system(level, {
                'message': message,
                'data': data
            })

    def info(self, message, data=None):
        """Info level message"""
        self.log('info', message, data)

    def warning(self, message, data=None):
        """Warning level message"""
        self.log('warning', message, data)

    def error(self, message, data=None):
        """Error level message"""
        self.log('error', message, data)

    def critical(self, message, data=None):
        """Critical level message"""
        self.log('critical', message, data)

    def debug(self, message, data=None):
        """Debug level message"""
        self.log('debug', message, data, channels=['console', 'file'])

    def user_event(self, event_type, user_id, data=None):
        """Log a user event"""
        self.log('info', f'User event: {event_type}', {
            'user_id': user_id,
            'event': event_type,
            'data': data
        })

    def stuck_user(self, user_id, location, reason):
        """Report a stuck user (triggers alarm system)"""
        self.log('warning', f'User {user_id} stuck at {location}', {
            'user_id': user_id,
            'location': location,
            'reason': reason
        }, channels=['console', 'file', 'nervous_system'])

        # Send specific stuck event
        self.send_to_nervous_system('user_stuck', {
            'user_id': user_id,
            'location': location,
            'reason': reason
        })

    def tap_on_shoulder(self, target_service_id, question):
        """
        Ask another service what it's doing
        This is the "tap on shoulder" Commander requested
        """
        try:
            response = requests.get(f'{self.nervous_system}/query/{target_service_id}', timeout=5)

            if response.status_code == 200:
                status = response.json()
                self.info(f"Queried {target_service_id}", status)
                return status
            else:
                self.warning(f"Could not query {target_service_id}")
                return None
        except Exception as e:
            self.error(f"Error querying {target_service_id}: {e}")
            return None

    def ask_service(self, target_service_id, endpoint, data=None):
        """Ask another service to do something"""
        try:
            response = requests.post(f'{self.nervous_system}/ask/{target_service_id}', json={
                'endpoint': endpoint,
                'data': data or {},
                'from': self.service_id
            }, timeout=10)

            if response.status_code == 200:
                result = response.json()
                self.info(f"Asked {target_service_id} to {endpoint}", result)
                return result
            else:
                self.warning(f"Failed to ask {target_service_id}")
                return None
        except Exception as e:
            self.error(f"Error asking {target_service_id}: {e}")
            return None


# Example usage
if __name__ == '__main__':
    print("\n🔊 COMMUNICATION CHANNELS TEST 🔊\n")

    # Create communication hub
    comm = CommunicationHub('test_service', 'Test Service')

    # Different log levels
    comm.debug("Debug message - verbose info")
    comm.info("Info message - normal operation")
    comm.warning("Warning message - something to watch")
    comm.error("Error message - something went wrong")
    comm.critical("Critical message - immediate action needed")

    # User events
    comm.user_event('page_view', 'user_123', {'page': '/dashboard'})
    comm.user_event('button_click', 'user_123', {'button': 'start_tour'})

    # Stuck user
    comm.stuck_user('user_456', '/police-accountability', 'refresh not working')

    # Tap on shoulder
    print("\n--- Tap on Shoulder Test ---")
    status = comm.tap_on_shoulder('trinity_api', 'What are you doing?')
    print(f"Status: {status}")

    print("\n✅ Communication channels test complete!")
    print(f"Check logs at: {LOGS_DIR}")
