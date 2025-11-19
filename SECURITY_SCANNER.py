#!/usr/bin/env python3
"""
🛡️ AUTOMATED SECURITY SCANNER
Detects XSS vulnerabilities and information disclosure across 100X platform
Built: October 17, 2025
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class SecurityScanner:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.vulnerabilities = []
        self.stats = {
            'files_scanned': 0,
            'xss_vulnerabilities': 0,
            'info_disclosure': 0,
            'unsafe_innerHTML': 0,
            'console_log_leaks': 0
        }

    def scan_all_files(self):
        """Scan all HTML and JS files for vulnerabilities"""
        print("🔍 Starting security scan...")

        # Scan HTML files
        for html_file in self.base_path.rglob('*.html'):
            self.scan_file(html_file, 'html')

        # Scan JS files
        for js_file in self.base_path.rglob('*.js'):
            self.scan_file(js_file, 'js')

        return self.generate_report()

    def scan_file(self, file_path, file_type):
        """Scan individual file for vulnerabilities"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

            self.stats['files_scanned'] += 1

            # Check for unsafe innerHTML usage
            self.check_innerHTML(file_path, content, lines)

            # Check for console.log information disclosure
            self.check_console_log(file_path, content, lines)

        except Exception as e:
            print(f"⚠️ Error scanning {file_path}: {e}")

    def check_innerHTML(self, file_path, content, lines):
        """Detect unsafe innerHTML usage that could lead to XSS"""

        # Pattern: innerHTML = ... without SafeDOM
        pattern = r'\.innerHTML\s*=\s*([^;]+)'

        for match in re.finditer(pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            assignment = match.group(1)

            # Check if SafeDOM.escapeHTML is used
            if 'SafeDOM' not in assignment and 'escapeHTML' not in assignment:
                # Check if it contains user-generated content patterns
                user_content_patterns = [
                    r'\$\{[^}]*\.(name|email|message|content|text|username|comment)',
                    r'\+\s*[a-z]+\.(name|email|message|content|text|username|comment)',
                    r'data\.',
                    r'user\.',
                    r'submission\.',
                    r'sub\.'
                ]

                is_dangerous = any(re.search(p, assignment) for p in user_content_patterns)

                if is_dangerous:
                    self.vulnerabilities.append({
                        'type': 'XSS_VULNERABILITY',
                        'severity': 'HIGH',
                        'file': str(file_path.relative_to(self.base_path)),
                        'line': line_num,
                        'code': lines[line_num - 1].strip() if line_num <= len(lines) else '',
                        'description': 'Unsafe innerHTML usage with user-generated content',
                        'fix': 'Apply SafeDOM.escapeHTML() or use textContent instead'
                    })
                    self.stats['xss_vulnerabilities'] += 1
                    self.stats['unsafe_innerHTML'] += 1

    def check_console_log(self, file_path, content, lines):
        """Detect console.log statements that leak sensitive information"""

        # Pattern: console.log with user data
        pattern = r'console\.log\([^)]*\b(username|email|password|token|user|data|credentials)\b[^)]*\)'

        for match in re.finditer(pattern, content, re.IGNORECASE):
            line_num = content[:match.start()].count('\n') + 1

            self.vulnerabilities.append({
                'type': 'INFO_DISCLOSURE',
                'severity': 'MEDIUM',
                'file': str(file_path.relative_to(self.base_path)),
                'line': line_num,
                'code': lines[line_num - 1].strip() if line_num <= len(lines) else '',
                'description': 'console.log may leak sensitive information',
                'fix': 'Remove or replace with console.error for production'
            })
            self.stats['info_disclosure'] += 1
            self.stats['console_log_leaks'] += 1

    def generate_report(self):
        """Generate comprehensive security report"""
        report = {
            'scan_date': datetime.now().isoformat(),
            'stats': self.stats,
            'vulnerabilities': self.vulnerabilities,
            'summary': self.generate_summary()
        }

        return report

    def generate_summary(self):
        """Generate human-readable summary"""
        total_vulns = len(self.vulnerabilities)
        critical = sum(1 for v in self.vulnerabilities if v['severity'] == 'CRITICAL')
        high = sum(1 for v in self.vulnerabilities if v['severity'] == 'HIGH')
        medium = sum(1 for v in self.vulnerabilities if v['severity'] == 'MEDIUM')

        return {
            'total_vulnerabilities': total_vulns,
            'by_severity': {
                'critical': critical,
                'high': high,
                'medium': medium
            },
            'security_score': max(0, 100 - (critical * 10 + high * 5 + medium * 2)),
            'manipulation_immunity': max(0, 100 - (critical * 8 + high * 4 + medium * 1.5))
        }

    def save_report(self, output_file):
        """Save report to JSON file"""
        report = self.generate_report()

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✅ Report saved to: {output_file}")
        return report

    def print_summary(self, report):
        """Print summary to console"""
        print("\n" + "="*80)
        print("🛡️ SECURITY SCAN RESULTS")
        print("="*80)

        print(f"\n📊 Files Scanned: {report['stats']['files_scanned']}")
        print(f"🔍 Total Vulnerabilities: {report['summary']['total_vulnerabilities']}")

        print("\n🎯 By Severity:")
        print(f"   🔴 Critical: {report['summary']['by_severity']['critical']}")
        print(f"   🟠 High: {report['summary']['by_severity']['high']}")
        print(f"   🟡 Medium: {report['summary']['by_severity']['medium']}")

        print("\n📈 Security Metrics:")
        print(f"   Security Score: {report['summary']['security_score']}/100")
        print(f"   Manipulation Immunity: {report['summary']['manipulation_immunity']}%")

        print("\n🔥 Vulnerability Breakdown:")
        print(f"   XSS Vulnerabilities: {report['stats']['xss_vulnerabilities']}")
        print(f"   Info Disclosure: {report['stats']['info_disclosure']}")
        print(f"   Unsafe innerHTML: {report['stats']['unsafe_innerHTML']}")
        print(f"   Console.log Leaks: {report['stats']['console_log_leaks']}")

        # Show top 10 most critical files
        if report['vulnerabilities']:
            print("\n⚠️ TOP PRIORITY FIXES:")

            # Group by file
            files_with_vulns = {}
            for vuln in report['vulnerabilities']:
                file = vuln['file']
                if file not in files_with_vulns:
                    files_with_vulns[file] = []
                files_with_vulns[file].append(vuln)

            # Sort by number of vulnerabilities
            sorted_files = sorted(files_with_vulns.items(), key=lambda x: len(x[1]), reverse=True)

            for i, (file, vulns) in enumerate(sorted_files[:10], 1):
                high_count = sum(1 for v in vulns if v['severity'] == 'HIGH')
                medium_count = sum(1 for v in vulns if v['severity'] == 'MEDIUM')
                print(f"\n   {i}. {file}")
                print(f"      🔴 {high_count} HIGH | 🟡 {medium_count} MEDIUM")

                # Show first vulnerability as example
                if vulns:
                    print(f"      Line {vulns[0]['line']}: {vulns[0]['description']}")

        print("\n" + "="*80)


def main():
    """Run security scanner"""
    base_path = Path(__file__).parent

    print("🛡️ 100X SECURITY SCANNER v1.0")
    print(f"📁 Scanning: {base_path}")

    scanner = SecurityScanner(base_path)
    report = scanner.scan_all_files()

    # Save report
    output_file = base_path / 'SECURITY_SCAN_REPORT.json'
    scanner.save_report(output_file)

    # Print summary
    scanner.print_summary(report)

    # Generate action items
    print("\n🎯 NEXT ACTIONS:")
    if report['summary']['by_severity']['high'] > 0:
        print("   1. Fix HIGH severity XSS vulnerabilities immediately")
        print("   2. Apply SafeDOM.escapeHTML() to all user input")
    if report['summary']['by_severity']['medium'] > 0:
        print("   3. Remove console.log statements with sensitive data")
    print("   4. Re-run scanner after fixes applied")
    print("\n🚀 Security Score Target: 95/100 (Manipulation Immunity: 95%+)")


if __name__ == '__main__':
    main()
