/**
 * 🎮 CONSCIOUSNESS OS MULTITASKING SYSTEM
 * iOS-style app switcher with background state management
 *
 * Usage: Include this script on any page to enable multitasking
 * Keyboard: Ctrl+Tab to open app switcher
 * Gesture: Swipe up from bottom (mobile)
 */

class ConsciousnessMultitasking {
    constructor() {
        this.apps = [];
        this.currentApp = null;
        this.switcher = null;
        this.init();
    }

    init() {
        // Load open apps from localStorage
        this.loadOpenApps();

        // Create app switcher UI
        this.createSwitcherUI();

        // Register current page as open app
        this.registerCurrentApp();

        // Set up keyboard shortcuts
        this.setupKeyboardShortcuts();

        // Set up mobile gesture
        this.setupMobileGesture();

        // Periodic state save
        setInterval(() => this.saveState(), 5000);
    }

    loadOpenApps() {
        const stored = localStorage.getItem('consciousnessOpenApps');
        this.apps = stored ? JSON.parse(stored) : [];
    }

    registerCurrentApp() {
        const appName = document.title || 'Consciousness OS';
        const appUrl = window.location.href;
        const appIcon = this.getAppIcon(appName);

        // Check if app is already registered
        const existing = this.apps.find(app => app.url === appUrl);
        if (existing) {
            existing.lastActive = Date.now();
            this.currentApp = existing;
        } else {
            // Register new app
            const newApp = {
                id: 'app_' + Date.now(),
                name: appName,
                url: appUrl,
                icon: appIcon,
                lastActive: Date.now(),
                state: {}
            };
            this.apps.push(newApp);
            this.currentApp = newApp;
        }

        this.saveState();
    }

    getAppIcon(appName) {
        const iconMap = {
            'Music': '🎵',
            'JARVIS': '🎮',
            'Settings': '⚙️',
            'Trinity': '🌀',
            'Manifestochart': '📊',
            'App Store': '📱',
            'Voice Control': '🎤',
            'Pattern': '🧠'
        };

        for (let key in iconMap) {
            if (appName.includes(key)) {
                return iconMap[key];
            }
        }
        return '🌐';
    }

    createSwitcherUI() {
        // Create overlay
        const overlay = document.createElement('div');
        overlay.id = 'consciousness-switcher-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            z-index: 99999;
            display: none;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;

        // Create switcher container
        const switcher = document.createElement('div');
        switcher.id = 'consciousness-switcher';
        switcher.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 90%;
            max-width: 1000px;
            max-height: 70vh;
            overflow-y: auto;
            z-index: 100000;
            display: none;
        `;

        // Add header
        const header = document.createElement('div');
        header.style.cssText = `
            text-align: center;
            color: white;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 30px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        `;
        header.textContent = '📱 Open Apps';
        switcher.appendChild(header);

        // Add apps grid
        const grid = document.createElement('div');
        grid.id = 'consciousness-switcher-grid';
        grid.style.cssText = `
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            padding: 20px;
        `;
        switcher.appendChild(grid);

        // Add close instruction
        const instruction = document.createElement('div');
        instruction.style.cssText = `
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
            margin-top: 30px;
            font-size: 0.9em;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        `;
        instruction.textContent = 'Press Esc or click outside to close';
        switcher.appendChild(instruction);

        overlay.appendChild(switcher);
        document.body.appendChild(overlay);

        // Click outside to close
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.closeSwitcher();
            }
        });

        this.switcher = switcher;
        this.overlay = overlay;
    }

    renderApps() {
        const grid = document.getElementById('consciousness-switcher-grid');
        if (!grid) return;

        grid.innerHTML = '';

        // Sort by last active
        const sortedApps = [...this.apps].sort((a, b) => b.lastActive - a.lastActive);

        sortedApps.forEach(app => {
            const card = document.createElement('div');
            card.style.cssText = `
                background: white;
                border-radius: 15px;
                padding: 20px;
                cursor: pointer;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            `;

            card.innerHTML = `
                <div style="
                    font-size: 3em;
                    text-align: center;
                    margin-bottom: 15px;
                ">${app.icon}</div>
                <div style="
                    font-size: 1.1em;
                    font-weight: 600;
                    text-align: center;
                    color: #2d3748;
                    margin-bottom: 10px;
                ">${app.name}</div>
                <div style="
                    text-align: center;
                    font-size: 0.8em;
                    color: #718096;
                ">${this.timeAgo(app.lastActive)}</div>
                <button style="
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: #ef4444;
                    color: white;
                    border: none;
                    border-radius: 50%;
                    width: 30px;
                    height: 30px;
                    cursor: pointer;
                    font-size: 1.2em;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                " onclick="event.stopPropagation(); consciousnessMultitasking.closeApp('${app.id}')">×</button>
            `;

            // Add hover effect
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'scale(1.05)';
                card.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.2)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'scale(1)';
                card.style.boxShadow = 'none';
            });

            // Switch to app on click
            card.addEventListener('click', () => {
                if (app.url !== window.location.href) {
                    window.location.href = app.url;
                } else {
                    this.closeSwitcher();
                }
            });

            grid.appendChild(card);
        });
    }

    timeAgo(timestamp) {
        const seconds = Math.floor((Date.now() - timestamp) / 1000);
        if (seconds < 60) return 'Just now';
        const minutes = Math.floor(seconds / 60);
        if (minutes < 60) return `${minutes}m ago`;
        const hours = Math.floor(minutes / 60);
        if (hours < 24) return `${hours}h ago`;
        const days = Math.floor(hours / 24);
        return `${days}d ago`;
    }

    openSwitcher() {
        this.renderApps();
        this.overlay.style.display = 'block';
        this.switcher.style.display = 'block';

        // Fade in
        setTimeout(() => {
            this.overlay.style.opacity = '1';
        }, 10);
    }

    closeSwitcher() {
        this.overlay.style.opacity = '0';
        setTimeout(() => {
            this.overlay.style.display = 'none';
            this.switcher.style.display = 'none';
        }, 300);
    }

    closeApp(appId) {
        this.apps = this.apps.filter(app => app.id !== appId);
        this.saveState();
        this.renderApps();
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Tab to open switcher
            if (e.ctrlKey && e.key === 'Tab') {
                e.preventDefault();
                this.openSwitcher();
            }

            // Esc to close switcher
            if (e.key === 'Escape') {
                this.closeSwitcher();
            }
        });
    }

    setupMobileGesture() {
        let touchStartY = 0;
        let touchEndY = 0;

        document.addEventListener('touchstart', (e) => {
            touchStartY = e.touches[0].clientY;
        });

        document.addEventListener('touchmove', (e) => {
            touchEndY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', () => {
            // Swipe up from bottom (150px from bottom)
            if (touchStartY > window.innerHeight - 150 && touchStartY - touchEndY > 100) {
                this.openSwitcher();
            }
        });
    }

    saveState() {
        // Remove apps older than 24 hours
        const oneDayAgo = Date.now() - (24 * 60 * 60 * 1000);
        this.apps = this.apps.filter(app => app.lastActive > oneDayAgo);

        // Save to localStorage
        localStorage.setItem('consciousnessOpenApps', JSON.stringify(this.apps));
    }

    // Public API for pages to save custom state
    saveAppState(state) {
        if (this.currentApp) {
            this.currentApp.state = state;
            this.saveState();
        }
    }

    getAppState() {
        return this.currentApp ? this.currentApp.state : {};
    }
}

// Initialize multitasking system
const consciousnessMultitasking = new ConsciousnessMultitasking();

// Export for use in pages
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ConsciousnessMultitasking;
}
