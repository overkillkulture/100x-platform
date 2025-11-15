# 100X Platform - Unified Authentication Setup

## Overview

This document describes the unified authentication system for the 100X Platform. The system consolidates all entry points into a single, clean authentication flow.

## Architecture

### Components

1. **start.html** - Single entry point with login/signup forms
2. **auth_server.py** - Flask backend using existing auth_system.py
3. **workspace.html** - Protected workspace (requires authentication)
4. **BACKEND/auth_system.py** - Core authentication logic (JWT + PostgreSQL)

### Flow

```
User visits / (start.html)
  ↓
Login or Signup
  ↓
JWT token stored in localStorage
  ↓
Redirect to /workspace
  ↓
workspace.html verifies token
  ↓
User accesses platform
```

## Setup Instructions

### 1. Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and fill in your actual credentials:

```bash
# Required for authentication
DATABASE_URL=postgresql://username:password@localhost/consciousness_revolution
JWT_SECRET_KEY=your-secret-key-here

# Optional: Other services
AIRTABLE_TOKEN=your-token
TWILIO_AUTH_TOKEN=your-token
# ... etc
```

**Generate a secure JWT secret:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Database Setup

The auth system requires PostgreSQL. Create the database:

```bash
createdb consciousness_revolution
```

Run the schema setup (if you have migrations):

```bash
python BACKEND/setup_database.py  # If this file exists
```

**Required tables:**
- `users` - User accounts
- `domain_access` - Access permissions per domain
- `conversion_events` - Analytics

### 3. Install Dependencies

```bash
pip install flask flask-cors psycopg2-binary bcrypt pyjwt
```

### 4. Start the Server

```bash
python auth_server.py
```

The server will start on `http://localhost:5000`

### 5. Test the Flow

1. Visit `http://localhost:5000` → You see start.html
2. Click "Sign Up" → Create an account
3. You're redirected to `/workspace` → workspace.html loads
4. Click "Logout" → Back to start.html
5. Login again → Workspace loads with your session

## API Endpoints

### Authentication

**POST /api/auth/signup**
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "full_name": "John Doe"
}
```

Response:
```json
{
  "success": true,
  "user_id": 123,
  "token": "eyJ...",
  "message": "Account created successfully"
}
```

**POST /api/auth/login**
```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

Response:
```json
{
  "success": true,
  "user_id": 123,
  "email": "user@example.com",
  "token": "eyJ...",
  "message": "Login successful"
}
```

**GET /api/auth/verify**

Headers: `Authorization: Bearer <token>`

Response:
```json
{
  "success": true,
  "user_id": 123,
  "email": "user@example.com"
}
```

### Access Control

**GET /api/access/{domain}**

Check if user has access to a specific domain (music, intelligence, tools, etc.)

Headers: `Authorization: Bearer <token>`

**POST /api/usage/{domain}/{action}**

Record usage for freemium limits

## Security Notes

1. **Never commit .env file** - It contains secrets
2. **Use strong JWT secret** - 32+ characters, random
3. **HTTPS in production** - Don't use HTTP for real deployments
4. **Rotate credentials** - Change tokens/passwords regularly
5. **Rate limiting** - Add rate limiting in production

## Migration from Old Gate Files

The old gate files (100X_GATE_*.py) used Airtable and consciousness screening. This new system:

- Uses PostgreSQL instead of Airtable for user data
- Provides proper JWT-based authentication
- Has a cleaner, simpler flow
- Supports cross-domain SSO

To migrate existing users:
1. Export data from Airtable
2. Import into PostgreSQL users table
3. Set initial passwords (send reset links)

## Environment Variables Reference

### Required
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret for JWT token generation

### Optional
- `PORT` - Server port (default: 5000)
- `FLASK_ENV` - Environment (development/production)
- `AIRTABLE_TOKEN` - For legacy integrations
- `TWILIO_*` - For SMS features
- `GMAIL_*` - For email features

See `.env.example` for complete list.

## Troubleshooting

### "Auth system not available"

Check:
1. Is PostgreSQL running?
2. Is DATABASE_URL correct?
3. Does the database exist?
4. Do the tables exist?

### "Invalid or expired token"

Token expired (7 days default) or invalid. User needs to login again.

### Can't access workspace

1. Check browser console for errors
2. Verify token exists in localStorage
3. Check server logs for auth verification

## What's Next

After authentication is working:

1. Add email verification
2. Add password reset flow
3. Add 2FA support
4. Add social login (Google, GitHub)
5. Add role-based access control
6. Add API rate limiting

## Files Modified

- `start.html` - NEW - Entry point
- `auth_server.py` - NEW - Main server
- `workspace.html` - MODIFIED - Added auth check
- `.env.example` - NEW - Environment template
- `BACKEND/auth_system.py` - EXISTING - Used as-is

## Support

For issues, check:
1. Server logs
2. Browser console
3. Network tab in DevTools
4. Database logs
