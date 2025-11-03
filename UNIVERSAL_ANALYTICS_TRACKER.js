/**
 * UNIVERSAL ANALYTICS TRACKER
 * Add this ONE script to EVERY page - it handles ALL tracking automatically
 *
 * Features:
 * - Tracks page views
 * - Tracks time on page
 * - Tracks clicks
 * - Tracks scrolling
 * - Identifies users (named or anonymous)
 * - Sends everything to Unified Analytics Master
 */

(function() {
    'use strict';

    // Configuration
    const ANALYTICS_URL = 'http://localhost:9000/track';  // Unified Analytics Master
    const UPDATE_INTERVAL = 5000;  // Send updates every 5 seconds

    // Session data
    let sessionData = {
        page: window.location.pathname,
        user_name: localStorage.getItem('user_name') || 'Anonymous',
        started: new Date().toISOString(),
        events: []
    };

    // Track page view immediately
    function trackPageView() {
        const data = {
            page: window.location.pathname,
            user_name: sessionData.user_name,
            title: document.title,
            referrer: document.referrer,
            screen: `${window.screen.width}x${window.screen.height}`,
            viewport: `${window.innerWidth}x${window.innerHeight}`,
            timestamp: new Date().toISOString()
        };

        sendToAnalytics(data);
    }

    // Send data to unified analytics
    function sendToAnalytics(data) {
        if (navigator.sendBeacon) {
            // Use sendBeacon for reliability (works even on page unload)
            const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
            navigator.sendBeacon(ANALYTICS_URL, blob);
        } else {
            // Fallback to fetch
            fetch(ANALYTICS_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
                keepalive: true
            }).catch(err => console.log('Analytics error:', err));
        }
    }

    // Track user interactions
    function trackClick(event) {
        sessionData.events.push({
            type: 'click',
            element: event.target.tagName,
            text: event.target.textContent?.substring(0, 50),
            timestamp: new Date().toISOString()
        });
    }

    function trackScroll() {
        const scrollPercent = Math.round(
            (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
        );

        sessionData.events.push({
            type: 'scroll',
            percent: scrollPercent,
            timestamp: new Date().toISOString()
        });
    }

    // Periodic heartbeat - proves user is still active
    function sendHeartbeat() {
        const data = {
            ...sessionData,
            heartbeat: true,
            time_on_page: Math.round((new Date() - new Date(sessionData.started)) / 1000),
            scroll_depth: getScrollDepth()
        };

        sendToAnalytics(data);
    }

    function getScrollDepth() {
        const scrollTop = window.scrollY;
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        return Math.round((scrollTop / scrollHeight) * 100) || 0;
    }

    // Set user name (if they identify themselves)
    window.setAnalyticsUserName = function(name) {
        sessionData.user_name = name;
        localStorage.setItem('user_name', name);

        // Send updated identity
        trackPageView();
    };

    // Initialize tracking
    function init() {
        // Track initial page view
        trackPageView();

        // Track interactions
        document.addEventListener('click', trackClick, true);
        window.addEventListener('scroll', trackScroll, { passive: true });

        // Send heartbeat every 5 seconds
        setInterval(sendHeartbeat, UPDATE_INTERVAL);

        // Track when user leaves
        window.addEventListener('beforeunload', () => {
            sendToAnalytics({
                ...sessionData,
                page_exit: true,
                total_time: Math.round((new Date() - new Date(sessionData.started)) / 1000)
            });
        });

        console.log('📊 Unified Analytics Tracking Active');
    }

    // Start tracking when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose global analytics object
    window.UnifiedAnalytics = {
        setUserName: window.setAnalyticsUserName,
        track: sendToAnalytics,
        sessionData: sessionData
    };

})();
