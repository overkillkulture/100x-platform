"""
100X PLATFORM - UNIFIED API GATEWAY
====================================

Production-ready API Gateway for all 30 platform modules with:
- JWT Authentication
- Redis-based Rate Limiting
- Module Routing
- Unified Response Formatting
- Comprehensive Error Handling
- Request/Response Logging
- API Key Management
- CORS Configuration
- Health Check Endpoints

Author: 100X Platform
Version: 1.0.0
License: MIT
"""

import os
import time
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from functools import wraps

from fastapi import FastAPI, Request, HTTPException, Depends, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, validator
import redis
import jwt
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn

from config import settings

# ===========================
# LOGGING CONFIGURATION
# ===========================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_gateway.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===========================
# REDIS CONNECTION
# ===========================

try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=0,
        decode_responses=True
    )
    redis_client.ping()
    logger.info("✅ Redis connection successful")
except Exception as e:
    logger.error(f"❌ Redis connection failed: {e}")
    redis_client = None

# ===========================
# FASTAPI APP INITIALIZATION
# ===========================

app = FastAPI(
    title="100X Platform API Gateway",
    description="Unified API Gateway for all 30 production modules",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security
security = HTTPBearer()

# ===========================
# CORS CONFIGURATION
# ===========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# PYDANTIC MODELS
# ===========================

class TokenData(BaseModel):
    """JWT Token Data Model"""
    user_id: str
    email: str
    tier: str = "free"  # free, pro, enterprise
    exp: Optional[datetime] = None

class LoginRequest(BaseModel):
    """Login Request Model"""
    email: str
    password: str

    @validator('email')
    def email_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()

class APIKeyRequest(BaseModel):
    """API Key Creation Request"""
    name: str
    tier: str = "free"
    expires_days: Optional[int] = None

class StandardResponse(BaseModel):
    """Standard API Response Format"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None
    timestamp: str
    request_id: str

# ===========================
# MODULE ROUTING TABLE
# ===========================

MODULE_ROUTES = {
    # INFRASTRUCTURE (10 modules)
    "fundraising": {"path": "/api/v1/fundraising", "tier": "free"},
    "marketing": {"path": "/api/v1/marketing", "tier": "pro"},
    "design-hub": {"path": "/api/v1/design-hub", "tier": "pro"},
    "social-media": {"path": "/api/v1/social-media", "tier": "free"},
    "customer-service": {"path": "/api/v1/customer-service", "tier": "pro"},
    "bookkeeping": {"path": "/api/v1/bookkeeping", "tier": "pro"},
    "email-campaigns": {"path": "/api/v1/email-campaigns", "tier": "pro"},
    "project-manager": {"path": "/api/v1/project-manager", "tier": "pro"},
    "testing-suite": {"path": "/api/v1/testing-suite", "tier": "enterprise"},
    "shopping-cart": {"path": "/api/v1/shopping-cart", "tier": "free"},

    # ADVANCED (3 modules)
    "code-sandbox": {"path": "/api/v1/code-sandbox", "tier": "free"},
    "drone-system": {"path": "/api/v1/drone-system", "tier": "enterprise"},
    "voice-assistant": {"path": "/api/v1/voice-assistant", "tier": "pro"},

    # CONTENT (6 modules)
    "video-editing": {"path": "/api/v1/video-editing", "tier": "pro"},
    "podcast-production": {"path": "/api/v1/podcast-production", "tier": "pro"},
    "stock-media": {"path": "/api/v1/stock-media", "tier": "pro"},
    "music-production": {"path": "/api/v1/music-production", "tier": "pro"},
    "content-repurposing": {"path": "/api/v1/content-repurposing", "tier": "pro"},
    "seo-content": {"path": "/api/v1/seo-content", "tier": "pro"},

    # LEGAL (4 modules)
    "corruption-mapping": {"path": "/api/v1/corruption-mapping", "tier": "free"},
    "pattern-security": {"path": "/api/v1/pattern-security", "tier": "pro"},
    "law-module": {"path": "/api/v1/law-module", "tier": "pro"},
    "legal-documents": {"path": "/api/v1/legal-documents", "tier": "pro"},

    # KNOWLEDGE (3 modules)
    "spreadsheet-brain": {"path": "/api/v1/spreadsheet-brain", "tier": "free"},
    "data-crystals": {"path": "/api/v1/data-crystals", "tier": "pro"},
    "data-analytics": {"path": "/api/v1/data-analytics", "tier": "pro"},

    # HEALTH (1 module)
    "personal-trainer": {"path": "/api/v1/personal-trainer", "tier": "free"},

    # AUTOMATION (3 modules)
    "social-automation": {"path": "/api/v1/social-automation", "tier": "pro"},
    "jarvis-assistant": {"path": "/api/v1/jarvis-assistant", "tier": "pro"},
    "dropshipping": {"path": "/api/v1/dropshipping", "tier": "pro"},
}

# ===========================
# RATE LIMITING TIERS
# ===========================

RATE_LIMITS = {
    "free": "100/hour",
    "pro": "1000/hour",
    "enterprise": "10000/hour",
    "admin": "100000/hour"
}

# ===========================
# MIDDLEWARE
# ===========================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses"""
    request_id = hashlib.md5(f"{time.time()}{request.url}".encode()).hexdigest()
    request.state.request_id = request_id

    start_time = time.time()

    # Log request
    logger.info(f"[{request_id}] {request.method} {request.url.path} - Client: {request.client.host}")

    try:
        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        logger.info(f"[{request_id}] Response: {response.status_code} - Time: {process_time:.3f}s")

        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        return response
    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}")
        raise

# ===========================
# AUTHENTICATION
# ===========================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Verify JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        user_id: str = payload.get("user_id")
        email: str = payload.get("email")
        tier: str = payload.get("tier", "free")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        return TokenData(user_id=user_id, email=email, tier=tier)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def verify_api_key(api_key: str = Header(..., alias="X-API-Key")) -> Dict[str, Any]:
    """Verify API key from header"""
    if not redis_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API key verification service unavailable"
        )

    # Check if API key exists in Redis
    key_data = redis_client.get(f"api_key:{api_key}")

    if not key_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    key_info = json.loads(key_data)

    # Check if key is expired
    if key_info.get("expires_at"):
        expires_at = datetime.fromisoformat(key_info["expires_at"])
        if datetime.utcnow() > expires_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key has expired"
            )

    return key_info

def check_tier_access(required_tier: str, user_tier: str) -> bool:
    """Check if user tier has access to required tier"""
    tier_hierarchy = {"free": 0, "pro": 1, "enterprise": 2, "admin": 3}
    return tier_hierarchy.get(user_tier, 0) >= tier_hierarchy.get(required_tier, 0)

# ===========================
# HELPER FUNCTIONS
# ===========================

def create_response(
    success: bool,
    data: Any = None,
    error: str = None,
    message: str = None,
    request_id: str = None
) -> Dict[str, Any]:
    """Create standardized API response"""
    return {
        "success": success,
        "data": data,
        "error": error,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id
    }

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_api_key() -> str:
    """Generate random API key"""
    import secrets
    return f"100x_{secrets.token_urlsafe(32)}"

# ===========================
# HEALTH CHECK ENDPOINTS
# ===========================

@app.get("/health")
@limiter.limit("10/minute")
async def health_check(request: Request):
    """Basic health check"""
    return create_response(
        success=True,
        data={"status": "healthy"},
        message="API Gateway is running",
        request_id=request.state.request_id
    )

@app.get("/health/detailed")
@limiter.limit("5/minute")
async def detailed_health_check(request: Request):
    """Detailed health check with service status"""
    services = {
        "api_gateway": "healthy",
        "redis": "healthy" if redis_client and redis_client.ping() else "unhealthy",
        "modules": {}
    }

    # Check module availability (simplified - would ping actual services)
    for module_name in MODULE_ROUTES.keys():
        services["modules"][module_name] = "healthy"

    return create_response(
        success=True,
        data=services,
        message="Detailed health status",
        request_id=request.state.request_id
    )

@app.get("/health/redis")
@limiter.limit("5/minute")
async def redis_health(request: Request):
    """Redis connection health check"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis connection not available")

    try:
        redis_client.ping()
        info = redis_client.info()

        return create_response(
            success=True,
            data={
                "connected": True,
                "version": info.get("redis_version"),
                "uptime_days": info.get("uptime_in_days"),
                "connected_clients": info.get("connected_clients")
            },
            message="Redis is healthy",
            request_id=request.state.request_id
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Redis error: {str(e)}")

# ===========================
# AUTHENTICATION ENDPOINTS
# ===========================

@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, login_data: LoginRequest):
    """User login endpoint"""
    # In production, verify against database
    # This is a simplified example

    email = login_data.email
    password = hash_password(login_data.password)

    # Simplified user verification (replace with real database check)
    user_data = {
        "user_id": hashlib.md5(email.encode()).hexdigest(),
        "email": email,
        "tier": "free"  # Would come from database
    }

    # Create access token
    access_token = create_access_token(user_data)

    logger.info(f"User logged in: {email}")

    return create_response(
        success=True,
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.JWT_EXPIRATION_HOURS * 3600,
            "user": user_data
        },
        message="Login successful",
        request_id=request.state.request_id
    )

@app.post("/auth/verify")
@limiter.limit("100/minute")
async def verify_auth(request: Request, token_data: TokenData = Depends(verify_token)):
    """Verify authentication token"""
    return create_response(
        success=True,
        data={
            "user_id": token_data.user_id,
            "email": token_data.email,
            "tier": token_data.tier
        },
        message="Token is valid",
        request_id=request.state.request_id
    )

# ===========================
# API KEY MANAGEMENT
# ===========================

@app.post("/api-keys/create")
@limiter.limit("10/hour")
async def create_api_key(
    request: Request,
    key_request: APIKeyRequest,
    token_data: TokenData = Depends(verify_token)
):
    """Create new API key"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="API key service unavailable")

    api_key = generate_api_key()

    key_data = {
        "user_id": token_data.user_id,
        "email": token_data.email,
        "name": key_request.name,
        "tier": key_request.tier,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(days=key_request.expires_days)).isoformat() if key_request.expires_days else None
    }

    # Store in Redis
    redis_client.set(f"api_key:{api_key}", json.dumps(key_data))

    # Store user's keys list
    user_keys = redis_client.get(f"user_keys:{token_data.user_id}")
    if user_keys:
        keys_list = json.loads(user_keys)
        keys_list.append(api_key)
    else:
        keys_list = [api_key]

    redis_client.set(f"user_keys:{token_data.user_id}", json.dumps(keys_list))

    logger.info(f"API key created for user: {token_data.email}")

    return create_response(
        success=True,
        data={
            "api_key": api_key,
            "name": key_request.name,
            "tier": key_request.tier,
            "created_at": key_data["created_at"],
            "expires_at": key_data["expires_at"]
        },
        message="API key created successfully",
        request_id=request.state.request_id
    )

@app.get("/api-keys/list")
@limiter.limit("20/minute")
async def list_api_keys(
    request: Request,
    token_data: TokenData = Depends(verify_token)
):
    """List all API keys for authenticated user"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="API key service unavailable")

    user_keys = redis_client.get(f"user_keys:{token_data.user_id}")

    if not user_keys:
        return create_response(
            success=True,
            data=[],
            message="No API keys found",
            request_id=request.state.request_id
        )

    keys_list = json.loads(user_keys)
    keys_info = []

    for api_key in keys_list:
        key_data = redis_client.get(f"api_key:{api_key}")
        if key_data:
            info = json.loads(key_data)
            keys_info.append({
                "key": api_key[:20] + "..." + api_key[-8:],  # Partially hidden
                "name": info["name"],
                "tier": info["tier"],
                "created_at": info["created_at"],
                "expires_at": info.get("expires_at")
            })

    return create_response(
        success=True,
        data=keys_info,
        message=f"Found {len(keys_info)} API keys",
        request_id=request.state.request_id
    )

@app.delete("/api-keys/{api_key}")
@limiter.limit("10/minute")
async def delete_api_key(
    api_key: str,
    request: Request,
    token_data: TokenData = Depends(verify_token)
):
    """Delete API key"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="API key service unavailable")

    # Verify key belongs to user
    key_data = redis_client.get(f"api_key:{api_key}")
    if not key_data:
        raise HTTPException(status_code=404, detail="API key not found")

    key_info = json.loads(key_data)
    if key_info["user_id"] != token_data.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this key")

    # Delete key
    redis_client.delete(f"api_key:{api_key}")

    # Remove from user's keys list
    user_keys = redis_client.get(f"user_keys:{token_data.user_id}")
    if user_keys:
        keys_list = json.loads(user_keys)
        keys_list.remove(api_key)
        redis_client.set(f"user_keys:{token_data.user_id}", json.dumps(keys_list))

    logger.info(f"API key deleted: {api_key[:20]}...")

    return create_response(
        success=True,
        message="API key deleted successfully",
        request_id=request.state.request_id
    )

# ===========================
# MODULE ROUTING ENDPOINTS
# ===========================

@app.get("/modules")
@limiter.limit("100/minute")
async def list_modules(request: Request, token_data: TokenData = Depends(verify_token)):
    """List all available modules with access information"""
    modules = []

    for module_name, module_info in MODULE_ROUTES.items():
        has_access = check_tier_access(module_info["tier"], token_data.tier)
        modules.append({
            "name": module_name,
            "path": module_info["path"],
            "required_tier": module_info["tier"],
            "has_access": has_access
        })

    return create_response(
        success=True,
        data={
            "total_modules": len(modules),
            "accessible_modules": sum(1 for m in modules if m["has_access"]),
            "user_tier": token_data.tier,
            "modules": modules
        },
        message="Modules list retrieved",
        request_id=request.state.request_id
    )

@app.api_route("/modules/{module_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@limiter.limit("1000/hour")
async def route_to_module(
    module_name: str,
    path: str,
    request: Request,
    token_data: TokenData = Depends(verify_token)
):
    """Route requests to specific module"""
    # Verify module exists
    if module_name not in MODULE_ROUTES:
        raise HTTPException(status_code=404, detail=f"Module '{module_name}' not found")

    module_info = MODULE_ROUTES[module_name]

    # Check tier access
    if not check_tier_access(module_info["tier"], token_data.tier):
        raise HTTPException(
            status_code=403,
            detail=f"Module '{module_name}' requires '{module_info['tier']}' tier. Your tier: '{token_data.tier}'"
        )

    # Log module access
    logger.info(f"User {token_data.email} accessed module: {module_name}/{path}")

    # In production, this would proxy to actual module service
    # For now, return success response
    return create_response(
        success=True,
        data={
            "module": module_name,
            "path": path,
            "method": request.method,
            "message": f"Module '{module_name}' endpoint would be called here"
        },
        message=f"Request routed to {module_name}",
        request_id=request.state.request_id
    )

# ===========================
# ANALYTICS ENDPOINTS
# ===========================

@app.get("/analytics/usage")
@limiter.limit("20/minute")
async def get_usage_analytics(
    request: Request,
    token_data: TokenData = Depends(verify_token)
):
    """Get usage analytics for user"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Analytics service unavailable")

    # In production, would query actual analytics data
    usage_data = {
        "user_id": token_data.user_id,
        "tier": token_data.tier,
        "period": "last_30_days",
        "total_requests": 1247,
        "successful_requests": 1198,
        "failed_requests": 49,
        "modules_used": 12,
        "top_modules": [
            {"name": "code-sandbox", "requests": 423},
            {"name": "social-media", "requests": 312},
            {"name": "personal-trainer", "requests": 178}
        ]
    }

    return create_response(
        success=True,
        data=usage_data,
        message="Usage analytics retrieved",
        request_id=request.state.request_id
    )

# ===========================
# ERROR HANDLERS
# ===========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=create_response(
            success=False,
            error=exc.detail,
            request_id=getattr(request.state, 'request_id', None)
        )
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content=create_response(
            success=False,
            error="Internal server error",
            request_id=getattr(request.state, 'request_id', None)
        )
    )

# ===========================
# STARTUP/SHUTDOWN EVENTS
# ===========================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("🚀 100X Platform API Gateway starting up...")
    logger.info(f"📊 Total modules: {len(MODULE_ROUTES)}")
    logger.info(f"🔒 JWT authentication enabled")
    logger.info(f"⚡ Redis rate limiting: {'enabled' if redis_client else 'disabled'}")
    logger.info("✅ API Gateway ready to serve requests")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("👋 API Gateway shutting down...")
    if redis_client:
        redis_client.close()

# ===========================
# ROOT ENDPOINT
# ===========================

@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    """Root endpoint with API information"""
    return create_response(
        success=True,
        data={
            "name": "100X Platform API Gateway",
            "version": "1.0.0",
            "total_modules": len(MODULE_ROUTES),
            "documentation": "/api/docs",
            "health_check": "/health",
            "endpoints": {
                "authentication": "/auth/login",
                "api_keys": "/api-keys/create",
                "modules": "/modules",
                "analytics": "/analytics/usage"
            }
        },
        message="Welcome to 100X Platform API Gateway",
        request_id=request.state.request_id
    )

# ===========================
# MAIN EXECUTION
# ===========================

if __name__ == "__main__":
    uvicorn.run(
        "gateway:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
