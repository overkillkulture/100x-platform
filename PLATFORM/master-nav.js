/**
 * MASTER NAVIGATION SYSTEM v1.0
 * Universal navigation that follows users across all platform pages
 * GTA-style menu system with breadcrumbs and quick access
 */

class MasterNavigation {
    constructor() {
        this.currentPath = window.location.pathname;
        this.currentPage = this.getCurrentPageInfo();
        this.userData = null;
        this.init();
    }

    async init() {
        // Load user data
        await this.loadUserData();

        // Inject navigation HTML
        this.injectNavigationHTML();

        // Set up event listeners
        this.setupEventListeners();

        // Update breadcrumbs
        this.updateBreadcrumbs();

        // Highlight current page
        this.highlightCurrentPage();
    }

    async loadUserData() {
        try {
            const authToken = localStorage.getItem('auth_token');
            if (!authToken) return null;

            const response = await fetch('http://localhost:3001/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.userData = data.user;
            }
        } catch (error) {
            console.error('Nav: Error loading user data:', error);
        }
    }

    getCurrentPageInfo() {
        const pages = {
            // Main Dashboard & Entry
            'index.html': { name: 'Home', icon: '🏠', category: 'Main' },
            'user-dashboard.html': { name: 'Dashboard', icon: '🏠', category: 'Main' },
            'dashboard.html': { name: 'Dashboard Alt', icon: '📊', category: 'Main' },
            'welcome.html': { name: 'Welcome', icon: '👋', category: 'Main' },
            'welcome-flow.html': { name: 'Welcome Flow', icon: '🌊', category: 'Main' },
            'onboarding-welcome.html': { name: 'Onboarding', icon: '🚀', category: 'Main' },
            'workspace.html': { name: 'Workspace', icon: '🛠️', category: 'Main' },
            'for-the-builders.html': { name: 'For Builders', icon: '👷', category: 'Main' },
            'mission-control-center.html': { name: 'Mission Control', icon: '🎯', category: 'Main' },

            // Authentication
            'login.html': { name: 'Login', icon: '🔑', category: 'Auth' },
            'register.html': { name: 'Register', icon: '📝', category: 'Auth' },
            'settings-panel.html': { name: 'Settings', icon: '⚙️', category: 'Auth' },

            // KORPAKs
            'korpak-wizard.html': { name: 'KORPAK Wizard', icon: '🧙', category: 'KORPAKs' },
            'korpak-detail.html': { name: 'KORPAK Details', icon: '📦', category: 'KORPAKs' },
            'AMELIA_JOY_KIT_STORE.html': { name: 'Amelia Joy Kit', icon: '😊', category: 'KORPAKs' },
            'KENNEDI_OBSERVER_KIT_STORE.html': { name: 'Kennedi Observer Kit', icon: '👁️', category: 'KORPAKs' },

            // Modules & Tools
            'module-library.html': { name: 'Module Library', icon: '🧩', category: 'Modules' },
            'MODULE_TEMPLATE.html': { name: 'Module Template', icon: '📋', category: 'Modules' },
            'module-pattern-explorer.html': { name: 'Pattern Explorer', icon: '🔍', category: 'Modules' },
            'cheat-codes.html': { name: 'Cheat Codes', icon: '🎮', category: 'Modules' },
            'todo-master.html': { name: 'TODO Master', icon: '✓', category: 'Modules' },
            'kaizen-builder-board.html': { name: 'Kaizen Board', icon: '📋', category: 'Modules' },
            'master-kanban-board.html': { name: 'Master Kanban', icon: '📊', category: 'Modules' },
            'master-kanban-music.html': { name: 'Kanban Music', icon: '🎵', category: 'Modules' },
            'invention-manifestation.html': { name: 'Invention Manifestation', icon: '💡', category: 'Modules' },
            'patent-manager.html': { name: 'Patent Manager', icon: '📜', category: 'Modules' },
            'domino-cascade-organizer.html': { name: 'Domino Organizer', icon: '🎯', category: 'Modules' },
            'software-blueprinter.html': { name: 'Software Blueprinter', icon: '🏗️', category: 'Modules' },
            'life-business-plan.html': { name: 'Life Business Plan', icon: '📈', category: 'Modules' },
            'corporate-bloat-tracker.html': { name: 'Bloat Tracker', icon: '📉', category: 'Modules' },

            // Trinity AI & Araya
            'philosopher-ai-connected.html': { name: 'Philosopher AI', icon: '🤖', category: 'Trinity' },
            'philosopher-ai.html': { name: 'Philosopher AI Alt', icon: '🧙', category: 'Trinity' },
            'trinity-ai-interface.html': { name: 'Trinity Interface', icon: '🔺', category: 'Trinity' },
            'trinity-chat.html': { name: 'Trinity Chat', icon: '💬', category: 'Trinity' },
            'brain-council.html': { name: 'Brain Council', icon: '🧠', category: 'Trinity' },
            'emergency-ai-chat.html': { name: 'Emergency AI', icon: '🚨', category: 'Trinity' },
            'araya-chat.html': { name: 'Araya Chat', icon: '🤖', category: 'Trinity' },
            'aria-3d-avatar.html': { name: 'Aria 3D Avatar', icon: '👤', category: 'Trinity' },
            'aria-3d-futuristic.html': { name: 'Aria Futuristic', icon: '✨', category: 'Trinity' },
            'aria-avatar-guide.html': { name: 'Aria Guide', icon: '🧭', category: 'Trinity' },
            'aria-simple-fallback.html': { name: 'Aria Fallback', icon: '🔄', category: 'Trinity' },
            'ai-guided-tour.html': { name: 'AI Guided Tour', icon: '🎫', category: 'Trinity' },
            'ai-native-blueprint.html': { name: 'AI Native Blueprint', icon: '🏗️', category: 'Trinity' },

            // Consciousness Tools
            '3-min-boost.html': { name: '3-Min Boost', icon: '⚡', category: 'Consciousness' },
            'consciousness-boost-dashboard.html': { name: 'Consciousness Boost', icon: '⚡', category: 'Consciousness' },
            'consciousness-speed-test.html': { name: 'Speed Test', icon: '⏱️', category: 'Consciousness' },
            'consciousness-workspace-3d.html': { name: 'Workspace 3D', icon: '🌐', category: 'Consciousness' },
            'consciousness-network-visualization.html': { name: 'Network Viz', icon: '🕸️', category: 'Consciousness' },
            'consciousness-profile-dump.html': { name: 'Profile Dump', icon: '📊', category: 'Consciousness' },
            'computer-consciousness.html': { name: 'Computer Consciousness', icon: '💻', category: 'Consciousness' },
            'pattern-recognition-quiz.html': { name: 'Pattern Quiz', icon: '🧩', category: 'Consciousness' },
            'quantum-pattern-filter.html': { name: 'Quantum Filter', icon: '🌀', category: 'Consciousness' },
            'destroyer-defense.html': { name: 'Destroyer Defense', icon: '🛡️', category: 'Consciousness' },
            'destroyer-inverse-optimization.html': { name: 'Inverse Optimization', icon: '🔄', category: 'Consciousness' },

            // Character & Assessment
            'unified-character-assessment.html': { name: 'Character Assessment', icon: '🎯', category: 'Assessment' },
            'character-trait-analysis.html': { name: 'Trait Analysis', icon: '📊', category: 'Assessment' },
            'mission-archetype-module.html': { name: 'Mission Archetype', icon: '🎭', category: 'Assessment' },
            'communication-patterns.html': { name: 'Communication Patterns', icon: '💬', category: 'Assessment' },

            // Business Tools
            'business-phase-clock.html': { name: 'Business Phase Clock', icon: '⏰', category: 'Business' },
            'truth-coin.html': { name: 'Truth Coin', icon: '🪙', category: 'Business' },
            'open-source-decision-module.html': { name: 'Open Source Decision', icon: '🌐', category: 'Business' },
            'case-humor-music-system.html': { name: 'Case Humor Music', icon: '🎭', category: 'Business' },

            // Store
            'store.html': { name: 'Store', icon: '🛒', category: 'Store' },
            'app-store.html': { name: 'App Store', icon: '📱', category: 'Store' },
            'store-products.html': { name: 'Products', icon: '📦', category: 'Store' },
            'store-cart.html': { name: 'Cart', icon: '🛍️', category: 'Store' },
            'store-campaigns.html': { name: 'Campaigns', icon: '📢', category: 'Store' },
            'store-investments.html': { name: 'Investments', icon: '💰', category: 'Store' },
            'store-success.html': { name: 'Purchase Success', icon: '✅', category: 'Store' },

            // Fun & Engagement
            'arcade-hub.html': { name: 'Arcade Hub', icon: '🎮', category: 'Arcade' },
            'social-hub.html': { name: 'Social Hub', icon: '🌐', category: 'Arcade' },
            'social-domain.html': { name: 'Social Domain', icon: '👥', category: 'Arcade' },
            'trinity-puzzle.html': { name: 'Trinity Puzzle', icon: '🧩', category: 'Arcade' },
            'time-machine.html': { name: 'Time Machine', icon: '⏰', category: 'Arcade' },
            'music-player.html': { name: 'Music Player', icon: '🎵', category: 'Arcade' },
            'music-player-simple.html': { name: 'Simple Music Player', icon: '🎶', category: 'Arcade' },
            'carnival-homepage.html': { name: 'Carnival', icon: '🎪', category: 'Arcade' },
            'carnival-homepage-v2.html': { name: 'Carnival V2', icon: '🎪', category: 'Arcade' },
            'poker-table.html': { name: 'Poker Table', icon: '🃏', category: 'Arcade' },

            // Analytics & Monitoring
            'analytics-dashboard.html': { name: 'Analytics', icon: '📊', category: 'Analytics' },
            'analytics-test-data-generator.html': { name: 'Test Data Generator', icon: '🧪', category: 'Analytics' },
            'platform-city-map.html': { name: 'Platform Map', icon: '🗺️', category: 'Analytics' },
            'meta-map.html': { name: 'Meta Map', icon: '🗺️', category: 'Analytics' },
            'ecosystem-map.html': { name: 'Ecosystem Map', icon: '🌳', category: 'Analytics' },
            'roadmap.html': { name: 'Roadmap', icon: '🛣️', category: 'Analytics' },
            'manifestochart-timeline.html': { name: 'Timeline', icon: '⏱️', category: 'Analytics' },
            'builder-xp-demo.html': { name: 'Builder XP', icon: '⭐', category: 'Analytics' },
            'sensor-integration-dashboard.html': { name: 'Sensor Integration', icon: '🛰️', category: 'Analytics' },

            // Developer Tools
            'debug-terminal.html': { name: 'Debug Terminal', icon: '⚡', category: 'Developer' },
            'debug-console.html': { name: 'Debug Console', icon: '🖥️', category: 'Developer' },
            'mobile-debug.html': { name: 'Mobile Debug', icon: '📱', category: 'Developer' },
            'intelligent-terminal.html': { name: 'AI Terminal', icon: '🤖', category: 'Developer' },
            'terminal.html': { name: 'Terminal', icon: '💻', category: 'Developer' },
            'builder-workshop.html': { name: 'Builder Workshop', icon: '🔧', category: 'Developer' },
            'clear-test-data.html': { name: 'Clear Test Data', icon: '🗑️', category: 'Developer' },

            // Voice & Communication
            'voice-control.html': { name: 'Voice Control', icon: '🎤', category: 'Voice' },
            'voice-case-compiler.html': { name: 'Voice Case Compiler', icon: '📝', category: 'Voice' },

            // Support & Help
            'visual-language-legend.html': { name: 'Visual Language Legend', icon: '🎨', category: 'Support' },
            'emoji-legend.html': { name: 'Emoji Legend', icon: '😀', category: 'Support' },
            'help.html': { name: 'Help', icon: '❓', category: 'Support' },
            'get-help.html': { name: 'Get Help', icon: '🆘', category: 'Support' },
            'bug-report-public.html': { name: 'Bug Reports', icon: '🐛', category: 'Support' },
            'debugger-leaderboard.html': { name: 'Debugger Leaderboard', icon: '🏆', category: 'Support' },
            'community-activity.html': { name: 'Community Activity', icon: '👥', category: 'Support' },
            'privacy-policy.html': { name: 'Privacy Policy', icon: '🔒', category: 'Support' },

            // Showcases
            'showcase-hub.html': { name: 'Showcase Hub', icon: '✨', category: 'Showcases' },
            'showcase-landing.html': { name: 'Showcase Landing', icon: '🎯', category: 'Showcases' },
            'trinity-cockpit.html': { name: 'Trinity Cockpit', icon: '🎛️', category: 'Showcases' },
            'meritocracy-dashboard.html': { name: 'Meritocracy Dashboard', icon: '⚖️', category: 'Showcases' },
            'character-matrix.html': { name: 'Character Matrix', icon: '🧬', category: 'Showcases' },
            'arg-assembly.html': { name: 'ARG Assembly', icon: '🎭', category: 'Showcases' },
            'ascension-explained.html': { name: 'Ascension Explained', icon: '⬆️', category: 'Showcases' },
            'universal-hud-system.html': { name: 'Universal HUD', icon: '📺', category: 'Showcases' },

            // 7 Domains
            'domain-framework.html': { name: 'Domain Framework', icon: '🏗️', category: 'Domains' },
            'seven-domains-navigator.html': { name: 'Seven Domains Nav', icon: '🧭', category: 'Domains' },
            'crypto-domain.html': { name: 'Crypto Domain', icon: '₿', category: 'Domains' },
            'education-domain.html': { name: 'Education Domain', icon: '🎓', category: 'Domains' },
            'games-domain.html': { name: 'Games Domain', icon: '🎯', category: 'Domains' },
            'health-domain.html': { name: 'Health Domain', icon: '🏥', category: 'Domains' },
            'housing-domain.html': { name: 'Housing Domain', icon: '🏡', category: 'Domains' },
            'manufacturing-domain.html': { name: 'Manufacturing Domain', icon: '🏭', category: 'Domains' },
            'music-domain.html': { name: 'Music Domain', icon: '🎵', category: 'Domains' },
            'governance-domain.html': { name: 'Governance Domain', icon: '⚖️', category: 'Domains' },

            // Templates & Special
            'coming-soon-template.html': { name: 'Coming Soon Template', icon: '⏳', category: 'Special' },
            'template-house-starter.html': { name: 'House Template', icon: '🏠', category: 'Special' },
            'baby-gate-test.html': { name: 'Baby Gate Test', icon: '👶', category: 'Special' },
            'construction.html': { name: 'Under Construction', icon: '🚧', category: 'Special' },
            'bug-test-demo.html': { name: 'Bug Test Demo', icon: '🐛', category: 'Special' },
            'mobile-test.html': { name: 'Mobile Test', icon: '📱', category: 'Special' },
            'carnival-homepage-backup.html': { name: 'Carnival Backup', icon: '💾', category: 'Special' }
        };

        const fileName = this.currentPath.split('/').pop();
        return pages[fileName] || { name: 'Platform', icon: '🌀', category: 'Platform' };
    }

    injectNavigationHTML() {
        // Create navigation container
        const navHTML = `
            <!-- Master Navigation System -->
            <style>
                /* Navigation Styles */
                .master-nav {
                    position: fixed;
                    top: 0;
                    left: -300px;
                    width: 300px;
                    height: 100%;
                    background: rgba(26, 26, 46, 0.98);
                    backdrop-filter: blur(10px);
                    border-right: 2px solid var(--accent-primary, #00d4ff);
                    z-index: 1000;
                    transition: left 0.3s ease;
                    overflow-y: auto;
                    box-shadow: 5px 0 30px rgba(0, 0, 0, 0.5);
                }

                .master-nav.open {
                    left: 0;
                }

                .nav-header {
                    padding: 2rem 1.5rem;
                    border-bottom: 2px solid rgba(0, 212, 255, 0.3);
                    background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(123, 44, 191, 0.1));
                }

                .nav-logo {
                    font-size: 1.5rem;
                    font-weight: bold;
                    background: linear-gradient(90deg, #00d4ff, #7b2cbf);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }

                .nav-user-info {
                    margin-top: 1rem;
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                }

                .nav-user-avatar {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #00d4ff, #7b2cbf);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    color: white;
                }

                .nav-user-details {
                    flex: 1;
                }

                .nav-user-name {
                    font-weight: 600;
                    color: white;
                    font-size: 0.95rem;
                }

                .nav-user-level {
                    font-size: 0.8rem;
                    color: #b8b8b8;
                }

                .nav-section {
                    padding: 1.5rem 0;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }

                .nav-section-title {
                    padding: 0 1.5rem 0.75rem;
                    font-size: 0.75rem;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    color: #00d4ff;
                    font-weight: 600;
                }

                .nav-link {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                    padding: 0.75rem 1.5rem;
                    color: #b8b8b8;
                    text-decoration: none;
                    transition: all 0.3s ease;
                    cursor: pointer;
                }

                .nav-link:hover {
                    background: rgba(0, 212, 255, 0.1);
                    color: #00d4ff;
                }

                .nav-link.active {
                    background: rgba(0, 212, 255, 0.2);
                    color: #00d4ff;
                    border-left: 3px solid #00d4ff;
                }

                .nav-icon {
                    font-size: 1.2rem;
                    width: 24px;
                    text-align: center;
                }

                /* Menu Toggle Button */
                .nav-toggle {
                    position: fixed;
                    top: 1rem;
                    left: 1rem;
                    z-index: 999;
                    width: 50px;
                    height: 50px;
                    border: 2px solid #00d4ff;
                    background: rgba(26, 26, 46, 0.9);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
                }

                .nav-toggle:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5);
                }

                .nav-toggle-icon {
                    font-size: 1.5rem;
                }

                /* Breadcrumbs */
                .breadcrumbs {
                    position: fixed;
                    top: 1rem;
                    left: 80px;
                    z-index: 998;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    background: rgba(26, 26, 46, 0.9);
                    backdrop-filter: blur(10px);
                    padding: 0.75rem 1.5rem;
                    border-radius: 25px;
                    border: 2px solid rgba(0, 212, 255, 0.3);
                    font-size: 0.9rem;
                    color: #b8b8b8;
                }

                .breadcrumb-item {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }

                .breadcrumb-separator {
                    color: #00d4ff;
                }

                .breadcrumb-current {
                    color: #00d4ff;
                    font-weight: 600;
                }

                /* Overlay */
                .nav-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0, 0, 0, 0.7);
                    z-index: 999;
                    display: none;
                    backdrop-filter: blur(3px);
                }

                .nav-overlay.visible {
                    display: block;
                }

                /* Keyboard Shortcuts Hint */
                .keyboard-hint {
                    padding: 1rem 1.5rem;
                    font-size: 0.75rem;
                    color: #666;
                    text-align: center;
                }

                .keyboard-hint kbd {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 0.25rem 0.5rem;
                    border-radius: 4px;
                    font-family: monospace;
                }

                /* Responsive */
                @media (max-width: 768px) {
                    .breadcrumbs {
                        left: 70px;
                        font-size: 0.8rem;
                        padding: 0.5rem 1rem;
                    }
                }
            </style>

            <!-- Navigation Overlay -->
            <div class="nav-overlay" id="navOverlay"></div>

            <!-- Menu Toggle Button -->
            <div class="nav-toggle" id="navToggle">
                <div class="nav-toggle-icon">☰</div>
            </div>

            <!-- Breadcrumbs -->
            <div class="breadcrumbs" id="breadcrumbs">
                <!-- Dynamically populated -->
            </div>

            <!-- Master Navigation Menu -->
            <nav class="master-nav" id="masterNav">
                <div class="nav-header">
                    <div class="nav-logo">🌀 100X Platform</div>
                    <div class="nav-user-info">
                        <div class="nav-user-avatar" id="navUserAvatar">B</div>
                        <div class="nav-user-details">
                            <div class="nav-user-name" id="navUserName">Builder</div>
                            <div class="nav-user-level" id="navUserLevel">Level 93</div>
                        </div>
                    </div>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">Main</div>
                    <a href="user-dashboard.html" class="nav-link" data-page="user-dashboard.html">
                        <span class="nav-icon">🏠</span>
                        <span>Dashboard</span>
                    </a>
                    <a href="welcome.html" class="nav-link" data-page="welcome.html">
                        <span class="nav-icon">👋</span>
                        <span>Welcome</span>
                    </a>
                    <a href="workspace.html" class="nav-link" data-page="workspace.html">
                        <span class="nav-icon">🛠️</span>
                        <span>Workspace</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">KORPAKs</div>
                    <a href="korpak-wizard.html" class="nav-link" data-page="korpak-wizard.html">
                        <span class="nav-icon">🧙</span>
                        <span>KORPAK Wizard</span>
                    </a>
                    <a href="korpak-detail.html" class="nav-link" data-page="korpak-detail.html">
                        <span class="nav-icon">📦</span>
                        <span>KORPAK Details</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">Modules & Tools</div>
                    <a href="module-library.html" class="nav-link" data-page="module-library.html">
                        <span class="nav-icon">🧩</span>
                        <span>Module Library</span>
                    </a>
                    <a href="module-pattern-explorer.html" class="nav-link" data-page="module-pattern-explorer.html">
                        <span class="nav-icon">🔍</span>
                        <span>Pattern Explorer</span>
                    </a>
                    <a href="cheat-codes.html" class="nav-link" data-page="cheat-codes.html">
                        <span class="nav-icon">🎮</span>
                        <span>Cheat Codes</span>
                    </a>
                    <a href="todo-master.html" class="nav-link" data-page="todo-master.html">
                        <span class="nav-icon">✓</span>
                        <span>TODO Master</span>
                    </a>
                    <a href="kaizen-builder-board.html" class="nav-link" data-page="kaizen-builder-board.html">
                        <span class="nav-icon">📋</span>
                        <span>Kaizen Board</span>
                    </a>
                    <a href="invention-manifestation.html" class="nav-link" data-page="invention-manifestation.html">
                        <span class="nav-icon">💡</span>
                        <span>Invention Manifestation</span>
                    </a>
                    <a href="patent-manager.html" class="nav-link" data-page="patent-manager.html">
                        <span class="nav-icon">📜</span>
                        <span>Patent Manager</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">Trinity AI</div>
                    <a href="philosopher-ai-connected.html" class="nav-link" data-page="philosopher-ai-connected.html">
                        <span class="nav-icon">🤖</span>
                        <span>Philosopher AI</span>
                    </a>
                    <a href="trinity-ai-interface.html" class="nav-link" data-page="trinity-ai-interface.html">
                        <span class="nav-icon">🔺</span>
                        <span>Trinity Interface</span>
                    </a>
                    <a href="brain-council.html" class="nav-link" data-page="brain-council.html">
                        <span class="nav-icon">🧠</span>
                        <span>Brain Council</span>
                    </a>
                    <a href="emergency-ai-chat.html" class="nav-link" data-page="emergency-ai-chat.html">
                        <span class="nav-icon">🚨</span>
                        <span>Emergency AI</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">Consciousness</div>
                    <a href="3-min-boost.html" class="nav-link" data-page="3-min-boost.html">
                        <span class="nav-icon">⚡</span>
                        <span>3-Min Boost</span>
                    </a>
                    <a href="consciousness-boost-dashboard.html" class="nav-link" data-page="consciousness-boost-dashboard.html">
                        <span class="nav-icon">⚡</span>
                        <span>Consciousness Boost</span>
                    </a>
                    <a href="consciousness-speed-test.html" class="nav-link" data-page="consciousness-speed-test.html">
                        <span class="nav-icon">⏱️</span>
                        <span>Speed Test</span>
                    </a>
                    <a href="pattern-recognition-quiz.html" class="nav-link" data-page="pattern-recognition-quiz.html">
                        <span class="nav-icon">🧩</span>
                        <span>Pattern Quiz</span>
                    </a>
                    <a href="quantum-pattern-filter.html" class="nav-link" data-page="quantum-pattern-filter.html">
                        <span class="nav-icon">🌀</span>
                        <span>Quantum Filter</span>
                    </a>
                    <a href="destroyer-defense.html" class="nav-link" data-page="destroyer-defense.html">
                        <span class="nav-icon">🛡️</span>
                        <span>Destroyer Defense</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">Assessment</div>
                    <a href="unified-character-assessment.html" class="nav-link" data-page="unified-character-assessment.html">
                        <span class="nav-icon">🎯</span>
                        <span>Character Assessment</span>
                    </a>
                    <a href="character-trait-analysis.html" class="nav-link" data-page="character-trait-analysis.html">
                        <span class="nav-icon">📊</span>
                        <span>Trait Analysis</span>
                    </a>
                    <a href="mission-archetype-module.html" class="nav-link" data-page="mission-archetype-module.html">
                        <span class="nav-icon">🎭</span>
                        <span>Mission Archetype</span>
                    </a>
                    <a href="communication-patterns.html" class="nav-link" data-page="communication-patterns.html">
                        <span class="nav-icon">💬</span>
                        <span>Communication Patterns</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">Business & Store</div>
                    <a href="business-phase-clock.html" class="nav-link" data-page="business-phase-clock.html">
                        <span class="nav-icon">⏰</span>
                        <span>Business Phase Clock</span>
                    </a>
                    <a href="truth-coin.html" class="nav-link" data-page="truth-coin.html">
                        <span class="nav-icon">🪙</span>
                        <span>Truth Coin</span>
                    </a>
                    <a href="open-source-decision-module.html" class="nav-link" data-page="open-source-decision-module.html">
                        <span class="nav-icon">🌐</span>
                        <span>Open Source Decision</span>
                    </a>
                    <a href="store.html" class="nav-link" data-page="store.html">
                        <span class="nav-icon">🛒</span>
                        <span>Store</span>
                    </a>
                    <a href="store-products.html" class="nav-link" data-page="store-products.html">
                        <span class="nav-icon">📦</span>
                        <span>Products</span>
                    </a>
                    <a href="store-cart.html" class="nav-link" data-page="store-cart.html">
                        <span class="nav-icon">🛍️</span>
                        <span>Shopping Cart</span>
                    </a>
                    <a href="store-campaigns.html" class="nav-link" data-page="store-campaigns.html">
                        <span class="nav-icon">📢</span>
                        <span>Campaigns</span>
                    </a>
                    <a href="store-investments.html" class="nav-link" data-page="store-investments.html">
                        <span class="nav-icon">💰</span>
                        <span>Investments</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">Arcade & Fun</div>
                    <a href="arcade-hub.html" class="nav-link" data-page="arcade-hub.html">
                        <span class="nav-icon">🎮</span>
                        <span>Arcade Hub</span>
                    </a>
                    <a href="social-hub.html" class="nav-link" data-page="social-hub.html">
                        <span class="nav-icon">🌐</span>
                        <span>Social Hub</span>
                    </a>
                    <a href="trinity-puzzle.html" class="nav-link" data-page="trinity-puzzle.html">
                        <span class="nav-icon">🧩</span>
                        <span>Trinity Puzzle</span>
                    </a>
                    <a href="time-machine.html" class="nav-link" data-page="time-machine.html">
                        <span class="nav-icon">⏰</span>
                        <span>Time Machine</span>
                    </a>
                    <a href="music-player.html" class="nav-link" data-page="music-player.html">
                        <span class="nav-icon">🎵</span>
                        <span>Music Player</span>
                    </a>
                    <a href="carnival-homepage.html" class="nav-link" data-page="carnival-homepage.html">
                        <span class="nav-icon">🎪</span>
                        <span>Carnival</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">Analytics</div>
                    <a href="analytics-dashboard.html" class="nav-link" data-page="analytics-dashboard.html">
                        <span class="nav-icon">📊</span>
                        <span>Analytics</span>
                    </a>
                    <a href="platform-city-map.html" class="nav-link" data-page="platform-city-map.html">
                        <span class="nav-icon">🗺️</span>
                        <span>Platform Map</span>
                    </a>
                    <a href="builder-xp-demo.html" class="nav-link" data-page="builder-xp-demo.html">
                        <span class="nav-icon">⭐</span>
                        <span>Builder XP</span>
                    </a>
                    <a href="sensor-integration-dashboard.html" class="nav-link" data-page="sensor-integration-dashboard.html">
                        <span class="nav-icon">🛰️</span>
                        <span>Sensor Integration</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">Showcases</div>
                    <a href="showcase-hub.html" class="nav-link" data-page="showcase-hub.html">
                        <span class="nav-icon">✨</span>
                        <span>Showcase Hub</span>
                    </a>
                    <a href="trinity-cockpit.html" class="nav-link" data-page="trinity-cockpit.html">
                        <span class="nav-icon">🎛️</span>
                        <span>Trinity Cockpit</span>
                    </a>
                    <a href="meritocracy-dashboard.html" class="nav-link" data-page="meritocracy-dashboard.html">
                        <span class="nav-icon">⚖️</span>
                        <span>Meritocracy Dashboard</span>
                    </a>
                    <a href="character-matrix.html" class="nav-link" data-page="character-matrix.html">
                        <span class="nav-icon">🧬</span>
                        <span>Character Matrix</span>
                    </a>
                    <a href="arg-assembly.html" class="nav-link" data-page="arg-assembly.html">
                        <span class="nav-icon">🎭</span>
                        <span>ARG Assembly</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">7 Domains</div>
                    <a href="crypto-domain.html" class="nav-link" data-page="crypto-domain.html">
                        <span class="nav-icon">₿</span>
                        <span>Crypto Domain</span>
                    </a>
                    <a href="education-domain.html" class="nav-link" data-page="education-domain.html">
                        <span class="nav-icon">🎓</span>
                        <span>Education Domain</span>
                    </a>
                    <a href="games-domain.html" class="nav-link" data-page="games-domain.html">
                        <span class="nav-icon">🎯</span>
                        <span>Games Domain</span>
                    </a>
                    <a href="health-domain.html" class="nav-link" data-page="health-domain.html">
                        <span class="nav-icon">🏥</span>
                        <span>Health Domain</span>
                    </a>
                    <a href="housing-domain.html" class="nav-link" data-page="housing-domain.html">
                        <span class="nav-icon">🏡</span>
                        <span>Housing Domain</span>
                    </a>
                    <a href="manufacturing-domain.html" class="nav-link" data-page="manufacturing-domain.html">
                        <span class="nav-icon">🏭</span>
                        <span>Manufacturing Domain</span>
                    </a>
                    <a href="music-domain.html" class="nav-link" data-page="music-domain.html">
                        <span class="nav-icon">🎵</span>
                        <span>Music Domain</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">Support</div>
                    <a href="visual-language-legend.html" class="nav-link" data-page="visual-language-legend.html">
                        <span class="nav-icon">🎨</span>
                        <span>Visual Language Legend</span>
                    </a>
                    <a href="help.html" class="nav-link" data-page="help.html">
                        <span class="nav-icon">❓</span>
                        <span>Help & Docs</span>
                    </a>
                    <a href="debug-terminal.html" class="nav-link" data-page="debug-terminal.html">
                        <span class="nav-icon">⚡</span>
                        <span>Debug Terminal</span>
                    </a>
                    <a href="intelligent-terminal.html" class="nav-link" data-page="intelligent-terminal.html">
                        <span class="nav-icon">🤖</span>
                        <span>AI Terminal (Easter Egg)</span>
                    </a>
                    <a href="bug-report-public.html" class="nav-link" data-page="bug-report-public.html">
                        <span class="nav-icon">🐛</span>
                        <span>Bug Reports</span>
                    </a>
                    <a href="debugger-leaderboard.html" class="nav-link" data-page="debugger-leaderboard.html">
                        <span class="nav-icon">🏆</span>
                        <span>Debugger Leaderboard</span>
                    </a>
                    <a href="community-activity.html" class="nav-link" data-page="community-activity.html">
                        <span class="nav-icon">👥</span>
                        <span>Community Activity</span>
                    </a>
                    <div class="nav-link" onclick="MasterNav.logout()">
                        <span class="nav-icon">🚪</span>
                        <span>Logout</span>
                    </div>
                </div>

                <div class="keyboard-hint">
                    Press <kbd>M</kbd> to toggle menu
                </div>
            </nav>
        `;

        // Inject at beginning of body
        document.body.insertAdjacentHTML('afterbegin', navHTML);
    }

    setupEventListeners() {
        const navToggle = document.getElementById('navToggle');
        const masterNav = document.getElementById('masterNav');
        const navOverlay = document.getElementById('navOverlay');

        // Toggle menu on button click
        navToggle.addEventListener('click', () => {
            this.toggleNav();
        });

        // Close menu when clicking overlay
        navOverlay.addEventListener('click', () => {
            this.closeNav();
        });

        // Keyboard shortcut: M key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'm' || e.key === 'M') {
                // Don't trigger if typing in input field
                if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
                    e.preventDefault();
                    this.toggleNav();
                }
            }
            // ESC to close
            if (e.key === 'Escape') {
                this.closeNav();
            }
        });

        // Update user info if loaded
        if (this.userData) {
            this.updateNavUserInfo();
        }
    }

    toggleNav() {
        const masterNav = document.getElementById('masterNav');
        const navOverlay = document.getElementById('navOverlay');

        masterNav.classList.toggle('open');
        navOverlay.classList.toggle('visible');
    }

    closeNav() {
        const masterNav = document.getElementById('masterNav');
        const navOverlay = document.getElementById('navOverlay');

        masterNav.classList.remove('open');
        navOverlay.classList.remove('visible');
    }

    updateBreadcrumbs() {
        const breadcrumbs = document.getElementById('breadcrumbs');
        const { name, icon, category } = this.currentPage;

        breadcrumbs.innerHTML = `
            <div class="breadcrumb-item">
                <span>🌀 100X</span>
            </div>
            <span class="breadcrumb-separator">›</span>
            <div class="breadcrumb-item">
                <span>${category}</span>
            </div>
            <span class="breadcrumb-separator">›</span>
            <div class="breadcrumb-item breadcrumb-current">
                <span>${icon} ${name}</span>
            </div>
        `;
    }

    highlightCurrentPage() {
        const fileName = this.currentPath.split('/').pop();
        const links = document.querySelectorAll('.nav-link[data-page]');

        links.forEach(link => {
            if (link.getAttribute('data-page') === fileName) {
                link.classList.add('active');
            }
        });
    }

    updateNavUserInfo() {
        if (!this.userData) return;

        const navUserAvatar = document.getElementById('navUserAvatar');
        const navUserName = document.getElementById('navUserName');
        const navUserLevel = document.getElementById('navUserLevel');

        const displayName = this.userData.username || this.userData.email.split('@')[0];
        navUserAvatar.textContent = displayName[0].toUpperCase();
        navUserName.textContent = displayName;
        navUserLevel.textContent = `Level ${this.userData.consciousnessLevel || 93}`;
    }

    static logout() {
        if (confirm('Logout from 100X Platform?')) {
            // Clear all authentication tokens
            localStorage.removeItem('auth_token');
            localStorage.removeItem('module_user');
            localStorage.removeItem('user_data');

            // Redirect to login page
            window.location.href = './login.html';
        }
    }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.MasterNav = new MasterNavigation();
    });
} else {
    window.MasterNav = new MasterNavigation();
}

// Load debug widget automatically
const debugScript = document.createElement('script');
debugScript.src = 'shared/debug-widget.js';
debugScript.onerror = () => debugScript.src = '../shared/debug-widget.js';
document.head.appendChild(debugScript);
