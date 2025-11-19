/**
 * 🧭 UNIVERSAL NAVIGATION SYSTEM
 * Adds consistent navigation to all pages
 * Auto-injects on page load
 */

(function() {
    'use strict';

    const navHTML = `
        <div id="universal-nav" style="
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            z-index: 10000;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        ">
            <div style="display: flex; align-items: center; gap: 30px;">
                <a href="/index.html" style="color: white; text-decoration: none; font-size: 1.3em; font-weight: bold;">
                    🌀 100X
                </a>
                <nav style="display: flex; gap: 20px;">
                    <a href="/dashboard.html" class="nav-link">Dashboard</a>
                    <a href="/tools-hub.html" class="nav-link">Tools</a>
                    <a href="/analytics-hub.html" class="nav-link">Analytics</a>
                    <a href="/trinity-hub.html" class="nav-link">Trinity</a>
                    <a href="/business-hub.html" class="nav-link">Business</a>
                </nav>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <button onclick="window.ArayaTour && window.ArayaTour.start()"
                        style="background: rgba(255,255,255,0.2); border: 1px solid white; color: white; padding: 8px 16px; border-radius: 6px; cursor: pointer;">
                    🤖 Tour with Araya
                </button>
                <span id="nav-user-name" style="color: white; opacity: 0.9;"></span>
                <button onclick="window.AuthGate && window.AuthGate.logout()"
                        style="background: rgba(255,255,255,0.2); border: 1px solid white; color: white; padding: 8px 16px; border-radius: 6px; cursor: pointer;">
                    Logout
                </button>
            </div>
        </div>
        <style>
            body { padding-top: 70px !important; }
            .nav-link {
                color: white;
                text-decoration: none;
                opacity: 0.9;
                transition: opacity 0.3s;
                font-weight: 500;
            }
            .nav-link:hover {
                opacity: 1;
                text-decoration: underline;
            }
            @media (max-width: 768px) {
                #universal-nav { flex-direction: column; gap: 15px; padding: 15px; }
                #universal-nav nav { flex-wrap: wrap; }
            }
        </style>
    `;

    function injectNav() {
        // Don't inject on login pages
        if (window.location.pathname.includes('login') ||
            window.location.pathname.includes('screening') ||
            window.location.pathname === '/') {
            return;
        }

        // Inject at top of body
        if (document.body) {
            document.body.insertAdjacentHTML('afterbegin', navHTML);

            // Show user name if logged in
            if (window.AuthGate) {
                const user = window.AuthGate.getCurrentUser();
                if (user && user.name) {
                    const nameEl = document.getElementById('nav-user-name');
                    if (nameEl) {
                        nameEl.textContent = user.name;
                    }
                }
            }
        }
    }

    // Auto-inject on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectNav);
    } else {
        injectNav();
    }

    console.log('🧭 Universal navigation loaded');
})();

// Load visitor tracking
const trackingScript = document.createElement('script');
trackingScript.src = '/simple-tracking.js';
document.head.appendChild(trackingScript);

// Load Universal HUD System
const hudScript = document.createElement('script');
hudScript.src = '/universal-hud.js';
document.head.appendChild(hudScript);
