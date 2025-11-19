"""
100X BUILDER GATE SYSTEM - WITH INSTANT ACCESS
Captures builder applications, runs consciousness screening, and gives IMMEDIATE access
"""

from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime
from CONSCIOUSNESS_SCREENER import ConsciousnessScreener

app = Flask(__name__)
CORS(app)

# Airtable Configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = "app7F75X1uny6jPfd"
AIRTABLE_TABLE_ID = "tblnf4KNaOfbU5FgK"

def save_to_airtable(builder_data, consciousness_analysis):
    """Save builder application to Airtable WITH consciousness screening"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }

    airtable_record = {
        "fields": {
            "Full Name": builder_data.get("name", ""),
            "Email Address": builder_data.get("email", ""),
            "Phone Number": builder_data.get("phone", ""),
            "Mission": builder_data.get("mission", ""),
            "Values": builder_data.get("values", ""),
            "Status": consciousness_analysis.get("status", "Pending"),
            "Consciousness Score": consciousness_analysis.get("consciousness_score", 0)
        }
    }

    try:
        response = requests.post(url, headers=headers, json=airtable_record)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

@app.route('/')
def home():
    """100X Gate System Interface"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>100X Builder Gate</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .gate-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo-circle {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            color: white;
            margin-bottom: 15px;
        }
        h1 { color: #333; font-size: 32px; margin-bottom: 10px; text-align: center; }
        .tagline { color: #666; text-align: center; margin-bottom: 30px; font-size: 14px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #333; font-weight: 600; font-size: 14px; }
        input, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
        }
        input:focus, textarea:focus { outline: none; border-color: #667eea; }
        textarea { resize: vertical; min-height: 80px; }
        .submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
        .submit-btn:hover { transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="gate-container">
        <div class="logo"><div class="logo-circle">🌀</div></div>
        <h1>100X</h1>
        <p class="tagline">CONSCIOUSNESS AUTHENTICATION</p>
        <form id="gateForm">
            <div class="form-group">
                <label for="name">Full Name</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="email">Email Address</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="phone">Phone Number</label>
                <input type="tel" id="phone" name="phone">
            </div>
            <div class="form-group">
                <label for="mission">Your Mission (Why are you building?)</label>
                <textarea id="mission" name="mission" required></textarea>
            </div>
            <div class="form-group">
                <label for="values">Your Values (What matters to you?)</label>
                <textarea id="values" name="values" required></textarea>
            </div>
            <button type="submit" class="submit-btn">Enter the 100X</button>
        </form>
    </div>
    <script>
        document.getElementById('gateForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                mission: document.getElementById('mission').value,
                values: document.getElementById('values').value
            };
            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                const result = await response.json();
                if (result.success) {
                    // REDIRECT TO WELCOME PAGE
                    window.location.href = `/welcome?score=${result.consciousness_score}&status=${result.status}&name=${encodeURIComponent(formData.name)}`;
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        });
    </script>
</body>
</html>
    ''')

@app.route('/submit', methods=['POST'])
def submit_application():
    """Handle builder application WITH consciousness screening"""
    try:
        data = request.get_json()

        screener = ConsciousnessScreener()
        consciousness_analysis = screener.get_detailed_analysis(
            data.get('mission', ''),
            data.get('values', '')
        )

        success, result = save_to_airtable(data, consciousness_analysis)

        if success:
            return jsonify({
                "success": True,
                "consciousness_score": consciousness_analysis['consciousness_score'],
                "status": consciousness_analysis['status'],
                "airtable_id": result.get('id')
            })
        else:
            return jsonify({"success": False, "message": "Failed to save"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/welcome')
def welcome():
    """Welcome page - loads WELCOME_PAGE.html"""
    file_path = os.path.join(os.path.dirname(__file__), 'WELCOME_PAGE.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/open-house')
def open_house():
    """Open house page - loads OPEN_HOUSE.html"""
    file_path = os.path.join(os.path.dirname(__file__), 'OPEN_HOUSE.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    print("🌀 100X GATE SYSTEM STARTING...")
    print("📍 http://localhost:3100")
    print("✅ Immediate access enabled - redirects to welcome page")
    print("🎯 Ready for builders!\n")
    app.run(host='0.0.0.0', port=3100, debug=True)
