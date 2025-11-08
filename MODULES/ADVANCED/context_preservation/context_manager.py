#!/usr/bin/env python3
"""
CONTEXT PRESERVATION MODULE
============================

Advanced context management for AI conversations with persistence,
compression, priority-based retention, and intelligent summarization.

Features:
- Conversation history tracking
- Context summarization and compression
- Priority-based context retention
- Multi-session continuity
- Semantic search over past context
- Context injection for new sessions
- Memory optimization
- Export/import capabilities

Module #22 of 100x Platform
"""

import json
import hashlib
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum
import re


class MessageRole(Enum):
    """Message roles in conversation"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Priority(Enum):
    """Context priority levels"""
    CRITICAL = "critical"  # Never compress or drop
    HIGH = "high"  # Compress only when necessary
    MEDIUM = "medium"  # Compress aggressively
    LOW = "low"  # Drop when space needed


@dataclass
class Message:
    """Single message in conversation"""
    role: MessageRole
    content: str
    timestamp: datetime
    priority: Priority = Priority.MEDIUM
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
        if isinstance(self.role, str):
            self.role = MessageRole(self.role)
        if isinstance(self.priority, str):
            self.priority = Priority(self.priority)

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'role': self.role.value,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'priority': self.priority.value,
            'metadata': self.metadata
        }


@dataclass
class ContextWindow:
    """Managing context within token limits"""
    messages: List[Message]
    max_tokens: int = 100000  # Maximum context window
    current_tokens: int = 0
    session_id: str = None

    def __post_init__(self):
        if self.session_id is None:
            self.session_id = self._generate_session_id()
        self._recalculate_tokens()

    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(timestamp.encode()).hexdigest()[:16]

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)"""
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4

    def _recalculate_tokens(self):
        """Recalculate total token usage"""
        self.current_tokens = sum(
            self._estimate_tokens(msg.content) for msg in self.messages
        )

    def add_message(self, message: Message) -> bool:
        """Add message to context window"""
        msg_tokens = self._estimate_tokens(message.content)

        # Check if fits
        if self.current_tokens + msg_tokens > self.max_tokens:
            # Try to make space
            self._optimize_context(msg_tokens)

        # Add if there's space now
        if self.current_tokens + msg_tokens <= self.max_tokens:
            self.messages.append(message)
            self.current_tokens += msg_tokens
            return True

        return False

    def _optimize_context(self, needed_tokens: int):
        """Optimize context to make space"""
        # Strategy:
        # 1. Summarize low-priority old messages
        # 2. Drop low-priority messages if needed
        # 3. Compress medium-priority messages

        # Sort messages by priority and age
        sortable = [(i, msg) for i, msg in enumerate(self.messages)]
        sortable.sort(key=lambda x: (
            x[1].priority.value,  # Lower priority first
            x[1].timestamp  # Older first
        ))

        freed_tokens = 0

        for idx, msg in sortable:
            if freed_tokens >= needed_tokens:
                break

            # Don't touch critical priority
            if msg.priority == Priority.CRITICAL:
                continue

            # Drop or compress
            if msg.priority == Priority.LOW:
                # Just drop it
                freed_tokens += self._estimate_tokens(msg.content)
                self.messages.remove(msg)
            elif msg.priority == Priority.MEDIUM:
                # Compress it
                original_tokens = self._estimate_tokens(msg.content)
                compressed = self._compress_message(msg)
                msg.content = compressed
                new_tokens = self._estimate_tokens(compressed)
                freed_tokens += (original_tokens - new_tokens)

        self._recalculate_tokens()

    def _compress_message(self, message: Message) -> str:
        """Compress message content"""
        content = message.content

        # For long messages, create a summary
        if len(content) > 500:
            # Simple compression: Keep first and last parts
            lines = content.split('\n')
            if len(lines) > 10:
                summary = (
                    f"[COMPRESSED] {lines[0]}\n"
                    f"... ({len(lines)-4} lines summarized) ...\n"
                    f"{lines[-2]}\n{lines[-1]}"
                )
                return summary

        return content

    def get_context_for_llm(self) -> List[Dict]:
        """Get context formatted for LLM"""
        return [
            {'role': msg.role.value, 'content': msg.content}
            for msg in self.messages
        ]

    def search_context(self, query: str, top_k: int = 5) -> List[Message]:
        """Semantic search over context (simple keyword-based)"""
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))

        # Score messages by keyword overlap
        scored = []
        for msg in self.messages:
            msg_words = set(re.findall(r'\w+', msg.content.lower()))
            overlap = len(query_words & msg_words)
            if overlap > 0:
                scored.append((overlap, msg))

        # Sort by score and return top_k
        scored.sort(reverse=True, key=lambda x: x[0])
        return [msg for score, msg in scored[:top_k]]


class ContextManager:
    """High-level context management with persistence"""

    def __init__(self, storage_dir: str = "context_storage"):
        """Initialize context manager"""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

        self.current_window = ContextWindow(messages=[])
        self.sessions: Dict[str, Path] = {}  # session_id -> file_path

        self._load_sessions_index()

    def _load_sessions_index(self):
        """Load index of existing sessions"""
        index_file = self.storage_dir / "sessions_index.json"
        if index_file.exists():
            with open(index_file) as f:
                data = json.load(f)
                self.sessions = {k: Path(v) for k, v in data.items()}

    def _save_sessions_index(self):
        """Save sessions index"""
        index_file = self.storage_dir / "sessions_index.json"
        with open(index_file, 'w') as f:
            json.dump({k: str(v) for k, v in self.sessions.items()}, f, indent=2)

    def add_message(self, role: MessageRole, content: str,
                   priority: Priority = Priority.MEDIUM,
                   metadata: Dict = None) -> bool:
        """Add message to current context"""
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            priority=priority,
            metadata=metadata or {}
        )
        return self.current_window.add_message(message)

    def save_session(self, session_name: Optional[str] = None) -> str:
        """Save current session to disk"""
        if session_name is None:
            session_name = f"session_{self.current_window.session_id}"

        session_file = self.storage_dir / f"{session_name}.json"

        session_data = {
            'session_id': self.current_window.session_id,
            'created': datetime.now().isoformat(),
            'messages': [msg.to_dict() for msg in self.current_window.messages],
            'metadata': {
                'total_messages': len(self.current_window.messages),
                'total_tokens': self.current_window.current_tokens
            }
        }

        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

        self.sessions[self.current_window.session_id] = session_file
        self._save_sessions_index()

        return str(session_file)

    def load_session(self, session_id: str) -> bool:
        """Load session from disk"""
        if session_id not in self.sessions:
            return False

        session_file = self.sessions[session_id]
        if not session_file.exists():
            return False

        with open(session_file) as f:
            data = json.load(f)

        # Reconstruct messages
        messages = [
            Message(
                role=MessageRole(msg['role']),
                content=msg['content'],
                timestamp=datetime.fromisoformat(msg['timestamp']),
                priority=Priority(msg['priority']),
                metadata=msg.get('metadata', {})
            )
            for msg in data['messages']
        ]

        self.current_window = ContextWindow(
            messages=messages,
            session_id=data['session_id']
        )

        return True

    def create_summary(self, max_length: int = 1000) -> str:
        """Create summary of current conversation"""
        if not self.current_window.messages:
            return "No conversation history."

        # Count messages by role
        role_counts = {}
        for msg in self.current_window.messages:
            role_counts[msg.role.value] = role_counts.get(msg.role.value, 0) + 1

        # Get key topics (simple keyword extraction)
        all_text = " ".join(msg.content for msg in self.current_window.messages)
        words = re.findall(r'\w+', all_text.lower())
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1

        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

        summary = f"""CONVERSATION SUMMARY
Session: {self.current_window.session_id}
Messages: {len(self.current_window.messages)} ({', '.join(f'{k}: {v}' for k, v in role_counts.items())})
Tokens: {self.current_window.current_tokens:,}

Key Topics: {', '.join(word for word, count in top_keywords)}

First Exchange:
{self.current_window.messages[0].content[:200]}...

Latest Exchange:
{self.current_window.messages[-1].content[:200]}...
"""
        return summary

    def export_markdown(self, output_file: str):
        """Export conversation to markdown"""
        with open(output_file, 'w') as f:
            f.write(f"# Conversation Export\n\n")
            f.write(f"**Session ID:** {self.current_window.session_id}\n")
            f.write(f"**Total Messages:** {len(self.current_window.messages)}\n")
            f.write(f"**Total Tokens:** {self.current_window.current_tokens:,}\n\n")
            f.write("---\n\n")

            for msg in self.current_window.messages:
                f.write(f"### {msg.role.value.upper()}\n")
                f.write(f"*{msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                f.write(f"{msg.content}\n\n")
                f.write("---\n\n")

    def get_stats(self) -> Dict:
        """Get statistics about current context"""
        return {
            'session_id': self.current_window.session_id,
            'total_messages': len(self.current_window.messages),
            'total_tokens': self.current_window.current_tokens,
            'max_tokens': self.current_window.max_tokens,
            'utilization': f"{(self.current_window.current_tokens / self.current_window.max_tokens * 100):.1f}%",
            'saved_sessions': len(self.sessions),
            'priority_breakdown': self._get_priority_breakdown()
        }

    def _get_priority_breakdown(self) -> Dict[str, int]:
        """Get count of messages by priority"""
        breakdown = {}
        for msg in self.current_window.messages:
            breakdown[msg.priority.value] = breakdown.get(msg.priority.value, 0) + 1
        return breakdown


def demo():
    """Demonstrate context manager"""
    print("=" * 70)
    print("CONTEXT PRESERVATION MODULE - MODULE #22")
    print("=" * 70)
    print()

    manager = ContextManager()

    # Simulate a conversation
    print("📝 Simulating conversation...")
    manager.add_message(MessageRole.SYSTEM, "You are a helpful AI assistant.", priority=Priority.CRITICAL)
    manager.add_message(MessageRole.USER, "What is machine learning?")
    manager.add_message(MessageRole.ASSISTANT, "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. It involves algorithms that can identify patterns, make predictions, and improve performance over time.")
    manager.add_message(MessageRole.USER, "Give me an example.")
    manager.add_message(MessageRole.ASSISTANT, "Sure! Email spam filters use machine learning. They learn to identify spam by analyzing thousands of emails labeled as spam or not spam, then automatically classify new emails based on those patterns.", priority=Priority.HIGH)
    manager.add_message(MessageRole.USER, "That's helpful, thanks!")
    manager.add_message(MessageRole.ASSISTANT, "You're welcome! Feel free to ask more questions.")

    print(f"✅ Added {len(manager.current_window.messages)} messages\n")

    # Show stats
    print("📊 CONTEXT STATISTICS:")
    print("-" * 70)
    stats = manager.get_stats()
    for key, value in stats.items():
        if key != 'priority_breakdown':
            print(f"   {key}: {value}")
    print(f"   Priority breakdown: {stats['priority_breakdown']}")
    print()

    # Search context
    print("🔍 SEARCHING CONTEXT for 'spam':")
    print("-" * 70)
    results = manager.current_window.search_context("spam")
    for i, msg in enumerate(results, 1):
        print(f"{i}. [{msg.role.value}] {msg.content[:100]}...")
    print()

    # Create summary
    print("📋 CONVERSATION SUMMARY:")
    print("-" * 70)
    print(manager.create_summary())
    print()

    # Save session
    print("💾 SAVING SESSION:")
    print("-" * 70)
    saved_path = manager.save_session("demo_session")
    print(f"   Saved to: {saved_path}")
    print()

    # Export
    print("📤 EXPORTING TO MARKDOWN:")
    print("-" * 70)
    manager.export_markdown("conversation_export.md")
    print("   Exported to: conversation_export.md")
    print()

    print("=" * 70)
    print("✅ Module #22 - Context Preservation - OPERATIONAL")
    print("=" * 70)


if __name__ == "__main__":
    demo()
