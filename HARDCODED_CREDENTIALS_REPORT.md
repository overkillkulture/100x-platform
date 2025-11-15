# Hardcoded Credentials Audit Report

## Summary

Found **39+ hardcoded credentials** across the codebase that need to be moved to environment variables.

## Critical Security Issues

### 🔴 HIGH PRIORITY - Exposed in Git

These credentials are currently committed to the repository and should be rotated immediately:

1. **Airtable Tokens**
   - `pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757`
   - `patAbUog4LkER4Fbc.e2942db8dca37f951ad341e47796c5d23b268607341bb0603726e5ac006dee1a`

2. **GitHub Token**
   - `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`

3. **Twilio Credentials**
   - Password: `Kill50780630#`
   - Auth Token: `340ca721c94a987177658a47bcf5a0d8`

4. **Gmail App Password**
   - `gzzvemuxppfnjsup`

5. **Commander API Key**
   - `ck_7pkwpCvVV6iFgMtrEaKDjtvJT1J4WraUdYgbi6-Lf7Q`

## Files Containing Hardcoded Credentials

### Airtable Tokens
- `ADD_AIRTABLE_FIELDS.py` (line 7)
- `CHECK_TEST_ENTRY.py` (line 7)
- `CHECK_SCORES.py` (line 3)
- `AIRTABLE_CONNECTION_TEST.py` (line 5)
- `CHECK_AIRTABLE_DATA.py` (line 3)
- `CREATE_BUG_TABLE.py` (line 9)
- `ADD_AIRTABLE_FIELDS_REAL.py` (line 8)
- `DISCOVER_AIRTABLE_INFO.py` (line 7)
- `GET_AIRTABLE_FIELD_NAMES.py` (line 8)

### Twilio Credentials
- `CONFIGURE_TWILIO_WEBHOOK.py` (line 13)
- `BUG_SMS_NOTIFIER_DOBBS.py` (line 16)
- `BUG_MONITOR_BACKGROUND.py` (line 16)
- `BUG_MONITOR_24_7.py` (line 16)

### Email Credentials
- `BUG_EMAIL_NOTIFIER.py` (line 19)
- `EMAIL_BUG_NOTIFIER.py` (line 19)
- `AUTO_SEND_BUILDER_PACKAGE.py` (line 20)

### GitHub Token
- `test_github_token.py` (line 6)

### API Keys
- `API_SERVER_SIMPLE.py` (line 18) - Commander API Key

## Immediate Actions Required

### 1. Rotate All Credentials

**Do this FIRST before anything else:**

- [ ] Airtable: Generate new Personal Access Tokens
- [ ] GitHub: Revoke `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` and create new
- [ ] Twilio: Reset Auth Token
- [ ] Gmail: Revoke app password and create new
- [ ] Commander API: Generate new API key

### 2. Create .env File

```bash
cp .env.example .env
```

Fill in with NEW credentials (not the old ones).

### 3. Update Each File

For each file listed above, replace hardcoded value with:

```python
import os

# Before:
AIRTABLE_TOKEN = "pat8DtOnZ1crQT56g..."

# After:
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
if not AIRTABLE_TOKEN:
    raise ValueError("AIRTABLE_TOKEN environment variable not set")
```

### 4. Add to .gitignore

Ensure `.env` is in `.gitignore`:

```bash
echo ".env" >> .gitignore
```

### 5. Remove from Git History

These credentials are in git history. Consider:

```bash
# WARNING: This rewrites history. Coordinate with team first.
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch ADD_AIRTABLE_FIELDS.py" \
  --prune-empty --tag-name-filter cat -- --all
```

Or use tools like:
- `git-filter-repo`
- `BFG Repo-Cleaner`

## Migration Checklist

### Phase 1: Airtable (9 files)
- [ ] `ADD_AIRTABLE_FIELDS.py`
- [ ] `CHECK_TEST_ENTRY.py`
- [ ] `CHECK_SCORES.py`
- [ ] `AIRTABLE_CONNECTION_TEST.py`
- [ ] `CHECK_AIRTABLE_DATA.py`
- [ ] `CREATE_BUG_TABLE.py`
- [ ] `ADD_AIRTABLE_FIELDS_REAL.py`
- [ ] `DISCOVER_AIRTABLE_INFO.py`
- [ ] `GET_AIRTABLE_FIELD_NAMES.py`

### Phase 2: Twilio (4 files)
- [ ] `CONFIGURE_TWILIO_WEBHOOK.py`
- [ ] `BUG_SMS_NOTIFIER_DOBBS.py`
- [ ] `BUG_MONITOR_BACKGROUND.py`
- [ ] `BUG_MONITOR_24_7.py`

### Phase 3: Email (3 files)
- [ ] `BUG_EMAIL_NOTIFIER.py`
- [ ] `EMAIL_BUG_NOTIFIER.py`
- [ ] `AUTO_SEND_BUILDER_PACKAGE.py`

### Phase 4: Other (2 files)
- [ ] `test_github_token.py`
- [ ] `API_SERVER_SIMPLE.py`

## Example Migration

### Before (ADD_AIRTABLE_FIELDS.py)
```python
AIRTABLE_TOKEN = "pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757"
```

### After
```python
import os

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
if not AIRTABLE_TOKEN:
    raise ValueError(
        "AIRTABLE_TOKEN not set. "
        "Please set it in .env file or environment variables."
    )
```

## Testing After Migration

1. Set environment variables in `.env`
2. Run each script individually:
   ```bash
   python ADD_AIRTABLE_FIELDS.py
   ```
3. Verify it works with env vars
4. Check no hardcoded values remain:
   ```bash
   grep -r "pat8DtOnZ1crQT56g" .
   grep -r "patAbUog4LkER4Fbc" .
   grep -r "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" .
   ```

## Prevention

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check for potential secrets
if git diff --cached | grep -E "(pat[A-Za-z0-9]{30,}|ghp_[A-Za-z0-9]{36}|sk-[A-Za-z0-9]{48})"; then
    echo "ERROR: Potential secret detected in commit!"
    exit 1
fi
```

### Use Secret Scanners

- `git-secrets` - AWS Labs tool
- `detect-secrets` - Yelp tool
- `truffleHog` - Searches git history
- GitHub Secret Scanning (enable in repo settings)

## Notes

- The gate files (100X_GATE_*.py) already use `os.getenv("AIRTABLE_TOKEN")` - good!
- `BACKEND/auth_system.py` already uses env vars properly - good!
- Most issues are in utility/test scripts

## Estimated Time

- Rotating credentials: 30 minutes
- Updating code: 2 hours
- Testing: 1 hour
- Total: ~3.5 hours

## Owner

Trinity Instance C1 - Mechanic Role

## Status

🔴 **CRITICAL** - Active credentials exposed in repository
