"""
ROGUE ACTIVITY TRACKER
Scans file system for changes, tracks who created what, and generates rollback data
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import time

# Configuration
WATCH_DIRS = [
    r"C:\Users\dwrek\100X_DEPLOYMENT",
    r"C:\Users\dwrek\Desktop",
    r"C:\Users\dwrek"
]

IGNORE_DIRS = [
    "node_modules",
    ".git",
    "__pycache__",
    "DAILY_BACKUPS",
    "TRINITY_OFFLINE_MIRROR"
]

ACTIVITY_LOG = r"C:\Users\dwrek\100X_DEPLOYMENT\ACTIVITY_DATA\activity_log.json"
FILE_INVENTORY = r"C:\Users\dwrek\100X_DEPLOYMENT\ACTIVITY_DATA\file_inventory.json"

# Create activity data directory if it doesn't exist
os.makedirs(r"C:\Users\dwrek\100X_DEPLOYMENT\ACTIVITY_DATA", exist_ok=True)


def get_file_hash(filepath):
    """Get MD5 hash of file for change detection"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None


def get_file_info(filepath):
    """Get comprehensive file info"""
    try:
        stat = os.stat(filepath)
        return {
            "path": str(filepath),
            "name": os.path.basename(filepath),
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "hash": get_file_hash(filepath)
        }
    except:
        return None


def scan_directory(directory, max_depth=5, current_depth=0):
    """Recursively scan directory for files"""
    files = []

    if current_depth > max_depth:
        return files

    try:
        for item in os.listdir(directory):
            # Skip ignored directories
            if any(ignore in item for ignore in IGNORE_DIRS):
                continue

            item_path = os.path.join(directory, item)

            if os.path.isfile(item_path):
                info = get_file_info(item_path)
                if info:
                    files.append(info)

            elif os.path.isdir(item_path):
                files.extend(scan_directory(item_path, max_depth, current_depth + 1))

    except Exception as e:
        print(f"Error scanning {directory}: {e}")

    return files


def find_new_files(current_inventory, previous_inventory):
    """Find files that were created since last scan"""
    current_paths = {f["path"] for f in current_inventory}
    previous_paths = {f["path"] for f in previous_inventory} if previous_inventory else set()

    new_paths = current_paths - previous_paths
    return [f for f in current_inventory if f["path"] in new_paths]


def find_modified_files(current_inventory, previous_inventory):
    """Find files that were modified since last scan"""
    if not previous_inventory:
        return []

    previous_map = {f["path"]: f["hash"] for f in previous_inventory}
    modified = []

    for f in current_inventory:
        path = f["path"]
        if path in previous_map and f["hash"] != previous_map[path]:
            modified.append(f)

    return modified


def find_deleted_files(current_inventory, previous_inventory):
    """Find files that were deleted since last scan"""
    if not previous_inventory:
        return []

    current_paths = {f["path"] for f in current_inventory}
    previous_paths = {f["path"] for f in previous_inventory}

    deleted_paths = previous_paths - current_paths
    return [f for f in previous_inventory if f["path"] in deleted_paths]


def detect_suspicious_patterns(new_files, modified_files, time_window_hours=6):
    """Detect suspicious activity patterns"""
    alerts = []

    # Check for high-volume creation
    if len(new_files) > 30:
        alerts.append({
            "type": "HIGH_VOLUME_CREATION",
            "severity": "MEDIUM",
            "message": f"{len(new_files)} files created in last scan",
            "timestamp": datetime.now().isoformat()
        })

    # Check for rapid modifications
    if len(modified_files) > 50:
        alerts.append({
            "type": "HIGH_VOLUME_MODIFICATION",
            "severity": "MEDIUM",
            "message": f"{len(modified_files)} files modified in last scan",
            "timestamp": datetime.now().isoformat()
        })

    # Check for large files
    large_files = [f for f in new_files if f["size"] > 10 * 1024 * 1024]  # > 10MB
    if large_files:
        alerts.append({
            "type": "LARGE_FILE_CREATED",
            "severity": "LOW",
            "message": f"{len(large_files)} large files (>10MB) created",
            "files": [f["name"] for f in large_files],
            "timestamp": datetime.now().isoformat()
        })

    return alerts


def guess_creator(filepath, new_files_batch):
    """Try to guess who created the file based on patterns"""
    filename = os.path.basename(filepath).lower()

    # Check for AI agent patterns
    if any(x in filename for x in ['claude', 'stonehenge', 'seven_domains', 'trinity', 'araya']):
        return "Claude AI Agent"

    # Check for user patterns
    if 'joshua' in filename or 'serrano' in filename:
        return "Joshua Serrano (PIN 1001)"

    if 'toby' in filename:
        return "Toby Burrowes (PIN 1002)"

    if 'dean' in filename or '47.ind' in filename:
        return "Dean Sabr (PIN 1004)"

    # Check for suspicious patterns
    if len(new_files_batch) > 30:
        return "🐯 TESTOSTERONE TIGER (Unknown)"

    # Check file creation time
    try:
        stat = os.stat(filepath)
        hour = datetime.fromtimestamp(stat.st_ctime).hour

        # Late night activity is suspicious
        if 0 <= hour < 6:
            return "Unknown (Late Night Activity)"
    except:
        pass

    return "Unknown Creator"


def generate_activity_report():
    """Generate comprehensive activity report"""
    print("🔍 SCANNING FILE SYSTEM...")
    print(f"Watching directories: {len(WATCH_DIRS)}")
    print()

    # Load previous inventory
    previous_inventory = []
    if os.path.exists(FILE_INVENTORY):
        try:
            with open(FILE_INVENTORY, 'r') as f:
                previous_inventory = json.load(f)
        except:
            pass

    # Scan current state
    current_inventory = []
    for directory in WATCH_DIRS:
        if os.path.exists(directory):
            print(f"Scanning: {directory}")
            files = scan_directory(directory)
            current_inventory.extend(files)
            print(f"  Found: {len(files)} files")

    print(f"\nTotal files tracked: {len(current_inventory)}")

    # Find changes
    new_files = find_new_files(current_inventory, previous_inventory)
    modified_files = find_modified_files(current_inventory, previous_inventory)
    deleted_files = find_deleted_files(current_inventory, previous_inventory)

    print(f"\n📊 CHANGES DETECTED:")
    print(f"  New files: {len(new_files)}")
    print(f"  Modified: {len(modified_files)}")
    print(f"  Deleted: {len(deleted_files)}")

    # Detect suspicious patterns
    alerts = detect_suspicious_patterns(new_files, modified_files)

    if alerts:
        print(f"\n⚠️  ALERTS: {len(alerts)}")
        for alert in alerts:
            print(f"  [{alert['severity']}] {alert['type']}: {alert['message']}")

    # Guess creators for new files
    creators_stats = {}
    for f in new_files[-50:]:  # Last 50 new files
        creator = guess_creator(f["path"], new_files)
        creators_stats[creator] = creators_stats.get(creator, 0) + 1

    if creators_stats:
        print(f"\n👤 TOP CREATORS (Last 50 new files):")
        for creator, count in sorted(creators_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {creator}: {count} files")

    # Generate activity log entry
    activity_entry = {
        "timestamp": datetime.now().isoformat(),
        "scan_completed": True,
        "total_files": len(current_inventory),
        "changes": {
            "new": len(new_files),
            "modified": len(modified_files),
            "deleted": len(deleted_files)
        },
        "new_files_sample": new_files[-20:],  # Last 20 new files
        "modified_files_sample": modified_files[-20:],  # Last 20 modified
        "creators_stats": creators_stats,
        "alerts": alerts,
        "rollback_points": []
    }

    # Save current inventory for next scan
    with open(FILE_INVENTORY, 'w') as f:
        json.dump(current_inventory, f, indent=2)

    # Append to activity log
    activity_log = []
    if os.path.exists(ACTIVITY_LOG):
        try:
            with open(ACTIVITY_LOG, 'r') as f:
                activity_log = json.load(f)
        except:
            pass

    activity_log.append(activity_entry)

    # Keep only last 100 entries
    if len(activity_log) > 100:
        activity_log = activity_log[-100:]

    with open(ACTIVITY_LOG, 'w') as f:
        json.dump(activity_log, f, indent=2)

    print(f"\n✅ Activity log saved to: {ACTIVITY_LOG}")
    print(f"✅ File inventory saved to: {FILE_INVENTORY}")

    return activity_entry


def watch_continuous(interval_seconds=300):
    """Continuously watch for changes"""
    print("🔍 STARTING CONTINUOUS MONITORING")
    print(f"Scan interval: {interval_seconds} seconds ({interval_seconds/60} minutes)")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            print(f"\n{'='*60}")
            print(f"SCAN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}")

            generate_activity_report()

            print(f"\nNext scan in {interval_seconds} seconds...")
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        # Continuous monitoring mode
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        watch_continuous(interval)
    else:
        # Single scan mode
        generate_activity_report()
        print("\n💡 TIP: Run with --watch to enable continuous monitoring")
        print("   Example: python TRACK_ALL_ACTIVITY.py --watch 300")
