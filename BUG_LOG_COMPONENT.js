/**
 * 🐛 BUG LOG COMPONENT 🐛
 * Universal bug reporting system for every page
 *
 * Features:
 * - Fixed bug report button on every page
 * - Quick submission form (overlay)
 * - Stores to localStorage (Airtable integration ready)
 * - Bug count indicator
 * - Admin view for reviewing bugs
 * - Integration with Module Phase System
 */

class BugLogSystem {
    constructor() {
        this.bugs = this.loadBugs();
        this.isAdmin = false; // Set true to see admin panel

        this.init();
    }

    loadBugs() {
        const saved = localStorage.getItem('bugLog');
        if (saved) return JSON.parse(saved);
        return [];
    }

    saveBugs() {
        localStorage.setItem('bugLog', JSON.stringify(this.bugs));
    }

    // Get current module info
    getCurrentModule() {
        const path = window.location.pathname;
        const filename = path.split('/').pop() || 'index.html';

        // Get phase if Module Phase System exists
        let phase = 'unknown';
        if (window.ModulePhase) {
            phase = window.ModulePhase.getCurrentModulePhase();
        }

        return {
            filename: filename,
            path: path,
            phase: phase,
            url: window.location.href
        };
    }

    // Submit bug report
    submitBug(description, type = 'bug', severity = 'medium') {
        const module = this.getCurrentModule();

        const bug = {
            id: Date.now(),
            timestamp: new Date().toISOString(),
            description: description,
            type: type, // bug, feature, improvement, question
            severity: severity, // low, medium, high, critical
            status: 'open', // open, in-progress, resolved, closed
            module: module,
            userAgent: navigator.userAgent,
            screenSize: `${window.innerWidth}x${window.innerHeight}`
        };

        this.bugs.push(bug);
        this.saveBugs();

        // If Airtable is configured, sync there too
        this.syncToAirtable(bug);

        // Update bug count indicator
        this.updateBugCount();

        return bug;
    }

    // Sync to Airtable (ready for when Airtable is set up)
    async syncToAirtable(bug) {
        // This will work once Airtable credentials are configured
        try {
            const airtableBase = localStorage.getItem('airtable_base_id');
            const airtableToken = localStorage.getItem('airtable_api_token');

            if (!airtableBase || !airtableToken) {
                console.log('Airtable not configured yet - bug saved locally');
                return;
            }

            const response = await fetch(`https://api.airtable.com/v0/${airtableBase}/Bug%20Reports`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${airtableToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    fields: {
                        'Description': bug.description,
                        'Type': bug.type,
                        'Severity': bug.severity,
                        'Status': bug.status,
                        'Module': bug.module.filename,
                        'Phase': bug.module.phase,
                        'Timestamp': bug.timestamp
                    }
                })
            });

            if (response.ok) {
                console.log('Bug synced to Airtable');
            }
        } catch (error) {
            console.log('Airtable sync pending:', error.message);
        }
    }

    // Get bugs for current module
    getModuleBugs() {
        const module = this.getCurrentModule();
        return this.bugs.filter(bug =>
            bug.module.filename === module.filename &&
            bug.status !== 'closed'
        );
    }

    // Update bug status
    updateBugStatus(bugId, newStatus) {
        const bug = this.bugs.find(b => b.id === bugId);
        if (bug) {
            bug.status = newStatus;
            bug.updatedAt = new Date().toISOString();
            this.saveBugs();

            // Trigger XP if bug resolved
            if (newStatus === 'resolved' && window.BuilderXP) {
                window.BuilderXP.rewardAction('pattern_found'); // +300 XP
            }
        }
    }

    // Create bug report button (fixed position)
    createBugButton() {
        const button = document.createElement('button');
        button.className = 'bug-report-button';
        button.innerHTML = `
            <span class="bug-icon">🐛</span>
            <span class="bug-count" id="bugCount">0</span>
        `;
        button.title = 'Report a bug or issue';

        button.onclick = () => this.openBugForm();

        return button;
    }

    // Create bug submission form (overlay)
    createBugForm() {
        const overlay = document.createElement('div');
        overlay.className = 'bug-form-overlay';
        overlay.id = 'bugFormOverlay';

        const module = this.getCurrentModule();
        const moduleBugs = this.getModuleBugs();

        overlay.innerHTML = `
            <div class="bug-form-container">
                <div class="bug-form-header">
                    <h3>🐛 Report Bug or Issue</h3>
                    <button class="close-btn" onclick="BugLog.closeBugForm()">×</button>
                </div>

                <div class="bug-form-body">
                    <div class="module-info">
                        <strong>Module:</strong> ${module.filename}
                        ${window.ModulePhase ? `<span class="phase-badge-mini" style="background: ${window.ModulePhase.phases[module.phase].color}">${window.ModulePhase.phases[module.phase].icon} ${module.phase}</span>` : ''}
                    </div>

                    <form id="bugSubmitForm">
                        <div class="form-group">
                            <label>Type:</label>
                            <select name="type" required>
                                <option value="bug">🐛 Bug</option>
                                <option value="feature">✨ Feature Request</option>
                                <option value="improvement">⚡ Improvement</option>
                                <option value="question">❓ Question</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Severity:</label>
                            <select name="severity" required>
                                <option value="low">Low</option>
                                <option value="medium" selected>Medium</option>
                                <option value="high">High</option>
                                <option value="critical">Critical</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Description:</label>
                            <textarea name="description" rows="5" placeholder="Describe the bug, feature, or issue..." required></textarea>
                        </div>

                        <button type="submit" class="submit-btn">Submit Report</button>
                    </form>

                    ${moduleBugs.length > 0 ? `
                        <div class="existing-bugs">
                            <h4>Recent Reports (${moduleBugs.length}):</h4>
                            <div class="bug-list">
                                ${moduleBugs.slice(-3).reverse().map(bug => `
                                    <div class="bug-item ${bug.severity}">
                                        <div class="bug-item-header">
                                            <span class="bug-type">${this.getTypeIcon(bug.type)} ${bug.type}</span>
                                            <span class="bug-severity">${bug.severity}</span>
                                        </div>
                                        <div class="bug-description">${bug.description}</div>
                                        <div class="bug-timestamp">${this.formatTimestamp(bug.timestamp)}</div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;

        return overlay;
    }

    getTypeIcon(type) {
        const icons = {
            bug: '🐛',
            feature: '✨',
            improvement: '⚡',
            question: '❓'
        };
        return icons[type] || '📝';
    }

    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;

        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        if (days < 7) return `${days}d ago`;

        return date.toLocaleDateString();
    }

    openBugForm() {
        let overlay = document.getElementById('bugFormOverlay');

        if (!overlay) {
            overlay = this.createBugForm();
            document.body.appendChild(overlay);

            // Add form submit handler
            const form = document.getElementById('bugSubmitForm');
            form.onsubmit = (e) => {
                e.preventDefault();
                const formData = new FormData(form);

                this.submitBug(
                    formData.get('description'),
                    formData.get('type'),
                    formData.get('severity')
                );

                // Show success message
                this.showSuccessMessage();

                // Close form
                this.closeBugForm();

                // Reset form
                form.reset();
            };

            // Close on overlay click
            overlay.onclick = (e) => {
                if (e.target === overlay) {
                    this.closeBugForm();
                }
            };
        }

        overlay.style.display = 'flex';
    }

    closeBugForm() {
        const overlay = document.getElementById('bugFormOverlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }

    showSuccessMessage() {
        const message = document.createElement('div');
        message.className = 'bug-success-message';
        message.innerHTML = `
            <div class="success-content">
                <span class="success-icon">✅</span>
                <span>Bug report submitted!</span>
            </div>
        `;

        document.body.appendChild(message);

        setTimeout(() => {
            message.classList.add('fade-out');
            setTimeout(() => message.remove(), 500);
        }, 3000);
    }

    updateBugCount() {
        const countElement = document.getElementById('bugCount');
        if (countElement) {
            const openBugs = this.bugs.filter(b => b.status === 'open').length;
            countElement.textContent = openBugs;
            countElement.style.display = openBugs > 0 ? 'flex' : 'none';
        }
    }

    // Create admin panel (for reviewing all bugs)
    createAdminPanel() {
        const panel = document.createElement('div');
        panel.className = 'bug-admin-panel';
        panel.id = 'bugAdminPanel';

        const bugsByModule = {};
        this.bugs.forEach(bug => {
            const moduleName = bug.module.filename;
            if (!bugsByModule[moduleName]) {
                bugsByModule[moduleName] = [];
            }
            bugsByModule[moduleName].push(bug);
        });

        const stats = {
            total: this.bugs.length,
            open: this.bugs.filter(b => b.status === 'open').length,
            inProgress: this.bugs.filter(b => b.status === 'in-progress').length,
            resolved: this.bugs.filter(b => b.status === 'resolved').length
        };

        panel.innerHTML = `
            <div class="admin-header">
                <h3>🐛 Bug Administration</h3>
                <button class="close-btn" onclick="BugLog.closeAdminPanel()">×</button>
            </div>

            <div class="admin-stats">
                <div class="stat-card">
                    <div class="stat-value">${stats.total}</div>
                    <div class="stat-label">Total Reports</div>
                </div>
                <div class="stat-card open">
                    <div class="stat-value">${stats.open}</div>
                    <div class="stat-label">Open</div>
                </div>
                <div class="stat-card in-progress">
                    <div class="stat-value">${stats.inProgress}</div>
                    <div class="stat-label">In Progress</div>
                </div>
                <div class="stat-card resolved">
                    <div class="stat-value">${stats.resolved}</div>
                    <div class="stat-label">Resolved</div>
                </div>
            </div>

            <div class="admin-bugs">
                ${Object.entries(bugsByModule).map(([module, bugs]) => `
                    <div class="module-bugs-section">
                        <h4>${module} (${bugs.length})</h4>
                        ${bugs.reverse().map(bug => `
                            <div class="admin-bug-item ${bug.status}">
                                <div class="bug-header">
                                    <span class="bug-type">${this.getTypeIcon(bug.type)} ${bug.type}</span>
                                    <span class="bug-severity severity-${bug.severity}">${bug.severity}</span>
                                    <span class="bug-status">${bug.status}</span>
                                </div>
                                <div class="bug-description">${bug.description}</div>
                                <div class="bug-meta">
                                    <span>${this.formatTimestamp(bug.timestamp)}</span>
                                    <span>Phase: ${bug.module.phase}</span>
                                </div>
                                <div class="bug-actions">
                                    ${bug.status !== 'in-progress' ? `<button onclick="BugLog.updateBugStatus(${bug.id}, 'in-progress')">▶ Start</button>` : ''}
                                    ${bug.status !== 'resolved' ? `<button onclick="BugLog.updateBugStatus(${bug.id}, 'resolved')">✓ Resolve</button>` : ''}
                                    ${bug.status !== 'closed' ? `<button onclick="BugLog.updateBugStatus(${bug.id}, 'closed')">✗ Close</button>` : ''}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `).join('')}
            </div>
        `;

        return panel;
    }

    toggleAdminPanel() {
        let panel = document.getElementById('bugAdminPanel');

        if (!panel) {
            panel = this.createAdminPanel();
            document.body.appendChild(panel);
        }

        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    }

    closeAdminPanel() {
        const panel = document.getElementById('bugAdminPanel');
        if (panel) {
            panel.style.display = 'none';
        }
    }

    // Auto-inject bug button on page load
    autoInject() {
        const button = this.createBugButton();
        button.style.cssText = `
            position: fixed;
            bottom: 80px;
            right: 20px;
            z-index: 9999;
        `;
        document.body.appendChild(button);

        // Update count
        this.updateBugCount();

        // If admin mode, add keyboard shortcut
        if (this.isAdmin) {
            document.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.shiftKey && e.key === 'B') {
                    this.toggleAdminPanel();
                }
            });
        }
    }

    init() {
        this.injectStyles();
    }

    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* Bug Report Button */
            .bug-report-button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
                transition: all 0.3s ease;
                position: relative;
            }

            .bug-report-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 30px rgba(102, 126, 234, 0.6);
            }

            .bug-icon {
                font-size: 28px;
            }

            .bug-count {
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
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }

            /* Bug Form Overlay */
            .bug-form-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.7);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                animation: fadeIn 0.2s ease;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .bug-form-container {
                background: white;
                border-radius: 15px;
                width: 90%;
                max-width: 600px;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 10px 50px rgba(0, 0, 0, 0.3);
                animation: slideUp 0.3s ease;
            }

            @keyframes slideUp {
                from { transform: translateY(50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }

            .bug-form-header {
                padding: 20px;
                border-bottom: 2px solid #f0f0f0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .bug-form-header h3 {
                margin: 0;
                color: #333;
            }

            .close-btn {
                background: none;
                border: none;
                font-size: 32px;
                color: #999;
                cursor: pointer;
                line-height: 1;
                transition: color 0.2s ease;
            }

            .close-btn:hover {
                color: #333;
            }

            .bug-form-body {
                padding: 20px;
            }

            .module-info {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .phase-badge-mini {
                padding: 4px 12px;
                border-radius: 12px;
                color: white;
                font-size: 0.85em;
                font-weight: bold;
            }

            .form-group {
                margin-bottom: 20px;
            }

            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
                color: #333;
            }

            .form-group select,
            .form-group textarea {
                width: 100%;
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                font-family: inherit;
                transition: border-color 0.2s ease;
            }

            .form-group select:focus,
            .form-group textarea:focus {
                outline: none;
                border-color: #667eea;
            }

            .submit-btn {
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.2s ease;
            }

            .submit-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }

            /* Existing Bugs */
            .existing-bugs {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px solid #f0f0f0;
            }

            .existing-bugs h4 {
                color: #333;
                margin-bottom: 15px;
            }

            .bug-list {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }

            .bug-item {
                padding: 12px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                background: #f8f9fa;
            }

            .bug-item.high {
                border-left-color: #ff9800;
            }

            .bug-item.critical {
                border-left-color: #f44336;
            }

            .bug-item-header {
                display: flex;
                justify-content: space-between;
                margin-bottom: 8px;
                font-size: 0.9em;
            }

            .bug-type {
                font-weight: bold;
                color: #667eea;
            }

            .bug-severity {
                background: #e0e0e0;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 0.85em;
                text-transform: uppercase;
            }

            .bug-description {
                color: #666;
                font-size: 0.9em;
                margin-bottom: 5px;
            }

            .bug-timestamp {
                color: #999;
                font-size: 0.8em;
            }

            /* Success Message */
            .bug-success-message {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10001;
                animation: slideInRight 0.3s ease;
            }

            .bug-success-message.fade-out {
                animation: fadeOut 0.5s ease;
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

            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }

            .success-content {
                background: #4caf50;
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: 0 5px 20px rgba(76, 175, 80, 0.4);
            }

            .success-icon {
                font-size: 24px;
            }

            /* Admin Panel */
            .bug-admin-panel {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 90%;
                max-width: 1200px;
                max-height: 90vh;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 50px rgba(0, 0, 0, 0.3);
                display: none;
                flex-direction: column;
                z-index: 10000;
                overflow: hidden;
            }

            .admin-header {
                padding: 20px;
                border-bottom: 2px solid #f0f0f0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }

            .admin-header h3 {
                margin: 0;
            }

            .admin-stats {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                padding: 20px;
                background: #f8f9fa;
            }

            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }

            .stat-value {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }

            .stat-card.open .stat-value {
                color: #ff9800;
            }

            .stat-card.in-progress .stat-value {
                color: #2196f3;
            }

            .stat-card.resolved .stat-value {
                color: #4caf50;
            }

            .stat-label {
                color: #666;
                font-size: 0.9em;
                margin-top: 5px;
            }

            .admin-bugs {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
            }

            .module-bugs-section {
                margin-bottom: 30px;
            }

            .module-bugs-section h4 {
                color: #333;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #f0f0f0;
            }

            .admin-bug-item {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }

            .admin-bug-item.open {
                border-left: 4px solid #ff9800;
            }

            .admin-bug-item.in-progress {
                border-left: 4px solid #2196f3;
            }

            .admin-bug-item.resolved {
                border-left: 4px solid #4caf50;
            }

            .bug-header {
                display: flex;
                gap: 10px;
                margin-bottom: 10px;
            }

            .bug-status {
                background: #e0e0e0;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.85em;
                font-weight: bold;
                text-transform: uppercase;
            }

            .severity-high {
                color: #ff9800;
            }

            .severity-critical {
                color: #f44336;
            }

            .bug-meta {
                display: flex;
                gap: 15px;
                color: #999;
                font-size: 0.85em;
                margin-top: 10px;
            }

            .bug-actions {
                display: flex;
                gap: 10px;
                margin-top: 15px;
            }

            .bug-actions button {
                padding: 8px 15px;
                border: none;
                border-radius: 6px;
                background: #667eea;
                color: white;
                cursor: pointer;
                font-size: 0.9em;
                transition: transform 0.2s ease;
            }

            .bug-actions button:hover {
                transform: translateY(-2px);
            }
        `;
        document.head.appendChild(style);
    }
}

// Global instance
window.BugLog = new BugLogSystem();

// Auto-inject on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        BugLog.autoInject();
    });
} else {
    BugLog.autoInject();
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BugLogSystem;
}
