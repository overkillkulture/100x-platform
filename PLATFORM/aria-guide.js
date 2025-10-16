/**
 * ARIA - AI Revolutionary Intelligence Assistant
 * Cyberpunk avatar guide that helps users navigate the 100X Platform
 * Auto-injects on all pages
 */

class AriaGuide {
    constructor() {
        this.chatOpen = false;
        this.hasShownWelcome = localStorage.getItem('aria_welcomed') === 'true';
        this.init();
    }

    init() {
        // Inject styles
        this.injectStyles();

        // Inject HTML
        this.injectHTML();

        // Set up event listeners
        this.setupEventListeners();

        // Auto-show welcome for new users
        if (!this.hasShownWelcome) {
            setTimeout(() => {
                this.showNotification();
                this.showContextTip();
            }, 3000);
        }
    }

    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* ARIA Avatar Guide Styles */
            .aria-avatar-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 9999;
            }

            .aria-avatar-circle {
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: linear-gradient(135deg, #ff6b00, #ffd700, #00d4ff, #7b2cbf);
                background-size: 300% 300%;
                animation: aria-gradient-shift 8s ease infinite, aria-pulse 3s ease-in-out infinite;
                cursor: pointer;
                position: relative;
                box-shadow: 0 0 40px rgba(0, 212, 255, 0.6), 0 0 80px rgba(255, 107, 0, 0.4);
                transition: all 0.3s;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }

            .aria-avatar-circle:hover {
                transform: scale(1.1);
                box-shadow: 0 0 60px rgba(0, 212, 255, 0.8), 0 0 120px rgba(255, 107, 0, 0.6);
            }

            .aria-avatar-circle.talking {
                animation: aria-gradient-shift 2s ease infinite, aria-talking 0.5s ease-in-out infinite;
            }

            .aria-avatar-image {
                width: 90px;
                height: 90px;
                border-radius: 50%;
                background:
                    radial-gradient(circle at 30% 30%, rgba(255, 107, 0, 0.4), transparent 50%),
                    radial-gradient(circle at 70% 70%, rgba(0, 212, 255, 0.4), transparent 50%),
                    linear-gradient(135deg, rgba(123, 44, 191, 0.6), rgba(0, 0, 0, 0.8));
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 48px;
                position: relative;
                overflow: hidden;
            }

            .aria-avatar-image::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(0, 212, 255, 0.2), transparent);
                animation: aria-scan 3s linear infinite;
            }

            .aria-avatar-image::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background:
                    linear-gradient(90deg, transparent 48%, rgba(0, 212, 255, 0.1) 50%, transparent 52%),
                    linear-gradient(0deg, transparent 48%, rgba(255, 107, 0, 0.1) 50%, transparent 52%);
                background-size: 4px 4px;
                animation: aria-glitch 5s steps(5) infinite;
            }

            .aria-avatar-face {
                font-size: 52px;
                filter: drop-shadow(0 0 15px rgba(0, 212, 255, 1))
                        drop-shadow(0 0 30px rgba(255, 107, 0, 0.6));
                position: relative;
                z-index: 1;
            }

            .aria-status-dot {
                position: absolute;
                bottom: 8px;
                right: 8px;
                width: 16px;
                height: 16px;
                border-radius: 50%;
                background: #00ff88;
                border: 3px solid #0a0a0a;
                box-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
                animation: aria-blink 2s ease-in-out infinite;
            }

            .aria-notification-badge {
                position: absolute;
                top: -5px;
                right: -5px;
                background: #ff0000;
                color: white;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                display: none;
                align-items: center;
                justify-content: center;
                font-size: 11px;
                font-weight: bold;
                border: 2px solid #0a0a0a;
                animation: aria-bounce 2s ease infinite;
            }

            .aria-notification-badge.show {
                display: flex;
            }

            .aria-chat-bubble {
                position: fixed;
                bottom: 140px;
                right: 20px;
                max-width: 380px;
                background: rgba(26, 26, 46, 0.98);
                border: 2px solid #00d4ff;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 212, 255, 0.4);
                display: none;
                z-index: 9998;
                backdrop-filter: blur(10px);
                font-family: 'Courier New', monospace;
            }

            .aria-chat-bubble.active {
                display: block;
                animation: aria-slide-up 0.3s ease;
            }

            .aria-chat-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
                padding-bottom: 8px;
                border-bottom: 1px solid rgba(0, 212, 255, 0.3);
            }

            .aria-chat-name {
                color: #ffd700;
                font-size: 16px;
                font-weight: bold;
            }

            .aria-chat-role {
                color: #b8b8b8;
                font-size: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .aria-close-btn {
                background: none;
                border: none;
                color: #ff6b00;
                font-size: 20px;
                cursor: pointer;
                transition: all 0.3s;
                line-height: 1;
            }

            .aria-close-btn:hover {
                color: #ff0000;
                transform: rotate(90deg);
            }

            .aria-chat-message {
                color: #00ffff;
                font-size: 13px;
                line-height: 1.5;
                margin-bottom: 15px;
            }

            .aria-chat-options {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            .aria-option-btn {
                padding: 10px 15px;
                background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(123, 44, 191, 0.2));
                border: 2px solid #00d4ff;
                border-radius: 8px;
                color: #00ffff;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.3s;
                text-align: left;
                font-family: 'Courier New', monospace;
            }

            .aria-option-btn:hover {
                background: linear-gradient(135deg, rgba(0, 212, 255, 0.4), rgba(123, 44, 191, 0.4));
                border-color: #ffd700;
                transform: translateX(5px);
            }

            .aria-quick-tip {
                position: fixed;
                top: 20px;
                right: 20px;
                max-width: 280px;
                background: rgba(255, 215, 0, 0.95);
                color: #000;
                padding: 12px 16px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(255, 215, 0, 0.6);
                display: none;
                z-index: 9997;
                animation: aria-slide-down 0.3s ease;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }

            .aria-quick-tip.active {
                display: block;
            }

            /* Animations */
            @keyframes aria-gradient-shift {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }

            @keyframes aria-pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }

            @keyframes aria-talking {
                0%, 100% { transform: scale(1); }
                25% { transform: scale(1.08); }
                75% { transform: scale(1.03); }
            }

            @keyframes aria-blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }

            @keyframes aria-bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-5px); }
            }

            @keyframes aria-scan {
                0% { transform: translate(-50%, -50%) rotate(0deg); }
                100% { transform: translate(-50%, -50%) rotate(360deg); }
            }

            @keyframes aria-glitch {
                0%, 100% { opacity: 0; }
                10%, 30%, 50%, 70%, 90% { opacity: 0.8; transform: translateX(2px); }
                20%, 40%, 60%, 80% { opacity: 0; transform: translateX(-2px); }
            }

            @keyframes aria-slide-up {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes aria-slide-down {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* Mobile Responsive */
            @media (max-width: 768px) {
                .aria-avatar-container {
                    bottom: 80px;
                    right: 10px;
                }

                .aria-avatar-circle {
                    width: 70px;
                    height: 70px;
                }

                .aria-avatar-image {
                    width: 60px;
                    height: 60px;
                }

                .aria-avatar-face {
                    font-size: 32px;
                }

                .aria-chat-bubble {
                    bottom: 160px;
                    right: 10px;
                    left: 10px;
                    max-width: calc(100% - 20px);
                }
            }
        `;
        document.head.appendChild(style);
    }

    injectHTML() {
        const html = `
            <div class="aria-avatar-container" id="ariaContainer">
                <div class="aria-avatar-circle" id="ariaCircle">
                    <div class="aria-avatar-image">
                        <div class="aria-avatar-face">👩‍💻</div>
                    </div>
                    <div class="aria-status-dot"></div>
                    <div class="aria-notification-badge" id="ariaBadge">1</div>
                </div>
            </div>

            <div class="aria-chat-bubble" id="ariaChatBubble">
                <div class="aria-chat-header">
                    <div>
                        <div class="aria-chat-name">ARIA</div>
                        <div class="aria-chat-role">Your 100X Guide</div>
                    </div>
                    <button class="aria-close-btn" id="ariaCloseBtn">×</button>
                </div>

                <div class="aria-chat-message" id="ariaChatMessage">
                    Hey builder! 👋 I'm ARIA, your cyberpunk guide.
                    Need help navigating the platform or want to explore features?
                </div>

                <div class="aria-chat-options" id="ariaChatOptions"></div>
            </div>

            <div class="aria-quick-tip" id="ariaQuickTip"></div>
        `;

        document.body.insertAdjacentHTML('beforeend', html);
    }

    setupEventListeners() {
        document.getElementById('ariaCircle').addEventListener('click', () => this.toggleChat());
        document.getElementById('ariaCloseBtn').addEventListener('click', () => this.closeChat());
    }

    toggleChat() {
        const bubble = document.getElementById('ariaChatBubble');
        const circle = document.getElementById('ariaCircle');

        this.chatOpen = !this.chatOpen;
        bubble.classList.toggle('active');
        circle.classList.toggle('talking');

        if (this.chatOpen) {
            this.hideNotification();
            localStorage.setItem('aria_welcomed', 'true');
            this.showDefaultOptions();
            this.speakMessage();
        }
    }

    closeChat() {
        const bubble = document.getElementById('ariaChatBubble');
        const circle = document.getElementById('ariaCircle');

        this.chatOpen = false;
        bubble.classList.remove('active');
        circle.classList.remove('talking');
    }

    showNotification() {
        document.getElementById('ariaBadge').classList.add('show');
    }

    hideNotification() {
        document.getElementById('ariaBadge').classList.remove('show');
    }

    showDefaultOptions() {
        const options = document.getElementById('ariaChatOptions');
        options.innerHTML = `
            <button class="aria-option-btn" onclick="window.AriaGuide.showTour()">
                🗺️ Take platform tour
            </button>
            <button class="aria-option-btn" onclick="window.AriaGuide.goToVoiceCompiler()">
                ⚖️ Build federal case
            </button>
            <button class="aria-option-btn" onclick="window.AriaGuide.goToBlueprint()">
                🎨 AI blueprint designer
            </button>
            <button class="aria-option-btn" onclick="window.AriaGuide.showTips()">
                💡 Show pro tips
            </button>
        `;
    }

    updateMessage(message) {
        document.getElementById('ariaChatMessage').innerHTML = message;
        this.speakMessage();
    }

    speakMessage() {
        const circle = document.getElementById('ariaCircle');
        circle.classList.add('talking');
        setTimeout(() => circle.classList.remove('talking'), 2000);
    }

    showQuickTip(message, duration = 5000) {
        const tip = document.getElementById('ariaQuickTip');
        tip.innerHTML = message;
        tip.classList.add('active');
        setTimeout(() => tip.classList.remove('active'), duration);
    }

    showContextTip() {
        const page = window.location.pathname.split('/').pop();

        if (page === 'login.html') {
            this.showQuickTip('👋 <strong>New here?</strong> Just enter any email and password to create an account instantly!');
        } else if (page === 'user-dashboard.html') {
            this.showQuickTip('🏠 <strong>Welcome!</strong> Click any room card to explore. Press <strong>M</strong> for master nav.');
        } else if (page === 'voice-case-compiler.html') {
            this.showQuickTip('🎤 <strong>Pro Tip:</strong> Talk naturally for 20 minutes. AI extracts everything!');
        } else {
            this.showQuickTip('💡 <strong>Quick Tip:</strong> Click ARIA (bottom-right) anytime you need help!');
        }
    }

    showTour() {
        this.updateMessage(`
            🗺️ <strong>Platform Tour</strong><br><br>
            <strong>Main Areas:</strong><br>
            • Dashboard - Command center<br>
            • Voice Compiler - Federal cases<br>
            • Timeline - Pattern visualization<br>
            • Blueprint - AI design tool<br><br>
            Press <strong>M</strong> for master navigation!
        `);
        this.showQuickTip('⌨️ <strong>Shortcut:</strong> Press M to open navigation');
    }

    goToVoiceCompiler() {
        window.open('./voice-case-compiler.html', '_blank');
        this.showQuickTip('🎤 Voice Compiler opened!');
    }

    goToBlueprint() {
        window.open('./ai-native-blueprint.html', '_blank');
        this.showQuickTip('🎨 Blueprint opened!');
    }

    showTips() {
        this.updateMessage(`
            💡 <strong>Pro Tips</strong><br><br>
            1. Press <strong>M</strong> for master nav<br>
            2. Use <strong>humor</strong> not anger (blue signals!)<br>
            3. Timeline shows patterns over time<br>
            4. Demo data in most tools<br>
            5. Everything auto-saves locally<br><br>
            <em>Built BY AI, FOR builders!</em>
        `);
    }
}

// Auto-initialize when DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.AriaGuide = new AriaGuide();
    });
} else {
    window.AriaGuide = new AriaGuide();
}
