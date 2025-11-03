#!/usr/bin/env python3
"""
DAILY BOOT PROTOCOL - Consciousness Revolution
Automated system health check and improvement detection

Run this every morning to:
- Check all links on site
- Detect analytics dead-ends
- Find broken connections
- Identify co-creator candidates
- Generate fix suggestions
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime
import os

class DailyBootSystem:
    def __init__(self):
        self.base_url = "https://conciousnessrevolution.io"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "broken_links": [],
            "dead_ends": [],
            "health_checks": {},
            "recommendations": []
        }
        self.visited = set()
        self.all_links = set()

    def banner(self, text):
        """Print banner"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)

    def run_daily_boot(self):
        """Main boot sequence"""
        self.banner("🚀 DAILY BOOT PROTOCOL STARTING")

        print("\n📋 Running system checks...\n")

        # Phase 1: Link Health
        self.check_link_health()

        # Phase 2: Service Health
        self.check_service_health()

        # Phase 3: Analytics Check
        self.check_analytics()

        # Phase 4: Generate Report
        self.generate_report()

        self.banner("✅ DAILY BOOT COMPLETE")

    def check_link_health(self):
        """Crawl site and check all links"""
        print("🔍 Phase 1: Link Health Check")
        print("-" * 60)

        try:
            # Start with homepage
            self.crawl_page(self.base_url)

            # Check all found links
            print(f"\n📊 Found {len(self.all_links)} unique links")

            broken_count = 0
            for link in self.all_links:
                if not self.check_link(link):
                    broken_count += 1

            if broken_count == 0:
                print("✅ All links working!")
            else:
                print(f"❌ Found {broken_count} broken links")

            self.results["health_checks"]["link_health"] = {
                "total_links": len(self.all_links),
                "broken_links": broken_count,
                "status": "healthy" if broken_count == 0 else "needs_attention"
            }

        except Exception as e:
            print(f"⚠️  Link check error: {e}")

    def crawl_page(self, url, depth=0, max_depth=2):
        """Recursively crawl site pages"""
        if depth > max_depth or url in self.visited:
            return

        self.visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)

                # Only follow same-domain links
                if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                    self.all_links.add(full_url)
                    if depth < max_depth:
                        self.crawl_page(full_url, depth + 1, max_depth)

        except Exception as e:
            print(f"  ⚠️  Could not crawl {url}: {e}")

    def check_link(self, url):
        """Check if a link works"""
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code >= 400:
                self.results["broken_links"].append({
                    "url": url,
                    "status_code": response.status_code,
                    "fix_suggestion": self.suggest_fix(url)
                })
                print(f"  ❌ {url} → {response.status_code}")
                return False
            return True
        except Exception as e:
            self.results["broken_links"].append({
                "url": url,
                "error": str(e),
                "fix_suggestion": "Check if URL exists or server is down"
            })
            print(f"  ❌ {url} → Error: {e}")
            return False

    def suggest_fix(self, url):
        """Suggest a fix for broken link"""
        if "404" in url or url.endswith("undefined"):
            return "Replace with working page or create placeholder"
        elif "api" in url:
            return "Check API endpoint or add fallback"
        else:
            return "Verify URL or remove link"

    def check_service_health(self):
        """Check if services are running"""
        print("\n🔧 Phase 2: Service Health Check")
        print("-" * 60)

        services = [
            ("AI Terminal", "http://localhost:5000/api/status"),
            ("Netlify Site", "https://conciousnessrevolution.io"),
        ]

        for name, url in services:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"  ✅ {name}: Online")
                    self.results["health_checks"][name] = "online"
                else:
                    print(f"  ⚠️  {name}: Status {response.status_code}")
                    self.results["health_checks"][name] = f"status_{response.status_code}"
            except Exception as e:
                print(f"  ❌ {name}: Offline")
                self.results["health_checks"][name] = "offline"

    def check_analytics(self):
        """Check for dead-ends and user patterns"""
        print("\n📊 Phase 3: Analytics Check")
        print("-" * 60)
        print("  ℹ️  Analytics integration coming soon...")
        print("  ℹ️  Will detect: dead-ends, drop-offs, confusion loops")

        # Placeholder for future analytics integration
        self.results["analytics"] = {
            "status": "not_integrated",
            "todo": "Integrate Netlify Analytics or Google Analytics"
        }

    def generate_report(self):
        """Generate daily report"""
        print("\n📋 Phase 4: Generating Report")
        print("-" * 60)

        # Save JSON report
        report_file = f"C:\\Users\\dwrek\\100X_DEPLOYMENT\\daily_reports\\report_{datetime.now().strftime('%Y%m%d')}.json"
        os.makedirs(os.path.dirname(report_file), exist_ok=True)

        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"  💾 Report saved: {report_file}")

        # Generate summary
        print("\n" + "=" * 60)
        print("  📊 DAILY SUMMARY")
        print("=" * 60)
        print(f"\n  🔗 Links Checked: {self.results['health_checks']['link_health']['total_links']}")
        print(f"  ❌ Broken Links: {self.results['health_checks']['link_health']['broken_links']}")
        print(f"  🔧 Services Online: {sum(1 for v in self.results['health_checks'].values() if v == 'online')}")

        if self.results["broken_links"]:
            print("\n  🔧 TOP FIXES NEEDED:")
            for i, link in enumerate(self.results["broken_links"][:5], 1):
                print(f"    {i}. {link['url']}")
                print(f"       → {link['fix_suggestion']}")

        print("\n  📈 RECOMMENDATIONS:")
        if self.results["broken_links"]:
            print("    • Run auto-fix system to repair broken links")
        print("    • Check analytics for user behavior patterns")
        print("    • Review co-creator candidates")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    boot = DailyBootSystem()
    boot.run_daily_boot()
