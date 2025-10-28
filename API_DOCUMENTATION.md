# OVERKORE API Documentation

**Base URL:** `https://conciousnessrevolution.io/.netlify/functions/`

**Version:** 1.0
**Last Updated:** October 28, 2025

---

## Authentication

Most endpoints are currently open (beta phase). Future versions will require API keys.

---

## Endpoints

### 1. User Detector API

**Endpoint:** `GET /.netlify/functions/user-detector`

**Purpose:** Returns workspace state and online users

**Request:**
```bash
curl https://conciousnessrevolution.io/.netlify/functions/user-detector
```

**Response:**
```json
{
  "workspace": {
    "status": "active",
    "online_users": 0,
    "modules_active": [],
    "recent_activity": []
  },
  "timestamp": "2025-10-28T10:00:00.000Z"
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

### 2. Araya User Profile API

**Endpoint:** `GET /.netlify/functions/araya-api/{userId}`

**Purpose:** Returns user profile data

**Request:**
```bash
curl https://conciousnessrevolution.io/.netlify/functions/araya-api/1001
```

**Response:**
```json
{
  "user": {
    "id": "1001",
    "name": "Builder",
    "role": "Beta Tester",
    "status": "Active",
    "permissions": ["dashboard", "jarvis", "analytics"],
    "joined": "2025-10-28T10:00:00.000Z"
  }
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

### 3. Web Bug Report API

**Endpoint:** `POST /.netlify/functions/web-bug-report`

**Purpose:** Submit bug reports that auto-create GitHub issues

**Request:**
```bash
curl -X POST https://conciousnessrevolution.io/.netlify/functions/web-bug-report \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Button not working",
    "description": "The submit button on login page is unresponsive",
    "reporter": "john@example.com"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Bug report received",
  "issue_number": 14,
  "issue_url": "https://github.com/overkillkulture/consciousness-bugs/issues/14"
}
```

**Status Codes:**
- `200` - Success
- `405` - Method not allowed (must be POST)
- `500` - Failed to create issue

---

### 4. SMS Bug Report API (Webhook)

**Endpoint:** `POST /.netlify/functions/sms-bug-report`

**Purpose:** Receives SMS messages from Twilio and creates GitHub issues

**Note:** This is a webhook endpoint called by Twilio, not meant for direct use.

**Twilio Webhook Config:**
- **URL:** `https://conciousnessrevolution.io/.netlify/functions/sms-bug-report`
- **Method:** POST
- **Event:** Incoming Message

**Request Body (from Twilio):**
```
Body=Bug report text here&From=+15551234567
```

**Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>✅ Bug received! GitHub issue #14 created. Track it here: https://github.com/overkillkulture/consciousness-bugs/issues/14</Message>
</Response>
```

**Status Codes:**
- `200` - Success (TwiML response)
- `500` - Error creating issue

---

## Builder Terminal API

**Base URL:** `https://stagey-hilary-nongremial.ngrok-free.dev`

**Note:** Currently using ngrok tunnel for development. Production endpoint coming soon.

### Chat Endpoint

**Endpoint:** `POST /chat`

**Purpose:** Send messages to Claude Sonnet 4 AI

**Request:**
```bash
curl -X POST https://stagey-hilary-nongremial.ngrok-free.dev/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a function that checks if a number is prime",
    "conversation_id": "user_12345"
  }'
```

**Response:**
```json
{
  "response": "Here's a function to check if a number is prime:\n\n```javascript\nfunction isPrime(n) {\n  if (n <= 1) return false;\n  for (let i = 2; i * i <= n; i++) {\n    if (n % i === 0) return false;\n  }\n  return true;\n}\n```",
  "conversation_id": "user_12345",
  "timestamp": "2025-10-28T10:00:00.000Z"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad request (missing message)
- `500` - AI service error

---

## Error Handling

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

Common error codes:
- `400` - Bad Request (missing/invalid parameters)
- `401` - Unauthorized (API key missing/invalid)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (endpoint doesn't exist)
- `405` - Method Not Allowed (wrong HTTP method)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error
- `503` - Service Unavailable (maintenance)

---

## Rate Limits

**Current (Beta):**
- No rate limits enforced
- Fair use policy applies

**Future (Production):**
- Free tier: 100 requests/day
- Pro tier: 10,000 requests/day
- Enterprise: Unlimited

---

## CORS

All endpoints support CORS with:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Headers: Content-Type`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`

---

## Webhooks

### SMS Bug Reporter Webhook

**Setup:**
1. Go to Twilio Console: https://console.twilio.com
2. Navigate to Phone Numbers → Manage → Active Numbers
3. Select your number
4. Under "Messaging Configuration":
   - Webhook URL: `https://conciousnessrevolution.io/.netlify/functions/sms-bug-report`
   - HTTP Method: POST
5. Save

**Testing:**
```bash
# Send test SMS via Twilio API
curl -X POST https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/Messages.json \
  --data-urlencode "From=+15092166552" \
  --data-urlencode "To=+15551234567" \
  --data-urlencode "Body=Test bug report" \
  -u {ACCOUNT_SID}:{AUTH_TOKEN}
```

---

## Code Examples

### JavaScript/Node.js

```javascript
// Submit bug report
const submitBug = async (title, description, reporter) => {
  const response = await fetch(
    'https://conciousnessrevolution.io/.netlify/functions/web-bug-report',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description, reporter })
    }
  );
  return response.json();
};

// Usage
const result = await submitBug(
  'Login button broken',
  'Button does not respond to clicks',
  'user@example.com'
);
console.log(`Issue created: ${result.issue_url}`);
```

### Python

```python
import requests

def submit_bug(title, description, reporter):
    url = 'https://conciousnessrevolution.io/.netlify/functions/web-bug-report'
    data = {
        'title': title,
        'description': description,
        'reporter': reporter
    }
    response = requests.post(url, json=data)
    return response.json()

# Usage
result = submit_bug(
    'Login button broken',
    'Button does not respond to clicks',
    'user@example.com'
)
print(f"Issue created: {result['issue_url']}")
```

### cURL

```bash
# Get workspace status
curl https://conciousnessrevolution.io/.netlify/functions/user-detector

# Get user profile
curl https://conciousnessrevolution.io/.netlify/functions/araya-api/1001

# Submit bug report
curl -X POST https://conciousnessrevolution.io/.netlify/functions/web-bug-report \
  -H "Content-Type: application/json" \
  -d '{"title":"Bug title","description":"Bug details","reporter":"user@example.com"}'
```

---

## SDK (Coming Soon)

We're building official SDKs for:
- JavaScript/TypeScript
- Python
- Go
- Ruby

**Current workaround:** Use the REST API directly with `fetch()` or `requests` library.

---

## Status Page

Check system status: https://conciousnessrevolution.io/status (Coming Soon)

Current uptime can be verified by hitting:
```bash
curl https://conciousnessrevolution.io/.netlify/functions/user-detector
```

If you get a `200` response, all systems operational.

---

## Support

**Bug Reports:**
- SMS: +1 (509) 216-6552
- GitHub: https://github.com/overkillkulture/consciousness-bugs/issues
- Email: [support email]

**Questions:**
- Email: [support email]
- Discord: [invite link] (Coming Soon)

---

## Changelog

### v1.0 (October 28, 2025)
- ✅ Initial API release
- ✅ User Detector endpoint
- ✅ Araya API endpoint
- ✅ Web Bug Report endpoint
- ✅ SMS Bug Report webhook
- ✅ Builder Terminal chat endpoint

### Upcoming (v1.1)
- 🚧 Authentication with API keys
- 🚧 Rate limiting
- 🚧 Araya computer control endpoints
- 🚧 Trinity AI collaboration endpoints
- 🚧 Workspace module creation API

---

*For the latest updates, visit: https://conciousnessrevolution.io/investment-hub.html*
