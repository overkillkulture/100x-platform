/**
 * Philosopher AI - API Client
 * Connects frontend to production backend on Railway
 *
 * Backend URL: https://cloud-funnel-production.up.railway.app
 */

class APIClient {
    constructor() {
        // Production backend URL
        this.baseURL = 'https://cloud-funnel-production.up.railway.app/api';
        this.token = localStorage.getItem('auth_token');

        // Initialize auth helper
        this.auth = {
            isAuthenticated: () => !!this.token,
            getCurrentUser: () => {
                const user = localStorage.getItem('current_user');
                return user ? JSON.parse(user) : null;
            },
            setToken: (token) => {
                this.token = token;
                localStorage.setItem('auth_token', token);
            },
            setUser: (user) => {
                localStorage.setItem('current_user', JSON.stringify(user));
            },
            logout: () => {
                this.token = null;
                localStorage.removeItem('auth_token');
                localStorage.removeItem('current_user');
            }
        };
    }

    /**
     * Make authenticated API request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error(`[API] Request failed:`, error);
            throw error;
        }
    }

    /**
     * Authentication Endpoints
     */
    async register(email, password, username) {
        const response = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ email, password, username })
        });

        if (response.token) {
            this.auth.setToken(response.token);
            this.auth.setUser(response.user);
        }

        return response;
    }

    async login(email, password) {
        const response = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        if (response.token) {
            this.auth.setToken(response.token);
            this.auth.setUser(response.user);
        }

        return response;
    }

    async getMe() {
        return await this.request('/auth/me');
    }

    /**
     * Questions Endpoints
     */
    async askQuestion(question) {
        return await this.request('/questions/ask', {
            method: 'POST',
            body: JSON.stringify({ question })
        });
    }

    async getQuestionHistory() {
        return await this.request('/questions/history');
    }

    async getUsageStats() {
        return await this.request('/usage/stats');
    }

    /**
     * Subscriptions Endpoints
     */
    async createCheckout(tier) {
        return await this.request('/subscriptions/create-checkout', {
            method: 'POST',
            body: JSON.stringify({ tier })
        });
    }

    async getCurrentSubscription() {
        return await this.request('/subscriptions/current');
    }

    /**
     * Health Check
     */
    async checkHealth() {
        return await fetch(`${this.baseURL}/health`).then(r => r.json());
    }
}

// Make APIClient available globally
window.APIClient = APIClient;

console.log('[API Client] Loaded - Backend:', 'https://cloud-funnel-production.up.railway.app');
