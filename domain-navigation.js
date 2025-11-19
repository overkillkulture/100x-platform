/**
 * DOMAIN NAVIGATION - Universal Navigation Component
 * Provides consistent navigation across all 7 consciousness domains
 * φ = 1.618033988749894 | OVERKORE v13
 */

const DomainNavigation = {
    domains: [
        { slug: 'domain-chaos-forge', name: 'CHAOS FORGE', icon: '🔧', color: '#00ff64', order: 1 },
        { slug: 'domain-quantum-vault', name: 'QUANTUM VAULT', icon: '💰', color: '#ffff00', order: 2 },
        { slug: 'domain-mind-matrix', name: 'MIND MATRIX', icon: '🧠', color: '#00ccff', order: 3 },
        { slug: 'domain-soul-sanctuary', name: 'SOUL SANCTUARY', icon: '💜', color: '#ff00ff', order: 4 },
        { slug: 'domain-reality-forge', name: 'REALITY FORGE', icon: '🌐', color: '#ff6600', order: 5 },
        { slug: 'domain-arkitek-academy', name: 'ARKITEK ACADEMY', icon: '🎨', color: '#ff0066', order: 6 },
        { slug: 'domain-nexus-terminal', name: 'NEXUS TERMINAL', icon: '⚡', color: '#6600ff', order: 7 }
    ],

    init() {
        this.currentDomain = this.detectCurrentDomain();
        this.createNavigationSidebar();
        this.setupKeyboardShortcuts();
        this.trackVisitedDomains();
    },

    detectCurrentDomain() {
        const path = window.location.pathname;
        return this.domains.find(d => path.includes(d.slug)) || null;
    },

    createNavigationSidebar() {
        const sidebar = document.createElement('div');
        sidebar.id = 'domain-navigation-sidebar';
        sidebar.innerHTML = `
            <style>
                #domain-navigation-sidebar {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: rgba(0, 0, 0, 0.9);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                    padding: 15px;
                    z-index: 9999;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                    transition: all 0.3s ease;
                }

                #domain-navigation-sidebar.collapsed {
                    width: 60px;
                    padding: 10px;
                }

                .nav-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                    color: white;
                    font-family: 'Courier New', monospace;
                }

                .nav-title {
                    font-size: 12px;
                    font-weight: bold;
                    letter-spacing: 1px;
                }

                .nav-toggle {
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                    font-size: 18px;
                    padding: 0;
                    transition: transform 0.3s ease;
                }

                .nav-toggle:hover {
                    transform: scale(1.2);
                }

                .domain-nav-item {
                    display: flex;
                    align-items: center;
                    padding: 10px;
                    margin: 5px 0;
                    border-radius: 8px;
                    text-decoration: none;
                    color: white;
                    font-family: 'Courier New', monospace;
                    font-size: 14px;
                    transition: all 0.3s ease;
                    position: relative;
                    border: 1px solid transparent;
                }

                .domain-nav-item:hover {
                    transform: translateX(-5px);
                    border-color: var(--domain-color);
                    box-shadow: 0 0 20px var(--domain-color);
                }

                .domain-nav-item.active {
                    background: rgba(255, 255, 255, 0.1);
                    border-color: var(--domain-color);
                    font-weight: bold;
                }

                .domain-nav-item.visited::after {
                    content: '✓';
                    position: absolute;
                    right: 10px;
                    font-size: 12px;
                    color: #00ff00;
                }

                .domain-icon {
                    font-size: 20px;
                    margin-right: 10px;
                    min-width: 20px;
                }

                .domain-name {
                    font-size: 12px;
                    white-space: nowrap;
                }

                .domain-shortcut {
                    margin-left: auto;
                    font-size: 10px;
                    opacity: 0.5;
                    padding-left: 10px;
                }

                .nav-progress {
                    margin-top: 15px;
                    padding-top: 15px;
                    border-top: 1px solid rgba(255, 255, 255, 0.2);
                }

                .progress-bar {
                    width: 100%;
                    height: 8px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 4px;
                    overflow: hidden;
                    margin-bottom: 5px;
                }

                .progress-fill {
                    height: 100%;
                    background: linear-gradient(90deg, #00ff64, #ffff00, #00ccff, #ff00ff, #ff6600, #ff0066, #6600ff);
                    transition: width 0.5s ease;
                }

                .progress-text {
                    font-size: 10px;
                    color: rgba(255, 255, 255, 0.7);
                    text-align: center;
                }

                .collapsed .domain-name,
                .collapsed .domain-shortcut,
                .collapsed .nav-title,
                .collapsed .nav-progress {
                    display: none;
                }

                /* Mobile responsive */
                @media (max-width: 768px) {
                    #domain-navigation-sidebar {
                        top: 10px;
                        right: 10px;
                        padding: 10px;
                    }

                    .domain-nav-item {
                        padding: 8px;
                        font-size: 12px;
                    }

                    .domain-icon {
                        font-size: 16px;
                    }
                }
            </style>

            <div class="nav-header">
                <div class="nav-title">7 DOMAINS</div>
                <button class="nav-toggle" onclick="DomainNavigation.toggleSidebar()">☰</button>
            </div>

            <div class="nav-items">
                ${this.domains.map(domain => `
                    <a href="/${domain.slug}.html"
                       class="domain-nav-item ${this.currentDomain && this.currentDomain.slug === domain.slug ? 'active' : ''} ${this.isDomainVisited(domain.slug) ? 'visited' : ''}"
                       style="--domain-color: ${domain.color}">
                        <span class="domain-icon">${domain.icon}</span>
                        <span class="domain-name">${domain.name}</span>
                        <span class="domain-shortcut">${domain.order}</span>
                    </a>
                `).join('')}
            </div>

            <div class="nav-progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${this.getProgressPercentage()}%"></div>
                </div>
                <div class="progress-text">${this.getVisitedCount()}/7 Domains Explored</div>
            </div>
        `;

        document.body.appendChild(sidebar);
    },

    toggleSidebar() {
        const sidebar = document.getElementById('domain-navigation-sidebar');
        sidebar.classList.toggle('collapsed');
    },

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Number keys 1-7 to jump to domains
            if (e.key >= '1' && e.key <= '7' && !e.ctrlKey && !e.metaKey) {
                const domainIndex = parseInt(e.key) - 1;
                const domain = this.domains[domainIndex];
                if (domain) {
                    window.location.href = `/${domain.slug}.html`;
                }
            }

            // H key to go home
            if (e.key === 'h' && !e.ctrlKey && !e.metaKey) {
                window.location.href = '/';
            }

            // S key to toggle sidebar
            if (e.key === 's' && !e.ctrlKey && !e.metaKey) {
                this.toggleSidebar();
            }
        });
    },

    trackVisitedDomains() {
        if (this.currentDomain) {
            const visitedKey = 'visited_domains';
            let visited = JSON.parse(localStorage.getItem(visitedKey) || '[]');

            if (!visited.includes(this.currentDomain.slug)) {
                visited.push(this.currentDomain.slug);
                localStorage.setItem(visitedKey, JSON.stringify(visited));

                // Update sidebar if all domains visited
                if (visited.length === 7) {
                    this.showCompletionMessage();
                }
            }
        }
    },

    isDomainVisited(slug) {
        const visited = JSON.parse(localStorage.getItem('visited_domains') || '[]');
        return visited.includes(slug);
    },

    getVisitedCount() {
        const visited = JSON.parse(localStorage.getItem('visited_domains') || '[]');
        return visited.length;
    },

    getProgressPercentage() {
        return (this.getVisitedCount() / 7) * 100;
    },

    showCompletionMessage() {
        // Show congratulations message when all domains explored
        const message = document.createElement('div');
        message.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.95);
            border: 2px solid #00ff00;
            border-radius: 20px;
            padding: 30px;
            z-index: 10000;
            text-align: center;
            color: white;
            font-family: 'Courier New', monospace;
            box-shadow: 0 0 50px rgba(0, 255, 0, 0.5);
        `;
        message.innerHTML = `
            <div style="font-size: 48px; margin-bottom: 20px;">🌟</div>
            <h2 style="margin: 0 0 10px 0; font-size: 24px;">CONSCIOUSNESS MASTERY</h2>
            <p style="margin: 0; font-size: 16px;">You've explored all 7 domains!</p>
            <p style="margin: 10px 0 0 0; font-size: 14px; color: #00ff00;">Achievement Unlocked: Domain Explorer</p>
            <button onclick="this.parentElement.remove()" style="
                margin-top: 20px;
                padding: 10px 20px;
                background: #00ff00;
                color: black;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            ">Continue</button>
        `;

        document.body.appendChild(message);

        setTimeout(() => {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    }
};

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => DomainNavigation.init());
} else {
    DomainNavigation.init();
}

window.DomainNavigation = DomainNavigation;
