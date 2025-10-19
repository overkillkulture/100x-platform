// UNIVERSAL BUG NOTEPAD V2 - WITH AUTO-DEBUG + TWO-WAY COMMUNICATION
// Automatically captures console errors, system info, and allows Commander responses

(function() {
    'use strict';

    // Auto-capture console errors
    let consoleErrors = [];
    const originalConsoleError = console.error;
    console.error = function(...args) {
        consoleErrors.push({
            timestamp: new Date().toISOString(),
            message: args.join(' ')
        });
        originalConsoleError.apply(console, args);
    };

    // Auto-capture console warnings
    let consoleWarnings = [];
    const originalConsoleWarn = console.warn;
    console.warn = function(...args) {
        consoleWarnings.push({
            timestamp: new Date().toISOString(),
            message: args.join(' ')
        });
        originalConsoleWarn.apply(console, args);
    };

    // Create bug notepad HTML
    const bugNotepadHTML = `
        <div id="bug-notepad-widget" style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 999999;
            font-family: 'Courier New', monospace;
        ">
            <!-- Notification Badge -->
            <div id="bug-notification-badge" style="
                display: none;
                position: absolute;
                top: -8px;
                right: -8px;
                background: #00ff41;
                color: #000;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                font-size: 0.8rem;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 10px rgba(0, 255, 65, 0.8);
                animation: badge-pulse 1s infinite;
            "></div>

            <!-- Minimized State: Just a button -->
            <div id="bug-notepad-minimized" style="
                background: linear-gradient(135deg, #ff4444, #cc0000);
                color: white;
                padding: 15px 20px;
                border-radius: 50px;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(255, 68, 68, 0.5);
                font-size: 1rem;
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s;
            ">
                🐛 REPORT BUG
            </div>

            <!-- Expanded State: Full notepad -->
            <div id="bug-notepad-expanded" style="
                display: none;
                background: rgba(0, 0, 0, 0.95);
                border: 3px solid #ff4444;
                border-radius: 15px;
                padding: 20px;
                width: 450px;
                max-height: 600px;
                overflow-y: auto;
                box-shadow: 0 10px 40px rgba(255, 68, 68, 0.5);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3 style="color: #ff4444; margin: 0; font-size: 1.3rem;">🐛 Bug Report (Auto-Debug)</h3>
                    <button id="bug-notepad-close" style="
                        background: transparent;
                        border: 2px solid #ff4444;
                        color: #ff4444;
                        padding: 5px 12px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 1rem;
                        font-weight: bold;
                    ">✕</button>
                </div>

                <!-- Commander Responses (if any) -->
                <div id="bug-responses" style="display: none; margin-bottom: 15px;">
                    <div style="
                        background: rgba(0, 255, 65, 0.1);
                        border: 2px solid #00ff41;
                        border-radius: 10px;
                        padding: 15px;
                    ">
                        <div style="color: #00ff41; font-size: 0.9rem; margin-bottom: 5px; font-weight: bold;">
                            📢 Commander Response:
                        </div>
                        <div id="bug-response-text" style="color: #00ff41; font-size: 1rem; line-height: 1.5;">
                        </div>
                    </div>
                </div>

                <div style="margin-bottom: 15px;">
                    <label style="color: #00ff41; display: block; margin-bottom: 5px; font-size: 0.9rem;">
                        What page are you on?
                    </label>
                    <input type="text" id="bug-page" readonly style="
                        width: 100%;
                        padding: 10px;
                        background: rgba(0, 255, 65, 0.1);
                        border: 2px solid #00ff41;
                        border-radius: 8px;
                        color: #00ff41;
                        font-family: 'Courier New', monospace;
                        font-size: 0.9rem;
                    ">
                </div>

                <div style="margin-bottom: 15px;">
                    <label style="color: #00ff41; display: block; margin-bottom: 5px; font-size: 0.9rem;">
                        What's broken? (describe the issue)
                    </label>
                    <textarea id="bug-description" placeholder="e.g., Voice recording not working, button doesn't click, page won't load..." style="
                        width: 100%;
                        height: 120px;
                        padding: 10px;
                        background: rgba(0, 255, 65, 0.1);
                        border: 2px solid #00ff41;
                        border-radius: 8px;
                        color: #00ff41;
                        font-family: 'Courier New', monospace;
                        font-size: 0.9rem;
                        resize: vertical;
                    "></textarea>
                </div>

                <!-- Auto-captured debug info (collapsible) -->
                <div style="margin-bottom: 15px;">
                    <button id="toggle-debug-info" style="
                        width: 100%;
                        padding: 10px;
                        background: rgba(255, 68, 68, 0.2);
                        border: 2px solid #ff4444;
                        border-radius: 8px;
                        color: #ff4444;
                        cursor: pointer;
                        font-family: 'Courier New', monospace;
                        font-size: 0.9rem;
                    ">
                        🔍 Show Auto-Captured Debug Info (${consoleErrors.length} errors detected)
                    </button>
                    <div id="debug-info-panel" style="
                        display: none;
                        margin-top: 10px;
                        background: rgba(0, 0, 0, 0.5);
                        border: 2px solid #ff4444;
                        border-radius: 8px;
                        padding: 10px;
                        max-height: 200px;
                        overflow-y: auto;
                    ">
                        <div style="color: #ff4444; font-size: 0.8rem; white-space: pre-wrap;" id="debug-info-content"></div>
                    </div>
                </div>

                <button id="bug-submit" style="
                    width: 100%;
                    padding: 12px;
                    background: linear-gradient(135deg, #ff4444, #cc0000);
                    border: none;
                    border-radius: 10px;
                    color: white;
                    font-size: 1.1rem;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s;
                    font-family: 'Courier New', monospace;
                ">
                    📤 SUBMIT BUG REPORT (With Auto-Debug)
                </button>

                <div id="bug-status" style="
                    margin-top: 15px;
                    padding: 10px;
                    background: rgba(0, 255, 65, 0.1);
                    border: 2px solid #00ff41;
                    border-radius: 8px;
                    color: #00ff41;
                    font-size: 0.9rem;
                    text-align: center;
                    display: none;
                "></div>
            </div>
        </div>

        <style>
            @keyframes badge-pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.2); }
            }
        </style>
    `;

    // Inject into page
    document.body.insertAdjacentHTML('beforeend', bugNotepadHTML);

    // Get elements
    const minimized = document.getElementById('bug-notepad-minimized');
    const expanded = document.getElementById('bug-notepad-expanded');
    const closeBtn = document.getElementById('bug-notepad-close');
    const submitBtn = document.getElementById('bug-submit');
    const pageInput = document.getElementById('bug-page');
    const descriptionInput = document.getElementById('bug-description');
    const statusDiv = document.getElementById('bug-status');
    const toggleDebugBtn = document.getElementById('toggle-debug-info');
    const debugInfoPanel = document.getElementById('debug-info-panel');
    const debugInfoContent = document.getElementById('debug-info-content');
    const responsesDiv = document.getElementById('bug-responses');
    const responseText = document.getElementById('bug-response-text');
    const notificationBadge = document.getElementById('bug-notification-badge');

    // Set current page URL
    pageInput.value = window.location.href;

    // Show/Hide notepad
    minimized.addEventListener('click', () => {
        minimized.style.display = 'none';
        expanded.style.display = 'block';
        checkForResponses();
    });

    closeBtn.addEventListener('click', () => {
        expanded.style.display = 'none';
        minimized.style.display = 'flex';
    });

    // Toggle debug info
    toggleDebugBtn.addEventListener('click', () => {
        if (debugInfoPanel.style.display === 'none') {
            debugInfoPanel.style.display = 'block';
            updateDebugInfo();
        } else {
            debugInfoPanel.style.display = 'none';
        }
    });

    // Update debug info
    function updateDebugInfo() {
        const debugInfo = {
            browser: navigator.userAgent,
            screen: `${window.screen.width}x${window.screen.height}`,
            viewport: `${window.innerWidth}x${window.innerHeight}`,
            url: window.location.href,
            timestamp: new Date().toISOString(),
            errors: consoleErrors,
            warnings: consoleWarnings,
            localStorage: localStorage.length + ' items',
            cookies: document.cookie ? 'Enabled' : 'Disabled'
        };

        debugInfoContent.textContent = JSON.stringify(debugInfo, null, 2);
        toggleDebugBtn.textContent = `🔍 Show Auto-Captured Debug Info (${consoleErrors.length} errors, ${consoleWarnings.length} warnings)`;
    }

    // Hover effect for minimized button
    minimized.addEventListener('mouseenter', () => {
        minimized.style.transform = 'scale(1.1)';
        minimized.style.boxShadow = '0 6px 30px rgba(255, 68, 68, 0.7)';
    });

    minimized.addEventListener('mouseleave', () => {
        minimized.style.transform = 'scale(1)';
        minimized.style.boxShadow = '0 4px 20px rgba(255, 68, 68, 0.5)';
    });

    // Check for Commander responses
    function checkForResponses() {
        const responses = JSON.parse(localStorage.getItem('commander_responses') || '[]');
        const currentPage = window.location.pathname;

        const relevantResponses = responses.filter(r =>
            r.page === currentPage && !r.read
        );

        if (relevantResponses.length > 0) {
            responsesDiv.style.display = 'block';
            responseText.innerHTML = relevantResponses.map(r =>
                `<div style="margin-bottom: 10px;">${r.message}</div>`
            ).join('');

            // Play notification sound
            playNotificationSound();

            // Mark as read
            responses.forEach(r => {
                if (relevantResponses.includes(r)) {
                    r.read = true;
                }
            });
            localStorage.setItem('commander_responses', JSON.stringify(responses));

            // Update badge
            notificationBadge.textContent = relevantResponses.length;
            notificationBadge.style.display = 'flex';
        } else {
            responsesDiv.style.display = 'none';
            notificationBadge.style.display = 'none';
        }
    }

    // Play notification sound
    function playNotificationSound() {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.frequency.value = 800; // Hz
        oscillator.type = 'sine';

        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
    }

    // Submit bug report
    submitBtn.addEventListener('click', async () => {
        const page = pageInput.value;
        const description = descriptionInput.value.trim();

        if (!description) {
            statusDiv.style.display = 'block';
            statusDiv.style.borderColor = '#ff4444';
            statusDiv.style.color = '#ff4444';
            statusDiv.textContent = '❌ Please describe the bug first!';
            return;
        }

        // Gather auto-debug info
        const debugInfo = {
            browser: navigator.userAgent,
            screen: `${window.screen.width}x${window.screen.height}`,
            viewport: `${window.innerWidth}x${window.innerHeight}`,
            url: window.location.href,
            timestamp: new Date().toISOString(),
            errors: consoleErrors,
            warnings: consoleWarnings,
            localStorage: localStorage.length + ' items',
            cookies: document.cookie ? 'Enabled' : 'Disabled',
            connection: navigator.connection ? {
                effectiveType: navigator.connection.effectiveType,
                downlink: navigator.connection.downlink
            } : 'Unknown'
        };

        // Save to localStorage
        const bugReport = {
            id: Date.now(),
            timestamp: new Date().toISOString(),
            page: page,
            description: description,
            debugInfo: debugInfo,
            read: false
        };

        // Get existing bug reports
        let bugReports = [];
        try {
            const existing = localStorage.getItem('bug_reports');
            if (existing) {
                bugReports = JSON.parse(existing);
            }
        } catch (e) {
            bugReports = [];
        }

        // Add new report
        bugReports.push(bugReport);
        localStorage.setItem('bug_reports', JSON.stringify(bugReports));

        // Play success sound
        playNotificationSound();

        // Show success message
        statusDiv.style.display = 'block';
        statusDiv.style.borderColor = '#00ff41';
        statusDiv.style.color = '#00ff41';
        statusDiv.innerHTML = `
            ✅ Bug report submitted!<br/>
            <small>Commander will review and may send you a response.</small>
        `;

        // Clear the description
        descriptionInput.value = '';

        // Auto-close after 3 seconds
        setTimeout(() => {
            expanded.style.display = 'none';
            minimized.style.display = 'flex';
            statusDiv.style.display = 'none';
        }, 3000);

        // Log to console for debugging
        console.log('🐛 BUG REPORT SUBMITTED:', bugReport);
    });

    // ESC key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && expanded.style.display === 'block') {
            expanded.style.display = 'none';
            minimized.style.display = 'flex';
        }
    });

    // Check for responses every 10 seconds
    setInterval(checkForResponses, 10000);

    // Initial check
    checkForResponses();

    console.log('🐛 Universal Bug Notepad V2 Active - Auto-debug enabled, two-way communication ready');
})();
