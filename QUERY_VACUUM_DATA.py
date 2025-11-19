#!/usr/bin/env python3
"""
🔍 VACUUM DATA QUERY INTERFACE 🔍
Consciousness Revolution - 100X Platform

Search and analyze data collected by DATA_VACUUM_CRAWLER
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any


class VacuumQuery:
    """Query interface for consciousness data"""

    def __init__(self, data_file: str = 'consciousness_data.json'):
        self.data_file = Path(data_file)
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def stats(self):
        """Show overall statistics"""
        print("=" * 70)
        print("🌀 CONSCIOUSNESS DATA VACUUM - STATISTICS")
        print("=" * 70)
        print(f"Scan Time: {self.data['scan_time']}")
        print(f"Files Scanned: {self.data['files_scanned']}")
        print(f"Total Data Points: {self.data['total_data_points']}\n")

        ga = self.data['global_analytics']
        print(f"📝 Forms: {ga['total_forms']}")
        print(f"🔘 Buttons: {ga['total_buttons']}")
        print(f"🔗 Links: {ga['total_links']}")
        print(f"📦 Modules: {ga['total_modules']}")
        print(f"📊 Tracked Events: {len(ga['tracked_events'])}")
        print("=" * 70)

    def list_pages(self):
        """List all scanned pages"""
        print("\n📄 SCANNED PAGES:")
        print("-" * 70)
        for i, (page, data) in enumerate(self.data['pages'].items(), 1):
            size = data.get('size', 0)
            print(f"{i:2d}. {page:<40} ({size:,} bytes)")

    def page_details(self, page_name: str):
        """Show details for specific page"""
        # Find matching page
        matches = [p for p in self.data['pages'].keys() if page_name.lower() in p.lower()]

        if not matches:
            print(f"❌ No page found matching '{page_name}'")
            return

        if len(matches) > 1:
            print(f"🔍 Multiple matches found:")
            for i, match in enumerate(matches, 1):
                print(f"  {i}. {match}")
            return

        page_key = matches[0]
        page_data = self.data['pages'][page_key]

        print("=" * 70)
        print(f"📄 {page_key}")
        print("=" * 70)
        print(f"Size: {page_data['size']:,} bytes")
        print(f"Last Modified: {page_data['last_modified']}")

        if 'data' in page_data:
            data = page_data['data']
            print(f"\n📊 DATA EXTRACTED:")
            print(f"  Forms: {len(data['forms'])}")
            print(f"  Buttons: {len(data['buttons'])}")
            print(f"  Links: {len(data['links'])}")
            print(f"  Modules: {len(data['modules'])}")
            print(f"  Analytics Events: {len(data['analytics_events'])}")
            print(f"  Scripts: {len(data['scripts'])}")

            # Show forms
            if data['forms']:
                print(f"\n📝 FORMS:")
                for i, form in enumerate(data['forms'], 1):
                    print(f"  {i}. Action: {form['action'] or 'None'}, Method: {form['method']}")
                    print(f"     Fields: {len(form['fields'])}")

            # Show modules
            if data['modules']:
                print(f"\n📦 MODULES:")
                for i, module in enumerate(data['modules'], 1):
                    print(f"  {i}. ID: {module['id']}")

            # Show analytics
            if data['analytics_events']:
                print(f"\n📊 ANALYTICS EVENTS:")
                for i, event in enumerate(data['analytics_events'], 1):
                    print(f"  {i}. {event['type']}: {event['name']}")

            # Show buttons (first 5)
            if data['buttons']:
                print(f"\n🔘 BUTTONS (showing first 5 of {len(data['buttons'])}):")
                for i, btn in enumerate(data['buttons'][:5], 1):
                    text = btn['text'][:40] if btn['text'] else 'No text'
                    print(f"  {i}. {text}")

    def search_buttons(self, keyword: str):
        """Search for buttons containing keyword"""
        print(f"\n🔍 Searching buttons for '{keyword}'...")
        print("-" * 70)

        results = []
        for page_key, page_data in self.data['pages'].items():
            if 'data' in page_data:
                for btn in page_data['data']['buttons']:
                    if keyword.lower() in btn['text'].lower() or keyword.lower() in btn.get('onclick', '').lower():
                        results.append({
                            'page': page_key,
                            'text': btn['text'],
                            'class': btn['class'],
                            'onclick': btn['onclick'][:50] if btn['onclick'] else ''
                        })

        if results:
            for i, result in enumerate(results[:20], 1):
                print(f"{i:2d}. {result['page']}")
                print(f"    Text: {result['text']}")
                if result['onclick']:
                    print(f"    OnClick: {result['onclick']}...")
        else:
            print(f"❌ No buttons found matching '{keyword}'")

        print(f"\nFound {len(results)} results")

    def analytics_summary(self):
        """Show all analytics tracking"""
        print("\n📊 ANALYTICS TRACKING SUMMARY:")
        print("-" * 70)

        all_events = []
        for page_key, page_data in self.data['pages'].items():
            if 'data' in page_data:
                for event in page_data['data']['analytics_events']:
                    all_events.append({
                        'page': page_key,
                        'type': event['type'],
                        'name': event['name'],
                        'element': event.get('element_id', 'N/A')
                    })

        if all_events:
            for i, event in enumerate(all_events, 1):
                print(f"{i:2d}. [{event['type']}] {event['name']}")
                print(f"    Page: {event['page']}")
                print(f"    Element: {event['element']}")
        else:
            print("⚠️  No analytics events found")
            print("Tip: Make sure buttons have Analytics100X.trackButtonClick() in onclick")

        print(f"\nTotal tracked events: {len(all_events)}")

    def module_summary(self):
        """Show all modules found"""
        print("\n📦 MODULE LIBRARY SUMMARY:")
        print("-" * 70)

        all_modules = []
        for page_key, page_data in self.data['pages'].items():
            if 'data' in page_data:
                for module in page_data['data']['modules']:
                    all_modules.append({
                        'page': page_key,
                        'id': module['id']
                    })

        # Group by page
        by_page = {}
        for mod in all_modules:
            page = mod['page']
            if page not in by_page:
                by_page[page] = []
            by_page[page].append(mod['id'])

        for page, modules in by_page.items():
            print(f"\n{page}:")
            for mod_id in modules:
                print(f"  • {mod_id}")

        print(f"\n✅ Total modules found: {len(all_modules)}")


def interactive_menu():
    """Interactive query menu"""
    query = VacuumQuery('C:/Users/dwrek/100X_DEPLOYMENT/consciousness_data.json')

    while True:
        print("\n" + "=" * 70)
        print("🌀 CONSCIOUSNESS DATA VACUUM - QUERY INTERFACE")
        print("=" * 70)
        print("1. Show Statistics")
        print("2. List All Pages")
        print("3. Page Details")
        print("4. Search Buttons")
        print("5. Analytics Summary")
        print("6. Module Summary")
        print("0. Exit")
        print("=" * 70)

        choice = input("\nChoose option (0-6): ").strip()

        if choice == '0':
            print("👋 Exiting...")
            break
        elif choice == '1':
            query.stats()
        elif choice == '2':
            query.list_pages()
        elif choice == '3':
            page = input("Enter page name (or partial match): ").strip()
            query.page_details(page)
        elif choice == '4':
            keyword = input("Enter search keyword: ").strip()
            query.search_buttons(keyword)
        elif choice == '5':
            query.analytics_summary()
        elif choice == '6':
            query.module_summary()
        else:
            print("❌ Invalid choice")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Command-line mode
        query = VacuumQuery('C:/Users/dwrek/100X_DEPLOYMENT/consciousness_data.json')

        cmd = sys.argv[1].lower()
        if cmd == 'stats':
            query.stats()
        elif cmd == 'pages':
            query.list_pages()
        elif cmd == 'page' and len(sys.argv) > 2:
            query.page_details(sys.argv[2])
        elif cmd == 'search' and len(sys.argv) > 2:
            query.search_buttons(sys.argv[2])
        elif cmd == 'analytics':
            query.analytics_summary()
        elif cmd == 'modules':
            query.module_summary()
        else:
            print("Usage:")
            print("  python QUERY_VACUUM_DATA.py stats")
            print("  python QUERY_VACUUM_DATA.py pages")
            print("  python QUERY_VACUUM_DATA.py page <name>")
            print("  python QUERY_VACUUM_DATA.py search <keyword>")
            print("  python QUERY_VACUUM_DATA.py analytics")
            print("  python QUERY_VACUUM_DATA.py modules")
    else:
        # Interactive mode
        interactive_menu()
