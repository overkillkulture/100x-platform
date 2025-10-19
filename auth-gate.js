/**
 * 🔐 UNIVERSAL AUTHENTICATION GATE
 * Simple, secure authentication system for Consciousness Revolution
 * Usage: Include on any protected page with <script src="/auth-gate.js"></script>
 */

(function() {
    'use strict';

    // Beta tester database (in production, fetch from server)
    const BETA_USERS = {
        "1001": {
            "pin": "1001",
            "name": "Joshua Serrano",
            "email": "joshua.serrano2022@gmail.com",
            "status": "Active",
            "role": "Beta Tester",
            "package": "JARVIS Mission Control"
        },
        "1002": {
            "pin": "1002",
            "name": "Toby Burrowes",
            "email": "toby.burrowes@gmail.com",
            "status": "Active",
            "role": "Beta Tester",
            "package": "Security & Analytics"
        },
        "1003": {
            "pin": "1003",
            "name": "WD Brotherton",
            "email": "wd.brotherton@gmail.com",
            "status": "Active",
            "role": "Beta Tester",
            "package": "Builder Tools Suite"
        },
        "1004": {
            "pin": "1004",
            "name": "Dean Sabr",
            "email": "dean.sabr@gmail.com",
            "status": "Active",
            "role": "Beta Tester",
            "package": "Pattern Recognition"
        },
        "1005": {
            "pin": "1005",
            "name": "Bill Varni",
            "email": "bill.varni@gmail.com",
            "status": "Active",
            "role": "Beta Tester",
            "package": "Team Leadership"
        },
        "1006": {
            "pin": "1006",
            "name": "Rutherford",
            "email": "rutherford@gmail.com",
            "status": "Active",
            "role": "Beta Tester",
            "package": "Scout & Explorer"
        },
        "2025": {
            "pin": "2025",
            "name": "Commander",
            "email": "darrick.preble@gmail.com",
            "status": "Active",
            "role": "Admin",
            "package": "Full Platform Access"
        }
    };

    // Check if user is authenticated
    function isAuthenticated() {
        const pin = localStorage.getItem('beta_user_pin');
        const name = localStorage.getItem('beta_user_name');
        return pin && name && BETA_USERS[pin];
    }

    // Get current user data
    function getCurrentUser() {
        const pin = localStorage.getItem('beta_user_pin');
        return BETA_USERS[pin] || null;
    }

    // Login function
    function login(pin) {
        const user = BETA_USERS[pin];
        if (user) {
            localStorage.setItem('beta_user_pin', pin);
            localStorage.setItem('beta_user_name', user.name);
            localStorage.setItem('beta_user_email', user.email);
            localStorage.setItem('beta_user_role', user.role);
            localStorage.setItem('beta_login_time', new Date().toISOString());
            return true;
        }
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

    // Protect page - redirect to login if not authenticated
    function protectPage() {
        // Don't protect the login page itself
        if (window.location.pathname.includes('beta-login.html') ||
            window.location.pathname.includes('forgot-pin.html') ||
            window.location.pathname.includes('screening.html')) {
            return;
        }

        if (!isAuthenticated()) {
            console.log('🔒 Authentication required - redirecting to login');
            window.location.href = '/beta-login.html?redirect=' + encodeURIComponent(window.location.pathname);
        } else {
            console.log('✅ User authenticated:', getCurrentUser().name);
        }
    }

    // Export functions to window
    window.AuthGate = {
        isAuthenticated: isAuthenticated,
        getCurrentUser: getCurrentUser,
        login: login,
        logout: logout,
        protectPage: protectPage,
        BETA_USERS: BETA_USERS
    };

    // Auto-protect page on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', protectPage);
    } else {
        protectPage();
    }

    console.log('🔐 Auth Gate loaded');
})();
