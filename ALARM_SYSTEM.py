"""
ALARM & NOTIFICATION SYSTEM
Watches for problems and SCREAMS when something's wrong

This monitors the Nervous System and triggers alarms when:
- Services go offline
- Users get stuck
- Errors spike
- System health degrades
- APIs stop responding
"""
import requests
import time
from datetime import datetime
from collections import defaultdict

NERVOUS_SYSTEM_URL = 'http://localhost:7776'
CHECK_INTERVAL = 10  # seconds

# Alarm thresholds
THRESHOLDS = {
    'service_offline': 1,  # Alarm if 1+ services offline
    'dead_services': 1,    # Alarm if 1+ services dead
    'stuck_users': 2,      # Alarm if 2+ users stuck
    'error_spike': 5,      # Alarm if 5+ errors in 60 seconds
    'no_heartbeat': 60     # Alarm if no heartbeat for 60 seconds
}

# Alarm state
ALARMS = []
ALARM_HISTORY = []
ERROR_COUNT = defaultdict(int)


def trigger_alarm(alarm_type, severity, message, data=None):
    """Trigger an alarm"""
    alarm = {
        'type': alarm_type,
        'severity': severity,  # 'critical', 'warning', 'info'
        'message': message,
        'data': data or {},
        'timestamp': datetime.now().isoformat()
    }

    ALARMS.append(alarm)
    ALARM_HISTORY.append(alarm)

    # Keep only recent alarms
    if len(ALARM_HISTORY) > 100:
        ALARM_HISTORY.pop(0)

    # Print alarm to console
    severity_icons = {
        'critical': '🚨',
        'warning': '⚠️',
        'info': 'ℹ️'
    }

    icon = severity_icons.get(severity, '🔔')
    print(f"\n{icon} ALARM [{severity.upper()}]: {message}")
    if data:
        print(f"   Data: {data}")

    # TODO: Send to notification channels (email, SMS, dashboard popup, etc.)

    return alarm


def clear_alarm(alarm_type):
    """Clear alarms of a specific type"""
    global ALARMS
    ALARMS = [a for a in ALARMS if a['type'] != alarm_type]


def check_service_health():
    """Check if services are healthy"""
    try:
        response = requests.get(f'{NERVOUS_SYSTEM_URL}/system/status', timeout=5)

        if response.status_code != 200:
            trigger_alarm('nervous_system', 'critical', 'Nervous System not responding!')
            return

        status = response.json()

        # Check for dead services
        if status['dead'] >= THRESHOLDS['dead_services']:
            dead_services = status['services']['dead']
            trigger_alarm('dead_services', 'critical', f"{status['dead']} services are DEAD!", {
                'dead_services': dead_services
            })
        else:
            clear_alarm('dead_services')

        # Check system health
        if status['system_health'] == 'critical':
            trigger_alarm('system_health', 'critical', 'System health is CRITICAL!', {
                'online': status['online'],
                'total': status['total_services']
            })
        else:
            clear_alarm('system_health')

        # Check for error events
        recent_events = status.get('recent_events', [])
        error_events = [e for e in recent_events if e.get('type') == 'error']

        if len(error_events) >= THRESHOLDS['error_spike']:
            trigger_alarm('error_spike', 'warning', f'{len(error_events)} errors detected!', {
                'errors': error_events[:5]  # Show first 5
            })

    except Exception as e:
        trigger_alarm('monitor_error', 'warning', f'Could not check system health: {e}')


def check_stuck_users():
    """Check for stuck users via analytics"""
    try:
        # TODO: Connect to analytics API to get stuck user count
        # For now, simulate by checking events
        response = requests.get(f'{NERVOUS_SYSTEM_URL}/events?limit=100', timeout=5)

        if response.status_code == 200:
            events = response.json().get('events', [])
            stuck_events = [e for e in events if e.get('type') == 'user_stuck']

            if len(stuck_events) >= THRESHOLDS['stuck_users']:
                trigger_alarm('stuck_users', 'warning', f'{len(stuck_events)} users are stuck!', {
                    'stuck_count': len(stuck_events)
                })
            else:
                clear_alarm('stuck_users')

    except Exception as e:
        pass  # Don't alarm on this check failure


def monitor_loop():
    """Main monitoring loop"""
    print("\n" + "=" * 60)
    print("🚨 ALARM SYSTEM MONITORING 🚨")
    print("=" * 60)
    print(f"\nMonitoring Nervous System at {NERVOUS_SYSTEM_URL}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print("\nThresholds:")
    for key, value in THRESHOLDS.items():
        print(f"  {key}: {value}")
    print("\n" + "=" * 60)
    print("Monitoring started...\n")

    iteration = 0

    while True:
        iteration += 1

        # Run checks
        check_service_health()
        check_stuck_users()

        # Status update every 6 iterations (60 seconds)
        if iteration % 6 == 0:
            active_alarms = len(ALARMS)
            if active_alarms > 0:
                print(f"\n⚠️  {active_alarms} ACTIVE ALARMS")
            else:
                print(f"\n✅ System OK - No active alarms")

        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    try:
        monitor_loop()
    except KeyboardInterrupt:
        print("\n\n🔌 Alarm system stopped")
        print(f"Total alarms triggered: {len(ALARM_HISTORY)}")
