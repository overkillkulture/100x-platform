/**
 * COMMUNITY WIDGET - Live Activity & Who's Online
 * Shows real-time community activity on any page
 * Floating widget in bottom-left corner (ARIA is bottom-right)
 */

class CommunityWidget {
    constructor() {
        this.isOpen = false;
        this.mockData = this.generateMockData();
        this.init();
    }

    generateMockData() {
        return {
            onlineUsers: [
                { name: 'CodeMaster', avatar: '👨‍💻', activity: 'Building KORPAK', status: 'online' },
                { name: 'PatternSeeker', avatar: '🧙', activity: 'Exploring modules', status: 'online' },
                { name: 'QuantumBuilder', avatar: '⚛️', activity: 'Testing Trinity AI', status: 'online' },
                { name: 'CyberArchitect', avatar: '🏗️', activity: 'Designing system', status: 'online' }
            ],
            recentActivity: [
                { user: 'CodeMaster', action: 'created KORPAK', icon: '📦', time: '2m' },
                { user: 'PatternSeeker', action: 'completed boost', icon: '⚡', time: '5m' },
                { user: 'QuantumBuilder', action: 'asked Trinity AI', icon: '🤖', time: '8m' }
            ],
            stats: {
                online: 4,
                building: 12,
                projects: 47
            }
        };
    }

    init() {
        // Check if widget was dismissed
        if (sessionStorage.getItem('communityWidgetDismissed') === 'true') {
            return; // Don't initialize if dismissed
        }
        this.injectStyles();
        this.createHTML();
        this.attachEventListeners();
        this.startAutoUpdate();
    }

    injectStyles() {
        const styles = `
            /* Community Widget Styles */
            .community-widget-container {
                position: fixed;
                bottom: 20px;
                left: 20px;
                z-index: 9999;
                font-family: 'Courier New', monospace;
            }

            .community-widget-button {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #00ffff, #0088ff);
                border: 3px solid #ffd700;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                box-shadow: 0 4px 20px rgba(0, 255, 255, 0.5);
                transition: all 0.3s ease;
                position: relative;
            }

            .community-widget-button.hidden {
                display: none;
            }

            .community-widget-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 30px rgba(0, 255, 255, 0.7);
            }

            .community-widget-button.open {
                background: linear-gradient(135deg, #ff6b00, #ffd700);
            }

            .community-badge {
                position: absolute;
                top: -5px;
                right: -5px;
                background: #00ff00;
                color: #000;
                font-size: 12px;
                font-weight: bold;
                padding: 2px 6px;
                border-radius: 10px;
                border: 2px solid #000;
            }

            .community-window {
                position: absolute;
                bottom: 70px;
                left: 0;
                width: 340px;
                max-height: 500px;
                background: rgba(10, 10, 20, 0.98);
                border: 3px solid #00ffff;
                border-radius: 20px;
                box-shadow: 0 8px 40px rgba(0, 255, 255, 0.4);
                display: none;
                flex-direction: column;
                overflow: hidden;
            }

            .community-window.open {
                display: flex;
                animation: community-slide-up 0.3s ease;
            }

            @keyframes community-slide-up {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .community-header {
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                padding: 15px;
                border-bottom: 2px solid #ffd700;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            .community-header h3 {
                color: #ffd700;
                font-size: 16px;
                margin: 0;
            }

            .community-close {
                color: #00ffff;
                font-size: 24px;
                cursor: pointer;
                transition: color 0.3s;
            }

            .community-close:hover {
                color: #ff6b00;
            }

            .community-dismiss {
                color: #ff6b00;
                font-size: 14px;
                cursor: pointer;
                transition: color 0.3s;
                margin-left: 10px;
            }

            .community-dismiss:hover {
                color: #ff0000;
            }

            .community-tabs {
                display: flex;
                background: rgba(0, 0, 0, 0.3);
                border-bottom: 2px solid #00ffff;
            }

            .community-tab {
                flex: 1;
                padding: 10px;
                text-align: center;
                color: #00ffff;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.3s;
                border-bottom: 3px solid transparent;
            }

            .community-tab.active {
                background: rgba(0, 255, 255, 0.2);
                border-bottom-color: #ffd700;
                color: #ffd700;
            }

            .community-tab:hover {
                background: rgba(0, 255, 255, 0.1);
            }

            .community-content {
                flex: 1;
                overflow-y: auto;
                padding: 15px;
            }

            .community-content::-webkit-scrollbar {
                width: 6px;
            }

            .community-content::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.3);
            }

            .community-content::-webkit-scrollbar-thumb {
                background: #00ffff;
                border-radius: 3px;
            }

            /* Stats View */
            .community-stat {
                background: rgba(0, 255, 255, 0.1);
                border: 1px solid #00ffff;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .stat-label {
                color: #00ffff;
                font-size: 12px;
            }

            .stat-value {
                color: #ffd700;
                font-size: 24px;
                font-weight: bold;
            }

            /* Online Users View */
            .online-user {
                background: rgba(0, 0, 0, 0.3);
                border-left: 3px solid #00ff00;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .user-avatar-small {
                width: 36px;
                height: 36px;
                background: linear-gradient(135deg, #ff6b00, #ffd700);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                border: 2px solid #00ffff;
            }

            .user-details {
                flex: 1;
            }

            .user-name {
                color: #ffd700;
                font-size: 13px;
                font-weight: bold;
            }

            .user-status {
                color: #00ffff;
                font-size: 11px;
            }

            /* Activity View */
            .activity-mini {
                background: rgba(0, 0, 0, 0.3);
                border-left: 3px solid #ff6b00;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
            }

            .activity-mini-header {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 5px;
            }

            .activity-mini-icon {
                font-size: 16px;
            }

            .activity-mini-user {
                color: #ffd700;
                font-size: 12px;
                font-weight: bold;
            }

            .activity-mini-time {
                margin-left: auto;
                color: #888;
                font-size: 10px;
            }

            .activity-mini-text {
                color: #00ffff;
                font-size: 11px;
                margin-left: 24px;
            }

            .view-all-btn {
                width: 100%;
                padding: 10px;
                background: linear-gradient(135deg, #ff6b00, #ffd700);
                border: none;
                border-radius: 8px;
                color: #000;
                font-weight: bold;
                cursor: pointer;
                font-family: 'Courier New', monospace;
                margin-top: 10px;
                transition: all 0.3s;
            }

            .view-all-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(255, 215, 0, 0.5);
            }

            @media (max-width: 480px) {
                .community-window {
                    width: calc(100vw - 40px);
                    bottom: 10px;
                    left: 10px;
                }

                .community-widget-container {
                    bottom: 10px;
                    left: 10px;
                }
            }
        `;

        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }

    createHTML() {
        const container = document.createElement('div');
        container.className = 'community-widget-container';
        container.innerHTML = `
            <div class="community-window" id="community-window">
                <div class="community-header">
                    <h3>🌐 Community</h3>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div class="community-dismiss" onclick="window.communityWidget.dismiss()">Hide</div>
                        <div class="community-close" onclick="window.communityWidget.toggle()">×</div>
                    </div>
                </div>

                <div class="community-tabs">
                    <div class="community-tab active" data-tab="stats" onclick="window.communityWidget.switchTab('stats')">
                        📊 Stats
                    </div>
                    <div class="community-tab" data-tab="online" onclick="window.communityWidget.switchTab('online')">
                        👥 Online
                    </div>
                    <div class="community-tab" data-tab="activity" onclick="window.communityWidget.switchTab('activity')">
                        ⚡ Activity
                    </div>
                </div>

                <div class="community-content" id="community-content">
                    <!-- Content will be inserted here -->
                </div>
            </div>

            <div class="community-widget-button" onclick="window.communityWidget.toggle()">
                🌐
                <div class="community-badge" id="community-badge">4</div>
            </div>
        `;

        document.body.appendChild(container);
    }

    attachEventListeners() {
        window.communityWidget = this;
        this.switchTab('stats'); // Default view
    }

    toggle() {
        this.isOpen = !this.isOpen;
        const window = document.getElementById('community-window');
        const button = document.querySelector('.community-widget-button');

        if (this.isOpen) {
            window.classList.add('open');
            button.classList.add('open');
        } else {
            window.classList.remove('open');
            button.classList.remove('open');
        }
    }

    switchTab(tab) {
        // Update active tab
        document.querySelectorAll('.community-tab').forEach(t => {
            t.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

        // Render content
        const content = document.getElementById('community-content');

        switch(tab) {
            case 'stats':
                content.innerHTML = this.renderStats();
                break;
            case 'online':
                content.innerHTML = this.renderOnline();
                break;
            case 'activity':
                content.innerHTML = this.renderActivity();
                break;
        }
    }

    renderStats() {
        return `
            <div class="community-stat">
                <div class="stat-label">
                    <i class="fas fa-circle" style="color: #00ff00;"></i> Online Now
                </div>
                <div class="stat-value">${this.mockData.stats.online}</div>
            </div>
            <div class="community-stat">
                <div class="stat-label">
                    <i class="fas fa-hammer" style="color: #ffd700;"></i> Building Now
                </div>
                <div class="stat-value">${this.mockData.stats.building}</div>
            </div>
            <div class="community-stat">
                <div class="stat-label">
                    <i class="fas fa-rocket" style="color: #ff6b00;"></i> Total Projects
                </div>
                <div class="stat-value">${this.mockData.stats.projects}</div>
            </div>
            <button class="view-all-btn" onclick="window.location.href='./community-activity.html'">
                View Full Dashboard
            </button>
        `;
    }

    renderOnline() {
        return this.mockData.onlineUsers.map(user => `
            <div class="online-user">
                <div class="user-avatar-small">${user.avatar}</div>
                <div class="user-details">
                    <div class="user-name">${user.name}</div>
                    <div class="user-status">${user.activity}</div>
                </div>
            </div>
        `).join('') + `
            <button class="view-all-btn" onclick="window.location.href='./community-activity.html'">
                View All Builders
            </button>
        `;
    }

    renderActivity() {
        return this.mockData.recentActivity.map(activity => `
            <div class="activity-mini">
                <div class="activity-mini-header">
                    <span class="activity-mini-icon">${activity.icon}</span>
                    <span class="activity-mini-user">${activity.user}</span>
                    <span class="activity-mini-time">${activity.time}</span>
                </div>
                <div class="activity-mini-text">${activity.action}</div>
            </div>
        `).join('') + `
            <button class="view-all-btn" onclick="window.location.href='./community-activity.html'">
                View All Activity
            </button>
        `;
    }

    updateStats() {
        // Simulate stats update
        this.mockData.stats.online = 4 + Math.floor(Math.random() * 3);
        this.mockData.stats.building = 10 + Math.floor(Math.random() * 5);
        this.mockData.stats.projects += Math.floor(Math.random() * 2);

        // Update badge
        document.getElementById('community-badge').textContent = this.mockData.stats.online;

        // Refresh if stats tab is active
        if (document.querySelector('[data-tab="stats"]').classList.contains('active')) {
            this.switchTab('stats');
        }
    }

    startAutoUpdate() {
        // Update stats every 15 seconds
        setInterval(() => {
            this.updateStats();
        }, 15000);
    }

    dismiss() {
        // Hide widget permanently for this session
        sessionStorage.setItem('communityWidgetDismissed', 'true');
        document.querySelector('.community-widget-container').style.display = 'none';
    }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new CommunityWidget();
    });
} else {
    new CommunityWidget();
}
