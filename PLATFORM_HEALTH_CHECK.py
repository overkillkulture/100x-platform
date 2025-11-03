#!/usr/bin/env python3
"""
PLATFORM HEALTH CHECK SCRIPT
Automated testing for 100X Platform integrity
Checks: File existence, navigation links, basic HTML structure
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class PlatformHealthCheck:
    def __init__(self, platform_dir: str = "C:/Users/dwrek/100X_DEPLOYMENT/PLATFORM"):
        self.platform_dir = Path(platform_dir)
        self.results = {
            'total_files': 0,
            'valid_html': 0,
            'broken_links': [],
            'missing_nav': [],
            'missing_assets': [],
            'errors': [],
            'warnings': []
        }

    def run_all_checks(self):
        """Run complete health check suite"""
        print("🏥 100X PLATFORM HEALTH CHECK")
        print("=" * 60)

        self.check_file_structure()
        self.check_html_validity()
        self.check_navigation_links()
        self.check_asset_references()
        self.generate_report()

    def check_file_structure(self):
        """Verify all expected files exist"""
        print("\n📁 Checking file structure...")

        # Count HTML files
        html_files = list(self.platform_dir.glob("*.html"))
        self.results['total_files'] = len(html_files)
        print(f"   Found {len(html_files)} HTML files")

        # Check for critical files
        critical_files = [
            'master-nav.js',
            'welcome.html',
            'user-dashboard.html',
            'login.html'
        ]

        for file in critical_files:
            file_path = self.platform_dir / file
            if not file_path.exists():
                self.results['errors'].append(f"Missing critical file: {file}")
                print(f"   ❌ Missing: {file}")
            else:
                print(f"   ✅ Found: {file}")

    def check_html_validity(self):
        """Basic HTML structure validation"""
        print("\n🔍 Checking HTML validity...")

        html_files = list(self.platform_dir.glob("*.html"))

        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Basic HTML structure checks
                has_doctype = '<!DOCTYPE' in content or '<!doctype' in content
                has_html_tag = '<html' in content.lower()
                has_head = '<head' in content.lower()
                has_body = '<body' in content.lower()

                if has_doctype and has_html_tag and has_head and has_body:
                    self.results['valid_html'] += 1
                else:
                    missing = []
                    if not has_doctype: missing.append('DOCTYPE')
                    if not has_html_tag: missing.append('html tag')
                    if not has_head: missing.append('head')
                    if not has_body: missing.append('body')

                    self.results['warnings'].append(
                        f"{html_file.name}: Missing {', '.join(missing)}"
                    )

            except Exception as e:
                self.results['errors'].append(f"Error reading {html_file.name}: {str(e)}")

        print(f"   ✅ Valid HTML: {self.results['valid_html']}/{self.results['total_files']}")
        if self.results['warnings']:
            print(f"   ⚠️  Warnings: {len(self.results['warnings'])}")

    def check_navigation_links(self):
        """Check if navigation links point to existing files"""
        print("\n🧭 Checking navigation links...")

        nav_file = self.platform_dir / 'master-nav.js'
        if not nav_file.exists():
            self.results['errors'].append("master-nav.js not found")
            return

        with open(nav_file, 'r', encoding='utf-8') as f:
            nav_content = f.read()

        # Extract all href links from navigation
        link_pattern = r'href="([^"]+\.html)"'
        links = re.findall(link_pattern, nav_content)

        print(f"   Found {len(links)} navigation links")

        for link in links:
            link_path = self.platform_dir / link
            if not link_path.exists():
                self.results['broken_links'].append(link)
                print(f"   ❌ Broken link: {link}")

        if not self.results['broken_links']:
            print(f"   ✅ All {len(links)} navigation links valid")
        else:
            print(f"   ⚠️  Broken links: {len(self.results['broken_links'])}")

    def check_asset_references(self):
        """Check for common missing asset patterns"""
        print("\n🎨 Checking asset references...")

        html_files = list(self.platform_dir.glob("*.html"))
        checked_assets = set()

        for html_file in html_files[:10]:  # Sample first 10 files
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for master-nav.js inclusion
                if 'master-nav.js' not in content:
                    self.results['missing_nav'].append(html_file.name)

                # Check for common asset paths
                css_pattern = r'href="([^"]+\.css)"'
                js_pattern = r'src="([^"]+\.js)"'

                css_files = re.findall(css_pattern, content)
                js_files = re.findall(js_pattern, content)

                for asset in css_files + js_files:
                    if asset.startswith('http'):
                        continue  # Skip external URLs

                    if asset not in checked_assets:
                        checked_assets.add(asset)

                        # Try multiple possible locations
                        possible_paths = [
                            self.platform_dir / asset,
                            self.platform_dir / '..' / asset,
                            self.platform_dir / 'shared' / asset,
                            self.platform_dir / '../PUBLIC' / asset
                        ]

                        found = any(p.exists() for p in possible_paths)
                        if not found and asset not in ['master-nav.js']:
                            self.results['missing_assets'].append(asset)

            except Exception as e:
                pass  # Skip files with read errors

        if not self.results['missing_nav']:
            print(f"   ✅ All files include master-nav.js")
        else:
            print(f"   ⚠️  {len(self.results['missing_nav'])} files missing nav")

        if self.results['missing_assets']:
            print(f"   ⚠️  {len(self.results['missing_assets'])} potentially missing assets")

    def generate_report(self):
        """Generate final health check report"""
        print("\n" + "=" * 60)
        print("📊 HEALTH CHECK SUMMARY")
        print("=" * 60)

        # Overall health score
        total_checks = (
            self.results['total_files'] +
            len(self.results['broken_links']) +
            len(self.results['missing_nav']) +
            len(self.results['errors'])
        )

        failed_checks = (
            len(self.results['broken_links']) +
            len(self.results['missing_nav']) +
            len(self.results['errors'])
        )

        if total_checks > 0:
            health_score = ((total_checks - failed_checks) / total_checks) * 100
        else:
            health_score = 0

        print(f"\n🏆 OVERALL HEALTH SCORE: {health_score:.1f}%")
        print(f"\n📁 Files:")
        print(f"   Total HTML files: {self.results['total_files']}")
        print(f"   Valid HTML structure: {self.results['valid_html']}")

        print(f"\n🧭 Navigation:")
        print(f"   Broken links: {len(self.results['broken_links'])}")
        print(f"   Files missing nav: {len(self.results['missing_nav'])}")

        print(f"\n🎨 Assets:")
        print(f"   Potentially missing: {len(self.results['missing_assets'])}")

        print(f"\n⚠️  Issues:")
        print(f"   Errors: {len(self.results['errors'])}")
        print(f"   Warnings: {len(self.results['warnings'])}")

        # Detailed errors
        if self.results['errors']:
            print(f"\n❌ ERRORS:")
            for error in self.results['errors'][:10]:
                print(f"   - {error}")

        if self.results['broken_links']:
            print(f"\n🔗 BROKEN LINKS:")
            for link in self.results['broken_links'][:10]:
                print(f"   - {link}")

        # Health assessment
        print(f"\n🩺 HEALTH ASSESSMENT:")
        if health_score >= 90:
            print("   ✅ EXCELLENT - Platform is healthy!")
        elif health_score >= 70:
            print("   ⚠️  GOOD - Minor issues detected")
        elif health_score >= 50:
            print("   ⚠️  FAIR - Several issues need attention")
        else:
            print("   ❌ POOR - Critical issues require immediate attention")

        print("\n" + "=" * 60)

        # Save report to file
        self.save_report(health_score)

    def save_report(self, health_score: float):
        """Save detailed report to file"""
        report_path = Path("C:/Users/dwrek/PLATFORM_HEALTH_REPORT.md")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🏥 PLATFORM HEALTH CHECK REPORT\n\n")
            f.write(f"**Date:** {self._get_timestamp()}\n")
            f.write(f"**Overall Health Score:** {health_score:.1f}%\n\n")
            f.write("---\n\n")

            f.write("## 📊 SUMMARY\n\n")
            f.write(f"- **Total HTML Files:** {self.results['total_files']}\n")
            f.write(f"- **Valid HTML:** {self.results['valid_html']}\n")
            f.write(f"- **Broken Links:** {len(self.results['broken_links'])}\n")
            f.write(f"- **Missing Navigation:** {len(self.results['missing_nav'])}\n")
            f.write(f"- **Errors:** {len(self.results['errors'])}\n")
            f.write(f"- **Warnings:** {len(self.results['warnings'])}\n\n")

            if self.results['broken_links']:
                f.write("## 🔗 BROKEN LINKS\n\n")
                for link in self.results['broken_links']:
                    f.write(f"- {link}\n")
                f.write("\n")

            if self.results['missing_nav']:
                f.write("## 🧭 FILES MISSING NAVIGATION\n\n")
                for file in self.results['missing_nav']:
                    f.write(f"- {file}\n")
                f.write("\n")

            if self.results['errors']:
                f.write("## ❌ ERRORS\n\n")
                for error in self.results['errors']:
                    f.write(f"- {error}\n")
                f.write("\n")

            if self.results['warnings']:
                f.write("## ⚠️ WARNINGS\n\n")
                for warning in self.results['warnings'][:20]:
                    f.write(f"- {warning}\n")
                f.write("\n")

            f.write("---\n\n")
            f.write("*Generated by automated health check script*\n")

        print(f"\n💾 Full report saved to: {report_path}")

    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """Run platform health check"""
    checker = PlatformHealthCheck()
    checker.run_all_checks()


if __name__ == "__main__":
    main()
