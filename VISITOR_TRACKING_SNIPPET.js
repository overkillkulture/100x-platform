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

        fetch('https://builder-pattern-api-production.up.railway.app/api/visitor/heartbeat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...pageData,
                timeOnPage: timeOnPage,
                isActive: true
            })
        }).catch(err => console.log('Tracking offline'));
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

    // Listen for intercom messages from Commander
    const eventSource = new EventSource(`https://builder-pattern-api-production.up.railway.app/api/intercom/listen?pin=${userPin}`);

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.type === 'message') {
            // Show intercom popup
            showIntercomMessage(data.from, data.message);
        }
    };

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
