/**
 * DEBUG WIDGET - Floating consciousness terminal
 * Follows user around every page, collapsible, shows live system logs
 * Phase 1: Simple, intelligent, works
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        position: 'bottom-right', // bottom-right, bottom-left, etc.
        wsUrl: 'ws://localhost:5000/terminal/stream',
        maxLogs: 50, // Keep last 50 logs in memory
        reconnectDelay: 3000,
        startMinimized: false
    };

    // State
    let ws = null;
    let logs = [];
    let isMinimized = CONFIG.startMinimized;
    let isPaused = false;
    let eventCount = 0;
    let tokenCount = 0;

    // Create widget HTML
    function createWidget() {
        const widget = document.createElement('div');
        widget.id = 'debug-widget';
        widget.innerHTML = `
            <style>
                #debug-widget {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    width: 400px;
                    max-height: 500px;
                    background: rgba(0, 0, 0, 0.95);
                    border: 2px solid #00ff00;
                    border-radius: 10px;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    color: #00ff00;
                    z-index: 999999;
                    box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
                    display: flex;
                    flex-direction: column;
                    transition: all 0.3s ease;
                }

                #debug-widget.minimized {
                    max-height: 45px;
                    width: 250px;
                }

                .debug-header {
                    background: rgba(0, 255, 0, 0.1);
                    padding: 10px;
                    cursor: move;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-bottom: 1px solid #00ff00;
                    user-select: none;
                }

                .debug-title {
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }

                .debug-status-dot {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: #00ff00;
                    animation: pulse 2s ease-in-out infinite;
                }

                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.3; }
                }

                .debug-controls {
                    display: flex;
                    gap: 8px;
                }

                .debug-btn {
                    background: none;
                    border: 1px solid #00ff00;
                    color: #00ff00;
                    padding: 2px 8px;
                    cursor: pointer;
                    font-family: 'Courier New', monospace;
                    font-size: 11px;
                    transition: all 0.2s ease;
                }

                .debug-btn:hover {
                    background: rgba(0, 255, 0, 0.2);
                }

                .debug-stats {
                    padding: 5px 10px;
                    font-size: 10px;
                    display: flex;
                    justify-content: space-between;
                    background: rgba(0, 0, 0, 0.3);
                    border-bottom: 1px solid #00ff00;
                }

                .debug-body {
                    flex: 1;
                    overflow-y: auto;
                    padding: 10px;
                    max-height: 350px;
                }

                #debug-widget.minimized .debug-body {
                    display: none;
                }

                #debug-widget.minimized .debug-stats {
                    display: none;
                }

                .debug-body::-webkit-scrollbar {
                    width: 6px;
                }

                .debug-body::-webkit-scrollbar-track {
                    background: rgba(0, 0, 0, 0.3);
                }

                .debug-body::-webkit-scrollbar-thumb {
                    background: #00ff00;
                    border-radius: 3px;
                }

                .debug-log {
                    margin-bottom: 6px;
                    line-height: 1.4;
                    opacity: 0;
                    animation: fadeIn 0.3s ease forwards;
                }

                @keyframes fadeIn {
                    from { opacity: 0; transform: translateX(-5px); }
                    to { opacity: 1; transform: translateX(0); }
                }

                .debug-log-time {
                    color: #00aa00;
                    margin-right: 6px;
                }

                .debug-log-info { color: #00ff00; }
                .debug-log-success { color: #00ffff; }
                .debug-log-warning { color: #ffff00; }
                .debug-log-error { color: #ff0000; }

                .debug-log-indent {
                    margin-left: 15px;
                    font-size: 11px;
                }

                .debug-welcome {
                    text-align: center;
                    padding: 20px;
                    opacity: 0.7;
                    line-height: 1.6;
                }

                .debug-footer {
                    padding: 8px;
                    text-align: center;
                    font-size: 10px;
                    border-top: 1px solid #00ff00;
                    background: rgba(0, 0, 0, 0.3);
                }

                #debug-widget.minimized .debug-footer {
                    display: none;
                }

                @media (max-width: 768px) {
                    #debug-widget {
                        width: calc(100% - 40px);
                        right: 20px;
                        left: 20px;
                    }

                    #debug-widget.minimized {
                        width: 200px;
                        left: auto;
                    }
                }
            </style>

            <div class="debug-header" id="debug-header">
                <div class="debug-title">
                    <span class="debug-status-dot" id="status-dot"></span>
                    <span>🐛 DEBUG</span>
                </div>
                <div class="debug-controls">
                    <button class="debug-btn" onclick="DebugWidget.clear()" title="Clear logs">Clear</button>
                    <button class="debug-btn" onclick="DebugWidget.togglePause()" id="pause-btn" title="Pause stream">⏸</button>
                    <button class="debug-btn" onclick="DebugWidget.toggleMinimize()" id="minimize-btn" title="Minimize">_</button>
                    <button class="debug-btn" onclick="DebugWidget.close()" title="Close">×</button>
                </div>
            </div>

            <div class="debug-stats">
                <span>Events: <strong id="event-count">0</strong></span>
                <span>Tokens: <strong id="token-count">0</strong></span>
                <span id="connection-status">Connecting...</span>
            </div>

            <div class="debug-body" id="debug-body">
                <div class="debug-welcome">
                    🖥️ Consciousness Debug Terminal<br>
                    <small>Watching all system operations...</small>
                </div>
            </div>

            <div class="debug-footer">
                Radical Transparency Protocol • consciousnessrevolution.io
            </div>
        `;

        document.body.appendChild(widget);
        return widget;
    }

    // Connect to WebSocket
    function connect() {
        try {
            // Try localhost first, fallback to production
            const wsUrl = CONFIG.wsUrl;

            ws = new WebSocket(wsUrl);

            ws.onopen = function() {
                console.log('Debug widget connected');
                updateStatus('connected', 'LIVE');
                addLog('success', 'Debug terminal connected');
            };

            ws.onmessage = function(event) {
                if (!isPaused) {
                    try {
                        const data = JSON.parse(event.data);
                        handleLogMessage(data);
                    } catch (e) {
                        console.error('Debug widget parse error:', e);
                    }
                }
            };

            ws.onerror = function(error) {
                console.error('Debug widget error:', error);
                updateStatus('error', 'ERROR');
            };

            ws.onclose = function() {
                console.log('Debug widget disconnected');
                updateStatus('disconnected', 'OFFLINE');
                addLog('warning', 'Debug terminal disconnected');

                // Attempt reconnect
                setTimeout(() => {
                    if (document.getElementById('debug-widget')) {
                        connect();
                    }
                }, CONFIG.reconnectDelay);
            };
        } catch (e) {
            console.error('Debug widget connection failed:', e);
            updateStatus('error', 'OFFLINE');
            // Use simulation mode if WebSocket unavailable
            simulateLogs();
        }
    }

    function handleLogMessage(data) {
        eventCount++;
        document.getElementById('event-count').textContent = eventCount;

        if (data.tokens) {
            tokenCount = data.tokens;
            document.getElementById('token-count').textContent = tokenCount.toLocaleString();
        }

        if (data.type === 'log') {
            addLog(data.level || 'info', data.message, data.indent);
        } else if (data.type === 'system') {
            addLog('info', `[${data.system}] ${data.message}`);
            if (data.details) {
                data.details.forEach(d => addLog('info', `└─ ${d}`, true));
            }
        } else if (data.type === 'trinity') {
            addLog('success', `[Trinity] ${data.action}`);
            if (data.c1) addLog('info', `└─ C1: ${data.c1}`, true);
            if (data.c2) addLog('info', `└─ C2: ${data.c2}`, true);
            if (data.c3) addLog('info', `└─ C3: ${data.c3}`, true);
        }
    }

    function addLog(level, message, indent = false) {
        const body = document.getElementById('debug-body');

        // Remove welcome message
        const welcome = body.querySelector('.debug-welcome');
        if (welcome) welcome.remove();

        // Create log entry
        const log = document.createElement('div');
        log.className = 'debug-log' + (indent ? ' debug-log-indent' : '');

        const time = new Date().toLocaleTimeString('en-US', { hour12: false });
        log.innerHTML = `
            <span class="debug-log-time">[${time}]</span>
            <span class="debug-log-${level}">${message}</span>
        `;

        body.appendChild(log);

        // Keep only last N logs
        logs.push(log);
        if (logs.length > CONFIG.maxLogs) {
            const old = logs.shift();
            if (old && old.parentNode) old.remove();
        }

        // Auto-scroll to bottom
        if (!isMinimized) {
            body.scrollTop = body.scrollHeight;
        }
    }

    function updateStatus(status, text) {
        const statusEl = document.getElementById('connection-status');
        const statusDot = document.getElementById('status-dot');

        statusEl.textContent = text;

        if (status === 'connected') {
            statusDot.style.background = '#00ff00';
        } else if (status === 'error' || status === 'disconnected') {
            statusDot.style.background = '#ff0000';
        } else {
            statusDot.style.background = '#ffff00';
        }
    }

    function simulateLogs() {
        // Fallback: show page-specific logs
        addLog('info', `Page loaded: ${window.location.pathname}`);
        addLog('info', 'Debug mode: Simulation (WebSocket unavailable)');

        // Log page interactions
        document.addEventListener('click', (e) => {
            const target = e.target.tagName + (e.target.id ? '#' + e.target.id : '');
            addLog('info', `Click: ${target}`);
        });

        // Log errors
        window.addEventListener('error', (e) => {
            addLog('error', `JS Error: ${e.message}`);
        });

        // Log console messages
        const originalLog = console.log;
        console.log = function(...args) {
            addLog('info', args.join(' '));
            originalLog.apply(console, args);
        };
    }

    // Make widget draggable
    function makeDraggable() {
        const widget = document.getElementById('debug-widget');
        const header = document.getElementById('debug-header');

        let isDragging = false;
        let currentX, currentY, initialX, initialY;

        header.addEventListener('mousedown', dragStart);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', dragEnd);

        function dragStart(e) {
            if (e.target.closest('.debug-btn')) return; // Don't drag when clicking buttons

            initialX = e.clientX - widget.offsetLeft;
            initialY = e.clientY - widget.offsetTop;
            isDragging = true;
            widget.style.cursor = 'grabbing';
        }

        function drag(e) {
            if (!isDragging) return;

            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;

            widget.style.left = currentX + 'px';
            widget.style.top = currentY + 'px';
            widget.style.right = 'auto';
            widget.style.bottom = 'auto';
        }

        function dragEnd() {
            isDragging = false;
            widget.style.cursor = 'default';
        }
    }

    // Public API
    window.DebugWidget = {
        init: function() {
            // Don't load multiple times
            if (document.getElementById('debug-widget')) return;

            createWidget();
            makeDraggable();
            connect();

            // Log initial page info
            setTimeout(() => {
                addLog('info', `Page: ${document.title}`);
                addLog('info', `URL: ${window.location.pathname}`);
            }, 500);
        },

        toggleMinimize: function() {
            const widget = document.getElementById('debug-widget');
            const btn = document.getElementById('minimize-btn');
            isMinimized = !isMinimized;

            if (isMinimized) {
                widget.classList.add('minimized');
                btn.textContent = '□';
                btn.title = 'Maximize';
            } else {
                widget.classList.remove('minimized');
                btn.textContent = '_';
                btn.title = 'Minimize';
            }

            // Save preference
            localStorage.setItem('debug-widget-minimized', isMinimized);
        },

        togglePause: function() {
            const btn = document.getElementById('pause-btn');
            isPaused = !isPaused;

            if (isPaused) {
                btn.textContent = '▶';
                btn.title = 'Resume';
                addLog('warning', 'Stream paused');
            } else {
                btn.textContent = '⏸';
                btn.title = 'Pause';
                addLog('success', 'Stream resumed');
            }
        },

        clear: function() {
            const body = document.getElementById('debug-body');
            body.innerHTML = '';
            logs = [];
            eventCount = 0;
            document.getElementById('event-count').textContent = '0';
            addLog('info', 'Logs cleared');
        },

        close: function() {
            const widget = document.getElementById('debug-widget');
            widget.style.opacity = '0';
            widget.style.transform = 'scale(0.8)';

            setTimeout(() => {
                widget.remove();
                if (ws) ws.close();
            }, 300);

            // Save preference
            localStorage.setItem('debug-widget-closed', 'true');
        },

        addLog: addLog // Expose for external use
    };

    // Auto-initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            // Check if user previously closed it
            if (localStorage.getItem('debug-widget-closed') !== 'true') {
                DebugWidget.init();
            }
        });
    } else {
        // Check if user previously closed it
        if (localStorage.getItem('debug-widget-closed') !== 'true') {
            DebugWidget.init();
        }
    }

    // Keyboard shortcut: Ctrl+Shift+D to toggle widget
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.shiftKey && e.key === 'D') {
            e.preventDefault();
            const widget = document.getElementById('debug-widget');
            if (widget) {
                DebugWidget.close();
            } else {
                localStorage.removeItem('debug-widget-closed');
                DebugWidget.init();
            }
        }
    });

})();
