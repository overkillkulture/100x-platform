/**
 * 100X Analytics System
 * Client-side tracking library for the 100X Builder Platform
 * Version: 1.0.0
 */

(function(window) {
    'use strict';

    const STORAGE_PREFIX = '100x_analytics_';
    const MAX_EVENTS = 1000;
    const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutes

    class Analytics100X {
        constructor() {
            this.sessionId = null;
            this.startTime = null;
            this.initialized = false;
        }

        /**
         * Initialize analytics system
         */
        init() {
            if (this.initialized) return;

            this.sessionId = this.getOrCreateSession();
            this.startTime = Date.now();
            this.initialized = true;

            // Track page unload time
            window.addEventListener('beforeunload', () => {
                this.trackTimeOnPage();
            });

            // Update last active time periodically
            setInterval(() => {
                this.updateLastActive();
            }, 30000); // Every 30 seconds

            console.log('📊 Analytics initialized:', this.sessionId);
        }

        /**
         * Get or create session ID
         */
        getOrCreateSession() {
            const sessionKey = STORAGE_PREFIX + 'session';
            let session = this.getFromStorage(sessionKey);

            // Check if session expired
            if (session && (Date.now() - session.last_active > SESSION_TIMEOUT)) {
                session = null; // Expire old session
            }

            if (!session) {
                session = {
                    session_id: this.generateId('sess'),
                    start_time: Date.now(),
                    last_active: Date.now(),
                    page_count: 0,
                    events: [],
                    is_active: true,
                    referrer: document.referrer || 'direct',
                    entry_page: window.location.pathname
                };
            }

            session.last_active = Date.now();
            session.page_count++;
            this.saveToStorage(sessionKey, session);

            return session.session_id;
        }

        /**
         * Update last active time
         */
        updateLastActive() {
            const sessionKey = STORAGE_PREFIX + 'session';
            let session = this.getFromStorage(sessionKey);
            if (session) {
                session.last_active = Date.now();
                this.saveToStorage(sessionKey, session);
            }
        }

        /**
         * Track page view
         */
        trackPageView(customData = {}) {
            const event = {
                id: this.generateId('evt'),
                session_id: this.sessionId,
                event_type: 'page_view',
                timestamp: Date.now(),
                page: window.location.pathname,
                data: {
                    url: window.location.href,
                    title: document.title,
                    referrer: document.referrer || 'direct',
                    ...customData
                },
                user: this.getUserInfo()
            };

            this.saveEvent(event);
            console.log('📄 Page view tracked:', event.page);
        }

        /**
         * Track button click
         */
        trackButtonClick(buttonData) {
            const event = {
                id: this.generateId('evt'),
                session_id: this.sessionId,
                event_type: 'button_click',
                timestamp: Date.now(),
                page: window.location.pathname,
                data: {
                    button_text: buttonData.text || 'Unknown',
                    button_id: buttonData.id || null,
                    target_url: buttonData.target || null,
                    system_name: buttonData.system || null
                },
                user: this.getUserInfo()
            };

            this.saveEvent(event);
            console.log('🖱️ Button click tracked:', buttonData.text);
        }

        /**
         * Track system access
         */
        trackSystemAccess(systemData) {
            const event = {
                id: this.generateId('evt'),
                session_id: this.sessionId,
                event_type: 'system_access',
                timestamp: Date.now(),
                page: window.location.pathname,
                data: {
                    system_name: systemData.name,
                    system_url: systemData.url || window.location.pathname,
                    access_method: systemData.method || 'direct'
                },
                user: this.getUserInfo()
            };

            this.saveEvent(event);
            console.log('⚡ System access tracked:', systemData.name);
        }

        /**
         * Track form interaction
         */
        trackFormStart(formId) {
            const event = {
                id: this.generateId('evt'),
                session_id: this.sessionId,
                event_type: 'form_start',
                timestamp: Date.now(),
                page: window.location.pathname,
                data: {
                    form_id: formId
                },
                user: this.getUserInfo()
            };

            this.saveEvent(event);
            console.log('📝 Form start tracked:', formId);
        }

        /**
         * Track form submission
         */
        trackFormSubmit(formId, success = true, customData = {}) {
            const event = {
                id: this.generateId('evt'),
                session_id: this.sessionId,
                event_type: 'form_submit',
                timestamp: Date.now(),
                page: window.location.pathname,
                data: {
                    form_id: formId,
                    success: success,
                    ...customData
                },
                user: this.getUserInfo()
            };

            this.saveEvent(event);
            console.log('✅ Form submit tracked:', formId, success ? 'success' : 'failed');
        }

        /**
         * Track time on page
         */
        trackTimeOnPage() {
            const timeSpent = Date.now() - this.startTime;
            const event = {
                id: this.generateId('evt'),
                session_id: this.sessionId,
                event_type: 'time_on_page',
                timestamp: Date.now(),
                page: window.location.pathname,
                data: {
                    duration_ms: timeSpent,
                    duration_readable: this.formatDuration(timeSpent)
                },
                user: this.getUserInfo()
            };

            this.saveEvent(event);
        }

        /**
         * Save event to storage
         */
        saveEvent(event) {
            const eventsKey = STORAGE_PREFIX + 'events';
            let events = this.getFromStorage(eventsKey) || [];

            events.push(event);

            // Keep only last MAX_EVENTS
            if (events.length > MAX_EVENTS) {
                events = events.slice(-MAX_EVENTS);
            }

            this.saveToStorage(eventsKey, events);

            // Add to session events list
            const sessionKey = STORAGE_PREFIX + 'session';
            let session = this.getFromStorage(sessionKey);
            if (session) {
                session.events.push(event.id);
                this.saveToStorage(sessionKey, session);
            }
        }

        /**
         * Get all events
         */
        getAllEvents() {
            const eventsKey = STORAGE_PREFIX + 'events';
            return this.getFromStorage(eventsKey) || [];
        }

        /**
         * Get current session
         */
        getCurrentSession() {
            const sessionKey = STORAGE_PREFIX + 'session';
            return this.getFromStorage(sessionKey);
        }

        /**
         * Get analytics summary
         */
        getSummary() {
            const events = this.getAllEvents();
            const session = this.getCurrentSession();

            const pageViews = events.filter(e => e.event_type === 'page_view');
            const buttonClicks = events.filter(e => e.event_type === 'button_click');
            const formSubmits = events.filter(e => e.event_type === 'form_submit');
            const systemAccess = events.filter(e => e.event_type === 'system_access');

            // Most popular systems
            const systemCounts = {};
            systemAccess.forEach(event => {
                const name = event.data.system_name;
                systemCounts[name] = (systemCounts[name] || 0) + 1;
            });

            const sortedSystems = Object.entries(systemCounts)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5);

            // Most viewed pages
            const pageCounts = {};
            pageViews.forEach(event => {
                const page = event.page;
                pageCounts[page] = (pageCounts[page] || 0) + 1;
            });

            const sortedPages = Object.entries(pageCounts)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5);

            return {
                total_events: events.length,
                page_views: pageViews.length,
                button_clicks: buttonClicks.length,
                form_submits: formSubmits.length,
                system_accesses: systemAccess.length,
                session_duration: Date.now() - session.start_time,
                pages_visited: session.page_count,
                top_systems: sortedSystems,
                top_pages: sortedPages,
                referrer: session.referrer,
                entry_page: session.entry_page
            };
        }

        /**
         * Export all data as JSON
         */
        exportData() {
            const data = {
                events: this.getAllEvents(),
                session: this.getCurrentSession(),
                summary: this.getSummary(),
                exported_at: new Date().toISOString()
            };

            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `100x-analytics-${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);

            console.log('📥 Analytics data exported');
        }

        /**
         * Clear all analytics data
         */
        clearData() {
            localStorage.removeItem(STORAGE_PREFIX + 'events');
            localStorage.removeItem(STORAGE_PREFIX + 'session');
            console.log('🗑️ Analytics data cleared');
        }

        /**
         * Get user info (anonymous)
         */
        getUserInfo() {
            return {
                screen: `${window.screen.width}x${window.screen.height}`,
                viewport: `${window.innerWidth}x${window.innerHeight}`,
                device: this.getDeviceType(),
                browser: this.getBrowserName(),
                os: this.getOS(),
                language: navigator.language
            };
        }

        /**
         * Helper: Get device type
         */
        getDeviceType() {
            const width = window.innerWidth;
            if (width < 768) return 'mobile';
            if (width < 1024) return 'tablet';
            return 'desktop';
        }

        /**
         * Helper: Get browser name
         */
        getBrowserName() {
            const ua = navigator.userAgent;
            if (ua.includes('Firefox')) return 'Firefox';
            if (ua.includes('Chrome')) return 'Chrome';
            if (ua.includes('Safari')) return 'Safari';
            if (ua.includes('Edge')) return 'Edge';
            return 'Other';
        }

        /**
         * Helper: Get OS
         */
        getOS() {
            const ua = navigator.userAgent;
            if (ua.includes('Win')) return 'Windows';
            if (ua.includes('Mac')) return 'MacOS';
            if (ua.includes('Linux')) return 'Linux';
            if (ua.includes('Android')) return 'Android';
            if (ua.includes('iOS')) return 'iOS';
            return 'Other';
        }

        /**
         * Helper: Generate unique ID
         */
        generateId(prefix = 'id') {
            return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        }

        /**
         * Helper: Format duration
         */
        formatDuration(ms) {
            const seconds = Math.floor(ms / 1000);
            const minutes = Math.floor(seconds / 60);
            const hours = Math.floor(minutes / 60);

            if (hours > 0) return `${hours}h ${minutes % 60}m`;
            if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
            return `${seconds}s`;
        }

        /**
         * Helper: Save to localStorage
         */
        saveToStorage(key, data) {
            try {
                localStorage.setItem(key, JSON.stringify(data));
            } catch (e) {
                console.error('Analytics storage error:', e);
            }
        }

        /**
         * Helper: Get from localStorage
         */
        getFromStorage(key) {
            try {
                const data = localStorage.getItem(key);
                return data ? JSON.parse(data) : null;
            } catch (e) {
                console.error('Analytics retrieval error:', e);
                return null;
            }
        }
    }

    // Create global instance
    window.Analytics100X = new Analytics100X();

    // Auto-initialize on script load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.Analytics100X.init();
        });
    } else {
        window.Analytics100X.init();
    }

})(window);
