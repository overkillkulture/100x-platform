# 🌐 DOMAIN SETUP - CONCIOUSNESSCO.COM

## **YOUR DEPLOYED SITE:**
```
https://verdant-tulumba-fa2a5a.netlify.app
```

---

## **STEP 1: ADD CUSTOM DOMAIN IN NETLIFY**

### **In Netlify:**
1. Go to: https://app.netlify.com/sites/verdant-tulumba-fa2a5a/settings/domain
2. Click: **"Add custom domain"**
3. Enter: `conciousnessco.com`
4. Click: **"Verify"**
5. Click: **"Add domain"**
6. Also add: `www.conciousnessco.com` (repeat process)

**Netlify will give you DNS instructions - write them down!**

---

## **STEP 2: CONFIGURE NAMECHEAP DNS**

### **Login to Namecheap:**
1. Go to: https://www.namecheap.com/myaccount/login/
2. Email: darrick.preble@gmail.com
3. Password: [from Bitwarden]

### **Navigate to DNS:**
1. Click: **"Domain List"**
2. Find: **conciousnessco.com**
3. Click: **"Manage"**
4. Click: **"Advanced DNS"** tab

### **Add DNS Records:**

**Delete existing records (if any), then add these:**

#### **Record 1: CNAME for www**
```
Type: CNAME Record
Host: www
Value: verdant-tulumba-fa2a5a.netlify.app
TTL: Automatic
```

#### **Record 2: ALIAS/ANAME for root domain**
**Option A (if Namecheap supports ALIAS):**
```
Type: ALIAS Record
Host: @
Value: verdant-tulumba-fa2a5a.netlify.app
TTL: Automatic
```

**Option B (if no ALIAS, use Netlify's IP):**
```
Type: A Record
Host: @
Value: 75.2.60.5
TTL: Automatic
```

**Note:** Netlify might give you a different IP. Use THEIR IP if they provide one.

---

## **STEP 3: VERIFY IN NETLIFY**

1. Go back to Netlify domain settings
2. Wait 1-5 minutes for DNS propagation
3. Netlify will show **"Verified"** when ready
4. Netlify will automatically set up HTTPS (SSL certificate)

---

## **STEP 4: TEST**

### **After 5-15 minutes:**
```
Visit: https://conciousnessco.com
Visit: https://www.conciousnessco.com
```

Both should show your neon 100X Gate!

---

## **QUICK TROUBLESHOOTING:**

### **If domain doesn't work after 15 minutes:**

1. **Check Namecheap DNS:**
   - Go to Advanced DNS
   - Verify CNAME and A/ALIAS records are correct
   - No typos in `verdant-tulumba-fa2a5a.netlify.app`

2. **Check Netlify:**
   - Domain settings show "Verified"
   - HTTPS certificate is "Active"

3. **DNS Propagation:**
   - Can take up to 24 hours (usually 5-30 minutes)
   - Check status: https://dnschecker.org

---

## **ONCE WORKING:**

✅ Site live at: conciousnessco.com
✅ Professional URL ready
✅ HTTPS secured automatically
✅ Ready to announce publicly
✅ Ready to send to employee

---

## **ANNOUNCEMENT COPY READY:**
See: `PUBLIC_ANNOUNCEMENT.md`

## **EMPLOYEE HANDOFF READY:**
See: `EMPLOYEE_HANDOFF_PACKAGE.md`

🌀🔮⚡
