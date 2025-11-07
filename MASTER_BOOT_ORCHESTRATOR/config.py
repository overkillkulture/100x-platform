"""
MASTER BOOT ORCHESTRATOR - CONFIGURATION
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "orchestrator.db"
LOG_DIR = BASE_DIR / "logs"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Ensure directories exist
LOG_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Server Configuration
API_HOST = "127.0.0.1"
API_PORT = 8888
API_KEY = os.getenv("ORCHESTRATOR_API_KEY", "consciousness-revolution-key-2025")

# Health Check Defaults
DEFAULT_HEALTH_CHECK_INTERVAL = 30  # seconds
DEFAULT_HEALTH_CHECK_TIMEOUT = 5  # seconds
MAX_HEALTH_CHECK_FAILURES = 3  # failures before marking as DOWN

# Auto-Healing Configuration
MAX_HEAL_ATTEMPTS = 3
HEAL_RETRY_DELAY = 10  # seconds
HEAL_BACKOFF_MULTIPLIER = 2  # exponential backoff

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_RETENTION_DAYS = 30

# Seven Domains
SEVEN_DOMAINS = [
    "Physical (CHAOS FORGE)",
    "Financial (QUANTUM VAULT)",
    "Mental (MIND MATRIX)",
    "Emotional (SOUL SANCTUARY)",
    "Social (REALITY FORGE)",
    "Creative (ARKITEK ACADEMY)",
    "Integration (NEXUS TERMINAL)"
]

# Service Types
SERVICE_TYPES = [
    "python_server",
    "node_server",
    "bash_script",
    "windows_service",
    "database",
    "monitoring",
    "custom"
]

# Notification Settings
ENABLE_DESKTOP_NOTIFICATIONS = True
ENABLE_EMAIL_NOTIFICATIONS = False
EMAIL_ON_FAILURE_ONLY = True
