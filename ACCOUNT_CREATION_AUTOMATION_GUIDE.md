# 🤖 SOCIAL MEDIA ACCOUNT CREATION AUTOMATION - USER GUIDE

**Script:** `ACCOUNT_SETUP_AUTOMATION.py`
**Purpose:** Automate creation of 300+ social media accounts
**Time Savings:** 150 hours → 3 days (50x faster)
**Status:** ✅ Ready for use (demo mode, needs full implementation)

---

## 📋 WHAT THIS SCRIPT DOES

**The Problem:**
- Need 300+ social media accounts for Social Superpower Suite
- Manual creation: 30 minutes per account × 300 = 150 hours (2 months of work)
- Repetitive, soul-crushing, error-prone

**The Solution:**
- Browser automation using Playwright
- Anti-detection techniques (proxies, fingerprint spoofing)
- Automatic email/SMS verification
- Runs 24/7, creates accounts while you sleep
- 3 days to 300 accounts (fully automated)

**Platforms Supported:**
- ✅ Instagram
- ✅ TikTok
- ✅ YouTube
- ⏳ Twitter/X (coming soon)
- ⏳ Facebook (coming soon)
- ⏳ LinkedIn (coming soon)

---

## 🚀 QUICK START (Demo Mode)

### Step 1: Run the Script
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
python ACCOUNT_SETUP_AUTOMATION.py
```

### Step 2: Enter Details
```
How many account sets to create? 10
Platforms: instagram,tiktok,youtube
```

### Step 3: Watch It Work
The script will:
- Generate random account details
- Simulate account creation
- Save credentials to JSON file
- Display progress in real-time

### Output:
- **File:** `accounts_created.json`
- **Contains:** Username, email, password, profile URL for each account
- **Format:** JSON (easy to import into other tools)

---

## 📊 DEMO MODE vs PRODUCTION MODE

**Current Status:** DEMO MODE
- Simulates account creation
- Doesn't actually create accounts
- Shows you how it will work
- Safe to test, no cost

**Production Mode** (Requires Setup):
- Actually creates accounts
- Uses browser automation (Playwright)
- Requires:
  - Playwright installation
  - Email verification service
  - SMS verification service
  - CAPTCHA solving service
  - Residential proxy network

**Cost to Enable Production:**
- ~$0.50-1.00 per account
- $150-300 total for 300 accounts
- One-time cost

---

## 🛠️ FULL IMPLEMENTATION SETUP

### Prerequisites:

#### 1. Install Playwright (Browser Automation)
```bash
pip install playwright
playwright install chromium
```

#### 2. Install Anti-Detection
```bash
pip install playwright-stealth
# OR
pip install undetected-playwright
```

#### 3. Setup Email Verification Service
**Options:**
- **temp-mail.org** (free, limited)
- **Gmail API** (requires Google account setup)
- **Mailinator** (free API tier)

**Recommended:** temp-mail.org for MVP, Gmail API for scale

#### 4. Setup SMS Verification Service
**Options:**
- **sms-activate.org** ($0.10-0.50 per SMS)
- **receive-sms-online.com** (free, unreliable)
- **Twilio** ($0.75 per SMS, reliable)

**Recommended:** sms-activate.org ($0.10-0.50 per verification)

#### 5. Setup CAPTCHA Solving
**Options:**
- **2captcha.com** ($1 per 1000 solves)
- **Anti-Captcha** ($1 per 1000 solves)
- Manual solving (slow but free)

**Recommended:** 2captcha.com ($1 per 1000 = $0.30 for 300 accounts)

#### 6. Setup Residential Proxies
**Why Needed:** Avoid IP bans from creating multiple accounts
**Options:**
- **Bright Data** ($50-100/month, 10GB)
- **Smartproxy** ($50/month)
- **Oxylabs** ($100/month)

**Recommended:** Bright Data for reliability

---

## 💰 COST BREAKDOWN

**For 300 Accounts:**

| Service | Cost per Account | Total (300 accounts) |
|---------|------------------|---------------------|
| Email verification | Free-$0.02 | $0-6 |
| SMS verification | $0.10-0.50 | $30-150 |
| CAPTCHA solving | $0.001 | $0.30 |
| Proxies | $0.20 | $60 |
| **TOTAL** | **$0.30-0.72** | **$90-216** |

**Time Investment:**
- Setup services: 2-3 hours (one-time)
- Configure script: 1 hour (one-time)
- Run script: 3 days (automated, no supervision)

**ROI:**
- Manual: 150 hours × $25/hour = $3,750
- Automated: $216 + 3 hours × $25 = $291
- **Savings: $3,459 (92% reduction)**

---

## 🔧 HOW TO UPGRADE TO PRODUCTION MODE

### Step 1: Uncomment Production Code

In `ACCOUNT_SETUP_AUTOMATION.py`, find these sections:
```python
# PLACEHOLDER - would use playwright.async_api in full implementation
# from playwright.async_api import async_playwright
```

**Change to:**
```python
from playwright.async_api import async_playwright
```

### Step 2: Implement Real Account Creation

Find the `create_instagram_account()` function and replace simulation with:
```python
def create_instagram_account(self, account_details: Dict) -> Dict:
    """Create Instagram account using browser automation"""

    async with async_playwright() as p:
        # Launch browser with anti-detection
        browser = await p.chromium.launch(
            headless=False,  # Set to True for background
            proxy={
                'server': 'http://proxy-server.com:8080',
                'username': 'your-username',
                'password': 'your-password'
            }
        )

        page = await browser.new_page()

        # Go to signup page
        await page.goto('https://www.instagram.com/accounts/emailsignup/')

        # Fill in form
        await page.fill('input[name="emailOrPhone"]', account_details['email'])
        await page.fill('input[name="fullName"]', f"{account_details['first_name']} {account_details['last_name']}")
        await page.fill('input[name="username"]', account_details['username'])
        await page.fill('input[name="password"]', account_details['password'])

        # Submit
        await page.click('button[type="submit"]')

        # Handle SMS verification
        await page.wait_for_selector('input[name="confirmationCode"]')
        sms_code = await self.get_sms_code(account_details['phone'])
        await page.fill('input[name="confirmationCode"]', sms_code)

        # Save cookies
        cookies = await browser.cookies()

        await browser.close()

        return {
            'platform': 'instagram',
            'username': account_details['username'],
            'cookies': cookies,
            'status': 'active'
        }
```

### Step 3: Integrate Services

Add API credentials to script:
```python
# Email service
EMAIL_API_KEY = "your-temp-mail-api-key"

# SMS service
SMS_API_KEY = "your-sms-activate-api-key"

# CAPTCHA service
CAPTCHA_API_KEY = "your-2captcha-api-key"

# Proxy
PROXY_SERVER = "http://your-proxy.com:8080"
PROXY_USERNAME = "your-username"
PROXY_PASSWORD = "your-password"
```

---

## 🎯 BEST PRACTICES

### Account Warming:
**Don't use accounts immediately!**

After creation, warm them up:
1. Follow 5-10 random accounts
2. Like 10-20 posts
3. Update profile picture
4. Wait 24-48 hours before heavy use

**Why:** Platforms flag brand new accounts that immediately start posting/following at scale

### Rate Limiting:
**Don't create accounts too fast!**

Recommended pace:
- Instagram: 1 account every 5-10 minutes
- TikTok: 1 account every 3-5 minutes
- YouTube: 1 account every 10-15 minutes

**Why:** Too fast = IP ban, account flagged as bot

### Account Storage:
**Keep credentials secure!**

Best practices:
- ✅ Store in encrypted database
- ✅ Use environment variables
- ✅ Backup to encrypted cloud storage
- ❌ Don't commit to git
- ❌ Don't share publicly
- ❌ Don't store in plain text

---

## 📦 OUTPUT FORMAT

### accounts_created.json:
```json
{
  "total_accounts": 300,
  "created_at": "2025-11-01T10:30:00",
  "accounts": [
    {
      "platform": "instagram",
      "username": "user_abc123",
      "email": "user_abc123@temp-mail.org",
      "password": "SecurePass123!@#",
      "profile_url": "https://instagram.com/user_abc123",
      "created_at": "2025-11-01T10:30:15",
      "status": "active",
      "cookies": {...}
    },
    {
      "platform": "tiktok",
      "username": "user_abc123",
      "email": "user_abc123@temp-mail.org",
      "password": "SecurePass123!@#",
      "profile_url": "https://tiktok.com/@user_abc123",
      "created_at": "2025-11-01T10:35:22",
      "status": "active"
    }
  ]
}
```

---

## 🚨 TROUBLESHOOTING

### "CAPTCHA detected"
**Solution:** Integrate 2captcha.com API, sends CAPTCHAs to human solvers

### "Phone number already used"
**Solution:** Rotate SMS verification services, use multiple providers

### "Email already exists"
**Solution:** Generate more unique email addresses, check temp-mail hasn't been used

### "IP banned"
**Solution:** Rotate residential proxies more frequently, slow down creation rate

### "Account immediately suspended"
**Solution:** Warm up accounts before use, don't follow/post immediately

---

## 🔗 INTEGRATION WITH QUANTUM VAULT

### How Employee Will Use This:

**Task:** Create 150 accounts (50 Instagram, 50 TikTok, 50 YouTube)

**Steps:**
1. Run script: `python ACCOUNT_SETUP_AUTOMATION.py`
2. Enter: `50` accounts
3. Enter: `instagram,tiktok,youtube`
4. Wait 3-5 days (runs automatically)
5. Upload `accounts_created.json` to Google Drive
6. Verify 90%+ success rate

**Success Criteria:**
- ✅ 135+ working accounts (90% success)
- ✅ All credentials saved correctly
- ✅ JSON file uploads successfully

**Payment:** $50 for this task (6-8 hours of monitoring)

---

## 🌟 FUTURE ENHANCEMENTS

### v2.0 (Week 2):
- ✅ Add Facebook support
- ✅ Add Twitter/X support
- ✅ Add LinkedIn support
- ✅ Parallel account creation (10 at once)

### v3.0 (Month 2):
- ✅ AI-powered profile customization
- ✅ Automatic bio generation
- ✅ Profile picture generation (AI faces)
- ✅ Smart username generation

### v4.0 (Month 3):
- ✅ Account health monitoring
- ✅ Automatic re-verification if flagged
- ✅ Account rotation system
- ✅ Multi-platform campaign management

---

## 📚 DOCUMENTATION REFERENCES

**Playwright Docs:** https://playwright.dev/python/
**Anti-Detection:** https://github.com/AtuboDad/playwright_stealth
**temp-mail API:** https://temp-mail.org/en/api/
**SMS Activate:** https://sms-activate.org/en/api2
**2captcha:** https://2captcha.com/api-docs

---

## ✅ READY TO USE

**Current Status:**
- ✅ Demo mode working
- ✅ Architecture complete
- ✅ Documentation complete
- ⏳ Production services (pending setup)

**To Go Production:**
1. Setup 4 services (3 hours)
2. Add API credentials (30 min)
3. Uncomment production code (30 min)
4. Test with 1 account (15 min)
5. Run batch of 300 (3 days automated)

**Total Time to Production:** 4 hours human time + 3 days machine time

---

**This script turns a 2-month manual nightmare into a 4-hour automated dream.** ✨

**Questions?** Check inline comments in `ACCOUNT_SETUP_AUTOMATION.py`
