# 💻 Intelligent Terminal Backend

Backend API for the Intelligent Terminal interface - provides Claude AI-powered debugging assistance with codeword protection.

## Features

- **AI Debugging Assistant**: Powered by Claude 3.5 Sonnet
- **Codeword Protection**: Secure access control
- **Conversation History**: Maintains context across messages
- **Bug Reporting**: Integrated bug report receiver
- **Demo Mode**: Works without API key (fallback responses)
- **Interaction Logging**: Logs all conversations for improvement
- **Terminal-Friendly Responses**: Concise, actionable guidance

## Quick Start

### Option 1: Windows Launcher (Easiest)

```bash
# Double-click START_TERMINAL.bat
# Or run from command line:
START_TERMINAL.bat
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and configure:
# - ANTHROPIC_API_KEY (get from https://console.anthropic.com/)
# - TERMINAL_CODEWORD (change from default "dog")

# Run server
python app.py
```

Server will start on `http://localhost:5002`

## API Endpoints

### Health Check
```
GET /api/health
```

Returns server status and configuration.

**Response:**
```json
{
  "status": "operational",
  "service": "intelligent-terminal",
  "timestamp": "2025-11-22T07:45:00.000Z",
  "anthropic_configured": true,
  "codeword_enabled": true
}
```

### Terminal Status
```
GET /terminal/status
```

Check if terminal API is online.

**Response:**
```json
{
  "status": "online",
  "service": "Terminal API",
  "version": "1.0",
  "timestamp": "2025-11-22T07:45:00.000Z",
  "codeword_required": true
}
```

### Verify Codeword
```
POST /terminal/verify
Content-Type: application/json

{
  "codeword": "dog"
}
```

Verify access codeword without making AI API call.

**Response (Success):**
```json
{
  "success": true,
  "message": "Access granted - terminal unlocked"
}
```

**Response (Failure):**
```json
{
  "success": false,
  "message": "Invalid codeword - access denied"
}
```

### Chat with AI
```
POST /terminal/chat
Content-Type: application/json

{
  "codeword": "dog",
  "message": "The analytics dashboard isn't loading. How do I debug this?",
  "history": [
    {
      "role": "user",
      "content": "Previous message"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ]
}
```

Submit a debugging question to Claude AI.

**Response:**
```json
{
  "success": true,
  "response": "Let's troubleshoot the analytics dashboard...\n\n1. Check browser console for errors\n2. Verify the backend is running on port 5100\n3. Check CORS configuration...",
  "demo_mode": false,
  "timestamp": "2025-11-22T07:45:00.000Z"
}
```

### Submit Bug Report
```
POST /api/bug-report
Content-Type: application/json

{
  "page": "analytics-dashboard.html",
  "description": "Dashboard shows blank screen",
  "email": "user@example.com",
  "browser": "Chrome 120",
  "screenshot": "data:image/png;base64,..."
}
```

Submit a bug report from the platform.

**Response:**
```json
{
  "success": true,
  "bug_id": "20251122_074500",
  "message": "Bug report received. Thank you!"
}
```

## Configuration

### Environment Variables (.env)

- `ANTHROPIC_API_KEY`: Anthropic API key for Claude AI (optional, uses demo mode if not set)
- `TERMINAL_CODEWORD`: Access codeword (default: "dog" - change for security!)

### Data Storage

The backend stores data in the `data/` directory:

- `data/logs/terminal_log_YYYY-MM-DD.txt`: Daily conversation logs
- `data/bugs/bug_YYYYMMDD_HHMMSS.json`: Individual bug reports
- `data/bugs/bugs_master_log.jsonl`: Master bug report log (JSONL format)

## Frontend Integration

The backend is designed to work with:
- `PLATFORM/intelligent-terminal.html` (AI-powered terminal)
- `PLATFORM/terminal.html` (basic terminal)
- `PLATFORM/debug-terminal.html` (debug interface)

Update the `API_URL` in the frontend to point to:
```javascript
const API_URL = 'http://localhost:5002';
```

## Security Features

### Codeword Protection

All terminal chat requests require a valid codeword. This prevents unauthorized access to the AI debugging assistant.

**Default codeword:** `dog`
**Important:** Change this in your `.env` file for production!

### Demo Mode

When `ANTHROPIC_API_KEY` is not configured, the system automatically switches to demo mode:
- Returns helpful fallback responses
- Logs interactions normally
- Indicates demo mode in response
- Guides user to configure API key

## System Prompt

The AI is configured as a debugging assistant with this system prompt:

```
You are a helpful debugging assistant for the 100X Consciousness Revolution platform.

Users accessing you through a terminal interface are authorized employees or helpers trying to:
- Debug website issues
- Get help with platform navigation
- Report bugs or problems
- Ask technical questions

Your responses should be:
- Concise and terminal-friendly (short paragraphs)
- Technical but friendly
- Include actionable debugging steps when relevant
- Reassuring - you're here to help solve problems

Format responses for terminal display (avoid markdown, use plain text).
Keep responses under 200 words unless explaining complex technical issues.
```

## Conversation History

The API maintains conversation context by accepting a `history` array in chat requests. The system:
- Keeps last 10 messages for context
- Passes conversation history to Claude API
- Enables multi-turn debugging conversations
- Maintains context across page refreshes (frontend responsibility)

## Dependencies

- **Flask**: Web framework
- **flask-cors**: CORS support for frontend integration
- **anthropic**: Anthropic Claude API client
- **python-dotenv**: Environment variable management

## Testing

Test endpoints using curl:

```bash
# Health check
curl http://localhost:5002/api/health

# Terminal status
curl http://localhost:5002/terminal/status

# Verify codeword
curl -X POST http://localhost:5002/terminal/verify \
  -H "Content-Type: application/json" \
  -d '{"codeword":"dog"}'

# Chat with AI
curl -X POST http://localhost:5002/terminal/chat \
  -H "Content-Type: application/json" \
  -d '{"codeword":"dog","message":"How do I fix a 404 error on the platform?"}'

# Submit bug report
curl -X POST http://localhost:5002/api/bug-report \
  -H "Content-Type: application/json" \
  -d '{"page":"test.html","description":"Test bug","email":"test@example.com"}'
```

## Production Deployment

For production deployment:

1. **Change default codeword** in `.env`
2. **Set ANTHROPIC_API_KEY** for AI responses
3. **Enable HTTPS/SSL** for secure transmission
4. **Add rate limiting** to prevent abuse
5. **Implement IP whitelisting** for extra security
6. **Set up backup** for conversation logs and bug reports
7. **Configure CORS** for specific domains only
8. **Add authentication** for bug report endpoint
9. **Set up monitoring** and alerting
10. **Regular log rotation** for conversation logs

## Port Configuration

- **Default Port:** 5002
- **Philosopher AI:** 5001
- **Analytics Dashboard:** 5100

If you need to change the port, edit the last line in `app.py`:
```python
app.run(host='0.0.0.0', port=5002, debug=True)  # Change 5002 to desired port
```

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not found" (not an error)
The system will run in demo mode. To enable AI responses:
1. Get API key from https://console.anthropic.com/
2. Add to `.env` file: `ANTHROPIC_API_KEY=your_key_here`
3. Restart the backend

### "Invalid codeword" error
Check your `.env` file and ensure `TERMINAL_CODEWORD` matches what you're sending from frontend.

### Port already in use
Change the port number in `app.py` or stop the conflicting service.

## Next Steps

1. ✅ Basic API implementation complete
2. ⏳ Test with frontend integration
3. ⏳ Change default codeword for security
4. ⏳ Configure ANTHROPIC_API_KEY for AI responses
5. ⏳ Deploy to production server

## Status

**✅ COMPLETE - Ready for Testing**

All core endpoints implemented. Codeword protection active. Demo mode works without API key. Frontend integration ready.

---

**Part of**: 100x Platform - Consciousness Revolution
**Created**: 2025-11-22
**Trinity Instance**: C1 Mechanic (Autonomous Work Protocol)
