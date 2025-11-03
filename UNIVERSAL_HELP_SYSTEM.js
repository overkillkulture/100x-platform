// 🌀 UNIVERSAL HELP SYSTEM v1.0 🌀
// Three-tier help available on EVERY screen
// Tier 1: Context-aware walkthrough tips
// Tier 2: Araya AI help widget
// Tier 3: Emergency help button

class UniversalHelpSystem {
    constructor() {
        this.currentPage = this.detectCurrentPage();
        this.arayaApiUrl = '/.netlify/functions/araya-chat';
        this.sessionId = localStorage.getItem('help_session_id') || 'session_' + Date.now();
        this.strugglingScore = 0;
        this.pageContext = this.getPageContext();

        // Save session ID
        localStorage.setItem('help_session_id', this.sessionId);

        this.init();
    }

    detectCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('workspace')) return 'workspace';
        if (path.includes('COMMAND_CENTER')) return 'command_center';
        if (path.includes('platform')) return 'builder';
        if (path.includes('jarvis')) return 'jarvis';
        if (path.includes('gate') || path.includes('login')) return 'login';
        if (path.includes('walkthrough') || path.includes('tour')) return 'tour';
        return 'general';
    }

    getPageContext() {
        const contexts = {
            workspace: {
                title: "Workspace Help",
                tips: [
                    "💼 Click any action card to explore features",
                    "🌀 Chat with Araya for personalized guidance",
                    "🟢 See who's online and collaborate in real-time"
                ],
                quickHelp: [
                    { q: "How do I create a module?", a: "Go to Tools Hub: <a href='/tools-hub.html' style='color:#00ff00'>conciousnessrevolution.io/tools-hub.html</a>" },
                    { q: "How do I start building?", a: "Click the 'Builder Platform' card or visit /builder" },
                    { q: "Where's the chat?", a: "Click 'Chat with Araya' card to get AI assistance" }
                ]
            },
            command_center: {
                title: "Command Center Help",
                tips: [
                    "🎮 Use the HUD controls to navigate different sections",
                    "📊 Monitor system status in real-time",
                    "💬 Access team chat for collaboration"
                ],
                quickHelp: [
                    { q: "What is the Command Center?", a: "Your central hub for monitoring all platform activity" },
                    { q: "How do I use the HUD?", a: "Click sections to expand, use tabs to switch views" },
                    { q: "Can I customize this?", a: "Yes! More customization options coming soon" }
                ]
            },
            builder: {
                title: "Builder Platform Help",
                tips: [
                    "🏗️ Start by exploring existing patterns",
                    "🎯 Use consciousness tools to track your progress",
                    "🤝 Collaborate with other builders in your network"
                ],
                quickHelp: [
                    { q: "I'm new to building, where do I start?", a: "Check out the Interactive Walkthrough at /tour" },
                    { q: "What can I build here?", a: "Anything that elevates consciousness and helps others" },
                    { q: "How do I get help?", a: "Araya is always here - just ask in the chat!" }
                ]
            },
            jarvis: {
                title: "JARVIS AI Help",
                tips: [
                    "🤖 Ask Araya anything about the platform",
                    "💡 Get personalized guidance for your projects",
                    "📚 Learn about consciousness patterns"
                ],
                quickHelp: [
                    { q: "What can Araya help me with?", a: "Platform navigation, consciousness concepts, building guidance" },
                    { q: "Is my conversation private?", a: "Yes, all chats are private to your session" },
                    { q: "Can Araya help me build?", a: "Absolutely! Araya can guide you through any project" }
                ]
            },
            login: {
                title: "Login Help",
                tips: [
                    "🔐 Choose a username you'll remember",
                    "🔑 Create a secure password (at least 4 characters)",
                    "✨ Once logged in, you'll have full platform access"
                ],
                quickHelp: [
                    { q: "I'm having trouble creating an account", a: "Try the Super Simple Mode - it auto-generates everything" },
                    { q: "What if I forget my password?", a: "We'll add password recovery soon. For now, write it down!" },
                    { q: "Do I need to verify email?", a: "No email verification needed - instant access!" }
                ]
            },
            tour: {
                title: "Walkthrough Help",
                tips: [
                    "🗺️ Follow the steps to learn the platform",
                    "👀 Click 'Next' to continue through each section",
                    "💡 You can restart the tour anytime"
                ],
                quickHelp: [
                    { q: "How long is this tour?", a: "About 3-5 minutes to see all major features" },
                    { q: "Can I skip ahead?", a: "Yes! Use the step indicators to jump to any section" },
                    { q: "What if I get confused?", a: "Ask Araya for clarification - help widget is always available" }
                ]
            },
            general: {
                title: "Platform Help",
                tips: [
                    "🌀 Explore the platform at your own pace",
                    "💬 Araya is always available to help",
                    "🆘 Use the emergency button if you get stuck"
                ],
                quickHelp: [
                    { q: "Where should I start?", a: "Visit /tour for a complete walkthrough" },
                    { q: "How do I navigate?", a: "Use the navigation bar at the top of every page" },
                    { q: "Can I get live support?", a: "Yes! Click the emergency button for direct assistance" }
                ]
            }
        };

        return contexts[this.currentPage] || contexts.general;
    }

    init() {
        this.injectStyles();
        this.createArayaWidget();
        this.createEmergencyButton();
        this.startStruggleDetection();

        // Show context tips after 2 seconds
        setTimeout(() => this.showContextTips(), 2000);
    }

    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* Araya Help Widget */
            .araya-help-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 350px;
                max-height: 500px;
                background: rgba(0, 0, 0, 0.95);
                border: 2px solid rgba(0, 255, 136, 0.5);
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0, 255, 136, 0.3);
                display: none;
                flex-direction: column;
                z-index: 10000;
                backdrop-filter: blur(10px);
                animation: slideInRight 0.4s ease-out;
            }

            .araya-help-widget.show {
                display: flex;
            }

            @keyframes slideInRight {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            .araya-widget-header {
                background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 255, 136, 0.2));
                padding: 15px;
                border-bottom: 1px solid rgba(0, 255, 136, 0.3);
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-radius: 13px 13px 0 0;
            }

            .araya-widget-title {
                color: #00ffff;
                font-weight: bold;
                font-size: 16px;
            }

            .araya-widget-close {
                background: none;
                border: none;
                color: rgba(255, 255, 255, 0.7);
                font-size: 20px;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 5px;
                transition: all 0.3s;
            }

            .araya-widget-close:hover {
                background: rgba(255, 0, 136, 0.2);
                color: #ff0088;
            }

            .araya-widget-body {
                padding: 15px;
                overflow-y: auto;
                flex: 1;
                max-height: 350px;
            }

            .araya-message {
                margin-bottom: 12px;
                padding: 10px;
                background: rgba(0, 255, 136, 0.1);
                border-left: 3px solid #00ff88;
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                line-height: 1.5;
                animation: fadeIn 0.3s;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .araya-quick-help {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 10px;
            }

            .quick-help-btn {
                background: rgba(0, 255, 255, 0.1);
                border: 1px solid rgba(0, 255, 255, 0.3);
                color: #00ffff;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .quick-help-btn:hover {
                background: rgba(0, 255, 255, 0.2);
                border-color: rgba(0, 255, 255, 0.6);
                transform: translateY(-2px);
            }

            .araya-input-area {
                padding: 15px;
                border-top: 1px solid rgba(0, 255, 136, 0.3);
                display: flex;
                gap: 10px;
            }

            .araya-input {
                flex: 1;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(0, 255, 136, 0.3);
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }

            .araya-send-btn {
                background: linear-gradient(135deg, #00ffff, #00ff88);
                border: none;
                color: black;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }

            .araya-send-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 20px rgba(0, 255, 136, 0.5);
            }

            .araya-loading {
                color: rgba(255, 255, 255, 0.5);
                font-style: italic;
                padding: 10px;
                text-align: center;
            }

            /* Emergency Help Button */
            .emergency-help-btn {
                position: fixed;
                bottom: 20px;
                left: 20px;
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, rgba(255, 0, 136, 0.3), rgba(255, 0, 68, 0.3));
                border: 2px solid rgba(255, 0, 136, 0.6);
                border-radius: 50%;
                color: #ff0088;
                font-size: 28px;
                cursor: pointer;
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: pulse 2s infinite;
                box-shadow: 0 5px 20px rgba(255, 0, 136, 0.4);
                transition: all 0.3s;
            }

            .emergency-help-btn:hover {
                transform: scale(1.1);
                animation: none;
                background: linear-gradient(135deg, rgba(255, 0, 136, 0.5), rgba(255, 0, 68, 0.5));
            }

            @keyframes pulse {
                0%, 100% {
                    box-shadow: 0 5px 20px rgba(255, 0, 136, 0.4);
                    transform: scale(1);
                }
                50% {
                    box-shadow: 0 5px 30px rgba(255, 0, 136, 0.8);
                    transform: scale(1.05);
                }
            }

            /* Emergency Modal */
            .emergency-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.9);
                z-index: 10001;
                display: none;
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.3s;
            }

            .emergency-modal.show {
                display: flex;
            }

            .emergency-content {
                background: rgba(0, 20, 40, 0.95);
                border: 2px solid rgba(255, 0, 136, 0.5);
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 90%;
                box-shadow: 0 20px 60px rgba(255, 0, 136, 0.5);
            }

            .emergency-title {
                font-size: 28px;
                color: #ff0088;
                text-align: center;
                margin-bottom: 10px;
            }

            .emergency-subtitle {
                color: rgba(255, 255, 255, 0.7);
                text-align: center;
                margin-bottom: 30px;
            }

            .help-options {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }

            .help-option {
                background: rgba(0, 255, 136, 0.1);
                border: 2px solid rgba(0, 255, 136, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s;
                color: white;
            }

            .help-option:hover {
                background: rgba(0, 255, 136, 0.2);
                border-color: rgba(0, 255, 136, 0.6);
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
            }

            .help-option-icon {
                font-size: 36px;
                margin-bottom: 10px;
            }

            .help-option-text {
                font-size: 14px;
                font-weight: bold;
            }

            .emergency-close-btn {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                cursor: pointer;
                display: block;
                margin: 0 auto;
                transition: all 0.3s;
            }

            .emergency-close-btn:hover {
                background: rgba(255, 255, 255, 0.2);
            }

            /* Context Tips */
            .context-tips {
                position: fixed;
                top: 80px;
                right: 20px;
                background: rgba(0, 255, 255, 0.1);
                border: 2px solid rgba(0, 255, 255, 0.4);
                border-radius: 12px;
                padding: 15px 20px;
                max-width: 350px;
                z-index: 9999;
                animation: slideInRight 0.5s ease-out;
                backdrop-filter: blur(10px);
            }

            .context-tips-title {
                color: #00ffff;
                font-weight: bold;
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .context-tips-close {
                background: none;
                border: none;
                color: rgba(255, 255, 255, 0.5);
                cursor: pointer;
                font-size: 18px;
            }

            .context-tips-list {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                line-height: 1.8;
            }

            .context-tips-list div {
                margin-bottom: 8px;
            }

            /* Mobile Responsive */
            @media (max-width: 768px) {
                .araya-help-widget {
                    width: 90%;
                    right: 5%;
                    bottom: 10px;
                }

                .emergency-help-btn {
                    width: 50px;
                    height: 50px;
                    font-size: 24px;
                    bottom: 15px;
                    left: 15px;
                }

                .context-tips {
                    top: 70px;
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }

                .help-options {
                    grid-template-columns: 1fr;
                }
            }
        `;
        document.head.appendChild(style);
    }

    createArayaWidget() {
        const widget = document.createElement('div');
        widget.className = 'araya-help-widget';
        widget.id = 'arayaHelpWidget';

        widget.innerHTML = `
            <div class="araya-widget-header">
                <div class="araya-widget-title">🌀 ${this.pageContext.title}</div>
                <button class="araya-widget-close" onclick="universalHelp.hideArayaWidget()">✕</button>
            </div>
            <div class="araya-widget-body" id="arayaMessages">
                <div class="araya-message">
                    👋 Hi! I'm Araya, your AI guide. I can help you with anything on this page.
                </div>
                <div class="araya-quick-help">
                    ${this.pageContext.quickHelp.map(item =>
                        `<button class="quick-help-btn" onclick="universalHelp.askQuickQuestion('${item.q.replace(/'/g, "\\'")}')">${item.q}</button>`
                    ).join('')}
                </div>
            </div>
            <div class="araya-input-area">
                <input type="text" class="araya-input" id="arayaInput" placeholder="Ask me anything..." />
                <button class="araya-send-btn" onclick="universalHelp.sendToAraya()">Send</button>
            </div>
        `;

        document.body.appendChild(widget);

        // Enter key support
        document.getElementById('arayaInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendToAraya();
        });
    }

    createEmergencyButton() {
        const btn = document.createElement('button');
        btn.className = 'emergency-help-btn';
        btn.innerHTML = '🆘';
        btn.onclick = () => this.showEmergencyModal();
        document.body.appendChild(btn);

        // Create emergency modal
        const modal = document.createElement('div');
        modal.className = 'emergency-modal';
        modal.id = 'emergencyModal';

        modal.innerHTML = `
            <div class="emergency-content">
                <div class="emergency-title">🆘 Emergency Help</div>
                <div class="emergency-subtitle">Choose how you'd like to get help:</div>

                <div class="help-options">
                    <div class="help-option" onclick="universalHelp.openFullChat()">
                        <div class="help-option-icon">💬</div>
                        <div class="help-option-text">Chat with Araya</div>
                    </div>

                    <div class="help-option" onclick="universalHelp.openWalkthrough()">
                        <div class="help-option-icon">🗺️</div>
                        <div class="help-option-text">Interactive Tour</div>
                    </div>

                    <div class="help-option" onclick="universalHelp.openVideoTutorial()">
                        <div class="help-option-icon">📹</div>
                        <div class="help-option-text">Video Tutorial</div>
                    </div>

                    <div class="help-option" onclick="universalHelp.contactSupport()">
                        <div class="help-option-icon">📞</div>
                        <div class="help-option-text">Live Support</div>
                    </div>
                </div>

                <button class="emergency-close-btn" onclick="universalHelp.hideEmergencyModal()">Close</button>
            </div>
        `;

        document.body.appendChild(modal);

        // Close on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.hideEmergencyModal();
        });
    }

    showContextTips() {
        // Don't show on tour page (would be redundant)
        if (this.currentPage === 'tour') return;

        const tips = document.createElement('div');
        tips.className = 'context-tips';
        tips.id = 'contextTips';

        tips.innerHTML = `
            <div class="context-tips-title">
                💡 Quick Tips
                <button class="context-tips-close" onclick="universalHelp.hideContextTips()">✕</button>
            </div>
            <div class="context-tips-list">
                ${this.pageContext.tips.map(tip => `<div>${tip}</div>`).join('')}
            </div>
        `;

        document.body.appendChild(tips);

        // Auto-hide after 10 seconds
        setTimeout(() => this.hideContextTips(), 10000);
    }

    hideContextTips() {
        const tips = document.getElementById('contextTips');
        if (tips) tips.remove();
    }

    showArayaWidget() {
        document.getElementById('arayaHelpWidget').classList.add('show');
    }

    hideArayaWidget() {
        document.getElementById('arayaHelpWidget').classList.remove('show');
    }

    async sendToAraya() {
        const input = document.getElementById('arayaInput');
        const message = input.value.trim();

        if (!message) return;

        // Clear input
        input.value = '';

        // Add user message to chat
        this.addMessage(`You: ${message}`, 'user');

        // Show loading
        this.addMessage('Araya is thinking...', 'loading');

        // 🔥 DETECT EDITING REQUESTS!
        const lowerMsg = message.toLowerCase();
        const isEditingRequest = lowerMsg.includes('change') || lowerMsg.includes('fix') ||
                                 lowerMsg.includes('make') || lowerMsg.includes('button') ||
                                 lowerMsg.includes('color') || lowerMsg.includes('text') ||
                                 lowerMsg.includes('bigger') || lowerMsg.includes('smaller') ||
                                 lowerMsg.includes('too small') || lowerMsg.includes('too big') ||
                                 lowerMsg.includes('layout') || lowerMsg.includes('sizing');

        // Route to EDIT endpoint if editing, CHAT endpoint otherwise
        const apiUrl = isEditingRequest ? '/.netlify/functions/araya-edit' : this.arayaApiUrl;

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: `[Page: ${this.currentPage}] ${message}`,
                    user_feedback: isEditingRequest ? message : null,
                    session_id: this.sessionId
                })
            });

            const data = await response.json();

            // Remove loading message
            const loadingMsg = document.querySelector('.araya-loading');
            if (loadingMsg) loadingMsg.remove();

            // Add Araya's response
            this.addMessage(`🌀 Araya: ${data.response}`, 'araya');

            // If there's a PROPOSAL, show it with APPROVE/REJECT buttons!
            if (data.proposal) {
                this.showProposal(data.proposal);
            }

        } catch (error) {
            console.error('Araya error:', error);
            const loadingMsg = document.querySelector('.araya-loading');
            if (loadingMsg) loadingMsg.remove();
            this.addMessage('⚠️ Connection error. Please try again.', 'error');
        }
    }


    showProposal(proposal) {
        const messagesDiv = document.getElementById('arayaMessages');
        const proposalDiv = document.createElement('div');
        proposalDiv.className = 'proposal-box';
        proposalDiv.innerHTML = `
            <div style="background: rgba(0,255,136,0.1); border: 2px solid #00ff88; border-radius: 12px; padding: 15px; margin: 10px 0;">
                <div style="font-size: 16px; font-weight: bold; color: #00ff88; margin-bottom: 10px;">
                    📋 PROPOSAL: ${proposal.title || proposal.description}
                </div>
                <div style="color: #e8e8e8; margin-bottom: 10px;">
                    ${proposal.description || ''}
                </div>
                <div style="color: #aaa; font-size: 14px; margin-bottom: 10px;">
                    File: ${proposal.changes ? proposal.changes[0].file : proposal.file || 'Unknown'}
                </div>
                <div style="color: ${proposal.risk_level === 'LOW' ? '#00ff88' : '#ffaa00'}; font-size: 14px; margin-bottom: 15px;">
                    Risk: ${proposal.risk_level || proposal.risk || 'UNKNOWN'}
                </div>
                <div style="display: flex; gap: 10px;">
                    <button onclick="universalHelp.approveProposal()" style="background: #00ff88; color: #0a0a0a; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold;">
                        ✅ APPROVE
                    </button>
                    <button onclick="universalHelp.rejectProposal()" style="background: #ff4444; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold;">
                        ❌ REJECT
                    </button>
                </div>
            </div>
        `;
        messagesDiv.appendChild(proposalDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        // Store proposal for approval
        this.currentProposal = proposal;
    }

    async approveProposal() {
        if (!this.currentProposal) return;

        this.addMessage('🔥 EXECUTING CHANGES...', 'loading');

        try {
            // 🔥 MORTAL KOMBAT FINISHER - Actually execute the proposal!
            // Extract file changes from proposal
            const changes = this.currentProposal.changes;

            // Call local file writer service for each file
            const results = [];
            for (const change of changes) {
                try {
                    const response = await fetch('http://localhost:8889/write-file', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            file: change.file,
                            content: change.new_content
                        })
                    });

                    const result = await response.json();
                    results.push(result);

                    console.log('✅ File write result:', result);
                } catch (error) {
                    console.error('❌ File write error:', error);
                    results.push({ success: false, file: change.file, error: error.message });
                }
            }

            const result = { success: results.every(r => r.success), results };

            // Remove loading message
            const loadingMsg = document.querySelector('.araya-loading');
            if (loadingMsg) loadingMsg.remove();

            if (result.success) {
                this.addMessage('✅ FATALITY! Changes written and deployed!', 'success');

                if (result.results) {
                    result.results.forEach(r => {
                        if (r.success) {
                            this.addMessage(`   ✓ ${r.file} - ${r.bytes_written} bytes written`, 'success');
                            if (r.deploy_triggered) {
                                this.addMessage(`   🚀 Netlify deploy triggered!`, 'success');
                            }
                        } else {
                            this.addMessage(`   ✗ ${r.file} - ${r.error}`, 'error');
                        }
                    });
                }

                // Clear proposal
                this.currentProposal = null;

                // Show deployment status
                setTimeout(() => {
                    this.addMessage('🔥 Changes will be live in ~30 seconds! Refresh to see updates.', 'araya');
                }, 1000);
            } else {
                this.addMessage(`❌ Execution failed: ${result.message || result.error}`, 'error');
            }

        } catch (error) {
            const loadingMsg = document.querySelector('.araya-loading');
            if (loadingMsg) loadingMsg.remove();

            this.addMessage(`❌ Error executing changes: ${error.message}`, 'error');
            console.error('Execution error:', error);
        }
    }

    rejectProposal() {
        this.addMessage('❌ Proposal rejected. No changes were made.', 'araya');
        this.currentProposal = null;
    }

    askQuickQuestion(question) {
        const input = document.getElementById('arayaInput');
        input.value = question;
        this.sendToAraya();
    }

    addMessage(text, type = 'araya') {
        const messagesDiv = document.getElementById('arayaMessages');
        const msg = document.createElement('div');

        if (type === 'loading') {
            msg.className = 'araya-loading';
        } else {
            msg.className = 'araya-message';
        }

        msg.textContent = text;
        messagesDiv.appendChild(msg);

        // Scroll to bottom
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    startStruggleDetection() {
        // Track user struggling (errors, repeated actions, time on page)
        let timeOnPage = 0;
        const checkInterval = setInterval(() => {
            timeOnPage += 5;

            // Auto-show Araya after 30 seconds if not already shown
            if (timeOnPage >= 30 && !document.getElementById('arayaHelpWidget').classList.contains('show')) {
                this.showArayaWidget();
                this.addMessage('I noticed you\'ve been here a while. Need any help?', 'araya');
                clearInterval(checkInterval);
            }
        }, 5000);

        // Listen for errors
        window.addEventListener('error', () => {
            this.strugglingScore++;
            if (this.strugglingScore >= 2 && !document.getElementById('arayaHelpWidget').classList.contains('show')) {
                this.showArayaWidget();
                this.addMessage('I detected you might be having trouble. How can I help?', 'araya');
            }
        });
    }

    showEmergencyModal() {
        document.getElementById('emergencyModal').classList.add('show');
    }

    hideEmergencyModal() {
        document.getElementById('emergencyModal').classList.remove('show');
    }

    // Emergency help actions
    openFullChat() {
        this.showArayaWidget();  // Open Platform Help widget (the one that creates proposals!)
        this.hideEmergencyModal();
    }

    openWalkthrough() {
        window.location.href = '/tour';
    }

    openVideoTutorial() {
        alert('📹 Video tutorials coming soon! For now, try the Interactive Tour or chat with Araya.');
        this.hideEmergencyModal();
        this.showArayaWidget();
    }

    contactSupport() {
        alert('📞 Live Support:\n\nEmail: support@conciousnessrevolution.io\nOr chat with Araya right now for instant help!');
        this.hideEmergencyModal();
        this.showArayaWidget();
    }
}

// Initialize on page load
let universalHelp;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        universalHelp = new UniversalHelpSystem();
    });
} else {
    universalHelp = new UniversalHelpSystem();
}

// Export for external access
window.universalHelp = universalHelp;
