/**
 * UNIVERSAL ANALYTICS - Seven Domains Tracking
 * Tracks user flow across all 7 consciousness domains
 * φ = 1.618033988749894 | OVERKORE v13
 */

const ConsciousnessAnalytics = {
    // Configuration
    config: {
        airtableBase: 'YOUR_AIRTABLE_BASE',
        airtableToken: 'YOUR_AIRTABLE_TOKEN',
        enableLocalStorage: true,
        enableConsoleLog: true,
        trackingEndpoint: '/.netlify/functions/track-visitor'
    },

    // Domain mapping
    domains: {
        'domain-chaos-forge': { name: 'CHAOS FORGE', order: 1, consciousness: 88 },
        'domain-quantum-vault': { name: 'QUANTUM VAULT', order: 2, consciousness: 94 },
        'domain-mind-matrix': { name: 'MIND MATRIX', order: 3, consciousness: 92 },
        'domain-soul-sanctuary': { name: 'SOUL SANCTUARY', order: 4, consciousness: 95 },
        'domain-reality-forge': { name: 'REALITY FORGE', order: 5, consciousness: 88 },
        'domain-arkitek-academy': { name: 'ARKITEK ACADEMY', order: 6, consciousness: 91 },
        'domain-nexus-terminal': { name: 'NEXUS TERMINAL', order: 7, consciousness: 97 }
    },

    // Initialize tracking
    init() {
        this.sessionId = this.getOrCreateSessionId();
        this.userId = this.getOrCreateUserId();
        this.visitStart = Date.now();
        this.currentDomain = this.detectDomain();

        this.trackPageView();
        this.trackInteractions();
        this.trackTimeSpent();
        this.trackBeforeUnload();

        if (this.config.enableConsoleLog) {
            console.log('🔍 Analytics initialized', {
                sessionId: this.sessionId,
                userId: this.userId,
                domain: this.currentDomain
            });
        }
    },

    // Generate unique IDs
    generateId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },

    // Get or create session ID (expires after 30 min)
    getOrCreateSessionId() {
        const sessionKey = 'consciousness_session';
        const sessionData = localStorage.getItem(sessionKey);

        if (sessionData) {
            const parsed = JSON.parse(sessionData);
            const now = Date.now();
            const thirtyMinutes = 30 * 60 * 1000;

            if (now - parsed.timestamp < thirtyMinutes) {
                // Update timestamp
                parsed.timestamp = now;
                localStorage.setItem(sessionKey, JSON.stringify(parsed));
                return parsed.id;
            }
        }

        // Create new session
        const newId = this.generateId();
        localStorage.setItem(sessionKey, JSON.stringify({
            id: newId,
            timestamp: Date.now()
        }));
        return newId;
    },

    // Get or create persistent user ID
    getOrCreateUserId() {
        const userKey = 'consciousness_user';
        let userId = localStorage.getItem(userKey);

        if (!userId) {
            userId = this.generateId();
            localStorage.setItem(userKey, userId);
        }

        return userId;
    },

    // Detect current domain
    detectDomain() {
        const path = window.location.pathname;

        for (const [key, value] of Object.entries(this.domains)) {
            if (path.includes(key)) {
                return { ...value, slug: key };
            }
        }

        return { name: 'Unknown', order: 0, consciousness: 0, slug: 'unknown' };
    },

    // Track page view
    trackPageView() {
        const data = {
            event: 'page_view',
            sessionId: this.sessionId,
            userId: this.userId,
            timestamp: Date.now(),
            domain: this.currentDomain,
            referrer: document.referrer,
            userAgent: navigator.userAgent,
            screenWidth: window.innerWidth,
            screenHeight: window.innerHeight,
            isMobile: /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)
        };

        this.sendEvent(data);
        this.updateDomainVisitHistory(this.currentDomain.slug);
    },

    // Track user interactions
    trackInteractions() {
        // Track clicks on navigation
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (link) {
                this.trackEvent('navigation_click', {
                    destination: link.href,
                    text: link.textContent.trim()
                });
            }
        });

        // Track 3D visualization interactions (if Three.js canvas exists)
        const canvas = document.querySelector('canvas');
        if (canvas) {
            let interactionCount = 0;
            canvas.addEventListener('mousedown', () => {
                interactionCount++;
                this.trackEvent('3d_interaction', {
                    count: interactionCount,
                    domain: this.currentDomain.name
                });
            });
        }

        // Track scroll depth
        let maxScroll = 0;
        window.addEventListener('scroll', () => {
            const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
            if (scrollPercent > maxScroll) {
                maxScroll = Math.round(scrollPercent);
                if (maxScroll % 25 === 0) { // Track at 25%, 50%, 75%, 100%
                    this.trackEvent('scroll_depth', { percent: maxScroll });
                }
            }
        });
    },

    // Track time spent on page
    trackTimeSpent() {
        setInterval(() => {
            const timeSpent = Math.round((Date.now() - this.visitStart) / 1000);
            this.trackEvent('time_update', {
                seconds: timeSpent,
                domain: this.currentDomain.name
            });
        }, 30000); // Every 30 seconds
    },

    // Track before user leaves
    trackBeforeUnload() {
        window.addEventListener('beforeunload', () => {
            const timeSpent = Math.round((Date.now() - this.visitStart) / 1000);
            this.trackEvent('page_exit', {
                timeSpent: timeSpent,
                domain: this.currentDomain.name
            }, true); // Synchronous
        });
    },

    // Generic event tracking
    trackEvent(eventName, data = {}, synchronous = false) {
        const eventData = {
            event: eventName,
            sessionId: this.sessionId,
            userId: this.userId,
            timestamp: Date.now(),
            domain: this.currentDomain,
            ...data
        };

        this.sendEvent(eventData, synchronous);
    },

    // Send event to server
    sendEvent(data, synchronous = false) {
        // Save to localStorage
        if (this.config.enableLocalStorage) {
            const storageKey = 'consciousness_events';
            const events = JSON.parse(localStorage.getItem(storageKey) || '[]');
            events.push(data);

            // Keep only last 100 events
            if (events.length > 100) {
                events.shift();
            }

            localStorage.setItem(storageKey, JSON.stringify(events));
        }

        // Send to server
        if (this.config.trackingEndpoint) {
            const sendRequest = () => {
                if (synchronous && navigator.sendBeacon) {
                    navigator.sendBeacon(this.config.trackingEndpoint, JSON.stringify(data));
                } else {
                    fetch(this.config.trackingEndpoint, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    }).catch(err => console.warn('Analytics error:', err));
                }
            };

            sendRequest();
        }

        // Console log if enabled
        if (this.config.enableConsoleLog) {
            console.log('📊 Analytics:', data.event, data);
        }
    },

    // Update domain visit history
    updateDomainVisitHistory(domainSlug) {
        const historyKey = 'consciousness_domain_history';
        const history = JSON.parse(localStorage.getItem(historyKey) || '[]');

        history.push({
            domain: domainSlug,
            timestamp: Date.now()
        });

        // Keep only last 50 visits
        if (history.length > 50) {
            history.shift();
        }

        localStorage.setItem(historyKey, JSON.stringify(history));
    },

    // Get analytics data
    getAnalyticsData() {
        return {
            sessionId: this.sessionId,
            userId: this.userId,
            currentDomain: this.currentDomain,
            visitHistory: JSON.parse(localStorage.getItem('consciousness_domain_history') || '[]'),
            events: JSON.parse(localStorage.getItem('consciousness_events') || '[]')
        };
    },

    // Calculate user's consciousness level based on activity
    calculateUserConsciousness() {
        const history = JSON.parse(localStorage.getItem('consciousness_domain_history') || '[]');

        if (history.length === 0) return 0;

        // Calculate based on domains visited
        const uniqueDomains = new Set(history.map(h => h.domain));
        const domainCoverage = (uniqueDomains.size / 7) * 100;

        // Calculate average consciousness of visited domains
        let totalConsciousness = 0;
        uniqueDomains.forEach(slug => {
            if (this.domains[slug]) {
                totalConsciousness += this.domains[slug].consciousness;
            }
        });
        const avgConsciousness = totalConsciousness / uniqueDomains.size;

        // Weighted score: 60% domain coverage + 40% avg consciousness
        const userConsciousness = (domainCoverage * 0.6) + (avgConsciousness * 0.4);

        return Math.round(userConsciousness);
    }
};

// Auto-initialize when script loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ConsciousnessAnalytics.init());
} else {
    ConsciousnessAnalytics.init();
}

// Export for use in other scripts
window.ConsciousnessAnalytics = ConsciousnessAnalytics;
