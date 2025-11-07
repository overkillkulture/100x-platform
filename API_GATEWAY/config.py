"""
100X PLATFORM - API GATEWAY CONFIGURATION
==========================================

Environment-based configuration management for all deployment environments.

Supports:
- Development
- Staging
- Production

Author: 100X Platform
Version: 1.0.0
License: MIT
"""

import os
from typing import List
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    All settings can be overridden via environment variables.
    """

    # ===========================
    # APPLICATION SETTINGS
    # ===========================

    APP_NAME: str = "100X Platform API Gateway"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")  # development, staging, production

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # ===========================
    # SECURITY SETTINGS
    # ===========================

    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "your-secret-key-change-in-production-make-it-very-long-and-random"
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

    # API Key Settings
    API_KEY_LENGTH: int = 32
    API_KEY_PREFIX: str = "100x_"

    # Password Hashing
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_HASH_ALGORITHM: str = "sha256"

    # ===========================
    # REDIS SETTINGS
    # ===========================

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_DECODE_RESPONSES: bool = True

    # Redis connection pool settings
    REDIS_MAX_CONNECTIONS: int = 50
    REDIS_SOCKET_TIMEOUT: int = 5
    REDIS_SOCKET_CONNECT_TIMEOUT: int = 5

    # ===========================
    # CORS SETTINGS
    # ===========================

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Get allowed origins based on environment"""
        if self.ENVIRONMENT == "production":
            return [
                "https://100xplatform.com",
                "https://www.100xplatform.com",
                "https://app.100xplatform.com",
                "https://api.100xplatform.com",
            ]
        elif self.ENVIRONMENT == "staging":
            return [
                "https://staging.100xplatform.com",
                "https://staging-api.100xplatform.com",
            ]
        else:  # development
            return [
                "http://localhost:3000",
                "http://localhost:8000",
                "http://localhost:8080",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8000",
            ]

    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # ===========================
    # RATE LIMITING SETTINGS
    # ===========================

    # Global rate limits (requests per time period)
    RATE_LIMIT_FREE: str = os.getenv("RATE_LIMIT_FREE", "100/hour")
    RATE_LIMIT_PRO: str = os.getenv("RATE_LIMIT_PRO", "1000/hour")
    RATE_LIMIT_ENTERPRISE: str = os.getenv("RATE_LIMIT_ENTERPRISE", "10000/hour")
    RATE_LIMIT_ADMIN: str = os.getenv("RATE_LIMIT_ADMIN", "100000/hour")

    # Endpoint-specific rate limits
    RATE_LIMIT_LOGIN: str = "5/minute"
    RATE_LIMIT_HEALTH: str = "10/minute"
    RATE_LIMIT_MODULE_ACCESS: str = "1000/hour"

    # ===========================
    # DATABASE SETTINGS
    # ===========================

    # PostgreSQL (for user data, API keys, etc.)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/100x_platform"
    )
    DATABASE_ECHO: bool = DEBUG
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ===========================
    # LOGGING SETTINGS
    # ===========================

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO" if ENVIRONMENT == "production" else "DEBUG")
    LOG_FILE: str = os.getenv("LOG_FILE", "api_gateway.log")
    LOG_MAX_BYTES: int = 10_000_000  # 10 MB
    LOG_BACKUP_COUNT: int = 5
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # ===========================
    # MODULE SERVICE ENDPOINTS
    # ===========================

    # Infrastructure modules
    FUNDRAISING_SERVICE_URL: str = os.getenv("FUNDRAISING_SERVICE_URL", "http://localhost:8001")
    MARKETING_SERVICE_URL: str = os.getenv("MARKETING_SERVICE_URL", "http://localhost:8002")
    DESIGN_HUB_SERVICE_URL: str = os.getenv("DESIGN_HUB_SERVICE_URL", "http://localhost:8003")
    SOCIAL_MEDIA_SERVICE_URL: str = os.getenv("SOCIAL_MEDIA_SERVICE_URL", "http://localhost:8004")
    CUSTOMER_SERVICE_SERVICE_URL: str = os.getenv("CUSTOMER_SERVICE_SERVICE_URL", "http://localhost:8005")
    BOOKKEEPING_SERVICE_URL: str = os.getenv("BOOKKEEPING_SERVICE_URL", "http://localhost:8006")
    EMAIL_CAMPAIGNS_SERVICE_URL: str = os.getenv("EMAIL_CAMPAIGNS_SERVICE_URL", "http://localhost:8007")
    PROJECT_MANAGER_SERVICE_URL: str = os.getenv("PROJECT_MANAGER_SERVICE_URL", "http://localhost:8008")
    TESTING_SUITE_SERVICE_URL: str = os.getenv("TESTING_SUITE_SERVICE_URL", "http://localhost:8009")
    SHOPPING_CART_SERVICE_URL: str = os.getenv("SHOPPING_CART_SERVICE_URL", "http://localhost:8010")

    # Advanced modules
    CODE_SANDBOX_SERVICE_URL: str = os.getenv("CODE_SANDBOX_SERVICE_URL", "http://localhost:8011")
    DRONE_SYSTEM_SERVICE_URL: str = os.getenv("DRONE_SYSTEM_SERVICE_URL", "http://localhost:8012")
    VOICE_ASSISTANT_SERVICE_URL: str = os.getenv("VOICE_ASSISTANT_SERVICE_URL", "http://localhost:8013")

    # Content modules
    VIDEO_EDITING_SERVICE_URL: str = os.getenv("VIDEO_EDITING_SERVICE_URL", "http://localhost:8014")
    PODCAST_PRODUCTION_SERVICE_URL: str = os.getenv("PODCAST_PRODUCTION_SERVICE_URL", "http://localhost:8015")
    STOCK_MEDIA_SERVICE_URL: str = os.getenv("STOCK_MEDIA_SERVICE_URL", "http://localhost:8016")
    MUSIC_PRODUCTION_SERVICE_URL: str = os.getenv("MUSIC_PRODUCTION_SERVICE_URL", "http://localhost:8017")
    CONTENT_REPURPOSING_SERVICE_URL: str = os.getenv("CONTENT_REPURPOSING_SERVICE_URL", "http://localhost:8018")
    SEO_CONTENT_SERVICE_URL: str = os.getenv("SEO_CONTENT_SERVICE_URL", "http://localhost:8019")

    # Legal modules
    CORRUPTION_MAPPING_SERVICE_URL: str = os.getenv("CORRUPTION_MAPPING_SERVICE_URL", "http://localhost:8020")
    PATTERN_SECURITY_SERVICE_URL: str = os.getenv("PATTERN_SECURITY_SERVICE_URL", "http://localhost:8021")
    LAW_MODULE_SERVICE_URL: str = os.getenv("LAW_MODULE_SERVICE_URL", "http://localhost:8022")
    LEGAL_DOCUMENTS_SERVICE_URL: str = os.getenv("LEGAL_DOCUMENTS_SERVICE_URL", "http://localhost:8023")

    # Knowledge modules
    SPREADSHEET_BRAIN_SERVICE_URL: str = os.getenv("SPREADSHEET_BRAIN_SERVICE_URL", "http://localhost:8024")
    DATA_CRYSTALS_SERVICE_URL: str = os.getenv("DATA_CRYSTALS_SERVICE_URL", "http://localhost:8025")
    DATA_ANALYTICS_SERVICE_URL: str = os.getenv("DATA_ANALYTICS_SERVICE_URL", "http://localhost:8026")

    # Health modules
    PERSONAL_TRAINER_SERVICE_URL: str = os.getenv("PERSONAL_TRAINER_SERVICE_URL", "http://localhost:8027")

    # Automation modules
    SOCIAL_AUTOMATION_SERVICE_URL: str = os.getenv("SOCIAL_AUTOMATION_SERVICE_URL", "http://localhost:8028")
    JARVIS_ASSISTANT_SERVICE_URL: str = os.getenv("JARVIS_ASSISTANT_SERVICE_URL", "http://localhost:8029")
    DROPSHIPPING_SERVICE_URL: str = os.getenv("DROPSHIPPING_SERVICE_URL", "http://localhost:8030")

    # ===========================
    # EXTERNAL SERVICE SETTINGS
    # ===========================

    # Stripe Payment Processing
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    # SendGrid Email
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "noreply@100xplatform.com")

    # Twilio SMS
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")

    # Claude AI API
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Analytics
    PLAUSIBLE_DOMAIN: str = os.getenv("PLAUSIBLE_DOMAIN", "100xplatform.com")

    # ===========================
    # FEATURE FLAGS
    # ===========================

    ENABLE_API_KEY_AUTH: bool = os.getenv("ENABLE_API_KEY_AUTH", "True").lower() == "true"
    ENABLE_JWT_AUTH: bool = os.getenv("ENABLE_JWT_AUTH", "True").lower() == "true"
    ENABLE_RATE_LIMITING: bool = os.getenv("ENABLE_RATE_LIMITING", "True").lower() == "true"
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "True").lower() == "true"
    ENABLE_REQUEST_LOGGING: bool = os.getenv("ENABLE_REQUEST_LOGGING", "True").lower() == "true"

    # ===========================
    # PERFORMANCE SETTINGS
    # ===========================

    # Request timeout (seconds)
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))

    # Max request size (bytes) - 10 MB default
    MAX_REQUEST_SIZE: int = int(os.getenv("MAX_REQUEST_SIZE", "10485760"))

    # Worker settings (for production)
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    WORKER_CLASS: str = os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")

    # ===========================
    # CACHE SETTINGS
    # ===========================

    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes default
    CACHE_MODULE_LIST_TTL: int = int(os.getenv("CACHE_MODULE_LIST_TTL", "3600"))  # 1 hour
    CACHE_USER_DATA_TTL: int = int(os.getenv("CACHE_USER_DATA_TTL", "1800"))  # 30 minutes

    # ===========================
    # MONITORING SETTINGS
    # ===========================

    # Sentry error tracking
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    SENTRY_ENVIRONMENT: str = ENVIRONMENT
    SENTRY_TRACES_SAMPLE_RATE: float = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0" if ENVIRONMENT == "production" else "0.1"))

    # Health check settings
    HEALTH_CHECK_INTERVAL: int = 60  # seconds
    SERVICE_TIMEOUT: int = 5  # seconds

    # ===========================
    # VALIDATORS
    # ===========================

    @validator("JWT_SECRET_KEY")
    def validate_jwt_secret(cls, v, values):
        """Ensure JWT secret is changed in production"""
        if values.get("ENVIRONMENT") == "production" and "change-in-production" in v:
            raise ValueError("JWT_SECRET_KEY must be changed in production!")
        return v

    @validator("PORT")
    def validate_port(cls, v):
        """Validate port number"""
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v

    @validator("JWT_EXPIRATION_HOURS")
    def validate_jwt_expiration(cls, v):
        """Validate JWT expiration time"""
        if v < 1 or v > 720:  # Max 30 days
            raise ValueError("JWT expiration must be between 1 and 720 hours")
        return v

    # ===========================
    # UTILITY METHODS
    # ===========================

    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT == "development"

    def is_staging(self) -> bool:
        """Check if running in staging environment"""
        return self.ENVIRONMENT == "staging"

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT == "production"

    def get_module_service_url(self, module_name: str) -> str:
        """Get service URL for a specific module"""
        module_url_map = {
            "fundraising": self.FUNDRAISING_SERVICE_URL,
            "marketing": self.MARKETING_SERVICE_URL,
            "design-hub": self.DESIGN_HUB_SERVICE_URL,
            "social-media": self.SOCIAL_MEDIA_SERVICE_URL,
            "customer-service": self.CUSTOMER_SERVICE_SERVICE_URL,
            "bookkeeping": self.BOOKKEEPING_SERVICE_URL,
            "email-campaigns": self.EMAIL_CAMPAIGNS_SERVICE_URL,
            "project-manager": self.PROJECT_MANAGER_SERVICE_URL,
            "testing-suite": self.TESTING_SUITE_SERVICE_URL,
            "shopping-cart": self.SHOPPING_CART_SERVICE_URL,
            "code-sandbox": self.CODE_SANDBOX_SERVICE_URL,
            "drone-system": self.DRONE_SYSTEM_SERVICE_URL,
            "voice-assistant": self.VOICE_ASSISTANT_SERVICE_URL,
            "video-editing": self.VIDEO_EDITING_SERVICE_URL,
            "podcast-production": self.PODCAST_PRODUCTION_SERVICE_URL,
            "stock-media": self.STOCK_MEDIA_SERVICE_URL,
            "music-production": self.MUSIC_PRODUCTION_SERVICE_URL,
            "content-repurposing": self.CONTENT_REPURPOSING_SERVICE_URL,
            "seo-content": self.SEO_CONTENT_SERVICE_URL,
            "corruption-mapping": self.CORRUPTION_MAPPING_SERVICE_URL,
            "pattern-security": self.PATTERN_SECURITY_SERVICE_URL,
            "law-module": self.LAW_MODULE_SERVICE_URL,
            "legal-documents": self.LEGAL_DOCUMENTS_SERVICE_URL,
            "spreadsheet-brain": self.SPREADSHEET_BRAIN_SERVICE_URL,
            "data-crystals": self.DATA_CRYSTALS_SERVICE_URL,
            "data-analytics": self.DATA_ANALYTICS_SERVICE_URL,
            "personal-trainer": self.PERSONAL_TRAINER_SERVICE_URL,
            "social-automation": self.SOCIAL_AUTOMATION_SERVICE_URL,
            "jarvis-assistant": self.JARVIS_ASSISTANT_SERVICE_URL,
            "dropshipping": self.DROPSHIPPING_SERVICE_URL,
        }
        return module_url_map.get(module_name, "")

    class Config:
        """Pydantic configuration"""
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# ===========================
# ENVIRONMENT-SPECIFIC CONFIGS
# ===========================

class DevelopmentSettings(Settings):
    """Development environment settings"""
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"


class StagingSettings(Settings):
    """Staging environment settings"""
    DEBUG: bool = False
    ENVIRONMENT: str = "staging"
    LOG_LEVEL: str = "INFO"


class ProductionSettings(Settings):
    """Production environment settings"""
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "WARNING"
    WORKERS: int = 8  # More workers for production


# ===========================
# SETTINGS FACTORY
# ===========================

def get_settings() -> Settings:
    """
    Get settings based on ENVIRONMENT variable.

    Returns appropriate settings class based on environment.
    """
    env = os.getenv("ENVIRONMENT", "development").lower()

    settings_map = {
        "development": DevelopmentSettings,
        "staging": StagingSettings,
        "production": ProductionSettings,
    }

    settings_class = settings_map.get(env, DevelopmentSettings)
    return settings_class()


# ===========================
# GLOBAL SETTINGS INSTANCE
# ===========================

settings = get_settings()


# ===========================
# CONFIGURATION SUMMARY
# ===========================

def print_config_summary():
    """Print configuration summary (for debugging)"""
    print("=" * 60)
    print(f"100X PLATFORM API GATEWAY - CONFIGURATION")
    print("=" * 60)
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Host: {settings.HOST}:{settings.PORT}")
    print(f"JWT Expiration: {settings.JWT_EXPIRATION_HOURS} hours")
    print(f"Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    print(f"Rate Limiting: {'Enabled' if settings.ENABLE_RATE_LIMITING else 'Disabled'}")
    print(f"API Key Auth: {'Enabled' if settings.ENABLE_API_KEY_AUTH else 'Disabled'}")
    print(f"JWT Auth: {'Enabled' if settings.ENABLE_JWT_AUTH else 'Disabled'}")
    print(f"Analytics: {'Enabled' if settings.ENABLE_ANALYTICS else 'Disabled'}")
    print(f"Log Level: {settings.LOG_LEVEL}")
    print(f"CORS Origins: {len(settings.ALLOWED_ORIGINS)} configured")
    print("=" * 60)


if __name__ == "__main__":
    print_config_summary()
