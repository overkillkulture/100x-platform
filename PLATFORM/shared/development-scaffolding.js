/**
 * DEVELOPMENT SCAFFOLDING SYSTEM
 * Like construction scaffolding - essential during building, removed for production
 *
 * Provides:
 * - Debug console panel (floating widget)
 * - Keyboard shortcuts for quick actions
 * - Test data generator
 * - State inspector/navigator
 * - Error injection for testing
 * - Performance monitoring
 * - One-command removal for production
 */

const DevScaffolding = {
    enabled: true, // Set to false in production
    version: '1.0.0',
    panelVisible: false,

    /**
     * Initialize scaffolding (call once per page)
     */
    init(config = {}) {
        if (!this.enabled) return;

        console.log('%c🔧 DEVELOPMENT SCAFFOLDING ACTIVE', 'color: #ff9800; font-size: 16px; font-weight: bold;');
        console.log('%cPress Ctrl+Shift+D to toggle debug panel', 'color: #ff9800; font-size: 12px;');
        console.log('%cType DevScaffolding.help() for all commands', 'color: #ff9800; font-size: 12px;');

        this.config = {
            productId: config.productId || 'unknown',
            productName: config.productName || 'Product',
            showOnLoad: config.showOnLoad || false,
            ...config
        };

        this.setupKeyboardShortcuts();
        this.createDebugPanel();
        this.startPerformanceMonitoring();
        this.injectQuickActions();

        if (this.config.showOnLoad) {
            this.showPanel();
        }

        // Log to scaffolding history
        this.log('Scaffolding initialized', { productId: this.config.productId });
    },

    /**
     * Create floating debug panel
     */
    createDebugPanel() {
        if (document.getElementById('devScaffoldingPanel')) return;

        const panel = document.createElement('div');
        panel.id = 'devScaffoldingPanel';
        panel.style.display = 'none';
        panel.innerHTML = `
            <style>
                #devScaffoldingPanel {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    width: 400px;
                    max-height: 80vh;
                    background: rgba(0, 0, 0, 0.95);
                    border: 2px solid #ff9800;
                    border-radius: 10px;
                    color: #fff;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    z-index: 999999;
                    overflow: hidden;
                    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.8);
                }

                .scaffold-header {
                    background: #ff9800;
                    color: #000;
                    padding: 10px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    font-weight: bold;
                    cursor: move;
                }

                .scaffold-close {
                    cursor: pointer;
                    font-size: 18px;
                    font-weight: bold;
                }

                .scaffold-body {
                    padding: 15px;
                    max-height: calc(80vh - 50px);
                    overflow-y: auto;
                }

                .scaffold-section {
                    margin-bottom: 20px;
                    border-bottom: 1px solid rgba(255, 152, 0, 0.3);
                    padding-bottom: 15px;
                }

                .scaffold-section:last-child {
                    border-bottom: none;
                }

                .scaffold-section h3 {
                    color: #ff9800;
                    margin-bottom: 10px;
                    font-size: 14px;
                }

                .scaffold-btn {
                    background: #ff9800;
                    color: #000;
                    border: none;
                    padding: 8px 12px;
                    margin: 3px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 11px;
                    font-weight: bold;
                    transition: all 0.2s ease;
                }

                .scaffold-btn:hover {
                    background: #ffa726;
                    transform: scale(1.05);
                }

                .scaffold-btn.danger {
                    background: #f44336;
                    color: #fff;
                }

                .scaffold-input {
                    width: 100%;
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid #ff9800;
                    color: #fff;
                    padding: 8px;
                    border-radius: 5px;
                    margin: 5px 0;
                    font-family: 'Courier New', monospace;
                }

                .scaffold-log {
                    background: rgba(0, 0, 0, 0.5);
                    padding: 10px;
                    border-radius: 5px;
                    max-height: 200px;
                    overflow-y: auto;
                    font-size: 10px;
                }

                .scaffold-log-entry {
                    margin: 3px 0;
                    opacity: 0.8;
                }

                .scaffold-log-entry.error {
                    color: #f44336;
                }

                .scaffold-log-entry.success {
                    color: #4caf50;
                }

                .scaffold-stat {
                    display: flex;
                    justify-content: space-between;
                    padding: 5px 0;
                    border-bottom: 1px solid rgba(255, 152, 0, 0.2);
                }

                .scaffold-stat-label {
                    opacity: 0.8;
                }

                .scaffold-stat-value {
                    color: #ff9800;
                    font-weight: bold;
                }
            </style>

            <div class="scaffold-header" id="scaffoldHeader">
                <div>🔧 DEV SCAFFOLDING</div>
                <div class="scaffold-close" onclick="DevScaffolding.hidePanel()">×</div>
            </div>

            <div class="scaffold-body">
                <!-- Product Info -->
                <div class="scaffold-section">
                    <h3>📦 Product Info</h3>
                    <div class="scaffold-stat">
                        <div class="scaffold-stat-label">Product:</div>
                        <div class="scaffold-stat-value" id="scaffoldProductName">-</div>
                    </div>
                    <div class="scaffold-stat">
                        <div class="scaffold-stat-label">ID:</div>
                        <div class="scaffold-stat-value" id="scaffoldProductId">-</div>
                    </div>
                    <div class="scaffold-stat">
                        <div class="scaffold-stat-label">URL:</div>
                        <div class="scaffold-stat-value" style="font-size: 9px;" id="scaffoldUrl">-</div>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="scaffold-section">
                    <h3>⚡ Quick Actions</h3>
                    <button class="scaffold-btn" onclick="DevScaffolding.clearAllData()">Clear All Data</button>
                    <button class="scaffold-btn" onclick="DevScaffolding.generateTestData()">Generate Test Data</button>
                    <button class="scaffold-btn" onclick="DevScaffolding.resetToStart()">Reset to Start</button>
                    <button class="scaffold-btn" onclick="DevScaffolding.skipToEnd()">Skip to End</button>
                    <button class="scaffold-btn" onclick="DevScaffolding.exportState()">Export State</button>
                    <button class="scaffold-btn" onclick="DevScaffolding.importState()">Import State</button>
                </div>

                <!-- State Inspector -->
                <div class="scaffold-section">
                    <h3>🔍 State Inspector</h3>
                    <div id="scaffoldStateInspector"></div>
                    <button class="scaffold-btn" onclick="DevScaffolding.refreshState()">Refresh State</button>
                </div>

                <!-- Error Testing -->
                <div class="scaffold-section">
                    <h3>💥 Error Testing</h3>
                    <button class="scaffold-btn danger" onclick="DevScaffolding.injectError('network')">Network Error</button>
                    <button class="scaffold-btn danger" onclick="DevScaffolding.injectError('validation')">Validation Error</button>
                    <button class="scaffold-btn danger" onclick="DevScaffolding.injectError('crash')">Crash Simulation</button>
                </div>

                <!-- Performance Monitor -->
                <div class="scaffold-section">
                    <h3>📊 Performance</h3>
                    <div class="scaffold-stat">
                        <div class="scaffold-stat-label">Load Time:</div>
                        <div class="scaffold-stat-value" id="scaffoldLoadTime">-</div>
                    </div>
                    <div class="scaffold-stat">
                        <div class="scaffold-stat-label">Memory:</div>
                        <div class="scaffold-stat-value" id="scaffoldMemory">-</div>
                    </div>
                    <div class="scaffold-stat">
                        <div class="scaffold-stat-label">Errors:</div>
                        <div class="scaffold-stat-value" id="scaffoldErrors">0</div>
                    </div>
                </div>

                <!-- Console Log -->
                <div class="scaffold-section">
                    <h3>📝 Scaffold Log</h3>
                    <div class="scaffold-log" id="scaffoldLog"></div>
                    <button class="scaffold-btn" onclick="DevScaffolding.clearLog()">Clear Log</button>
                </div>

                <!-- Keyboard Shortcuts -->
                <div class="scaffold-section">
                    <h3>⌨️ Keyboard Shortcuts</h3>
                    <div style="font-size: 10px; opacity: 0.8;">
                        <div>Ctrl+Shift+D - Toggle Panel</div>
                        <div>Ctrl+Shift+R - Reset All</div>
                        <div>Ctrl+Shift+T - Test Data</div>
                        <div>Ctrl+Shift+C - Clear Console</div>
                        <div>Ctrl+Shift+E - Export State</div>
                    </div>
                </div>

                <!-- Remove Scaffolding -->
                <div class="scaffold-section">
                    <h3>🚨 Production Mode</h3>
                    <button class="scaffold-btn danger" onclick="DevScaffolding.removeAllScaffolding()">
                        REMOVE ALL SCAFFOLDING
                    </button>
                    <div style="font-size: 10px; opacity: 0.6; margin-top: 10px;">
                        ⚠️ Removes all debug systems for production deployment
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(panel);

        // Make draggable
        this.makeDraggable();

        // Update info
        this.updatePanelInfo();
    },

    /**
     * Show debug panel
     */
    showPanel() {
        const panel = document.getElementById('devScaffoldingPanel');
        if (panel) {
            panel.style.display = 'block';
            this.panelVisible = true;
            this.refreshState();
            this.updatePerformanceStats();
        }
    },

    /**
     * Hide debug panel
     */
    hidePanel() {
        const panel = document.getElementById('devScaffoldingPanel');
        if (panel) {
            panel.style.display = 'none';
            this.panelVisible = false;
        }
    },

    /**
     * Toggle panel visibility
     */
    togglePanel() {
        if (this.panelVisible) {
            this.hidePanel();
        } else {
            this.showPanel();
        }
    },

    /**
     * Update panel info
     */
    updatePanelInfo() {
        document.getElementById('scaffoldProductName').textContent = this.config.productName;
        document.getElementById('scaffoldProductId').textContent = this.config.productId;
        document.getElementById('scaffoldUrl').textContent = window.location.pathname;
    },

    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (!this.enabled) return;

            // Ctrl+Shift+D - Toggle panel
            if (e.ctrlKey && e.shiftKey && e.key === 'D') {
                e.preventDefault();
                this.togglePanel();
            }

            // Ctrl+Shift+R - Reset all
            if (e.ctrlKey && e.shiftKey && e.key === 'R') {
                e.preventDefault();
                this.resetToStart();
            }

            // Ctrl+Shift+T - Generate test data
            if (e.ctrlKey && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                this.generateTestData();
            }

            // Ctrl+Shift+C - Clear console
            if (e.ctrlKey && e.shiftKey && e.key === 'C') {
                e.preventDefault();
                console.clear();
                this.log('Console cleared');
            }

            // Ctrl+Shift+E - Export state
            if (e.ctrlKey && e.shiftKey && e.key === 'E') {
                e.preventDefault();
                this.exportState();
            }
        });
    },

    /**
     * Clear all localStorage data
     */
    clearAllData() {
        if (confirm('Clear ALL localStorage data? This cannot be undone.')) {
            localStorage.clear();
            this.log('All data cleared', 'success');
            this.refreshState();
            alert('All data cleared! Page will reload.');
            location.reload();
        }
    },

    /**
     * Generate test data
     */
    generateTestData() {
        this.log('Generating test data...');

        // Generate test data for current product
        const testData = {
            [`test_${this.config.productId}_timestamp`]: new Date().toISOString(),
            [`test_${this.config.productId}_user`]: 'TestUser123',
            [`test_${this.config.productId}_completed`]: true,
            [`test_${this.config.productId}_score`]: Math.floor(Math.random() * 100),
            [`test_${this.config.productId}_feedback`]: 'Test feedback - auto-generated'
        };

        Object.entries(testData).forEach(([key, value]) => {
            localStorage.setItem(key, JSON.stringify(value));
        });

        this.log('Test data generated', 'success');
        this.refreshState();
    },

    /**
     * Reset to start
     */
    resetToStart() {
        if (confirm('Reset product to starting state?')) {
            // Clear product-specific data only
            Object.keys(localStorage).forEach(key => {
                if (key.includes(this.config.productId)) {
                    localStorage.removeItem(key);
                }
            });

            this.log('Reset to start', 'success');
            location.reload();
        }
    },

    /**
     * Skip to end (product-specific)
     */
    skipToEnd() {
        this.log('Skipping to end state...');
        alert('Product-specific skip logic should be implemented here');
        // Product would implement: window.productInstance.skipToEnd();
    },

    /**
     * Export state
     */
    exportState() {
        const state = {};
        Object.keys(localStorage).forEach(key => {
            state[key] = localStorage.getItem(key);
        });

        const json = JSON.stringify(state, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.config.productId}_state_${Date.now()}.json`;
        a.click();

        this.log('State exported', 'success');
    },

    /**
     * Import state
     */
    importState() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = (e) => {
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.onload = (event) => {
                try {
                    const state = JSON.parse(event.target.result);
                    Object.entries(state).forEach(([key, value]) => {
                        localStorage.setItem(key, value);
                    });
                    this.log('State imported', 'success');
                    alert('State imported! Page will reload.');
                    location.reload();
                } catch (error) {
                    this.log(`Import failed: ${error.message}`, 'error');
                    alert('Failed to import state');
                }
            };
            reader.readAsText(file);
        };
        input.click();
    },

    /**
     * Refresh state inspector
     */
    refreshState() {
        const container = document.getElementById('scaffoldStateInspector');
        if (!container) return;

        const items = [];
        Object.keys(localStorage).forEach(key => {
            if (key.includes(this.config.productId) || key.includes('approvals') || key.includes('consciousness')) {
                const value = localStorage.getItem(key);
                items.push(`
                    <div class="scaffold-stat">
                        <div class="scaffold-stat-label" style="font-size: 9px;">${key}:</div>
                        <div class="scaffold-stat-value" style="font-size: 9px;">${value.substring(0, 30)}${value.length > 30 ? '...' : ''}</div>
                    </div>
                `);
            }
        });

        container.innerHTML = items.length > 0
            ? items.join('')
            : '<div style="opacity: 0.5;">No state data found</div>';
    },

    /**
     * Inject error for testing
     */
    injectError(type) {
        this.log(`Injecting ${type} error...`, 'error');

        switch (type) {
            case 'network':
                throw new Error('SCAFFOLDING: Simulated network error');
            case 'validation':
                alert('SCAFFOLDING: Validation error injected');
                this.log('Validation error triggered', 'error');
                break;
            case 'crash':
                setTimeout(() => {
                    throw new Error('SCAFFOLDING: Simulated crash');
                }, 100);
                break;
        }
    },

    /**
     * Start performance monitoring
     */
    startPerformanceMonitoring() {
        // Track load time
        window.addEventListener('load', () => {
            const loadTime = performance.now();
            document.getElementById('scaffoldLoadTime').textContent = `${loadTime.toFixed(0)}ms`;
        });

        // Track errors
        window.addEventListener('error', (e) => {
            const errorCount = parseInt(document.getElementById('scaffoldErrors').textContent) + 1;
            document.getElementById('scaffoldErrors').textContent = errorCount;
            this.log(`Error: ${e.message}`, 'error');
        });

        // Update memory periodically
        setInterval(() => {
            if (performance.memory) {
                const used = (performance.memory.usedJSHeapSize / 1048576).toFixed(1);
                document.getElementById('scaffoldMemory').textContent = `${used} MB`;
            }
        }, 2000);
    },

    /**
     * Update performance stats
     */
    updatePerformanceStats() {
        // Refresh all stats
        if (performance.memory) {
            const used = (performance.memory.usedJSHeapSize / 1048576).toFixed(1);
            document.getElementById('scaffoldMemory').textContent = `${used} MB`;
        }
    },

    /**
     * Inject quick action buttons (floating)
     */
    injectQuickActions() {
        const quickBar = document.createElement('div');
        quickBar.id = 'scaffoldQuickBar';
        quickBar.innerHTML = `
            <style>
                #scaffoldQuickBar {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    background: rgba(255, 152, 0, 0.9);
                    color: #000;
                    padding: 10px 15px;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 14px;
                    cursor: pointer;
                    z-index: 999998;
                    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
                    transition: all 0.3s ease;
                }
                #scaffoldQuickBar:hover {
                    transform: scale(1.1);
                    background: rgba(255, 152, 0, 1);
                }
            </style>
            🔧 DEV MODE
        `;
        quickBar.onclick = () => this.togglePanel();
        document.body.appendChild(quickBar);
    },

    /**
     * Make panel draggable
     */
    makeDraggable() {
        const panel = document.getElementById('devScaffoldingPanel');
        const header = document.getElementById('scaffoldHeader');
        let isDragging = false;
        let currentX, currentY, initialX, initialY;

        header.addEventListener('mousedown', (e) => {
            isDragging = true;
            initialX = e.clientX - panel.offsetLeft;
            initialY = e.clientY - panel.offsetTop;
        });

        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                e.preventDefault();
                currentX = e.clientX - initialX;
                currentY = e.clientY - initialY;
                panel.style.left = currentX + 'px';
                panel.style.top = currentY + 'px';
                panel.style.right = 'auto';
            }
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
    },

    /**
     * Log to scaffold console
     */
    log(message, type = 'info') {
        const logContainer = document.getElementById('scaffoldLog');
        if (!logContainer) return;

        const entry = document.createElement('div');
        entry.className = `scaffold-log-entry ${type}`;
        entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;

        logContainer.appendChild(entry);
        logContainer.scrollTop = logContainer.scrollHeight;

        // Keep last 50 entries
        while (logContainer.children.length > 50) {
            logContainer.removeChild(logContainer.firstChild);
        }
    },

    /**
     * Clear scaffold log
     */
    clearLog() {
        document.getElementById('scaffoldLog').innerHTML = '';
        this.log('Log cleared');
    },

    /**
     * Remove ALL scaffolding (production mode)
     */
    removeAllScaffolding() {
        if (confirm('⚠️ REMOVE ALL DEVELOPMENT SCAFFOLDING?\n\nThis will:\n- Remove debug panel\n- Remove quick actions\n- Disable keyboard shortcuts\n- Clear scaffold data\n\nThis should only be done for production deployment!')) {
            if (confirm('Are you REALLY sure? This prepares for production.')) {
                // Remove panel
                const panel = document.getElementById('devScaffoldingPanel');
                if (panel) panel.remove();

                // Remove quick bar
                const quickBar = document.getElementById('scaffoldQuickBar');
                if (quickBar) quickBar.remove();

                // Disable scaffolding
                this.enabled = false;

                // Clear scaffold data from localStorage
                Object.keys(localStorage).forEach(key => {
                    if (key.startsWith('scaffold_') || key.startsWith('test_')) {
                        localStorage.removeItem(key);
                    }
                });

                console.log('%c🚀 SCAFFOLDING REMOVED - PRODUCTION MODE', 'color: #4caf50; font-size: 16px; font-weight: bold;');
                console.log('%cSet DevScaffolding.enabled = false in code for permanent removal', 'color: #4caf50; font-size: 12px;');

                alert('✅ Scaffolding removed!\n\nFor permanent removal, set:\nDevScaffolding.enabled = false\n\nOr remove the script tag entirely.');
            }
        }
    },

    /**
     * Help command
     */
    help() {
        console.log('%c🔧 DEVELOPMENT SCAFFOLDING COMMANDS', 'color: #ff9800; font-size: 16px; font-weight: bold;');
        console.log('%cPanel Commands:', 'color: #ff9800; font-size: 14px;');
        console.log('  DevScaffolding.showPanel() - Show debug panel');
        console.log('  DevScaffolding.hidePanel() - Hide debug panel');
        console.log('  DevScaffolding.togglePanel() - Toggle panel');
        console.log('');
        console.log('%cData Commands:', 'color: #ff9800; font-size: 14px;');
        console.log('  DevScaffolding.clearAllData() - Clear localStorage');
        console.log('  DevScaffolding.generateTestData() - Generate test data');
        console.log('  DevScaffolding.exportState() - Export current state');
        console.log('  DevScaffolding.importState() - Import state from file');
        console.log('');
        console.log('%cNavigation Commands:', 'color: #ff9800; font-size: 14px;');
        console.log('  DevScaffolding.resetToStart() - Reset to starting state');
        console.log('  DevScaffolding.skipToEnd() - Skip to end state');
        console.log('');
        console.log('%cKeyboard Shortcuts:', 'color: #ff9800; font-size: 14px;');
        console.log('  Ctrl+Shift+D - Toggle panel');
        console.log('  Ctrl+Shift+R - Reset all');
        console.log('  Ctrl+Shift+T - Generate test data');
        console.log('  Ctrl+Shift+C - Clear console');
        console.log('  Ctrl+Shift+E - Export state');
        console.log('');
        console.log('%cProduction:', 'color: #ff9800; font-size: 14px;');
        console.log('  DevScaffolding.removeAllScaffolding() - Remove all scaffolding');
    }
};

// Make available globally
window.DevScaffolding = DevScaffolding;

// Auto-initialize if in development
if (window.location.hostname === 'localhost' || window.location.hostname.includes('netlify.app')) {
    // Will be initialized by each product
    console.log('%c🔧 Development Scaffolding loaded', 'color: #ff9800; font-size: 12px;');
    console.log('%cCall DevScaffolding.init() to activate', 'color: #ff9800; font-size: 12px;');
}
