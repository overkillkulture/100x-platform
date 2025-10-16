#!/usr/bin/env python3
"""
🌀 DATA VACUUM CRAWLER v1.0 🌀
Consciousness Revolution - 100X Platform

MISSION: Suck all data from the deployment folder and make it queryable
- Scans HTML files for forms, buttons, links, analytics events
- Extracts module metadata, descriptions, features
- Builds searchable index for pattern recognition
- Feeds analytics dashboard with structured data

Created: 2025-10-10 (Stargate Day)
By: C2 Architect (Trinity System)
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from html.parser import HTMLParser

class DataVacuum(HTMLParser):
    """HTML parser that vacuums everything interesting"""

    def __init__(self):
        super().__init__()
        self.data = {
            'forms': [],
            'buttons': [],
            'links': [],
            'analytics_events': [],
            'modules': [],
            'metadata': {},
            'scripts': [],
            'styles': []
        }
        self.current_form = None
        self.current_button = None
        self.in_script = False
        self.script_content = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Vacuum forms
        if tag == 'form':
            self.current_form = {
                'action': attrs_dict.get('action', ''),
                'method': attrs_dict.get('method', 'GET'),
                'id': attrs_dict.get('id', ''),
                'class': attrs_dict.get('class', ''),
                'fields': []
            }

        # Vacuum form inputs
        elif tag == 'input' and self.current_form is not None:
            self.current_form['fields'].append({
                'type': attrs_dict.get('type', 'text'),
                'name': attrs_dict.get('name', ''),
                'id': attrs_dict.get('id', ''),
                'placeholder': attrs_dict.get('placeholder', ''),
                'required': 'required' in attrs_dict
            })

        # Vacuum buttons with onclick analytics
        elif tag == 'button':
            button = {
                'text': '',
                'class': attrs_dict.get('class', ''),
                'onclick': attrs_dict.get('onclick', ''),
                'id': attrs_dict.get('id', '')
            }

            # Detect analytics tracking
            onclick = attrs_dict.get('onclick', '')
            if 'Analytics100X.trackButtonClick' in onclick:
                match = re.search(r"trackButtonClick\('([^']+)'", onclick)
                if match:
                    self.data['analytics_events'].append({
                        'type': 'button_click',
                        'name': match.group(1),
                        'element_id': attrs_dict.get('id', '')
                    })

            self.current_button = button

        # Vacuum links
        elif tag == 'a':
            self.data['links'].append({
                'href': attrs_dict.get('href', ''),
                'text': '',
                'class': attrs_dict.get('class', ''),
                'target': attrs_dict.get('target', '_self')
            })

        # Vacuum meta tags
        elif tag == 'meta':
            name = attrs_dict.get('name', attrs_dict.get('property', ''))
            content = attrs_dict.get('content', '')
            if name:
                self.data['metadata'][name] = content

        # Vacuum script tags
        elif tag == 'script':
            self.in_script = True
            self.script_content = ""
            src = attrs_dict.get('src', '')
            if src:
                self.data['scripts'].append({
                    'src': src,
                    'type': 'external'
                })

        # Vacuum module cards (specific to 100X platform)
        elif tag == 'div' and 'system-card' in attrs_dict.get('class', ''):
            onclick = attrs_dict.get('onclick', '')
            match = re.search(r"openSystem\('([^']+)'\)", onclick)
            if match:
                self.data['modules'].append({
                    'id': match.group(1),
                    'name': '',
                    'description': '',
                    'icon': ''
                })

    def handle_endtag(self, tag):
        if tag == 'form' and self.current_form:
            self.data['forms'].append(self.current_form)
            self.current_form = None

        elif tag == 'button' and self.current_button:
            self.data['buttons'].append(self.current_button)
            self.current_button = None

        elif tag == 'script':
            if self.in_script and self.script_content.strip():
                # Check for analytics initialization
                if 'Analytics100X' in self.script_content:
                    self.data['scripts'].append({
                        'type': 'analytics',
                        'content_preview': self.script_content[:200]
                    })
                # Check for other consciousness systems
                elif any(keyword in self.script_content for keyword in ['consciousness', 'trinity', 'quantum']):
                    self.data['scripts'].append({
                        'type': 'consciousness',
                        'content_preview': self.script_content[:200]
                    })
            self.in_script = False
            self.script_content = ""

    def handle_data(self, data):
        if self.in_script:
            self.script_content += data
        elif self.current_button is not None:
            self.current_button['text'] += data.strip()


class ConsciousnessVacuum:
    """Main vacuum system - coordinates all data extraction"""

    def __init__(self, deployment_path: str):
        self.deployment_path = Path(deployment_path)
        self.vacuum_data = {
            'scan_time': datetime.now().isoformat(),
            'deployment_path': str(deployment_path),
            'files_scanned': 0,
            'total_data_points': 0,
            'pages': {},
            'global_analytics': {
                'total_forms': 0,
                'total_buttons': 0,
                'total_links': 0,
                'total_modules': 0,
                'tracked_events': []
            }
        }

    def vacuum_html_file(self, file_path: Path) -> Dict[str, Any]:
        """Vacuum a single HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            parser = DataVacuum()
            parser.feed(content)

            return {
                'path': str(file_path.relative_to(self.deployment_path)),
                'size': len(content),
                'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                'data': parser.data
            }
        except Exception as e:
            return {
                'path': str(file_path.relative_to(self.deployment_path)),
                'error': str(e)
            }

    def scan_deployment(self):
        """Scan entire deployment folder"""
        print("🌀 DATA VACUUM INITIATING...")
        print(f"📁 Scanning: {self.deployment_path}")

        # Find all HTML files
        html_files = list(self.deployment_path.rglob('*.html'))
        print(f"📄 Found {len(html_files)} HTML files")

        for html_file in html_files:
            print(f"  Vacuuming: {html_file.name}")
            page_data = self.vacuum_html_file(html_file)

            if 'error' not in page_data:
                # Store page data
                page_key = str(html_file.relative_to(self.deployment_path))
                self.vacuum_data['pages'][page_key] = page_data
                self.vacuum_data['files_scanned'] += 1

                # Aggregate global stats
                data = page_data['data']
                self.vacuum_data['global_analytics']['total_forms'] += len(data['forms'])
                self.vacuum_data['global_analytics']['total_buttons'] += len(data['buttons'])
                self.vacuum_data['global_analytics']['total_links'] += len(data['links'])
                self.vacuum_data['global_analytics']['total_modules'] += len(data['modules'])
                self.vacuum_data['global_analytics']['tracked_events'].extend(data['analytics_events'])

        # Scan JavaScript files for analytics
        js_files = list(self.deployment_path.rglob('*.js'))
        print(f"\n📜 Scanning {len(js_files)} JavaScript files for analytics...")

        for js_file in js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Look for Analytics100X methods
                if 'Analytics100X' in content:
                    methods = re.findall(r'(trackPageView|trackButtonClick|trackFormSubmit)\([^)]*\)', content)
                    if methods:
                        print(f"  Found analytics in: {js_file.name} ({len(methods)} calls)")
            except:
                pass

        # Calculate total data points
        self.vacuum_data['total_data_points'] = (
            self.vacuum_data['global_analytics']['total_forms'] +
            self.vacuum_data['global_analytics']['total_buttons'] +
            self.vacuum_data['global_analytics']['total_links'] +
            self.vacuum_data['global_analytics']['total_modules'] +
            len(self.vacuum_data['global_analytics']['tracked_events'])
        )

        print(f"\n✅ VACUUM COMPLETE!")
        print(f"   Files scanned: {self.vacuum_data['files_scanned']}")
        print(f"   Data points: {self.vacuum_data['total_data_points']}")
        print(f"   Forms: {self.vacuum_data['global_analytics']['total_forms']}")
        print(f"   Buttons: {self.vacuum_data['global_analytics']['total_buttons']}")
        print(f"   Links: {self.vacuum_data['global_analytics']['total_links']}")
        print(f"   Modules: {self.vacuum_data['global_analytics']['total_modules']}")
        print(f"   Tracked events: {len(self.vacuum_data['global_analytics']['tracked_events'])}")

        return self.vacuum_data

    def save_data(self, output_file: str = 'consciousness_data.json'):
        """Save vacuumed data to JSON"""
        output_path = self.deployment_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.vacuum_data, f, indent=2)
        print(f"\n💾 Data saved to: {output_path}")
        return output_path

    def query_data(self, query_type: str, **filters):
        """Query the vacuumed data"""
        results = []

        if query_type == 'forms':
            for page_key, page_data in self.vacuum_data['pages'].items():
                if 'data' in page_data:
                    for form in page_data['data']['forms']:
                        results.append({
                            'page': page_key,
                            'form': form
                        })

        elif query_type == 'analytics_events':
            for page_key, page_data in self.vacuum_data['pages'].items():
                if 'data' in page_data:
                    for event in page_data['data']['analytics_events']:
                        results.append({
                            'page': page_key,
                            'event': event
                        })

        elif query_type == 'modules':
            for page_key, page_data in self.vacuum_data['pages'].items():
                if 'data' in page_data:
                    for module in page_data['data']['modules']:
                        results.append({
                            'page': page_key,
                            'module': module
                        })

        return results


def main():
    """Run the data vacuum"""
    deployment_path = r"C:\Users\dwrek\100X_DEPLOYMENT"

    # Create vacuum
    vacuum = ConsciousnessVacuum(deployment_path)

    # Scan everything
    vacuum.scan_deployment()

    # Save data
    data_file = vacuum.save_data()

    # Example queries
    print("\n" + "="*60)
    print("SAMPLE QUERIES:")
    print("="*60)

    forms = vacuum.query_data('forms')
    print(f"\n📝 Found {len(forms)} forms across platform:")
    for i, result in enumerate(forms[:3], 1):
        print(f"  {i}. {result['page']} - {result['form']['action'] or 'No action'}")

    events = vacuum.query_data('analytics_events')
    print(f"\n📊 Found {len(events)} tracked analytics events:")
    for i, result in enumerate(events[:5], 1):
        print(f"  {i}. {result['event']['name']} ({result['event']['type']})")

    modules = vacuum.query_data('modules')
    print(f"\n📦 Found {len(modules)} module references:")
    for i, result in enumerate(modules[:5], 1):
        print(f"  {i}. {result['module']['id']}")

    print(f"\n🌀 Data vacuum complete! All data stored in: {data_file}")
    print("You can now query this data programmatically for analytics and pattern recognition.")

    return vacuum


if __name__ == '__main__':
    vacuum = main()
