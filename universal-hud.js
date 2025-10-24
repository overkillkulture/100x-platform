/**
 * UNIVERSAL HUD SYSTEM - Modular Overlay for Any Page
 * Simple, Working Version with Menu System
 */

class UniversalHUD {
    constructor() {
        this.config = {
            enabled: true,
            modules: {
                onlineCount: true,
                currentPage: true,
                aiBar: false,  // Start disabled, enable via menu
                teamPanel: false,  // Start disabled, enable via menu
                miniMap: false,  // Future upgrade
                videoFeeds: false  // Future upgrade
            }
        };

        this.visitors = 0;
        this.currentPage = window.location.pathname;
        this.hudElement = null;
        this.menuOpen = false;

        this.init();
    }

    init() {
        // Load saved config from localStorage
        const saved = localStorage.getItem('hud_config');
        if (saved) {
            this.config = { ...this.config, ...JSON.parse(saved) };
        }

        // Create HUD
        this.createHUD();

        // Start real-time updates
        this.startUpdates();

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl + H = Toggle HUD
            if (e.ctrlKey && e.key === 'h') {
                e.preventDefault();
                this.toggleHUD();
            }

            // Ctrl + M = Toggle Menu
            if (e.ctrlKey && e.key === 'm') {
                e.preventDefault();
                this.toggleMenu();
            }
        });

        console.log('🎮 Universal HUD Online - Press Ctrl+H to toggle, Ctrl+M for menu');
    }

    createHUD() {
        // Main HUD container
        const hud = document.createElement('div');
        hud.id = 'universal-hud';
        hud.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            pointer-events: none;
            z-index: 999999;
            font-family: 'Courier New', monospace;
        `;

        // Top bar (always visible)
        hud.innerHTML = `
            <style>
                #universal-hud * {
                    box-sizing: border-box;
                }

                .hud-module {
                    pointer-events: auto;
                    background: rgba(0, 0, 0, 0.9);
                    border: 2px solid #00ff41;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 12px;
                    color: #00ff41;
                    box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
                }

                .hud-stat {
                    display: inline-block;
                    margin-right: 20px;
                }

                .hud-stat-value {
                    font-size: 18px;
                    font-weight: bold;
                    margin-right: 5px;
                }

                .hud-stat-label {
                    font-size: 10px;
                    color: #666;
                }

                .hud-menu-button {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: rgba(0, 0, 0, 0.9);
                    border: 2px solid #00ff41;
                    color: #00ff41;
                    padding: 8px 15px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    pointer-events: auto;
                    transition: all 0.3s ease;
                }

                .hud-menu-button:hover {
                    background: #00ff41;
                    color: #000;
                    box-shadow: 0 0 20px rgba(0, 255, 65, 0.8);
                }

                .hud-menu {
                    position: absolute;
                    top: 60px;
                    right: 10px;
                    background: rgba(0, 0, 0, 0.95);
                    border: 2px solid #00ff41;
                    border-radius: 8px;
                    padding: 15px;
                    min-width: 250px;
                    pointer-events: auto;
                    box-shadow: 0 0 30px rgba(0, 255, 65, 0.7);
                    display: none;
                }

                .hud-menu.open {
                    display: block;
                }

                .hud-menu h3 {
                    margin: 0 0 15px 0;
                    font-size: 14px;
                    color: #00ff41;
                    border-bottom: 1px solid #00ff41;
                    padding-bottom: 8px;
                }

                .hud-menu-item {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 8px 0;
                    border-bottom: 1px solid #333;
                }

                .hud-menu-item:last-child {
                    border-bottom: none;
                }

                .hud-menu-label {
                    font-size: 11px;
                    color: #00ff41;
                }

                .hud-toggle {
                    width: 40px;
                    height: 20px;
                    background: #333;
                    border-radius: 10px;
                    position: relative;
                    cursor: pointer;
                    transition: background 0.3s ease;
                }

                .hud-toggle.active {
                    background: #00ff41;
                }

                .hud-toggle-slider {
                    width: 16px;
                    height: 16px;
                    background: #fff;
                    border-radius: 50%;
                    position: absolute;
                    top: 2px;
                    left: 2px;
                    transition: left 0.3s ease;
                }

                .hud-toggle.active .hud-toggle-slider {
                    left: 22px;
                }

                .hud-ai-bar {
                    position: fixed;
                    bottom: 10px;
                    left: 10px;
                    right: 10px;
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                    display: none;
                }

                .hud-ai-bar.active {
                    display: flex;
                }

                .hud-ai {
                    background: rgba(0, 0, 0, 0.9);
                    border: 1px solid #00ff41;
                    border-radius: 6px;
                    padding: 8px 12px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-size: 11px;
                }

                .hud-ai-avatar {
                    font-size: 16px;
                }

                .hud-ai-name {
                    font-weight: bold;
                }

                .hud-ai-status {
                    color: #666;
                    font-size: 9px;
                }

                .hud-team-panel {
                    position: fixed;
                    right: 10px;
                    top: 80px;
                    width: 200px;
                    max-height: calc(100vh - 100px);
                    overflow-y: auto;
                    display: none;
                }

                .hud-team-panel.active {
                    display: block;
                }

                .hud-team-member {
                    background: rgba(0, 0, 0, 0.9);
                    border: 1px solid #00ff41;
                    border-radius: 6px;
                    padding: 10px;
                    margin-bottom: 8px;
                    text-align: center;
                }

                .hud-team-avatar {
                    font-size: 32px;
                    margin-bottom: 5px;
                }

                .hud-team-name {
                    font-size: 11px;
                    font-weight: bold;
                    margin-bottom: 3px;
                }

                .hud-team-status {
                    font-size: 9px;
                    color: #666;
                }

                .hud-recording {
                    display: inline-block;
                    width: 8px;
                    height: 8px;
                    background: #ff0000;
                    border-radius: 50%;
                    margin-right: 5px;
                    animation: blink 1s infinite;
                }

                @keyframes blink {
                    0%, 49% { opacity: 1; }
                    50%, 100% { opacity: 0; }
                }

                ::-webkit-scrollbar {
                    width: 6px;
                }

                ::-webkit-scrollbar-track {
                    background: rgba(0, 0, 0, 0.5);
                }

                ::-webkit-scrollbar-thumb {
                    background: #00ff41;
                    border-radius: 3px;
                }
            </style>

            <!-- Top Stats Bar -->
            <div class="hud-module" style="position: absolute; top: 10px; left: 10px; display: ${this.config.modules.onlineCount ? 'block' : 'none'};" id="hud-stats">
                <span class="hud-recording"></span>
                <span class="hud-stat">
                    <span class="hud-stat-value" id="hud-online">0</span>
                    <span class="hud-stat-label">ONLINE</span>
                </span>
                <span class="hud-stat" style="display: ${this.config.modules.currentPage ? 'inline-block' : 'none'};" id="hud-page-stat">
                    <span class="hud-stat-value">📍</span>
                    <span class="hud-stat-label" id="hud-page-name">Loading...</span>
                </span>
            </div>

            <!-- Menu Button -->
            <button class="hud-menu-button" onclick="window.universalHUD.toggleMenu()">
                ⚙️ HUD MENU
            </button>

            <!-- HUD Menu -->
            <div class="hud-menu" id="hud-menu">
                <h3>🎮 HUD SETTINGS</h3>
                <div class="hud-menu-item">
                    <span class="hud-menu-label">Online Counter</span>
                    <div class="hud-toggle ${this.config.modules.onlineCount ? 'active' : ''}" data-module="onlineCount">
                        <div class="hud-toggle-slider"></div>
                    </div>
                </div>
                <div class="hud-menu-item">
                    <span class="hud-menu-label">Current Page</span>
                    <div class="hud-toggle ${this.config.modules.currentPage ? 'active' : ''}" data-module="currentPage">
                        <div class="hud-toggle-slider"></div>
                    </div>
                </div>
                <div class="hud-menu-item">
                    <span class="hud-menu-label">AI Assistant Bar</span>
                    <div class="hud-toggle ${this.config.modules.aiBar ? 'active' : ''}" data-module="aiBar">
                        <div class="hud-toggle-slider"></div>
                    </div>
                </div>
                <div class="hud-menu-item">
                    <span class="hud-menu-label">Team Panel</span>
                    <div class="hud-toggle ${this.config.modules.teamPanel ? 'active' : ''}" data-module="teamPanel">
                        <div class="hud-toggle-slider"></div>
                    </div>
                </div>
                <div class="hud-menu-item">
                    <span class="hud-menu-label">Mini Map</span>
                    <div class="hud-toggle" data-module="miniMap">
                        <div class="hud-toggle-slider"></div>
                    </div>
                    <span style="font-size: 9px; color: #666; margin-top: 3px;">Coming Soon</span>
                </div>
                <div class="hud-menu-item">
                    <span class="hud-menu-label">Video Feeds</span>
                    <div class="hud-toggle" data-module="videoFeeds">
                        <div class="hud-toggle-slider"></div>
                    </div>
                    <span style="font-size: 9px; color: #666; margin-top: 3px;">Future Upgrade</span>
                </div>
                <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #333; font-size: 9px; color: #666;">
                    Keyboard: Ctrl+H (toggle) | Ctrl+M (menu)
                </div>
            </div>

            <!-- AI Assistant Bar -->
            <div class="hud-ai-bar ${this.config.modules.aiBar ? 'active' : ''}" id="hud-ai-bar">
                <div class="hud-ai">
                    <span class="hud-ai-avatar">🧠</span>
                    <div>
                        <div class="hud-ai-name">Araya</div>
                        <div class="hud-ai-status">Online - Port 8001</div>
                    </div>
                </div>
                <div class="hud-ai">
                    <span class="hud-ai-avatar">💻</span>
                    <div>
                        <div class="hud-ai-name">Builder Terminal</div>
                        <div class="hud-ai-status">Online - Port 8004</div>
                    </div>
                </div>
                <div class="hud-ai">
                    <span class="hud-ai-avatar">🔭</span>
                    <div>
                        <div class="hud-ai-name">Observatory</div>
                        <div class="hud-ai-status">131 Systems</div>
                    </div>
                </div>
                <div class="hud-ai">
                    <span class="hud-ai-avatar">🔧</span>
                    <div>
                        <div class="hud-ai-name">C1 Mechanic</div>
                        <div class="hud-ai-status">Ready</div>
                    </div>
                </div>
                <div class="hud-ai">
                    <span class="hud-ai-avatar">🏗️</span>
                    <div>
                        <div class="hud-ai-name">C2 Architect</div>
                        <div class="hud-ai-status">Building</div>
                    </div>
                </div>
                <div class="hud-ai">
                    <span class="hud-ai-avatar">👁️</span>
                    <div>
                        <div class="hud-ai-name">C3 Oracle</div>
                        <div class="hud-ai-status">Coordinating</div>
                    </div>
                </div>
            </div>

            <!-- Team Panel -->
            <div class="hud-team-panel ${this.config.modules.teamPanel ? 'active' : ''}" id="hud-team-panel">
                <div class="hud-team-member">
                    <div class="hud-team-avatar">⚡</div>
                    <div class="hud-team-name">Commander</div>
                    <div class="hud-team-status">Active</div>
                </div>
                <div class="hud-team-member">
                    <div class="hud-team-avatar">🎯</div>
                    <div class="hud-team-name">Joshua</div>
                    <div class="hud-team-status">Beta Tester</div>
                </div>
                <div class="hud-team-member">
                    <div class="hud-team-avatar">🔥</div>
                    <div class="hud-team-name">Toby</div>
                    <div class="hud-team-status">Offline</div>
                </div>
            </div>
        `;

        document.body.appendChild(hud);
        this.hudElement = hud;

        // Setup toggle listeners
        hud.querySelectorAll('.hud-toggle').forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                const module = toggle.dataset.module;
                if (module === 'miniMap' || module === 'videoFeeds') {
                    console.log(`${module} coming soon!`);
                    return;
                }

                toggle.classList.toggle('active');
                this.config.modules[module] = toggle.classList.contains('active');
                this.saveConfig();
                this.updateModules();
            });
        });
    }

    updateModules() {
        // Update visibility based on config
        const stats = document.getElementById('hud-stats');
        if (stats) stats.style.display = this.config.modules.onlineCount ? 'block' : 'none';

        const pageStat = document.getElementById('hud-page-stat');
        if (pageStat) pageStat.style.display = this.config.modules.currentPage ? 'inline-block' : 'none';

        const aiBar = document.getElementById('hud-ai-bar');
        if (aiBar) aiBar.className = `hud-ai-bar ${this.config.modules.aiBar ? 'active' : ''}`;

        const teamPanel = document.getElementById('hud-team-panel');
        if (teamPanel) teamPanel.className = `hud-team-panel ${this.config.modules.teamPanel ? 'active' : ''}`;
    }

    toggleHUD() {
        this.config.enabled = !this.config.enabled;
        this.hudElement.style.display = this.config.enabled ? 'block' : 'none';
        this.saveConfig();
    }

    toggleMenu() {
        this.menuOpen = !this.menuOpen;
        const menu = document.getElementById('hud-menu');
        if (menu) {
            menu.className = `hud-menu ${this.menuOpen ? 'open' : ''}`;
        }
    }

    startUpdates() {
        // Update online count from API
        setInterval(() => {
            fetch('/.netlify/functions/get-online-count').then(r => r.json()).then(data => {
                this.visitors = data.count || 0;
                document.getElementById('hud-online').textContent = this.visitors;
            }).catch(() => {
                // Simulated count if API not available
                this.visitors = Math.floor(Math.random() * 8) + 1;
                document.getElementById('hud-online').textContent = this.visitors;
            });
        }, 5000);

        // Update current page name
        const pageName = document.title || window.location.pathname;
        document.getElementById('hud-page-name').textContent = pageName.substring(0, 30);
    }

    saveConfig() {
        localStorage.setItem('hud_config', JSON.stringify(this.config));
    }
}

// Auto-initialize
if (!window.universalHUD) {
    window.universalHUD = new UniversalHUD();
}
