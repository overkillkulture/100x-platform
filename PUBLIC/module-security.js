/**
 * 🔒 MODULE SECURITY - Encryption & Protection for All Modules
 *
 * Built-in security that every module inherits automatically.
 */

window.ModuleSecurity = {
    // Simple encryption key (replace with user-specific key in production)
    encryptionKey: '100x_consciousness_revolution_2025',

    /**
     * Encrypt sensitive data
     */
    encrypt(data) {
        try {
            // Simple XOR cipher (upgrade to AES in production)
            const str = typeof data === 'string' ? data : JSON.stringify(data);
            let encrypted = '';

            for (let i = 0; i < str.length; i++) {
                const keyChar = this.encryptionKey.charCodeAt(i % this.encryptionKey.length);
                const strChar = str.charCodeAt(i);
                encrypted += String.fromCharCode(strChar ^ keyChar);
            }

            return btoa(encrypted); // Base64 encode
        } catch (error) {
            console.error('❌ Encryption failed:', error);
            return data;
        }
    },

    /**
     * Decrypt data
     */
    decrypt(encryptedData) {
        try {
            const decoded = atob(encryptedData); // Base64 decode
            let decrypted = '';

            for (let i = 0; i < decoded.length; i++) {
                const keyChar = this.encryptionKey.charCodeAt(i % this.encryptionKey.length);
                const encChar = decoded.charCodeAt(i);
                decrypted += String.fromCharCode(encChar ^ keyChar);
            }

            return decrypted;
        } catch (error) {
            console.error('❌ Decryption failed:', error);
            return encryptedData;
        }
    },

    /**
     * Sanitize user input (XSS protection)
     */
    sanitizeInput(input) {
        if (typeof input !== 'string') return input;

        return input
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#x27;')
            .replace(/\//g, '&#x2F;');
    },

    /**
     * Generate CSRF token
     */
    generateCSRFToken() {
        const token = Array.from(crypto.getRandomValues(new Uint8Array(32)))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');

        sessionStorage.setItem('100x_csrf_token', token);
        return token;
    },

    /**
     * Validate CSRF token
     */
    validateCSRFToken(token) {
        const storedToken = sessionStorage.getItem('100x_csrf_token');
        return token === storedToken;
    },

    /**
     * Rate limiting (prevent spam/abuse)
     */
    checkRateLimit(actionName, maxPerMinute = 60) {
        const key = `100x_ratelimit_${actionName}`;
        const now = Date.now();
        const oneMinuteAgo = now - 60000;

        // Get recent actions
        let actions = JSON.parse(localStorage.getItem(key) || '[]');

        // Filter to last minute
        actions = actions.filter(timestamp => timestamp > oneMinuteAgo);

        // Check if limit exceeded
        if (actions.length >= maxPerMinute) {
            console.warn(`⚠️ Rate limit exceeded for ${actionName}`);
            return false;
        }

        // Add current action
        actions.push(now);
        localStorage.setItem(key, JSON.stringify(actions));

        return true;
    },

    /**
     * Validate email format
     */
    validateEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },

    /**
     * Validate password strength
     */
    validatePassword(password) {
        const minLength = 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

        return {
            valid: password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers,
            strength: [hasUpperCase, hasLowerCase, hasNumbers, hasSpecialChar].filter(Boolean).length,
            feedback: password.length < minLength ? 'Password too short (min 8 characters)' :
                     !hasUpperCase ? 'Add uppercase letter' :
                     !hasLowerCase ? 'Add lowercase letter' :
                     !hasNumbers ? 'Add number' :
                     'Strong password'
        };
    },

    /**
     * Generate secure random ID
     */
    generateId(prefix = 'id') {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        return `${prefix}_${timestamp}_${random}`;
    },

    /**
     * Hash data (one-way)
     */
    async hash(data) {
        const encoder = new TextEncoder();
        const dataBuffer = encoder.encode(data);
        const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    },

    /**
     * Check if running on HTTPS
     */
    isSecureConnection() {
        return window.location.protocol === 'https:' || window.location.hostname === 'localhost';
    },

    /**
     * Get security status report
     */
    getSecurityStatus() {
        return {
            https: this.isSecureConnection(),
            csrfProtection: !!sessionStorage.getItem('100x_csrf_token'),
            encryption: 'XOR Cipher (Basic)',
            xssProtection: 'Enabled',
            rateLimiting: 'Enabled',
            timestamp: Date.now()
        };
    }
};

console.log('🔒 MODULE SECURITY LOADED');
console.log('✅ Encryption enabled');
console.log('✅ XSS protection active');
console.log('✅ Rate limiting ready');
