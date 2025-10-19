/**
 * BUILDER TRACKING SCRIPT - Add to all pages
 * Automatically tracks visitor behavior and calculates Builder Score
 * No cookies, no forms, just pattern recognition
 */

(function() {
    'use strict';

    const BUILDER_API = 'https://builder-pattern-api-production.up.railway.app/api/builder';
    let pageLoadTime = Date.now();
    let currentPage = window.location.pathname;

    // Track page visit when user leaves or closes
    function trackPageVisit() {
        const timeSpent = Math.floor((Date.now() - pageLoadTime) / 1000);

        // Only track if they spent more than 5 seconds
        if (timeSpent < 5) return;

        // Send tracking data
        fetch(`${BUILDER_API}/track`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                page_url: currentPage,
                time_spent_seconds: timeSpent
            }),
            keepalive: true  // Important: ensures request completes even if page closes
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('✅ Builder Score:', data.builder_score);
                console.log('📊 Access Level:', data.access_level);
                console.log('🎯 Traits:', data.builder_traits);

                // Store in localStorage for quick access
                localStorage.setItem('builder_score', data.builder_score);
                localStorage.setItem('access_level', data.access_level);
                localStorage.setItem('builder_traits', data.builder_traits);

                // Trigger custom event for other scripts to react
                window.dispatchEvent(new CustomEvent('builderScoreUpdate', {
                    detail: data
                }));
            }
        })
        .catch(err => console.error('Builder tracking error:', err));
    }

    // Track on page unload
    window.addEventListener('beforeunload', trackPageVisit);

    // Track on visibility change (user switches tabs)
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            trackPageVisit();
            pageLoadTime = Date.now(); // Reset timer
        }
    });

    // Track every 30 seconds for long visits
    setInterval(trackPageVisit, 30000);

    /**
     * Check access to Amelia features
     * Call this before showing Amelia content
     */
    window.checkAmeliaAccess = function(requiredLevel = 'level_2_education') {
        return fetch(`${BUILDER_API}/check-access?level=${requiredLevel}`)
            .then(response => response.json())
            .then(data => {
                if (data.has_access) {
                    console.log(`✅ Access granted to ${requiredLevel}`);
                    console.log(`Builder Score: ${data.builder_score}/100`);
                } else {
                    console.log(`❌ Access denied to ${requiredLevel}`);
                    console.log(`Current score: ${data.builder_score}/100`);
                    console.log(`Next unlock:`, data.next_unlock);
                }
                return data;
            });
    };

    /**
     * Show Builder Score badge (optional UI element)
     */
    window.showBuilderScore = function() {
        const score = localStorage.getItem('builder_score') || 0;
        const traits = localStorage.getItem('builder_traits') || 'Exploring...';

        // Create badge element
        const badge = document.createElement('div');
        badge.id = 'builder-score-badge';
        badge.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            font-family: Arial, sans-serif;
            z-index: 9999;
            cursor: pointer;
            transition: transform 0.3s;
        `;
        badge.innerHTML = `
            <div style="font-size: 12px; opacity: 0.9;">Builder Score</div>
            <div style="font-size: 24px; font-weight: bold;">${score}/100</div>
            <div style="font-size: 11px; margin-top: 5px;">${traits}</div>
        `;
        badge.onmouseenter = () => badge.style.transform = 'scale(1.05)';
        badge.onmouseleave = () => badge.style.transform = 'scale(1)';

        document.body.appendChild(badge);

        // Click to see full details
        badge.onclick = () => {
            window.checkAmeliaAccess().then(data => {
                alert(`
Builder Score: ${data.builder_score}/100
Access Level: ${data.access_level || 'none'}
Traits: ${data.builder_traits || 'Keep exploring!'}

Visits: ${data.statistics?.total_visits || 0}
Analytical Pages: ${data.statistics?.analytical_pages || 0}
Domains Explored: ${data.statistics?.domains_explored?.join(', ') || 'None yet'}

${data.next_unlock ? `Next Unlock: ${data.next_unlock.description} (${data.next_unlock.points_needed} more points)` : 'Maximum access unlocked!'}
                `.trim());
            });
        };
    };

    // Auto-show badge after 10 seconds on page
    setTimeout(() => {
        if (localStorage.getItem('builder_score')) {
            window.showBuilderScore();
        }
    }, 10000);

    console.log('🌀 Builder Pattern Detector: ACTIVE');

})();
