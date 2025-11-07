#!/usr/bin/env python3
"""
MULTI_AI_IMPORTER.py
Import AI conversation data from ChatGPT, Claude, and other platforms

Created: November 4, 2025 (Autonomous Build)
Usage: python MULTI_AI_IMPORTER.py
"""

import os
import json
import psycopg2
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import sys

class MultiAIImporter:
    """Import conversations from multiple AI platforms"""

    def __init__(self, db_url: str = None):
        """Initialize importer with database connection"""
        self.db_url = db_url or os.getenv('DATABASE_URL')
        if not self.db_url:
            raise ValueError("DATABASE_URL not set. Check .env.multi_ai file")

        self.conn = psycopg2.connect(self.db_url)
        self.cursor = self.conn.cursor()

        # Export paths
        self.export_base = Path(r"C:\Users\dwrek\.ai_exports")
        self.chatgpt_path = self.export_base / "chatgpt"
        self.claude_path = self.export_base / "claude"

        print(f"✅ Connected to database: {self.db_url[:30]}...")

    def import_chatgpt(self, conversations_file: Path = None):
        """Import ChatGPT conversations.json file"""
        print("\n" + "=" * 80)
        print("📥 IMPORTING CHATGPT DATA")
        print("=" * 80)

        if not conversations_file:
            # Find conversations.json in chatgpt export folder
            json_files = list(self.chatgpt_path.glob("**/conversations.json"))
            if not json_files:
                print("❌ No conversations.json found in chatgpt export folder")
                print(f"   Looking in: {self.chatgpt_path}")
                return 0
            conversations_file = json_files[0]

        print(f"📂 Reading: {conversations_file}")

        with open(conversations_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        conversation_count = 0
        message_count = 0

        for conversation in data:
            try:
                # Insert conversation
                conv_id = self._insert_conversation(
                    platform='chatgpt',
                    conversation_id=conversation.get('id'),
                    title=conversation.get('title', 'Untitled'),
                    created_at=datetime.fromtimestamp(conversation.get('create_time', 0)),
                    updated_at=datetime.fromtimestamp(conversation.get('update_time', 0)),
                    metadata=conversation
                )

                conversation_count += 1

                # Insert messages
                mapping = conversation.get('mapping', {})
                for node_id, node in mapping.items():
                    message = node.get('message')
                    if message and message.get('content'):
                        content_parts = message['content'].get('parts', [])
                        if content_parts:
                            content = '\n'.join(str(part) for part in content_parts)

                            self._insert_message(
                                conversation_id=conv_id,
                                role=message['author']['role'],
                                content=content,
                                timestamp=datetime.fromtimestamp(message.get('create_time', 0)),
                                model=message.get('metadata', {}).get('model_slug'),
                                metadata=message
                            )

                            message_count += 1

                if conversation_count % 10 == 0:
                    print(f"   ⏳ Processed {conversation_count} conversations...")

            except Exception as e:
                print(f"   ⚠️  Error importing conversation {conversation.get('id')}: {e}")
                continue

        self.conn.commit()

        print(f"\n✅ ChatGPT import complete:")
        print(f"   📊 Conversations: {conversation_count}")
        print(f"   💬 Messages: {message_count}")

        return conversation_count

    def import_claude(self, export_file: Path = None):
        """Import Claude conversation export"""
        print("\n" + "=" * 80)
        print("📥 IMPORTING CLAUDE DATA")
        print("=" * 80)

        if not export_file:
            # Find all JSON files in claude export folder
            json_files = list(self.claude_path.glob("**/*.json"))
            if not json_files:
                print("❌ No JSON files found in claude export folder")
                print(f"   Looking in: {self.claude_path}")
                return 0
        else:
            json_files = [export_file]

        conversation_count = 0
        message_count = 0

        for json_file in json_files:
            try:
                print(f"📂 Reading: {json_file.name}")

                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Handle both single conversation and array of conversations
                conversations = data if isinstance(data, list) else [data]

                for conversation in conversations:
                    conv_id = self._insert_conversation(
                        platform='claude',
                        conversation_id=conversation.get('id', f'manual_{json_file.stem}'),
                        title=conversation.get('title', json_file.stem),
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                        metadata=conversation
                    )

                    conversation_count += 1

                    # Insert messages
                    messages = conversation.get('messages', [])
                    for message in messages:
                        if isinstance(message, dict) and 'content' in message:
                            self._insert_message(
                                conversation_id=conv_id,
                                role=message.get('role', 'unknown'),
                                content=message['content'],
                                timestamp=message.get('timestamp', datetime.now()),
                                model='claude',
                                metadata=message
                            )

                            message_count += 1

            except Exception as e:
                print(f"   ⚠️  Error importing {json_file.name}: {e}")
                continue

        self.conn.commit()

        print(f"\n✅ Claude import complete:")
        print(f"   📊 Conversations: {conversation_count}")
        print(f"   💬 Messages: {message_count}")

        return conversation_count

    def _insert_conversation(self, platform, conversation_id, title, created_at, updated_at, metadata):
        """Insert conversation into database"""
        self.cursor.execute("""
            INSERT INTO ai_conversations
            (platform, conversation_id, title, created_at, updated_at, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (platform, conversation_id) DO UPDATE
            SET title = EXCLUDED.title,
                updated_at = EXCLUDED.updated_at,
                metadata = EXCLUDED.metadata
            RETURNING id
        """, (platform, conversation_id, title, created_at, updated_at, json.dumps(metadata)))

        return self.cursor.fetchone()[0]

    def _insert_message(self, conversation_id, role, content, timestamp, model, metadata):
        """Insert message into database"""
        tokens = len(content.split())  # Simple token estimate

        self.cursor.execute("""
            INSERT INTO ai_messages
            (conversation_id, role, content, timestamp, tokens, model, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (conversation_id, role, content, timestamp, tokens, model, json.dumps(metadata)))

    def show_stats(self):
        """Show import statistics"""
        print("\n" + "=" * 80)
        print("📊 DATABASE STATISTICS")
        print("=" * 80)

        # Platform stats
        self.cursor.execute("""
            SELECT * FROM v_platform_stats ORDER BY message_count DESC
        """)

        print("\n🤖 Platform Breakdown:")
        print(f"{'Platform':<15} {'Conversations':<15} {'Messages':<12} {'Avg Length':<12}")
        print("-" * 80)

        for row in self.cursor.fetchall():
            platform, conv_count, msg_count, avg_len, first_conv, last_msg = row
            print(f"{platform:<15} {conv_count:<15} {msg_count:<12} {int(avg_len or 0):<12}")

        # Total stats
        self.cursor.execute("""
            SELECT
                COUNT(DISTINCT c.id) as total_conversations,
                COUNT(m.id) as total_messages,
                SUM(m.tokens) as total_tokens
            FROM ai_conversations c
            LEFT JOIN ai_messages m ON c.id = m.conversation_id
        """)

        total_conv, total_msg, total_tokens = self.cursor.fetchone()

        print("\n📈 Totals:")
        print(f"   Conversations: {total_conv:,}")
        print(f"   Messages: {total_msg:,}")
        print(f"   Tokens: {total_tokens:,}")

        # Recent conversations
        self.cursor.execute("""
            SELECT platform, title, message_count, last_message
            FROM v_recent_conversations
            LIMIT 5
        """)

        print("\n🕐 Most Recent Conversations:")
        for platform, title, msg_count, last_msg in self.cursor.fetchall():
            print(f"   [{platform}] {title[:50]} ({msg_count} messages)")

    def search_demo(self):
        """Demo search functionality"""
        print("\n" + "=" * 80)
        print("🔍 SEARCH DEMO")
        print("=" * 80)

        test_queries = [
            "VR World",
            "pattern theory",
            "consciousness revolution"
        ]

        for query in test_queries:
            print(f"\nSearching for: '{query}'")

            self.cursor.execute("""
                SELECT * FROM search_messages(%s) LIMIT 3
            """, (query,))

            results = self.cursor.fetchall()
            if results:
                for platform, title, role, content, timestamp, relevance in results:
                    print(f"  [{platform}] {title[:40]}")
                    print(f"    {content[:100]}...")
                    print(f"    Relevance: {relevance:.3f}")
            else:
                print("  No results found")

    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.conn.close()
        print("\n✅ Database connection closed")

def main():
    """Main import function"""
    print()
    print("🌌" * 40)
    print()
    print("        MULTI-AI IMPORTER")
    print("        Import AI Conversations from All Platforms")
    print()
    print("🌌" * 40)

    try:
        # Load environment
        from dotenv import load_dotenv
        env_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/.env.multi_ai")
        if env_file.exists():
            load_dotenv(env_file)

        # Initialize importer
        importer = MultiAIImporter()

        # Import ChatGPT
        chatgpt_count = importer.import_chatgpt()

        # Import Claude
        claude_count = importer.import_claude()

        # Show stats
        importer.show_stats()

        # Demo search
        if chatgpt_count > 0 or claude_count > 0:
            importer.search_demo()

        # Close
        importer.close()

        print("\n" + "=" * 80)
        print("✅ IMPORT COMPLETE!")
        print("=" * 80)
        print("\n🔍 To search your AI conversations:")
        print("   SELECT * FROM search_messages('your search query');")
        print("\n📊 To view stats:")
        print("   SELECT * FROM v_platform_stats;")

    except Exception as e:
        print(f"\n❌ Error during import: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
