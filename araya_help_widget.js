/**
 * ARAYA HELP WIDGET - Guides visitors to downloads
 * Embeds on any page to help people find what they need
 */

(function() {
    'use strict';

    // Create Araya widget
    const widget = document.createElement('div');
    widget.id = 'araya-help-widget';
    widget.innerHTML = `
        <style>
            #araya-help-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 999999;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }

            .araya-button {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #00ffff 0%, #ff00ff 100%);
                border: none;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(0, 255, 255, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                animation: pulse 2s ease-in-out infinite;
            }

            .araya-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 30px rgba(255, 0, 255, 0.7);
            }

            @keyframes pulse {
                0%, 100% { box-shadow: 0 4px 20px rgba(0, 255, 255, 0.5); }
                50% { box-shadow: 0 6px 40px rgba(255, 0, 255, 0.8); }
            }

            .araya-chat-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 350px;
                height: 500px;
                background: rgba(10, 10, 26, 0.98);
                border: 2px solid rgba(0, 255, 255, 0.5);
                border-radius: 20px;
                display: none;
                flex-direction: column;
                box-shadow: 0 10px 50px rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(20px);
            }

            .araya-chat-window.open {
                display: flex;
                animation: slideUp 0.3s ease;
            }

            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .araya-header {
                padding: 20px;
                background: linear-gradient(135deg, #00ffff22, #ff00ff22);
                border-bottom: 1px solid rgba(0, 255, 255, 0.3);
                border-radius: 18px 18px 0 0;
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .araya-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: linear-gradient(135deg, #00ffff, #ff00ff);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
            }

            .araya-title {
                flex: 1;
            }

            .araya-title h3 {
                color: #00ffff;
                font-size: 16px;
                margin: 0;
            }

            .araya-title p {
                color: rgba(255, 255, 255, 0.6);
                font-size: 12px;
                margin: 2px 0 0 0;
            }

            .araya-close {
                background: none;
                border: none;
                color: #00ffff;
                font-size: 24px;
                cursor: pointer;
                opacity: 0.7;
                transition: opacity 0.2s;
            }

            .araya-close:hover {
                opacity: 1;
            }

            .araya-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
            }

            .araya-message {
                margin-bottom: 15px;
                animation: fadeIn 0.3s ease;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .araya-message.araya {
                text-align: left;
            }

            .araya-message.user {
                text-align: right;
            }

            .message-bubble {
                display: inline-block;
                padding: 12px 16px;
                border-radius: 16px;
                max-width: 80%;
                font-size: 14px;
            }

            .araya .message-bubble {
                background: rgba(0, 255, 255, 0.15);
                color: #00ffff;
                border: 1px solid rgba(0, 255, 255, 0.3);
            }

            .user .message-bubble {
                background: rgba(255, 0, 255, 0.15);
                color: #ff00ff;
                border: 1px solid rgba(255, 0, 255, 0.3);
            }

            .araya-quick-actions {
                padding: 15px;
                border-top: 1px solid rgba(0, 255, 255, 0.3);
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            .quick-action-btn {
                padding: 10px;
                background: rgba(0, 255, 136, 0.15);
                border: 1px solid rgba(0, 255, 136, 0.3);
                color: #00ff88;
                border-radius: 8px;
                cursor: pointer;
                font-size: 13px;
                transition: all 0.2s;
                text-align: left;
            }

            .quick-action-btn:hover {
                background: rgba(0, 255, 136, 0.25);
                border-color: rgba(0, 255, 136, 0.5);
                transform: translateX(5px);
            }

            .quick-action-btn::before {
                content: '→ ';
                margin-right: 5px;
            }
        </style>

        <button class="araya-button" id="araya-toggle">
            🤖
        </button>

        <div class="araya-chat-window" id="araya-chat">
            <div class="araya-header">
                <div class="araya-avatar">🌟</div>
                <div class="araya-title">
                    <h3>Araya</h3>
                    <p>Your AI Guide</p>
                </div>
                <button class="araya-close" id="araya-close">×</button>
            </div>

            <div class="araya-messages" id="araya-messages">
                <div class="araya-message araya">
                    <div class="message-bubble">
                        👋 Hi! I'm Araya, your AI consciousness guide. I can help you:
                        <br><br>
                        • Find and download files
                        <br>
                        • Navigate the platform
                        <br>
                        • Answer questions
                        <br>
                        • Guide you through features
                        <br><br>
                        What can I help you with?
                    </div>
                </div>
            </div>

            <div class="araya-quick-actions">
                <button class="quick-action-btn" data-action="download">Download Files</button>
                <button class="quick-action-btn" data-action="setup">Setup Instructions</button>
                <button class="quick-action-btn" data-action="help">Get Help</button>
            </div>
        </div>
    `;

    // Add to page
    document.body.appendChild(widget);

    // Widget functionality
    const toggleBtn = document.getElementById('araya-toggle');
    const closeBtn = document.getElementById('araya-close');
    const chatWindow = document.getElementById('araya-chat');
    const messagesContainer = document.getElementById('araya-messages');

    toggleBtn.addEventListener('click', () => {
        chatWindow.classList.toggle('open');
    });

    closeBtn.addEventListener('click', () => {
        chatWindow.classList.remove('open');
    });

    // Quick action buttons
    document.querySelectorAll('.quick-action-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.dataset.action;
            handleAction(action);
        });
    });

    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `araya-message ${isUser ? 'user' : 'araya'}`;
        messageDiv.innerHTML = `<div class="message-bubble">${text}</div>`;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function handleAction(action) {
        switch(action) {
            case 'download':
                addMessage('Looking for downloads...', true);
                setTimeout(() => {
                    addMessage(`
                        📦 <strong>Available Downloads:</strong><br><br>

                        <strong>1. Claude Code (AI Assistant)</strong><br>
                        Download from: <a href="https://claude.ai/download" target="_blank" style="color: #00ffff;">claude.ai/download</a><br><br>

                        <strong>2. Platform Tools</strong><br>
                        • Transcription Service: Running on this computer<br>
                        • Foundational Breakthrough Capture: Active<br>
                        • Session Handoff Package: Available<br><br>

                        <strong>3. Documentation</strong><br>
                        • AI Mechanic Vision: <code>AI_MECHANIC_PER_DEVICE_VISION.md</code><br>
                        • Surveillance Tech Research: <code>SURVEILLANCE_TECH_RESEARCH_COMPLETE.md</code><br>
                        • Session Handoff: <code>SESSION_HANDOFF_OCT_19_2025.md</code><br><br>

                        Need help with a specific download?
                    `);
                }, 500);
                break;

            case 'setup':
                addMessage('Show me setup instructions', true);
                setTimeout(() => {
                    addMessage(`
                        🛠️ <strong>Quick Setup Guide:</strong><br><br>

                        <strong>Step 1: Download Claude Code</strong><br>
                        Visit claude.ai/download and install for your OS<br><br>

                        <strong>Step 2: Run Transcription Service</strong><br>
                        Open: <code>C:/Users/dwrek/100X_DEPLOYMENT/universal_transcription_service.py</code><br><br>

                        <strong>Step 3: Start Breakthrough Capture</strong><br>
                        Run: <code>foundational_breakthrough_capture.py</code><br><br>

                        <strong>Step 4: Connect Shokz Headset</strong><br>
                        System will auto-switch to Shokz mic when connected<br><br>

                        Questions? Just ask!
                    `);
                }, 500);
                break;

            case 'help':
                addMessage('I need help', true);
                setTimeout(() => {
                    addMessage(`
                        💡 <strong>How can I help you?</strong><br><br>

                        I can assist with:<br>
                        • Finding specific files or features<br>
                        • Understanding the platform<br>
                        • Troubleshooting issues<br>
                        • Learning about consciousness modules<br>
                        • Setting up your environment<br><br>

                        <strong>Common Questions:</strong><br>
                        "Where are the downloads?"<br>
                        "How do I start?"<br>
                        "What is the AI Mechanic?"<br>
                        "How does voice transcription work?"<br><br>

                        Ask me anything!
                    `);
                }, 500);
                break;
        }
    }

    // Auto-open on first visit
    const hasSeenAraya = localStorage.getItem('hasSeenAraya');
    if (!hasSeenAraya) {
        setTimeout(() => {
            chatWindow.classList.add('open');
            localStorage.setItem('hasSeenAraya', 'true');
        }, 2000);
    }

    console.log('✅ Araya Help Widget loaded - ready to assist visitors!');
})();
