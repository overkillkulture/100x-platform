/**
 * TRINITY FOUNDATION - API CLIENT
 * Frontend JavaScript client for calling the unified API Gateway
 *
 * BEFORE: Frontend called 41 different ports
 * AFTER: Frontend calls ONE port (8080) via this client
 *
 * Usage:
 *   const client = new APIClient();
 *   const data = await client.get('/users/active');
 *   await client.post('/auth/login', { email, password });
 */

class APIClient {
    constructor(options = {}) {
        // Configuration
        this.baseURL = options.baseURL || this.detectGatewayURL();
        this.timeout = options.timeout || 30000;
        this.retries = options.retries || 3;
        this.debug = options.debug || false;

        // Request tracking
        this.requestLog = [];
        this.maxLogSize = 100;

        if (this.debug) {
            console.log('[APIClient] Initialized with baseURL:', this.baseURL);
        }
    }

    /**
     * Automatically detect the API Gateway URL
     * Works in both development and production
     */
    detectGatewayURL() {
        // Check if we're on localhost
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8080';
        }

        // In production, use the same host with /api prefix
        // This assumes API Gateway is deployed on same domain
        return `${window.location.protocol}//${window.location.host}`;
    }

    /**
     * Log request for debugging
     */
    logRequest(method, path, status, duration, error = null) {
        const entry = {
            timestamp: new Date().toISOString(),
            method,
            path,
            status,
            duration,
            error
        };

        this.requestLog.push(entry);
        if (this.requestLog.length > this.maxLogSize) {
            this.requestLog.shift();
        }

        if (this.debug) {
            console.log(`[APIClient] ${method} ${path} - ${status} (${duration}ms)`, error || '');
        }
    }

    /**
     * Make HTTP request with retry logic
     */
    async request(method, path, options = {}) {
        const startTime = Date.now();
        let lastError = null;

        // Ensure path starts with /api
        if (!path.startsWith('/api/')) {
            path = `/api${path.startsWith('/') ? '' : '/'}${path}`;
        }

        const url = `${this.baseURL}${path}`;

        for (let attempt = 1; attempt <= this.retries; attempt++) {
            try {
                const fetchOptions = {
                    method,
                    headers: {
                        'Content-Type': 'application/json',
                        ...(options.headers || {})
                    }
                };

                // Add body for POST/PUT/PATCH
                if (options.body && ['POST', 'PUT', 'PATCH'].includes(method)) {
                    fetchOptions.body = JSON.stringify(options.body);
                }

                // Add timeout
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), this.timeout);
                fetchOptions.signal = controller.signal;

                const response = await fetch(url, fetchOptions);
                clearTimeout(timeoutId);

                const duration = Date.now() - startTime;

                // Parse response
                let data;
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    data = await response.json();
                } else {
                    data = await response.text();
                }

                // Log request
                this.logRequest(method, path, response.status, duration);

                // Handle errors
                if (!response.ok) {
                    throw new APIError(
                        data.error || data.message || `HTTP ${response.status}`,
                        response.status,
                        data
                    );
                }

                return data;

            } catch (error) {
                lastError = error;
                const duration = Date.now() - startTime;

                // Don't retry on client errors (4xx)
                if (error.status >= 400 && error.status < 500) {
                    this.logRequest(method, path, error.status, duration, error.message);
                    throw error;
                }

                // Log and retry on network/server errors
                this.logRequest(method, path, 0, duration, error.message);

                if (attempt < this.retries) {
                    // Exponential backoff
                    const delay = Math.min(1000 * Math.pow(2, attempt - 1), 5000);
                    if (this.debug) {
                        console.log(`[APIClient] Retry ${attempt}/${this.retries} after ${delay}ms`);
                    }
                    await this.sleep(delay);
                } else {
                    throw lastError;
                }
            }
        }

        throw lastError;
    }

    /**
     * HTTP Methods
     */
    async get(path, options = {}) {
        return this.request('GET', path, options);
    }

    async post(path, body, options = {}) {
        return this.request('POST', path, { ...options, body });
    }

    async put(path, body, options = {}) {
        return this.request('PUT', path, { ...options, body });
    }

    async patch(path, body, options = {}) {
        return this.request('PATCH', path, { ...options, body });
    }

    async delete(path, options = {}) {
        return this.request('DELETE', path, options);
    }

    /**
     * Utility: Sleep
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Get request statistics
     */
    getStats() {
        const total = this.requestLog.length;
        const successful = this.requestLog.filter(r => r.status >= 200 && r.status < 300).length;
        const failed = total - successful;

        return {
            total,
            successful,
            failed,
            successRate: total > 0 ? (successful / total * 100).toFixed(2) + '%' : 'N/A',
            recentRequests: this.requestLog.slice(-10)
        };
    }

    /**
     * Health check
     */
    async healthCheck() {
        try {
            const response = await this.get('/health');
            return {
                healthy: true,
                gateway: response
            };
        } catch (error) {
            return {
                healthy: false,
                error: error.message
            };
        }
    }

    /**
     * Check all backend services
     */
    async checkServices() {
        try {
            return await this.get('/services/health');
        } catch (error) {
            return {
                error: 'Could not check services',
                message: error.message
            };
        }
    }
}

/**
 * Custom error class for API errors
 */
class APIError extends Error {
    constructor(message, status, data) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.data = data;
    }
}

/**
 * Service-specific helper methods
 * These provide a clean interface for common operations
 */
class ServiceAPI extends APIClient {
    constructor(options = {}) {
        super(options);
    }

    // Authentication
    async login(email, password) {
        return this.post('/auth/login', { email, password });
    }

    async signup(email, password, fullName) {
        return this.post('/auth/signup', { email, password, full_name: fullName });
    }

    async logout() {
        return this.post('/auth/logout');
    }

    // User Detection
    async pingActivity(userId, userName, location, action) {
        return this.post('/users/ping', {
            user_id: userId,
            user_name: userName,
            location,
            action
        });
    }

    async getActiveUsers() {
        return this.get('/users/active');
    }

    async getWorkspaceState() {
        return this.get('/users/workspace/state');
    }

    // Araya AI
    async chatWithAraya(userId, message) {
        return this.post('/araya/chat', {
            user_id: userId,
            message
        });
    }

    async getUserProfile(userId) {
        return this.get(`/araya/user/${userId}`);
    }

    // Analytics
    async trackEvent(eventType, data) {
        return this.post('/analytics/event', {
            event_type: eventType,
            ...data
        });
    }

    // Bug Reports
    async submitBugReport(report) {
        return this.post('/bugs/report', report);
    }

    // Trinity
    async getTrinityStatus() {
        return this.get('/trinity/status');
    }

    async sendTrinityMission(agent, mission) {
        return this.post('/trinity/mission', { agent, mission });
    }
}

// Global instance for easy use
const apiClient = new ServiceAPI({ debug: false });

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { APIClient, ServiceAPI, APIError, apiClient };
}
