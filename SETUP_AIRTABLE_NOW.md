# 🔐 AIRTABLE SETUP - GET THE GATE WORKING

## 🎯 WHAT WE NEED

The gate is failing because we need **real** Airtable credentials. Here's how to get them:

---

## 📋 STEP 1: CREATE AIRTABLE BASE

1. Go to: https://airtable.com
2. Log in (or create free account)
3. Click **"Create a base"**
4. Name it: **"100X Builders"**
5. Create a table named: **"Submissions"**

---

## 📋 STEP 2: SET UP TABLE FIELDS

In your "Submissions" table, create these fields:

| Field Name | Field Type |
|------------|------------|
| Name | Single line text |
| Email | Email |
| Phone | Phone number |
| Mission | Long text |
| Values | Long text |
| Submitted | Date and time |

---

## 📋 STEP 3: GET YOUR BASE ID

**Method 1: From URL**
- Open your base
- Look at the URL: `https://airtable.com/appXXXXXXXXXXXXXX/...`
- The part after `airtable.com/` starting with `app` is your Base ID
- Example: `appD0L28VPIzkSDQk`

**Method 2: From API Documentation**
- Open your base
- Click "Help" menu (top right)
- Click "API Documentation"
- Your Base ID is shown at the top

---

## 📋 STEP 4: CREATE PERSONAL ACCESS TOKEN

1. Go to: https://airtable.com/create/tokens
2. Click **"Create new token"**
3. Name it: **"100X Gate"**
4. Under **Scopes**, select:
   - ✅ `data.records:read`
   - ✅ `data.records:write`
5. Under **Access**, add your base:
   - Click "Add a base"
   - Select "100X Builders"
6. Click **"Create token"**
7. **COPY THE TOKEN** (you can't see it again!)

---

## 📋 STEP 5: UPDATE THE CREDENTIALS

Once you have:
- ✅ Base ID (starts with `app`)
- ✅ Personal Access Token (starts with `pat`)
- ✅ Table Name (probably "Submissions")

Run this command:

```bash
python UPDATE_GATE_CREDENTIALS.py
```

It will prompt you for each value and update the gate automatically.

---

## 🧪 STEP 6: TEST IT

After updating credentials:

```bash
python TEST_GATE_WITH_REAL_CREDENTIALS.py
```

This will:
1. Test Airtable connection
2. Submit a test record
3. Verify it arrives in your base
4. Report success/failure

---

## ⚡ QUICK START (IF YOU'RE READY NOW)

If you have your Airtable account ready:

1. Tell me your Base ID
2. Tell me your Personal Access Token
3. Tell me your Table Name

I'll update the gate immediately and redeploy.

---

## 🔒 SECURITY NOTE

The Personal Access Token is sensitive. We can:
- **Option A:** Put it directly in the HTML (quick, but exposed in source code)
- **Option B:** Create a backend proxy (more secure, but more complex)

For the 100X gate screening builders, **Option A is probably fine** - we're filtering for consciousness, not protecting bank accounts.

---

**Ready to set this up?** Give me the credentials and I'll have it working in 2 minutes.
