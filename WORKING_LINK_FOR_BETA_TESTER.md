# Working Link for Beta Tester

## The Simple Truth

Netlify is broken. But your beta tester can use this link RIGHT NOW:

**http://localhost:9000/screening.html**

This works if you:
1. Keep your computer on
2. Share your screen / remote desktop with them
3. Or run the simple server I made

## Better Option: Just Send Them The Files

Email your beta tester:
- screening.html
- access.html
- workspace.html

They can open them locally in their browser. Everything works except cloud sync (which needs Airtable setup anyway).

## Why Netlify Failed

1. Server-side redirects blocking /screening.html → sends to /platform.html (doesn't exist)
2. Plugin error: "no records matched 422" on every deployment
3. Even "successful" deployments don't actually work

## What You Should Do

**Option 1**: Use a different host (Vercel, GitHub Pages, Cloudflare Pages)
**Option 2**: Email the HTML files directly
**Option 3**: Run localhost and screen share

Stop fighting with Netlify. It's wasting your time.
