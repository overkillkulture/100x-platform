"""
UNIVERSAL ERROR LOGGER
Import this module to add automatic error logging to any Python script

Usage:
    from UNIVERSAL_ERROR_LOGGER import setup_logging, log_error

    logger = setup_logging(__file__)
    logger.info("Script started")
    logger.error("Something went wrong")
"""

import logging
import os
import sys
from datetime import datetime
import traceback
import json

# Ensure logs directory exists
LOG_DIR = 'C:/Users/dwrek/100X_DEPLOYMENT/LOGS'
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging(script_name, level=logging.INFO):
    """
    Set up logging for a Python script

    Args:
        script_name: Name of the script (use __file__)
        level: Logging level (default: INFO)

    Returns:
        logger object
    """
    # Get script basename without path
    script_basename = os.path.basename(script_name).replace('.py', '')

    # Create logger
    logger = logging.getLogger(script_basename)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create formatters
    detailed_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler - daily log file
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f'{script_basename}_{today}.log')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    # Also write to combined log
    combined_log = os.path.join(LOG_DIR, f'ALL_SYSTEMS_{today}.log')
    combined_handler = logging.FileHandler(combined_log, encoding='utf-8')
    combined_handler.setLevel(logging.INFO)
    combined_handler.setFormatter(detailed_formatter)
    logger.addHandler(combined_handler)

    # Console handler - still print to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

def log_error(logger, error, context=None):
    """
    Log an error with full traceback and context

    Args:
        logger: Logger object
        error: Exception object
        context: Optional dict with additional context
    """
    error_data = {
        'timestamp': datetime.now().isoformat(),
        'error_type': type(error).__name__,
        'error_message': str(error),
        'traceback': traceback.format_exc(),
        'context': context or {}
    }

    # Log to file
    logger.error(f"ERROR: {error_data['error_type']} - {error_data['error_message']}")
    logger.debug(f"Traceback:\n{error_data['traceback']}")

    # Also save to JSON error log
    today = datetime.now().strftime('%Y-%m-%d')
    error_log = os.path.join(LOG_DIR, f'ERRORS_{today}.jsonl')
    with open(error_log, 'a', encoding='utf-8') as f:
        f.write(json.dumps(error_data) + '\n')

def log_api_call(logger, endpoint, method, status_code, duration_ms):
    """Log API calls for monitoring"""
    logger.info(f"API {method} {endpoint} - {status_code} ({duration_ms}ms)")

def log_user_action(logger, action, user_email=None, details=None):
    """Log user actions for analytics"""
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'user_email': user_email or 'anonymous',
        'details': details or {}
    }
    logger.info(f"USER ACTION: {action} - {user_email or 'anonymous'}")

    # Save to user actions log
    today = datetime.now().strftime('%Y-%m-%d')
    actions_log = os.path.join(LOG_DIR, f'USER_ACTIONS_{today}.jsonl')
    with open(actions_log, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_data) + '\n')

# Example usage wrapper
def logged_function(func):
    """Decorator to automatically log function calls and errors"""
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        try:
            logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            log_error(logger, e, context={'function': func.__name__, 'args': str(args), 'kwargs': str(kwargs)})
            raise
    return wrapper

if __name__ == '__main__':
    # Test the logger
    logger = setup_logging(__file__)
    logger.info("✅ Universal Error Logger Test")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")

    try:
        1 / 0
    except Exception as e:
        log_error(logger, e, context={'test': 'division by zero'})

    log_user_action(logger, 'test_action', user_email='test@example.com', details={'test_key': 'test_value'})

    print(f"\n✅ Logs saved to: {LOG_DIR}")
    print("Check the following files:")
    print(f"  - UNIVERSAL_ERROR_LOGGER_{datetime.now().strftime('%Y-%m-%d')}.log")
    print(f"  - ALL_SYSTEMS_{datetime.now().strftime('%Y-%m-%d')}.log")
    print(f"  - ERRORS_{datetime.now().strftime('%Y-%m-%d')}.jsonl")
    print(f"  - USER_ACTIONS_{datetime.now().strftime('%Y-%m-%d')}.jsonl")
