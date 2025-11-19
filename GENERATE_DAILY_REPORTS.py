"""
DAILY ACTIVITY REPORTS
Generates end-of-day summary showing what each person created
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Configuration
ACTIVITY_LOG = r"C:\Users\dwrek\100X_DEPLOYMENT\ACTIVITY_DATA\activity_log.json"
DAILY_REPORTS_DIR = r"C:\Users\dwrek\100X_DEPLOYMENT\DAILY_REPORTS"
BETA_USERS_DB = r"C:\Users\dwrek\100X_DEPLOYMENT\BETA_USERS_DATABASE.json"

# Create reports directory
os.makedirs(DAILY_REPORTS_DIR, exist_ok=True)


def load_beta_users():
    """Load beta user database for name matching"""
    try:
        with open(BETA_USERS_DB, 'r') as f:
            data = json.load(f)
            return data.get('users', {})
    except:
        return {}


def load_activity_log():
    """Load activity log"""
    try:
        with open(ACTIVITY_LOG, 'r') as f:
            return json.load(f)
    except:
        return []


def get_todays_activity(activity_log):
    """Get all activity from today"""
    today = datetime.now().date()
    todays_entries = []

    for entry in activity_log:
        try:
            entry_date = datetime.fromisoformat(entry['timestamp']).date()
            if entry_date == today:
                todays_entries.append(entry)
        except:
            continue

    return todays_entries


def get_date_activity(activity_log, target_date):
    """Get activity from specific date"""
    if isinstance(target_date, str):
        target_date = datetime.fromisoformat(target_date).date()

    date_entries = []

    for entry in activity_log:
        try:
            entry_date = datetime.fromisoformat(entry['timestamp']).date()
            if entry_date == target_date:
                date_entries.append(entry)
        except:
            continue

    return date_entries


def categorize_files_by_creator(entries):
    """Group files by who created them"""
    creator_files = defaultdict(lambda: {
        'new': [],
        'modified': [],
        'total_new': 0,
        'total_modified': 0,
        'file_sizes': []
    })

    for entry in entries:
        # Process new files
        if 'new_files_sample' in entry:
            for file_info in entry['new_files_sample']:
                # Guess creator from filename or path
                creator = guess_creator_from_file(file_info)
                creator_files[creator]['new'].append(file_info)
                creator_files[creator]['total_new'] += 1
                if 'size' in file_info:
                    creator_files[creator]['file_sizes'].append(file_info['size'])

        # Process modified files
        if 'modified_files_sample' in entry:
            for file_info in entry['modified_files_sample']:
                creator = guess_creator_from_file(file_info)
                creator_files[creator]['modified'].append(file_info)
                creator_files[creator]['total_modified'] += 1

        # Use creator stats if available
        if 'creators_stats' in entry:
            for creator, count in entry['creators_stats'].items():
                if creator not in creator_files:
                    creator_files[creator]['total_new'] = count

    return dict(creator_files)


def guess_creator_from_file(file_info):
    """Guess creator from file path/name"""
    path = file_info.get('path', '').lower()
    name = file_info.get('name', '').lower()

    # AI agent patterns
    if any(x in path or x in name for x in ['claude', 'stonehenge', 'seven_domains', 'trinity', 'araya', 'consciousness']):
        return "🤖 Claude AI Agent"

    # Beta tester patterns
    if 'joshua' in path or 'serrano' in path:
        return "Joshua Serrano (PIN 1001)"

    if 'toby' in path or 'burrowes' in path:
        return "Toby Burrowes (PIN 1002)"

    if 'dean' in path or 'sabr' in path:
        return "Dean Sabr (PIN 1004)"

    if 'bill' in path or 'varni' in path:
        return "Bill Varni (PIN 1005)"

    if 'angeline' in path or 'realm' in path:
        return "Angeline Realm (PIN 1007)"

    if 'crypt' in path or 'information.crypt' in path:
        return "Info Crypt (PIN 1008)"

    if 'alex' in path or 'lancaster' in path or 'hawaii' in path:
        return "Alex Lancaster (PIN 1009)"

    # Check timestamps for late-night work (suspicious)
    try:
        created = file_info.get('created', '')
        if created:
            hour = datetime.fromisoformat(created).hour
            if 0 <= hour < 6:
                return "🐯 TESTOSTERONE TIGER (Late Night Activity)"
    except:
        pass

    # Default
    return "Unknown Creator"


def format_file_size(bytes_size):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def generate_daily_report_text(date, creator_files):
    """Generate text report"""
    report = []
    report.append("=" * 80)
    report.append(f"DAILY ACTIVITY REPORT - {date.strftime('%Y-%m-%d (%A)')}")
    report.append("=" * 80)
    report.append("")

    # Summary
    total_creators = len(creator_files)
    total_new = sum(data['total_new'] for data in creator_files.values())
    total_modified = sum(data['total_modified'] for data in creator_files.values())

    report.append("📊 SUMMARY:")
    report.append(f"  Active Creators: {total_creators}")
    report.append(f"  Files Created:   {total_new}")
    report.append(f"  Files Modified:  {total_modified}")
    report.append("")

    # Sort creators by activity (most active first)
    sorted_creators = sorted(
        creator_files.items(),
        key=lambda x: x[1]['total_new'] + x[1]['total_modified'],
        reverse=True
    )

    # Per-creator breakdown
    report.append("=" * 80)
    report.append("BREAKDOWN BY CREATOR:")
    report.append("=" * 80)
    report.append("")

    for creator, data in sorted_creators:
        activity_level = data['total_new'] + data['total_modified']

        # Activity indicator
        if activity_level > 50:
            indicator = "🔥 HIGH ACTIVITY"
        elif activity_level > 20:
            indicator = "⚡ MODERATE"
        else:
            indicator = "✅ NORMAL"

        report.append("-" * 80)
        report.append(f"👤 {creator}")
        report.append(f"   {indicator}")
        report.append(f"   Created: {data['total_new']} files")
        report.append(f"   Modified: {data['total_modified']} files")

        # Average file size
        if data['file_sizes']:
            avg_size = sum(data['file_sizes']) / len(data['file_sizes'])
            report.append(f"   Avg Size: {format_file_size(avg_size)}")

        report.append("")

        # List new files (up to 20)
        if data['new']:
            report.append(f"   📁 NEW FILES ({len(data['new'])}):")
            for file_info in data['new'][:20]:
                name = file_info.get('name', 'Unknown')
                size = format_file_size(file_info.get('size', 0))
                created = file_info.get('created', 'Unknown')
                try:
                    created_time = datetime.fromisoformat(created).strftime('%H:%M:%S')
                except:
                    created_time = 'Unknown'

                report.append(f"      [{created_time}] {name} ({size})")

            if len(data['new']) > 20:
                report.append(f"      ... and {len(data['new']) - 20} more")
            report.append("")

        # List modified files (up to 10)
        if data['modified']:
            report.append(f"   ✏️  MODIFIED FILES ({len(data['modified'])}):")
            for file_info in data['modified'][:10]:
                name = file_info.get('name', 'Unknown')
                report.append(f"      {name}")

            if len(data['modified']) > 10:
                report.append(f"      ... and {len(data['modified']) - 10} more")
            report.append("")

    report.append("=" * 80)
    report.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 80)

    return "\n".join(report)


def generate_daily_report_html(date, creator_files):
    """Generate HTML report"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Daily Report - {date.strftime('%Y-%m-%d')}</title>
    <style>
        body {{
            background: #000;
            color: #0f0;
            font-family: 'Courier New', monospace;
            padding: 20px;
        }}
        .header {{
            border-bottom: 2px solid #0f0;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #0ff;
            text-shadow: 0 0 10px #0ff;
        }}
        .summary {{
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #0f0;
            padding: 15px;
            margin: 20px 0;
        }}
        .creator {{
            background: rgba(0, 255, 255, 0.05);
            border-left: 3px solid #0ff;
            padding: 15px;
            margin: 20px 0;
        }}
        .creator-name {{
            font-size: 1.2em;
            color: #0ff;
            font-weight: bold;
        }}
        .stats {{
            margin: 10px 0;
            opacity: 0.8;
        }}
        .file-list {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .file-item {{
            padding: 3px 0;
            opacity: 0.7;
        }}
        .high-activity {{
            color: #f00;
            font-weight: bold;
        }}
        .moderate {{
            color: #ff0;
        }}
        .normal {{
            color: #0f0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 DAILY ACTIVITY REPORT</h1>
        <h2>{date.strftime('%Y-%m-%d (%A)')}</h2>
    </div>
"""

    # Summary
    total_creators = len(creator_files)
    total_new = sum(data['total_new'] for data in creator_files.values())
    total_modified = sum(data['total_modified'] for data in creator_files.values())

    html += f"""
    <div class="summary">
        <h3>Summary</h3>
        <div class="stats">Active Creators: {total_creators}</div>
        <div class="stats">Files Created: {total_new}</div>
        <div class="stats">Files Modified: {total_modified}</div>
    </div>
"""

    # Per-creator breakdown
    sorted_creators = sorted(
        creator_files.items(),
        key=lambda x: x[1]['total_new'] + x[1]['total_modified'],
        reverse=True
    )

    for creator, data in sorted_creators:
        activity_level = data['total_new'] + data['total_modified']

        if activity_level > 50:
            activity_class = "high-activity"
            indicator = "🔥 HIGH ACTIVITY"
        elif activity_level > 20:
            activity_class = "moderate"
            indicator = "⚡ MODERATE"
        else:
            activity_class = "normal"
            indicator = "✅ NORMAL"

        html += f"""
    <div class="creator">
        <div class="creator-name">{creator}</div>
        <div class="stats {activity_class}">{indicator}</div>
        <div class="stats">Created: {data['total_new']} files</div>
        <div class="stats">Modified: {data['total_modified']} files</div>
"""

        if data['new']:
            html += f"""
        <div class="file-list">
            <strong>📁 New Files ({len(data['new'])}):</strong><br>
"""
            for file_info in data['new'][:20]:
                name = file_info.get('name', 'Unknown')
                html += f'            <div class="file-item">{name}</div>\n'

            if len(data['new']) > 20:
                html += f'            <div class="file-item">... and {len(data["new"]) - 20} more</div>\n'

            html += "        </div>\n"

        html += "    </div>\n"

    html += f"""
    <div style="margin-top: 40px; opacity: 0.5; text-align: center;">
        Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>
"""

    return html


def generate_todays_report():
    """Generate report for today"""
    print("📊 GENERATING DAILY REPORT FOR TODAY...")

    activity_log = load_activity_log()
    if not activity_log:
        print("❌ No activity log found. Run TRACK_ALL_ACTIVITY.py first.")
        return None

    today = datetime.now().date()
    todays_entries = get_todays_activity(activity_log)

    if not todays_entries:
        print(f"📭 No activity recorded for {today}")
        return None

    print(f"Found {len(todays_entries)} activity entries for today")

    # Categorize by creator
    creator_files = categorize_files_by_creator(todays_entries)

    # Generate reports
    text_report = generate_daily_report_text(today, creator_files)
    html_report = generate_daily_report_html(today, creator_files)

    # Save reports
    date_str = today.strftime('%Y%m%d')
    text_path = os.path.join(DAILY_REPORTS_DIR, f"report_{date_str}.txt")
    html_path = os.path.join(DAILY_REPORTS_DIR, f"report_{date_str}.html")
    json_path = os.path.join(DAILY_REPORTS_DIR, f"report_{date_str}.json")

    with open(text_path, 'w') as f:
        f.write(text_report)

    with open(html_path, 'w') as f:
        f.write(html_report)

    with open(json_path, 'w') as f:
        json.dump({
            'date': today.isoformat(),
            'creator_files': creator_files,
            'summary': {
                'total_creators': len(creator_files),
                'total_new': sum(d['total_new'] for d in creator_files.values()),
                'total_modified': sum(d['total_modified'] for d in creator_files.values())
            }
        }, f, indent=2)

    print(f"\n✅ REPORTS GENERATED:")
    print(f"   Text: {text_path}")
    print(f"   HTML: {html_path}")
    print(f"   JSON: {json_path}")

    # Print summary to console
    print("\n" + text_report)

    return text_path, html_path, json_path


def generate_date_report(date_string):
    """Generate report for specific date (YYYY-MM-DD)"""
    target_date = datetime.fromisoformat(date_string).date()

    print(f"📊 GENERATING REPORT FOR {target_date}...")

    activity_log = load_activity_log()
    if not activity_log:
        print("❌ No activity log found.")
        return None

    date_entries = get_date_activity(activity_log, target_date)

    if not date_entries:
        print(f"📭 No activity recorded for {target_date}")
        return None

    creator_files = categorize_files_by_creator(date_entries)

    # Generate and save reports
    text_report = generate_daily_report_text(target_date, creator_files)
    html_report = generate_daily_report_html(target_date, creator_files)

    date_str = target_date.strftime('%Y%m%d')
    text_path = os.path.join(DAILY_REPORTS_DIR, f"report_{date_str}.txt")
    html_path = os.path.join(DAILY_REPORTS_DIR, f"report_{date_str}.html")

    with open(text_path, 'w') as f:
        f.write(text_report)

    with open(html_path, 'w') as f:
        f.write(html_report)

    print(f"\n✅ REPORTS GENERATED:")
    print(f"   Text: {text_path}")
    print(f"   HTML: {html_path}")

    print("\n" + text_report)

    return text_path, html_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Generate for specific date
        date_arg = sys.argv[1]
        generate_date_report(date_arg)
    else:
        # Generate for today
        generate_todays_report()
