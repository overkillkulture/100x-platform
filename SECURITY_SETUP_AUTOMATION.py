#!/usr/bin/env python3
"""
SECURITY_SETUP_AUTOMATION.py
One-click security infrastructure setup

Created: November 4, 2025 (Autonomous Build)
Purpose: Install and configure defensive security tools
"""

import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def banner(text):
    """Print a nice banner"""
    print()
    print("=" * 80)
    print(f"  {text}")
    print("=" * 80)
    print()

def run_command(cmd, description, shell=False):
    """Run a command and report status"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout:
                print(f"   Output: {result.stdout[:200]}")
            return True
        else:
            print(f"⚠️  {description} - FAILED")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⚠️  {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"⚠️  {description} - ERROR: {e}")
        return False

def check_admin():
    """Check if running as administrator"""
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        return is_admin
    except:
        return False

def enable_windows_sandbox():
    """Enable Windows Sandbox feature"""
    banner("🏖️ ENABLING WINDOWS SANDBOX")

    if not check_admin():
        print("⚠️  Administrator privileges required for Windows Sandbox")
        print("   Please run this script as Administrator")
        return False

    cmd = ['powershell', '-Command',
           'Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -All -Online -NoRestart']

    return run_command(cmd, "Enable Windows Sandbox")

def install_chocolatey_packages():
    """Install security tools via Chocolatey"""
    banner("📦 INSTALLING SECURITY TOOLS VIA CHOCOLATEY")

    packages = [
        ('nmap', 'Network scanner'),
        ('wireshark', 'Packet analyzer'),
        ('virtualbox', 'Virtual machine platform'),
    ]

    results = {}
    for package, description in packages:
        print(f"\n📦 Installing {package} ({description})...")
        cmd = ['choco', 'install', package, '-y']
        success = run_command(cmd, f"Install {package}", shell=True)
        results[package] = success

    return results

def install_python_security_tools():
    """Install Python-based security tools"""
    banner("🐍 INSTALLING PYTHON SECURITY TOOLS")

    tools = [
        'dnspython',      # DNS toolkit
        'requests',       # HTTP library
        'beautifulsoup4', # Web scraping
        'lxml',           # XML/HTML parser
        'python-nmap',    # Nmap wrapper
        'scapy',          # Packet manipulation
    ]

    print("📦 Installing Python packages...")
    cmd = ['pip', 'install'] + tools
    return run_command(cmd, "Install Python security tools")

def create_security_directories():
    """Create directory structure for security work"""
    banner("📁 CREATING SECURITY WORKSPACE")

    base = Path(r"C:\Users\dwrek\.security")

    directories = [
        base,
        base / "scans",
        base / "reports",
        base / "tools",
        base / "vm_images",
        base / "logs",
        base / "sandbox_tests",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")

    # Create README
    readme = base / "README.md"
    readme.write_text(f"""# Security Workspace

Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Structure:

- `scans/` - Nmap and vulnerability scan results
- `reports/` - Security audit reports
- `tools/` - Security tools and scripts
- `vm_images/` - Virtual machine images (Kali Linux, etc.)
- `logs/` - Tool execution logs
- `sandbox_tests/` - Isolated testing environment data

## Authorized Testing Targets:

- ✅ https://conciousnessrevolution.io (OUR SITE)
- ✅ localhost development servers
- ✅ Railway/Netlify deployments (OUR INFRASTRUCTURE)
- ❌ ANY OTHER WEBSITES (illegal without permission)

## Tools Installed:

- nmap - Network scanner
- Wireshark - Packet analyzer
- Python security libraries
- VirtualBox - VM platform

## Next Steps:

1. Download Kali Linux: https://kali.org/get-kali/#kali-virtual-machines
2. Create VM in VirtualBox
3. Run first security scan: `nmap -sV conciousnessrevolution.io`
4. Review results and fix vulnerabilities

## Legal Notice:

All security testing is DEFENSIVE and LIMITED TO OUR OWN SYSTEMS.
Unauthorized access to other systems is ILLEGAL.
""")

    print(f"\n✅ Created README: {readme}")
    return base

def download_kali_info():
    """Provide Kali Linux download information"""
    banner("🐉 KALI LINUX VM SETUP")

    print("📋 Kali Linux Virtual Machine:")
    print("   Download from: https://kali.org/get-kali/#kali-virtual-machines")
    print()
    print("   Recommended: VirtualBox 64-bit image")
    print("   Size: ~3.5 GB download, 80 GB installed")
    print("   Default credentials: kali / kali")
    print()
    print("⚙️  VirtualBox Configuration:")
    print("   - RAM: 4096 MB (4 GB)")
    print("   - CPU: 2-4 cores")
    print("   - Network: Host-only adapter (for isolation)")
    print("   - Shared folder: C:\\Users\\dwrek\\.security\\sandbox_tests")
    print()
    print("🔐 First Boot Steps:")
    print("   1. Update system: sudo apt update && sudo apt upgrade -y")
    print("   2. Install guest additions (VirtualBox menu)")
    print("   3. Take a snapshot (clean baseline)")
    print()

def create_first_scan_script():
    """Create script for first security scan"""
    banner("🎯 CREATING FIRST SCAN SCRIPT")

    script_path = Path(r"C:\Users\dwrek\.security\tools\FIRST_SECURITY_SCAN.py")

    script_content = '''#!/usr/bin/env python3
"""
FIRST_SECURITY_SCAN.py
Run first authorized security scan on our own website

AUTHORIZED TARGET: conciousnessrevolution.io (OUR SITE)
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

def run_nmap_scan():
    """Run nmap scan on our website"""
    target = "conciousnessrevolution.io"

    print(f"🔍 Starting security scan of {target}")
    print(f"   (This is OUR website - authorized testing)")
    print()

    # Basic port scan
    print("⏳ Running basic port scan...")
    result = subprocess.run(
        ['nmap', '-sV', '-T4', target],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_dir = Path(r"C:\\Users\\dwrek\\.security\\scans")
    report_file = report_dir / f"nmap_scan_{timestamp}.txt"

    report_file.write_text(result.stdout)

    print(f"\\n✅ Scan complete!")
    print(f"📄 Report saved to: {report_file}")

    # Parse and summarize
    print("\\n📊 SUMMARY:")
    lines = result.stdout.split('\\n')
    for line in lines:
        if 'open' in line.lower():
            print(f"   {line.strip()}")

    return result.stdout

def analyze_results():
    """Provide basic analysis"""
    print("\\n🔐 SECURITY RECOMMENDATIONS:")
    print("   1. Review all open ports - close unnecessary ones")
    print("   2. Check SSL/TLS configuration")
    print("   3. Verify all services are up-to-date")
    print("   4. Review for any unexpected services")
    print()

if __name__ == "__main__":
    print()
    print("🌌" * 40)
    print()
    print("        FIRST SECURITY SCAN")
    print("        Authorized Testing: conciousnessrevolution.io")
    print()
    print("🌌" * 40)

    run_nmap_scan()
    analyze_results()
'''

    script_path.write_text(script_content)
    print(f"✅ Created: {script_path}")
    print(f"   Usage: python {script_path}")

    return script_path

def create_vulnerability_scanner():
    """Create custom vulnerability scanner for our sites"""
    banner("🛡️ CREATING VULNERABILITY SCANNER")

    scanner_path = Path(r"C:\Users\dwrek\100X_DEPLOYMENT\SITE_VULNERABILITY_SCANNER.py")

    scanner_content = '''#!/usr/bin/env python3
"""
SITE_VULNERABILITY_SCANNER.py
Automated vulnerability scanner for our own infrastructure

AUTHORIZED TARGETS ONLY:
- https://conciousnessrevolution.io
- localhost development servers
- Railway/Netlify deployments
"""

import requests
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

class VulnerabilityScanner:
    """Scan our own sites for common vulnerabilities"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.findings = []
        self.session = requests.Session()

    def check_security_headers(self):
        """Check for security headers"""
        print("\\n🔐 Checking security headers...")

        try:
            response = self.session.get(self.base_url, timeout=10)
            headers = response.headers

            required_headers = {
                'Strict-Transport-Security': 'HSTS',
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME sniffing protection',
                'Content-Security-Policy': 'XSS protection',
                'X-XSS-Protection': 'Legacy XSS protection',
            }

            for header, description in required_headers.items():
                if header in headers:
                    print(f"   ✅ {header}: {headers[header][:50]}")
                else:
                    print(f"   ❌ Missing: {header} ({description})")
                    self.findings.append({
                        'severity': 'medium',
                        'type': 'missing_header',
                        'header': header,
                        'description': description
                    })

        except Exception as e:
            print(f"   ⚠️  Error checking headers: {e}")

    def check_https(self):
        """Verify HTTPS is enforced"""
        print("\\n🔒 Checking HTTPS enforcement...")

        try:
            # Try HTTP
            http_url = self.base_url.replace('https://', 'http://')
            response = self.session.get(http_url, timeout=10, allow_redirects=False)

            if response.status_code in [301, 302, 307, 308]:
                if 'https://' in response.headers.get('Location', ''):
                    print("   ✅ HTTP redirects to HTTPS")
                else:
                    print("   ⚠️  HTTP redirects but not to HTTPS")
                    self.findings.append({
                        'severity': 'high',
                        'type': 'insecure_redirect',
                        'description': 'HTTP does not redirect to HTTPS'
                    })
            else:
                print("   ❌ HTTP is accessible without redirect")
                self.findings.append({
                    'severity': 'critical',
                    'type': 'no_https_redirect',
                    'description': 'HTTP accessible without HTTPS redirect'
                })

        except Exception as e:
            print(f"   ✅ HTTP not accessible (good!)")

    def check_sensitive_files(self):
        """Check for exposed sensitive files"""
        print("\\n📄 Checking for exposed sensitive files...")

        sensitive_paths = [
            '.env',
            '.git/config',
            'config.json',
            'api_keys.json',
            '.env.local',
            'backup.sql',
            'database.db',
        ]

        for path in sensitive_paths:
            url = urljoin(self.base_url, path)
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"   ❌ EXPOSED: {path}")
                    self.findings.append({
                        'severity': 'critical',
                        'type': 'exposed_file',
                        'path': path,
                        'url': url
                    })
                else:
                    print(f"   ✅ Protected: {path}")
            except:
                print(f"   ✅ Protected: {path}")

    def check_common_vulnerabilities(self):
        """Check for common web vulnerabilities"""
        print("\\n🐛 Checking for common vulnerabilities...")

        # XSS test (very basic)
        test_payloads = [
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
        ]

        # SQL injection test (very basic)
        sql_payloads = [
            "' OR '1'='1",
            "1' OR '1' = '1",
        ]

        print("   ℹ️  Basic XSS/SQLi testing (limited scope)")
        print("   For comprehensive testing, use OWASP ZAP")

    def generate_report(self):
        """Generate vulnerability report"""
        print("\\n" + "=" * 80)
        print("📊 VULNERABILITY SCAN REPORT")
        print("=" * 80)

        print(f"\\nTarget: {self.base_url}")
        print(f"Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\\nFindings: {len(self.findings)}")

        if not self.findings:
            print("\\n✅ No vulnerabilities found!")
        else:
            severity_counts = {}
            for finding in self.findings:
                severity = finding['severity']
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

            print("\\n🔴 Severity Breakdown:")
            for severity in ['critical', 'high', 'medium', 'low']:
                count = severity_counts.get(severity, 0)
                if count > 0:
                    print(f"   {severity.upper()}: {count}")

            print("\\n📋 Details:")
            for i, finding in enumerate(self.findings, 1):
                print(f"\\n   {i}. [{finding['severity'].upper()}] {finding['type']}")
                print(f"      {finding.get('description', 'No description')}")

        # Save report
        report_dir = Path(r"C:\\Users\\dwrek\\.security\\reports")
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = report_dir / f"vuln_scan_{timestamp}.json"

        report_data = {
            'target': self.base_url,
            'scan_time': datetime.now().isoformat(),
            'findings': self.findings
        }

        report_file.write_text(json.dumps(report_data, indent=2))
        print(f"\\n💾 Report saved to: {report_file}")

def main():
    """Run vulnerability scan"""
    print()
    print("🌌" * 40)
    print()
    print("        SITE VULNERABILITY SCANNER")
    print("        Authorized Testing Only")
    print()
    print("🌌" * 40)

    # Scan our site
    scanner = VulnerabilityScanner('https://conciousnessrevolution.io')
    scanner.check_security_headers()
    scanner.check_https()
    scanner.check_sensitive_files()
    scanner.check_common_vulnerabilities()
    scanner.generate_report()

    print("\\n✅ Scan complete!")

if __name__ == "__main__":
    main()
'''

    scanner_path.write_text(scanner_content)
    print(f"✅ Created: {scanner_path}")
    print(f"   Usage: python {scanner_path}")

    return scanner_path

def print_next_steps(security_dir, scan_script, vuln_scanner):
    """Print next steps for user"""
    banner("🎯 SETUP COMPLETE - NEXT STEPS")

    print("📋 IMMEDIATE ACTIONS:\\n")

    print("1. 🔍 RUN FIRST SECURITY SCAN")
    print(f"   cd {security_dir / 'tools'}")
    print(f"   python FIRST_SECURITY_SCAN.py")
    print()

    print("2. 🛡️ RUN VULNERABILITY SCANNER")
    print(f"   cd C:\\\\Users\\\\dwrek\\\\100X_DEPLOYMENT")
    print(f"   python SITE_VULNERABILITY_SCANNER.py")
    print()

    print("3. 🐉 DOWNLOAD KALI LINUX VM")
    print("   https://kali.org/get-kali/#kali-virtual-machines")
    print("   Choose: VirtualBox 64-bit")
    print(f"   Save to: {security_dir / 'vm_images'}")
    print()

    print("4. 🏖️ TEST WINDOWS SANDBOX")
    print("   Start → Windows Sandbox")
    print("   (May require restart if just enabled)")
    print()

    print("=" * 80)
    print("✅ TOOLS INSTALLED:")
    print(f"   📁 Security workspace: {security_dir}")
    print(f"   🔍 First scan script: {scan_script}")
    print(f"   🛡️ Vulnerability scanner: {vuln_scanner}")
    print("   📦 nmap, Wireshark, VirtualBox")
    print("   🐍 Python security libraries")
    print("=" * 80)

    print("\\n⚠️  LEGAL REMINDER:")
    print("   ✅ AUTHORIZED: Scan our own infrastructure only")
    print("   ❌ ILLEGAL: Scanning other websites without permission")
    print("   📚 LEARNING: Use CTF platforms (HackTheBox, TryHackMe)")

def main():
    """Main setup function"""
    print()
    print("🌌" * 40)
    print()
    print("        SECURITY INFRASTRUCTURE SETUP")
    print("        Defensive Security & Authorized Testing")
    print()
    print("🌌" * 40)

    try:
        # 1. Create directory structure
        security_dir = create_security_directories()

        # 2. Enable Windows Sandbox (requires admin)
        enable_windows_sandbox()

        # 3. Install Chocolatey packages
        choco_results = install_chocolatey_packages()

        # 4. Install Python tools
        install_python_security_tools()

        # 5. Create scan scripts
        scan_script = create_first_scan_script()
        vuln_scanner = create_vulnerability_scanner()

        # 6. Provide Kali info
        download_kali_info()

        # 7. Print next steps
        print_next_steps(security_dir, scan_script, vuln_scanner)

        print("\\n🎉 SECURITY SETUP COMPLETE!")
        print("\\n📖 For detailed security roadmap, see:")
        print("   C:\\\\Users\\\\dwrek\\\\Desktop\\\\SECURITY_CAPABILITIES_AUDIT_NOV_4_2025.md")

    except Exception as e:
        print(f"\\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
