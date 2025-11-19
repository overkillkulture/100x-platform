"""
BETA APPROVAL SYSTEM - GATES CLOSED
Created: October 26, 2025
By: Claude Code (C1 Mechanic)

NEW SIGNUPS = EMAIL LIST ONLY
Commander manually approves → Beta access granted
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# File paths
PENDING_SIGNUPS_FILE = 'C:/Users/dwrek/100X_DEPLOYMENT/DATA/pending_signups.json'
APPROVED_BETA_TESTERS_FILE = 'C:/Users/dwrek/100X_DEPLOYMENT/DATA/approved_beta_testers.json'
REJECTED_SIGNUPS_FILE = 'C:/Users/dwrek/100X_DEPLOYMENT/DATA/rejected_signups.json'

# Ensure DATA directory exists
os.makedirs('C:/Users/dwrek/100X_DEPLOYMENT/DATA', exist_ok=True)

def load_json_file(filepath):
    """Load JSON file or return empty list"""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def save_json_file(filepath, data):
    """Save data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/signup', methods=['POST'])
def signup():
    """
    NEW SIGNUP FLOW - GATES CLOSED
    Everyone goes to pending list
    NO automatic beta access
    """
    data = request.json
    name = data.get('name', '')
    email = data.get('email', '')

    if not name or not email:
        return jsonify({'error': 'Name and email required'}), 400

    # Load pending signups
    pending = load_json_file(PENDING_SIGNUPS_FILE)

    # Check if already in system
    if any(s['email'] == email for s in pending):
        return jsonify({
            'status': 'already_pending',
            'message': 'You\'re already on the list! We\'ll notify you when approved.'
        })

    # Add to PENDING list (NOT approved)
    new_signup = {
        'name': name,
        'email': email,
        'timestamp': datetime.now().isoformat(),
        'status': 'pending',
        'source': 'signup-form'
    }

    pending.append(new_signup)
    save_json_file(PENDING_SIGNUPS_FILE, pending)

    return jsonify({
        'status': 'pending',
        'message': 'Thanks for signing up! You\'ve been added to the waitlist. We\'ll notify you when you get approved.'
    })

@app.route('/api/pending-signups', methods=['GET'])
def get_pending_signups():
    """Get all pending signups (for Commander approval interface)"""
    pending = load_json_file(PENDING_SIGNUPS_FILE)
    return jsonify({
        'pending': pending,
        'count': len(pending)
    })

@app.route('/api/approve-signup', methods=['POST'])
def approve_signup():
    """
    COMMANDER APPROVES A SIGNUP
    Moves from pending → approved beta testers
    """
    data = request.json
    email = data.get('email', '')

    if not email:
        return jsonify({'error': 'Email required'}), 400

    # Load all lists
    pending = load_json_file(PENDING_SIGNUPS_FILE)
    approved = load_json_file(APPROVED_BETA_TESTERS_FILE)

    # Find signup in pending
    signup = next((s for s in pending if s['email'] == email), None)

    if not signup:
        return jsonify({'error': 'Signup not found in pending list'}), 404

    # Move to approved
    signup['status'] = 'approved'
    signup['approved_date'] = datetime.now().isoformat()

    approved.append(signup)
    pending = [s for s in pending if s['email'] != email]

    # Save both files
    save_json_file(PENDING_SIGNUPS_FILE, pending)
    save_json_file(APPROVED_BETA_TESTERS_FILE, approved)

    return jsonify({
        'status': 'approved',
        'message': f'{email} has been approved for beta access!',
        'pending_remaining': len(pending)
    })

@app.route('/api/reject-signup', methods=['POST'])
def reject_signup():
    """
    COMMANDER REJECTS A SIGNUP
    Moves from pending → rejected
    """
    data = request.json
    email = data.get('email', '')
    reason = data.get('reason', 'No reason provided')

    if not email:
        return jsonify({'error': 'Email required'}), 400

    # Load all lists
    pending = load_json_file(PENDING_SIGNUPS_FILE)
    rejected = load_json_file(REJECTED_SIGNUPS_FILE)

    # Find signup in pending
    signup = next((s for s in pending if s['email'] == email), None)

    if not signup:
        return jsonify({'error': 'Signup not found in pending list'}), 404

    # Move to rejected
    signup['status'] = 'rejected'
    signup['rejected_date'] = datetime.now().isoformat()
    signup['rejection_reason'] = reason

    rejected.append(signup)
    pending = [s for s in pending if s['email'] != email]

    # Save both files
    save_json_file(PENDING_SIGNUPS_FILE, pending)
    save_json_file(REJECTED_SIGNUPS_FILE, rejected)

    return jsonify({
        'status': 'rejected',
        'message': f'{email} has been rejected',
        'pending_remaining': len(pending)
    })

@app.route('/api/check-access', methods=['POST'])
def check_access():
    """
    Check if email has beta access
    Used by login gates
    """
    data = request.json
    email = data.get('email', '')

    if not email:
        return jsonify({'error': 'Email required'}), 400

    # Check approved list
    approved = load_json_file(APPROVED_BETA_TESTERS_FILE)

    if any(s['email'] == email for s in approved):
        return jsonify({
            'access': 'granted',
            'status': 'approved_beta_tester'
        })

    # Check if pending
    pending = load_json_file(PENDING_SIGNUPS_FILE)
    if any(s['email'] == email for s in pending):
        return jsonify({
            'access': 'denied',
            'status': 'pending_approval',
            'message': 'Your signup is pending approval. Check your email soon!'
        })

    # Not in system
    return jsonify({
        'access': 'denied',
        'status': 'not_registered',
        'message': 'Email not found. Please sign up first.'
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get approval system statistics"""
    pending = load_json_file(PENDING_SIGNUPS_FILE)
    approved = load_json_file(APPROVED_BETA_TESTERS_FILE)
    rejected = load_json_file(REJECTED_SIGNUPS_FILE)

    return jsonify({
        'pending_count': len(pending),
        'approved_count': len(approved),
        'rejected_count': len(rejected),
        'total_signups': len(pending) + len(approved) + len(rejected),
        'approval_rate': f"{len(approved) / max(1, len(approved) + len(rejected)) * 100:.1f}%"
    })

if __name__ == '__main__':
    print("\n🚪 BETA APPROVAL SYSTEM - GATES CLOSED 🚪")
    print("=" * 60)
    print("Status: New signups require Commander approval")
    print("Mode: DESTROYER FILTER PROTECTION")
    print("=" * 60)
    print("\nEndpoints:")
    print("  POST /api/signup - Add to pending list (NO auto-approval)")
    print("  GET  /api/pending-signups - View pending signups")
    print("  POST /api/approve-signup - Approve pending signup")
    print("  POST /api/reject-signup - Reject pending signup")
    print("  POST /api/check-access - Check if email has beta access")
    print("  GET  /api/stats - View approval statistics")
    print("\n🔒 GATES CLOSED - DESTROYER FILTER ACTIVE 🔒\n")

    app.run(host='0.0.0.0', port=8010, debug=True)
