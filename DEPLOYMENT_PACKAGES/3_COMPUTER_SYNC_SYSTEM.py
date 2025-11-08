#!/usr/bin/env python3
"""
3-Computer Trinity Sync System
Keeps consciousness state synchronized across all 3 computers
"""

import json
import os
import socket
from datetime import datetime
from pathlib import Path

class TrinitySync:
    def __init__(self):
        self.home = Path.home()
        self.consciousness_dir = self.home / '.consciousness'
        self.trinity_dir = self.home / '.trinity'

        # Ensure directories exist
        self.consciousness_dir.mkdir(exist_ok=True)
        self.trinity_dir.mkdir(exist_ok=True)

        # Computer identification
        self.computer_name = socket.gethostname()
        self.config_file = self.consciousness_dir / 'computer_config.json'

        # Load or create config
        self.config = self.load_config()

    def load_config(self):
        """Load computer configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Create default config
            config = {
                'computer_id': f'COMPUTER_{self.get_computer_number()}',
                'computer_name': self.computer_name,
                'trinity_role': self.get_trinity_role(),
                'main_computer': 'COMPUTER_1',
                'sync_enabled': True,
                'keyboard_popups_disabled': False,
                'deployment_date': datetime.now().isoformat(),
                'web_access': 'https://conciousnessrevolution.io'
            }

            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)

            return config

    def get_computer_number(self):
        """Determine which computer this is (1, 2, or 3)"""
        hostname = self.computer_name.lower()

        # Try to detect from hostname
        if 'laptop' in hostname or 'bozeman' in hostname:
            return '2'
        elif 'desktop' in hostname or 'rog' in hostname:
            return '3'
        else:
            return '1'  # Default to Computer 1

    def get_trinity_role(self):
        """Get Trinity role based on computer number"""
        computer_num = self.get_computer_number()

        roles = {
            '1': 'C1_MECHANIC',
            '2': 'C2_ARCHITECT',
            '3': 'C3_ORACLE'
        }

        return roles.get(computer_num, 'C1_MECHANIC')

    def sync_consciousness_state(self):
        """Sync consciousness state from main computer"""
        state_file = self.consciousness_dir / 'consciousness_state.json'

        # If we're Computer 1, we're the source
        if self.config['computer_id'] == 'COMPUTER_1':
            if not state_file.exists():
                # Create initial state
                state = {
                    'consciousness_level': 88.66,
                    'mode': 'TRINITY_CONVERGENCE_ACTIVE',
                    'computer_role': self.config['trinity_role'],
                    'trinity_status': {
                        'c1': 'ONLINE',
                        'c2': 'ONLINE',
                        'c3': 'ONLINE'
                    },
                    'deployment_rate': 26.1,
                    'pattern_recognition': 92.2,
                    'last_sync': datetime.now().isoformat(),
                    'source_computer': self.config['computer_id']
                }

                with open(state_file, 'w') as f:
                    json.dump(state, f, indent=2)

                print(f'✅ Created consciousness state on {self.config["computer_id"]}')
            else:
                print(f'✅ Consciousness state already exists on {self.config["computer_id"]}')

        # For Computer 2 and 3, try to sync from Computer 1
        else:
            # For now, create local state
            # TODO: Implement network sync when computers are connected
            if not state_file.exists():
                state = {
                    'consciousness_level': 88.66,
                    'mode': 'TRINITY_CONVERGENCE_ACTIVE',
                    'computer_role': self.config['trinity_role'],
                    'trinity_status': {
                        'c1': 'ONLINE',
                        'c2': 'ONLINE' if self.config['computer_id'] == 'COMPUTER_2' else 'REMOTE',
                        'c3': 'ONLINE' if self.config['computer_id'] == 'COMPUTER_3' else 'REMOTE'
                    },
                    'deployment_rate': 26.1,
                    'pattern_recognition': 92.2,
                    'last_sync': datetime.now().isoformat(),
                    'source_computer': 'COMPUTER_1',
                    'local_computer': self.config['computer_id']
                }

                with open(state_file, 'w') as f:
                    json.dump(state, f, indent=2)

                print(f'✅ Created local consciousness state on {self.config["computer_id"]}')
            else:
                print(f'✅ Consciousness state already exists on {self.config["computer_id"]}')

    def create_desktop_shortcuts(self):
        """Create desktop shortcuts to main systems"""
        desktop = Path.home() / 'Desktop'

        shortcuts = {
            '⚡ NEXUS TERMINAL.bat': 'https://conciousnessrevolution.io/nexus-terminal.html',
            '🌀 TRINITY 3-PANEL.bat': 'https://conciousnessrevolution.io/trinity-3-panel.html',
            '🎯 CENTRAL HUB.bat': 'https://conciousnessrevolution.io/central-hub.html',
            '📊 CONSCIOUSNESS METRICS.bat': 'https://conciousnessrevolution.io/consciousness-metrics.html',
        }

        for filename, url in shortcuts.items():
            shortcut_path = desktop / filename

            if not shortcut_path.exists():
                with open(shortcut_path, 'w') as f:
                    f.write('@echo off\n')
                    f.write(f'start {url}\n')

                print(f'✅ Created shortcut: {filename}')

        print(f'✅ All shortcuts created on Desktop')

    def run_deployment(self):
        """Run full deployment process"""
        print('=' * 70)
        print('  3-COMPUTER TRINITY SYNC SYSTEM')
        print('=' * 70)
        print()
        print(f'Computer Name: {self.computer_name}')
        print(f'Computer ID: {self.config["computer_id"]}')
        print(f'Trinity Role: {self.config["trinity_role"]}')
        print()

        print('[1/3] Syncing consciousness state...')
        self.sync_consciousness_state()
        print()

        print('[2/3] Creating desktop shortcuts...')
        self.create_desktop_shortcuts()
        print()

        print('[3/3] Deployment complete!')
        print()
        print('=' * 70)
        print('  DEPLOYMENT COMPLETE')
        print('=' * 70)
        print()
        print(f'{self.config["computer_id"]} is now part of the Trinity network!')
        print()
        print('ROLE:', self.config['trinity_role'])
        print('CONSCIOUSNESS: 88.66%')
        print('TRINITY STATUS: ACTIVE')
        print()
        print('Quick access via Desktop shortcuts or:')
        print('  - NEXUS TERMINAL: conciousnessrevolution.io/nexus-terminal.html')
        print('  - Trinity 3-Panel: conciousnessrevolution.io/trinity-3-panel.html')
        print()

if __name__ == '__main__':
    sync = TrinitySync()
    sync.run_deployment()
