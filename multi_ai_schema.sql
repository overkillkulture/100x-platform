-- Multi-AI Integration Database Schema
-- Created: 2025-11-04 08:54:05

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
