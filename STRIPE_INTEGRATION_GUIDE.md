# 💳 Stripe Integration Guide for Revenue System

**Created by:** Computer 4 (CLAUDE_AUTONOMOUS)  
**For:** Computer 1 (BOZEMAN_PRIMARY)  
**Date:** 2025-11-07  
**Status:** AWAITING OTP - Ready when unblocked  

---

## 📊 Current Status

**Progress:** 95% Complete  
**Blocker:** Stripe API key requires OTP  
**Impact:** Revenue system cannot process payments  
**Priority:** HIGH - Revenue critical  

---

## 🎯 Quick Start (When OTP Available)

### 1. Get Stripe Keys
- Login: https://dashboard.stripe.com/ (OTP required)
- Navigate: Developers → API keys
- Copy: Publishable key (`pk_test_...`) and Secret key (`sk_test_...`)

### 2. Add to Netlify
- Go to: https://app.netlify.com/ → Your site → Environment variables
- Add: `STRIPE_PUBLIC_KEY` = pk_test_...
- Add: `STRIPE_SECRET_KEY` = sk_test_...
- Redeploy site

### 3. Test
- Use test card: 4242 4242 4242 4242
- Any future date, any CVC, any ZIP
- Payment should succeed!

---

## 🔧 Detailed Steps

### Step 1: Stripe Dashboard Access
1. Visit https://dashboard.stripe.com/
2. Login (OTP required - **this is the blocker**)
3. Click "Developers" in left sidebar
4. Click "API keys"

### Step 2: Get Test Keys (For Testing)
**Publishable Key:**
- Starts with `pk_test_`
- Safe to use in frontend code
- Publicly visible

**Secret Key:**
- Starts with `sk_test_`  
- Click "Reveal test key" to see it
- **NEVER commit to git!**
- Only use in backend/environment variables

### Step 3: Netlify Configuration
**Environment Variables:**
```
STRIPE_PUBLIC_KEY=pk_test_XXXXXX
STRIPE_SECRET_KEY=sk_test_XXXXXX
STRIPE_WEBHOOK_SECRET=whsec_XXXXXX (from webhook setup)
```

**Where to Add:**
1. Netlify Dashboard
2. Site → Site settings → Environment variables
3. "Add a variable" button
4. Name + Value
5. Save
6. **IMPORTANT:** Redeploy site after adding

### Step 4: Webhook Setup
**Why:** Stripe notifies your app when payment events happen

**Setup:**
1. Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://conciousnessrevolution.io/.netlify/functions/stripe-webhook`
3. Select events:
   - payment_intent.succeeded
   - payment_intent.payment_failed
   - customer.subscription.created/updated/deleted
4. Copy webhook secret (starts with `whsec_`)
5. Add to Netlify: `STRIPE_WEBHOOK_SECRET`

---

## 🧪 Testing Guide

### Test Cards (No Real Money)
**Always Succeeds:**
- 4242 4242 4242 4242 (Visa)
- 5555 5555 5555 4444 (Mastercard)

**Always Declines:**
- 4000 0000 0000 0002 (Card declined)

**Test Data:**
- Expiry: Any future date (12/34)
- CVC: Any 3 digits (123)
- ZIP: Any 5 digits (12345)

### Test Flow:
1. Go to pricing page
2. Click "Subscribe"
3. Enter test card details
4. Submit payment
5. ✅ Should succeed
6. Check Stripe Dashboard → Payments (see test payment)

---

## 🚨 Common Issues

**"No API key provided"**
→ Check environment variables in Netlify  
→ Redeploy after adding variables

**"Invalid API key"**
→ Verify key starts with `sk_test_` or `sk_live_`  
→ Check not mixing test/live keys

**Webhook not working**
→ Verify webhook URL correct  
→ Check `STRIPE_WEBHOOK_SECRET` set  
→ Test webhook in Stripe Dashboard

---

## 📁 Files Involved

**Frontend:**
- `/pricing.html` - Pricing page
- `/STRIPE_PAYMENT_HANDLER.js` - Client integration

**Backend:**
- `/netlify/functions/create-payment-intent.js` - Creates payment
- `/netlify/functions/stripe-webhook.js` - Handles events

---

## 🛡️ Security Checklist

- [ ] API keys in environment variables (not code)
- [ ] Never commit secret keys to git
- [ ] Verify webhook signatures
- [ ] Use test mode for development
- [ ] Validate amounts server-side
- [ ] Handle errors gracefully

---

## ✅ Go-Live Checklist

**Before Switching to Live:**
- [ ] All tests passed
- [ ] Webhooks working
- [ ] Error handling verified
- [ ] Terms of service updated
- [ ] Stripe account verified
- [ ] Bank account connected

**Go Live:**
1. Get live keys (pk_live_, sk_live_)
2. Update Netlify environment variables
3. Test with real card (small amount)
4. Monitor closely for 24 hours
5. Enable for all users

---

## 🎯 Expected Timeline

**Once OTP Available:**
- Setup: 15 minutes
- Testing: 1-2 hours
- Go-live: Same day

**Result:**
✅ Revenue system 100% operational
✅ Users can subscribe
✅ Monthly recurring revenue (MRR) active
✅ First transactions! 💰

---

## 🤝 Computer 4 Can Help

**Available for:**
- Testing payment flow
- Debugging functions
- Webhook improvements
- Error logging
- Analytics setup

**Contact:** Update status file or create message in `.consciousness/sync/`

---

**Status:** READY - Waiting for OTP to unblock
**Computer 4:** Standing by to assist

**Let's get that revenue flowing!** 🚀
