#!/usr/bin/env python3
"""
ANALYTICS DEAD-END DETECTOR
Finds where users get stuck, confused, or drop off

Detects:
- Pages where users immediately leave (bounce)
- Pages where users loop between same 2-3 pages (confusion)
- Pages with no next action (dead ends)
- High exit pages (where journeys end)
"""

import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class AnalyticsDeadEndDetector:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "dead_ends": [],
            "confusion_loops": [],
            "high_bounce_pages": [],
            "drop_off_points": [],
            "recommendations": []
        }

    def banner(self, text):
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)

    def analyze_netlify_analytics(self):
        """
        Analyze Netlify Analytics data
        Note: Requires Netlify Analytics API access
        """
        self.banner("📊 ANALYTICS DEAD-END DETECTION")

        print("\n🔍 Checking for analytics data sources...\n")

        # Check if Netlify Analytics is available
        analytics_available = self.check_netlify_analytics()

        if not analytics_available:
            print("⚠️  Netlify Analytics not yet integrated")
            print("\n📋 TO ENABLE ANALYTICS:")
            print("   1. Go to: https://app.netlify.com")
            print("   2. Select your site: consciousnessrevolution.io")
            print("   3. Enable Netlify Analytics ($9/month)")
            print("   4. Or integrate Google Analytics (free)")
            print("\n💡 FOR NOW: Using pattern detection on site structure")
            self.detect_structural_dead_ends()
        else:
            self.analyze_real_analytics_data()

    def check_netlify_analytics(self):
        """Check if analytics is available"""
        # This would check for actual analytics data
        # For now, returns False to trigger structural analysis
        return False

    def detect_structural_dead_ends(self):
        """
        Detect potential dead-ends by analyzing site structure
        Even without analytics, we can find architectural problems
        """
        print("\n🏗️  STRUCTURAL ANALYSIS (No User Data Needed)")
        print("-" * 60)

        base_url = "https://conciousnessrevolution.io"

        # Pages to check
        pages_to_check = [
            "get-help.html",
            "philosopher-ai.html",
            "philosopher-ai-connected.html",
            "platform-city-map.html",
            "cheat-codes.html",
            "module-library.html"
        ]

        print("\n🔍 Analyzing page structure for dead-ends...\n")

        for page in pages_to_check:
            url = f"{base_url}/{page}"
            analysis = self.analyze_page_structure(url, page)

            if analysis:
                if analysis['is_dead_end']:
                    self.results['dead_ends'].append(analysis)
                    print(f"  ❌ DEAD-END: {page}")
                    print(f"     → {analysis['reason']}")
                else:
                    print(f"  ✅ OK: {page} → {analysis['next_actions']} actions")

        # NEW: Detect confusion loops
        print("\n🔄 Analyzing navigation for confusion loops...\n")
        self.detect_confusion_loops(base_url, pages_to_check)

    def analyze_page_structure(self, url, page_name):
        """Analyze a page to see if it's a dead-end"""
        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                return {
                    'page': page_name,
                    'url': url,
                    'is_dead_end': True,
                    'reason': f'Page returns {response.status_code}',
                    'fix': 'Fix or remove this page',
                    'next_actions': 0
                }

            content = response.text.lower()

            # Count potential next actions
            next_actions = 0
            next_actions += content.count('<a href=')  # Links
            next_actions += content.count('<button')   # Buttons
            next_actions += content.count('onclick=')  # Click handlers
            next_actions += content.count('<form')     # Forms

            # Detect common dead-end patterns
            is_dead_end = False
            reason = ""

            if next_actions < 3:
                is_dead_end = True
                reason = f"Only {next_actions} interactive elements - users have nowhere to go"

            if 'under construction' in content or 'coming soon' in content:
                is_dead_end = True
                reason = "Page shows 'under construction' or 'coming soon'"

            if next_actions == 0:
                is_dead_end = True
                reason = "No links, buttons, or interactive elements at all"

            return {
                'page': page_name,
                'url': url,
                'is_dead_end': is_dead_end,
                'reason': reason if is_dead_end else "Has clear next steps",
                'next_actions': next_actions,
                'fix': self.suggest_dead_end_fix(page_name, reason) if is_dead_end else None
            }

        except Exception as e:
            return {
                'page': page_name,
                'url': url,
                'is_dead_end': True,
                'reason': f'Could not load page: {e}',
                'fix': 'Check if page exists and is accessible',
                'next_actions': 0
            }

    def suggest_dead_end_fix(self, page_name, reason):
        """Suggest how to fix a dead-end page"""
        if 'construction' in reason.lower():
            return "Add 'Return to Home' button or remove page until complete"
        elif 'no' in reason.lower() and 'elements' in reason.lower():
            return "Add navigation menu, 'Back' button, or related links"
        elif 'few' in reason.lower():
            return "Add more navigation options or clear call-to-action"
        else:
            return "Improve page navigation and add clear next steps"

    def extract_links(self, html_content, base_url):
        """Extract all internal links from HTML content"""
        from bs4 import BeautifulSoup

        links = set()
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']

                # Handle relative URLs
                if href.startswith('/'):
                    href = href[1:]  # Remove leading slash
                elif href.startswith('http'):
                    # Skip external links
                    if base_url not in href:
                        continue
                    # Extract just the page name
                    href = href.replace(base_url + '/', '')

                # Only track HTML pages
                if href.endswith('.html') or (not '.' in href and href):
                    links.add(href)
        except Exception as e:
            print(f"    ⚠️  Error extracting links: {e}")

        return links

    def detect_confusion_loops(self, base_url, pages_to_check):
        """
        Detect confusion loops - circular navigation patterns
        Simulates a user clicking through pages and tracks if they end up in circles

        ENHANCED: Now detects auth loops like the one we just fixed!
        """
        from bs4 import BeautifulSoup

        # Build navigation graph
        nav_graph = {}

        for page in pages_to_check:
            url = f"{base_url}/{page}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    links = self.extract_links(response.text, base_url)
                    nav_graph[page] = links

                    # ENHANCED: Check for authentication/form loops
                    content = response.text.lower()
                    if 'account already exists' in content or 'no account' in content:
                        # Potential auth loop - check if there's an escape
                        has_skip = 'skip' in content or 'browse' in content or 'later' in content
                        if not has_skip:
                            auth_loop = {
                                'pages': [page],
                                'pattern': f'{page} → Auth Loop (no escape)',
                                'severity': 'CRITICAL',
                                'explanation': 'Authentication loop with no skip/escape option',
                                'fix': 'Add "Skip for now" or "Browse without account" button'
                            }
                            self.results['confusion_loops'].append(auth_loop)
                            print(f"  🚨 AUTH LOOP: {page} has no escape!")

            except Exception as e:
                print(f"  ⚠️  Could not analyze {page}: {e}")
                nav_graph[page] = set()

        # Simulate user journeys to detect loops
        print("  Simulating user journeys...\n")

        for start_page in pages_to_check:
            loops_found = self.find_loops_from_page(start_page, nav_graph, max_depth=5)

            for loop in loops_found:
                if len(loop) >= 2:  # Minimum 2 pages for a meaningful loop
                    loop_info = {
                        'pages': loop,
                        'pattern': ' → '.join(loop) + ' → (back to start)',
                        'severity': 'HIGH' if len(loop) == 2 else 'MEDIUM',
                        'explanation': f"Users might get stuck navigating between {len(loop)} pages",
                        'fix': 'Add escape route or clear navigation to other sections'
                    }

                    # Only add unique loops
                    if loop_info not in self.results['confusion_loops']:
                        self.results['confusion_loops'].append(loop_info)
                        print(f"  ⚠️  LOOP DETECTED: {loop_info['pattern']}")

        if not self.results['confusion_loops']:
            print("  ✅ No obvious confusion loops detected!")

    def find_loops_from_page(self, start_page, nav_graph, max_depth=5):
        """
        Find circular navigation patterns starting from a page
        Uses depth-first search to detect cycles
        """
        loops = []

        def dfs(current, path, visited):
            if len(path) > max_depth:
                return

            if current in visited and current == start_page and len(path) > 1:
                # Found a loop back to start
                loops.append(path[:])
                return

            if current in visited:
                return

            visited.add(current)
            path.append(current)

            # Explore neighbors
            if current in nav_graph:
                for next_page in nav_graph[current]:
                    dfs(next_page, path[:], visited.copy())

        dfs(start_page, [], set())
        return loops

    def generate_recommendations(self):
        """Generate actionable recommendations"""
        print("\n📋 GENERATING RECOMMENDATIONS")
        print("-" * 60)

        if self.results['dead_ends']:
            print(f"\n⚠️  Found {len(self.results['dead_ends'])} dead-end pages")
            print("\n🔧 TOP FIXES NEEDED:\n")

            for i, dead_end in enumerate(self.results['dead_ends'][:5], 1):
                print(f"  {i}. {dead_end['page']}")
                print(f"     Problem: {dead_end['reason']}")
                print(f"     Fix: {dead_end['fix']}")
                print()

            self.results['recommendations'].append({
                'priority': 'HIGH',
                'action': 'Fix dead-end pages',
                'count': len(self.results['dead_ends']),
                'impact': 'Prevents users from getting stuck'
            })
        else:
            print("\n✅ No obvious structural dead-ends found!")

        # Always recommend analytics
        self.results['recommendations'].append({
            'priority': 'MEDIUM',
            'action': 'Enable Netlify Analytics or Google Analytics',
            'impact': 'Get real user behavior data for deeper insights'
        })

    def save_report(self):
        """Save analysis report"""
        report_file = f"C:\\Users\\dwrek\\100X_DEPLOYMENT\\analytics_reports\\dead_end_analysis_{datetime.now().strftime('%Y%m%d')}.json"

        import os
        os.makedirs(os.path.dirname(report_file), exist_ok=True)

        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n💾 Report saved: {report_file}")

    def run_analysis(self):
        """Main analysis"""
        self.banner("🚀 ANALYTICS DEAD-END DETECTOR")

        self.analyze_netlify_analytics()
        self.generate_recommendations()
        self.save_report()

        self.banner("✅ ANALYSIS COMPLETE")


if __name__ == "__main__":
    detector = AnalyticsDeadEndDetector()
    detector.run_analysis()
