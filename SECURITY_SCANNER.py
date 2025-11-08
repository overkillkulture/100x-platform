"""SECURITY SCANNER - Scan code for vulnerabilities"""
import re, os
from typing import List
from dataclasses import dataclass

@dataclass
class SecurityIssue:
    severity: str
    category: str
    file: str
    line: int
    description: str

class SecurityScanner:
    def __init__(self):
        self.issues: List[SecurityIssue] = []
        self.patterns = {
            'sql_injection': (r'execute.*SELECT', 'critical', 'SQL injection risk'),
            'eval_usage': (r'\beval\s*\(', 'high', 'Dangerous eval() usage'),
            'hardcoded_secret': (r'password\s*=\s*["\'][^"\']+', 'high', 'Hardcoded password'),
        }

    def scan_file(self, filepath: str):
        try:
            with open(filepath, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    for cat, (pattern, sev, desc) in self.patterns.items():
                        if re.search(pattern, line, re.I):
                            self.issues.append(SecurityIssue(sev, cat, filepath, line_num, desc))
        except: pass

    def scan_directory(self, directory: str):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    self.scan_file(os.path.join(root, file))

    def generate_report(self) -> str:
        report = f"Security Scan: {len(self.issues)} issues found\n"
        for issue in self.issues:
            report += f"[{issue.severity}] {issue.file}:{issue.line} - {issue.description}\n"
        return report

if __name__ == "__main__":
    print("✅ Security Scanner ready!")
