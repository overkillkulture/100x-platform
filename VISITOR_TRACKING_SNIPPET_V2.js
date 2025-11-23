/**
 * VISITOR TRACKING SNIPPET V2 - ANALYTICS TRAPS DEPLOYED
 * Add this to every page on consciousnessrevolution.io
 * Tracks EVERYTHING: clicks, scrolls, forms, building activity, engagement quality
 */

(function() {
    // ===== SESSION INITIALIZATION =====
    const userPin = localStorage.getItem('beta_user_pin');
    const userName = localStorage.getItem('beta_user_name');
    const loginTime = localStorage.getItem('beta_login_time');

    const sessionId = sessionStorage.getItem('analytics_session_id') ||
                      `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    sessionStorage.setItem('analytics_session_id', sessionId);

    const sessionStartTime = Date.now();
    let lastActivity = Date.now();
    let eventQueue = [];
    let maxScrollDepth = 0;
    let clickCount = 0;
    let actionCount = 0;

    // ===== BASE PAGE DATA =====
    const baseData = {
        pin: userPin || 'anonymous',
        name: userName || 'Guest',
        page: window.location.pathname,
        sessionId: sessionId,
        sessionStart: loginTime || new Date().toISOString(),
        userAgent: navigator.userAgent,
        referrer: document.referrer,
        screenWidth: window.screen.width,
        screenHeight: window.screen.height,
        viewportWidth: window.innerWidth,
        viewportHeight: window.innerHeight,
        deviceType: getDeviceType(),
        browser: getBrowser()
    };

    function getDeviceType() {
        const ua = navigator.userAgent;
        if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) return 'tablet';
        if (/Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) return 'mobile';
        return 'desktop';
    }

    function getBrowser() {
        const ua = navigator.userAgent;
        if (ua.includes('Firefox')) return 'Firefox';
        if (ua.includes('SamsungBrowser')) return 'Samsung';
        if (ua.includes('Opera') || ua.includes('OPR')) return 'Opera';
        if (ua.includes('Trident')) return 'IE';
        if (ua.includes('Edge')) return 'Edge';
        if (ua.includes('Chrome')) return 'Chrome';
        if (ua.includes('Safari')) return 'Safari';
        return 'Unknown';
    }

    // ===== EVENT TRACKING SYSTEM =====
    function trackEvent(eventType, eventData = {}) {
        const event = {
            ...baseData,
            eventType: eventType,
            eventData: eventData,
            timestamp: new Date().toISOString(),
            timeInSession: Date.now() - sessionStartTime
        };

        eventQueue.push(event);
        actionCount++;

        // Send immediately for critical events, batch for others
        if (['page_enter', 'page_exit', 'form_submit', 'project_save'].includes(eventType)) {
            sendEvents();
        }
    }

    function sendEvents() {
        if (eventQueue.length === 0) return;

        const batch = [...eventQueue];
        eventQueue = [];

        // Send to local nerve collector
        fetch('http://localhost:6000/api/analytics/track', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ events: batch })
        }).catch(err => console.log('Local analytics offline'));

        // Send to cloud backup
        fetch('https://builder-pattern-api-production.up.railway.app/api/analytics/track', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ events: batch })
        }).catch(err => console.log('Cloud analytics offline'));
    }

    // Batch send events every 10 seconds
    setInterval(sendEvents, 10000);

    // ===== PAGE ENTRY TRAP =====
    trackEvent('page_enter', {
        entryTime: new Date().toISOString(),
        previousPage: document.referrer,
        urlParams: window.location.search
    });

    // ===== PAGE EXIT TRAP =====
    window.addEventListener('beforeunload', () => {
        trackEvent('page_exit', {
            timeSpent: Date.now() - sessionStartTime,
            scrollDepth: maxScrollDepth,
            clickCount: clickCount,
            actionCount: actionCount,
            qualityScore: calculateQualityScore()
        });
        sendEvents(); // Force send before page unloads
    });

    // ===== ACTIVITY DETECTION =====
    const activityEvents = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    activityEvents.forEach(event => {
        document.addEventListener(event, () => {
            lastActivity = Date.now();
        }, { passive: true });
    });

    // ===== IDLE DETECTION =====
    setInterval(() => {
        const idleTime = Date.now() - lastActivity;
        if (idleTime > 60000 && idleTime < 61000) { // Just crossed 1 minute idle
            trackEvent('user_idle', { idleDuration: idleTime });
        }
    }, 1000);

    // ===== CLICK TRACKING TRAP =====
    document.addEventListener('click', (e) => {
        clickCount++;

        trackEvent('click', {
            element: e.target.tagName,
            id: e.target.id || null,
            className: e.target.className || null,
            text: e.target.innerText?.substring(0, 100) || null,
            x: e.clientX,
            y: e.clientY,
            pageX: e.pageX,
            pageY: e.pageY,
            href: e.target.href || e.target.closest('a')?.href || null,
            button: e.target.closest('button')?.innerText || null
        });
    }, { passive: true });

    // ===== SCROLL TRACKING TRAP =====
    let scrollTimeout;
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = scrollHeight > 0 ? Math.round((scrollTop / scrollHeight) * 100) : 0;

        maxScrollDepth = Math.max(maxScrollDepth, scrollPercent);

        // Debounce scroll events
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            trackEvent('scroll', {
                currentDepth: scrollPercent,
                maxDepth: maxScrollDepth,
                scrollTop: scrollTop
            });
        }, 1000);
    }, { passive: true });

    // ===== FORM INTERACTION TRAPS =====
    let formStartTimes = new Map();

    // Track form start
    document.addEventListener('focusin', (e) => {
        if (e.target.matches('input, textarea, select')) {
            const form = e.target.closest('form');
            if (form && !formStartTimes.has(form)) {
                const formId = form.id || form.name || 'unnamed_form';
                formStartTimes.set(form, Date.now());

                trackEvent('form_start', {
                    formId: formId,
                    firstField: e.target.name || e.target.id
                });
            }
        }
    }, { passive: true });

    // Track individual field interactions
    document.addEventListener('focus', (e) => {
        if (e.target.matches('input, textarea, select')) {
            trackEvent('input_focus', {
                field: e.target.name || e.target.id || e.target.type,
                fieldType: e.target.type
            });
        }
    }, { passive: true });

    document.addEventListener('blur', (e) => {
        if (e.target.matches('input, textarea, select')) {
            trackEvent('input_blur', {
                field: e.target.name || e.target.id || e.target.type,
                hasValue: e.target.value.length > 0,
                valueLength: e.target.value.length
            });
        }
    }, { passive: true });

    // Track form submissions
    document.addEventListener('submit', (e) => {
        const form = e.target;
        const formId = form.id || form.name || 'unnamed_form';
        const startTime = formStartTimes.get(form);
        const timeToComplete = startTime ? Date.now() - startTime : null;

        trackEvent('form_submit', {
            formId: formId,
            timeToComplete: timeToComplete,
            fieldCount: form.elements.length,
            action: form.action,
            method: form.method
        });
    });

    // Track form abandonment
    window.addEventListener('beforeunload', () => {
        formStartTimes.forEach((startTime, form) => {
            const formId = form.id || form.name || 'unnamed_form';
            const activeElement = document.activeElement;

            trackEvent('form_abandon', {
                formId: formId,
                timeSpent: Date.now() - startTime,
                lastField: activeElement?.name || activeElement?.id || null,
                fieldsFilled: getFilledFieldsCount(form)
            });
        });
    });

    function getFilledFieldsCount(form) {
        if (!form) return 0;
        const inputs = form.querySelectorAll('input, textarea, select');
        let filled = 0;
        inputs.forEach(input => {
            if (input.value && input.value.length > 0) filled++;
        });
        return filled;
    }

    // ===== BUILDER/TOOL TRACKING =====
    // Track clicks on builder tools
    document.addEventListener('click', (e) => {
        const tool = e.target.closest('[data-tool]');
        if (tool) {
            trackEvent('tool_used', {
                tool: tool.dataset.tool,
                toolName: tool.innerText || tool.dataset.toolName
            });
        }

        // Track save/export actions
        if (e.target.matches('[data-action="save"], [data-action="export"], .save-btn, .export-btn')) {
            trackEvent('project_save', {
                action: e.target.dataset.action || 'save',
                buttonText: e.target.innerText
            });
        }
    }, { passive: true });

    // ===== VISIBILITY TRACKING =====
    let visibilityStartTime = Date.now();
    let totalVisibleTime = 0;

    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            const visibleDuration = Date.now() - visibilityStartTime;
            totalVisibleTime += visibleDuration;

            trackEvent('page_hidden', {
                visibleDuration: visibleDuration,
                totalVisibleTime: totalVisibleTime
            });
        } else {
            visibilityStartTime = Date.now();

            trackEvent('page_visible', {
                totalVisibleTime: totalVisibleTime
            });
        }
    });

    // ===== HEARTBEAT (Legacy compatibility + live status) =====
    function sendHeartbeat() {
        const heartbeatData = {
            ...baseData,
            timeOnPage: Math.floor((Date.now() - sessionStartTime) / 1000),
            isActive: (Date.now() - lastActivity) < 30000, // Active in last 30 seconds
            scrollDepth: maxScrollDepth,
            clickCount: clickCount,
            actionCount: actionCount
        };

        // Local nerve collector
        fetch('http://localhost:6000/api/visitor/heartbeat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(heartbeatData)
        }).catch(err => {});

        // Cloud backup
        fetch('https://builder-pattern-api-production.up.railway.app/api/visitor/heartbeat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(heartbeatData)
        }).catch(err => {});
    }

    setInterval(sendHeartbeat, 10000);
    sendHeartbeat(); // Initial heartbeat

    // ===== SESSION QUALITY SCORE =====
    function calculateQualityScore() {
        const sessionDuration = (Date.now() - sessionStartTime) / 1000; // seconds
        const idleTime = (Date.now() - lastActivity) / 1000;
        const activeTime = sessionDuration - idleTime;

        let score = 0;

        // Time on site (max 30 points)
        if (sessionDuration > 300) score += 30; // 5+ minutes
        else if (sessionDuration > 120) score += 20; // 2+ minutes
        else if (sessionDuration > 60) score += 10; // 1+ minute

        // Engagement (max 30 points)
        if (clickCount > 20) score += 30;
        else if (clickCount > 10) score += 20;
        else if (clickCount > 5) score += 10;

        // Scroll depth (max 20 points)
        score += Math.min(20, Math.floor(maxScrollDepth / 5));

        // Form interaction (max 20 points)
        if (formStartTimes.size > 0) score += 20;

        return Math.min(100, score);
    }

    // ===== INTERCOM POLLING (Legacy compatibility) =====
    async function pollIntercomMessages() {
        if (!userPin || userPin === 'anonymous') return;

        try {
            const response = await fetch(`http://localhost:6000/api/intercom/poll/${userPin}`);
            const messages = await response.json();

            if (messages && messages.length > 0) {
                messages.forEach(msg => {
                    showIntercomMessage(msg.from, msg.message);
                });
            }
        } catch (err) {
            console.log('Intercom service offline');
        }
    }

    setInterval(pollIntercomMessages, 5000);
    pollIntercomMessages();

    function showIntercomMessage(from, message) {
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
        setTimeout(() => popup.remove(), 10000);
    }

    console.log('[Analytics Traps] Deployed successfully - Tracking EVERYTHING');
})();
