# URGENT: Remove Redirects in Netlify Dashboard

## Problem
Server-side redirects in Netlify dashboard are blocking screening.html:
- `/screening.html` → redirects to `/platform.html` (404)
- `/screening` → redirects to `/platform.html` (404)
- `/` → redirects to `/platform.html` (404)

## Fix
1. Go to: https://app.netlify.com/sites/verdant-tulumba-fa2a5a/configuration/redirects
2. Delete ALL redirect rules
3. Save
4. Redeploy

## Why This Happened
Old configuration from previous site setup. The redirects are configured server-side, not in netlify.toml.
