-- =====================================================
-- CONSCIOUSNESS REVOLUTION - UNIFIED DATABASE SCHEMA
-- Complete Revenue System Architecture
-- =====================================================
-- Purpose: Single database for all 7 domains
-- Supports: $10M Year 1 scaling to $1B+
-- =====================================================

-- =====================================================
-- CORE USER MANAGEMENT
-- =====================================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    consciousness_score INTEGER DEFAULT 0,

    -- Profile
    avatar_url TEXT,
    bio TEXT,
    timezone VARCHAR(50) DEFAULT 'UTC',

    -- Status
    email_verified BOOLEAN DEFAULT FALSE,
    account_status VARCHAR(20) DEFAULT 'active', -- active, suspended, deleted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,

    -- Tracking
    signup_source VARCHAR(100), -- organic, referral, affiliate, ad
    referrer_id INTEGER REFERENCES users(id),
    utm_source VARCHAR(100),
    utm_campaign VARCHAR(100),

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_email (email),
    INDEX idx_consciousness_score (consciousness_score),
    INDEX idx_created_at (created_at)
);

-- =====================================================
-- SUBSCRIPTION MANAGEMENT
-- =====================================================

CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    domain VARCHAR(50) NOT NULL, -- music, education, intelligence, etc.
    tier VARCHAR(50) NOT NULL, -- free, pro, pro_plus, enterprise

    -- Stripe Integration
    stripe_subscription_id VARCHAR(255) UNIQUE,
    stripe_customer_id VARCHAR(255),
    stripe_price_id VARCHAR(255),

    -- Pricing
    price_monthly DECIMAL(10,2),
    price_annual DECIMAL(10,2),
    billing_period VARCHAR(20), -- monthly, annual

    -- Status
    status VARCHAR(20) DEFAULT 'active', -- active, past_due, canceled, paused
    trial_end_date TIMESTAMP,
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    canceled_at TIMESTAMP,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_user_id (user_id),
    INDEX idx_domain (domain),
    INDEX idx_status (status),
    INDEX idx_stripe_subscription_id (stripe_subscription_id)
);

-- =====================================================
-- PAYMENT TRANSACTIONS
-- =====================================================

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    subscription_id INTEGER REFERENCES subscriptions(id),

    -- Transaction Details
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    type VARCHAR(50) NOT NULL, -- subscription, one_time, refund, marketplace_payout

    -- Stripe Integration
    stripe_payment_intent_id VARCHAR(255),
    stripe_invoice_id VARCHAR(255),

    -- Status
    status VARCHAR(20) DEFAULT 'pending', -- pending, succeeded, failed, refunded
    failure_reason TEXT,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP,
    refunded_at TIMESTAMP,

    -- Metadata
    description TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_user_id (user_id),
    INDEX idx_subscription_id (subscription_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_stripe_payment_intent_id (stripe_payment_intent_id)
);

-- =====================================================
-- DOMAIN ACCESS CONTROL
-- =====================================================

CREATE TABLE domain_access (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    domain VARCHAR(50) NOT NULL, -- music, education, intelligence, etc.

    -- Access Level
    tier VARCHAR(50) NOT NULL, -- free, pro, pro_plus, enterprise
    feature_flags JSONB DEFAULT '{}'::jsonb, -- {"ai_actions_per_month": 25, "unlimited_modules": false}

    -- Usage Tracking
    usage_current_month JSONB DEFAULT '{}'::jsonb, -- {"ai_actions": 12, "modules_created": 3}
    usage_reset_date TIMESTAMP,

    -- Status
    active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP,

    -- Timestamps
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_user_domain (user_id, domain),
    INDEX idx_domain (domain),
    INDEX idx_active (active),
    UNIQUE(user_id, domain)
);

-- =====================================================
-- MARKETPLACE (Creator Economy)
-- =====================================================

CREATE TABLE marketplace_items (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER NOT NULL REFERENCES users(id),

    -- Item Details
    type VARCHAR(50) NOT NULL, -- korpak, module, data_crystal, course, template
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    tags TEXT[], -- ['automation', 'social-media', 'instagram']

    -- Pricing
    price DECIMAL(10,2) NOT NULL,
    commission_rate DECIMAL(5,2) DEFAULT 30.00, -- Platform takes 30%

    -- Content
    file_url TEXT,
    preview_url TEXT,
    demo_url TEXT,

    -- Stats
    total_sales INTEGER DEFAULT 0,
    total_revenue DECIMAL(10,2) DEFAULT 0,
    average_rating DECIMAL(3,2),
    review_count INTEGER DEFAULT 0,

    -- Status
    status VARCHAR(20) DEFAULT 'draft', -- draft, pending_review, published, suspended
    published_at TIMESTAMP,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_creator_id (creator_id),
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_total_sales (total_sales DESC)
);

CREATE TABLE marketplace_purchases (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER NOT NULL REFERENCES users(id),
    item_id INTEGER NOT NULL REFERENCES marketplace_items(id),
    creator_id INTEGER NOT NULL REFERENCES users(id),

    -- Transaction
    price_paid DECIMAL(10,2) NOT NULL,
    creator_earnings DECIMAL(10,2) NOT NULL, -- 70% of price
    platform_commission DECIMAL(10,2) NOT NULL, -- 30% of price
    transaction_id INTEGER REFERENCES transactions(id),

    -- Status
    status VARCHAR(20) DEFAULT 'completed', -- completed, refunded
    refunded_at TIMESTAMP,

    -- Timestamps
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_buyer_id (buyer_id),
    INDEX idx_item_id (item_id),
    INDEX idx_creator_id (creator_id),
    INDEX idx_purchased_at (purchased_at)
);

CREATE TABLE creator_payouts (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER NOT NULL REFERENCES users(id),

    -- Payout Details
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',

    -- Stripe Connect
    stripe_transfer_id VARCHAR(255),
    stripe_connect_account_id VARCHAR(255),

    -- Status
    status VARCHAR(20) DEFAULT 'pending', -- pending, processing, paid, failed

    -- Timestamps
    period_start DATE,
    period_end DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP,

    -- Metadata
    items_count INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_creator_id (creator_id),
    INDEX idx_status (status),
    INDEX idx_period_end (period_end)
);

-- =====================================================
-- KORPAK SYSTEM (Autonomous Work Generation)
-- =====================================================

CREATE TABLE korpaks (
    id SERIAL PRIMARY KEY,

    -- KORPAK Identity
    name VARCHAR(255) NOT NULL,
    mission TEXT NOT NULL,
    category VARCHAR(100), -- revenue, product, marketing, operations

    -- Configuration
    steps JSONB NOT NULL, -- [{"step": 1, "action": "...", "ai_executable": true}, ...]
    estimated_timeline_days INTEGER,

    -- Prerequisites
    required_tools TEXT[],
    required_access TEXT[],
    required_resources JSONB,

    -- Success Criteria
    success_metrics JSONB, -- {"mrr_target": 10000, "user_target": 100}

    -- Marketplace
    is_public BOOLEAN DEFAULT FALSE,
    creator_id INTEGER REFERENCES users(id),
    price DECIMAL(10,2),

    -- Stats
    times_executed INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2),
    average_completion_days DECIMAL(5,1),

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_category (category),
    INDEX idx_is_public (is_public)
);

CREATE TABLE korpak_executions (
    id SERIAL PRIMARY KEY,
    korpak_id INTEGER NOT NULL REFERENCES korpaks(id),
    user_id INTEGER NOT NULL REFERENCES users(id),

    -- Execution State
    status VARCHAR(20) DEFAULT 'pending', -- pending, in_progress, completed, failed, paused
    current_step INTEGER DEFAULT 1,
    total_steps INTEGER NOT NULL,

    -- Progress Tracking
    steps_completed INTEGER DEFAULT 0,
    steps_failed INTEGER DEFAULT 0,
    steps_skipped INTEGER DEFAULT 0,
    completion_percentage DECIMAL(5,2) DEFAULT 0,

    -- Execution Log
    execution_log JSONB DEFAULT '[]'::jsonb, -- [{"step": 1, "completed_at": "...", "result": "..."}]

    -- Timestamps
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    estimated_completion_date TIMESTAMP,

    -- Results
    final_metrics JSONB, -- {"mrr_achieved": 8500, "users_acquired": 87}
    success BOOLEAN,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_korpak_id (korpak_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_started_at (started_at)
);

-- =====================================================
-- REVENUE ANALYTICS
-- =====================================================

CREATE TABLE revenue_snapshots (
    id SERIAL PRIMARY KEY,

    -- Snapshot Period
    period_type VARCHAR(20) NOT NULL, -- daily, weekly, monthly
    period_date DATE NOT NULL,

    -- Revenue Metrics
    mrr DECIMAL(10,2) DEFAULT 0,
    arr DECIMAL(10,2) DEFAULT 0,
    one_time_revenue DECIMAL(10,2) DEFAULT 0,
    total_revenue DECIMAL(10,2) DEFAULT 0,

    -- Customer Metrics
    total_customers INTEGER DEFAULT 0,
    new_customers INTEGER DEFAULT 0,
    churned_customers INTEGER DEFAULT 0,
    churn_rate DECIMAL(5,2) DEFAULT 0,

    -- Conversion Metrics
    free_tier_users INTEGER DEFAULT 0,
    trial_users INTEGER DEFAULT 0,
    paid_users INTEGER DEFAULT 0,
    conversion_rate DECIMAL(5,2) DEFAULT 0,

    -- Financial Metrics
    average_revenue_per_user DECIMAL(10,2) DEFAULT 0,
    customer_lifetime_value DECIMAL(10,2) DEFAULT 0,
    customer_acquisition_cost DECIMAL(10,2) DEFAULT 0,
    ltv_cac_ratio DECIMAL(5,2) DEFAULT 0,

    -- Domain Breakdown
    revenue_by_domain JSONB DEFAULT '{}'::jsonb,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(period_type, period_date),
    INDEX idx_period_date (period_date DESC)
);

-- =====================================================
-- FREEMIUM CONVERSION TRACKING
-- =====================================================

CREATE TABLE conversion_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),

    -- Event Details
    event_type VARCHAR(50) NOT NULL, -- signup, trial_start, upgrade, downgrade, cancel
    from_tier VARCHAR(50),
    to_tier VARCHAR(50),
    domain VARCHAR(50) NOT NULL,

    -- Context
    trigger VARCHAR(100), -- user_initiated, usage_limit_hit, trial_ending, promotional_offer
    page_url TEXT,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_user_id (user_id),
    INDEX idx_event_type (event_type),
    INDEX idx_domain (domain),
    INDEX idx_created_at (created_at)
);

-- =====================================================
-- ALLY NETWORK (Customer Acquisition)
-- =====================================================

CREATE TABLE keystone_allies (
    id SERIAL PRIMARY KEY,

    -- Ally Details
    name VARCHAR(255) NOT NULL,
    platform VARCHAR(50), -- twitter, youtube, podcast, newsletter
    handle VARCHAR(255),
    url TEXT,

    -- Reach
    follower_count INTEGER,
    engagement_rate DECIMAL(5,2),
    estimated_reach INTEGER,

    -- Categories
    categories TEXT[], -- ['crypto', 'consciousness', 'entrepreneurship']

    -- Engagement Status
    status VARCHAR(20) DEFAULT 'target', -- target, engaging, unlocked, active, dormant
    unlock_date TIMESTAMP,

    -- Engagement History
    total_interactions INTEGER DEFAULT 0,
    last_interaction_date TIMESTAMP,
    interaction_log JSONB DEFAULT '[]'::jsonb,

    -- Results
    estimated_users_referred INTEGER DEFAULT 0,
    confirmed_users_referred INTEGER DEFAULT 0,
    revenue_attributed DECIMAL(10,2) DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_status (status),
    INDEX idx_unlock_date (unlock_date)
);

-- =====================================================
-- AUTOMATED MONITORING & ALERTS
-- =====================================================

CREATE TABLE system_alerts (
    id SERIAL PRIMARY KEY,

    -- Alert Details
    severity VARCHAR(20) NOT NULL, -- critical, warning, advisory, info
    category VARCHAR(50) NOT NULL, -- revenue, churn, conversion, technical, security
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,

    -- Status
    status VARCHAR(20) DEFAULT 'active', -- active, acknowledged, resolved
    acknowledged_at TIMESTAMP,
    resolved_at TIMESTAMP,

    -- Action Items
    suggested_actions JSONB, -- [{"action": "...", "priority": "high"}]
    auto_fix_attempted BOOLEAN DEFAULT FALSE,
    auto_fix_result TEXT,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    INDEX idx_severity (severity),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC)
);

-- =====================================================
-- MUSIC DOMAIN SPECIFIC TABLES
-- =====================================================

CREATE TABLE music_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) UNIQUE,

    -- Artist Info
    artist_name VARCHAR(255),
    genre VARCHAR(100),
    spotify_artist_id VARCHAR(255),
    apple_music_artist_id VARCHAR(255),

    -- Connected Platforms
    spotify_access_token TEXT,
    apple_music_token TEXT,
    youtube_channel_id VARCHAR(255),
    soundcloud_id VARCHAR(255),

    -- Revenue Streams Status
    streams_tracking_enabled BOOLEAN DEFAULT FALSE,
    sync_licensing_enabled BOOLEAN DEFAULT FALSE,
    merchandise_enabled BOOLEAN DEFAULT FALSE,
    patreon_connected BOOLEAN DEFAULT FALSE,

    -- Stats
    total_monthly_streams INTEGER DEFAULT 0,
    estimated_monthly_revenue DECIMAL(10,2) DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_user_id (user_id)
);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Active Paying Customers by Domain
CREATE VIEW active_subscriptions_by_domain AS
SELECT
    domain,
    tier,
    COUNT(*) as subscriber_count,
    SUM(CASE
        WHEN billing_period = 'monthly' THEN price_monthly
        WHEN billing_period = 'annual' THEN price_annual / 12
    END) as monthly_recurring_revenue
FROM subscriptions
WHERE status = 'active'
GROUP BY domain, tier;

-- Monthly Revenue Report
CREATE VIEW monthly_revenue_report AS
SELECT
    DATE_TRUNC('month', created_at) as month,
    SUM(amount) as total_revenue,
    COUNT(DISTINCT user_id) as unique_customers,
    AVG(amount) as average_transaction
FROM transactions
WHERE status = 'succeeded'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;

-- User Lifetime Value
CREATE VIEW user_lifetime_value AS
SELECT
    user_id,
    SUM(amount) as total_revenue,
    COUNT(*) as transaction_count,
    MIN(created_at) as first_purchase,
    MAX(created_at) as last_purchase,
    EXTRACT(DAYS FROM (MAX(created_at) - MIN(created_at))) as customer_tenure_days
FROM transactions
WHERE status = 'succeeded'
GROUP BY user_id;

-- =====================================================
-- FUNCTIONS FOR AUTOMATION
-- =====================================================

-- Calculate MRR from subscriptions
CREATE OR REPLACE FUNCTION calculate_mrr()
RETURNS DECIMAL(10,2) AS $$
    SELECT COALESCE(SUM(
        CASE
            WHEN billing_period = 'monthly' THEN price_monthly
            WHEN billing_period = 'annual' THEN price_annual / 12
            ELSE 0
        END
    ), 0)
    FROM subscriptions
    WHERE status = 'active';
$$ LANGUAGE SQL;

-- Update timestamps automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_marketplace_items_updated_at BEFORE UPDATE ON marketplace_items
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_korpaks_updated_at BEFORE UPDATE ON korpaks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Composite indexes for common queries
CREATE INDEX idx_active_subscriptions ON subscriptions(user_id, status) WHERE status = 'active';
CREATE INDEX idx_recent_transactions ON transactions(user_id, created_at DESC);
CREATE INDEX idx_published_marketplace ON marketplace_items(status, created_at DESC) WHERE status = 'published';

-- =====================================================
-- INITIAL DATA SETUP
-- =====================================================

-- Insert tier configurations
CREATE TABLE subscription_tiers (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(50) NOT NULL,
    tier_name VARCHAR(50) NOT NULL,
    monthly_price DECIMAL(10,2) NOT NULL,
    annual_price DECIMAL(10,2) NOT NULL,
    features JSONB NOT NULL,
    stripe_price_id_monthly VARCHAR(255),
    stripe_price_id_annual VARCHAR(255),
    active BOOLEAN DEFAULT TRUE,

    UNIQUE(domain, tier_name)
);

-- Seed subscription tiers
INSERT INTO subscription_tiers (domain, tier_name, monthly_price, annual_price, features) VALUES
('music', 'free', 0, 0, '{"streams_tracking": true, "basic_analytics": true, "monthly_limit": 100}'),
('music', 'pro', 29.99, 299.99, '{"streams_tracking": true, "advanced_analytics": true, "sync_licensing": true, "unlimited": true}'),
('music', 'pro_plus', 49.99, 499.99, '{"everything_in_pro": true, "team_collaboration": true, "api_access": true, "priority_support": true}'),
('intelligence', 'free', 0, 0, '{"ai_actions_per_month": 25, "basic_models": true}'),
('intelligence', 'pro', 49.99, 499.99, '{"ai_actions_unlimited": true, "advanced_models": true, "trinity_access": true}'),
('tools', 'free', 0, 0, '{"modules_limit": 5, "basic_features": true}'),
('tools', 'pro', 97, 970, '{"modules_unlimited": true, "all_features": true, "priority_builds": true}');

-- =====================================================
-- DATABASE SCHEMA COMPLETE
-- Ready for deployment to Railway/Render/Supabase
-- Supports $10M+ Year 1 revenue scaling
-- =====================================================
