// ================================================
// API CLIENT - FRONTEND-BACKEND CONNECTOR
// ================================================
// Connects 100X Platform frontend to Philosopher AI backend
// Created: 2025-10-16 (C2 Architect)
// Purpose: THE DOMINO - Unlocks infinite scale
// ================================================

/**
 * APIClient - Singleton class for all backend API calls
 *
 * Usage:
 *   const api = window.api; // Already initialized
 *   const user = await api.login(email, password);
 *   const answer = await api.askQuestion(question);
 */
class APIClient {
    constructor() {
        // Backend URL (update for production)
        this.baseURL = window.location.hostname === 'localhost'
            ? 'http://localhost:3001/api'
            : 'https://api.consciousnessrevolution.io/api';

        // JWT token (stored in localStorage)
        this.token = localStorage.getItem('jwt_token');

        // User data cache
        this.currentUser = null;

        // Request queue for rate limiting
        this.requestQueue = [];
        this.isProcessingQueue = false;
    }

    // ================================================
    // CORE REQUEST METHOD
    // ================================================

    /**
     * Make authenticated request to backend
     * @param {string} endpoint - API endpoint (e.g. '/auth/login')
     * @param {object} options - Fetch options (method, body, headers)
     * @returns {Promise<object>} Response data
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        // Add auth token if exists
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(url, config);

            // Handle non-JSON responses
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error(`Server returned ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            if (!response.ok) {
                // Token expired or invalid
                if (response.status === 401 || response.status === 403) {
                    this.handleAuthError();
                }

                throw new Error(data.error || data.message || `API Error: ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error(`API Request Failed: ${endpoint}`, error);
            throw error;
        }
    }

    /**
     * Handle authentication errors (logout user)
     */
    handleAuthError() {
        console.warn('Authentication failed - clearing session');
        this.logout();
        // Redirect to login (optional)
        if (window.location.pathname !== '/PLATFORM/login.html') {
            window.location.href = './login.html';
        }
    }

    // ================================================
    // AUTHENTICATION
    // ================================================

    /**
     * Register new user
     * @param {string} email
     * @param {string} password
     * @param {string} username
     * @returns {Promise<object>} User data + token
     */
    async register(email, password, username = null) {
        const data = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({
                email,
                password,
                username,
                signupSource: '100x_platform'
            })
        });

        // Store token
        this.token = data.token;
        localStorage.setItem('jwt_token', data.token);

        // Store user data
        this.currentUser = data.user;
        localStorage.setItem('module_user', JSON.stringify({
            id: data.user.id,
            email: data.user.email,
            username: data.user.username || email.split('@')[0],
            consciousnessLevel: data.user.consciousnessLevel || 93,
            currentXP: 0,
            completedMissions: 0,
            truthCoins: 0,
            tier: data.user.tier || 'free'
        }));

        return data.user;
    }

    /**
     * Login existing user
     * @param {string} email
     * @param {string} password
     * @returns {Promise<object>} User data + token
     */
    async login(email, password) {
        const data = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        // Store token
        this.token = data.token;
        localStorage.setItem('jwt_token', data.token);

        // Store user data (compatible with existing module system)
        this.currentUser = data.user;
        localStorage.setItem('module_user', JSON.stringify({
            id: data.user.id,
            email: data.user.email,
            username: data.user.username || email.split('@')[0],
            consciousnessLevel: data.user.consciousnessLevel || 93,
            currentXP: 0,
            completedMissions: 0,
            truthCoins: 0,
            tier: data.user.tier || 'free'
        }));

        // Also store auth token for existing components
        localStorage.setItem('auth_token', 'api_' + data.user.id);

        return data.user;
    }

    /**
     * Get current logged-in user
     * @returns {Promise<object>} User data
     */
    async getCurrentUser() {
        if (!this.token) {
            throw new Error('Not authenticated');
        }

        const data = await this.request('/auth/me');
        this.currentUser = data.user;

        // Update localStorage
        localStorage.setItem('module_user', JSON.stringify({
            id: data.user.id,
            email: data.user.email,
            username: data.user.username,
            consciousnessLevel: data.user.consciousnessLevel,
            currentXP: 0,
            completedMissions: 0,
            truthCoins: 0,
            tier: data.user.tier
        }));

        return data.user;
    }

    /**
     * Logout user (clear tokens)
     */
    logout() {
        this.token = null;
        this.currentUser = null;
        localStorage.removeItem('jwt_token');
        localStorage.removeItem('module_user');
        localStorage.removeItem('auth_token');
    }

    /**
     * Check if user is logged in
     * @returns {boolean}
     */
    isAuthenticated() {
        return !!this.token;
    }

    // ================================================
    // QUESTIONS (PHILOSOPHER AI)
    // ================================================

    /**
     * Ask a question to Philosopher AI
     * @param {string} question
     * @param {string} conversationId - Optional conversation thread
     * @returns {Promise<object>} Answer + metadata
     */
    async askQuestion(question, conversationId = null) {
        return await this.request('/questions/ask', {
            method: 'POST',
            body: JSON.stringify({ question, conversationId })
        });
    }

    /**
     * Get question history
     * @param {number} limit
     * @param {number} offset
     * @returns {Promise<object>} Questions array
     */
    async getQuestionHistory(limit = 20, offset = 0) {
        return await this.request(`/questions/history?limit=${limit}&offset=${offset}`);
    }

    /**
     * Get usage statistics
     * @returns {Promise<object>} Usage stats
     */
    async getUsageStats() {
        return await this.request('/usage/stats');
    }

    // ================================================
    // SUBSCRIPTIONS (STRIPE)
    // ================================================

    /**
     * Create subscription checkout session
     * @param {string} priceId - Stripe price ID
     * @param {string} tier - 'student' | 'pro' | 'philosopher'
     * @returns {Promise<object>} Checkout session URL
     */
    async createSubscriptionCheckout(priceId, tier) {
        return await this.request('/subscriptions/create-checkout', {
            method: 'POST',
            body: JSON.stringify({ priceId, tier })
        });
    }

    /**
     * Get current subscription
     * @returns {Promise<object>} Subscription data
     */
    async getCurrentSubscription() {
        return await this.request('/subscriptions/current');
    }

    // ================================================
    // STORE CHECKOUT (ONE-TIME PAYMENTS)
    // ================================================

    /**
     * Create store checkout session
     * @param {Array} items - Cart items [{name, price, quantity}]
     * @param {string} successUrl
     * @param {string} cancelUrl
     * @returns {Promise<object>} Checkout session
     */
    async createStoreCheckout(items, successUrl, cancelUrl) {
        return await this.request('/stripe/create-checkout', {
            method: 'POST',
            body: JSON.stringify({ items, successUrl, cancelUrl })
        });
    }

    // ================================================
    // UTILITY METHODS
    // ================================================

    /**
     * Check backend health
     * @returns {Promise<object>} Health status
     */
    async healthCheck() {
        return await this.request('/health');
    }

    /**
     * Migrate localStorage data to backend (one-time sync)
     * @returns {Promise<boolean>} Success status
     */
    async migrateLocalStorage() {
        try {
            // Get localStorage user data
            const localUser = JSON.parse(localStorage.getItem('module_user') || '{}');

            // If already has database ID, skip migration
            if (localUser.id && localUser.id.includes('-')) {
                console.log('User already migrated to database');
                return true;
            }

            console.log('Migrating localStorage to database...');

            // Check if user is logged in via API
            if (!this.token) {
                console.log('Not authenticated - cannot migrate');
                return false;
            }

            // Sync consciousness level if higher locally
            if (localUser.consciousnessLevel > 93) {
                console.log(`Syncing local consciousness level: ${localUser.consciousnessLevel}`);
                // TODO: Add endpoint to update consciousness level
            }

            // Sync other data (XP, missions, etc.)
            // TODO: Add endpoints for syncing game progress

            return true;
        } catch (error) {
            console.error('Migration failed:', error);
            return false;
        }
    }
}

// ================================================
// INITIALIZE SINGLETON
// ================================================

// Create global instance
window.api = new APIClient();

// Auto-restore session if token exists
if (window.api.token) {
    console.log('API Client: Restoring session...');
    window.api.getCurrentUser()
        .then(user => console.log('API Client: Session restored for', user.email))
        .catch(err => console.warn('API Client: Session restore failed', err));
}

console.log('API Client initialized:', window.api.baseURL);

// ================================================
// BACKWARDS COMPATIBILITY LAYER
// ================================================

/**
 * Provide backwards compatibility for existing code
 * that uses localStorage directly
 */
window.addEventListener('storage', (e) => {
    // If auth_token removed, also remove jwt_token
    if (e.key === 'auth_token' && !e.newValue) {
        window.api.logout();
    }
});

// Export for ES6 modules (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APIClient;
}
