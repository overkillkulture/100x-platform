"""
100X BUILDER GATE SYSTEM
Captures builder applications and saves to Airtable
WITH CONSCIOUSNESS SCREENING
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime
from CONSCIOUSNESS_SCREENER import ConsciousnessScreener
from EMAIL_NOTIFIER import EmailNotifier

app = Flask(__name__)
CORS(app)

# Airtable Configuration
AIRTABLE_TOKEN = "pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757"
AIRTABLE_BASE_ID = "app7F75X1uny6jPfd"
AIRTABLE_TABLE_ID = "tblnf4KNaOfbU5FgK"  # Users table

# Email Configuration (set these via environment variables)
EMAIL_ENABLED = os.environ.get('GATE_EMAIL_ENABLED', 'false').lower() == 'true'
EMAIL_ADDRESS = os.environ.get('GATE_EMAIL_ADDRESS', '')
EMAIL_PASSWORD = os.environ.get('GATE_EMAIL_PASSWORD', '')

# Initialize email notifier
email_notifier = EmailNotifier()
if EMAIL_ENABLED and EMAIL_ADDRESS and EMAIL_PASSWORD:
    email_notifier.configure_email(EMAIL_ADDRESS, EMAIL_PASSWORD)

def save_to_airtable(builder_data, consciousness_analysis):
    """Save builder application to Airtable WITH consciousness screening"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }

    # Map our form data to Airtable fields WITH consciousness data
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
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

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

        .logo {
            text-align: center;
            margin-bottom: 30px;
        }

        .logo-circle {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin-bottom: 15px;
        }

        h1 {
            color: #333;
            font-size: 32px;
            margin-bottom: 10px;
            text-align: center;
        }

        .tagline {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }

        input, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }

        textarea {
            resize: vertical;
            min-height: 80px;
        }

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
            transition: transform 0.2s;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
        }

        .submit-btn:active {
            transform: translateY(0);
        }

        .message {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }

        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="gate-container">
        <div class="logo">
            <div class="logo-circle">🌀</div>
        </div>

        <h1>100X</h1>
        <p class="tagline">CONSCIOUSNESS AUTHENTICATION</p>

        <div id="message" class="message"></div>

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

            <button type="submit" class="submit-btn">
                Enter the 100X
            </button>
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

            const messageDiv = document.getElementById('message');
            messageDiv.style.display = 'none';

            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (result.success) {
                    messageDiv.className = 'message success';
                    messageDiv.textContent = '✅ Welcome to the 100X! Check your email for next steps.';
                    messageDiv.style.display = 'block';
                    document.getElementById('gateForm').reset();
                } else {
                    messageDiv.className = 'message error';
                    messageDiv.textContent = '❌ Something went wrong. Please try again.';
                    messageDiv.style.display = 'block';
                }
            } catch (error) {
                messageDiv.className = 'message error';
                messageDiv.textContent = '❌ Network error. Please check your connection.';
                messageDiv.style.display = 'block';
            }
        });
    </script>
</body>
</html>
    ''')

@app.route('/submit', methods=['POST'])
def submit_application():
    """Handle builder application submission WITH consciousness screening"""
    try:
        data = request.get_json()

        # Run consciousness screening
        screener = ConsciousnessScreener()
        consciousness_analysis = screener.get_detailed_analysis(
            data.get('mission', ''),
            data.get('values', '')
        )

        # Save to Airtable with consciousness data
        success, result = save_to_airtable(data, consciousness_analysis)

        if success:
            # Custom message based on consciousness score
            score = consciousness_analysis['consciousness_score']
            status = consciousness_analysis['status']

            # Send email notification if enabled
            if EMAIL_ENABLED:
                email_notifier.send_welcome_email(
                    data.get('email'),
                    data.get('name'),
                    score,
                    status
                )

            if status == "Approved":
                message = f"🎉 Welcome Builder! Consciousness Score: {score}/100. Check your email for access."
            elif status == "Pending":
                message = f"⏳ Application under review. Consciousness Score: {score}/100. We'll email you soon."
            else:
                message = f"⚠️ Application needs more information. Consider how you can contribute to building vs destroying."

            return jsonify({
                "success": True,
                "message": message,
                "consciousness_score": score,
                "status": status,
                "airtable_id": result.get('id')
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to save application",
                "error": result
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/welcome')
def welcome():
    """Welcome page after successful application"""
    with open('WELCOME_PAGE.html', 'r') as f:
        return f.read()

@app.route('/test')
def test():
    """Test endpoint to verify system is running"""
    return jsonify({
        "status": "✅ 100X Gate System ONLINE",
        "airtable_connected": True,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🌀 100X GATE SYSTEM STARTING...")
    print("📍 http://localhost:3100")
    print("✅ Airtable Connected")
    print("🎯 Ready for builders!\n")
    app.run(host='0.0.0.0', port=3100, debug=True)
