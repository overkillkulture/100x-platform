"""
🏆 MERITOCRACY ENGINE - Automatic Builder Ranking System
Best builders rise to the top automatically based on contributions
No voting, no politics - just pure output measurement
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Data file
DATA_FILE = "C:/Users/dwrek/100X_DEPLOYMENT/DATA/meritocracy_data.json"

# Rank thresholds
RANKS = {
    0: {"name": "Observer", "icon": "👁️", "color": "#888888"},
    10: {"name": "Awakened Builder", "icon": "⚡", "color": "#00d4ff"},
    50: {"name": "Consciousness Engineer", "icon": "🔧", "color": "#7b2cbf"},
    200: {"name": "General", "icon": "⭐", "color": "#ffd700"},
    1000: {"name": "Commander", "icon": "👑", "color": "#ff6b9d"}
}

# Contribution types and their base points
CONTRIBUTION_TYPES = {
    # Code contributions
    "code_commit": {"points": 5, "category": "builder"},
    "code_review": {"points": 3, "category": "builder"},
    "bug_fix": {"points": 10, "category": "builder"},
    "feature_shipped": {"points": 25, "category": "builder"},

    # Documentation & Teaching
    "docs_written": {"points": 8, "category": "teacher"},
    "tutorial_created": {"points": 15, "category": "teacher"},
    "issue_explained": {"points": 4, "category": "teacher"},
    "mentor_session": {"points": 10, "category": "teacher"},

    # Vision & Strategy
    "idea_proposed": {"points": 5, "category": "visionary"},
    "pattern_identified": {"points": 12, "category": "visionary"},
    "paradigm_shift": {"points": 50, "category": "visionary"},
    "connection_made": {"points": 8, "category": "visionary"},

    # Community & Growth
    "builder_recruited": {"points": 20, "category": "growth"},
    "problem_solved": {"points": 15, "category": "growth"},
    "collaboration": {"points": 7, "category": "growth"}
}

def ensure_data_file():
    """Ensure data directory and file exist"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({
                "builders": {},
                "contributions": [],
                "ranks": RANKS
            }, f, indent=2)

def load_data():
    """Load meritocracy data"""
    ensure_data_file()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    """Save meritocracy data"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_rank_for_score(score):
    """Get rank based on score"""
    rank = RANKS[0]  # Default to Observer
    for threshold, rank_data in sorted(RANKS.items(), reverse=True):
        if score >= threshold:
            return {**rank_data, "threshold": threshold}
    return {**rank, "threshold": 0}

def calculate_builder_stats(builder_data):
    """Calculate detailed stats for a builder"""
    contributions = builder_data.get("contributions", [])

    # Category scores
    categories = {
        "builder": 0,
        "teacher": 0,
        "visionary": 0,
        "growth": 0
    }

    for contrib in contributions:
        contrib_type = CONTRIBUTION_TYPES.get(contrib["type"], {})
        category = contrib_type.get("category", "builder")
        points = contrib.get("points", 0)
        categories[category] += points

    # Total score
    total_score = sum(categories.values())

    # Specialization (highest category)
    specialization = max(categories.items(), key=lambda x: x[1])[0] if total_score > 0 else "none"

    return {
        "total_score": total_score,
        "categories": categories,
        "specialization": specialization,
        "contribution_count": len(contributions),
        "rank": get_rank_for_score(total_score)
    }

@app.route('/meritocracy/status', methods=['GET'])
def status():
    """Get system status"""
    data = load_data()

    return jsonify({
        "status": "operational",
        "total_builders": len(data["builders"]),
        "total_contributions": len(data["contributions"]),
        "contribution_types": list(CONTRIBUTION_TYPES.keys()),
        "ranks": RANKS
    })

@app.route('/meritocracy/builder/<builder_id>', methods=['GET'])
def get_builder(builder_id):
    """Get builder profile"""
    data = load_data()

    if builder_id not in data["builders"]:
        return jsonify({"error": "Builder not found"}), 404

    builder = data["builders"][builder_id]
    stats = calculate_builder_stats(builder)

    return jsonify({
        "id": builder_id,
        "name": builder.get("name", builder_id),
        "joined": builder.get("joined"),
        "stats": stats,
        "contributions": builder.get("contributions", [])
    })

@app.route('/meritocracy/builder/<builder_id>/register', methods=['POST'])
def register_builder(builder_id):
    """Register a new builder"""
    data = load_data()

    if builder_id in data["builders"]:
        return jsonify({"error": "Builder already exists"}), 400

    body = request.json

    data["builders"][builder_id] = {
        "name": body.get("name", builder_id),
        "joined": datetime.now().isoformat(),
        "contributions": []
    }

    save_data(data)

    return jsonify({
        "success": True,
        "builder_id": builder_id,
        "rank": get_rank_for_score(0)
    })

@app.route('/meritocracy/contribution', methods=['POST'])
def add_contribution():
    """Add a contribution"""
    data = load_data()
    body = request.json

    builder_id = body.get("builder_id")
    contrib_type = body.get("type")
    description = body.get("description", "")
    evidence = body.get("evidence", "")  # Link to PR, commit, etc.

    if not builder_id or not contrib_type:
        return jsonify({"error": "builder_id and type required"}), 400

    if contrib_type not in CONTRIBUTION_TYPES:
        return jsonify({"error": f"Unknown contribution type: {contrib_type}"}), 400

    # Ensure builder exists
    if builder_id not in data["builders"]:
        data["builders"][builder_id] = {
            "name": builder_id,
            "joined": datetime.now().isoformat(),
            "contributions": []
        }

    # Calculate points (can be modified by quality multiplier)
    base_points = CONTRIBUTION_TYPES[contrib_type]["points"]
    quality_multiplier = body.get("quality_multiplier", 1.0)  # 0.5 to 2.0
    points = int(base_points * quality_multiplier)

    # Create contribution record
    contribution = {
        "id": len(data["contributions"]) + 1,
        "builder_id": builder_id,
        "type": contrib_type,
        "description": description,
        "evidence": evidence,
        "points": points,
        "timestamp": datetime.now().isoformat()
    }

    # Add to global contributions
    data["contributions"].append(contribution)

    # Add to builder's contributions
    data["builders"][builder_id]["contributions"].append(contribution)

    save_data(data)

    # Get updated stats
    stats = calculate_builder_stats(data["builders"][builder_id])

    # Check for rank up
    old_rank = body.get("old_rank", 0)
    new_rank_threshold = stats["rank"]["threshold"]
    rank_up = new_rank_threshold > old_rank

    return jsonify({
        "success": True,
        "contribution": contribution,
        "builder_stats": stats,
        "rank_up": rank_up,
        "new_rank": stats["rank"] if rank_up else None
    })

@app.route('/meritocracy/leaderboard', methods=['GET'])
def leaderboard():
    """Get ranked leaderboard"""
    data = load_data()

    # Calculate stats for all builders
    builders_with_stats = []
    for builder_id, builder_data in data["builders"].items():
        stats = calculate_builder_stats(builder_data)
        builders_with_stats.append({
            "id": builder_id,
            "name": builder_data.get("name", builder_id),
            "score": stats["total_score"],
            "rank": stats["rank"],
            "specialization": stats["specialization"],
            "contribution_count": stats["contribution_count"]
        })

    # Sort by score
    builders_with_stats.sort(key=lambda x: x["score"], reverse=True)

    # Add rank position
    for i, builder in enumerate(builders_with_stats):
        builder["position"] = i + 1

    return jsonify({
        "leaderboard": builders_with_stats,
        "total_builders": len(builders_with_stats)
    })

@app.route('/meritocracy/contributions/recent', methods=['GET'])
def recent_contributions():
    """Get recent contributions"""
    data = load_data()
    limit = request.args.get('limit', 50, type=int)

    # Get recent contributions
    recent = data["contributions"][-limit:]
    recent.reverse()  # Most recent first

    return jsonify({
        "contributions": recent,
        "total": len(data["contributions"])
    })

@app.route('/meritocracy/stats', methods=['GET'])
def global_stats():
    """Get global statistics"""
    data = load_data()

    # Calculate category totals
    category_totals = {
        "builder": 0,
        "teacher": 0,
        "visionary": 0,
        "growth": 0
    }

    for contrib in data["contributions"]:
        contrib_type = CONTRIBUTION_TYPES.get(contrib["type"], {})
        category = contrib_type.get("category", "builder")
        category_totals[category] += contrib.get("points", 0)

    # Rank distribution
    rank_distribution = {}
    for builder_data in data["builders"].values():
        stats = calculate_builder_stats(builder_data)
        rank_name = stats["rank"]["name"]
        rank_distribution[rank_name] = rank_distribution.get(rank_name, 0) + 1

    return jsonify({
        "total_builders": len(data["builders"]),
        "total_contributions": len(data["contributions"]),
        "total_points": sum(category_totals.values()),
        "category_distribution": category_totals,
        "rank_distribution": rank_distribution
    })

if __name__ == "__main__":
    print("="*60)
    print("🏆 MERITOCRACY ENGINE STARTING")
    print("="*60)
    print("Best builders rise automatically based on contributions")
    print("No voting, no politics - pure output measurement")
    print("="*60)

    ensure_data_file()

    print("\n🚀 Starting Meritocracy API server on port 8000...")
    print("Status: http://localhost:8000/meritocracy/status")
    print("Leaderboard: http://localhost:8000/meritocracy/leaderboard")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=8000, debug=False)
