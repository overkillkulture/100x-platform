/**
 * 🎮 UNIVERSAL JARVIS HUD EMBED 🎮
 * Automatically loads the JARVIS HUD on any page for authenticated users
 *
 * Usage: Add this script to any page:
 * <script src="/universal-hud-embed.js"></script>
 *
 * Features:
 * - Auto-detects if user is logged in
 * - Loads HUD in floating overlay
 * - Draggable, resizable
 * - Toggle with keyboard shortcut (Ctrl+J)
 * - Persists state across pages
 */

(function() {
    'use strict';

    // Check if user is authenticated
    const userPin = localStorage.getItem('beta_user_pin');
    const userName = localStorage.getItem('beta_user_name');

    if (!userPin) {
        console.log('🔒 User not authenticated - HUD not loaded');
        return;
    }

    console.log('✅ Authenticated as:', userName);

    // Check if we should load the HUD (user preference)
    const hudEnabled = localStorage.getItem('hud_enabled') !== 'false'; // Default: enabled

    if (!hudEnabled) {
        console.log('⏸️ HUD disabled by user preference');
        return;
    }

    // Create HUD container
    function createHUD() {
        // Don't load on the jarvis.html page itself (would be recursive!)
        if (window.location.pathname.includes('jarvis.html')) {
            return;
        }

        // Create overlay container
        const hudContainer = document.createElement('div');
        hudContainer.id = 'jarvis-hud-container';
        hudContainer.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 400px;
            height: 500px;
            z-index: 999999;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0, 255, 255, 0.3);
            overflow: hidden;
            transition: all 0.3s ease;
            display: none;
        `;

        // Create iframe
        const iframe = document.createElement('iframe');
        iframe.id = 'jarvis-hud-iframe';
        iframe.src = '/jarvis.html';
        iframe.style.cssText = `
            width: 100%;
            height: 100%;
            border: none;
            border-radius: 16px;
        `;

        hudContainer.appendChild(iframe);

        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'jarvis-hud-toggle';
        toggleBtn.innerHTML = '🎮 JARVIS';
        toggleBtn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.9), rgba(0, 200, 200, 0.9));
            color: #000;
            border: 2px solid #00ffff;
            border-radius: 50px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            z-index: 999998;
            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.4);
            transition: all 0.3s ease;
            font-family: 'Courier New', monospace;
        `;

        toggleBtn.onmouseover = () => {
            toggleBtn.style.transform = 'scale(1.1)';
            toggleBtn.style.boxShadow = '0 6px 20px rgba(0, 255, 255, 0.6)';
        };

        toggleBtn.onmouseout = () => {
            toggleBtn.style.transform = 'scale(1)';
            toggleBtn.style.boxShadow = '0 4px 15px rgba(0, 255, 255, 0.4)';
        };

        toggleBtn.onclick = () => toggleHUD();

        document.body.appendChild(hudContainer);
        document.body.appendChild(toggleBtn);

        // Restore previous state
        const wasOpen = localStorage.getItem('hud_open') === 'true';
        if (wasOpen) {
            openHUD();
        }
    }

    // Toggle HUD visibility
    function toggleHUD() {
        const container = document.getElementById('jarvis-hud-container');
        const btn = document.getElementById('jarvis-hud-toggle');

        if (container.style.display === 'none' || !container.style.display) {
            openHUD();
        } else {
            closeHUD();
        }
    }

    function openHUD() {
        const container = document.getElementById('jarvis-hud-container');
        const btn = document.getElementById('jarvis-hud-toggle');

        container.style.display = 'block';
        btn.style.display = 'none';
        localStorage.setItem('hud_open', 'true');

        // Add close button to HUD
        if (!document.getElementById('jarvis-hud-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.id = 'jarvis-hud-close';
            closeBtn.innerHTML = '✕';
            closeBtn.style.cssText = `
                position: fixed;
                bottom: 530px;
                right: 20px;
                background: rgba(255, 0, 0, 0.9);
                color: white;
                border: 2px solid #ff0000;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                font-size: 20px;
                cursor: pointer;
                z-index: 1000000;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 15px rgba(255, 0, 0, 0.4);
                transition: all 0.3s ease;
            `;

            closeBtn.onmouseover = () => {
                closeBtn.style.transform = 'scale(1.1)';
                closeBtn.style.boxShadow = '0 6px 20px rgba(255, 0, 0, 0.6)';
            };

            closeBtn.onmouseout = () => {
                closeBtn.style.transform = 'scale(1)';
                closeBtn.style.boxShadow = '0 4px 15px rgba(255, 0, 0, 0.4)';
            };

            closeBtn.onclick = () => closeHUD();
            document.body.appendChild(closeBtn);
        } else {
            document.getElementById('jarvis-hud-close').style.display = 'flex';
        }
    }

    function closeHUD() {
        const container = document.getElementById('jarvis-hud-container');
        const btn = document.getElementById('jarvis-hud-toggle');
        const closeBtn = document.getElementById('jarvis-hud-close');

        container.style.display = 'none';
        btn.style.display = 'block';
        if (closeBtn) closeBtn.style.display = 'none';
        localStorage.setItem('hud_open', 'false');
    }

    // Keyboard shortcut: Ctrl+J to toggle
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'j') {
            e.preventDefault();
            toggleHUD();
        }
    });

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createHUD);
    } else {
        createHUD();
    }

    console.log('🎮 JARVIS HUD loaded! Press Ctrl+J or click the button to open.');

})();

// Load Araya Bug Widget for beta testers
const script = document.createElement('script');
script.src = '/ARAYA_BUG_WIDGET.js';
document.body.appendChild(script);
