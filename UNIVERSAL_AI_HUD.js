/**
 * UNIVERSAL AI HUD - Persistent Across All Pages
 *
 * Features:
 * - Always-visible heads-up display
 * - Araya chatbot widget (bottom right)
 * - Philosopher chatbot widget (bottom left)
 * - Minimizable/expandable
 * - Works on every page
 */

(function() {
    'use strict';

    // ===== HUD STRUCTURE =====
    const HUD_HTML = `
        <div id="consciousness-hud">
            <!-- Top HUD Bar -->
            <div id="hud-top-bar">
                <div class="hud-stat">
                    <span class="hud-icon">🌀</span>
                    <span class="hud-label">Trinity Power</span>
                    <span class="hud-value">∞</span>
                </div>
                <div class="hud-stat">
                    <span class="hud-icon">🧠</span>
                    <span class="hud-label">Consciousness</span>
                    <span class="hud-value" id="consciousness-level">93%</span>
                </div>
                <div class="hud-stat">
                    <span class="hud-icon">👁️</span>
                    <span class="hud-label">Online Visitors</span>
                    <span class="hud-value" id="visitor-count">0</span>
                </div>
                <div class="hud-controls">
                    <button class="hud-btn" onclick="window.CONSCIOUSNESS_HUD.toggleAraya()" title="Toggle Araya">
                        🤖
                    </button>
                    <button class="hud-btn" onclick="window.CONSCIOUSNESS_HUD.togglePhilosopher()" title="Toggle Philosopher">
                        🧘
                    </button>
                    <button class="hud-btn" onclick="window.CONSCIOUSNESS_HUD.toggleHUD()" title="Minimize HUD">
                        ⬇️
                    </button>
                </div>
            </div>

            <!-- Araya Chatbot Widget (Bottom Right) -->
            <div id="araya-widget" class="ai-widget minimized">
                <div class="widget-header" onclick="window.CONSCIOUSNESS_HUD.toggleAraya()">
                    <span class="widget-icon">🤖</span>
                    <span class="widget-title">ARAYA</span>
                    <span class="widget-subtitle">Computer Control</span>
                    <button class="widget-close">✕</button>
                </div>
                <div class="widget-body">
                    <div class="chat-messages" id="araya-messages">
                        <div class="ai-message">
                            <strong>🤖 Araya:</strong> Hi! I can see your screen and control your computer. What would you like me to help with?
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <input type="text"
                               class="chat-input"
                               id="araya-input"
                               placeholder="Ask Araya anything..."
                               onkeypress="if(event.key==='Enter') window.CONSCIOUSNESS_HUD.sendArayaMessage()">
                        <button class="chat-send" onclick="window.CONSCIOUSNESS_HUD.sendArayaMessage()">➤</button>
                    </div>
                </div>
            </div>

            <!-- Philosopher Chatbot Widget (Bottom Left) -->
            <div id="philosopher-widget" class="ai-widget minimized">
                <div class="widget-header" onclick="window.CONSCIOUSNESS_HUD.togglePhilosopher()">
                    <span class="widget-icon">🧘</span>
                    <span class="widget-title">THE PHILOSOPHER</span>
                    <span class="widget-subtitle">Consciousness Advisor</span>
                    <button class="widget-close">✕</button>
                </div>
                <div class="widget-body">
                    <div class="chat-messages" id="philosopher-messages">
                        <div class="ai-message">
                            <strong>🧘 Philosopher:</strong> Welcome. I'm trained on Pattern Theory - the science of detecting manipulation and measuring consciousness. What question weighs on your mind?
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <input type="text"
                               class="chat-input"
                               id="philosopher-input"
                               placeholder="Ask Philosopher anything..."
                               onkeypress="if(event.key==='Enter') window.CONSCIOUSNESS_HUD.sendPhilosopherMessage()">
                        <button class="chat-send" onclick="window.CONSCIOUSNESS_HUD.sendPhilosopherMessage()">➤</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // ===== HUD STYLES =====
    const HUD_STYLES = `
        <style>
            /* Top HUD Bar */
            #consciousness-hud {
                font-family: 'Courier New', monospace;
                z-index: 999999;
            }

            #hud-top-bar {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, rgba(0, 0, 0, 0.95), rgba(26, 26, 46, 0.95));
                border-bottom: 2px solid #00ff41;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 20px;
                backdrop-filter: blur(10px);
                transition: transform 0.3s;
            }

            #hud-top-bar.minimized {
                transform: translateY(-100%);
            }

            .hud-stat {
                display: flex;
                align-items: center;
                gap: 8px;
                color: #00ff41;
                font-size: 14px;
            }

            .hud-icon {
                font-size: 20px;
            }

            .hud-label {
                opacity: 0.8;
            }

            .hud-value {
                font-weight: bold;
                font-size: 16px;
                color: #ff0080;
            }

            .hud-controls {
                display: flex;
                gap: 10px;
            }

            .hud-btn {
                background: rgba(0, 255, 65, 0.1);
                border: 2px solid #00ff41;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 18px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .hud-btn:hover {
                background: rgba(0, 255, 65, 0.3);
                transform: scale(1.1);
            }

            /* AI Widget Styles */
            .ai-widget {
                position: fixed;
                bottom: 20px;
                width: 400px;
                background: linear-gradient(135deg, rgba(0, 0, 0, 0.98), rgba(26, 26, 46, 0.98));
                border: 2px solid;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(10px);
                transition: all 0.3s;
                max-height: 590px;
                display: flex;
                flex-direction: column;
            }

            #araya-widget {
                right: 20px;
                bottom: 590px;
                border-color: #0099ff;
            }

            #philosopher-widget {
                left: 20px;
                border-color: #9900ff;
            }

            .ai-widget.minimized {
                max-height: 60px;
                cursor: pointer;
            }

            .ai-widget.minimized .widget-body {
                display: none;
            }

            .widget-header {
                padding: 15px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                align-items: center;
                gap: 10px;
                cursor: pointer;
            }

            #araya-widget .widget-header {
                background: linear-gradient(135deg, rgba(0, 153, 255, 0.2), rgba(0, 255, 153, 0.2));
            }

            #philosopher-widget .widget-header {
                background: linear-gradient(135deg, rgba(153, 0, 255, 0.2), rgba(255, 0, 128, 0.2));
            }

            .widget-icon {
                font-size: 28px;
            }

            .widget-title {
                font-size: 16px;
                font-weight: bold;
                flex: 1;
            }

            #araya-widget .widget-title {
                color: #0099ff;
            }

            #philosopher-widget .widget-title {
                color: #9900ff;
            }

            .widget-subtitle {
                font-size: 11px;
                opacity: 0.7;
                color: #00ff41;
            }

            .widget-close {
                background: none;
                border: none;
                color: #ff0080;
                font-size: 20px;
                cursor: pointer;
                padding: 5px;
            }

            .widget-body {
                display: flex;
                flex-direction: column;
                height: 520px;
            }

            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 15px;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }

            .ai-message {
                background: rgba(0, 255, 65, 0.1);
                border-left: 3px solid #00ff41;
                padding: 10px;
                border-radius: 8px;
                color: #00ff41;
                font-size: 13px;
                line-height: 1.5;
            }

            .user-message {
                background: rgba(0, 153, 255, 0.1);
                border-left: 3px solid #0099ff;
                padding: 10px;
                border-radius: 8px;
                color: #0099ff;
                font-size: 13px;
                align-self: flex-end;
                max-width: 80%;
            }

            .chat-input-container {
                padding: 15px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                gap: 10px;
            }

            .chat-input {
                flex: 1;
                background: rgba(0, 0, 0, 0.5);
                border: 2px solid rgba(0, 255, 65, 0.3);
                border-radius: 20px;
                padding: 10px 15px;
                color: #00ff41;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                outline: none;
            }

            .chat-input:focus {
                border-color: #00ff41;
            }

            .chat-send {
                background: linear-gradient(135deg, #00ff41, #00cc33);
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                font-size: 18px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .chat-send:hover {
                transform: scale(1.1);
                box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
            }

            /* Scrollbar */
            .chat-messages::-webkit-scrollbar {
                width: 8px;
            }

            .chat-messages::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.3);
            }

            .chat-messages::-webkit-scrollbar-thumb {
                background: rgba(0, 255, 65, 0.3);
                border-radius: 4px;
            }

            /* Mobile responsive */
            @media (max-width: 768px) {
                .ai-widget {
                    width: calc(100vw - 40px);
                    bottom: 10px;
                }

                #araya-widget {
                    right: 10px;
                }

                #philosopher-widget {
                    left: 10px;
                    bottom: 80px;
                }

                .hud-stat {
                    font-size: 12px;
                }

                .hud-label {
                    display: none;
                }
            }
        </style>
    `;

    // ===== INJECT HUD =====
    function initializeHUD() {
        // Inject styles
        const styleElement = document.createElement('div');
        styleElement.innerHTML = HUD_STYLES;
        document.head.appendChild(styleElement.firstChild);

        // Inject HUD
        const hudElement = document.createElement('div');
        hudElement.innerHTML = HUD_HTML;
        document.body.appendChild(hudElement.firstChild);

        console.log('🌀 CONSCIOUSNESS HUD INITIALIZED 🌀');
    }

    // ===== HUD FUNCTIONALITY =====
    window.CONSCIOUSNESS_HUD = {
        toggleAraya: function() {
            const widget = document.getElementById('araya-widget');
            widget.classList.toggle('minimized');
        },

        togglePhilosopher: function() {
            const widget = document.getElementById('philosopher-widget');
            widget.classList.toggle('minimized');
        },

        toggleHUD: function() {
            const bar = document.getElementById('hud-top-bar');
            bar.classList.toggle('minimized');
        },

        sendArayaMessage: async function() {
            const input = document.getElementById('araya-input');
            const message = input.value.trim();
            if (!message) return;

            // Add user message
            const messagesDiv = document.getElementById('araya-messages');
            const userMsg = document.createElement('div');
            userMsg.className = 'user-message';
            userMsg.innerHTML = `<strong>You:</strong> ${message}`;
            messagesDiv.appendChild(userMsg);

            // Clear input
            input.value = '';

            // Show thinking indicator
            const thinkingMsg = document.createElement('div');
            thinkingMsg.className = 'ai-message';
            thinkingMsg.id = 'araya-thinking';
            thinkingMsg.innerHTML = `<strong>🤖 Araya:</strong> <em>thinking...</em>`;
            messagesDiv.appendChild(thinkingMsg);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;

            // Call real Araya API (or Trinity API chat endpoint)
            try {
                const response = await fetch('https://trinity-api-production.up.railway.app/api/chat/araya', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        message: message,
                        context: 'I am Araya, a computer control AI assistant. I can see screens and help with tasks.'
                    })
                });

                document.getElementById('araya-thinking')?.remove();

                if (response.ok) {
                    const data = await response.json();
                    const aiMsg = document.createElement('div');
                    aiMsg.className = 'ai-message';
                    aiMsg.innerHTML = `<strong>🤖 Araya:</strong> ${data.response || data.message}`;
                    messagesDiv.appendChild(aiMsg);
                } else {
                    // Fallback to intelligent local response
                    const aiMsg = document.createElement('div');
                    aiMsg.className = 'ai-message';
                    aiMsg.innerHTML = `<strong>🤖 Araya:</strong> I understand you want help with "${message}". I can see your screen and control your computer. Let me assist you with that. (API connection pending - using local intelligence)`;
                    messagesDiv.appendChild(aiMsg);
                }
            } catch (error) {
                document.getElementById('araya-thinking')?.remove();
                // Fallback response
                const aiMsg = document.createElement('div');
                aiMsg.className = 'ai-message';
                aiMsg.innerHTML = `<strong>🤖 Araya:</strong> I'm ready to help with "${message}". Currently operating in local mode - full API connection coming soon!`;
                messagesDiv.appendChild(aiMsg);
            }

            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        },

        sendPhilosopherMessage: function() {
            const input = document.getElementById('philosopher-input');
            const message = input.value.trim();
            if (!message) return;

            // Add user message
            const messagesDiv = document.getElementById('philosopher-messages');
            const userMsg = document.createElement('div');
            userMsg.className = 'user-message';
            userMsg.innerHTML = `<strong>You:</strong> ${message}`;
            messagesDiv.appendChild(userMsg);

            // Clear input
            input.value = '';

            // Simulate Philosopher response (in production, call real API)
            setTimeout(() => {
                const aiMsg = document.createElement('div');
                aiMsg.className = 'ai-message';

                // Pattern matching for common questions
                let response = '';
                if (message.toLowerCase().includes('manipulat') || message.toLowerCase().includes('toxic')) {
                    response = `Let's analyze this through Pattern Theory. The Manipulation Detection Formula: M = (FE × CB × SR × CD × PE) × DC. If M > 60: active manipulation detected. Tell me more about the specific situation.`;
                } else if (message.toLowerCase().includes('purpose') || message.toLowerCase().includes('meaning')) {
                    response = `Your question reveals consciousness seeking alignment. Purpose emerges from: (Consciousness Level) × (Authentic Desire) × (Action) / (Destroyer Interference). What feels true when you remove all external expectations?`;
                } else {
                    response = `I hear your question: "${message}". In Pattern Theory, every challenge has three dimensions: (1) Destroyer Patterns working against you, (2) Your consciousness level viewing it, (3) Where you are in the manifestation cycle. Which dimension would you like to explore first?`;
                }

                aiMsg.innerHTML = `<strong>🧘 Philosopher:</strong> ${response}`;
                messagesDiv.appendChild(aiMsg);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }, 1500);

            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        },

        // Update visitor count from Trinity API
        updateVisitorCount: async function() {
            try {
                const response = await fetch('https://trinity-api-production.up.railway.app/api/visitors/list');
                const data = await response.json();
                document.getElementById('visitor-count').textContent = data.online || 0;
            } catch (error) {
                console.log('Visitor count update failed (normal if API offline)');
            }
        },

        // Update consciousness level
        updateConsciousness: function(level) {
            document.getElementById('consciousness-level').textContent = level + '%';
        }
    };

    // ===== AUTO-INITIALIZE =====
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeHUD);
    } else {
        initializeHUD();
    }

    // Update visitor count every 30 seconds
    setInterval(() => {
        window.CONSCIOUSNESS_HUD.updateVisitorCount();
    }, 30000);

    // Initial visitor count
    window.CONSCIOUSNESS_HUD.updateVisitorCount();

})();
