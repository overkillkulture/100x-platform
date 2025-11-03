/**
 * CONSCIOUSNESS REVOLUTION - JavaScript SDK
 *
 * Client-side SDK for interacting with all backend services
 * Handles authentication, payments, analytics, marketplace
 *
 * Usage:
 * const cr = new ConsciousnessRevolution({
 *   apiBaseUrl: 'https://api.conciousnessrevolution.io',
 *   stripePublishableKey: 'pk_live_...'
 * });
 *
 * await cr.auth.signup({ email, password, fullName });
 * await cr.payments.createSubscription('music', 'pro');
 * await cr.vault.getMRR();
 */

class ConsciousnessRevolution {
    constructor(config = {}) {
        this.config = {
            apiBaseUrl: config.apiBaseUrl || 'http://localhost:5000',
            stripePublishableKey: config.stripePublishableKey || '',
            onAuthChange: config.onAuthChange || (() => {}),
            onError: config.onError || console.error
        };

        // Initialize auth token from localStorage
        this.authToken = localStorage.getItem('cr_auth_token');

        // Initialize modules
        this.auth = new AuthModule(this);
        this.payments = new PaymentsModule(this);
        this.music = new MusicModule(this);
        this.vault = new VaultModule(this);
        this.marketplace = new MarketplaceModule(this);
        this.conversion = new ConversionModule(this);
        this.monitoring = new MonitoringModule(this);
        this.korpak = new KorpakModule(this);
    }

    // Internal: Make authenticated API request
    async _request(endpoint, options = {}) {
        const url = `${this.config.apiBaseUrl}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        // Add auth token if available
        if (this.authToken) {
            headers['Authorization'] = `Bearer ${this.authToken}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            this.config.onError(error);
            throw error;
        }
    }

    // Set auth token and persist
    _setAuthToken(token) {
        this.authToken = token;
        localStorage.setItem('cr_auth_token', token);
        this.config.onAuthChange(!!token);
    }

    // Clear auth token
    _clearAuthToken() {
        this.authToken = null;
        localStorage.removeItem('cr_auth_token');
        this.config.onAuthChange(false);
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.authToken;
    }
}

// =====================================================
// AUTHENTICATION MODULE
// =====================================================

class AuthModule {
    constructor(sdk) {
        this.sdk = sdk;
    }

    async signup({ email, password, fullName, source = 'website' }) {
        const data = await this.sdk._request('/api/auth/signup', {
            method: 'POST',
            body: JSON.stringify({ email, password, full_name: fullName, source })
        });

        if (data.success && data.token) {
            this.sdk._setAuthToken(data.token);
        }

        return data;
    }

    async login({ email, password }) {
        const data = await this.sdk._request('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        if (data.success && data.token) {
            this.sdk._setAuthToken(data.token);
        }

        return data;
    }

    async verify() {
        try {
            const data = await this.sdk._request('/api/auth/verify');
            return data;
        } catch (error) {
            // Token invalid, clear it
            this.sdk._clearAuthToken();
            throw error;
        }
    }

    logout() {
        this.sdk._clearAuthToken();
    }

    async checkAccess(domain) {
        return await this.sdk._request(`/api/access/${domain}`);
    }

    async recordUsage(domain, action, count = 1) {
        return await this.sdk._request(`/api/usage/${domain}/${action}`, {
            method: 'POST',
            body: JSON.stringify({ count })
        });
    }
}

// =====================================================
// PAYMENTS MODULE
// =====================================================

class PaymentsModule {
    constructor(sdk) {
        this.sdk = sdk;
        this.stripe = null;

        // Initialize Stripe if publishable key provided
        if (sdk.config.stripePublishableKey && window.Stripe) {
            this.stripe = window.Stripe(sdk.config.stripePublishableKey);
        }
    }

    async createSubscription(domain, tier, billingPeriod = 'monthly') {
        const data = await this.sdk._request('/api/payments/subscription/create', {
            method: 'POST',
            body: JSON.stringify({ domain, tier, billing_period: billingPeriod })
        });

        // If Stripe Elements needed, confirm payment
        if (data.client_secret && this.stripe) {
            const { error } = await this.stripe.confirmCardPayment(data.client_secret);
            if (error) {
                throw new Error(error.message);
            }
        }

        return data;
    }

    async cancelSubscription(subscriptionId, immediately = false) {
        return await this.sdk._request('/api/payments/subscription/cancel', {
            method: 'POST',
            body: JSON.stringify({ subscription_id: subscriptionId, immediately })
        });
    }

    async upgradeSubscription(subscriptionId, newTier) {
        return await this.sdk._request('/api/payments/subscription/upgrade', {
            method: 'POST',
            body: JSON.stringify({ subscription_id: subscriptionId, new_tier: newTier })
        });
    }

    async createPaymentIntent(amount, description) {
        return await this.sdk._request('/api/payments/intent/create', {
            method: 'POST',
            body: JSON.stringify({ amount, description })
        });
    }

    // Create Stripe checkout session
    createCheckoutSession({ domain, tier, billingPeriod = 'monthly' }) {
        if (!this.stripe) {
            throw new Error('Stripe not initialized');
        }

        // This would redirect to Stripe Checkout
        // Implementation depends on backend creating session
        return this.sdk._request('/api/payments/checkout/create', {
            method: 'POST',
            body: JSON.stringify({ domain, tier, billing_period: billingPeriod })
        });
    }
}

// =====================================================
// MUSIC DOMAIN MODULE
// =====================================================

class MusicModule {
    constructor(sdk) {
        this.sdk = sdk;
    }

    async getDashboard() {
        return await this.sdk._request('/api/music/dashboard');
    }

    async connectSpotify(authCode) {
        return await this.sdk._request('/api/music/spotify/connect', {
            method: 'POST',
            body: JSON.stringify({ auth_code: authCode })
        });
    }

    async getAnalytics(range = '30d') {
        return await this.sdk._request(`/api/music/analytics?range=${range}`);
    }

    async submitDistribution(trackData) {
        return await this.sdk._request('/api/music/distribution/submit', {
            method: 'POST',
            body: JSON.stringify(trackData)
        });
    }

    async createNFT(nftData) {
        return await this.sdk._request('/api/music/nft/create', {
            method: 'POST',
            body: JSON.stringify(nftData)
        });
    }

    async createSamplePack(packData) {
        return await this.sdk._request('/api/music/samples/create', {
            method: 'POST',
            body: JSON.stringify(packData)
        });
    }

    async bookCoaching(sessionData) {
        return await this.sdk._request('/api/music/coaching/book', {
            method: 'POST',
            body: JSON.stringify(sessionData)
        });
    }

    async activate(tier) {
        return await this.sdk._request('/api/music/activate', {
            method: 'POST',
            body: JSON.stringify({ tier })
        });
    }
}

// =====================================================
// QUANTUM VAULT MODULE
// =====================================================

class VaultModule {
    constructor(sdk) {
        this.sdk = sdk;
    }

    async getDashboard() {
        return await this.sdk._request('/api/vault/dashboard');
    }

    async getMRR(domain = null) {
        const endpoint = domain ? `/api/vault/mrr?domain=${domain}` : '/api/vault/mrr';
        return await this.sdk._request(endpoint);
    }

    async getARR(domain = null) {
        const endpoint = domain ? `/api/vault/arr?domain=${domain}` : '/api/vault/arr';
        return await this.sdk._request(endpoint);
    }

    async getRevenueByDomain() {
        return await this.sdk._request('/api/vault/domains');
    }

    async getGrowth(days = 30) {
        return await this.sdk._request(`/api/vault/growth?days=${days}`);
    }

    async getFibonacci() {
        return await this.sdk._request('/api/vault/fibonacci');
    }

    async getLtvCac() {
        return await this.sdk._request('/api/vault/ltv-cac');
    }

    async getChurn(days = 30) {
        return await this.sdk._request(`/api/vault/churn?days=${days}`);
    }

    async getMarketplace() {
        return await this.sdk._request('/api/vault/marketplace');
    }

    async getSubscriptionHealth() {
        return await this.sdk._request('/api/vault/subscription-health');
    }

    async getHistory(days = 90) {
        return await this.sdk._request(`/api/vault/history?days=${days}`);
    }
}

// =====================================================
// MARKETPLACE MODULE
// =====================================================

class MarketplaceModule {
    constructor(sdk) {
        this.sdk = sdk;
    }

    async onboardCreator(creatorData) {
        return await this.sdk._request('/api/marketplace/creator/onboard', {
            method: 'POST',
            body: JSON.stringify(creatorData)
        });
    }

    async getCreatorStatus() {
        return await this.sdk._request('/api/marketplace/creator/status');
    }

    async createItem(itemData) {
        return await this.sdk._request('/api/marketplace/item/create', {
            method: 'POST',
            body: JSON.stringify(itemData)
        });
    }

    async updateItem(itemId, updates) {
        return await this.sdk._request(`/api/marketplace/item/${itemId}`, {
            method: 'PUT',
            body: JSON.stringify(updates)
        });
    }

    async purchase(itemId, paymentMethodId) {
        return await this.sdk._request('/api/marketplace/purchase', {
            method: 'POST',
            body: JSON.stringify({ item_id: itemId, payment_method_id: paymentMethodId })
        });
    }

    async getDownload(purchaseId) {
        return await this.sdk._request(`/api/marketplace/download/${purchaseId}`);
    }

    async getCreatorDashboard() {
        return await this.sdk._request('/api/marketplace/creator/dashboard');
    }

    async browse({ domain = null, type = null, sort = 'popular', limit = 20 } = {}) {
        const params = new URLSearchParams();
        if (domain) params.append('domain', domain);
        if (type) params.append('type', type);
        params.append('sort', sort);
        params.append('limit', limit);

        return await this.sdk._request(`/api/marketplace/browse?${params}`);
    }
}

// =====================================================
// CONVERSION MODULE
// =====================================================

class ConversionModule {
    constructor(sdk) {
        this.sdk = sdk;
    }

    async checkLimits(domain, action) {
        return await this.sdk._request('/api/conversion/check-limits', {
            method: 'POST',
            body: JSON.stringify({ domain, action })
        });
    }

    async trackUpgradeClick(domain, fromTier, toTier) {
        return await this.sdk._request('/api/conversion/track-click', {
            method: 'POST',
            body: JSON.stringify({ domain, from_tier: fromTier, to_tier: toTier })
        });
    }

    async getMetrics(domain = null, days = 30) {
        const params = new URLSearchParams({ days });
        if (domain) params.append('domain', domain);

        return await this.sdk._request(`/api/conversion/metrics?${params}`);
    }

    async getBestTriggers(days = 30) {
        return await this.sdk._request(`/api/conversion/best-triggers?days=${days}`);
    }
}

// =====================================================
// MONITORING MODULE
// =====================================================

class MonitoringModule {
    constructor(sdk) {
        this.sdk = sdk;
    }

    async getHealth() {
        return await this.sdk._request('/api/monitoring/health');
    }

    async getPaymentHealth() {
        return await this.sdk._request('/api/monitoring/payments');
    }

    async getSubscriptionHealth() {
        return await this.sdk._request('/api/monitoring/subscriptions');
    }

    async getApiHealth() {
        return await this.sdk._request('/api/monitoring/api');
    }

    async getDatabaseHealth() {
        return await this.sdk._request('/api/monitoring/database');
    }

    async getAnomalies() {
        return await this.sdk._request('/api/monitoring/anomalies');
    }

    async getAlerts(hours = 24, severity = null) {
        const params = new URLSearchParams({ hours });
        if (severity) params.append('severity', severity);

        return await this.sdk._request(`/api/monitoring/alerts?${params}`);
    }

    async resolveAlert(alertId, notes = null) {
        return await this.sdk._request(`/api/monitoring/alerts/${alertId}/resolve`, {
            method: 'POST',
            body: JSON.stringify({ notes })
        });
    }
}

// =====================================================
// KORPAK MODULE
// =====================================================

class KorpakModule {
    constructor(sdk) {
        this.sdk = sdk;
    }

    async generateRevenueMissions() {
        return await this.sdk._request('/api/korpak/generate/revenue', {
            method: 'POST'
        });
    }

    async generateGrowthMissions() {
        return await this.sdk._request('/api/korpak/generate/growth', {
            method: 'POST'
        });
    }

    async create(korpakData) {
        return await this.sdk._request('/api/korpak/create', {
            method: 'POST',
            body: JSON.stringify(korpakData)
        });
    }

    async execute(korpakId) {
        return await this.sdk._request(`/api/korpak/${korpakId}/execute`, {
            method: 'POST'
        });
    }

    async expand(korpakId) {
        return await this.sdk._request(`/api/korpak/${korpakId}/expand`, {
            method: 'POST'
        });
    }

    async getDashboard() {
        return await this.sdk._request('/api/korpak/dashboard');
    }
}

// =====================================================
// EXPORT
// =====================================================

// Make available globally
if (typeof window !== 'undefined') {
    window.ConsciousnessRevolution = ConsciousnessRevolution;
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ConsciousnessRevolution;
}
