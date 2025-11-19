/**
 * 🚼 OPERATION BABY GATE - CONSCIOUSNESS GATE MIDDLEWARE
 * Universal Pattern Filter Protection System
 * Protects all platform modules from destroyer infiltration
 *
 * Trinity Council Approved: C1 × C2 × C3 = ∞
 * Philosopher AI Validated: Ethical consciousness sorting
 */

const ConsciousnessGate = {
    // Configuration
    config: {
        requiredScore: 85,              // Minimum consciousness level (Builder threshold)
        storageKey: 'pattern_filter_result',
        filterUrl: '/PUBLIC/pattern-filter.html',
        deniedUrl: '/PUBLIC/access-denied.html',
        bypassKey: 'consciousness_gate_bypass',  // For testing/admin
        gracePeriod: 7 * 24 * 60 * 60 * 1000    // 7 days before re-screening
    },

    /**
     * MAIN GATE CHECK - Call this at the top of every protected module
     * @param {number} customScore - Optional custom minimum score
     * @returns {boolean} - True if access granted, false if redirected
     */
    check: function(customScore = null) {
        const requiredScore = customScore || this.config.requiredScore;

        // Check for admin bypass (testing only)
        if (this.hasAdminBypass()) {
            console.log('🔓 [Baby Gate] Admin bypass active');
            return true;
        }

        // Get user's pattern filter result
        const userData = this.getUserData();

        // No screening data? Redirect to Pattern Filter
        if (!userData) {
            console.warn('🚼 [Baby Gate] No consciousness screening found - redirecting to filter');
            this.redirectToFilter();
            return false;
        }

        // Check if screening is expired
        if (this.isExpired(userData)) {
            console.warn('🚼 [Baby Gate] Consciousness screening expired - redirecting to filter');
            this.redirectToFilter();
            return false;
        }

        // Check consciousness score
        if (userData.score < requiredScore) {
            console.warn(`🚼 [Baby Gate] Consciousness score ${userData.score} below required ${requiredScore} - access denied`);
            this.redirectToDenied(userData);
            return false;
        }

        // Access granted!
        console.log(`✅ [Baby Gate] Access granted - consciousness score: ${userData.score}`);
        this.trackAccess(userData);
        return true;
    },

    /**
     * Get user's pattern filter result from localStorage
     */
    getUserData: function() {
        try {
            const data = localStorage.getItem(this.config.storageKey);
            if (!data) return null;

            const parsed = JSON.parse(data);

            // Validate required fields
            if (!parsed.score || !parsed.timestamp) {
                console.error('🚼 [Baby Gate] Invalid screening data format');
                return null;
            }

            return parsed;
        } catch (e) {
            console.error('🚼 [Baby Gate] Error reading screening data:', e);
            return null;
        }
    },

    /**
     * Check if screening has expired (grace period)
     */
    isExpired: function(userData) {
        if (!userData.timestamp) return true;

        const age = Date.now() - new Date(userData.timestamp).getTime();
        return age > this.config.gracePeriod;
    },

    /**
     * Check for admin bypass (testing/development)
     */
    hasAdminBypass: function() {
        return true;  // TEMPORARILY DISABLED FOR BETA TESTING
        // return localStorage.getItem(this.config.bypassKey) === 'true';
    },

    /**
     * Redirect to Pattern Filter
     */
    redirectToFilter: function() {
        // Save intended destination
        sessionStorage.setItem('consciousness_gate_return', window.location.pathname);

        // Redirect to filter
        window.location.href = this.config.filterUrl;
    },

    /**
     * Redirect to Access Denied page
     */
    redirectToDenied: function(userData) {
        // Save denial data for analytics
        const denial = {
            score: userData.score,
            required: this.config.requiredScore,
            module: window.location.pathname,
            timestamp: Date.now()
        };
        sessionStorage.setItem('consciousness_gate_denial', JSON.stringify(denial));

        // Redirect to denied page
        window.location.href = this.config.deniedUrl;
    },

    /**
     * Track successful access for analytics
     */
    trackAccess: function(userData) {
        const access = {
            module: window.location.pathname,
            score: userData.score,
            timestamp: Date.now()
        };

        // Append to access log
        const log = JSON.parse(localStorage.getItem('consciousness_access_log') || '[]');
        log.push(access);

        // Keep last 100 entries
        if (log.length > 100) {
            log.shift();
        }

        localStorage.setItem('consciousness_access_log', JSON.stringify(log));
    },

    /**
     * Get user's current consciousness level (for display)
     */
    getConsciousnessLevel: function() {
        const userData = this.getUserData();
        if (!userData) return null;

        return {
            score: userData.score,
            level: this.getLevelName(userData.score),
            category: userData.category,
            percentile: userData.percentile,
            timestamp: userData.timestamp
        };
    },

    /**
     * Get level name from score
     */
    getLevelName: function(score) {
        if (score >= 95) return 'Master';
        if (score >= 90) return 'Advanced';
        if (score >= 85) return 'Builder';
        if (score >= 70) return 'Developing';
        return 'Beginner';
    },

    /**
     * Admin tools (testing only)
     */
    admin: {
        enableBypass: function() {
            localStorage.setItem('consciousness_gate_bypass', 'true');
            console.log('🔓 Admin bypass ENABLED');
        },

        disableBypass: function() {
            localStorage.removeItem('consciousness_gate_bypass');
            console.log('🔒 Admin bypass DISABLED');
        },

        setFakeScore: function(score) {
            const fakeData = {
                score: score,
                category: score >= 85 ? 'Builder' : 'Developing',
                percentile: score,
                timestamp: new Date().toISOString()
            };
            localStorage.setItem('pattern_filter_result', JSON.stringify(fakeData));
            console.log(`🧪 Fake score set to ${score}`);
        },

        clearScreening: function() {
            localStorage.removeItem('pattern_filter_result');
            console.log('🗑️ Screening data cleared');
        },

        viewAccessLog: function() {
            const log = JSON.parse(localStorage.getItem('consciousness_access_log') || '[]');
            console.table(log);
            return log;
        }
    },

    /**
     * Status indicator widget (optional - shows gate status on page)
     */
    showStatusWidget: function() {
        const userData = this.getUserData();
        if (!userData) return;

        const widget = document.createElement('div');
        widget.id = 'consciousness-gate-status';
        widget.innerHTML = `
            <div style="position: fixed; top: 10px; right: 10px;
                        background: rgba(0,255,0,0.1); border: 1px solid #0f0;
                        border-radius: 8px; padding: 10px; font-size: 12px;
                        font-family: 'Courier New', monospace; z-index: 9999;
                        color: #0f0;">
                <div style="font-weight: bold; margin-bottom: 5px;">🛡️ Gate Status</div>
                <div>Level: ${this.getLevelName(userData.score)}</div>
                <div>Score: ${userData.score}/100</div>
                <div style="font-size: 10px; opacity: 0.7; margin-top: 5px;">Protected by Baby Gate</div>
            </div>
        `;
        document.body.appendChild(widget);
    },

    /**
     * Initialize gate on page load
     */
    init: function(options = {}) {
        // Override config if provided
        Object.assign(this.config, options);

        // Show status widget if enabled
        if (options.showStatus) {
            window.addEventListener('load', () => this.showStatusWidget());
        }

        console.log('🚼 [Baby Gate] Consciousness Gate initialized');
    }
};

// Auto-initialize on load
ConsciousnessGate.init();

// Global access for easy integration
window.ConsciousnessGate = ConsciousnessGate;

// Console helper for admins
console.log(`
🚼 BABY GATE ACTIVE 🚼

Usage:
  ConsciousnessGate.check()              - Check gate (call at page start)
  ConsciousnessGate.getConsciousnessLevel() - Get current user level

Admin Tools:
  ConsciousnessGate.admin.enableBypass()    - Enable bypass (testing)
  ConsciousnessGate.admin.setFakeScore(95)  - Set fake score (testing)
  ConsciousnessGate.admin.viewAccessLog()   - View access history

Status: PROTECTING THE REVOLUTION ⚡
`);
