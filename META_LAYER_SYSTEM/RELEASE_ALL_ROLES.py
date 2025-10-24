"""
Release all active roles (cleanup utility)
"""
from META_LAYER_MANAGER import get_active_sessions, handoff_role

sessions = get_active_sessions()

for session in sessions:
    session_id = session['session_id']
    role = session['role']
    print(f"Releasing {session_id} from {role}...")
    handoff_role(session_id, None, role)

print("\n✅ All roles released!")
