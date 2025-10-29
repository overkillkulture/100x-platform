# 100X Platform - Bug Tracker

**Last Updated**: October 29, 2025

---

## 🔴 CRITICAL BUGS

### BUG-002: Insecure password hashing in server.js
- **Status**: IDENTIFIED
- **Severity**: CRITICAL - Security vulnerability
- **Reported**: October 29, 2025
- **Description**: server.js uses SHA256 for password hashing (line 48-50), which is NOT secure for passwords. SHA256 is fast and can be brute-forced.
- **Files Affected**: server.js:48-50
- **Expected Behavior**: Use bcrypt with proper salt rounds (already implemented in server-production.js)
- **Actual Behavior**: Uses crypto.createHash('sha256') which is vulnerable
- **Impact**: User passwords in database.json could be compromised if leaked
- **Recommendation**:
  - server.js is for local development only
  - Ensure production uses server-production.js which has bcrypt
  - Consider migrating existing user passwords or warning users
  - Document that server.js is DEV ONLY

---

## 🟡 MEDIUM PRIORITY

### BUG-001: Missing message from Computer one
- **Status**: INVESTIGATING
- **Description**: User reports "Computer one" left an urgent message at coordination/messages/122.md but file doesn't exist
- **Impact**: Possible communication breakdown between Claude instances
- **Next Steps**: Created coordination directory structure, waiting for clarification

### BUG-003: Hardcoded session secret in server.js
- **Status**: IDENTIFIED
- **Severity**: MEDIUM - Security issue for local dev
- **Reported**: October 29, 2025
- **Description**: server.js has hardcoded session secret 'consciousness-revolution-2025' (line 19)
- **Files Affected**: server.js:19
- **Expected Behavior**: Use environment variable
- **Actual Behavior**: Hardcoded string
- **Impact**: Session hijacking possible in local development if attacker knows the secret
- **Recommendation**:
  - This is OK for local dev only
  - Ensure production uses server-production.js with SESSION_SECRET env var
  - Add warning comment in code

### BUG-004: Weak fallback session secret in server-production.js
- **Status**: IDENTIFIED
- **Severity**: MEDIUM - Security issue if deployed without env var
- **Reported**: October 29, 2025
- **Description**: server-production.js has fallback 'change-this-in-production' if SESSION_SECRET not set (lines 246, 264)
- **Files Affected**: server-production.js:246, 264
- **Expected Behavior**: Fail fast if SESSION_SECRET not provided
- **Actual Behavior**: Falls back to weak default
- **Impact**: If deployed without env var, sessions are insecure
- **Recommendation**: Throw error if SESSION_SECRET not set, don't use fallback

---

## 🟢 LOW PRIORITY / ENHANCEMENTS

### ENHANCE-001: Trinity AI not integrated
- **Status**: DOCUMENTED
- **Reported**: October 29, 2025
- **Description**: TODO comment at server.js:351 - Trinity AI chat uses mock responses, not real Anthropic API
- **Files Affected**: server.js:351-363
- **Impact**: Feature incomplete - users get canned responses
- **Next Steps**: Need Anthropic API key and integration code
- **Priority**: LOW - mock responses work for alpha testing

---

## ✅ RESOLVED BUGS

None yet.

---

## 📋 BUG REPORT TEMPLATE

```markdown
### BUG-XXX: [Short description]
- **Status**: NEW / IN_PROGRESS / RESOLVED
- **Severity**: CRITICAL / MEDIUM / LOW
- **Reported**: [Date]
- **Reported By**: [Name/Session ID]
- **Description**: [Detailed description]
- **Steps to Reproduce**:
  1.
  2.
  3.
- **Expected Behavior**:
- **Actual Behavior**:
- **Impact**:
- **Files Affected**:
- **Next Steps**:
```

---

## 🔍 CODE REVIEW NOTES

### Areas to Review
- [ ] server.js - Main backend logic
- [ ] server-production.js - Production configuration
- [ ] database.json - User data integrity
- [ ] SSL/HTTPS configuration
- [ ] Authentication security
- [ ] Genesis key system
