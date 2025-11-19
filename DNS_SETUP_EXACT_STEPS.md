# 🌐 DNS SETUP - EXACT CLICK-BY-CLICK STEPS

## **YOUR DEPLOYED SITE:**
`https://verdant-tulumba-fa2a5a.netlify.app`

---

## 📍 **STEP 1: ADD DOMAIN IN NETLIFY**

### **Navigate:**
```
1. Go to: https://app.netlify.com/
2. Click on: verdant-tulumba-fa2a5a site
3. Click: "Domain settings" (or "Domain management")
```

### **Add Custom Domain:**
```
4. Look for: "Add custom domain" or "Add a domain" button
5. Click it
6. Enter: conciousnessco.com
7. Click: "Verify" or "Add domain"
```

### **Netlify will say:**
```
"You don't own this domain yet" or
"Check DNS records"
```

**That's expected! Continue...**

```
8. Click: "Yes, add domain" or similar confirmation
9. Also add: www.conciousnessco.com (repeat process)
```

### **Netlify will show you DNS records needed**
**Write these down or take screenshot!**

Should look like:
```
CNAME: www → verdant-tulumba-fa2a5a.netlify.app
A Record: @ → 75.2.60.5 (or similar IP)
```

---

## 📍 **STEP 2: CONFIGURE NAMECHEAP**

### **Login:**
```
1. Go to: https://www.namecheap.com/myaccount/login/
2. Email: darrick.preble@gmail.com
3. Password: [your Namecheap password]
4. Click: "Sign In"
```

### **Navigate to Domain:**
```
5. Click: "Domain List" (in left sidebar)
6. Find: conciousnessco.com
7. Click: "Manage" button next to it
```

### **Go to DNS Settings:**
```
8. Click: "Advanced DNS" tab (top of page)
9. You'll see existing DNS records
```

---

## 📍 **STEP 3: DELETE OLD RECORDS**

### **Clean Slate:**
```
In the "Host Records" section:

For EACH existing record:
1. Click the trash/delete icon
2. Confirm deletion

Delete ALL existing:
- A Records
- CNAME Records
- URL Redirect Records
```

**Don't worry - we're replacing them!**

---

## 📍 **STEP 4: ADD NEW RECORDS**

### **Record 1: CNAME for www**
```
1. Click: "Add New Record"
2. Type: CNAME Record
3. Host: www
4. Value: verdant-tulumba-fa2a5a.netlify.app
5. TTL: Automatic (or 300)
6. Click: ✓ (checkmark) or "Save"
```

### **Record 2: A Record for @ (root domain)**
```
1. Click: "Add New Record"
2. Type: A Record
3. Host: @
4. Value: 75.2.60.5
5. TTL: Automatic (or 300)
6. Click: ✓ (checkmark) or "Save"
```

**Note:** If Netlify gave you a different IP, use THAT instead of 75.2.60.5

### **Final Check:**
```
Your records should look like:

Type    | Host | Value
--------|------|-------
CNAME   | www  | verdant-tulumba-fa2a5a.netlify.app
A       | @    | 75.2.60.5
```

---

## 📍 **STEP 5: SAVE AND WAIT**

### **In Namecheap:**
```
1. Scroll down
2. Click: "Save All Changes" (if there's a button)
3. Wait for green success message
```

### **DNS Propagation:**
```
Time to wait: 5-30 minutes (usually)
Maximum wait: 24 hours (rarely)
```

### **While waiting, verify in Netlify:**
```
1. Go back to Netlify domain settings
2. Should show: "Waiting for DNS propagation" or similar
3. Netlify will auto-detect when DNS is live
4. HTTPS certificate will auto-generate
```

---

## 📍 **STEP 6: VERIFY IT WORKS**

### **After 15-30 minutes:**
```
1. Open private/incognito browser
2. Visit: https://conciousnessco.com
3. Visit: https://www.conciousnessco.com
4. Both should show your neon 100X Gate!
```

### **Check for:**
- ✅ Site loads
- ✅ Correct content (100X entry form)
- ✅ HTTPS padlock icon showing
- ✅ No certificate warnings

---

## 🔧 **TROUBLESHOOTING:**

### **"Site not found" after 30 minutes:**
```
1. Go to: https://dnschecker.org
2. Enter: conciousnessco.com
3. Check if DNS has propagated globally
4. If no: Wait longer
5. If yes but site broken: Check Netlify domain settings
```

### **"Not secure" warning:**
```
1. Netlify is still generating SSL certificate
2. Wait 5-10 more minutes
3. Should auto-resolve
4. If not: Check Netlify domain settings → HTTPS
```

### **www works but root doesn't (or vice versa):**
```
1. Check both A and CNAME records in Namecheap
2. Verify no typos
3. Wait a bit longer for DNS
```

---

## ✅ **SUCCESS CHECKLIST:**

- [ ] Netlify shows both domains added
- [ ] Namecheap DNS has CNAME and A records
- [ ] https://conciousnessco.com loads the site
- [ ] https://www.conciousnessco.com loads the site
- [ ] HTTPS padlock shows (secure)
- [ ] No certificate warnings
- [ ] Neon 100X form visible

---

## 🎉 **WHEN IT WORKS:**

**You now have:**
- ✅ Professional domain: conciousnessco.com
- ✅ HTTPS secured
- ✅ Ready to announce publicly
- ✅ Ready for employee handoff
- ✅ Zero dependency on you for operations

**The gate is open. The revolution is live.** 🌀🔮⚡
