/**
 * 🔐 AUTHENTICATION GATE - AIRTABLE VERSION
 * Fetches users from Airtable instead of hardcoded data
 */

(function() {
    'use strict';

    const AIRTABLE_TOKEN = 'pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757';
    const AIRTABLE_BASE = 'app7F75X1uny6jPfd';
    const AIRTABLE_TABLE = 'Beta_Users';

    let BETA_USERS = {};
    let usersLoaded = false;

    // Load users from Airtable
    async function loadUsers() {
        try {
            const response = await fetch(
                `https://api.airtable.com/v0/${AIRTABLE_BASE}/${AIRTABLE_TABLE}`,
                {
                    headers: {
                        'Authorization': `Bearer ${AIRTABLE_TOKEN}`
                    }
                }
            );

            const data = await response.json();

            // Convert to PIN-keyed object
            BETA_USERS = {};
            data.records.forEach(record => {
                const pin = record.fields.PIN;
                if (pin) {
                    BETA_USERS[pin] = {
                        pin: pin,
                        name: record.fields.Name || '',
                        email: record.fields.Email || '',
                        status: record.fields.Status || 'Active',
                        role: record.fields.Role || 'Beta Tester',
                        package: record.fields.Package || ''
                    };
                }
            });

            usersLoaded = true;
            console.log('✅ Loaded', Object.keys(BETA_USERS).length, 'users from Airtable');
            return true;
        } catch (error) {
            console.error('❌ Error loading users:', error);
            return false;
        }
    }

    // Check if user is authenticated
    function isAuthenticated() {
        const pin = localStorage.getItem('beta_user_pin');
        const name = localStorage.getItem('beta_user_name');
        return pin && name;
    }

    // Get current user data
    function getCurrentUser() {
        const pin = localStorage.getItem('beta_user_pin');
        return BETA_USERS[pin] || {
            pin: pin,
            name: localStorage.getItem('beta_user_name'),
            email: localStorage.getItem('beta_user_email'),
            role: localStorage.getItem('beta_user_role')
        };
    }

    // Login function
    async function login(pin) {
        // Make sure users are loaded
        if (!usersLoaded) {
            await loadUsers();
        }

        const user = BETA_USERS[pin];
        if (user && user.status === 'Active') {
            localStorage.setItem('beta_user_pin', pin);
            localStorage.setItem('beta_user_name', user.name);
            localStorage.setItem('beta_user_email', user.email);
            localStorage.setItem('beta_user_role', user.role);
            localStorage.setItem('beta_login_time', new Date().toISOString());
            console.log('✅ Logged in as:', user.name);
            return true;
        }
        console.log('❌ Invalid PIN or inactive user');
        return false;
    }

    // Logout function
    function logout() {
        localStorage.removeItem('beta_user_pin');
        localStorage.removeItem('beta_user_name');
        localStorage.removeItem('beta_user_email');
        localStorage.removeItem('beta_user_role');
        localStorage.removeItem('beta_login_time');
        window.location.href = '/beta-login.html';
    }

    // Protect page
    async function protectPage() {
        // Don't protect public pages
        if (window.location.pathname.includes('beta-login.html') ||
            window.location.pathname.includes('forgot-pin.html') ||
            window.location.pathname.includes('screening.html') ||
            window.location.pathname === '/' ||
            window.location.pathname === '/index.html') {
            return;
        }

        // Load users first
        if (!usersLoaded) {
            await loadUsers();
        }

        if (!isAuthenticated()) {
            console.log('🔒 Authentication required');
            window.location.href = '/beta-login.html?redirect=' + encodeURIComponent(window.location.pathname);
        } else {
            const user = getCurrentUser();
            console.log('✅ Authenticated:', user.name);
        }
    }

    // Export to window
    window.AuthGate = {
        isAuthenticated,
        getCurrentUser,
        login,
        logout,
        protectPage,
        loadUsers,
        get BETA_USERS() { return BETA_USERS; }
    };

    // Auto-load users and protect page
    (async function init() {
        await loadUsers();
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', protectPage);
        } else {
            await protectPage();
        }
    })();

    console.log('🔐 Auth Gate (Airtable) loaded');
})();
