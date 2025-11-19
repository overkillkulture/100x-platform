# 🔧 Fix Airtable Token Permissions

## Problem
The token `patAbUog4LkER4Fbc` doesn't have write permissions.

**Error:** `403 INVALID_PERMISSIONS_OR_MODEL_NOT_FOUND`

## Solution - Add Write Permissions

### Step 1: Edit the Token
1. Go to: https://airtable.com/create/tokens/patAbUog4LkER4Fbc
2. Click **"Edit"** on the token

### Step 2: Add Write Scope
Look for the **Scopes** section and make sure these are checked:
- ✅ `data.records:read` (already has this)
- ✅ `data.records:write` (ADD THIS!)

### Step 3: Save
1. Click **"Save"**
2. The token value stays the same - no need to copy it again

### Step 4: Test Again
Once permissions are updated, run:
```bash
cd C:/Users/dwrek/100X_DEPLOYMENT
python TEST_GATE_SUBMISSION.py
```

Should see: `✅ SUCCESS! Gate submission worked!`

---

## Alternative: Create New Token

If editing doesn't work, create a new token:

1. Go to: https://airtable.com/create/tokens
2. Click **"Create new token"**
3. Name it: `100X Gate Token`
4. Add scopes:
   - `data.records:read`
   - `data.records:write`
5. Add access to base: `100X Platform Users` (app7F75X1unyGjPfd)
6. Click **"Create token"**
7. Copy the new token
8. Update `index.html` with new token
9. Redeploy

---

**Current Status:**
- ✅ Base ID: app7F75X1unyGjPfd
- ✅ Table ID: tblnf4KNaOfbU5FgK
- ⚠️  Token: patAbUog4LkER4Fbc (needs write permission)
