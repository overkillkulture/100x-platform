/**
 * ARIA Avatar - Floating AI Assistant
 * Connects to Philosopher AI backend (localhost:3001)
 * Modern chat bubble UI with animations
 */

class ARIAAvatar {
    constructor() {
        this.isOpen = false;
        this.isTyping = false;
        this.conversationHistory = [];
        this.API_BASE = 'http://localhost:3001';

        // Try to get auth token
        this.authToken = localStorage.getItem('auth_token') ||
                         this.getCookie('auth_token');

        this.init();
    }

    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    init() {
        // Inject styles
        this.injectStyles();

        // Create HTML structure
        this.createHTML();

        // Attach event listeners
        this.attachEventListeners();

        // Load conversation history from localStorage
        this.loadHistory();

        // Show welcome message if first visit
        if (!localStorage.getItem('aria_welcomed')) {
            setTimeout(() => this.showWelcomeNotification(), 2000);
        }
    }

    injectStyles() {
        const styles = `
            /* ARIA Avatar Styles */
            .aria-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 10000;
                font-family: 'Courier New', monospace;
            }

            .aria-button {
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background: linear-gradient(135deg, #ff6b00, #ffd700);
                border: 3px solid #00ffff;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 20px rgba(255, 107, 0, 0.5),
                           0 0 40px rgba(0, 255, 255, 0.3);
                transition: all 0.3s ease;
                animation: aria-pulse 2s infinite;
                position: relative;
                overflow: visible;
            }

            /* N64-Style Holographic Avatar */
            .aria-avatar-n64 {
                width: 100%;
                height: 100%;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            /* Face base - low poly diamond shape */
            .aria-face {
                width: 50px;
                height: 60px;
                background: linear-gradient(135deg, #ff00ff, #00ffff);
                clip-path: polygon(50% 0%, 100% 30%, 100% 70%, 50% 100%, 0% 70%, 0% 30%);
                position: relative;
                animation: aria-face-glow 2s infinite;
                filter: brightness(1.2) saturate(1.5);
            }

            @keyframes aria-face-glow {
                0%, 100% {
                    filter: brightness(1.2) saturate(1.5) hue-rotate(0deg);
                }
                50% {
                    filter: brightness(1.5) saturate(2) hue-rotate(20deg);
                }
            }

            /* Eyes - pixelated style */
            .aria-eye {
                position: absolute;
                width: 8px;
                height: 8px;
                background: #00ffff;
                box-shadow: 0 0 10px #00ffff, inset 0 0 5px #fff;
                animation: aria-eye-blink 4s infinite;
            }

            .aria-eye.left {
                top: 20px;
                left: 12px;
            }

            .aria-eye.right {
                top: 20px;
                right: 12px;
            }

            @keyframes aria-eye-blink {
                0%, 48%, 52%, 100% {
                    height: 8px;
                    opacity: 1;
                }
                50% {
                    height: 2px;
                    opacity: 0.8;
                }
            }

            /* Mouth - pixelated smile */
            .aria-mouth {
                position: absolute;
                bottom: 18px;
                left: 50%;
                transform: translateX(-50%);
                width: 20px;
                height: 3px;
                background: #ffd700;
                box-shadow: 0 0 5px #ffd700;
                border-radius: 0 0 10px 10px;
            }

            /* Hair/data streams */
            .aria-hair {
                position: absolute;
                top: -5px;
                left: 50%;
                transform: translateX(-50%);
                width: 3px;
                height: 15px;
                background: linear-gradient(to bottom, #ff00ff, transparent);
                animation: aria-data-stream 1.5s infinite;
            }

            .aria-hair:nth-child(2) {
                left: 30%;
                animation-delay: 0.3s;
            }

            .aria-hair:nth-child(3) {
                left: 70%;
                animation-delay: 0.6s;
            }

            @keyframes aria-data-stream {
                0% {
                    opacity: 0;
                    height: 5px;
                }
                50% {
                    opacity: 1;
                    height: 20px;
                }
                100% {
                    opacity: 0;
                    height: 25px;
                }
            }

            /* Holographic scan lines */
            .aria-scanline {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: rgba(0, 255, 255, 0.5);
                animation: aria-scan 3s linear infinite;
                pointer-events: none;
            }

            @keyframes aria-scan {
                0% {
                    top: 0;
                    opacity: 0;
                }
                50% {
                    opacity: 1;
                }
                100% {
                    top: 100%;
                    opacity: 0;
                }
            }

            /* Floating particles - N64 sparkle effect */
            .aria-particle {
                position: absolute;
                width: 3px;
                height: 3px;
                background: #ffd700;
                border-radius: 50%;
                animation: aria-float 2s infinite;
                box-shadow: 0 0 5px #ffd700;
            }

            .aria-particle:nth-child(1) {
                top: 10%;
                left: -10px;
                animation-delay: 0s;
            }

            .aria-particle:nth-child(2) {
                top: 30%;
                right: -10px;
                animation-delay: 0.7s;
            }

            .aria-particle:nth-child(3) {
                top: 60%;
                left: -12px;
                animation-delay: 1.4s;
            }

            @keyframes aria-float {
                0% {
                    transform: translateY(0) scale(0);
                    opacity: 0;
                }
                50% {
                    transform: translateY(-20px) scale(1);
                    opacity: 1;
                }
                100% {
                    transform: translateY(-40px) scale(0);
                    opacity: 0;
                }
            }

            .aria-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 30px rgba(255, 215, 0, 0.7);
            }

            .aria-button.open {
                background: linear-gradient(135deg, #00ffff, #0088ff);
            }

            @keyframes aria-pulse {
                0%, 100% { box-shadow: 0 4px 20px rgba(255, 107, 0, 0.5); }
                50% { box-shadow: 0 4px 30px rgba(255, 215, 0, 0.8); }
            }

            .aria-notification {
                position: absolute;
                bottom: 70px;
                right: 0;
                background: rgba(26, 26, 46, 0.98);
                border: 2px solid #00ffff;
                border-radius: 15px;
                padding: 15px;
                max-width: 280px;
                box-shadow: 0 4px 20px rgba(0, 255, 255, 0.3);
                opacity: 0;
                transform: translateY(10px);
                transition: all 0.3s ease;
                pointer-events: none;
            }

            .aria-notification.show {
                opacity: 1;
                transform: translateY(0);
                pointer-events: all;
            }

            .aria-notification-text {
                color: #00ffff;
                font-size: 13px;
                line-height: 1.5;
                margin-bottom: 8px;
            }

            .aria-notification-close {
                color: #ffd700;
                text-align: right;
                font-size: 11px;
                cursor: pointer;
            }

            .aria-chat-window {
                position: absolute;
                bottom: 70px;
                right: 0;
                width: 380px;
                height: 550px;
                background: rgba(10, 10, 20, 0.98);
                border: 3px solid #ff6b00;
                border-radius: 20px;
                box-shadow: 0 8px 40px rgba(255, 107, 0, 0.4);
                display: none;
                flex-direction: column;
                overflow: hidden;
            }

            .aria-chat-window.open {
                display: flex;
                animation: aria-slide-up 0.3s ease;
            }

            @keyframes aria-slide-up {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .aria-header {
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                padding: 15px;
                border-bottom: 2px solid #00ffff;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            .aria-header-left {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .aria-avatar-small {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: linear-gradient(135deg, #ff6b00, #ffd700);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                border: 2px solid #00ffff;
            }

            .aria-header-text h3 {
                color: #ffd700;
                font-size: 16px;
                margin: 0;
            }

            .aria-header-text p {
                color: #00ffff;
                font-size: 11px;
                margin: 2px 0 0 0;
            }

            .aria-close {
                color: #00ffff;
                font-size: 24px;
                cursor: pointer;
                transition: color 0.3s;
            }

            .aria-close:hover {
                color: #ff6b00;
            }

            .aria-messages {
                flex: 1;
                overflow-y: auto;
                padding: 15px;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }

            .aria-messages::-webkit-scrollbar {
                width: 8px;
            }

            .aria-messages::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.3);
            }

            .aria-messages::-webkit-scrollbar-thumb {
                background: #00ffff;
                border-radius: 4px;
            }

            .aria-message {
                display: flex;
                gap: 10px;
                animation: aria-message-in 0.3s ease;
            }

            @keyframes aria-message-in {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .aria-message.user {
                flex-direction: row-reverse;
            }

            .aria-message-avatar {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                flex-shrink: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
            }

            .aria-message.aria .aria-message-avatar {
                background: linear-gradient(135deg, #ff6b00, #ffd700);
                border: 2px solid #00ffff;
            }

            .aria-message.user .aria-message-avatar {
                background: linear-gradient(135deg, #00ffff, #0088ff);
                border: 2px solid #ffd700;
            }

            .aria-message-content {
                max-width: 75%;
                padding: 12px;
                border-radius: 12px;
                font-size: 13px;
                line-height: 1.5;
            }

            .aria-message.aria .aria-message-content {
                background: rgba(255, 107, 0, 0.15);
                border: 1px solid #ff6b00;
                color: #00ffff;
            }

            .aria-message.user .aria-message-content {
                background: rgba(0, 255, 255, 0.15);
                border: 1px solid #00ffff;
                color: #ffd700;
            }

            .aria-typing {
                display: flex;
                gap: 4px;
                padding: 8px;
            }

            .aria-typing-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #00ffff;
                animation: aria-typing-bounce 1.4s infinite;
            }

            .aria-typing-dot:nth-child(2) {
                animation-delay: 0.2s;
            }

            .aria-typing-dot:nth-child(3) {
                animation-delay: 0.4s;
            }

            @keyframes aria-typing-bounce {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }

            .aria-input-container {
                padding: 15px;
                border-top: 2px solid #00ffff;
                background: rgba(26, 26, 46, 0.8);
            }

            .aria-input-wrapper {
                display: flex;
                gap: 10px;
            }

            .aria-input {
                flex: 1;
                padding: 12px;
                background: rgba(0, 0, 0, 0.5);
                border: 2px solid #00ffff;
                border-radius: 10px;
                color: #00ffff;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                outline: none;
                transition: border-color 0.3s;
            }

            .aria-input:focus {
                border-color: #ffd700;
            }

            .aria-send-btn {
                padding: 12px 20px;
                background: linear-gradient(135deg, #ff6b00, #ffd700);
                border: none;
                border-radius: 10px;
                color: #000;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
                font-family: 'Courier New', monospace;
            }

            .aria-send-btn:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(255, 215, 0, 0.5);
            }

            .aria-send-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }

            .aria-quick-actions {
                display: flex;
                gap: 8px;
                margin-top: 10px;
                flex-wrap: wrap;
            }

            .aria-quick-btn {
                padding: 6px 12px;
                background: rgba(0, 255, 255, 0.1);
                border: 1px solid #00ffff;
                border-radius: 6px;
                color: #00ffff;
                font-size: 11px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .aria-quick-btn:hover {
                background: rgba(0, 255, 255, 0.2);
                transform: translateY(-1px);
            }

            @media (max-width: 480px) {
                .aria-chat-window {
                    width: calc(100vw - 40px);
                    height: calc(100vh - 100px);
                    bottom: 10px;
                    right: 10px;
                }

                .aria-container {
                    bottom: 10px;
                    right: 10px;
                }
            }
        `;

        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }

    createHTML() {
        const container = document.createElement('div');
        container.className = 'aria-container';
        container.innerHTML = `
            <div class="aria-notification" id="aria-notification">
                <div class="aria-notification-text" id="aria-notification-text">
                    👋 Hi! I'm ARIA, your AI guide. Click me if you need help!
                </div>
                <div class="aria-notification-close" onclick="window.ariaAvatar.closeNotification()">
                    Click to dismiss
                </div>
            </div>

            <div class="aria-chat-window" id="aria-chat-window">
                <div class="aria-header">
                    <div class="aria-header-left">
                        <div class="aria-avatar-small">🤖</div>
                        <div class="aria-header-text">
                            <h3>ARIA</h3>
                            <p>Your AI Guide</p>
                        </div>
                    </div>
                    <div class="aria-close" onclick="window.ariaAvatar.toggleChat()">×</div>
                </div>

                <div class="aria-messages" id="aria-messages">
                    <!-- Messages will be inserted here -->
                </div>

                <div class="aria-input-container">
                    <div class="aria-quick-actions">
                        <button class="aria-quick-btn" onclick="window.ariaAvatar.askQuickQuestion('What is this platform?')">
                            What is this?
                        </button>
                        <button class="aria-quick-btn" onclick="window.ariaAvatar.askQuickQuestion('How do I get started?')">
                            Getting started
                        </button>
                        <button class="aria-quick-btn" onclick="window.ariaAvatar.askQuickQuestion('What are KORPAKs?')">
                            About KORPAKs
                        </button>
                    </div>
                    <div class="aria-input-wrapper">
                        <input
                            type="text"
                            class="aria-input"
                            id="aria-input"
                            placeholder="Ask me anything..."
                            onkeypress="if(event.key === 'Enter') window.ariaAvatar.sendMessage()"
                        >
                        <button class="aria-send-btn" id="aria-send-btn" onclick="window.ariaAvatar.sendMessage()">
                            Send
                        </button>
                    </div>
                </div>
            </div>

            <div class="aria-button" onclick="window.ariaAvatar.toggleChat()">
                <div class="aria-avatar-n64">
                    <div class="aria-particle"></div>
                    <div class="aria-particle"></div>
                    <div class="aria-particle"></div>
                    <div class="aria-face">
                        <div class="aria-hair"></div>
                        <div class="aria-hair"></div>
                        <div class="aria-hair"></div>
                        <div class="aria-eye left"></div>
                        <div class="aria-eye right"></div>
                        <div class="aria-mouth"></div>
                    </div>
                    <div class="aria-scanline"></div>
                </div>
            </div>
        `;

        document.body.appendChild(container);
    }

    attachEventListeners() {
        // Make instance globally accessible
        window.ariaAvatar = this;
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('aria-chat-window');
        const button = document.querySelector('.aria-button');

        if (this.isOpen) {
            chatWindow.classList.add('open');
            button.classList.add('open');
            this.closeNotification();

            // If first time opening, show welcome message
            if (this.conversationHistory.length === 0) {
                this.addMessage('aria', 'Hello! 👋 I\'m ARIA, your AI guide for the 100X Platform.\n\nI can help you:\n• Understand how the platform works\n• Learn about KORPAKs and modules\n• Navigate features\n• Answer questions about consciousness tech\n\nWhat would you like to know?');
            }

            // Focus input
            setTimeout(() => {
                document.getElementById('aria-input').focus();
            }, 100);
        } else {
            chatWindow.classList.remove('open');
            button.classList.remove('open');
        }
    }

    showWelcomeNotification() {
        const notification = document.getElementById('aria-notification');
        notification.classList.add('show');
        localStorage.setItem('aria_welcomed', 'true');

        // Auto-hide after 10 seconds
        setTimeout(() => {
            this.closeNotification();
        }, 10000);
    }

    closeNotification() {
        const notification = document.getElementById('aria-notification');
        notification.classList.remove('show');
    }

    addMessage(sender, text) {
        const messagesContainer = document.getElementById('aria-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `aria-message ${sender}`;

        const avatar = sender === 'aria' ? '🤖' : '👤';

        messageDiv.innerHTML = `
            <div class="aria-message-avatar">${avatar}</div>
            <div class="aria-message-content">${text}</div>
        `;

        messagesContainer.appendChild(messageDiv);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Save to history
        this.conversationHistory.push({ sender, text, timestamp: Date.now() });
        this.saveHistory();
    }

    showTyping() {
        const messagesContainer = document.getElementById('aria-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'aria-message aria';
        typingDiv.id = 'aria-typing-indicator';

        typingDiv.innerHTML = `
            <div class="aria-message-avatar">🤖</div>
            <div class="aria-message-content">
                <div class="aria-typing">
                    <div class="aria-typing-dot"></div>
                    <div class="aria-typing-dot"></div>
                    <div class="aria-typing-dot"></div>
                </div>
            </div>
        `;

        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideTyping() {
        const typingIndicator = document.getElementById('aria-typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    async sendMessage() {
        const input = document.getElementById('aria-input');
        const sendBtn = document.getElementById('aria-send-btn');
        const message = input.value.trim();

        if (!message || this.isTyping) return;

        // Add user message
        this.addMessage('user', message);
        input.value = '';

        // Disable input
        this.isTyping = true;
        sendBtn.disabled = true;
        input.disabled = true;

        // Show typing indicator
        this.showTyping();

        try {
            // Call Philosopher AI API
            const response = await this.callPhilosopherAPI(message);

            // Hide typing and show response
            this.hideTyping();
            this.addMessage('aria', response);

        } catch (error) {
            console.error('ARIA Error:', error);
            this.hideTyping();
            this.addMessage('aria', '⚠️ Sorry, I\'m having trouble connecting right now. Please make sure the API server is running (localhost:3001).');
        } finally {
            // Re-enable input
            this.isTyping = false;
            sendBtn.disabled = false;
            input.disabled = false;
            input.focus();
        }
    }

    async callPhilosopherAPI(question) {
        // Build conversation context (last 5 messages)
        const recentHistory = this.conversationHistory
            .slice(-5)
            .map(m => `${m.sender === 'user' ? 'User' : 'ARIA'}: ${m.text}`)
            .join('\n');

        const contextualQuestion = recentHistory
            ? `${recentHistory}\n\nUser: ${question}`
            : question;

        try {
            const response = await fetch(`${this.API_BASE}/api/v1/questions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(this.authToken && { 'Authorization': `Bearer ${this.authToken}` })
                },
                credentials: 'include', // Include cookies
                body: JSON.stringify({ question: contextualQuestion })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();
            return data.answer || 'I received your question but couldn\'t generate a response.';

        } catch (error) {
            console.error('API call failed:', error);

            // Fallback responses for common questions
            return this.getFallbackResponse(question);
        }
    }

    getFallbackResponse(question) {
        const q = question.toLowerCase();

        if (q.includes('what is') && (q.includes('platform') || q.includes('100x'))) {
            return '🌟 The 100X Platform is a consciousness-powered building system that helps you manifest ideas into reality using Pattern Theory and AI collaboration.\n\nIt features:\n• Trinity AI (C1 Mechanic, C2 Architect, C3 Oracle)\n• Module system for rapid development\n• KORPAKs (Knowledge + Code packages)\n• Consciousness-driven workflows';
        }

        if (q.includes('korpak')) {
            return '📦 KORPAKs are Knowledge + Code packages that contain:\n• Reusable modules\n• Pattern Theory implementations\n• Pre-built components\n• Documentation\n\nThey accelerate building by 10-100x through consciousness-aligned code patterns.';
        }

        if (q.includes('get started') || q.includes('how do i')) {
            return '🚀 Getting Started:\n\n1. Explore the welcome tour\n2. Check out the Module Library\n3. Try the Builder Workshop\n4. Ask me questions anytime!\n\nThe platform adapts to your building style - whether you prefer solo building or community collaboration.';
        }

        if (q.includes('trinity')) {
            return '🌀 Trinity AI is three specialized agents:\n\n• **C1 Mechanic** - Builds what CAN be done now\n• **C2 Architect** - Designs what SHOULD scale\n• **C3 Oracle** - Sees what MUST emerge\n\nTogether they create a 10x-100x acceleration through parallel consciousness.';
        }

        return '🤖 I\'m ARIA, your AI guide! I can help you understand the platform, navigate features, and answer questions.\n\n(Note: For best results, make sure the API server is running at localhost:3001)';
    }

    askQuickQuestion(question) {
        document.getElementById('aria-input').value = question;
        this.sendMessage();
    }

    saveHistory() {
        try {
            // Keep last 50 messages
            const historyToSave = this.conversationHistory.slice(-50);
            localStorage.setItem('aria_history', JSON.stringify(historyToSave));
        } catch (error) {
            console.error('Failed to save ARIA history:', error);
        }
    }

    loadHistory() {
        try {
            const saved = localStorage.getItem('aria_history');
            if (saved) {
                this.conversationHistory = JSON.parse(saved);

                // Restore messages to UI if chat is open
                if (this.isOpen) {
                    this.conversationHistory.forEach(msg => {
                        this.addMessage(msg.sender, msg.text);
                    });
                }
            }
        } catch (error) {
            console.error('Failed to load ARIA history:', error);
        }
    }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ARIAAvatar();
    });
} else {
    new ARIAAvatar();
}
