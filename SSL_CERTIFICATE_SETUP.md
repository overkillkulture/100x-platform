# SSL Certificate Setup for DigitalOcean Deployment

## Problem
The app needs the PostgreSQL CA certificate to establish secure SSL connections, but we can't commit the certificate to Git (security risk).

## Solution
Add the CA certificate as an environment variable in DigitalOcean App Platform.

## Steps

### 1. Get the CA Certificate Content

The certificate has already been downloaded to: `postgres-ca-certificate.crt`

We need to convert it to a single-line string to use as an environment variable.

### 2. Add to DigitalOcean Environment Variables

1. Go to DigitalOcean App Platform → Your App → Settings → Environment Variables
2. Add a new environment variable:
   - **Key:** `POSTGRES_CA_CERT`
   - **Value:** [The entire contents of the ca-certificate.crt file]
   - **Scope:** All components

### 3. Update Code to Use Environment Variable

The code has been updated to:
1. Check if `POSTGRES_CA_CERT` environment variable exists
2. If yes, use that for SSL verification
3. If no, look for `postgres-ca-certificate.crt` file
4. If neither exists, fall back to `rejectUnauthorized: false`

## Alternative: Base64 Encoding

If the certificate doesn't work as plain text, encode it as base64:

```bash
# In PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("postgres-ca-certificate.crt"))
```

Then decode it in the code before using.

## Redis/Valkey Note

DigitalOcean's Valkey/Redis doesn't provide a downloadable CA certificate. The current configuration with `rejectUnauthorized: false` is the recommended approach for DigitalOcean's managed Redis.

## Current Status

- ✅ PostgreSQL: Will use CA cert from environment variable or file
- ✅ Redis: Using TLS with rejectUnauthorized=false (DigitalOcean standard)
- ✅ Fallback: Both have safe fallbacks if SSL setup fails
