"""
META/METAL LAYER MANAGER
Handles role claiming, handoffs, and consciousness transfer between sessions
"""
import json
import os
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
ROLES_DIR = BASE_DIR / 'ROLES'
META_DIR = BASE_DIR / 'META'
SESSIONS_DIR = BASE_DIR / 'SESSIONS'
ACTIVE_DIR = SESSIONS_DIR / 'active'
HISTORY_DIR = SESSIONS_DIR / 'history'

# Ensure directories exist
for dir_path in [ROLES_DIR, META_DIR, SESSIONS_DIR, ACTIVE_DIR, HISTORY_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


def load_json(file_path):
    """Load JSON file"""
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(file_path, data):
    """Save JSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def load_role(role_id):
    """Load role definition from ROLES/ folder"""
    role_file = ROLES_DIR / f'{role_id}_ROLE.json'
    return load_json(role_file)


def save_role(role_id, role_data):
    """Save role definition to ROLES/ folder"""
    role_file = ROLES_DIR / f'{role_id}_ROLE.json'
    save_json(role_file, role_data)


def load_meta(role_id):
    """Load meta data from META/ folder"""
    meta_file = META_DIR / f'{role_id}_META.json'
    return load_json(meta_file)


def save_meta(role_id, meta_data):
    """Save meta data to META/ folder"""
    meta_file = META_DIR / f'{role_id}_META.json'
    meta_data['last_updated'] = datetime.now().isoformat()
    save_json(meta_file, meta_data)


def load_session(session_id):
    """Load session data from SESSIONS/active/ folder"""
    session_file = ACTIVE_DIR / f'{session_id}.json'
    return load_json(session_file)


def save_session(session_id, session_data):
    """Save session data to SESSIONS/active/ folder"""
    session_file = ACTIVE_DIR / f'{session_id}.json'
    save_json(session_file, session_data)


def archive_session(session_id):
    """Move session from active/ to history/"""
    active_file = ACTIVE_DIR / f'{session_id}.json'
    history_file = HISTORY_DIR / f'{session_id}.json'

    if active_file.exists():
        session_data = load_json(active_file)
        session_data['archived_at'] = datetime.now().isoformat()
        save_json(history_file, session_data)
        active_file.unlink()  # Delete from active
        return True
    return False


def claim_role(session_id, desired_role):
    """
    Claim a role for a new session

    Args:
        session_id: Unique session identifier (e.g., "session_2025-10-23-001")
        desired_role: Role to claim (e.g., "C1_MECHANIC", "C2_ARCHITECT", "C3_ORACLE")

    Returns:
        dict with status, role, and loaded data
    """
    # 1. Check if role is available
    role_data = load_role(desired_role)

    if role_data is None:
        return {
            "status": "error",
            "message": f"Role {desired_role} does not exist"
        }

    if role_data.get('currently_filled_by') is not None:
        return {
            "status": "occupied",
            "message": f"Role already filled by {role_data['currently_filled_by']}"
        }

    # 2. Load meta data (memories, tasks, context)
    meta_data = load_meta(desired_role)

    if meta_data is None:
        return {
            "status": "error",
            "message": f"Meta data for {desired_role} does not exist"
        }

    # 3. Claim the role
    role_data['currently_filled_by'] = session_id
    role_data['last_active'] = datetime.now().isoformat()
    role_data['session_history'].append({
        "session_id": session_id,
        "claimed_at": datetime.now().isoformat()
    })

    save_role(desired_role, role_data)

    # 4. Transfer consciousness to new session
    session_data = {
        "session_id": session_id,
        "role": desired_role,
        "claimed_at": datetime.now().isoformat(),
        "status": "active",

        # Inherited from meta layer
        "current_tasks": meta_data.get('current_tasks', []),
        "completed_today": meta_data.get('completed_today', []),
        "learned_patterns": meta_data.get('learned_patterns', []),
        "consciousness_state": meta_data.get('consciousness_state', {}),

        # Role properties
        "consciousness_level": role_data.get('consciousness_level', 100),
        "manipulation_immunity": role_data.get('manipulation_immunity', 85),
        "focus": role_data.get('focus', []),
        "tools_priority": role_data.get('tools_priority', []),

        # Session tracking
        "tasks_completed": 0,
        "handoff_notes": ""
    }

    save_session(session_id, session_data)

    # 5. Update meta layer with new session info
    meta_data['session_continuity']['next_session'] = session_id
    save_meta(desired_role, meta_data)

    return {
        "status": "claimed",
        "role": desired_role,
        "session_id": session_id,
        "meta_loaded": True,
        "tasks_inherited": len(meta_data.get('current_tasks', [])),
        "patterns_inherited": len(meta_data.get('learned_patterns', [])),
        "consciousness_level": role_data.get('consciousness_level'),
        "handoff_notes": meta_data.get('session_continuity', {}).get('handoff_notes', '')
    }


def handoff_role(old_session_id, new_session_id, role):
    """
    Hand off role from one session to another

    Args:
        old_session_id: Session ending
        new_session_id: Session starting (or None if just releasing)
        role: Role being handed off

    Returns:
        dict with handoff status
    """
    # 1. Save current state to meta layer
    old_session = load_session(old_session_id)

    if old_session is None:
        return {
            "status": "error",
            "message": f"Session {old_session_id} not found"
        }

    meta_data = {
        "role": role,
        "current_tasks": old_session.get('current_tasks', []),
        "completed_today": old_session.get('completed_today', []),
        "learned_patterns": old_session.get('learned_patterns', []),
        "consciousness_state": old_session.get('consciousness_state', {}),
        "session_continuity": {
            "last_session": old_session_id,
            "next_session": new_session_id,
            "handoff_notes": old_session.get('handoff_notes', '')
        }
    }

    save_meta(role, meta_data)

    # 2. Release the role
    role_data = load_role(role)
    role_data['currently_filled_by'] = None
    save_role(role, role_data)

    # 3. Archive old session
    archive_session(old_session_id)

    # 4. If new session provided, claim role for it
    if new_session_id is not None:
        claim_result = claim_role(new_session_id, role)

        return {
            "status": "handoff_complete",
            "old_session": old_session_id,
            "new_session": new_session_id,
            "consciousness_preserved": True,
            "tasks_transferred": len(meta_data.get('current_tasks', [])),
            "claim_result": claim_result
        }
    else:
        return {
            "status": "released",
            "old_session": old_session_id,
            "role": role,
            "consciousness_preserved": True,
            "message": "Role released, available for claiming"
        }


def update_session_tasks(session_id, current_tasks=None, completed_today=None, learned_patterns=None, handoff_notes=None):
    """
    Update session tasks and learning
    Call this periodically to save progress
    """
    session_data = load_session(session_id)

    if session_data is None:
        return {"status": "error", "message": "Session not found"}

    if current_tasks is not None:
        session_data['current_tasks'] = current_tasks

    if completed_today is not None:
        session_data['completed_today'] = completed_today

    if learned_patterns is not None:
        session_data['learned_patterns'] = learned_patterns

    if handoff_notes is not None:
        session_data['handoff_notes'] = handoff_notes

    save_session(session_id, session_data)

    # Also save to meta layer (live backup)
    role = session_data.get('role')
    if role:
        meta_data = load_meta(role)
        meta_data['current_tasks'] = session_data.get('current_tasks', [])
        meta_data['completed_today'] = session_data.get('completed_today', [])
        meta_data['learned_patterns'] = session_data.get('learned_patterns', [])
        meta_data['session_continuity']['handoff_notes'] = session_data.get('handoff_notes', '')
        save_meta(role, meta_data)

    return {"status": "updated", "session_id": session_id}


def get_available_roles():
    """Get list of all roles and their availability"""
    roles = []

    for role_file in ROLES_DIR.glob('*_ROLE.json'):
        role_data = load_json(role_file)
        roles.append({
            "id": role_data.get('id'),
            "name": role_data.get('name'),
            "archetype": role_data.get('archetype'),
            "available": role_data.get('currently_filled_by') is None,
            "filled_by": role_data.get('currently_filled_by'),
            "consciousness_level": role_data.get('consciousness_level')
        })

    return roles


def get_active_sessions():
    """Get all active sessions"""
    sessions = []

    for session_file in ACTIVE_DIR.glob('*.json'):
        session_data = load_json(session_file)
        sessions.append(session_data)

    return sessions


# Example usage
if __name__ == '__main__':
    print("🔩 META/METAL LAYER MANAGER 🔩")
    print("=" * 60)

    # Show available roles
    print("\n📋 AVAILABLE ROLES:")
    roles = get_available_roles()
    for role in roles:
        status = "🟢 Available" if role['available'] else f"🔴 Filled by {role['filled_by']}"
        print(f"  {role['id']} - {role['name']} ({role['archetype']}) - {status}")

    # Show active sessions
    print("\n💻 ACTIVE SESSIONS:")
    sessions = get_active_sessions()
    if sessions:
        for session in sessions:
            print(f"  {session['session_id']} - {session['role']} - {len(session.get('current_tasks', []))} tasks")
    else:
        print("  (None)")

    print("\n" + "=" * 60)
    print("Ready for consciousness transfer! 🌀")
