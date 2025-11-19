# 🚀 STRIPE API - QUICK START GUIDE

## STEP 1: CREATE STRIPE ACCOUNT (5 minutes)

1. Go to: **https://dashboard.stripe.com/register**
2. Sign up with email
3. Verify email
4. Complete business profile (can use personal info for now)

**Done!** ✅

---

## STEP 2: GET YOUR API KEYS (1 minute)

1. Go to: **https://dashboard.stripe.com/test/apikeys**
2. You'll see two keys:
   - **Publishable key** (starts with `pk_test_`)
   - **Secret key** (starts with `sk_test_`) - **CLICK "Reveal test key"**

3. Copy the **Secret key** (sk_test_...)

---

## STEP 3: CONFIGURE THE SCRIPT (1 minute)

1. Open: `C:\Users\dwrek\100X_DEPLOYMENT\STRIPE_API_SETUP.py`

2. Find this line (near top):
   ```python
   stripe.api_key = "sk_test_YOUR_SECRET_KEY_HERE"
   ```

3. Replace with YOUR secret key:
   ```python
   stripe.api_key = "sk_test_51ABC123..."  # Your actual key
   ```

4. Save file

---

## STEP 4: INSTALL STRIPE LIBRARY (30 seconds)

```bash
pip install stripe
```

**That's it!**

---

## STEP 5: RUN THE SETUP (30 seconds)

```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
python STRIPE_API_SETUP.py
```

**What happens:**
- Creates all 9 consciousness kit products in Stripe
- Generates payment links for each
- Saves configuration
- Ready to accept payments! ✅

---

## STEP 6: SHARE PAYMENT LINKS

The script will output links like:

```
AMELIA Joy Kit - Starter
$39.00 - https://buy.stripe.com/test_abc123...
```

**Share these anywhere:**
- GoFundMe campaign descriptions
- Instagram bio
- Email to contacts
- Direct messages

**Anyone clicks → Pays → You get money automatically** 🚀

---

## STEP 7: SEE PAYMENTS IN DASHBOARD

Go to: **https://dashboard.stripe.com/test/payments**

Every payment shows up immediately with:
- Customer email
- Amount paid
- Product purchased
- 40% to AMELIA/KENNEDI fund (in metadata)

---

## SWITCHING TO LIVE MODE (When Ready)

**Test mode = Fake money for testing**
**Live mode = REAL MONEY**

**To go live:**

1. Get live API keys: https://dashboard.stripe.com/apikeys
2. Replace `sk_test_...` with `sk_live_...`
3. Run setup script again
4. New payment links = REAL PAYMENTS

**Start in test mode. Switch to live when ready to accept real money.**

---

## TROUBLESHOOTING

**Error: "Invalid API key"**
- Check you copied the FULL secret key
- Make sure it starts with `sk_test_`
- No extra spaces

**Error: "stripe module not found"**
```bash
pip install stripe
```

**Products already exist?**
- They're in test mode, that's fine
- Can delete and recreate anytime in test mode
- Dashboard → Products → Delete

---

## TOTAL TIME: ~10 MINUTES

**Then you have:**
- ✅ 9 products ready (all kits, all tiers)
- ✅ Payment links to share
- ✅ Automatic payment processing
- ✅ Money goes directly to your bank account

**No GoFundMe fees. No middleman. Direct payments.** 💰

---

## NEXT: WEBHOOK SERVER

Once payments are working, set up webhook server to:
- Send confirmation emails
- Track orders
- Trigger manufacturing
- Update dashboard

See: `WEBHOOK_SERVER.py`

---

**Status:** READY TO ACCEPT PAYMENTS ✅
**Complexity:** DEAD SIMPLE ✅
**Time to First Dollar:** ~10 MINUTES ✅
