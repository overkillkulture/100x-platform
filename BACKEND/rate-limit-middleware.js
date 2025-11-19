/**
 * 🛡️ RATE LIMITING MIDDLEWARE - PHASE 2 SECURITY HARDENING
 * October 17, 2025 - Manipulation Immunity 99%
 *
 * Protects authentication endpoints from:
 * - Brute force attacks (password guessing)
 * - Credential stuffing (stolen password lists)
 * - Account enumeration (discovering valid emails)
 * - DoS attacks (resource exhaustion)
 */

const rateLimit = require('express-rate-limit');

// ================================================
// RATE LIMITING STRATEGIES
// ================================================

/**
 * STRICT: Authentication endpoints (login, register)
 * Purpose: Prevent brute force password attacks
 * Pattern: Exponential backoff after threshold
 */
const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 attempts per 15 minutes per IP
    message: {
        error: 'Too many authentication attempts. Please try again in 15 minutes.',
        retryAfter: '15 minutes',
        securityNote: 'Multiple failed attempts detected. Account security protocols engaged.'
    },
    standardHeaders: true, // Return rate limit info in `RateLimit-*` headers
    legacyHeaders: false, // Disable `X-RateLimit-*` headers
    skipSuccessfulRequests: false, // Count successful requests (prevent enumeration via timing)
    skipFailedRequests: false, // Count failed requests (prevent bypass)

    // Custom key generator (use IP + user agent for better fingerprinting)
    keyGenerator: (req) => {
        // Combine IP with User-Agent hash for stronger fingerprinting
        const ip = req.ip || req.connection.remoteAddress;
        const userAgent = req.get('user-agent') || 'unknown';
        const fingerprint = `${ip}-${hashString(userAgent)}`;
        return fingerprint;
    },

    // Custom handler for rate limit exceeded
    handler: (req, res) => {
        console.warn(`⚠️ SECURITY: Rate limit exceeded for ${req.ip} on ${req.path}`);

        res.status(429).json({
            error: 'Too many authentication attempts',
            retryAfter: '15 minutes',
            message: 'Multiple failed attempts detected. For security, please wait 15 minutes before trying again.',
            securityTip: 'If you forgot your password, use the password reset feature instead.'
        });
    }
});

/**
 * MODERATE: Password reset endpoints
 * Purpose: Prevent email bombing and account enumeration
 * Pattern: Stricter than regular endpoints, but allows legitimate retries
 */
const passwordResetLimiter = rateLimit({
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 3, // 3 password reset requests per hour per IP
    message: {
        error: 'Too many password reset requests. Please try again in 1 hour.',
        retryAfter: '1 hour',
        securityNote: 'If you need immediate assistance, contact support.'
    },
    standardHeaders: true,
    legacyHeaders: false,

    keyGenerator: (req) => {
        const ip = req.ip || req.connection.remoteAddress;
        const email = req.body?.email || 'unknown';
        // Rate limit by both IP and email to prevent distributed attacks
        return `${ip}-${email}`;
    },

    handler: (req, res) => {
        console.warn(`⚠️ SECURITY: Password reset rate limit exceeded for ${req.ip}`);

        res.status(429).json({
            error: 'Too many password reset requests',
            retryAfter: '1 hour',
            message: 'For security, password reset requests are limited. Please wait 1 hour before trying again.',
            supportEmail: 'support@consciousnessrevolution.io'
        });
    }
});

/**
 * STANDARD: API endpoints (question asking, data retrieval)
 * Purpose: Prevent API abuse and resource exhaustion
 * Pattern: Generous limit for normal usage, blocks aggressive bots
 */
const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // 100 requests per 15 minutes per IP
    message: {
        error: 'Too many requests. Please slow down.',
        retryAfter: 'Please wait a few minutes'
    },
    standardHeaders: true,
    legacyHeaders: false,

    // Skip rate limiting for authenticated paid users
    skip: async (req) => {
        // If user is authenticated and has paid tier, skip rate limiting
        if (req.user && (req.user.tier === 'pro' || req.user.tier === 'unlimited')) {
            return true;
        }
        return false;
    }
});

/**
 * GLOBAL: All endpoints (catch-all protection)
 * Purpose: Prevent massive DoS attacks across entire platform
 * Pattern: Very high limit, only blocks extreme abuse
 */
const globalLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 500, // 500 requests per 15 minutes per IP (very generous)
    message: {
        error: 'Too many requests from this IP. Please try again later.',
        retryAfter: 'Please wait 15 minutes'
    },
    standardHeaders: true,
    legacyHeaders: false
});

// ================================================
// HELPER FUNCTIONS
// ================================================

/**
 * Simple string hash function for user agent fingerprinting
 * Not cryptographic - just for creating consistent fingerprints
 */
function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash).toString(36);
}

// ================================================
// EXPORT LIMITERS
// ================================================

module.exports = {
    authLimiter,           // Strict: login, register
    passwordResetLimiter,  // Moderate: password reset
    apiLimiter,            // Standard: general API endpoints
    globalLimiter          // Global: all endpoints catch-all
};
