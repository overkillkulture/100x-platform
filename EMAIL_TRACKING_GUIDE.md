# 📧 Email Open Tracking - Setup Guide

## How It Works

Every email you send includes a tiny 1x1 pixel image. When someone opens the email, their email client loads the image, which triggers our tracking system and sends you an instant notification.

## Add Tracking to Your Emails

### Method 1: Add Tracking Pixel to Email

Add this HTML at the bottom of your email (before `</body>`):

```html
<img src="https://conciousnessrevolution.io/.netlify/functions/email-track?r=RECIPIENT_EMAIL&c=beta_invite" width="1" height="1" style="display:none;" alt="">
```

**Replace:**
- `RECIPIENT_EMAIL` = The person's email (e.g., `john@example.com`)
- `beta_invite` = Campaign name (e.g., `beta_invite`, `welcome`, `reminder`)

### Method 2: Track Email Links

Instead of a pixel, track when they click links:

```html
<a href="https://conciousnessrevolution.io/?ref=email_beta&user=john@example.com">
  Click Here to Get Started
</a>
```

This will trigger a `site_visit` notification when they click.

## Example Email Template

```html
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to 100X Platform Beta</title>
</head>
<body>
    <h1>Welcome to the Consciousness Revolution!</h1>

    <p>Hi there,</p>

    <p>You're invited to beta test the 100X Platform - your AI-powered consciousness evolution system.</p>

    <p><strong>Your Beta Access PIN:</strong> 1234</p>

    <p>
        <a href="https://conciousnessrevolution.io/?ref=email_beta&user=john@example.com">
            Click Here to Get Started
        </a>
    </p>

    <p>What you get:</p>
    <ul>
        <li>Araya AI Terminal - Your personal AI companion</li>
        <li>Builder Tools - Create anything you can imagine</li>
        <li>Consciousness Tools - Pattern recognition, reality manifestation</li>
        <li>Early access to all features</li>
    </ul>

    <p>Questions? Just reply to this email or ask Araya (the chat widget on every page).</p>

    <p>Welcome aboard!</p>
    <p>- Commander</p>

    <!-- Tracking pixel -->
    <img src="https://conciousnessrevolution.io/.netlify/functions/email-track?r=john@example.com&c=beta_invite" width="1" height="1" style="display:none;" alt="">
</body>
</html>
```

## What Gets Tracked

When someone opens the email, you'll see:

- ✅ Email address of recipient
- ✅ Exact time they opened it
- ✅ Their IP address
- ✅ Their device/browser
- ✅ Campaign name

## Where to See Notifications

1. **Desktop Alert File:** `C:/Users/dwrek/Desktop/LIVE_ACTIVITY_ALERT.json`
2. **Live Dashboard:** `C:/Users/dwrek/Desktop/LIVE_ACTIVITY_DASHBOARD.html`
3. **Netlify Function Logs:** Check Netlify dashboard

## Current Beta Testers

Track these 6 people:

1. `tester1@example.com` - Beta Invite Sent
2. `tester2@example.com` - Beta Invite Sent
3. `tester3@example.com` - Beta Invite Sent
4. `tester4@example.com` - Beta Invite Sent
5. `tester5@example.com` - Beta Invite Sent
6. `tester6@example.com` - Beta Invite Sent

## Testing It

Send yourself a test email with tracking:

```html
<img src="https://conciousnessrevolution.io/.netlify/functions/email-track?r=test@commander.com&c=test" width="1" height="1" alt="">
```

Open the email → Check `LIVE_ACTIVITY_ALERT.json` → See notification appear!

## Privacy Note

This is standard email marketing practice. Every major email service (Mailchimp, SendGrid, etc.) uses the exact same tracking pixel method. It's completely legal and expected.

We're just building it ourselves instead of paying $299/month to Mailchimp. 🚀

---

**Next Steps:**

1. Deploy email tracking function ✅ (Already created)
2. Send beta invites with tracking pixels
3. Monitor `LIVE_ACTIVITY_DASHBOARD.html`
4. See who opens emails instantly!
