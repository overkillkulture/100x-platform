/**
 * UNIVERSAL USER DISPLAY
 * Shows logged-in user on every page in small, non-intrusive corner
 * Bug #91 fix
 */

(function() {
    'use strict';

    function init() {
        // Get username from localStorage
        const username = localStorage.getItem('userName') ||          // From login.html
                         localStorage.getItem('workspace_user_name') ||
                         localStorage.getItem('user_name') ||
                         localStorage.getItem('username');

        if (!username) {
            console.log('[USER DISPLAY] No logged-in user found');
            return; // Don't show widget if no user logged in
        }

        // Create user display widget
        const userDisplay = document.createElement('div');
        userDisplay.id = 'userDisplay';
        userDisplay.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.85);
            border: 1px solid #00ff88;
            color: #00ff88;
            padding: 8px 12px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            z-index: 999998;
            box-shadow: 0 2px 10px rgba(0, 255, 136, 0.3);
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            transition: all 0.3s;
        `;

        userDisplay.innerHTML = `
            <span style="opacity: 0.7;">👤</span>
            <span style="font-weight: bold;">${username}</span>
        `;

        // Hover effect
        userDisplay.addEventListener('mouseenter', () => {
            userDisplay.style.background = 'rgba(0, 255, 136, 0.15)';
            userDisplay.style.transform = 'scale(1.05)';
        });

        userDisplay.addEventListener('mouseleave', () => {
            userDisplay.style.background = 'rgba(0, 0, 0, 0.85)';
            userDisplay.style.transform = 'scale(1)';
        });

        // Click to show user menu (optional - can expand later)
        userDisplay.addEventListener('click', () => {
            console.log('[USER DISPLAY] User:', username);
            // Could add logout, profile, etc. here in future
        });

        document.body.appendChild(userDisplay);
        console.log('[USER DISPLAY] Showing user:', username);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
