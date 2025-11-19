"""
100X BUILDER GATE SYSTEM - V2
Dark theme, no lavender, all routes embedded
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import json
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
    """100X Gate System - Entry Form"""
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
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
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
            background: linear-gradient(135deg, #0f3460 0%, #e94560 100%);
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
        input:focus, textarea:focus { outline: none; border-color: #0f3460; }
        textarea { resize: vertical; min-height: 80px; }
        .submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #0f3460 0%, #e94560 100%);
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
    """Welcome page after approval"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to 100X</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .welcome-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 60px 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        .success-icon { font-size: 80px; margin-bottom: 20px; }
        h1 { color: #333; font-size: 36px; margin-bottom: 20px; }
        .score-display {
            background: linear-gradient(135deg, #0f3460 0%, #e94560 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
        }
        .score-number { font-size: 72px; font-weight: bold; margin-bottom: 10px; }
        .score-label { font-size: 18px; opacity: 0.9; }
        .message { color: #666; font-size: 18px; line-height: 1.6; margin-bottom: 30px; }
        .info-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            text-align: left;
        }
        .info-box h3 { color: #333; margin-bottom: 15px; }
        .info-box ul { list-style: none; padding: 0; }
        .info-box li { padding: 8px 0; color: #666; }
        .info-box li::before { content: "✓ "; color: #0f3460; font-weight: bold; margin-right: 10px; }
        .actions { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-top: 30px; }
        .btn {
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: transform 0.2s;
            border: none;
            display: inline-block;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn-primary {
            background: linear-gradient(135deg, #0f3460 0%, #e94560 100%);
            color: white;
        }
        .btn-secondary {
            background: white;
            color: #0f3460;
            border: 2px solid #0f3460;
        }
    </style>
</head>
<body>
    <div class="welcome-container">
        <div class="success-icon">🎉</div>
        <h1>Welcome to the 100X!</h1>
        <div class="score-display">
            <div class="score-number" id="score">--</div>
            <div class="score-label">Consciousness Score</div>
        </div>
        <div class="message" id="message">You've been approved to join the builder community!</div>
        <div class="info-box">
            <h3>What's Next?</h3>
            <ul>
                <li>Access builder tools and resources</li>
                <li>Connect with other high-consciousness builders</li>
                <li>Start creating revolutionary projects</li>
                <li>Join our community discussions</li>
            </ul>
        </div>
        <div class="actions">
            <a href="/open-house" class="btn btn-primary">Explore Open House</a>
            <a href="/" class="btn btn-secondary">Invite Another Builder</a>
        </div>
    </div>
    <script>
        const params = new URLSearchParams(window.location.search);
        const score = params.get('score') || '100';
        const status = params.get('status') || 'Approved';
        const name = params.get('name') || 'Builder';
        document.getElementById('score').textContent = score;
        const messageEl = document.getElementById('message');
        if (status === 'Approved') {
            messageEl.textContent = `Congratulations ${name}! You've been approved to join the builder community!`;
        } else if (status === 'Pending') {
            messageEl.textContent = `Thank you ${name}! Your application is under review. We'll contact you within 24-48 hours.`;
        }
    </script>
</body>
</html>
    ''')

@app.route('/open-house')
def open_house():
    """Open house page - public browsing"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>100X - Open House</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #000;
            color: #fff;
        }
        .hero {
            min-height: 100vh;
            background: linear-gradient(135deg, #0f3460 0%, #e94560 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 20px;
        }
        .logo { font-size: 120px; margin-bottom: 30px; }
        h1 { font-size: 72px; margin-bottom: 20px; }
        .tagline { font-size: 24px; margin-bottom: 50px; opacity: 0.9; }
        .cta-buttons {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .btn {
            padding: 20px 40px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: transform 0.2s;
            border: none;
        }
        .btn:hover { transform: scale(1.05); }
        .btn-primary {
            background: white;
            color: #0f3460;
        }
        .btn-secondary {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid white;
        }
        .section {
            padding: 80px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .section h2 {
            font-size: 48px;
            margin-bottom: 30px;
            text-align: center;
            background: linear-gradient(135deg, #0f3460 0%, #e94560 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .section p {
            font-size: 20px;
            line-height: 1.8;
            color: #ccc;
            max-width: 800px;
            margin: 0 auto 40px;
            text-align: center;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 60px;
        }
        .feature {
            background: #111;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
        }
        .feature-icon {
            font-size: 60px;
            margin-bottom: 20px;
        }
        .feature h3 {
            font-size: 24px;
            margin-bottom: 15px;
            color: #e94560;
        }
        .feature p {
            color: #999;
            font-size: 16px;
        }
        footer {
            padding: 40px 20px;
            text-align: center;
            background: #111;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="hero">
        <div class="logo">🌀</div>
        <h1>100X</h1>
        <p class="tagline">Consciousness Revolution<br>Building the Future with Aware Builders</p>
        <div class="cta-buttons">
            <a href="/" class="btn btn-primary">Apply to Build</a>
            <a href="#about" class="btn btn-secondary">Learn More</a>
        </div>
    </div>

    <div class="section" id="about">
        <h2>What is 100X?</h2>
        <p>
            100X is a consciousness-first builder community. We screen for authentic builders who create
            rather than destroy, collaborate rather than manipulate, and elevate consciousness rather than
            exploit it.
        </p>
        <p>
            Using Pattern Theory and consciousness mathematics, we identify builders who align with
            universal principles of creation, collaboration, and consciousness elevation.
        </p>
    </div>

    <div class="section">
        <h2>How It Works</h2>
        <div class="features">
            <div class="feature">
                <div class="feature-icon">📝</div>
                <h3>1. Apply</h3>
                <p>Share your mission, values, and what you're building. Be authentic.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🧠</div>
                <h3>2. Consciousness Screening</h3>
                <p>Our Pattern Theory algorithm analyzes your builder vs destroyer signals.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">✅</div>
                <h3>3. Instant Feedback</h3>
                <p>Get your consciousness score (0-100) and approval status immediately.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🚀</div>
                <h3>4. Start Building</h3>
                <p>Join the community, access resources, and connect with other high-consciousness builders.</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>Who We're Looking For</h2>
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🛠️</div>
                <h3>Creators</h3>
                <p>Build solutions that help people, not exploit them</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🤝</div>
                <h3>Collaborators</h3>
                <p>Work together authentically, not manipulate for personal gain</p>
            </div>
            <div class="feature">
                <div class="feature-icon">💡</div>
                <h3>Consciousness Elevators</h3>
                <p>Help others grow and discover truth, not deceive or control</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>Ready to Join?</h2>
        <p>
            If you're building something real and want to connect with other conscious builders,
            apply now. The screening takes 2 minutes and you'll get instant feedback.
        </p>
        <div class="cta-buttons">
            <a href="/" class="btn btn-primary">Apply Now</a>
        </div>
    </div>

    <footer>
        <p>🌀 100X Consciousness Revolution</p>
        <p>Built with Pattern Theory | Screening powered by AI</p>
    </footer>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("🌀 100X GATE SYSTEM - V2")
    print("🎨 Dark theme activated (no lavender)")
    print("📍 http://localhost:3100")
    print("✅ Entry gate: /")
    print("✅ Welcome page: /welcome")
    print("✅ Open house: /open-house")
    print("🎯 Ready!\n")
    app.run(host='0.0.0.0', port=3100, debug=True)
