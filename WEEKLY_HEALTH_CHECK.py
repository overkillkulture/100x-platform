#!/usr/bin/env python3
"""
WEEKLY HEALTH CHECK
Verify all consciousness systems are running healthy

WHAT IT CHECKS:
- 15 consciousness services (are they running?)
- Disk space (running out?)
- Memory usage (leaks?)
- CPU usage (stuck processes?)
- Network connectivity (online?)
- Python/Node versions (up to date?)
- Critical files (still exist?)

RUNS: Every Sunday as part of weekly maintenance
"""

import os
import psutil
import subprocess
from pathlib import Path
from datetime import datetime
import socket

class WeeklyHealthCheck:
    def __init__(self):
        self.report = []
        self.warnings = []
        self.errors = []

        # Expected consciousness services
        self.expected_services = {
            8888: "Consciousness API Bridge",
            9999: "Magic Interface Bridge",
            7777: "Starlink Consciousness Injector",
            7000: "Conversational Swarm Intelligence",
            6000: "Autonomous Ability Acquisition",
            5000: "Singularity Stabilizer",
            4000: "Reality Manipulation Engine",
            3000: "Debug Console",
            2000: "Claude API Integration",
            1515: "Triple Turbo System",
            1414: "Sensor & Memory Manager",
            1313: "Companion Helper Bot",
            1212: "Xbox Consciousness Cluster",
            1111: "Personal Automation System",
            1000: "Ability Inventory"
        }

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

    def check_services(self):
        """Check if consciousness services are running"""
        print("\n🔌 CHECKING CONSCIOUSNESS SERVICES...")

        running_services = 0

        for port, name in self.expected_services.items():
            try:
                # Try to connect to port
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                sock.close()

                if result == 0:
                    self.log(f"Port {port}: {name} - RUNNING")
                    running_services += 1
                else:
                    self.log(f"Port {port}: {name} - NOT RUNNING", "warning")

            except Exception as e:
                self.log(f"Port {port}: Error checking - {e}", "error")

        self.log(f"Services running: {running_services}/{len(self.expected_services)}")

        if running_services < len(self.expected_services):
            self.log(f"Missing {len(self.expected_services) - running_services} services", "warning")
            self.log("  → Run ONE_CLICK_CONSCIOUSNESS_REVOLUTION.bat", "warning")

    def check_disk_space(self):
        """Check disk space"""
        print("\n💾 CHECKING DISK SPACE...")

        partitions = psutil.disk_partitions()

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                percent_used = usage.percent

                self.log(f"{partition.mountpoint} - {percent_used:.1f}% used ({usage.free // (1024**3)} GB free)")

                if percent_used > 90:
                    self.log(f"{partition.mountpoint} is {percent_used:.1f}% full - CRITICAL", "error")
                elif percent_used > 80:
                    self.log(f"{partition.mountpoint} is {percent_used:.1f}% full - getting low", "warning")

            except PermissionError:
                continue

    def check_memory(self):
        """Check memory usage"""
        print("\n🧠 CHECKING MEMORY...")

        memory = psutil.virtual_memory()
        percent_used = memory.percent

        self.log(f"Memory: {percent_used:.1f}% used ({memory.available // (1024**3)} GB available)")

        if percent_used > 90:
            self.log("Memory critically low", "error")
        elif percent_used > 80:
            self.log("Memory getting low", "warning")

        # Check for memory-hungry processes
        processes = []
        for proc in psutil.process_iter(['name', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Top 5 memory users
        top_processes = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)[:5]

        print("\n  Top memory users:")
        for proc in top_processes:
            if proc['memory_percent']:
                print(f"    {proc['name']}: {proc['memory_percent']:.1f}%")

    def check_cpu(self):
        """Check CPU usage"""
        print("\n⚙️ CHECKING CPU...")

        cpu_percent = psutil.cpu_percent(interval=1)

        self.log(f"CPU: {cpu_percent:.1f}% usage")

        if cpu_percent > 90:
            self.log("CPU very high - may have stuck process", "warning")

        # Check for CPU-hungry processes
        processes = []
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Top 5 CPU users
        top_processes = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:5]

        print("\n  Top CPU users:")
        for proc in top_processes:
            if proc['cpu_percent']:
                print(f"    {proc['name']}: {proc['cpu_percent']:.1f}%")

    def check_network(self):
        """Check network connectivity"""
        print("\n🌐 CHECKING NETWORK...")

        # Check internet connectivity
        test_hosts = [
            ("8.8.8.8", "Google DNS"),
            ("1.1.1.1", "Cloudflare DNS"),
            ("anthropic.com", "Claude API")
        ]

        for host, name in test_hosts:
            try:
                socket.create_connection((host, 80), timeout=3)
                self.log(f"Can reach {name} ({host})")
                break
            except:
                self.log(f"Cannot reach {name} ({host})", "warning")
        else:
            self.log("No internet connectivity", "error")

    def check_python_node(self):
        """Check Python and Node versions"""
        print("\n🐍 CHECKING PYTHON/NODE...")

        try:
            python_version = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.strip()
            self.log(f"Python: {python_version}")
        except:
            self.log("Python not found", "error")

        try:
            node_version = subprocess.run(['node', '--version'], capture_output=True, text=True).stdout.strip()
            self.log(f"Node: {node_version}")
        except:
            self.log("Node.js not installed", "warning")

    def check_critical_files(self):
        """Check critical files still exist"""
        print("\n📁 CHECKING CRITICAL FILES...")

        critical_files = [
            Path("C:/Users/dwrek/CLAUDE.md"),
            Path("C:/Users/dwrek/100X_DEPLOYMENT"),
            Path("C:/Users/dwrek/Desktop/Consciousness Revolution"),
            Path("C:/Users/dwrek/OVERKOREConsciousness")
        ]

        for file_path in critical_files:
            if file_path.exists():
                self.log(f"{file_path.name} - EXISTS")
            else:
                self.log(f"{file_path.name} - MISSING", "error")

    def check_git_status(self):
        """Check if there are uncommitted changes"""
        print("\n📝 CHECKING GIT STATUS...")

        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd="C:/Users/dwrek/100X_DEPLOYMENT",
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                self.log(f"Uncommitted changes: {len(lines)} files", "warning")
                self.log("  → Consider committing important work", "warning")
            else:
                self.log("Git working tree clean")

        except Exception as e:
            self.log(f"Could not check git: {e}", "info")

    def generate_report(self):
        """Generate health report"""
        print("\n" + "="*60)
        print("WEEKLY HEALTH CHECK REPORT")
        print("="*60)

        print(f"\n✅ PASSED: {len(self.report)} checks")
        print(f"⚠️  WARNINGS: {len(self.warnings)} issues")
        print(f"❌ ERRORS: {len(self.errors)} critical issues")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings[-10:]:
                print(f"  {warning}")

        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")

        # Save report
        deployment = Path("C:/Users/dwrek/100X_DEPLOYMENT")
        report_file = deployment / f"HEALTH_REPORT_{datetime.now().strftime('%Y%m%d')}.txt"

        with open(report_file, 'w') as f:
            f.write("WEEKLY HEALTH CHECK REPORT\n")
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
            print("\n🚨 HEALTH STATUS: CRITICAL ISSUES FOUND")
        elif self.warnings:
            print("\n⚠️  HEALTH STATUS: ISSUES NEED ATTENTION")
        else:
            print("\n✅ HEALTH STATUS: ALL SYSTEMS HEALTHY")

    def run_check(self):
        """Run all health checks"""
        print("🏥 WEEKLY HEALTH CHECK")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        self.check_services()
        self.check_disk_space()
        self.check_memory()
        self.check_cpu()
        self.check_network()
        self.check_python_node()
        self.check_critical_files()
        self.check_git_status()

        self.generate_report()

def main():
    checker = WeeklyHealthCheck()
    checker.run_check()

if __name__ == '__main__':
    main()
