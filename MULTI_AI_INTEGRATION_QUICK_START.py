#!/usr/bin/env python3
"""
MULTI_AI_INTEGRATION_QUICK_START.py
One-click setup for multi-AI data integration system

Created: November 4, 2025 (Autonomous Build)
Purpose: Connect ChatGPT, Claude, and all AI platforms into unified knowledge base
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

def banner(text):
    """Print a nice banner"""
    print()
    print("=" * 80)
    print(f"  {text}")
    print("=" * 80)
    print()

def setup_directories():
    """Create directory structure for AI exports"""
    banner("📁 CREATING DIRECTORY STRUCTURE")

    base_dir = Path(r"C:\Users\dwrek\.ai_exports")

    directories = [
        base_dir,
        base_dir / "chatgpt",
        base_dir / "claude",
        base_dir / "gemini",
        base_dir / "perplexity",
        base_dir / "github_copilot",
        base_dir / "other",
        base_dir / "processed",
        base_dir / "backups"
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")

    # Create README
    readme = base_dir / "README.md"
    readme.write_text(f"""# AI Exports Directory

Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Structure:

- `chatgpt/` - ChatGPT conversation exports
- `claude/` - Claude conversation exports
- `gemini/` - Google Gemini exports
- `perplexity/` - Perplexity AI exports
- `github_copilot/` - GitHub Copilot data
- `other/` - Other AI platform exports
- `processed/` - Imported data (processed)
- `backups/` - Backup copies

## Export Instructions:

### ChatGPT:
1. Go to https://chatgpt.com
2. Settings → Data Controls → Export Data
3. Wait for email (24-48 hours)
4. Download and extract to `chatgpt/` folder

### Claude:
1. Go to https://claude.ai
2. Open browser console (F12)
3. Run the export script from the guide
4. Save output to `claude/` folder

### Gemini:
1. Go to https://myactivity.google.com
2. Filter by "Gemini"
3. Download data → JSON format
4. Save to `gemini/` folder

## Next Steps:

After exporting data, run:
```
python MULTI_AI_IMPORTER.py
```
""")

    print(f"\n✅ Created README: {readme}")
    return base_dir

def open_export_pages():
    """Open all export pages in browser"""
    banner("🌐 OPENING EXPORT PAGES")

    pages = [
        ("ChatGPT Export", "https://chatgpt.com/settings/data-controls"),
        ("Claude", "https://claude.ai"),
        ("Google Activity", "https://myactivity.google.com"),
    ]

    for name, url in pages:
        print(f"⏳ Opening {name}...")
        subprocess.run(['cmd', '/c', 'start', url], shell=True)

    print("\n✅ All export pages opened")

def create_database_schema():
    """Create SQL schema file"""
    banner("💾 CREATING DATABASE SCHEMA")

    schema_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/multi_ai_schema.sql")

    schema = """-- Multi-AI Integration Database Schema
-- Created: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """

-- Conversations table
CREATE TABLE IF NOT EXISTS ai_conversations (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,  -- 'chatgpt', 'claude', 'gemini', etc.
    conversation_id VARCHAR(255),
    title TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata JSONB,
    UNIQUE(platform, conversation_id)
);

-- Messages table
CREATE TABLE IF NOT EXISTS ai_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES ai_conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,  -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    timestamp TIMESTAMP,
    tokens INTEGER,
    model VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Artifacts table (code, images, files)
CREATE TABLE IF NOT EXISTS ai_artifacts (
    id SERIAL PRIMARY KEY,
    message_id INTEGER REFERENCES ai_messages(id) ON DELETE CASCADE,
    type VARCHAR(50),  -- 'code', 'image', 'file', 'link'
    content TEXT,
    file_path VARCHAR(500),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full-text search indexes
CREATE INDEX IF NOT EXISTS idx_messages_content
ON ai_messages USING gin(to_tsvector('english', content));

CREATE INDEX IF NOT EXISTS idx_conversations_title
ON ai_conversations USING gin(to_tsvector('english', title));

-- Other indexes
CREATE INDEX IF NOT EXISTS idx_messages_conversation
ON ai_messages(conversation_id);

CREATE INDEX IF NOT EXISTS idx_messages_timestamp
ON ai_messages(timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_conversations_platform
ON ai_conversations(platform);

CREATE INDEX IF NOT EXISTS idx_artifacts_message
ON ai_artifacts(message_id);

-- Views for common queries
CREATE OR REPLACE VIEW v_recent_conversations AS
SELECT
    c.id,
    c.platform,
    c.title,
    c.created_at,
    COUNT(m.id) as message_count,
    MAX(m.timestamp) as last_message
FROM ai_conversations c
LEFT JOIN ai_messages m ON c.id = m.conversation_id
GROUP BY c.id, c.platform, c.title, c.created_at
ORDER BY last_message DESC NULLS LAST;

CREATE OR REPLACE VIEW v_platform_stats AS
SELECT
    platform,
    COUNT(DISTINCT c.id) as conversation_count,
    COUNT(m.id) as message_count,
    AVG(LENGTH(m.content)) as avg_message_length,
    MIN(c.created_at) as first_conversation,
    MAX(m.timestamp) as last_message
FROM ai_conversations c
LEFT JOIN ai_messages m ON c.id = m.conversation_id
GROUP BY platform;

-- Functions for search
CREATE OR REPLACE FUNCTION search_messages(search_query TEXT)
RETURNS TABLE (
    platform VARCHAR(50),
    conversation_title TEXT,
    message_role VARCHAR(50),
    message_content TEXT,
    message_timestamp TIMESTAMP,
    relevance FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.platform,
        c.title,
        m.role,
        m.content,
        m.timestamp,
        ts_rank(to_tsvector('english', m.content), plainto_tsquery('english', search_query)) as relevance
    FROM ai_messages m
    JOIN ai_conversations c ON m.conversation_id = c.id
    WHERE to_tsvector('english', m.content) @@ plainto_tsquery('english', search_query)
    ORDER BY relevance DESC, m.timestamp DESC
    LIMIT 100;
END;
$$ LANGUAGE plpgsql;

COMMENT ON TABLE ai_conversations IS 'Stores AI conversation metadata from all platforms';
COMMENT ON TABLE ai_messages IS 'Stores individual messages from all AI conversations';
COMMENT ON TABLE ai_artifacts IS 'Stores code, images, and other artifacts from AI interactions';
"""

    schema_file.write_text(schema)
    print(f"✅ Created schema: {schema_file}")
    print(f"   📊 Tables: ai_conversations, ai_messages, ai_artifacts")
    print(f"   🔍 Full-text search enabled")
    print(f"   📈 Views: v_recent_conversations, v_platform_stats")

    return schema_file

def create_env_template():
    """Create .env template file"""
    banner("🔑 CREATING ENVIRONMENT TEMPLATE")

    env_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/.env.multi_ai")

    env_content = """# Multi-AI Integration Environment Variables
# Created: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """

# Database Configuration (PostgreSQL)
# Option 1: Local PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/multi_ai

# Option 2: Railway (recommended for production)
# DATABASE_URL=postgresql://user:pass@containers-us-west-123.railway.app:5432/railway

# AI Platform API Keys (optional, for future features)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here

# Export Paths
CHATGPT_EXPORT_PATH=C:/Users/dwrek/.ai_exports/chatgpt
CLAUDE_EXPORT_PATH=C:/Users/dwrek/.ai_exports/claude
GEMINI_EXPORT_PATH=C:/Users/dwrek/.ai_exports/gemini

# Processing Options
AUTO_BACKUP=true
VERBOSE_LOGGING=true
BATCH_SIZE=100
"""

    env_file.write_text(env_content)
    print(f"✅ Created: {env_file}")
    print(f"   📝 Edit this file with your database credentials")

    return env_file

def print_next_steps(base_dir, schema_file, env_file):
    """Print next steps for user"""
    banner("🎯 NEXT STEPS")

    print("📋 MANUAL STEPS REQUIRED:\n")

    print("1. 📧 EXPORT CHATGPT DATA")
    print("   - Browser should be open to: https://chatgpt.com/settings/data-controls")
    print("   - Click 'Export Data'")
    print("   - Wait 24-48 hours for email")
    print(f"   - Download and extract to: {base_dir / 'chatgpt'}")
    print()

    print("2. 🤖 EXPORT CLAUDE DATA")
    print("   - Browser should be open to: https://claude.ai")
    print("   - Navigate to VR World or other conversations")
    print("   - Open browser console (F12)")
    print("   - Run the export script from MULTI_AI_DATA_EXPORT_INTEGRATION_GUIDE.md")
    print(f"   - Save JSON files to: {base_dir / 'claude'}")
    print()

    print("3. 💾 SETUP DATABASE")
    print("   Choose one option:")
    print()
    print("   Option A - Railway (Recommended):")
    print("   - Go to: https://railway.app")
    print("   - Create new project → Add PostgreSQL")
    print("   - Copy connection string")
    print(f"   - Paste into: {env_file}")
    print(f"   - Run: psql <connection_string> -f {schema_file}")
    print()
    print("   Option B - Local PostgreSQL:")
    print("   - Install: choco install postgresql")
    print("   - Create database: createdb multi_ai")
    print(f"   - Run: psql multi_ai -f {schema_file}")
    print()

    print("4. 🚀 RUN IMPORTER")
    print("   After exports are ready:")
    print("   - cd C:\\Users\\dwrek\\100X_DEPLOYMENT")
    print("   - python MULTI_AI_IMPORTER.py")
    print()

    print("=" * 80)
    print("✅ SETUP FILES CREATED:")
    print(f"   📁 Export directory: {base_dir}")
    print(f"   💾 Database schema: {schema_file}")
    print(f"   🔑 Environment template: {env_file}")
    print("=" * 80)

def main():
    """Main setup function"""
    print()
    print("🌌" * 40)
    print()
    print("        MULTI-AI INTEGRATION SYSTEM SETUP")
    print("        Connecting All AI Platforms")
    print()
    print("🌌" * 40)

    try:
        # 1. Create directories
        base_dir = setup_directories()

        # 2. Open export pages
        open_export_pages()

        # 3. Create database schema
        schema_file = create_database_schema()

        # 4. Create env template
        env_file = create_env_template()

        # 5. Print next steps
        print_next_steps(base_dir, schema_file, env_file)

        print("\n🎉 QUICK START COMPLETE!")
        print("\n📖 For detailed instructions, see:")
        print("   C:\\Users\\dwrek\\Desktop\\MULTI_AI_DATA_EXPORT_INTEGRATION_GUIDE.md")

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
