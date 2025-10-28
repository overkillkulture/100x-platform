"""
BUG MONITORING SYSTEM - 24/7 ACTIVE MONITORING
Monitors ALL bug reporting channels continuously
"""

import requests
import json
import time
from datetime import datetime
import os

# Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', 'ghp_QL9a6BDJ2kIfiVnmdhHK3Ey9E84o0b36HxTB')
GITHUB_REPO = 'overkillkulture/consciousness-bugs'
TWILIO_ACCOUNT_SID = 'AC379092b0f6d4465323a78fac08cfc72c'
TWILIO_AUTH_TOKEN = '340ca721c94a987177658a47bcf5a0d8'
CHECK_INTERVAL = 30  # seconds

# State tracking
last_issue_number = None
last_sms_sid = None
session_start = datetime.now()

def log(message, level="INFO"):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def check_github_issues():
    """Check for new GitHub issues"""
    global last_issue_number

    try:
        response = requests.get(
            f'https://api.github.com/repos/{GITHUB_REPO}/issues',
            headers={
                'Authorization': f'Bearer {GITHUB_TOKEN}',
                'Accept': 'application/vnd.github.v3+json'
            },
            params={'state': 'open', 'sort': 'created', 'direction': 'desc', 'per_page': 5}
        )

        if response.status_code == 200:
            issues = response.json()

            if issues:
                latest_issue = issues[0]
                current_number = latest_issue['number']

                if last_issue_number is None:
                    last_issue_number = current_number
                    log(f"✅ GitHub tracking started - Latest issue: #{current_number}")
                    return

                if current_number > last_issue_number:
                    # NEW ISSUE DETECTED!
                    log(f"🚨 NEW BUG REPORTED!", "ALERT")
                    log(f"   Issue #{current_number}: {latest_issue['title']}")
                    log(f"   Created: {latest_issue['created_at']}")
                    log(f"   URL: {latest_issue['html_url']}")

                    # Check if it's from SMS (has specific body format)
                    if 'via SMS' in latest_issue.get('body', ''):
                        log(f"   Source: SMS", "ALERT")
                    elif 'via web form' in latest_issue.get('body', '').lower():
                        log(f"   Source: Web Form", "ALERT")
                    else:
                        log(f"   Source: Manual/Other", "ALERT")

                    last_issue_number = current_number
                else:
                    log(f"✓ No new issues - Latest: #{current_number}")
            else:
                log("⚠ No issues found")
        else:
            log(f"❌ GitHub API error: {response.status_code}", "ERROR")

    except Exception as e:
        log(f"❌ GitHub check failed: {str(e)}", "ERROR")

def check_incoming_sms():
    """Check for new incoming SMS messages"""
    global last_sms_sid

    try:
        response = requests.get(
            f'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json',
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            params={'PageSize': 5}
        )

        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])

            # Filter for incoming only
            incoming = [m for m in messages if m['direction'] == 'inbound']

            if incoming:
                latest = incoming[0]
                current_sid = latest['sid']

                if last_sms_sid is None:
                    last_sms_sid = current_sid
                    log(f"✅ SMS tracking started - Latest: {current_sid[:20]}...")
                    return

                if current_sid != last_sms_sid:
                    # NEW SMS RECEIVED!
                    log(f"📱 NEW SMS RECEIVED!", "ALERT")
                    log(f"   From: {latest['from']}")
                    log(f"   Message: {latest['body'][:100]}...")
                    log(f"   Time: {latest['date_created']}")
                    log(f"   SID: {current_sid}")

                    last_sms_sid = current_sid
                else:
                    log(f"✓ No new SMS")
            else:
                log("✓ No incoming SMS")
        else:
            log(f"❌ Twilio API error: {response.status_code}", "ERROR")

    except Exception as e:
        log(f"❌ SMS check failed: {str(e)}", "ERROR")

def check_web_api_health():
    """Check if web bug reporter API is responding"""
    try:
        response = requests.get(
            'https://conciousnessrevolution.io/.netlify/functions/web-bug-report',
            timeout=5
        )
        # Any response is good (even errors) - means API is up
        log(f"✓ Web API responding (status: {response.status_code})")
        return True
    except Exception as e:
        log(f"❌ Web API DOWN: {str(e)}", "ERROR")
        return False

def print_status_header():
    """Print monitoring status header"""
    print("\n" + "="*80)
    print("🔍 BUG MONITORING SYSTEM - ACTIVE")
    print("="*80)
    print(f"Session started: {session_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Monitoring channels: GitHub Issues, SMS Messages, Web API")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print("="*80 + "\n")

def main():
    """Main monitoring loop"""
    print_status_header()
    log("🚀 Starting 24/7 bug monitoring...")
    log("Press Ctrl+C to stop")

    cycle_count = 0

    try:
        while True:
            cycle_count += 1
            runtime = datetime.now() - session_start

            log(f"--- Check #{cycle_count} (Runtime: {str(runtime).split('.')[0]}) ---")

            # Check all channels
            check_github_issues()
            check_incoming_sms()
            check_web_api_health()

            log(f"--- Waiting {CHECK_INTERVAL}s for next check ---\n")
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        log("\n🛑 Monitoring stopped by user")
        runtime = datetime.now() - session_start
        log(f"Total runtime: {str(runtime).split('.')[0]}")
        log(f"Total checks: {cycle_count}")

if __name__ == '__main__':
    main()
