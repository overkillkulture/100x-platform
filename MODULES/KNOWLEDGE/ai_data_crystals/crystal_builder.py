#!/usr/bin/env python3
"""
AI DATA CRYSTALS - Knowledge → AI Transformation Engine
Converts your documents and knowledge into a queryable AI crystal
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

try:
    import anthropic
    from dotenv import load_dotenv
except ImportError:
    print("❌ Required packages missing")
    print("   pip install anthropic python-dotenv")
    exit(1)


class CrystalBuilder:
    """Builds AI crystals from your knowledge"""

    def __init__(self, crystal_name: str):
        load_dotenv()

        self.crystal_name = crystal_name
        self.crystal_dir = Path.home() / ".ai_crystals" / crystal_name
        self.crystal_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Claude
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.claude = anthropic.Anthropic(api_key=api_key)

        # Crystal metadata
        self.metadata_file = self.crystal_dir / "metadata.json"
        self.knowledge_file = self.crystal_dir / "knowledge_base.txt"
        self.index_file = self.crystal_dir / "index.json"

        self._load_or_create_metadata()

    def _load_or_create_metadata(self):
        """Load existing crystal or create new one"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
            print(f"📦 Loaded existing crystal: {self.crystal_name}")
        else:
            self.metadata = {
                "name": self.crystal_name,
                "created": datetime.now().isoformat(),
                "documents": [],
                "total_size": 0,
                "last_updated": datetime.now().isoformat()
            }
            self._save_metadata()
            print(f"💎 Created new crystal: {self.crystal_name}")

    def _save_metadata(self):
        """Save crystal metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def add_document(self, file_path: str, category: Optional[str] = None):
        """Add a document to the crystal"""
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False

        print(f"\n📄 Processing: {file_path.name}")

        # Read file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            print("   ⚠️  Binary file, skipping...")
            return False

        # Extract knowledge using Claude
        print("   🧠 Extracting knowledge...")
        summary = self._extract_knowledge(content, file_path.name)

        # Append to knowledge base
        with open(self.knowledge_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n{'='*60}\n")
            f.write(f"SOURCE: {file_path.name}\n")
            f.write(f"CATEGORY: {category or 'General'}\n")
            f.write(f"DATE ADDED: {datetime.now().isoformat()}\n")
            f.write(f"{'='*60}\n\n")
            f.write(summary)

        # Update metadata
        self.metadata["documents"].append({
            "filename": file_path.name,
            "category": category,
            "added": datetime.now().isoformat(),
            "size": len(content)
        })
        self.metadata["total_size"] += len(content)
        self.metadata["last_updated"] = datetime.now().isoformat()
        self._save_metadata()

        print(f"   ✅ Added to crystal")
        return True

    def _extract_knowledge(self, content: str, filename: str) -> str:
        """Use Claude to extract key knowledge from document"""

        # Truncate if too long
        max_chars = 50000
        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n[... content truncated ...]"

        prompt = f"""Extract the key knowledge, insights, and concepts from this document.

Document: {filename}

Content:
{content}

Provide:
1. Main topics and themes
2. Key insights and takeaways
3. Important facts and data
4. Concepts and ideas
5. Any unique perspectives or approaches

Format as clear, searchable text that captures the essence of this document."""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text

        except Exception as e:
            print(f"   ⚠️  Extraction failed: {e}")
            return content[:2000]  # Fallback to first 2000 chars

    def query(self, question: str) -> str:
        """Query the crystal with a question"""
        if not self.knowledge_file.exists():
            return "Crystal is empty. Add documents first."

        # Load knowledge base
        with open(self.knowledge_file, 'r', encoding='utf-8') as f:
            knowledge = f.read()

        # Truncate if needed
        max_knowledge = 100000
        if len(knowledge) > max_knowledge:
            knowledge = knowledge[-max_knowledge:]  # Use most recent

        print(f"\n🔮 Querying crystal: {question}")

        prompt = f"""You are an AI crystal containing the collected knowledge of a person.
Answer questions based ONLY on the knowledge provided below.

If the answer isn't in the knowledge base, say so clearly.

Knowledge Base:
{knowledge}

Question: {question}

Answer:"""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            answer = response.content[0].text
            print(f"\n💎 Crystal says:\n{answer}\n")
            return answer

        except Exception as e:
            return f"Error querying crystal: {e}"

    def export_summary(self) -> Dict:
        """Export crystal summary"""
        return {
            "name": self.crystal_name,
            "documents": len(self.metadata["documents"]),
            "total_size": self.metadata["total_size"],
            "created": self.metadata["created"],
            "last_updated": self.metadata["last_updated"],
            "categories": list(set(
                doc.get("category", "General")
                for doc in self.metadata["documents"]
            ))
        }


def main():
    """CLI interface"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='AI Data Crystals - Your Knowledge Becomes an AI')
    parser.add_argument('crystal_name', help='Name of your crystal')
    parser.add_argument('--add', type=str, help='Add document to crystal')
    parser.add_argument('--category', type=str, help='Category for document')
    parser.add_argument('--query', type=str, help='Query your crystal')
    parser.add_argument('--summary', action='store_true', help='Show crystal summary')

    args = parser.parse_args()

    print("=" * 60)
    print("💎 AI DATA CRYSTALS")
    print("=" * 60)

    # Create/load crystal
    crystal = CrystalBuilder(args.crystal_name)

    if args.add:
        # Add document
        crystal.add_document(args.add, args.category)

    elif args.query:
        # Query crystal
        crystal.query(args.query)

    elif args.summary:
        # Show summary
        summary = crystal.export_summary()
        print(f"\n📊 Crystal Summary:")
        print(f"   Name: {summary['name']}")
        print(f"   Documents: {summary['documents']}")
        print(f"   Total Size: {summary['total_size']:,} chars")
        print(f"   Categories: {', '.join(summary['categories'])}")
        print(f"   Created: {summary['created']}")
        print(f"   Last Updated: {summary['last_updated']}")

    else:
        print("\nUsage:")
        print(f"  Add document:  python crystal_builder.py my_crystal --add document.txt --category 'Tech'")
        print(f"  Query crystal: python crystal_builder.py my_crystal --query 'What do I know about AI?'")
        print(f"  Show summary:  python crystal_builder.py my_crystal --summary")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
