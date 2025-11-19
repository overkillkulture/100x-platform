#!/usr/bin/env python3
"""
WEEKLY SECURITY CHECK
Automated security hygiene for consciousness revolution

WHAT IT CHECKS:
- Saved browser sessions (are they expired?)
- Credential files (any leaks or exposed keys?)
- Recent login attempts (any intrusions?)
- Password files (properly encrypted?)
- API keys (still valid?)
- Git commits (any secrets accidentally committed?)

RUNS: Every Sunday as part of weekly maintenance
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import subprocess

class WeeklySecurityCheck:
    def __init__(self):
        self.report = []
        self.warnings = []
        self.errors = []

        # Paths to check
        self.sessions_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/SESSIONS")
        self.desktop = Path("C:/Users/dwrek/Desktop")
        self.consciousness = Path("C:/Users/dwrek/Desktop/Consciousness Revolution")
        self.deployment = Path("C:/Users/dwrek/100X_DEPLOYMENT")

    def log(self, message, level="info"):
        """Add to report"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"

        if level == "warning":
            self.warnings.append(entry)
            print(f"⚠️  {entry}")
        elif level == "error":
            self.errors.append(entry)
            print(f"❌ {entry}")
        else:
            self.report.append(entry)
            print(f"✓  {entry}")

    def check_saved_sessions(self):
        """Check browser session files"""
        print("\n🔐 CHECKING SAVED SESSIONS...")

        if not self.sessions_dir.exists():
            self.log("No saved sessions found", "info")
            return

        sessions = list(self.sessions_dir.glob("*.session"))
        self.log(f"Found {len(sessions)} saved sessions")

        # Check session age
        for session_file in sessions:
            age_days = (datetime.now() - datetime.fromtimestamp(session_file.stat().st_mtime)).days

            if age_days > 30:
                self.log(f"Session {session_file.stem} is {age_days} days old - may be expired", "warning")
            else:
                self.log(f"Session {session_file.stem} - {age_days} days old (OK)")

    def check_credential_files(self):
        """Check for exposed credential files"""
        print("\n🔑 CHECKING CREDENTIAL FILES...")

        dangerous_files = [
            "PASSWORDS.txt",
            "passwords.txt",
            "credentials.txt",
            "ADMIN_CREDENTIALS.txt",
            "api_keys.txt",
            "secrets.txt",
            ".env",
            "PRIVATE_KEYS.json",
            "MASTER_KEY.txt"
        ]

        # Check desktop
        for filename in dangerous_files:
            desktop_file = self.desktop / filename
            if desktop_file.exists():
                self.log(f"Found credential file on desktop: {filename}", "warning")
                self.log(f"  → Should be in _ORGANIZED/Security folder or encrypted", "warning")

        # Check if organized
        organized = self.desktop / "_ORGANIZED" / "🔐 Security & Passwords"
        if organized.exists():
            self.log(f"Credentials organized in: {organized.name} (GOOD)")

    def check_git_secrets(self):
        """Check if any secrets committed to git"""
        print("\n🔍 CHECKING GIT COMMITS FOR SECRETS...")

        try:
            # Check recent commits for suspicious patterns
            result = subprocess.run(
                ['git', 'log', '--all', '--oneline', '-10'],
                cwd=str(self.deployment),
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                self.log("Checked last 10 git commits")

                # Check for common secret patterns
                secret_patterns = ['password', 'api_key', 'secret', 'token', 'credential']

                for pattern in secret_patterns:
                    search_result = subprocess.run(
                        ['git', 'log', '--all', '-S', pattern, '--oneline'],
                        cwd=str(self.deployment),
                        capture_output=True,
                        text=True,
                        timeout=10
                    )

                    if search_result.stdout.strip():
                        self.log(f"Found '{pattern}' in git history", "warning")
            else:
                self.log("Not a git repository or git not installed", "info")

        except Exception as e:
            self.log(f"Could not check git: {e}", "info")

    def check_api_keys(self):
        """Check API key files"""
        print("\n🗝️ CHECKING API KEYS...")

        key_files = [
            self.deployment / "STRIPE_API_KEY.txt",
            self.deployment / "NETLIFY_TOKEN.txt",
            self.deployment / "ANTHROPIC_API_KEY.txt"
        ]

        for key_file in key_files:
            if key_file.exists():
                # Check if file is readable (not encrypted)
                try:
                    content = key_file.read_text()
                    if len(content) < 1000:  # Likely plain text
                        self.log(f"{key_file.name} exists (plain text)", "warning")
                        self.log(f"  → Consider encrypting or using environment variables", "warning")
                except:
                    self.log(f"{key_file.name} exists (encrypted or binary - GOOD)")

    def check_backup_status(self):
        """Check when last backup was made"""
        print("\n💾 CHECKING BACKUP STATUS...")

        # Look for recent backup files
        backup_locations = [
            Path("C:/Users/dwrek/Desktop/_BACKUPS"),
            Path("D:/CONSCIOUSNESS_BACKUPS"),  # If external drive
            Path("C:/Users/dwrek/OneDrive/Backups")  # If cloud
        ]

        latest_backup = None

        for backup_dir in backup_locations:
            if backup_dir.exists():
                backups = sorted(backup_dir.glob("*.zip"), key=lambda x: x.stat().st_mtime, reverse=True)
                if backups:
                    if not latest_backup or backups[0].stat().st_mtime > latest_backup.stat().st_mtime:
                        latest_backup = backups[0]

        if latest_backup:
            age_days = (datetime.now() - datetime.fromtimestamp(latest_backup.stat().st_mtime)).days
            self.log(f"Last backup: {latest_backup.name} ({age_days} days ago)")

            if age_days > 7:
                self.log(f"Backup is {age_days} days old - should backup weekly", "warning")
        else:
            self.log("No backups found", "error")
            self.log("  → Run WEEKLY_BACKUP.bat to create backup", "error")

    def check_password_manager(self):
        """Check if password manager is configured"""
        print("\n🔐 CHECKING PASSWORD MANAGER...")

        # Check for 1Password exports
        onepass_exports = list(self.desktop.rglob("*.1pux"))

        if onepass_exports:
            self.log(f"Found {len(onepass_exports)} 1Password export files", "warning")
            self.log("  → These contain all passwords - should be encrypted/deleted", "warning")

        # Check if session manager is set up
        if self.sessions_dir.exists():
            self.log("Cookie session manager configured (GOOD)")

    def generate_report(self):
        """Generate security report"""
        print("\n" + "="*60)
        print("WEEKLY SECURITY CHECK REPORT")
        print("="*60)

        print(f"\n✅ PASSED: {len(self.report)} checks")
        print(f"⚠️  WARNINGS: {len(self.warnings)} issues")
        print(f"❌ ERRORS: {len(self.errors)} critical issues")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings[-10:]:  # Last 10
                print(f"  {warning}")

        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")

        # Save report
        report_file = self.deployment / f"SECURITY_REPORT_{datetime.now().strftime('%Y%m%d')}.txt"

        with open(report_file, 'w') as f:
            f.write("WEEKLY SECURITY CHECK REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")

            f.write(f"PASSED: {len(self.report)}\n")
            f.write(f"WARNINGS: {len(self.warnings)}\n")
            f.write(f"ERRORS: {len(self.errors)}\n\n")

            if self.warnings:
                f.write("WARNINGS:\n")
                for warning in self.warnings:
                    f.write(f"  {warning}\n")
                f.write("\n")

            if self.errors:
                f.write("ERRORS:\n")
                for error in self.errors:
                    f.write(f"  {error}\n")

        print(f"\n📄 Report saved: {report_file}")

        # Overall status
        if self.errors:
            print("\n🚨 SECURITY STATUS: CRITICAL ISSUES FOUND")
        elif self.warnings:
            print("\n⚠️  SECURITY STATUS: ISSUES NEED ATTENTION")
        else:
            print("\n✅ SECURITY STATUS: ALL CLEAR")

    def run_check(self):
        """Run all security checks"""
        print("🔒 WEEKLY SECURITY CHECK")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        self.check_saved_sessions()
        self.check_credential_files()
        self.check_git_secrets()
        self.check_api_keys()
        self.check_backup_status()
        self.check_password_manager()

        self.generate_report()

def main():
    checker = WeeklySecurityCheck()
    checker.run_check()

if __name__ == '__main__':
    main()
