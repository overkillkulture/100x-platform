"""
TRINITY FOUNDATION - CENTRALIZED CONFIGURATION
Single source of truth for all environment variables and settings
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Centralized configuration service
    Provides clean interface for accessing all configuration values
    """

    # API Keys
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

    # Airtable
    AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN', '')
    AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', '')

    # Payment Processing
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')

    # Communication Services
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')

    # Social Media
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
    INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN', '')

    # GitHub
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')

    # AI Services
    STABLE_DIFFUSION_API_KEY = os.getenv('STABLE_DIFFUSION_API_KEY', '')
    RUNWAY_API_KEY = os.getenv('RUNWAY_API_KEY', '')

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/consciousness_revolution')

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.urandom(32).hex())

    # API Gateway
    GATEWAY_PORT = int(os.getenv('GATEWAY_PORT', '8080'))
    GATEWAY_HOST = os.getenv('GATEWAY_HOST', '0.0.0.0')

    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # CORS
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return getattr(cls, key, default)

    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """
        Get all configuration values (excluding sensitive data)

        Returns:
            Dictionary of configuration values
        """
        config_dict = {}
        sensitive_keys = ['SECRET', 'KEY', 'TOKEN', 'PASSWORD', 'SID']

        for key in dir(cls):
            if key.isupper() and not key.startswith('_'):
                value = getattr(cls, key)
                # Mask sensitive values
                if any(sensitive in key for sensitive in sensitive_keys):
                    config_dict[key] = '***MASKED***' if value else 'NOT_SET'
                else:
                    config_dict[key] = value

        return config_dict

    @classmethod
    def is_configured(cls, key: str) -> bool:
        """
        Check if a configuration value is set

        Args:
            key: Configuration key

        Returns:
            True if configured, False otherwise
        """
        value = getattr(cls, key, None)
        return bool(value)

    @classmethod
    def validate(cls) -> Dict[str, bool]:
        """
        Validate that all required configuration is present

        Returns:
            Dictionary of validation results
        """
        required_keys = [
            'JWT_SECRET_KEY',
            'DATABASE_URL',
            'GATEWAY_PORT'
        ]

        results = {}
        for key in required_keys:
            results[key] = cls.is_configured(key)

        return results

# Singleton instance
config = Config()

# Export for easy import
__all__ = ['Config', 'config']
