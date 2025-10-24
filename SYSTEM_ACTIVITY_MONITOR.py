"""
SYSTEM ACTIVITY MONITOR
Track everything happening in the system:
- File changes (newest additions)
- User activity (who's stuck, who's active)
- Service activity (what's being added/edited)
- System modifications

Commander's request: "How do we make sure nobody's getting stuck or that it's even added at all"
"""
import os
import time
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import hashlib

# Directories to monitor
MONITORED_DIRS = [
    Path('C:/Users/dwrek/100X_DEPLOYMENT'),
    Path('C:/Users/dwrek/100X_DEPLOYMENT/META_LAYER_SYSTEM')
]

# Data storage
ACTIVITY_LOG = []
FILE_HASHES = {}
USER_ACTIVITY = defaultdict(list)
STUCK_USERS = {}

DATA_DIR = Path('C:/Users/dwrek/100X_DEPLOYMENT/ACTIVITY_DATA')
DATA_DIR.mkdir(exist_ok=True)


def get_file_hash(file_path):
    """Get MD5 hash of file"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None


def scan_for_changes():
    """Scan directories for new/modified files"""
    global FILE_HASHES

    changes = {
        'new_files': [],
        'modified_files': [],
        'deleted_files': []
    }

    current_files = {}

    # Scan all monitored directories
    for base_dir in MONITORED_DIRS:
        if not base_dir.exists():
            continue

        for file_path in base_dir.rglob('*'):
            if file_path.is_file():
                # Skip certain files
                if any(skip in str(file_path) for skip in ['.git', '__pycache__', '.pyc', 'node_modules']):
                    continue

                file_hash = get_file_hash(file_path)
                if file_hash:
                    current_files[str(file_path)] = {
                        'hash': file_hash,
                        'size': file_path.stat().st_size,
                        'modified': file_path.stat().st_mtime
                    }

    # Compare with previous scan
    for file_path, info in current_files.items():
        if file_path not in FILE_HASHES:
            # New file!
            changes['new_files'].append({
                'path': file_path,
                'name': Path(file_path).name,
                'size': info['size'],
                'modified': datetime.fromtimestamp(info['modified']).isoformat()
            })
        elif FILE_HASHES[file_path]['hash'] != info['hash']:
            # Modified file!
            changes['modified_files'].append({
                'path': file_path,
                'name': Path(file_path).name,
                'size': info['size'],
                'modified': datetime.fromtimestamp(info['modified']).isoformat()
            })

    # Check for deleted files
    for file_path in FILE_HASHES:
        if file_path not in current_files:
            changes['deleted_files'].append({
                'path': file_path,
                'name': Path(file_path).name
            })

    # Update file hashes
    FILE_HASHES = current_files

    return changes


def log_activity(activity_type, data):
    """Log an activity"""
    activity = {
        'type': activity_type,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }

    ACTIVITY_LOG.append(activity)

    # Keep only last 1000 activities
    if len(ACTIVITY_LOG) > 1000:
        ACTIVITY_LOG.pop(0)

    # Save to disk
    log_file = DATA_DIR / f'activity_{datetime.now().strftime("%Y%m%d")}.jsonl'
    with open(log_file, 'a') as f:
        f.write(json.dumps(activity) + '\n')

    return activity


def check_stuck_users():
    """Check for stuck users by querying Nervous System"""
    global STUCK_USERS

    try:
        import requests
        response = requests.get('http://localhost:7776/events?limit=100', timeout=5)
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])

            # Look for stuck user events
            stuck_events = [e for e in events if e.get('type') == 'user_stuck']

            # Count stuck events per user
            stuck_counts = defaultdict(int)
            for event in stuck_events:
                user_id = event.get('data', {}).get('user_id')
                if user_id:
                    stuck_counts[user_id] += 1

            # Update stuck users
            STUCK_USERS = {
                user_id: {
                    'count': count,
                    'last_stuck': datetime.now().isoformat(),
                    'needs_help': count >= 2
                }
                for user_id, count in stuck_counts.items()
            }

            return STUCK_USERS
    except:
        pass

    return {}


def get_newest_additions(limit=20):
    """Get newest file additions"""
    changes = scan_for_changes()

    # Combine new and modified
    all_changes = []

    for file in changes['new_files']:
        file['change_type'] = 'NEW'
        all_changes.append(file)

    for file in changes['modified_files']:
        file['change_type'] = 'MODIFIED'
        all_changes.append(file)

    # Sort by modification time
    all_changes.sort(key=lambda x: x['modified'], reverse=True)

    return all_changes[:limit]


def get_activity_summary():
    """Get summary of recent activity"""
    # Scan for changes
    changes = scan_for_changes()

    # Check stuck users
    stuck = check_stuck_users()

    # Get recent activity from Nervous System
    recent_events = []
    try:
        import requests
        response = requests.get('http://localhost:7776/events?limit=20', timeout=5)
        if response.status_code == 200:
            data = response.json()
            recent_events = data.get('events', [])
    except:
        pass

    summary = {
        'timestamp': datetime.now().isoformat(),
        'file_changes': {
            'new': len(changes['new_files']),
            'modified': len(changes['modified_files']),
            'deleted': len(changes['deleted_files'])
        },
        'newest_additions': get_newest_additions(10),
        'stuck_users': stuck,
        'stuck_count': len([u for u in stuck.values() if u['needs_help']]),
        'recent_events': recent_events,
        'system_health': 'healthy' if len(stuck) == 0 else 'warning'
    }

    return summary


def monitor_loop(interval=30):
    """Main monitoring loop"""
    print("\n" + "=" * 60)
    print("📊 SYSTEM ACTIVITY MONITOR")
    print("=" * 60)
    print(f"\nMonitoring directories:")
    for dir in MONITORED_DIRS:
        print(f"  • {dir}")
    print(f"\nCheck interval: {interval} seconds")
    print("=" * 60 + "\n")

    iteration = 0

    while True:
        iteration += 1
        print(f"\n⏰ Check #{iteration} - {datetime.now().strftime('%H:%M:%S')}")

        # Get activity summary
        summary = get_activity_summary()

        # Report changes
        if summary['file_changes']['new'] > 0:
            print(f"   ✨ {summary['file_changes']['new']} NEW files")
            for file in summary['newest_additions'][:3]:
                if file['change_type'] == 'NEW':
                    print(f"      • {file['name']}")

        if summary['file_changes']['modified'] > 0:
            print(f"   📝 {summary['file_changes']['modified']} MODIFIED files")
            for file in summary['newest_additions'][:3]:
                if file['change_type'] == 'MODIFIED':
                    print(f"      • {file['name']}")

        if summary['file_changes']['deleted'] > 0:
            print(f"   🗑️  {summary['file_changes']['deleted']} DELETED files")

        # Report stuck users
        if summary['stuck_count'] > 0:
            print(f"\n   ⚠️  {summary['stuck_count']} users STUCK and need help!")
            for user_id, info in summary['stuck_users'].items():
                if info['needs_help']:
                    print(f"      • {user_id} (stuck {info['count']} times)")

        # Log activity
        if summary['file_changes']['new'] > 0 or summary['file_changes']['modified'] > 0:
            log_activity('file_changes', summary['file_changes'])

        if summary['stuck_count'] > 0:
            log_activity('stuck_users_detected', summary['stuck_users'])

        # Save summary
        summary_file = DATA_DIR / 'latest_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        time.sleep(interval)


if __name__ == '__main__':
    try:
        # Initial scan
        print("🔍 Performing initial scan...")
        scan_for_changes()
        print("✅ Initial scan complete\n")

        # Start monitoring
        monitor_loop(interval=30)
    except KeyboardInterrupt:
        print("\n\n🔌 Activity Monitor stopped")
        print(f"Logged {len(ACTIVITY_LOG)} activities")
