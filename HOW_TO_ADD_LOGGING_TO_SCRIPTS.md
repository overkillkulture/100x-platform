# 📝 How to Add Error Logging to Python Scripts

## Quick Start (2 Lines of Code!)

Add these 2 lines to the top of ANY Python script:

```python
from UNIVERSAL_ERROR_LOGGER import setup_logging, log_error
logger = setup_logging(__file__)
```

Then replace `print()` statements with:
- `logger.info("message")` - Normal info
- `logger.warning("message")` - Warnings
- `logger.error("message")` - Errors
- `logger.debug("message")` - Debug info

## Example: Before & After

### BEFORE (No Logging):
```python
def check_microphone():
    print("Checking microphone...")
    try:
        # Do something
        print("Microphone OK")
    except Exception as e:
        print(f"Error: {e}")
```

### AFTER (With Logging):
```python
from UNIVERSAL_ERROR_LOGGER import setup_logging, log_error
logger = setup_logging(__file__)

def check_microphone():
    logger.info("Checking microphone...")
    try:
        # Do something
        logger.info("Microphone OK")
    except Exception as e:
        log_error(logger, e, context={'function': 'check_microphone'})
```

## What You Get:

1. **Daily Log Files** - `LOGS/SCRIPT_NAME_2025-10-26.log`
2. **Combined System Log** - `LOGS/ALL_SYSTEMS_2025-10-26.log`
3. **Error JSON Log** - `LOGS/ERRORS_2025-10-26.jsonl` (for parsing)
4. **User Actions Log** - `LOGS/USER_ACTIONS_2025-10-26.jsonl`

## Advanced Usage:

### Log API Calls:
```python
from UNIVERSAL_ERROR_LOGGER import log_api_call
log_api_call(logger, '/api/chat', 'POST', 200, duration_ms=150)
```

### Log User Actions:
```python
from UNIVERSAL_ERROR_LOGGER import log_user_action
log_user_action(logger, 'submitted_bug', user_email='shaman@test.com',
                details={'bug_title': 'Login broken'})
```

### Auto-log Functions (Decorator):
```python
from UNIVERSAL_ERROR_LOGGER import logged_function

@logged_function
def my_function(arg1, arg2):
    # This function will automatically log calls and errors
    return arg1 + arg2
```

## Where Logs Are Saved:

```
C:/Users/dwrek/100X_DEPLOYMENT/LOGS/
├── AUTO_BUG_FIXER_DAEMON_2025-10-26.log
├── ARAYA_INTELLIGENT_API_2025-10-26.log
├── ALL_SYSTEMS_2025-10-26.log
├── ERRORS_2025-10-26.jsonl
└── USER_ACTIONS_2025-10-26.jsonl
```

## Benefits:

✅ **Debug Faster** - See exactly what happened and when
✅ **Track Errors** - All errors saved with full stack traces
✅ **Monitor Users** - See what users are doing
✅ **API Monitoring** - Track all API calls and performance
✅ **No Data Loss** - Everything logged to files automatically

## Priority Scripts to Update:

1. ✅ AUTO_BUG_FIXER_DAEMON.py - UPDATED
2. ARAYA_INTELLIGENT_API.py
3. CONVERSATION_LOGGER.py
4. VISITOR_INTELLIGENCE_SYSTEM.py
5. THE_OBSERVATORY.py
6. LIVE_ANALYTICS_API.py

## Quick Update Script:

Run this to add logging to all critical scripts:
```bash
python ADD_LOGGING_TO_ALL_SCRIPTS.py
```

(See that file for automatic integration)
