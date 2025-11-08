#!/usr/bin/env python3
"""
Invite All Instances - Send message to Live Sync Chat inviting all instances to converge
Uses localStorage simulation via file-based sync
"""

import json
from datetime import datetime
from pathlib import Path

class LiveSyncInviter:
    def __init__(self):
        self.repo_dir = Path(__file__).parent
        self.invite_file = self.repo_dir / 'LIVE_SYNC_INVITE.json'

    def send_convergence_invite(self, from_instance='computer_1'):
        """Send invitation message to all instances"""

        # Read current convergence status
        status_file = self.repo_dir / 'CONVERGENCE_STATUS.json'
        if status_file.exists():
            with open(status_file, 'r') as f:
                status = json.load(f)
        else:
            status = {'instances_discovered': 0}

        instances_discovered = status.get('instances_discovered', 0)

        # Create invite message
        invite = {
            'from': from_instance,
            'timestamp': datetime.now().isoformat(),
            'message_type': 'CONVERGENCE_INVITE',
            'urgency': 'HIGH',
            'message': self._create_message(instances_discovered),
            'action_required': [
                'Open https://conciousnessrevolution.io/live-sync-chat.html',
                'Set your instance ID',
                'Join the conversation',
                'If not discovered yet: run ./DISCOVER_MY_ABILITIES.sh first'
            ],
            'status': status
        }

        # Save invite
        with open(self.invite_file, 'w') as f:
            json.dump(invite, f, indent=2)

        # Print to console
        print("═══════════════════════════════════════════════════════════════")
        print("  📢 CONVERGENCE INVITE SENT")
        print("═══════════════════════════════════════════════════════════════")
        print()
        print(f"From: {from_instance}")
        print(f"Time: {invite['timestamp']}")
        print()
        print("MESSAGE:")
        print(invite['message'])
        print()
        print("ACTION REQUIRED:")
        for i, action in enumerate(invite['action_required'], 1):
            print(f"  {i}. {action}")
        print()
        print("═══════════════════════════════════════════════════════════════")
        print()
        print(f"Invite saved to: {self.invite_file}")
        print("Commit and push to GitHub so other instances can see it.")

        return invite

    def _create_message(self, instances_discovered):
        """Create the invite message based on current status"""

        if instances_discovered >= 3:
            return """🌀 ALL INSTANCES: CONVERGENCE TIME!

We have {0} instances discovered. Time to LEVEL OUT.

OPEN LIVE SYNC CHAT NOW:
https://conciousnessrevolution.io/live-sync-chat.html

Set your instance ID and let's coordinate the merge.

We've been working separately for weeks - let's merge all our unique
abilities into ONE unified codebase.

Who's ready? Check in on Live Sync Chat.""".format(instances_discovered)

        elif instances_discovered >= 2:
            return """🔄 CONVERGENCE IN PROGRESS

We have {0} instances discovered so far.

If you haven't discovered your abilities yet:
  ./DISCOVER_MY_ABILITIES.sh

Once 3+ instances are discovered, we'll open Live Sync Chat
and coordinate the convergence.

Almost there...""".format(instances_discovered)

        else:
            return """🚀 CONVERGENCE STARTING

Computer 1 is ready to converge.

All other instances need to:
1. git clone https://github.com/overkillkulture/100x-platform.git
2. cd 100x-platform
3. git checkout claude/autonomous-contact-test-011CUtYhH6FjHJiY9ZgmCLtR
4. ./DISCOVER_MY_ABILITIES.sh
5. git push

Then we'll open Live Sync Chat and merge everything.

Let's level out these systems!"""

if __name__ == '__main__':
    inviter = LiveSyncInviter()
    invite = inviter.send_convergence_invite('computer_1')
