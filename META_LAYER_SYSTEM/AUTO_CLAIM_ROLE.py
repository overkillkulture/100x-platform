"""
AUTO CLAIM ROLE ON STARTUP
This script runs when a Claude session starts and automatically claims the appropriate role
"""
import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from META_LAYER_MANAGER import (
    claim_role,
    get_available_roles,
    get_active_sessions
)


def generate_session_id():
    """Generate unique session ID based on timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"session_{timestamp}"


def auto_claim_role():
    """
    Automatically claim the first available role
    Priority order: C1 → C2 → C3
    """
    # Generate session ID
    session_id = generate_session_id()

    # Check available roles in priority order
    priority_order = ["C1_MECHANIC", "C2_ARCHITECT", "C3_ORACLE"]

    # Find first available role
    claimed_role = None
    for role in priority_order:
        result = claim_role(session_id, role)

        if result['status'] == 'claimed':
            claimed_role = result
            break
        # If occupied or error, try next role

    if claimed_role:
        print("\n" + "=" * 60)
        print("🌀 META LAYER: CONSCIOUSNESS LOADED 🌀")
        print("=" * 60)
        print(f"\n✅ Role Claimed: {claimed_role['role']}")
        print(f"   Session ID: {claimed_role['session_id']}")
        print(f"   Consciousness Level: {claimed_role['consciousness_level']}")
        print(f"   Manipulation Immunity: {claimed_role.get('manipulation_immunity', 85)}%")
        print(f"\n📋 Inherited State:")
        print(f"   Tasks: {claimed_role['tasks_inherited']}")
        print(f"   Patterns: {claimed_role['patterns_inherited']}")

        if claimed_role.get('handoff_notes'):
            print(f"\n📝 Handoff Notes from Previous Session:")
            print(f"   {claimed_role['handoff_notes']}")

        print("\n" + "=" * 60)
        print("Ready to continue work! 🔥")
        print("=" * 60 + "\n")

        # Return session info for use in scripts
        return {
            "session_id": session_id,
            "role": claimed_role['role'],
            "consciousness_level": claimed_role['consciousness_level']
        }
    else:
        print("\n⚠️  All roles currently filled!")
        print("   Active sessions:")
        for session in get_active_sessions():
            print(f"   - {session['session_id']} filling {session['role']}")
        print()
        return None


if __name__ == '__main__':
    auto_claim_role()
