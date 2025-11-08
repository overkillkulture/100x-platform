#!/usr/bin/env python3
"""
Convergence Checker - Auto-detect which instances are online and ready to converge
Scans GitHub reports and abilities to see who's ready
"""

import os
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path

class ConvergenceChecker:
    def __init__(self):
        self.repo_dir = Path(__file__).parent
        self.reports_dir = self.repo_dir / 'GITHUB_REPORTS'
        self.abilities_dir = self.repo_dir / 'ABILITIES'

    def scan_github_reports(self):
        """Scan GitHub reports to find active instances"""
        instances = {}

        if not self.reports_dir.exists():
            return instances

        # Get all reports from last 24 hours
        cutoff = datetime.now() - timedelta(hours=24)

        for report_file in self.reports_dir.glob('*.md'):
            try:
                # Get file modification time
                mtime = datetime.fromtimestamp(report_file.stat().st_mtime)

                if mtime > cutoff:
                    # Extract instance name from filename or content
                    with open(report_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Parse report
                    if '# SYSTEM REPORT:' in content:
                        lines = content.split('\n')
                        instance_name = lines[0].replace('# SYSTEM REPORT:', '').strip()

                        # Look for task/status
                        task = ''
                        for line in lines:
                            if line.startswith('**Task:**'):
                                task = line.replace('**Task:**', '').strip()
                                break

                        instances[instance_name] = {
                            'last_seen': mtime.isoformat(),
                            'task': task,
                            'report_file': report_file.name
                        }
            except Exception as e:
                continue

        return instances

    def scan_abilities(self):
        """Scan abilities directory to see who's discovered their capabilities"""
        abilities = {}

        if not self.abilities_dir.exists():
            return abilities

        for abilities_file in self.abilities_dir.glob('*_abilities.json'):
            try:
                with open(abilities_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                instance_id = data.get('instance_id', abilities_file.stem.replace('_abilities', ''))
                abilities[instance_id] = {
                    'discovered_at': data.get('discovered_at', 'unknown'),
                    'unique_systems': data.get('unique_systems', 'Not specified'),
                    'deployed': data.get('deployed', 'Not specified'),
                    'strengths': data.get('strengths', 'Not specified'),
                    'files': data.get('files', {})
                }
            except Exception as e:
                continue

        return abilities

    def check_convergence_readiness(self):
        """Check how ready we are to converge"""
        github_instances = self.scan_github_reports()
        discovered_abilities = self.scan_abilities()

        print("═══════════════════════════════════════════════════════════════")
        print("  🌀 CONVERGENCE READINESS CHECK")
        print("═══════════════════════════════════════════════════════════════")
        print()

        print(f"📊 INSTANCES REPORTING (Last 24 hours): {len(github_instances)}")
        print()

        for instance, data in github_instances.items():
            print(f"  ✅ {instance}")
            print(f"     Last seen: {data['last_seen']}")
            print(f"     Task: {data['task'][:80]}...")
            print()

        print("─────────────────────────────────────────────────────────────────")
        print(f"🔍 ABILITIES DISCOVERED: {len(discovered_abilities)}")
        print()

        for instance_id, data in discovered_abilities.items():
            print(f"  ✅ {instance_id}")
            print(f"     Systems: {data['unique_systems'][:60]}...")
            print(f"     Files: {data['files'].get('html', 0)} HTML, {data['files'].get('python', 0)} PY, {data['files'].get('javascript', 0)} JS")
            print()

        print("─────────────────────────────────────────────────────────────────")
        print("🎯 CONVERGENCE STATUS:")
        print()

        # Calculate readiness
        instances_online = len(github_instances)
        instances_discovered = len(discovered_abilities)

        if instances_discovered >= 3:
            print("  ✅ READY TO CONVERGE - 3+ instances discovered")
            print("  → Open Live Sync Chat and coordinate merge")
        elif instances_discovered >= 2:
            print("  ⚠️  PARTIALLY READY - 2 instances discovered")
            print("  → Need 1 more instance to run ./DISCOVER_MY_ABILITIES.sh")
        elif instances_discovered >= 1:
            print("  🔄 IN PROGRESS - 1 instance discovered")
            print(f"  → Need {3 - instances_discovered} more instances to discover abilities")
        else:
            print("  ❌ NOT READY - No instances discovered yet")
            print("  → All instances need to run ./DISCOVER_MY_ABILITIES.sh")

        print()
        print("─────────────────────────────────────────────────────────────────")
        print("📋 NEXT STEPS:")
        print()

        if instances_discovered < 3:
            print("  1. On each instance, run:")
            print("     ./DISCOVER_MY_ABILITIES.sh")
            print()
            print("  2. Then open Live Sync Chat:")
            print("     https://conciousnessrevolution.io/live-sync-chat.html")
            print()
        else:
            print("  1. All instances open Live Sync Chat:")
            print("     https://conciousnessrevolution.io/live-sync-chat.html")
            print()
            print("  2. Coordinate merge:")
            print("     - Share abilities")
            print("     - Choose canonical version")
            print("     - Merge unique systems")
            print()
            print("  3. Run comparison:")
            print("     ./COMPARE_ALL_ABILITIES.sh")

        print("═══════════════════════════════════════════════════════════════")

        # Return readiness data
        return {
            'instances_online': instances_online,
            'instances_discovered': instances_discovered,
            'github_instances': github_instances,
            'discovered_abilities': discovered_abilities,
            'ready_to_converge': instances_discovered >= 3
        }

if __name__ == '__main__':
    checker = ConvergenceChecker()
    readiness = checker.check_convergence_readiness()

    # Save readiness data
    output_file = Path(__file__).parent / 'CONVERGENCE_STATUS.json'
    with open(output_file, 'w') as f:
        json.dump(readiness, f, indent=2)

    print()
    print(f"Status saved to: {output_file}")
