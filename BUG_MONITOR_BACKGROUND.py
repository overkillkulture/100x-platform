"""
BUG MONITORING SYSTEM - BACKGROUND VERSION
Runs silently and logs to file
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
LOG_FILE = 'C:/Users/dwrek/Desktop/BUG_MONITOR_LOG.txt'

# State tracking
last_issue_number = None
last_sms_sid = None
session_start = datetime.now()

def log(message, level="INFO", alert=False):
    """Log with timestamp to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}\n"

    # Write to file
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line)

    # Print to console
    print(log_line.strip())

    # If alert, also write to alerts file
    if alert:
        with open('C:/Users/dwrek/Desktop/BUG_ALERTS.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(log_line)
            f.write(f"{'='*60}\n")

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
                    log(f"GitHub tracking started - Latest issue: #{current_number}")
                    return

                if current_number > last_issue_number:
                    # NEW ISSUE DETECTED!
                    log(f"🚨 NEW BUG REPORTED! Issue #{current_number}: {latest_issue['title']}", "ALERT", alert=True)
                    log(f"   Created: {latest_issue['created_at']}", "ALERT", alert=True)
                    log(f"   URL: {latest_issue['html_url']}", "ALERT", alert=True)

                    # Check source
                    body = latest_issue.get('body', '').lower()
                    if 'via sms' in body:
                        log(f"   Source: SMS", "ALERT", alert=True)
                    elif 'via web form' in body:
                        log(f"   Source: Web Form", "ALERT", alert=True)
                    else:
                        log(f"   Source: Manual/Other", "ALERT", alert=True)

                    last_issue_number = current_number
                else:
                    log(f"No new GitHub issues (latest: #{current_number})")
            else:
                log("No GitHub issues found")
        else:
            log(f"GitHub API error: {response.status_code}", "ERROR")

    except Exception as e:
        log(f"GitHub check failed: {str(e)}", "ERROR")

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
            incoming = [m for m in messages if m['direction'] == 'inbound']

            if incoming:
                latest = incoming[0]
                current_sid = latest['sid']

                if last_sms_sid is None:
                    last_sms_sid = current_sid
                    log(f"SMS tracking started")
                    return

                if current_sid != last_sms_sid:
                    # NEW SMS RECEIVED!
                    log(f"📱 NEW SMS RECEIVED!", "ALERT", alert=True)
                    log(f"   From: {latest['from']}", "ALERT", alert=True)
                    log(f"   Message: {latest['body'][:200]}", "ALERT", alert=True)
                    log(f"   Time: {latest['date_created']}", "ALERT", alert=True)

                    last_sms_sid = current_sid
                else:
                    log(f"No new SMS messages")
            else:
                log("No incoming SMS")
        else:
            log(f"Twilio API error: {response.status_code}", "ERROR")

    except Exception as e:
        log(f"SMS check failed: {str(e)}", "ERROR")

def main():
    """Main monitoring loop"""
    log("="*60)
    log("BUG MONITORING SYSTEM STARTED")
    log(f"Session: {session_start.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Check interval: {CHECK_INTERVAL} seconds")
    log(f"Log file: {LOG_FILE}")
    log("="*60)

    cycle_count = 0

    try:
        while True:
            cycle_count += 1

            log(f"\n--- Check #{cycle_count} ---")
            check_github_issues()
            check_incoming_sms()

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        runtime = datetime.now() - session_start
        log(f"\nMonitoring stopped - Runtime: {str(runtime).split('.')[0]}, Checks: {cycle_count}")

if __name__ == '__main__':
    main()
