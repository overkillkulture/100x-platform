/**
 * UNIVERSAL NAVIGATION SYSTEM
 * Permanent integration component for seamless platform navigation
 * Automatically injects navigation UI on all 100X Platform pages
 */

const PLATFORM_PAGES = {
    home: { url: '/', name: 'Home', icon: '🏠' },
    login: { url: '/simple-gate.html', name: 'Login', icon: '🔐' },
    workspace: { url: '/workspace-v3.html', name: 'Workspace', icon: '💼' },
    commandCenter: { url: '/COMMAND_CENTER_HUD_COMMS.html', name: 'Command Center', icon: '🎮' },
    mobile: { url: '/COMMAND_CENTER_MOBILE.html', name: 'Mobile HUD', icon: '📱' },
    walkthrough: { url: '/SITE_WALKTHROUGH_INTERACTIVE.html', name: 'Tour', icon: '🗺️' },
    platform: { url: '/platform.html', name: 'Builder', icon: '🏗️' },
    jarvis: { url: '/jarvis.html', name: 'Jarvis', icon: '🤖' }
};

class UniversalNavigation {
    constructor() {
        this.currentPage = this.detectCurrentPage();
        this.isAuthenticated = this.checkAuth();
        this.init();
    }

    detectCurrentPage() {
        const path = window.location.pathname;
        for (const [key, page] of Object.entries(PLATFORM_PAGES)) {
            if (path.includes(page.url.replace('/', ''))) {
                return key;
            }
        }
        return 'home';
    }

    checkAuth() {
        return localStorage.getItem('currentUser') !== null;
    }

    init() {
        // Auto-inject navigation UI when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.injectNavigation());
        } else {
            this.injectNavigation();
        }
    }

    injectNavigation() {
        // Create navigation bar
        const navBar = this.createNavigationBar();

        // Find insertion point (after body opening or before first element)
        if (document.body.firstChild) {
            document.body.insertBefore(navBar, document.body.firstChild);
        } else {
            document.body.appendChild(navBar);
        }

        // Inject styles
        this.injectStyles();
    }

    createNavigationBar() {
        const nav = document.createElement('div');
        nav.id = 'universal-nav';
        nav.className = 'universal-nav';

        // Logo section
        const logo = document.createElement('div');
        logo.className = 'nav-logo';
        logo.innerHTML = `
            <span class="logo-icon">🌀</span>
            <span class="logo-text">100X Platform</span>
        `;
        logo.onclick = () => this.navigate('workspace');

        // Navigation links
        const links = document.createElement('div');
        links.className = 'nav-links';

        // Filter pages based on auth status
        const visiblePages = this.isAuthenticated
            ? Object.entries(PLATFORM_PAGES).filter(([key]) => key !== 'login')
            : [['home', PLATFORM_PAGES.home], ['login', PLATFORM_PAGES.login], ['walkthrough', PLATFORM_PAGES.walkthrough]];

        visiblePages.forEach(([key, page]) => {
            const link = document.createElement('a');
            link.className = `nav-link ${this.currentPage === key ? 'active' : ''}`;
            link.href = page.url;
            link.innerHTML = `${page.icon} <span class="nav-text">${page.name}</span>`;
            links.appendChild(link);
        });

        // User section
        const userSection = document.createElement('div');
        userSection.className = 'nav-user';

        if (this.isAuthenticated) {
            const username = JSON.parse(localStorage.getItem('currentUser')).username;
            userSection.innerHTML = `
                <span class="user-name">👤 ${username}</span>
                <button class="logout-btn" onclick="universalNav.logout()">Logout</button>
            `;
        } else {
            userSection.innerHTML = `
                <a href="/simple-gate.html" class="login-btn">Login</a>
            `;
        }

        // Assemble navigation bar
        nav.appendChild(logo);
        nav.appendChild(links);
        nav.appendChild(userSection);

        return nav;
    }

    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .universal-nav {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                height: 60px;
                background: linear-gradient(135deg, rgba(0,0,0,0.95), rgba(0,50,80,0.95));
                backdrop-filter: blur(10px);
                border-bottom: 2px solid rgba(0,255,255,0.3);
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 20px;
                z-index: 999999;
                box-shadow: 0 4px 20px rgba(0,255,255,0.2);
                font-family: 'Segoe UI', system-ui, sans-serif;
            }

            /* Ensure body has top padding to avoid overlap */
            body {
                padding-top: 60px !important;
            }

            .nav-logo {
                display: flex;
                align-items: center;
                gap: 10px;
                cursor: pointer;
                transition: transform 0.2s;
            }

            .nav-logo:hover {
                transform: scale(1.05);
            }

            .logo-icon {
                font-size: 24px;
                animation: spin 3s linear infinite;
            }

            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }

            .logo-text {
                font-size: 18px;
                font-weight: bold;
                background: linear-gradient(90deg, #00ffff, #00ff88);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .nav-links {
                display: flex;
                gap: 5px;
                align-items: center;
                flex: 1;
                justify-content: center;
            }

            .nav-link {
                padding: 8px 15px;
                border-radius: 8px;
                text-decoration: none;
                color: rgba(255,255,255,0.8);
                display: flex;
                align-items: center;
                gap: 5px;
                transition: all 0.3s;
                font-size: 14px;
                border: 1px solid transparent;
            }

            .nav-link:hover {
                background: rgba(0,255,255,0.1);
                color: #00ffff;
                border-color: rgba(0,255,255,0.3);
                transform: translateY(-2px);
            }

            .nav-link.active {
                background: rgba(0,255,255,0.2);
                color: #00ffff;
                border-color: rgba(0,255,255,0.5);
                box-shadow: 0 0 10px rgba(0,255,255,0.3);
            }

            .nav-user {
                display: flex;
                align-items: center;
                gap: 15px;
            }

            .user-name {
                color: #00ff88;
                font-weight: 500;
            }

            .logout-btn, .login-btn {
                padding: 8px 16px;
                border-radius: 6px;
                border: 1px solid rgba(0,255,255,0.5);
                background: rgba(0,255,255,0.1);
                color: #00ffff;
                cursor: pointer;
                transition: all 0.3s;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
            }

            .logout-btn:hover, .login-btn:hover {
                background: rgba(0,255,255,0.2);
                box-shadow: 0 0 15px rgba(0,255,255,0.4);
                transform: translateY(-2px);
            }

            /* Mobile responsive */
            @media (max-width: 768px) {
                .universal-nav {
                    padding: 0 10px;
                }

                .nav-text {
                    display: none;
                }

                .nav-link {
                    padding: 8px 10px;
                    font-size: 18px;
                }

                .logo-text {
                    display: none;
                }

                .nav-links {
                    gap: 2px;
                }
            }
        `;
        document.head.appendChild(style);
    }

    navigate(pageKey) {
        if (PLATFORM_PAGES[pageKey]) {
            window.location.href = PLATFORM_PAGES[pageKey].url;
        }
    }

    logout() {
        localStorage.removeItem('currentUser');
        window.location.href = '/simple-gate.html';
    }
}

// Auto-initialize on script load
let universalNav;
if (typeof window !== 'undefined') {
    universalNav = new UniversalNavigation();
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UniversalNavigation;
}
