# 100X Platform API Gateway - Quick Start Guide

## 5-Minute Setup

### Step 1: Prerequisites

Install required software:

```bash
# Python 3.11+
python --version  # Should be 3.11 or higher

# Redis
redis-server --version

# PostgreSQL (optional but recommended)
psql --version
```

### Step 2: Environment Setup

```bash
# Navigate to API Gateway directory
cd /home/user/100x-platform/API_GATEWAY

# Copy environment file
cp .env.example .env

# Generate secure JWT secret
python -c "import secrets; print(secrets.token_urlsafe(64))"

# Edit .env and paste the generated secret
nano .env  # or your preferred editor
```

**IMPORTANT:** Update these values in `.env`:
- `JWT_SECRET_KEY` - Use the generated secret above
- `REDIS_HOST` - Your Redis host (default: localhost)
- `DATABASE_URL` - Your PostgreSQL connection string

### Step 3: Start Services

#### Option A: Automated Start (Recommended)

```bash
# Make start script executable
chmod +x start.sh

# Run startup script
./start.sh
```

#### Option B: Manual Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Redis (if not running)
redis-server --daemonize yes

# Start API Gateway
uvicorn gateway:app --host 0.0.0.0 --port 8000 --reload
```

#### Option C: Docker (Production)

```bash
# Start all services with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Step 4: Test the API

Open your browser or use curl:

```bash
# Health check
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/api/docs
```

Expected response:
```json
{
  "success": true,
  "data": {
    "status": "healthy"
  },
  "message": "API Gateway is running",
  "timestamp": "2025-11-07T12:00:00Z",
  "request_id": "req_abc123"
}
```

### Step 5: Create Your First User

```bash
# Login (creates user automatically in development mode)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password"
  }'
```

Save the `access_token` from the response!

### Step 6: Access Modules

```bash
# List all available modules
curl -X GET http://localhost:8000/modules \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Access a specific module (e.g., Code Sandbox)
curl -X POST http://localhost:8000/modules/code-sandbox/execute \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello from 100X Platform!\")",
    "language": "python"
  }'
```

## Common Commands

### Development

```bash
# Start development server
uvicorn gateway:app --reload

# Run with custom port
uvicorn gateway:app --port 8080

# Enable debug logging
LOG_LEVEL=DEBUG uvicorn gateway:app --reload
```

### Production

```bash
# Start production server (4 workers)
uvicorn gateway:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn
gunicorn gateway:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker

```bash
# Build image
docker build -t 100x-api-gateway .

# Run container
docker run -d -p 8000:8000 --name api-gateway 100x-api-gateway

# View logs
docker logs -f api-gateway

# Stop container
docker stop api-gateway
```

### Troubleshooting

```bash
# Check Redis
redis-cli ping

# Check database connection
psql $DATABASE_URL -c "SELECT 1"

# View logs
tail -f api_gateway.log

# Test configuration
python config.py
```

## Essential Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/docs` | GET | API documentation |
| `/auth/login` | POST | User login |
| `/api-keys/create` | POST | Create API key |
| `/modules` | GET | List all modules |
| `/modules/{name}/*` | * | Access module |

## Next Steps

1. ✅ API Gateway is running
2. 📚 Read full documentation: `README.md`
3. 🔑 Create API keys for applications
4. 🚀 Explore all 30 modules
5. 🎯 Build your first integration

## Support

- **Documentation:** See `README.md` for comprehensive guide
- **Issues:** Check logs in `api_gateway.log`
- **Configuration:** Review `.env` file
- **Examples:** See `README.md` Examples section

---

**You're ready to go! 🚀**

The API Gateway is now running and ready to serve all 30 platform modules.

Visit http://localhost:8000/api/docs to explore the interactive API documentation.
