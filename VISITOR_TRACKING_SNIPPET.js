/**
 * VISITOR TRACKING SNIPPET
 * Add this to every page on consciousnessrevolution.io
 * Sends real-time data to Commander's dashboard
 */

(function() {
    // Get user info from localStorage
    const userPin = localStorage.getItem('beta_user_pin');
    const userName = localStorage.getItem('beta_user_name');
    const loginTime = localStorage.getItem('beta_login_time');

    // Track page view
    const pageData = {
        pin: userPin || 'anonymous',
        name: userName || 'Guest',
        page: window.location.pathname,
        timestamp: new Date().toISOString(),
        sessionStart: loginTime || new Date().toISOString(),
        userAgent: navigator.userAgent,
        referrer: document.referrer
    };

    // Send heartbeat every 10 seconds to show "online" status
    let lastActivity = Date.now();

    function sendHeartbeat() {
        const timeOnPage = Math.floor((Date.now() - lastActivity) / 1000);

        const heartbeatData = {
            ...pageData,
            timeOnPage: timeOnPage,
            isActive: true
        };

        // Send to LOCAL nerve collector FIRST (in-house)
        fetch('http://localhost:6000/api/visitor/heartbeat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(heartbeatData)
        }).catch(err => console.log('Local nerves offline'));

        // Also send to Railway (cloud backup)
        fetch('https://builder-pattern-api-production.up.railway.app/api/visitor/heartbeat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(heartbeatData)
        }).catch(err => console.log('Cloud backup offline'));
    }

    // Track mouse movement = active
    document.addEventListener('mousemove', () => {
        lastActivity = Date.now();
    });

    // Track page visibility
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            fetch('https://builder-pattern-api-production.up.railway.app/api/visitor/inactive', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(pageData)
            }).catch(err => {});
        } else {
            sendHeartbeat();
        }
    });

    // Initial heartbeat
    sendHeartbeat();

    // Heartbeat every 10 seconds
    setInterval(sendHeartbeat, 10000);

    // Poll for intercom messages from Commander every 5 seconds
    async function pollIntercomMessages() {
        if (!userPin || userPin === 'anonymous') return;

        try {
            // Try local first
            const response = await fetch(`http://localhost:6000/api/intercom/poll/${userPin}`);
            const messages = await response.json();

            if (messages && messages.length > 0) {
                messages.forEach(msg => {
                    showIntercomMessage(msg.from, msg.message);
                });
            }
        } catch (err) {
            // Local server offline - that's okay
            console.log('Intercom service offline');
        }
    }

    // Poll every 5 seconds
    setInterval(pollIntercomMessages, 5000);
    pollIntercomMessages(); // Initial poll

    function showIntercomMessage(from, message) {
        // Create floating intercom popup
        const popup = document.createElement('div');
        popup.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            max-width: 300px;
            z-index: 99999;
            animation: slideIn 0.3s ease;
        `;
        popup.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 10px;">${from}:</div>
            <div>${message}</div>
            <button onclick="this.parentElement.remove()" style="
                background: white;
                color: #667eea;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                margin-top: 10px;
                cursor: pointer;
                font-weight: bold;
            ">Got it!</button>
        `;
        document.body.appendChild(popup);

        // Auto-remove after 10 seconds
        setTimeout(() => popup.remove(), 10000);
    }
})();
