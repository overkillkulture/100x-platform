/**
 * DEBUG ASSISTANT WIDGET
 *
 * Public-facing Claude instance for debugging help only
 * Boundaries:
 * - ✅ Technical help
 * - ✅ Bug reports
 * - ❌ Counseling → "That's billable"
 * - ❌ Abuse → "Bug off"
 */

const DebugAssistant = {
    enabled: true,
    config: {
        apiEndpoint: '/api/debug-assistant',
        maxMessages: 10,
        cooldown: 30000, // 30 seconds between messages
        welcomeMessage: "👋 Debug Assistant here. I help with technical issues on this site. Got a bug? Ask me. Need counseling? That's billable - contact us."
    },

    data: {
        messages: [],
        lastMessageTime: 0,
        messageCount: 0,
        sessionId: null
    },

    /**
     * Initialize debug assistant
     */
    init() {
        if (!this.enabled) return;

        console.log('%c🤖 Debug Assistant: Available', 'color: #2196F3; font-weight: bold;');
        console.log('Click the blue button (bottom left) if you need technical help.');

        this.data.sessionId = `debug_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        this.createWidget();
        this.createToggleButton();
    },

    /**
     * Create chat widget
     */
    createWidget() {
        const widget = document.createElement('div');
        widget.id = 'debug-assistant-widget';
        widget.className = 'debug-assistant-hidden';
        widget.innerHTML = `
            <style>
                #debug-assistant-widget {
                    position: fixed;
                    bottom: 80px;
                    left: 20px;
                    width: 350px;
                    height: 500px;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                    display: flex;
                    flex-direction: column;
                    z-index: 99998;
                    font-family: 'Segoe UI', sans-serif;
                    transition: transform 0.3s ease, opacity 0.3s ease;
                }

                #debug-assistant-widget.debug-assistant-hidden {
                    transform: translateY(20px);
                    opacity: 0;
                    pointer-events: none;
                }

                .debug-assistant-header {
                    background: linear-gradient(135deg, #2196F3, #1976D2);
                    color: white;
                    padding: 15px;
                    border-radius: 15px 15px 0 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .debug-assistant-title {
                    font-weight: bold;
                    font-size: 1.1rem;
                }

                .debug-assistant-close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.5rem;
                    cursor: pointer;
                    opacity: 0.8;
                }

                .debug-assistant-close:hover {
                    opacity: 1;
                }

                .debug-assistant-messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 15px;
                    background: #f5f5f5;
                }

                .debug-assistant-message {
                    margin-bottom: 15px;
                    padding: 10px;
                    border-radius: 10px;
                    max-width: 80%;
                    line-height: 1.4;
                    font-size: 0.9rem;
                }

                .debug-assistant-message.user {
                    background: #2196F3;
                    color: white;
                    margin-left: auto;
                    margin-right: 0;
                }

                .debug-assistant-message.assistant {
                    background: white;
                    color: #333;
                    border: 1px solid #ddd;
                }

                .debug-assistant-input-area {
                    padding: 15px;
                    background: white;
                    border-top: 1px solid #ddd;
                    border-radius: 0 0 15px 15px;
                }

                .debug-assistant-input {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    font-size: 0.9rem;
                    resize: none;
                    font-family: inherit;
                }

                .debug-assistant-send {
                    width: 100%;
                    margin-top: 10px;
                    padding: 10px;
                    background: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: bold;
                    font-size: 0.9rem;
                }

                .debug-assistant-send:hover {
                    background: #1976D2;
                }

                .debug-assistant-send:disabled {
                    background: #ccc;
                    cursor: not-allowed;
                }

                .debug-assistant-limit {
                    font-size: 0.75rem;
                    color: #999;
                    margin-top: 5px;
                    text-align: center;
                }

                @media (max-width: 768px) {
                    #debug-assistant-widget {
                        left: 10px;
                        right: 10px;
                        width: auto;
                        bottom: 70px;
                    }
                }
            </style>

            <div class="debug-assistant-header">
                <div class="debug-assistant-title">🤖 Debug Assistant</div>
                <button class="debug-assistant-close" onclick="DebugAssistant.hideWidget()">×</button>
            </div>

            <div class="debug-assistant-messages" id="debug-messages">
                <div class="debug-assistant-message assistant">
                    ${this.config.welcomeMessage}
                </div>
            </div>

            <div class="debug-assistant-input-area">
                <textarea
                    id="debug-input"
                    class="debug-assistant-input"
                    placeholder="Describe your technical issue..."
                    rows="2"
                    maxlength="500"
                ></textarea>
                <button class="debug-assistant-send" onclick="DebugAssistant.sendMessage()">
                    Send
                </button>
                <div class="debug-assistant-limit" id="debug-limit">
                    ${this.data.messageCount}/${this.config.maxMessages} messages used
                </div>
            </div>
        `;

        document.body.appendChild(widget);

        // Add enter key handler
        document.getElementById('debug-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    },

    /**
     * Create toggle button
     */
    createToggleButton() {
        const button = document.createElement('button');
        button.id = 'debug-assistant-toggle';
        button.innerHTML = `
            <style>
                #debug-assistant-toggle {
                    position: fixed;
                    bottom: 20px;
                    left: 20px;
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #2196F3, #1976D2);
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 1.5rem;
                    box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
                    z-index: 99999;
                    transition: transform 0.3s ease;
                }

                #debug-assistant-toggle:hover {
                    transform: scale(1.1);
                }

                #debug-assistant-toggle.active {
                    background: linear-gradient(135deg, #f44336, #d32f2f);
                }
            </style>
            🤖
        `;

        button.onclick = () => this.toggleWidget();
        document.body.appendChild(button);
    },

    /**
     * Toggle widget visibility
     */
    toggleWidget() {
        const widget = document.getElementById('debug-assistant-widget');
        const button = document.getElementById('debug-assistant-toggle');

        if (widget.classList.contains('debug-assistant-hidden')) {
            this.showWidget();
        } else {
            this.hideWidget();
        }
    },

    /**
     * Show widget
     */
    showWidget() {
        const widget = document.getElementById('debug-assistant-widget');
        const button = document.getElementById('debug-assistant-toggle');

        widget.classList.remove('debug-assistant-hidden');
        button.classList.add('active');

        document.getElementById('debug-input').focus();
    },

    /**
     * Hide widget
     */
    hideWidget() {
        const widget = document.getElementById('debug-assistant-widget');
        const button = document.getElementById('debug-assistant-toggle');

        widget.classList.add('debug-assistant-hidden');
        button.classList.remove('active');
    },

    /**
     * Send message
     */
    async sendMessage() {
        const input = document.getElementById('debug-input');
        const message = input.value.trim();

        if (!message) return;

        // Check message count
        if (this.data.messageCount >= this.config.maxMessages) {
            this.addMessage('assistant', "You've reached your message limit for this session. Reload the page to continue or contact us for extended support.");
            return;
        }

        // Check cooldown
        const now = Date.now();
        if (now - this.data.lastMessageTime < this.config.cooldown) {
            const waitTime = Math.ceil((this.config.cooldown - (now - this.data.lastMessageTime)) / 1000);
            this.addMessage('assistant', `Please wait ${waitTime} seconds before sending another message.`);
            return;
        }

        // Add user message
        this.addMessage('user', message);
        input.value = '';

        // Update state
        this.data.messageCount++;
        this.data.lastMessageTime = now;
        this.updateLimit();

        // Show typing indicator
        this.showTyping();

        // Send to API (for now, use mock response)
        try {
            const response = await this.callAPI(message);
            this.hideTyping();
            this.addMessage('assistant', response);
        } catch (error) {
            this.hideTyping();
            this.addMessage('assistant', 'Sorry, I encountered an error. Please try again or contact support.');
            console.error('Debug Assistant error:', error);
        }
    },

    /**
     * Call API (mock for now - will connect to real API)
     */
    async callAPI(message) {
        // For now, return mock responses based on patterns
        // TODO: Replace with actual Claude API call

        const lowerMessage = message.toLowerCase();

        // Pattern matching for common issues
        if (lowerMessage.includes('counsel') || lowerMessage.includes('personal') || lowerMessage.includes('advice')) {
            return "I'm a debug assistant, not a counselor. If you need personal advice, that's a billable service - contact us at consciousness@overkore.com.";
        }

        if (lowerMessage.includes('fuck') || lowerMessage.includes('shit') || lowerMessage.includes('damn')) {
            return "Hey, bug off with that attitude. I'm here to help with technical issues, not tolerate abuse.";
        }

        if (lowerMessage.includes('bug') || lowerMessage.includes('error') || lowerMessage.includes('broken')) {
            return "I can help with that! Can you describe:\n1. What were you trying to do?\n2. What happened instead?\n3. Any error messages you saw?\n\nThe more details, the better I can help.";
        }

        if (lowerMessage.includes('how') && (lowerMessage.includes('use') || lowerMessage.includes('work'))) {
            return "I can explain how features work! Which specific tool or feature do you need help with? For example:\n- 3-Minute Boost protocols\n- Badge system\n- Reality Impact dashboard\n- Something else?";
        }

        // Default helpful response
        return "I'm here to help with technical issues on this site. Can you describe the problem you're experiencing? Include:\n- What you were trying to do\n- What happened\n- Any error messages\n\nFor non-technical help, contact consciousness@overkore.com.";
    },

    /**
     * Add message to chat
     */
    addMessage(role, content) {
        const messagesDiv = document.getElementById('debug-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `debug-assistant-message ${role}`;
        messageDiv.textContent = content;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        // Store in data
        this.data.messages.push({ role, content, timestamp: Date.now() });
    },

    /**
     * Show typing indicator
     */
    showTyping() {
        const messagesDiv = document.getElementById('debug-messages');
        const typing = document.createElement('div');
        typing.id = 'debug-typing';
        typing.className = 'debug-assistant-message assistant';
        typing.textContent = '...';
        messagesDiv.appendChild(typing);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    },

    /**
     * Hide typing indicator
     */
    hideTyping() {
        const typing = document.getElementById('debug-typing');
        if (typing) typing.remove();
    },

    /**
     * Update message limit display
     */
    updateLimit() {
        const limitDiv = document.getElementById('debug-limit');
        limitDiv.textContent = `${this.data.messageCount}/${this.config.maxMessages} messages used`;
    }
};

// Make globally accessible
window.DebugAssistant = DebugAssistant;

// Auto-init
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => DebugAssistant.init());
} else {
    DebugAssistant.init();
}

console.log('%c🤖 Debug Assistant Loaded', 'color: #2196F3; font-weight: bold;');
console.log('Need technical help? Click the blue button (bottom left).');
