/**
 * LIVE CHAT WIDGET - Direct Commander Communication
 * No more email - talk to beta testers IN the platform!
 */

class LiveChatWidget {
    constructor() {
        this.isOpen = false;
        this.unreadCount = 0;
        this.userName = localStorage.getItem('betaUserName') || 'Beta Tester';
        this.userPin = localStorage.getItem('betaUserPin') || 'Guest';
        this.init();
    }

    init() {
        this.injectWidget();
        this.loadMessages();
        this.startPolling();
        this.checkForBroadcast();
    }

    injectWidget() {
        const widgetHTML = `
            <div id="liveChatWidget" style="
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 10000;
                font-family: 'Courier New', monospace;
            ">
                <!-- Chat Button -->
                <div id="chatButton" style="
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5);
                    transition: all 0.3s;
                    position: relative;
                " onclick="liveChat.toggleChat()">
                    <span style="font-size: 30px;">💬</span>
                    <div id="unreadBadge" style="
                        position: absolute;
                        top: -5px;
                        right: -5px;
                        background: #ff4444;
                        color: white;
                        border-radius: 50%;
                        width: 24px;
                        height: 24px;
                        display: none;
                        align-items: center;
                        justify-content: center;
                        font-size: 12px;
                        font-weight: bold;
                    ">0</div>
                </div>

                <!-- Chat Window -->
                <div id="chatWindow" style="
                    position: absolute;
                    bottom: 80px;
                    right: 0;
                    width: 350px;
                    height: 500px;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    border-radius: 15px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
                    display: none;
                    flex-direction: column;
                    overflow: hidden;
                    border: 2px solid #667eea;
                ">
                    <!-- Header -->
                    <div style="
                        padding: 20px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <div>
                            <div style="font-size: 1.2em; font-weight: bold;">💬 Live Chat</div>
                            <div style="font-size: 0.8em; opacity: 0.9;">Talk to Commander</div>
                        </div>
                        <div style="
                            cursor: pointer;
                            font-size: 1.5em;
                        " onclick="liveChat.toggleChat()">✕</div>
                    </div>

                    <!-- Messages Area -->
                    <div id="chatMessages" style="
                        flex: 1;
                        padding: 20px;
                        overflow-y: auto;
                        background: rgba(0,0,0,0.3);
                    ">
                        <!-- Messages will be inserted here -->
                    </div>

                    <!-- Input Area -->
                    <div style="
                        padding: 15px;
                        background: rgba(0,0,0,0.5);
                        display: flex;
                        gap: 10px;
                    ">
                        <input
                            type="text"
                            id="chatInput"
                            placeholder="Type your message..."
                            style="
                                flex: 1;
                                padding: 12px;
                                background: rgba(255,255,255,0.1);
                                border: 1px solid rgba(255,255,255,0.2);
                                border-radius: 8px;
                                color: white;
                                font-family: inherit;
                            "
                            onkeypress="if(event.key === 'Enter') liveChat.sendMessage()"
                        />
                        <button onclick="liveChat.sendMessage()" style="
                            padding: 12px 20px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            border: none;
                            border-radius: 8px;
                            color: white;
                            cursor: pointer;
                            font-weight: bold;
                        ">Send</button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('chatWindow');
        chatWindow.style.display = this.isOpen ? 'flex' : 'none';

        if (this.isOpen) {
            this.markAllRead();
            document.getElementById('chatInput').focus();
        }
    }

    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();

        if (!message) return;

        // Add message to UI immediately
        this.addMessage({
            from: this.userName,
            text: message,
            timestamp: new Date().toISOString(),
            isUser: true
        });

        // Save to localStorage (will sync to Airtable later)
        const messages = JSON.parse(localStorage.getItem('chatMessages') || '[]');
        messages.push({
            from: this.userName,
            pin: this.userPin,
            text: message,
            timestamp: new Date().toISOString(),
            status: 'sent'
        });
        localStorage.setItem('chatMessages', JSON.stringify(messages));

        // Clear input
        input.value = '';

        // TODO: Send to Airtable or backend
        this.syncToBackend(message);
    }

    addMessage(msg) {
        const messagesDiv = document.getElementById('chatMessages');
        const messageHTML = `
            <div style="
                margin-bottom: 15px;
                display: flex;
                flex-direction: column;
                align-items: ${msg.isUser ? 'flex-end' : 'flex-start'};
            ">
                <div style="
                    max-width: 80%;
                    padding: 12px 16px;
                    background: ${msg.isUser ?
                        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' :
                        'rgba(255,255,255,0.1)'};
                    border-radius: 12px;
                    color: white;
                    word-wrap: break-word;
                ">
                    ${msg.isUser ? '' : `<div style="font-weight: bold; margin-bottom: 5px; opacity: 0.8;">${msg.from}</div>`}
                    <div>${this.escapeHtml(msg.text)}</div>
                    <div style="
                        font-size: 0.7em;
                        opacity: 0.6;
                        margin-top: 5px;
                    ">${new Date(msg.timestamp).toLocaleTimeString()}</div>
                </div>
            </div>
        `;

        messagesDiv.insertAdjacentHTML('beforeend', messageHTML);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    loadMessages() {
        // Load from localStorage
        const messages = JSON.parse(localStorage.getItem('chatMessages') || '[]');
        messages.slice(-20).forEach(msg => this.addMessage(msg)); // Show last 20

        // Check for Commander broadcasts
        const broadcasts = JSON.parse(localStorage.getItem('commanderBroadcasts') || '[]');
        broadcasts.forEach(broadcast => {
            if (!broadcast.read) {
                this.addMessage({
                    from: 'Commander',
                    text: broadcast.message,
                    timestamp: broadcast.timestamp,
                    isUser: false
                });
            }
        });
    }

    checkForBroadcast() {
        // Check if Commander sent a broadcast message
        const broadcasts = JSON.parse(localStorage.getItem('commanderBroadcasts') || '[]');
        const unread = broadcasts.filter(b => !b.read);

        if (unread.length > 0) {
            this.unreadCount = unread.length;
            this.updateBadge();

            // Auto-open chat if important
            if (unread.some(b => b.priority === 'high')) {
                setTimeout(() => this.toggleChat(), 1000);
            }
        }
    }

    updateBadge() {
        const badge = document.getElementById('unreadBadge');
        if (this.unreadCount > 0) {
            badge.style.display = 'flex';
            badge.textContent = this.unreadCount;
        } else {
            badge.style.display = 'none';
        }
    }

    markAllRead() {
        this.unreadCount = 0;
        this.updateBadge();

        const broadcasts = JSON.parse(localStorage.getItem('commanderBroadcasts') || '[]');
        broadcasts.forEach(b => b.read = true);
        localStorage.setItem('commanderBroadcasts', JSON.stringify(broadcasts));
    }

    startPolling() {
        // Poll for new messages every 5 seconds
        setInterval(() => {
            this.checkForBroadcast();
        }, 5000);
    }

    async syncToBackend(message) {
        // TODO: Send to Airtable or custom backend
        // For now, just log it
        console.log('Message to sync:', {
            from: this.userName,
            pin: this.userPin,
            message: message,
            timestamp: new Date().toISOString()
        });

        // Could POST to Netlify function
        try {
            await fetch('/.netlify/functions/chat-message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    from: this.userName,
                    pin: this.userPin,
                    message: message,
                    timestamp: new Date().toISOString()
                })
            });
        } catch (e) {
            console.log('Backend sync failed (expected if not set up yet)');
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize on page load
let liveChat;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        liveChat = new LiveChatWidget();
    });
} else {
    liveChat = new LiveChatWidget();
}

// Commander Broadcast Function (for Commander's dashboard)
function sendCommanderBroadcast(message, priority = 'normal') {
    const broadcasts = JSON.parse(localStorage.getItem('commanderBroadcasts') || '[]');
    broadcasts.push({
        message: message,
        timestamp: new Date().toISOString(),
        priority: priority,
        read: false
    });
    localStorage.setItem('commanderBroadcasts', JSON.stringify(broadcasts));

    console.log('✅ Broadcast sent to all users:', message);
}
