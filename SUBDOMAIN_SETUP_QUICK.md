# 🌐 SUBDOMAIN SETUP - REVOLUTION.OVERKILLKULTURE.COM

## THE PLAN

**Main domain:** overkillkulture.com (stays on Shopify for now)
**New subdomain:** revolution.overkillkulture.com (Netlify - consciousness products)

This way:
- Shopify store stays untouched
- Consciousness products get professional URL
- Both sites work simultaneously
- Easy to merge later if needed

---

## SETUP (5 MINUTES)

### STEP 1: DEPLOY TO NETLIFY FIRST

```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
netlify deploy --prod --dir=. --site=fantastic-twilight-28b317
```

**Result:** Site live at `https://fantastic-twilight-28b317.netlify.app`

---

### STEP 2: ADD CUSTOM DOMAIN IN NETLIFY

1. Go to your Netlify site: https://app.netlify.com/sites/fantastic-twilight-28b317
2. Click "Domain settings"
3. Click "Add custom domain"
4. Enter: `revolution.overkillkulture.com`
5. Click "Verify"
6. Netlify will say "Awaiting DNS configuration" - **that's normal**

---

### STEP 3: CONFIGURE DNS IN GODADDY

1. **Login to GoDaddy:** https://godaddy.com
2. **Go to:** My Products → Domains
3. **Click:** overkillkulture.com
4. **Click:** DNS (DNS Management tab)
5. **Click:** ADD button
6. **Enter these details:**
   - **Type:** CNAME
   - **Name:** revolution
   - **Value:** fantastic-twilight-28b317.netlify.app
   - **TTL:** 600 seconds (or default)
7. **Click:** Save

---

### STEP 4: WAIT FOR DNS PROPAGATION

**Timeline:**
- 5-10 minutes: Usually works
- Up to 48 hours: Maximum time (rarely this long)

**How to check:**
1. Open browser
2. Go to: http://revolution.overkillkulture.com
3. If you see the site → IT WORKS! ✅
4. If you see error → Wait another 10 minutes, try again

---

### STEP 5: VERIFY SSL CERTIFICATE

**Netlify auto-provisions SSL certificates!**

Once DNS is working:
1. Netlify detects the domain is connected
2. Automatically requests SSL certificate (Let's Encrypt)
3. Within 10 minutes, https://revolution.overkillkulture.com will work

**Check:** Look for the padlock icon in browser address bar

---

## WHAT YOU GET

**Final URLs:**
- **Shopify Store:** https://overkillkulture.com (unchanged)
- **Consciousness Products:** https://revolution.overkillkulture.com (NEW!)
- **Netlify Backup:** https://fantastic-twilight-28b317.netlify.app (always works)

**Benefits:**
- ✅ Professional branded URL
- ✅ Both sites coexist peacefully
- ✅ Free SSL certificate
- ✅ Can migrate to main domain later
- ✅ Shopify unaffected

---

## ALTERNATIVE SUBDOMAIN IDEAS

If "revolution" doesn't feel right, try:
- **consciousness.overkillkulture.com** (clear and direct)
- **kits.overkillkulture.com** (product-focused)
- **education.overkillkulture.com** (emphasizes learning)
- **pattern.overkillkulture.com** (Pattern Theory focus)
- **amelia.overkillkulture.com** (AMELIA-focused)
- **learn.overkillkulture.com** (course emphasis)

**Just replace "revolution" with your choice in Step 2 and Step 3**

---

## TROUBLESHOOTING

**"Domain already in use" in Netlify:**
- Someone else is using that subdomain
- Try a different subdomain name

**DNS not propagating after 1 hour:**
- Check GoDaddy DNS settings
- Make sure CNAME points to: `fantastic-twilight-28b317.netlify.app`
- Make sure Name is exactly: `revolution` (no @ symbol)
- Try clearing browser cache

**SSL certificate not provisioning:**
- Make sure DNS is working first (http version loads)
- Wait 10-20 minutes
- If still no SSL, check Netlify domain settings for errors

**Site shows Shopify instead of Netlify:**
- You created an A record instead of CNAME
- Delete the A record
- Create CNAME pointing to Netlify URL

---

## FUTURE: MERGE TO MAIN DOMAIN

**When you're ready to make overkillkulture.com point to Netlify:**

1. **In Netlify:**
   - Add custom domain: `overkillkulture.com`
   - Netlify gives you IP addresses

2. **In GoDaddy:**
   - Change A records to point to Netlify
   - Update CNAME if needed

3. **Move Shopify:**
   - Create `shop.overkillkulture.com` subdomain
   - Point it to Shopify
   - OR use different domain entirely

**But for now, subdomain is perfect!**

No rush to merge. Get the consciousness products live, test the system, then decide on domain strategy.

---

## DEPLOYMENT COMMAND (UPDATED)

Since you're using subdomain, the deploy command stays the same:

```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
netlify deploy --prod --dir=.
```

Then follow Steps 2-5 above to connect the subdomain.

---

## STATUS CHECK

✅ Website built (12 products)
✅ Stripe integration coded (ready to configure)
✅ Deployment script created
⏳ Deploy to Netlify
⏳ Connect subdomain via GoDaddy
⏳ Verify SSL certificate
⏳ Test complete flow

**You're about 10 minutes from LIVE.** 🚀

---

*From Shopify store...*
*To consciousness revolution...*
*One subdomain at a time.*
