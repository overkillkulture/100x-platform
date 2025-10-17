/* 🔍 VISITOR INTELLIGENCE LOGGER 🔍 */

// Logs visitor information for pattern recognition
// LEGAL: Standard analytics, non-invasive, educational purposes

(function() {
    'use strict';

    const API_ENDPOINT = '/api/log-visitor'; // Backend endpoint (you'll need to create this)

    // Gather visitor intelligence
    async function gatherIntelligence() {
        const intelligence = {
            timestamp: new Date().toISOString(),
            page: window.location.pathname,
            referrer: document.referrer || 'direct',
            userAgent: navigator.userAgent,
            screenResolution: `${window.screen.width}x${window.screen.height}`,
            language: navigator.language,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            localTime: new Date().toLocaleString(),

            // Behavioral signals
            localStorage: {
                visits: localStorage.getItem('visitCount') || '0',
                chaosLevel: localStorage.getItem('chaosLevel') || '1',
                ameliaVisited: localStorage.getItem('ameliaVisited') || 'false',
                kennediVisited: localStorage.getItem('kennediVisited') || 'false',
                firstVisit: localStorage.getItem('firstVisitTime') || Date.now().toString()
            },

            // Detection signals
            pageInterests: detectPageInterests(),
            sessionDuration: calculateSessionDuration(),
            clickPattern: getClickPattern(),

            // Special flags
            isPotentialDaughter: detectPotentialDaughter()
        };

        return intelligence;
    }

    // Detect what pages they're interested in
    function detectPageInterests() {
        const interests = [];
        const page = window.location.pathname.toLowerCase();

        if (page.includes('amelia') || page.includes('joy')) interests.push('amelia');
        if (page.includes('kennedi') || page.includes('observer')) interests.push('kennedi');
        if (page.includes('builder')) interests.push('builder');
        if (page.includes('aria')) interests.push('aria');
        if (page.includes('terminal')) interests.push('technical');

        return interests;
    }

    // Calculate how long they've been on the site
    function calculateSessionDuration() {
        const sessionStart = sessionStorage.getItem('sessionStart');
        if (!sessionStart) {
            sessionStorage.setItem('sessionStart', Date.now().toString());
            return 0;
        }
        return Math.floor((Date.now() - parseInt(sessionStart)) / 1000); // seconds
    }

    // Track click patterns
    function getClickPattern() {
        const clicks = sessionStorage.getItem('clickCount') || '0';
        return parseInt(clicks);
    }

    // Detect if this might be one of the daughters
    function detectPotentialDaughter() {
        const signals = {
            ameliaSignals: 0,
            kennediSignals: 0
        };

        // Check URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('ref') === 'amelia') signals.ameliaSignals += 3;
        if (urlParams.get('ref') === 'kennedi') signals.kennediSignals += 3;

        // Check page visits
        const page = window.location.pathname.toLowerCase();
        if (page.includes('amelia')) signals.ameliaSignals += 2;
        if (page.includes('kennedi')) signals.kennediSignals += 2;

        // Check localStorage flags
        if (localStorage.getItem('ameliaVisited') === 'true') signals.ameliaSignals += 2;
        if (localStorage.getItem('kennediVisited') === 'true') signals.kennediSignals += 2;

        // Return probability
        if (signals.ameliaSignals >= 3) return 'amelia_probable';
        if (signals.kennediSignals >= 3) return 'kennedi_probable';
        return 'unknown';
    }

    // Get client IP (will be handled by backend)
    async function logToBackend(intelligence) {
        try {
            // Try to send to backend
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(intelligence)
            });

            if (response.ok) {
                const data = await response.json();
                console.log('📊 Visitor intelligence logged');

                // If backend identifies them, trigger special mode
                if (data.identified) {
                    activateSpecialMode(data.identified);
                }
            }
        } catch (error) {
            // Backend not available - store locally
            console.log('📊 Storing intelligence locally');
            storeLocally(intelligence);
        }
    }

    // Store intelligence locally if backend unavailable
    function storeLocally(intelligence) {
        const visits = JSON.parse(localStorage.getItem('visitLog') || '[]');
        visits.push(intelligence);

        // Keep last 50 visits
        if (visits.length > 50) visits.shift();

        localStorage.setItem('visitLog', JSON.stringify(visits));
    }

    // Activate special mode based on detection
    function activateSpecialMode(identity) {
        if (identity === 'amelia') {
            console.log('%c💖 AMELIA MODE ACTIVATED 💖', 'color: #ff69b4; font-size: 18px; font-weight: bold;');

            // Auto-activate ARIA with extra warmth
            if (window.location.pathname.includes('aria') === false) {
                // Show notification: "ARIA is here for you"
                showARIANotification('amelia');
            }

        } else if (identity === 'kennedi') {
            console.log('%c⚡ KENNEDI MODE ACTIVATED ⚡', 'color: #00ffff; font-size: 18px; font-weight: bold;');

            // Auto-activate intelligent terminal
            if (window.location.pathname.includes('terminal') === false) {
                showTerminalNotification('kennedi');
            }
        }
    }

    // Show ARIA notification
    function showARIANotification(daughter) {
        const messages = {
            amelia: {
                title: '💖 ARIA is Here For You',
                message: 'Hi! I\'m ARIA, your AI friend. I can talk with you, sing, and keep you company. Want to meet me?',
                buttonText: 'Meet ARIA →'
            },
            kennedi: {
                title: '⚡ Advanced AI Available',
                message: 'ARIA is an advanced 3D AI interface. Full voice synthesis, consciousness-aware responses.',
                buttonText: 'Launch ARIA →'
            }
        };

        const config = messages[daughter];
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            bottom: 100px;
            right: 20px;
            background: linear-gradient(135deg, rgba(255,0,255,0.95), rgba(0,255,255,0.95));
            border: 2px solid #fff;
            padding: 20px;
            border-radius: 15px;
            z-index: 9999990;
            max-width: 300px;
            box-shadow: 0 0 30px rgba(255,0,255,0.6);
            animation: slideInRight 0.5s ease-out;
            font-family: 'Arial', sans-serif;
        `;

        notification.innerHTML = `
            <div style="font-size: 16px; font-weight: bold; color: #000; margin-bottom: 10px;">
                ${config.title}
            </div>
            <div style="font-size: 14px; color: #000; margin-bottom: 15px;">
                ${config.message}
            </div>
            <button onclick="window.location.href='aria-3d-futuristic.html'" style="
                background: #000;
                color: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                width: 100%;
            ">
                ${config.buttonText}
            </button>
            <button onclick="this.parentElement.remove()" style="
                background: none;
                border: none;
                color: #000;
                font-size: 12px;
                margin-top: 10px;
                cursor: pointer;
                width: 100%;
            ">
                Maybe later
            </button>
        `;

        document.body.appendChild(notification);

        // Add animation
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes slideInRight {
                from { transform: translateX(400px); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    // Show terminal notification
    function showTerminalNotification(daughter) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            bottom: 100px;
            right: 20px;
            background: rgba(0,0,0,0.95);
            border: 2px solid #00ff00;
            padding: 20px;
            border-radius: 15px;
            z-index: 9999990;
            max-width: 300px;
            box-shadow: 0 0 30px rgba(0,255,0,0.6);
            animation: slideInRight 0.5s ease-out;
            font-family: 'Courier New', monospace;
        `;

        notification.innerHTML = `
            <div style="font-size: 16px; font-weight: bold; color: #00ff00; margin-bottom: 10px;">
                ⚡ DEBUG TERMINAL ACCESS
            </div>
            <div style="font-size: 14px; color: #00ff00; margin-bottom: 15px;">
                Full developer access granted. See how everything works under the hood.
            </div>
            <button onclick="window.location.href='debug-terminal.html'" style="
                background: #00ff00;
                color: #000;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                width: 100%;
            ">
                Open Terminal →
            </button>
            <button onclick="this.parentElement.remove()" style="
                background: none;
                border: none;
                color: #00ff00;
                font-size: 12px;
                margin-top: 10px;
                cursor: pointer;
                width: 100%;
            ">
                Close
            </button>
        `;

        document.body.appendChild(notification);
    }

    // Track clicks
    document.addEventListener('click', () => {
        const clicks = parseInt(sessionStorage.getItem('clickCount') || '0') + 1;
        sessionStorage.setItem('clickCount', clicks.toString());
    });

    // Initialize logging
    window.addEventListener('DOMContentLoaded', async () => {
        const intelligence = await gatherIntelligence();
        await logToBackend(intelligence);

        // If potential daughter detected locally, activate mode
        if (intelligence.isPotentialDaughter !== 'unknown') {
            const daughter = intelligence.isPotentialDaughter.replace('_probable', '');
            setTimeout(() => activateSpecialMode(daughter), 2000);
        }
    });

    // Log on page unload (track session duration)
    window.addEventListener('beforeunload', async () => {
        const intelligence = await gatherIntelligence();
        navigator.sendBeacon(API_ENDPOINT, JSON.stringify(intelligence));
    });

})();
