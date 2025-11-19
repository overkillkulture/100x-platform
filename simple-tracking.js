/**
 * SIMPLE VISITOR TRACKING
 * Works without backend - uses localStorage and console logging
 * Commander can see activity in real-time
 */

(function() {
    'use strict';

    // Get user info
    const pin = localStorage.getItem('beta_user_pin') || 'anonymous';
    const name = localStorage.getItem('beta_user_name') || 'Guest';

    // Create page view event
    const pageView = {
        pin: pin,
        name: name,
        page: window.location.pathname,
        timestamp: new Date().toISOString(),
        sessionStart: localStorage.getItem('beta_login_time') || new Date().toISOString()
    };

    // Log to console (Commander can see this!)
    console.log('📊 VISITOR TRACKING:', pageView);

    // Try to send to Netlify Function
    fetch('/.netlify/functions/track-visitor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pageView)
    })
    .then(r => r.json())
    .then(data => console.log('✅ Tracked:', data))
    .catch(err => console.log('⚠️ Tracking offline (expected until deployed)'));

    // Store locally for analytics dashboard
    const viewHistory = JSON.parse(localStorage.getItem('page_view_history') || '[]');
    viewHistory.push(pageView);
    if (viewHistory.length > 50) viewHistory.shift(); // Keep last 50
    localStorage.setItem('page_view_history', JSON.stringify(viewHistory));

    // Heartbeat - send every 30 seconds to show "still here"
    let activityTime = Date.now();

    setInterval(() => {
        const timeOnPage = Math.floor((Date.now() - activityTime) / 1000);

        console.log(`💓 Heartbeat: ${name} on ${window.location.pathname} (${timeOnPage}s)`);

        fetch('/.netlify/functions/track-visitor', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...pageView,
                action: 'heartbeat',
                timeOnPage: timeOnPage
            })
        }).catch(() => {}); // Silent fail
    }, 30000);

    // Track user activity
    ['mousemove', 'keydown', 'click', 'scroll'].forEach(event => {
        document.addEventListener(event, () => {
            activityTime = Date.now();
        }, { passive: true, once: false });
    });

    // Broadcast to Commander if he's watching
    window.addEventListener('storage', (e) => {
        if (e.key === 'commander_message') {
            const msg = JSON.parse(e.newValue);
            if (msg.to === pin || msg.to === 'all') {
                showCommanderMessage(msg.message);
            }
        }
    });

    function showCommanderMessage(message) {
        const popup = document.createElement('div');
        popup.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
            max-width: 350px;
            z-index: 999999;
            animation: slideIn 0.4s ease;
        `;
        popup.innerHTML = `
            <div style="font-weight: bold; font-size: 1.1em; margin-bottom: 10px;">
                📡 Message from Commander:
            </div>
            <div style="margin-bottom: 15px;">${message}</div>
            <button onclick="this.parentElement.remove()" style="
                background: white;
                color: #667eea;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                width: 100%;
            ">Got it!</button>
        `;
        document.body.appendChild(popup);

        // Auto-remove after 15 seconds
        setTimeout(() => popup.remove(), 15000);
    }

    console.log('✅ Tracking initialized for', name, `(PIN: ${pin})`);
})();
