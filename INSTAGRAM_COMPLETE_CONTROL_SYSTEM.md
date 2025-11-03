# 📷 INSTAGRAM COMPLETE CONTROL SYSTEM 📷

**Goal**: See who's online on Instagram, send them DMs from Neighborhood Watch

---

## 🎯 TWO APPROACHES

### Approach 1: Official Instagram API (SAFE)
**Pros**:
- ✅ FREE, official Meta API
- ✅ No risk of account ban
- ✅ Scales to unlimited messages
- ✅ Can handle media (images, videos)

**Cons**:
- ❌ Requires Business Account + Facebook Page
- ❌ Can only REPLY to messages (customer initiates first)
- ❌ Cannot check if someone is "online"
- ❌ Cannot initiate DMs to cold contacts

**Best for**: Customer service, responding to inbound messages

---

### Approach 2: Browser Automation (POWERFUL BUT RISKY)
**Pros**:
- ✅ Can message ANYONE
- ✅ Can check online status
- ✅ Can see "Active Now" indicator
- ✅ Full Instagram feature access

**Cons**:
- ❌ Violates Instagram ToS
- ❌ Risk of account ban
- ❌ Requires careful rate limiting (10-20 DMs/hour max)
- ❌ Needs session management, 2FA handling

**Best for**: Personal use, small-scale messaging, checking status

---

## 🚀 RECOMMENDED STRATEGY: USE BOTH

**For checking if someone is online**:
→ Use Browser Automation (Approach 2)

**For sending messages at scale**:
→ Use Official API (Approach 1) when possible
→ Use Browser Automation as backup

---

## 📋 SETUP GUIDE: APPROACH 1 (Official API)

### Step 1: Convert to Business Account
1. Open Instagram app
2. Settings → Account → Switch to Professional Account
3. Choose "Business"
4. Connect to Facebook Page (create one if needed)

### Step 2: Add to Meta Business Manager
1. Go to: https://business.facebook.com
2. Business Settings → Accounts → Instagram Accounts
3. Add your Instagram Business Account

### Step 3: Create Facebook App
1. Go to: https://developers.facebook.com
2. My Apps → Create App
3. Select "Business" type
4. Add Instagram Graph API

### Step 4: Get Access Token
```python
import requests

# You'll get these from Facebook Developer Console
APP_ID = 'your_app_id'
APP_SECRET = 'your_app_secret'
ACCESS_TOKEN = 'your_long_lived_token'

# Test the connection
response = requests.get(
    f'https://graph.facebook.com/v18.0/me/accounts',
    params={'access_token': ACCESS_TOKEN}
)
print(response.json())
```

### Step 5: Receive and Reply to DMs
```python
def reply_to_instagram_dm(message_id, reply_text):
    url = f'https://graph.facebook.com/v18.0/{message_id}/messages'

    response = requests.post(url, json={
        'recipient': {'id': message_id},
        'message': {'text': reply_text},
        'access_token': ACCESS_TOKEN
    })

    return response.json()

# Usage
reply_to_instagram_dm('message_12345', 'Thanks for reaching out!')
```

**Limitation**: Customer must message YOU first!

---

## 📋 SETUP GUIDE: APPROACH 2 (Browser Automation)

### Step 1: Install Playwright
```bash
pip install playwright
playwright install chromium
```

### Step 2: Instagram Login Script
```python
from playwright.sync_api import sync_playwright
import time

def login_instagram(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to Instagram
        page.goto('https://www.instagram.com/')
        time.sleep(3)

        # Login
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        time.sleep(5)

        # Save cookies (session)
        context = page.context
        context.storage_state(path='instagram_session.json')

        print("✅ Logged in! Session saved.")
        browser.close()

# Run once to save session
login_instagram('your_username', 'your_password')
```

### Step 3: Check If Someone Is Online
```python
def check_instagram_online(username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state='instagram_session.json')
        page = context.new_page()

        # Go to DMs
        page.goto('https://www.instagram.com/direct/inbox/')
        time.sleep(3)

        # Search for user
        page.fill('input[placeholder="Search"]', username)
        time.sleep(2)

        # Click on user
        page.click(f'text={username}')
        time.sleep(2)

        # Check for "Active now" indicator
        try:
            active_indicator = page.locator('text=Active now').count()
            is_online = active_indicator > 0

            if is_online:
                print(f"🟢 {username} is ONLINE")
            else:
                # Try to get "Active X ago"
                last_active = page.locator('[class*="active"]').inner_text()
                print(f"⚪ {username} was active: {last_active}")

            return is_online
        except:
            print(f"❓ Could not determine status for {username}")
            return None
        finally:
            browser.close()
```

### Step 4: Send Instagram DM
```python
def send_instagram_dm(username, message):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state='instagram_session.json')
        page = context.new_page()

        # Go to DMs
        page.goto('https://www.instagram.com/direct/inbox/')
        time.sleep(3)

        # Search for user
        page.fill('input[placeholder="Search"]', username)
        time.sleep(2)

        # Click on user
        page.click(f'text={username}')
        time.sleep(2)

        # Type and send message
        page.fill('textarea[placeholder="Message..."]', message)
        page.click('button:has-text("Send")')
        time.sleep(2)

        print(f"✅ Message sent to {username}")
        browser.close()
```

### Step 5: Safety Limits (CRITICAL!)
```python
import time
from datetime import datetime, timedelta

class InstagramSafetyLimiter:
    def __init__(self):
        self.message_log = []
        self.max_per_hour = 15  # Conservative limit
        self.min_delay = 60  # 60 seconds between messages

    def can_send_message(self):
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)

        # Remove old messages from log
        self.message_log = [t for t in self.message_log if t > one_hour_ago]

        if len(self.message_log) >= self.max_per_hour:
            print(f"⚠️  RATE LIMIT: {self.max_per_hour} messages sent in last hour")
            return False

        return True

    def log_message(self):
        self.message_log.append(datetime.now())

    def wait_between_messages(self):
        time.sleep(self.min_delay)

# Usage
limiter = InstagramSafetyLimiter()

if limiter.can_send_message():
    send_instagram_dm('joshua', 'Hey, saw you online!')
    limiter.log_message()
    limiter.wait_between_messages()
else:
    print("Too many messages sent recently. Waiting...")
```

---

## 🏘️ INTEGRATION: NEIGHBORHOOD WATCH

### Updated Neighborhood Watch Code
Add this to fetch Instagram online status:

```python
# Flask endpoint for Instagram status check
@app.route('/api/instagram/status/<username>', methods=['GET'])
def get_instagram_status(username):
    # Check if user is online via browser automation
    is_online = check_instagram_online(username)

    return jsonify({
        'username': username,
        'online': is_online,
        'timestamp': datetime.now().isoformat()
    })
```

Add to Neighborhood Watch frontend:

```javascript
async function updateInstagramStatus(person) {
    try {
        const response = await fetch(`http://localhost:6000/api/instagram/status/${person.instagram_username}`);
        const data = await response.json();

        person.channels.instagram.active = data.online;
        person.channels.instagram.status = data.online ? 'Active now' : 'Offline';
    } catch (err) {
        console.log('Instagram status check failed:', err);
    }
}
```

---

## ⚠️ IMPORTANT WARNINGS

### Using Browser Automation:
1. **Start slow**: 5-10 messages per day initially
2. **Vary timing**: Don't send at exact intervals
3. **Use human-like delays**: 30-120 seconds between actions
4. **Session management**: Re-login weekly to avoid detection
5. **2FA ready**: Have backup codes ready
6. **Backup account**: Don't use your main account

### Instagram Will Ban You If:
- ❌ Sending 50+ DMs per hour
- ❌ Copy-paste same message to everyone
- ❌ Messaging people who don't follow you (high spam rate)
- ❌ Running 24/7 without breaks
- ❌ Multiple accounts from same IP

### Safe Practices:
- ✅ Limit to 15-20 messages per hour
- ✅ Personalize each message
- ✅ Message followers or people you know
- ✅ Add random 1-5 minute breaks
- ✅ Use residential IP (not datacenter/VPN)

---

## 🎯 RECOMMENDED SETUP FOR YOUR USE CASE

**For Joshua and your team**:

1. **Use Browser Automation** (Approach 2)
   - Check if they're online
   - Send occasional DMs
   - Perfect for 5-10 people

2. **Set up Official API** (Approach 1) as backup
   - For when you scale to 50+ people
   - Customer service bot
   - Automated responses

3. **Integrate into Neighborhood Watch**
   - Real-time online status
   - One-click DM from the dashboard
   - Multi-channel view (website + Instagram + SMS)

---

## 📁 FILES TO CREATE

**For Browser Automation**:
1. `INSTAGRAM_AUTOMATION.py` - Login, check status, send DMs
2. `INSTAGRAM_SAFETY_LIMITER.py` - Rate limiting
3. `instagram_session.json` - Saved session (auto-generated)

**For Official API**:
1. `INSTAGRAM_GRAPH_API.py` - Official API integration
2. `INSTAGRAM_WEBHOOK_RECEIVER.py` - Receive inbound DMs

**For Integration**:
1. Update `LOCAL_NERVE_COLLECTOR.py` - Add Instagram endpoints
2. Update `NEIGHBORHOOD_WATCH.html` - Instagram status display

---

## 🚀 NEXT STEPS

1. **Choose your approach** (I recommend: Both!)
2. **For Browser Automation**: Run Instagram login script, save session
3. **For Official API**: Convert to Business Account, create Facebook App
4. **Test with one person**: Check status, send test DM
5. **Integrate into Neighborhood Watch**: See online status live

**Want me to build the complete Instagram automation system now?** 📷🔥
