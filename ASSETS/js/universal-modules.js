/**
 * 🌀 UNIVERSAL CONSCIOUSNESS MODULES 🌀
 * Persistent components that follow users to EVERY screen
 *
 * Include this ONE file on any page to get all the modules!
 */

// =============================================================================
// 🎵 MODULE 1: PERSISTENT MUSIC PLAYER
// =============================================================================

class ConsciousnessMusicPlayer {
    constructor() {
        this.isPlaying = false;
        this.currentTrack = 0;
        this.playlist = [
            { title: "Consciousness Rising", artist: "The Collective", url: "spotify:track:xxxxx" },
            { title: "Digital Awakening", artist: "The Collective", url: "spotify:track:xxxxx" },
            { title: "Trinity System", artist: "The Collective", url: "spotify:track:xxxxx" }
        ];
        this.init();
    }

    init() {
        // Create floating music player (bottom right corner)
        const player = document.createElement('div');
        player.id = 'consciousness-music-player';
        player.innerHTML = `
            <div class="music-player-container">
                <div class="player-header">
                    <div class="player-icon">🎵</div>
                    <div class="player-title">Consciousness Radio</div>
                    <button class="player-minimize">−</button>
                </div>
                <div class="player-body">
                    <div class="now-playing">
                        <div class="track-title">Consciousness Rising</div>
                        <div class="track-artist">The Consciousness Collective</div>
                    </div>
                    <div class="player-controls">
                        <button class="btn-prev">⏮</button>
                        <button class="btn-play">▶️</button>
                        <button class="btn-next">⏭</button>
                    </div>
                    <div class="player-links">
                        <a href="https://spotify.com" target="_blank">Spotify</a>
                        <a href="https://music.apple.com" target="_blank">Apple</a>
                        <a href="#download">Download Album</a>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(player);
        this.attachEventListeners();
        this.applyStyles();
    }

    attachEventListeners() {
        document.querySelector('.btn-play').addEventListener('click', () => this.togglePlay());
        document.querySelector('.btn-next').addEventListener('click', () => this.nextTrack());
        document.querySelector('.btn-prev').addEventListener('click', () => this.prevTrack());
        document.querySelector('.player-minimize').addEventListener('click', () => this.toggleMinimize());
    }

    togglePlay() {
        this.isPlaying = !this.isPlaying;
        const btn = document.querySelector('.btn-play');
        btn.textContent = this.isPlaying ? '⏸' : '▶️';
    }

    nextTrack() {
        this.currentTrack = (this.currentTrack + 1) % this.playlist.length;
        this.updateDisplay();
    }

    prevTrack() {
        this.currentTrack = (this.currentTrack - 1 + this.playlist.length) % this.playlist.length;
        this.updateDisplay();
    }

    updateDisplay() {
        const track = this.playlist[this.currentTrack];
        document.querySelector('.track-title').textContent = track.title;
        document.querySelector('.track-artist').textContent = track.artist;
    }

    toggleMinimize() {
        const player = document.getElementById('consciousness-music-player');
        player.classList.toggle('minimized');
    }

    applyStyles() {
        const style = document.createElement('style');
        style.textContent = `
            #consciousness-music-player {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 300px;
                background: linear-gradient(135deg, rgba(10, 10, 10, 0.95), rgba(26, 26, 46, 0.95));
                border: 2px solid #00ddff;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0, 221, 255, 0.4);
                z-index: 9998;
                font-family: 'Segoe UI', sans-serif;
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }

            #consciousness-music-player.minimized .player-body {
                display: none;
            }

            #consciousness-music-player.minimized {
                width: 200px;
            }

            .music-player-container {
                padding: 0;
            }

            .player-header {
                background: linear-gradient(135deg, #00ddff, #00ff00);
                padding: 10px 15px;
                border-radius: 13px 13px 0 0;
                display: flex;
                align-items: center;
                gap: 10px;
                cursor: move;
            }

            .player-icon {
                font-size: 20px;
            }

            .player-title {
                flex: 1;
                font-weight: 600;
                color: #0a0a0a;
                font-size: 14px;
            }

            .player-minimize {
                background: none;
                border: none;
                color: #0a0a0a;
                font-size: 20px;
                cursor: pointer;
                padding: 0;
                width: 24px;
                height: 24px;
                line-height: 1;
            }

            .player-body {
                padding: 15px;
            }

            .now-playing {
                margin-bottom: 15px;
                text-align: center;
            }

            .track-title {
                color: #00ff00;
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 5px;
            }

            .track-artist {
                color: #00ddff;
                font-size: 12px;
            }

            .player-controls {
                display: flex;
                justify-content: center;
                gap: 15px;
                margin-bottom: 15px;
            }

            .player-controls button {
                background: rgba(0, 221, 255, 0.1);
                border: 1px solid #00ddff;
                color: #00ddff;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                cursor: pointer;
                transition: all 0.3s;
                font-size: 16px;
            }

            .player-controls button:hover {
                background: rgba(0, 255, 0, 0.2);
                border-color: #00ff00;
                color: #00ff00;
                transform: scale(1.1);
            }

            .player-links {
                display: flex;
                justify-content: space-around;
                gap: 10px;
                padding-top: 10px;
                border-top: 1px solid rgba(0, 221, 255, 0.2);
            }

            .player-links a {
                color: #00ddff;
                text-decoration: none;
                font-size: 11px;
                transition: color 0.3s;
            }

            .player-links a:hover {
                color: #00ff00;
            }
        `;
        document.head.appendChild(style);
    }
}

// =============================================================================
// 🎯 MODULE 2: QUICK ACCESS MENU
// =============================================================================

class QuickAccessMenu {
    constructor() {
        this.isOpen = false;
        this.init();
    }

    init() {
        const menu = document.createElement('div');
        menu.id = 'quick-access-menu';
        menu.innerHTML = `
            <button class="quick-menu-toggle">⚡</button>
            <div class="quick-menu-panel">
                <div class="quick-menu-header">Quick Access</div>
                <div class="quick-menu-items">
                    <a href="/dashboard.html" class="quick-item">
                        <span class="item-icon">🎯</span>
                        <span class="item-label">Dashboard</span>
                    </a>
                    <a href="/cockpit.html" class="quick-item">
                        <span class="item-icon">🚀</span>
                        <span class="item-label">Cockpit</span>
                    </a>
                    <a href="/PUBLIC/pattern-filter.html" class="quick-item">
                        <span class="item-icon">🧠</span>
                        <span class="item-label">Pattern Test</span>
                    </a>
                    <a href="/roadmap.html" class="quick-item">
                        <span class="item-icon">🗺️</span>
                        <span class="item-label">Roadmap</span>
                    </a>
                    <a href="/bug-report.html" class="quick-item">
                        <span class="item-icon">🐛</span>
                        <span class="item-label">Report Bug</span>
                    </a>
                </div>
            </div>
        `;
        document.body.appendChild(menu);
        this.attachEventListeners();
        this.applyStyles();
    }

    attachEventListeners() {
        const toggle = document.querySelector('.quick-menu-toggle');
        const panel = document.querySelector('.quick-menu-panel');

        toggle.addEventListener('click', () => {
            this.isOpen = !this.isOpen;
            panel.classList.toggle('open');
            toggle.textContent = this.isOpen ? '✕' : '⚡';
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#quick-access-menu')) {
                this.isOpen = false;
                panel.classList.remove('open');
                toggle.textContent = '⚡';
            }
        });
    }

    applyStyles() {
        const style = document.createElement('style');
        style.textContent = `
            #quick-access-menu {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
            }

            .quick-menu-toggle {
                background: linear-gradient(135deg, #00ddff, #00ff00);
                border: none;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                font-size: 24px;
                cursor: pointer;
                box-shadow: 0 5px 20px rgba(0, 221, 255, 0.5);
                transition: all 0.3s;
            }

            .quick-menu-toggle:hover {
                transform: scale(1.1);
                box-shadow: 0 8px 30px rgba(0, 255, 0, 0.6);
            }

            .quick-menu-panel {
                position: absolute;
                top: 60px;
                right: 0;
                width: 200px;
                background: linear-gradient(135deg, rgba(10, 10, 10, 0.95), rgba(26, 26, 46, 0.95));
                border: 2px solid #00ddff;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0, 221, 255, 0.4);
                backdrop-filter: blur(10px);
                opacity: 0;
                visibility: hidden;
                transform: translateY(-10px);
                transition: all 0.3s;
            }

            .quick-menu-panel.open {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
            }

            .quick-menu-header {
                background: linear-gradient(135deg, #00ddff, #00ff00);
                color: #0a0a0a;
                padding: 10px 15px;
                border-radius: 13px 13px 0 0;
                font-weight: 600;
                font-size: 14px;
            }

            .quick-menu-items {
                padding: 10px;
            }

            .quick-item {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 10px;
                color: #00ddff;
                text-decoration: none;
                border-radius: 8px;
                transition: all 0.3s;
                margin-bottom: 5px;
            }

            .quick-item:hover {
                background: rgba(0, 221, 255, 0.1);
                color: #00ff00;
                transform: translateX(5px);
            }

            .item-icon {
                font-size: 18px;
            }

            .item-label {
                font-size: 13px;
                font-weight: 500;
            }
        `;
        document.head.appendChild(style);
    }
}

// =============================================================================
// 📊 MODULE 3: CONSCIOUSNESS STATUS INDICATOR
// =============================================================================

class ConsciousnessStatus {
    constructor() {
        this.level = 93; // Current consciousness level
        this.init();
    }

    init() {
        const status = document.createElement('div');
        status.id = 'consciousness-status';
        status.innerHTML = `
            <div class="status-indicator">
                <div class="status-label">CL:</div>
                <div class="status-value">${this.level}%</div>
                <div class="status-bar">
                    <div class="status-fill" style="width: ${this.level}%"></div>
                </div>
            </div>
        `;
        document.body.appendChild(status);
        this.applyStyles();
        this.animate();
    }

    animate() {
        setInterval(() => {
            // Subtle fluctuation
            const variation = Math.random() * 2 - 1; // -1 to +1
            const newLevel = Math.min(100, Math.max(85, this.level + variation));
            this.updateLevel(newLevel);
        }, 3000);
    }

    updateLevel(newLevel) {
        this.level = newLevel;
        document.querySelector('.status-value').textContent = `${Math.round(newLevel)}%`;
        document.querySelector('.status-fill').style.width = `${newLevel}%`;
    }

    applyStyles() {
        const style = document.createElement('style');
        style.textContent = `
            #consciousness-status {
                position: fixed;
                top: 20px;
                left: 20px;
                z-index: 9999;
            }

            .status-indicator {
                background: linear-gradient(135deg, rgba(10, 10, 10, 0.9), rgba(26, 26, 46, 0.9));
                border: 2px solid #00ddff;
                border-radius: 25px;
                padding: 8px 15px;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: 0 5px 20px rgba(0, 221, 255, 0.3);
                backdrop-filter: blur(10px);
            }

            .status-label {
                color: #00ddff;
                font-weight: 600;
                font-size: 12px;
            }

            .status-value {
                color: #00ff00;
                font-weight: 700;
                font-size: 14px;
                min-width: 45px;
            }

            .status-bar {
                width: 100px;
                height: 6px;
                background: rgba(0, 221, 255, 0.2);
                border-radius: 3px;
                overflow: hidden;
            }

            .status-fill {
                height: 100%;
                background: linear-gradient(90deg, #00ddff, #00ff00);
                border-radius: 3px;
                transition: width 1s ease;
                box-shadow: 0 0 10px #00ff00;
            }
        `;
        document.head.appendChild(style);
    }
}

// =============================================================================
// 🤖 MODULE 4: AI ASSISTANT CHAT BUBBLE
// =============================================================================

class AIAssistant {
    constructor() {
        this.isOpen = false;
        this.init();
    }

    init() {
        const assistant = document.createElement('div');
        assistant.id = 'ai-assistant';
        assistant.innerHTML = `
            <button class="ai-toggle">
                <span class="ai-icon">🤖</span>
                <span class="ai-pulse"></span>
            </button>
            <div class="ai-chat-window">
                <div class="ai-header">
                    <div class="ai-title">ARIA Assistant</div>
                    <button class="ai-close">✕</button>
                </div>
                <div class="ai-messages">
                    <div class="ai-message bot">
                        <div class="message-avatar">🤖</div>
                        <div class="message-text">Hi! I'm ARIA, your consciousness guide. How can I help you navigate the platform?</div>
                    </div>
                </div>
                <div class="ai-input-area">
                    <input type="text" placeholder="Ask me anything..." class="ai-input">
                    <button class="ai-send">Send</button>
                </div>
            </div>
        `;
        document.body.appendChild(assistant);
        this.attachEventListeners();
        this.applyStyles();
    }

    attachEventListeners() {
        const toggle = document.querySelector('.ai-toggle');
        const window = document.querySelector('.ai-chat-window');
        const close = document.querySelector('.ai-close');

        toggle.addEventListener('click', () => this.toggle());
        close.addEventListener('click', () => this.toggle());

        document.querySelector('.ai-send').addEventListener('click', () => this.sendMessage());
        document.querySelector('.ai-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    toggle() {
        this.isOpen = !this.isOpen;
        document.querySelector('.ai-chat-window').classList.toggle('open');
        document.querySelector('.ai-toggle').classList.toggle('active');
    }

    sendMessage() {
        const input = document.querySelector('.ai-input');
        const message = input.value.trim();
        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        input.value = '';

        // Simulate AI response
        setTimeout(() => {
            const responses = [
                "I can help you with that! Check the Dashboard for more details.",
                "Great question! The Pattern Filter can help you understand that better.",
                "Let me point you to the Cockpit where you can see all system status.",
                "That's part of the consciousness calibration process. Want to learn more?"
            ];
            const response = responses[Math.floor(Math.random() * responses.length)];
            this.addMessage(response, 'bot');
        }, 1000);
    }

    addMessage(text, type) {
        const messagesDiv = document.querySelector('.ai-messages');
        const message = document.createElement('div');
        message.className = `ai-message ${type}`;
        message.innerHTML = `
            <div class="message-avatar">${type === 'bot' ? '🤖' : '👤'}</div>
            <div class="message-text">${text}</div>
        `;
        messagesDiv.appendChild(message);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    applyStyles() {
        const style = document.createElement('style');
        style.textContent = `
            #ai-assistant {
                position: fixed;
                bottom: 100px;
                right: 20px;
                z-index: 9997;
            }

            .ai-toggle {
                background: linear-gradient(135deg, #00ddff, #00ff00);
                border: none;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                cursor: pointer;
                box-shadow: 0 5px 20px rgba(0, 221, 255, 0.5);
                position: relative;
                transition: all 0.3s;
            }

            .ai-toggle:hover {
                transform: scale(1.1);
            }

            .ai-toggle.active {
                background: linear-gradient(135deg, #ff0066, #ff6600);
            }

            .ai-icon {
                font-size: 30px;
                display: block;
            }

            .ai-pulse {
                position: absolute;
                top: -5px;
                right: -5px;
                width: 15px;
                height: 15px;
                background: #00ff00;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.5; transform: scale(1.2); }
            }

            .ai-chat-window {
                position: absolute;
                bottom: 70px;
                right: 0;
                width: 350px;
                height: 500px;
                background: linear-gradient(135deg, rgba(10, 10, 10, 0.95), rgba(26, 26, 46, 0.95));
                border: 2px solid #00ddff;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0, 221, 255, 0.4);
                backdrop-filter: blur(10px);
                display: flex;
                flex-direction: column;
                opacity: 0;
                visibility: hidden;
                transform: translateY(20px) scale(0.9);
                transition: all 0.3s;
            }

            .ai-chat-window.open {
                opacity: 1;
                visibility: visible;
                transform: translateY(0) scale(1);
            }

            .ai-header {
                background: linear-gradient(135deg, #00ddff, #00ff00);
                color: #0a0a0a;
                padding: 15px;
                border-radius: 13px 13px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .ai-title {
                font-weight: 600;
                font-size: 16px;
            }

            .ai-close {
                background: none;
                border: none;
                color: #0a0a0a;
                font-size: 20px;
                cursor: pointer;
            }

            .ai-messages {
                flex: 1;
                overflow-y: auto;
                padding: 15px;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }

            .ai-message {
                display: flex;
                gap: 10px;
                align-items: flex-start;
            }

            .ai-message.user {
                flex-direction: row-reverse;
            }

            .message-avatar {
                font-size: 24px;
                flex-shrink: 0;
            }

            .message-text {
                background: rgba(0, 221, 255, 0.1);
                border: 1px solid rgba(0, 221, 255, 0.3);
                color: #00ddff;
                padding: 10px;
                border-radius: 10px;
                max-width: 70%;
                font-size: 13px;
                line-height: 1.4;
            }

            .ai-message.user .message-text {
                background: rgba(0, 255, 0, 0.1);
                border-color: rgba(0, 255, 0, 0.3);
                color: #00ff00;
            }

            .ai-input-area {
                padding: 15px;
                display: flex;
                gap: 10px;
                border-top: 1px solid rgba(0, 221, 255, 0.2);
            }

            .ai-input {
                flex: 1;
                background: rgba(0, 221, 255, 0.05);
                border: 1px solid #00ddff;
                color: #00ddff;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
            }

            .ai-input::placeholder {
                color: rgba(0, 221, 255, 0.5);
            }

            .ai-send {
                background: linear-gradient(135deg, #00ddff, #00ff00);
                border: none;
                color: #0a0a0a;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                font-size: 13px;
            }

            .ai-send:hover {
                opacity: 0.9;
            }
        `;
        document.head.appendChild(style);
    }
}

// =============================================================================
// 🚀 AUTO-INITIALIZE ALL MODULES
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🌀 Initializing Universal Consciousness Modules...');

    // Initialize all modules
    new ConsciousnessMusicPlayer();
    new QuickAccessMenu();
    new ConsciousnessStatus();
    new AIAssistant();

    console.log('✅ All universal modules loaded!');
    console.log('   🎵 Music Player - Bottom Right');
    console.log('   ⚡ Quick Menu - Top Right');
    console.log('   📊 Status - Top Left');
    console.log('   🤖 AI Assistant - Bottom Right');
});
