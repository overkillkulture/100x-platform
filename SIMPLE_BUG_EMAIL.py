"""
DEAD SIMPLE BUG EMAILER
Runs locally, receives bugs via HTTP, emails them immediately
No Netlify, no complicated setup - just works

USAGE: python SIMPLE_BUG_EMAIL.py
Then visit: http://localhost:8877
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

GMAIL_USER = "darrick.preble@gmail.com"
GMAIL_PASS = os.getenv("GMAIL_APP_PASSWORD", "gzzvemuxppfnjsup")

@app.route('/submit-bug', methods=['POST', 'OPTIONS'])
def submit_bug():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.json
        message = data.get('message', 'No message')

        # Email it
        msg = MIMEText(f"""
NEW BUG REPORT FROM BETA TESTER

Message: {message}

Time: {datetime.now()}
Page: {data.get('page', 'Unknown')}
        """)

        msg['Subject'] = f'🐛 BUG REPORT: {message[:50]}'
        msg['From'] = GMAIL_USER
        msg['To'] = GMAIL_USER

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print(f"✅ EMAILED: {message}")

        return jsonify({'success': True, 'message': 'Emailed!'})

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Bug Reporter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; padding:40px; background:#000; color:#0f0; font-family:monospace; min-height:100vh;">
    <div style="max-width:600px; margin:0 auto;">
        <h1 style="color:#0f0; text-align:center;">🐛 BUG REPORTER 🐛</h1>
        <p style="text-align:center; margin-bottom:30px;">Type and press Enter - emails instantly</p>

        <input type="text" id="msg" placeholder="Type your message..." style="
            width:100%;
            padding:20px;
            font-size:18px;
            background:#111;
            border:3px solid #0f0;
            color:#0f0;
            border-radius:10px;
            font-family:monospace;
            box-sizing:border-box;
        ">

        <div id="status" style="margin-top:20px; text-align:center; font-size:24px; color:#0f0;"></div>

        <div style="margin-top:40px; padding:20px; background:#111; border:2px solid #333; border-radius:10px;">
            <h3 style="margin-top:0;">Sent Messages:</h3>
            <div id="history" style="font-size:14px; line-height:1.8;"></div>
        </div>
    </div>

    <script>
    const input = document.getElementById('msg');
    const status = document.getElementById('status');
    const history = document.getElementById('history');

    function showHistory() {
        const msgs = localStorage.getItem('sent_bugs') || '';
        history.innerHTML = msgs.split('\\n').filter(m => m.trim()).map(m =>
            '<div>' + m + '</div>'
        ).join('') || '<div style="color:#666;">No messages yet</div>';
    }
    showHistory();

    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const msg = this.value.trim();
            if (!msg) return;

            status.textContent = '⏳ Sending...';
            status.style.color = 'yellow';

            fetch('http://localhost:8877/submit-bug', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg, page: 'local'})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    status.textContent = '✅ EMAILED!';
                    status.style.color = '#0f0';

                    const time = new Date().toLocaleTimeString();
                    const entry = `[${time}] ${msg}`;
                    const all = localStorage.getItem('sent_bugs') || '';
                    localStorage.setItem('sent_bugs', all + entry + '\\n');

                    input.value = '';
                    showHistory();
                } else {
                    status.textContent = '❌ FAILED: ' + data.error;
                    status.style.color = 'red';
                }
            })
            .catch(err => {
                status.textContent = '❌ ERROR: ' + err;
                status.style.color = 'red';
            });

            setTimeout(() => status.textContent = '', 3000);
        }
    });

    input.focus();
    </script>
</body>
</html>
    '''

if __name__ == '__main__':
    print("🐛 BUG EMAIL SERVER STARTING...")
    print("📧 Will email bugs to: darrick.preble@gmail.com")
    print("🌐 Open: http://localhost:8877")
    print("")
    app.run(host='0.0.0.0', port=8877, debug=False)
