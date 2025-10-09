# ⚡ DEPLOY TO CONCIOUSNESSCO.COM - RIGHT NOW ⚡

## YOUR DOMAIN: conciousnessco.com
**Registered:** Oct 6, 2025
**Login:** darrick.preble@gmail.com
**Registrar:** Namecheap

## FASTEST DEPLOY (2 MINUTES):

### STEP 1: Netlify Drag & Drop
1. Go to: https://app.netlify.com/drop
2. Drag folder: `C:\Users\dwrek\100X_DEPLOYMENT`
3. Get instant URL like: `https://something-123.netlify.app`

### STEP 2: Point Domain
In Netlify (after upload):
1. Site settings → Domain management
2. Add custom domain: **conciousnessco.com**
3. Netlify gives you the DNS records

### STEP 3: Update Namecheap DNS
1. Login: https://namecheap.com (darrick.preble@gmail.com)
2. Go to: Domain List → conciousnessco.com → Advanced DNS
3. **DELETE** existing redirect records
4. **ADD** these records:

```
Type: A Record
Host: @
Value: 75.2.60.5
TTL: Automatic
```

```
Type: CNAME Record
Host: www
Value: [your-site].netlify.app
TTL: Automatic
```

## DONE!
Site will be live at **https://conciousnessco.com** in 5-10 minutes!

---

## ALTERNATIVE: Use Namecheap Redirect (30 seconds)

**FASTEST IF YOU ALREADY HAVE A NETLIFY SITE:**

1. Get your Netlify URL: https://app.netlify.com
2. Go to Namecheap → conciousnessco.com → Domain
3. Find "Redirect Domain" section
4. Change from: http://www.conciousnessco.com/
5. Change to: https://[YOUR-NETLIFY-URL].netlify.app
6. Save

**BOOM - LIVE IN 30 SECONDS!**
