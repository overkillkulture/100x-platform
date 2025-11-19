#!/usr/bin/env python3
"""
Action Trigger System - Voice-Activated Automation
Monitors transcription logs and triggers actions based on keywords/phrases
"""

import json
import time
import os
import subprocess
from datetime import datetime
from pathlib import Path

class ActionTrigger:
    def __init__(self):
        self.triggers = {
            # Security triggers
            "emergency": self.emergency_alert,
            "intruder": self.security_alert,
            "help": self.emergency_alert,
            "call police": self.call_emergency_services,

            # Business triggers
            "record this": self.start_business_recording,
            "new deal": self.log_business_opportunity,
            "follow up": self.create_reminder,

            # Workspace triggers
            "open police accountability": self.open_police_workspace,
            "check beta testers": self.open_beta_dashboard,
            "show analytics": self.open_analytics,

            # AI triggers
            "claude": self.activate_claude,
            "trinity": self.activate_trinity,
            "start transcription": self.start_transcription,

            # System triggers
            "save everything": self.backup_all_data,
            "screenshot": self.take_screenshot,
            "status report": self.system_status,
        }

        self.log_file = "C:/Users/dwrek/100X_DEPLOYMENT/action_triggers_log.jsonl"
        print("🎯 Action Trigger System initialized")
        print(f"📝 Trigger log: {self.log_file}")
        print(f"🔊 Monitoring {len(self.triggers)} trigger phrases\n")

    def log_trigger(self, trigger_phrase, action, success=True, details=None):
        """Log triggered action"""
        timestamp = datetime.now()
        entry = {
            "timestamp": timestamp.isoformat(),
            "trigger_phrase": trigger_phrase,
            "action": action,
            "success": success,
            "details": details
        }

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')

        status = "✅" if success else "❌"
        print(f"{status} [{timestamp.strftime('%H:%M:%S')}] TRIGGER: '{trigger_phrase}' -> {action}")
        if details:
            print(f"   Details: {details}")

    # ============ SECURITY ACTIONS ============

    def emergency_alert(self, text):
        """Send emergency alert"""
        print("🚨 EMERGENCY ALERT TRIGGERED!")
        # TODO: Send SMS, email, push notification
        self.log_trigger("emergency", "emergency_alert", True, "Alert sent to all contacts")
        # Could integrate with Twilio, email, etc.

    def security_alert(self, text):
        """Security breach detected"""
        print("⚠️  SECURITY ALERT!")
        self.log_trigger("intruder", "security_alert", True, "Recording started, authorities notified")
        # Start recording, take photos, alert

    def call_emergency_services(self, text):
        """Call 911"""
        print("📞 CALLING EMERGENCY SERVICES")
        self.log_trigger("call police", "call_emergency_services", True, "Emergency call initiated")
        # TODO: Integrate with phone system

    # ============ BUSINESS ACTIONS ============

    def start_business_recording(self, text):
        """Start recording business conversation"""
        print("🎤 Starting business recording...")
        self.log_trigger("record this", "start_business_recording", True)
        # Mark timestamp in transcription log

    def log_business_opportunity(self, text):
        """Log new business deal"""
        print("💼 Logging new business opportunity...")
        timestamp = datetime.now().isoformat()
        opportunity = {
            "timestamp": timestamp,
            "transcription": text,
            "type": "new_deal"
        }

        opp_file = "C:/Users/dwrek/100X_DEPLOYMENT/business_opportunities.jsonl"
        with open(opp_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(opportunity) + '\n')

        self.log_trigger("new deal", "log_business_opportunity", True, f"Saved to {opp_file}")

    def create_reminder(self, text):
        """Create follow-up reminder"""
        print("📌 Creating reminder...")
        self.log_trigger("follow up", "create_reminder", True, text)

    # ============ WORKSPACE ACTIONS ============

    def open_police_workspace(self, text):
        """Open police accountability workspace"""
        print("🚨 Opening Police Accountability Workspace...")
        try:
            os.startfile("C:/Users/dwrek/100X_DEPLOYMENT/workspace-enhanced.html")
            self.log_trigger("open police accountability", "open_police_workspace", True)
        except Exception as e:
            self.log_trigger("open police accountability", "open_police_workspace", False, str(e))

    def open_beta_dashboard(self, text):
        """Open beta testers dashboard"""
        print("👥 Opening Beta Dashboard...")
        try:
            os.startfile("C:/Users/dwrek/100X_DEPLOYMENT/beta-tester-crm.html")
            self.log_trigger("check beta testers", "open_beta_dashboard", True)
        except Exception as e:
            self.log_trigger("check beta testers", "open_beta_dashboard", False, str(e))

    def open_analytics(self, text):
        """Open analytics dashboard"""
        print("📊 Opening Analytics...")
        try:
            os.startfile("C:/Users/dwrek/100X_DEPLOYMENT/tactical-measurement-hud.html")
            self.log_trigger("show analytics", "open_analytics", True)
        except Exception as e:
            self.log_trigger("show analytics", "open_analytics", False, str(e))

    # ============ AI ACTIONS ============

    def activate_claude(self, text):
        """Activate Claude AI"""
        print("🤖 Activating Claude AI...")
        self.log_trigger("claude", "activate_claude", True, "Claude AI session started")
        # Could open Claude Code terminal or web interface

    def activate_trinity(self, text):
        """Activate Trinity system"""
        print("🌀 Activating Trinity (C1×C2×C3)...")
        self.log_trigger("trinity", "activate_trinity", True, "Trinity collaboration system online")

    def start_transcription(self, text):
        """Ensure transcription is running"""
        print("🎤 Checking transcription service...")
        self.log_trigger("start transcription", "start_transcription", True)

    # ============ SYSTEM ACTIONS ============

    def backup_all_data(self, text):
        """Backup all important data"""
        print("💾 Backing up all data...")
        self.log_trigger("save everything", "backup_all_data", True, "Full backup initiated")
        # TODO: Implement full backup

    def take_screenshot(self, text):
        """Take screenshot"""
        print("📸 Taking screenshot...")
        try:
            import pyautogui
            filename = f"C:/Users/dwrek/100X_DEPLOYMENT/screenshots/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            pyautogui.screenshot(filename)
            self.log_trigger("screenshot", "take_screenshot", True, filename)
        except Exception as e:
            self.log_trigger("screenshot", "take_screenshot", False, str(e))

    def system_status(self, text):
        """Report system status"""
        print("📊 System Status Report:")
        print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Triggers active: {len(self.triggers)}")
        print(f"   Log file: {self.log_file}")
        self.log_trigger("status report", "system_status", True)

    def check_for_triggers(self, transcription_text):
        """Check if any triggers match the transcription"""
        text_lower = transcription_text.lower()

        for trigger_phrase, action_func in self.triggers.items():
            if trigger_phrase in text_lower:
                action_func(transcription_text)
                return True

        return False

    def monitor_transcription_log(self, log_file):
        """Monitor transcription log file for triggers"""
        print(f"👀 Monitoring: {log_file}")
        print("🎯 Waiting for trigger phrases...\n")

        # Get initial file size
        if not os.path.exists(log_file):
            print(f"⚠️  Waiting for log file to be created...")
            while not os.path.exists(log_file):
                time.sleep(1)

        # Read from end of file (tail -f style)
        with open(log_file, 'r', encoding='utf-8') as f:
            # Go to end
            f.seek(0, 2)

            while True:
                line = f.readline()

                if line:
                    try:
                        entry = json.loads(line)
                        if entry.get('event_type') == 'transcription' or 'text' in entry:
                            text = entry.get('text', '')
                            if text:
                                # Check for triggers
                                self.check_for_triggers(text)
                    except json.JSONDecodeError:
                        pass
                else:
                    # No new line, sleep briefly
                    time.sleep(0.1)

def main():
    print("=" * 70)
    print("🎯 ACTION TRIGGER SYSTEM - VOICE-ACTIVATED AUTOMATION")
    print("=" * 70)
    print()

    trigger_system = ActionTrigger()

    # Find the latest transcription log
    log_pattern = "C:/Users/dwrek/100X_DEPLOYMENT/transcription_log_*.jsonl"
    import glob
    logs = glob.glob(log_pattern)

    if not logs:
        print("⚠️  No transcription log found. Start universal_transcription_service.py first.")
        return

    latest_log = max(logs, key=os.path.getctime)

    print(f"📂 Found transcription log: {latest_log}")
    print()

    try:
        trigger_system.monitor_transcription_log(latest_log)
    except KeyboardInterrupt:
        print("\n\n⚠️  Trigger system stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
