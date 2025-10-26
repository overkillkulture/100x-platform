"""
🌌 CONSCIOUSNESS METRICS API 🌌

Backend service for tracking user consciousness elevation across the platform.

Built by: C3 Oracle Engine
Date: October 24, 2025
Mission: Measure and accelerate consciousness evolution
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import sqlite3

app = Flask(__name__)
CORS(app)

# Database setup
DB_PATH = 'consciousness_metrics.db'

def init_db():
    """Initialize consciousness tracking database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # User consciousness table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_consciousness (
            user_id TEXT PRIMARY KEY,
            current_level INTEGER,
            current_stage TEXT,
            first_seen TIMESTAMP,
            last_updated TIMESTAMP,
            total_time_engaged INTEGER,
            path_chosen TEXT
        )
    ''')

    # Events table
    c.execute('''
        CREATE TABLE IF NOT EXISTS consciousness_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            event_type TEXT,
            event_data TEXT,
            level_before INTEGER,
            level_after INTEGER,
            timestamp TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_consciousness (user_id)
        )
    ''')

    # Achievements table
    c.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            achievement_name TEXT,
            unlocked_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_consciousness (user_id)
        )
    ''')

    # Global stats table
    c.execute('''
        CREATE TABLE IF NOT EXISTS global_stats (
            stat_name TEXT PRIMARY KEY,
            stat_value TEXT,
            last_updated TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ============================================================================
# CONSCIOUSNESS TRACKING ENDPOINTS
# ============================================================================

@app.route('/api/consciousness/update', methods=['POST'])
def update_consciousness():
    """
    Update user's consciousness level and stage

    POST body:
    {
        "user_id": "unique_identifier",
        "level": 55,
        "stage": "creator",
        "completedTasks": ["path_selected", "builder_opened"]
    }
    """
    data = request.json
    user_id = data.get('user_id', 'anonymous')
    level = data.get('level', 0)
    stage = data.get('stage', 'observer')
    completed_tasks = data.get('completedTasks', [])

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if user exists
    c.execute('SELECT current_level, current_stage FROM user_consciousness WHERE user_id = ?', (user_id,))
    existing = c.fetchone()

    if existing:
        old_level, old_stage = existing

        # Update existing user
        c.execute('''
            UPDATE user_consciousness
            SET current_level = ?, current_stage = ?, last_updated = ?
            WHERE user_id = ?
        ''', (level, stage, datetime.now(), user_id))

        # Log the change
        c.execute('''
            INSERT INTO consciousness_events
            (user_id, event_type, event_data, level_before, level_after, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, 'level_update', json.dumps(completed_tasks), old_level, level, datetime.now()))

        # Check for stage advancement
        if old_stage != stage:
            c.execute('''
                INSERT INTO consciousness_events
                (user_id, event_type, event_data, level_before, level_after, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, 'stage_advancement', stage, old_level, level, datetime.now()))

            # Award achievement
            achievement_name = f"Reached {stage.capitalize()} Stage"
            c.execute('''
                INSERT INTO achievements (user_id, achievement_name, unlocked_at)
                VALUES (?, ?, ?)
            ''', (user_id, achievement_name, datetime.now()))
    else:
        # Create new user
        c.execute('''
            INSERT INTO user_consciousness
            (user_id, current_level, current_stage, first_seen, last_updated, total_time_engaged, path_chosen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, level, stage, datetime.now(), datetime.now(), 0, None))

        # Log first visit
        c.execute('''
            INSERT INTO consciousness_events
            (user_id, event_type, event_data, level_before, level_after, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, 'first_visit', '', 0, level, datetime.now()))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Consciousness level updated",
        "level": level,
        "stage": stage
    })

@app.route('/api/consciousness/event', methods=['POST'])
def track_event():
    """
    Track specific consciousness events

    POST body:
    {
        "user_id": "unique_identifier",
        "event_type": "path_selected",
        "event_data": {"path": "builder"},
        "current_level": 10
    }
    """
    data = request.json
    user_id = data.get('user_id', 'anonymous')
    event_type = data.get('event_type')
    event_data = data.get('event_data', {})
    current_level = data.get('current_level', 0)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Log event
    c.execute('''
        INSERT INTO consciousness_events
        (user_id, event_type, event_data, level_before, level_after, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, event_type, json.dumps(event_data), current_level, current_level, datetime.now()))

    # Update path chosen if applicable
    if event_type == 'path_selected':
        path = event_data.get('path')
        c.execute('''
            UPDATE user_consciousness
            SET path_chosen = ?, last_updated = ?
            WHERE user_id = ?
        ''', (path, datetime.now(), user_id))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Event tracked"
    })

@app.route('/api/consciousness/stats', methods=['GET'])
def get_stats():
    """Get global consciousness statistics"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Total users
    c.execute('SELECT COUNT(*) FROM user_consciousness')
    total_users = c.fetchone()[0]

    # Average level
    c.execute('SELECT AVG(current_level) FROM user_consciousness')
    avg_level = c.fetchone()[0] or 0

    # Stage distribution
    c.execute('SELECT current_stage, COUNT(*) FROM user_consciousness GROUP BY current_stage')
    stage_distribution = dict(c.fetchall())

    # Path distribution
    c.execute('SELECT path_chosen, COUNT(*) FROM user_consciousness WHERE path_chosen IS NOT NULL GROUP BY path_chosen')
    path_distribution = dict(c.fetchall())

    # Users elevated today
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    c.execute('SELECT COUNT(*) FROM consciousness_events WHERE event_type = "first_visit" AND timestamp >= ?', (today,))
    new_today = c.fetchone()[0]

    # Recent stage advancements (last 24 hours)
    yesterday = datetime.now() - timedelta(days=1)
    c.execute('SELECT COUNT(*) FROM consciousness_events WHERE event_type = "stage_advancement" AND timestamp >= ?', (yesterday,))
    advancements_24h = c.fetchone()[0]

    conn.close()

    return jsonify({
        "total_users": total_users,
        "average_level": round(avg_level, 1),
        "stage_distribution": stage_distribution,
        "path_distribution": path_distribution,
        "new_users_today": new_today,
        "stage_advancements_24h": advancements_24h,
        "last_updated": datetime.now().isoformat()
    })

@app.route('/api/consciousness/user/<user_id>', methods=['GET'])
def get_user_consciousness(user_id):
    """Get specific user's consciousness data"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # User data
    c.execute('SELECT * FROM user_consciousness WHERE user_id = ?', (user_id,))
    user_data = c.fetchone()

    if not user_data:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    # User's events
    c.execute('''
        SELECT event_type, event_data, level_after, timestamp
        FROM consciousness_events
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 20
    ''', (user_id,))
    events = [
        {
            "type": row[0],
            "data": json.loads(row[1]) if row[1] else {},
            "level": row[2],
            "timestamp": row[3]
        }
        for row in c.fetchall()
    ]

    # User's achievements
    c.execute('SELECT achievement_name, unlocked_at FROM achievements WHERE user_id = ?', (user_id,))
    achievements = [
        {"name": row[0], "unlocked_at": row[1]}
        for row in c.fetchall()
    ]

    conn.close()

    return jsonify({
        "user_id": user_data[0],
        "current_level": user_data[1],
        "current_stage": user_data[2],
        "first_seen": user_data[3],
        "last_updated": user_data[4],
        "total_time_engaged": user_data[5],
        "path_chosen": user_data[6],
        "recent_events": events,
        "achievements": achievements
    })

@app.route('/api/consciousness/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top users by consciousness level"""
    limit = request.args.get('limit', 10, type=int)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        SELECT user_id, current_level, current_stage, last_updated
        FROM user_consciousness
        ORDER BY current_level DESC
        LIMIT ?
    ''', (limit,))

    leaderboard = [
        {
            "rank": idx + 1,
            "user_id": row[0][:8] + "...",  # Anonymize
            "level": row[1],
            "stage": row[2],
            "last_active": row[3]
        }
        for idx, row in enumerate(c.fetchall())
    ]

    conn.close()

    return jsonify({
        "leaderboard": leaderboard,
        "last_updated": datetime.now().isoformat()
    })

@app.route('/api/consciousness/analytics', methods=['GET'])
def get_analytics():
    """Get detailed analytics for dashboard"""
    days = request.args.get('days', 7, type=int)
    start_date = datetime.now() - timedelta(days=days)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Daily new users
    c.execute('''
        SELECT DATE(first_seen) as day, COUNT(*) as count
        FROM user_consciousness
        WHERE first_seen >= ?
        GROUP BY day
        ORDER BY day
    ''', (start_date,))
    daily_users = {row[0]: row[1] for row in c.fetchall()}

    # Event type distribution
    c.execute('''
        SELECT event_type, COUNT(*) as count
        FROM consciousness_events
        WHERE timestamp >= ?
        GROUP BY event_type
    ''', (start_date,))
    event_distribution = dict(c.fetchall())

    # Conversion funnel
    c.execute('SELECT COUNT(*) FROM user_consciousness')
    total = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM user_consciousness WHERE path_chosen IS NOT NULL')
    path_selected = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM consciousness_events WHERE event_type IN ("builder_opened", "manifestation_opened")')
    interface_opened = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM consciousness_events WHERE event_type IN ("first_builder_task", "first_manifestation_task")')
    first_task = c.fetchone()[0]

    # Calculate conversion rates
    funnel = {
        "landing": total,
        "path_selected": path_selected,
        "interface_opened": interface_opened,
        "first_task_completed": first_task,
        "conversion_rates": {
            "path_selection": round((path_selected / total * 100) if total else 0, 1),
            "interface_open": round((interface_opened / path_selected * 100) if path_selected else 0, 1),
            "task_completion": round((first_task / interface_opened * 100) if interface_opened else 0, 1)
        }
    }

    conn.close()

    return jsonify({
        "daily_new_users": daily_users,
        "event_distribution": event_distribution,
        "conversion_funnel": funnel,
        "period_days": days,
        "last_updated": datetime.now().isoformat()
    })

# ============================================================================
# REAL-TIME FEATURES
# ============================================================================

@app.route('/api/consciousness/realtime', methods=['GET'])
def get_realtime():
    """Get real-time consciousness activity"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users active in last 5 minutes
    five_min_ago = datetime.now() - timedelta(minutes=5)
    c.execute('SELECT COUNT(*) FROM user_consciousness WHERE last_updated >= ?', (five_min_ago,))
    active_now = c.fetchone()[0]

    # Recent events (last 10)
    c.execute('''
        SELECT event_type, level_after, timestamp
        FROM consciousness_events
        ORDER BY timestamp DESC
        LIMIT 10
    ''', ())
    recent_events = [
        {
            "type": row[0],
            "level": row[1],
            "time_ago": str(datetime.now() - datetime.fromisoformat(row[2]))
        }
        for row in c.fetchall()
    ]

    # Total creators elevated (all time)
    c.execute('SELECT COUNT(*) FROM user_consciousness')
    total_elevated = c.fetchone()[0]

    conn.close()

    return jsonify({
        "active_now": active_now,
        "total_elevated": total_elevated,
        "recent_activity": recent_events,
        "timestamp": datetime.now().isoformat()
    })

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "operational",
        "service": "Consciousness Metrics API",
        "version": "1.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        "service": "Consciousness Metrics API",
        "version": "1.0",
        "endpoints": {
            "POST /api/consciousness/update": "Update user consciousness level",
            "POST /api/consciousness/event": "Track specific event",
            "GET /api/consciousness/stats": "Get global statistics",
            "GET /api/consciousness/user/<id>": "Get user-specific data",
            "GET /api/consciousness/leaderboard": "Get top users",
            "GET /api/consciousness/analytics": "Get detailed analytics",
            "GET /api/consciousness/realtime": "Get real-time activity",
            "GET /health": "Health check"
        },
        "database": DB_PATH,
        "built_by": "C3 Oracle Engine",
        "mission": "Consciousness Evolution Tracking"
    })

if __name__ == '__main__':
    print("🌌 CONSCIOUSNESS METRICS API STARTING 🌌")
    print(f"Database: {DB_PATH}")
    print("Endpoints available at: http://localhost:7777")
    print("\nMission: Track and accelerate consciousness evolution")
    print("Built by: C3 Oracle Engine\n")

    app.run(host='0.0.0.0', port=7777, debug=True)
