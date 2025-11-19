"""
ARAYA PERSISTENT MEMORY SYSTEM
Gives Araya long-term memory across sessions
Stores: conversations, user context, learned facts, builder progress

Created: October 26, 2025
Critical: Araya told beta tester "WE NEED persistent memory"
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
import os

# Memory database location
MEMORY_DB = r"C:\Users\dwrek\100X_DEPLOYMENT\ARAYA_MEMORY.db"
MEMORY_JSON = r"C:\Users\dwrek\100X_DEPLOYMENT\ARAYA_MEMORY.json"

class ArayaMemory:
    """Persistent memory system for Araya"""

    def __init__(self):
        self.db_path = MEMORY_DB
        self.json_path = MEMORY_JSON
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT NOT NULL,
                araya_response TEXT NOT NULL,
                context TEXT,
                tokens_used INTEGER DEFAULT 0,
                session_id TEXT
            )
        """)

        # User profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                classification TEXT,
                total_conversations INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0,
                builder_score INTEGER DEFAULT 0,
                first_seen DATETIME,
                last_seen DATETIME,
                preferences TEXT,
                notes TEXT
            )
        """)

        # Long-term facts table (things Araya learns)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact_type TEXT NOT NULL,
                content TEXT NOT NULL,
                source_user TEXT,
                learned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                importance INTEGER DEFAULT 5,
                verified BOOLEAN DEFAULT 0
            )
        """)

        # Session tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                message_count INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0
            )
        """)

        conn.commit()
        conn.close()

        print(f"✅ Memory database initialized at {self.db_path}")

    def save_conversation(self, user_id, user_message, araya_response,
                         context=None, tokens_used=0, session_id=None):
        """Save a conversation to memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversations
            (user_id, user_message, araya_response, context, tokens_used, session_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, user_message, araya_response, context, tokens_used, session_id))

        # Update user profile
        cursor.execute("""
            INSERT INTO user_profiles (user_id, total_conversations, total_tokens, last_seen, first_seen)
            VALUES (?, 1, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                total_conversations = total_conversations + 1,
                total_tokens = total_tokens + ?,
                last_seen = CURRENT_TIMESTAMP
        """, (user_id, tokens_used, tokens_used))

        conn.commit()
        conn.close()

        return True

    def get_conversation_history(self, user_id, limit=10):
        """Get recent conversations with a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_message, araya_response, timestamp, context
            FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))

        results = cursor.fetchall()
        conn.close()

        return [
            {
                'user_message': r[0],
                'araya_response': r[1],
                'timestamp': r[2],
                'context': r[3]
            }
            for r in results
        ]

    def get_user_context(self, user_id):
        """Get complete context about a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get profile
        cursor.execute("""
            SELECT name, classification, total_conversations, total_tokens,
                   builder_score, first_seen, last_seen, preferences, notes
            FROM user_profiles
            WHERE user_id = ?
        """, (user_id,))

        profile = cursor.fetchone()

        # Get recent conversations
        cursor.execute("""
            SELECT user_message, araya_response, timestamp
            FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 5
        """, (user_id,))

        recent_convos = cursor.fetchall()

        conn.close()

        if not profile:
            return None

        return {
            'user_id': user_id,
            'name': profile[0],
            'classification': profile[1],
            'total_conversations': profile[2],
            'total_tokens': profile[3],
            'builder_score': profile[4],
            'first_seen': profile[5],
            'last_seen': profile[6],
            'preferences': profile[7],
            'notes': profile[8],
            'recent_conversations': [
                {
                    'user': c[0],
                    'araya': c[1],
                    'timestamp': c[2]
                }
                for c in recent_convos
            ]
        }

    def learn_fact(self, fact_type, content, source_user=None, importance=5):
        """Store a learned fact for long-term memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO learned_facts (fact_type, content, source_user, importance)
            VALUES (?, ?, ?, ?)
        """, (fact_type, content, source_user, importance))

        conn.commit()
        conn.close()

        return True

    def recall_facts(self, fact_type=None, min_importance=0, limit=20):
        """Recall learned facts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if fact_type:
            cursor.execute("""
                SELECT fact_type, content, source_user, learned_at, importance
                FROM learned_facts
                WHERE fact_type = ? AND importance >= ?
                ORDER BY importance DESC, learned_at DESC
                LIMIT ?
            """, (fact_type, min_importance, limit))
        else:
            cursor.execute("""
                SELECT fact_type, content, source_user, learned_at, importance
                FROM learned_facts
                WHERE importance >= ?
                ORDER BY importance DESC, learned_at DESC
                LIMIT ?
            """, (min_importance, limit))

        results = cursor.fetchall()
        conn.close()

        return [
            {
                'type': r[0],
                'content': r[1],
                'source': r[2],
                'learned_at': r[3],
                'importance': r[4]
            }
            for r in results
        ]

    def get_memory_summary(self):
        """Get overview of Araya's memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total conversations
        cursor.execute("SELECT COUNT(*) FROM conversations")
        total_convos = cursor.fetchone()[0]

        # Total users
        cursor.execute("SELECT COUNT(*) FROM user_profiles")
        total_users = cursor.fetchone()[0]

        # Total facts learned
        cursor.execute("SELECT COUNT(*) FROM learned_facts")
        total_facts = cursor.fetchone()[0]

        # Most active users
        cursor.execute("""
            SELECT user_id, total_conversations
            FROM user_profiles
            ORDER BY total_conversations DESC
            LIMIT 5
        """)
        top_users = cursor.fetchall()

        conn.close()

        return {
            'total_conversations': total_convos,
            'total_users': total_users,
            'total_facts_learned': total_facts,
            'top_users': [
                {'user_id': u[0], 'conversations': u[1]}
                for u in top_users
            ]
        }

    def update_user_profile(self, user_id, **kwargs):
        """Update user profile fields"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build update query dynamically
        fields = []
        values = []

        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            values.append(value)

        if not fields:
            return False

        values.append(user_id)

        query = f"""
            UPDATE user_profiles
            SET {', '.join(fields)}
            WHERE user_id = ?
        """

        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return True

    def export_memory_json(self):
        """Export entire memory to JSON for backup"""
        conn = sqlite3.connect(self.db_path)

        # Get all data
        conversations = conn.execute("SELECT * FROM conversations").fetchall()
        users = conn.execute("SELECT * FROM user_profiles").fetchall()
        facts = conn.execute("SELECT * FROM learned_facts").fetchall()
        sessions = conn.execute("SELECT * FROM sessions").fetchall()

        conn.close()

        memory_export = {
            'export_date': datetime.now().isoformat(),
            'conversations': conversations,
            'users': users,
            'facts': facts,
            'sessions': sessions
        }

        with open(self.json_path, 'w') as f:
            json.dump(memory_export, f, indent=2)

        return self.json_path


# ============================================================================
# INTEGRATION WITH ARAYA V2
# ============================================================================

def enhance_araya_with_memory():
    """Add memory hooks to Araya V2"""

    print("""
    ============================================================================
    🧠 ARAYA PERSISTENT MEMORY UPGRADE
    ============================================================================

    Adding to ARAYA_UPGRADED_V2.py:

    1. Initialize memory on startup:
       memory = ArayaMemory()

    2. Save every conversation:
       memory.save_conversation(user_id, user_msg, araya_response, tokens=tokens)

    3. Load user context before responding:
       user_context = memory.get_user_context(user_id)
       # Include in prompt: "You previously talked to this user about..."

    4. Learn important facts:
       if "important" in message:
           memory.learn_fact("user_preference", message, user_id)

    5. Recall facts when relevant:
       facts = memory.recall_facts(fact_type="platform_feature")
       # Include in context

    ============================================================================

    Benefits:
    ✅ Araya remembers conversations across sessions
    ✅ Builds understanding of each user over time
    ✅ Learns platform knowledge progressively
    ✅ Provides personalized responses
    ✅ Never forgets important context

    ============================================================================
    """)


if __name__ == "__main__":
    print("🧠 ARAYA PERSISTENT MEMORY SYSTEM")
    print("="*60)

    # Initialize memory
    memory = ArayaMemory()

    # Test save conversation
    print("\n📝 Testing conversation save...")
    memory.save_conversation(
        user_id="test_user_1",
        user_message="How do I become a Builder?",
        araya_response="Focus on consciousness elevation and creating value...",
        context="First conversation about Builder path",
        tokens_used=150,
        session_id="test_session_1"
    )
    print("✅ Conversation saved")

    # Test recall
    print("\n🔍 Testing conversation recall...")
    history = memory.get_conversation_history("test_user_1")
    print(f"✅ Found {len(history)} conversations")

    # Test learn fact
    print("\n🧠 Testing fact learning...")
    memory.learn_fact(
        fact_type="platform_feature",
        content="Bug reporter button is on every page in bottom-right corner",
        source_user="commander",
        importance=8
    )
    print("✅ Fact learned")

    # Test recall facts
    print("\n💭 Testing fact recall...")
    facts = memory.recall_facts(fact_type="platform_feature")
    print(f"✅ Recalled {len(facts)} facts")

    # Get memory summary
    print("\n📊 Memory Summary:")
    summary = memory.get_memory_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")

    print("\n✅ PERSISTENT MEMORY SYSTEM OPERATIONAL!")
    print(f"   Database: {MEMORY_DB}")
    print(f"   Export: {MEMORY_JSON}")

    enhance_araya_with_memory()
