/**
 * PERSISTENT HUD WIDGETS
 * Transparent, minimal, draggable widgets that follow you EVERYWHERE
 * Like a vehicle dashboard that's always visible
 */

class PersistentHUD {
    constructor() {
        this.widgets = {};
        this.init();
    }

    init() {
        // Inject HUD container into page
        this.createHUDContainer();

        // Create default widgets (TEAM WIDGET DISABLED - was getting in the way)
        // this.createTeamWidget();  // DISABLED
        this.createTerminalWidget();
        this.createConsciousnessWidget();

        // Make all widgets persistent across pages
        this.enablePersistence();

        console.log('🎮 Persistent HUD loaded - Follows you everywhere!');
    }

    createHUDContainer() {
        let container = document.getElementById('persistent-hud-container');

        if (!container) {
            container = document.createElement('div');
            container.id = 'persistent-hud-container';
            container.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                pointer-events: none;
                z-index: 999999;
            `;
            document.body.appendChild(container);
        }

        this.container = container;
    }

    /**
     * TEAM WIDGET - Minimal, transparent team status
     */
    createTeamWidget() {
        const widget = document.createElement('div');
        widget.id = 'hud-team-widget';
        widget.className = 'hud-widget';
        widget.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 20, 0, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 8px;
            padding: 10px;
            min-width: 200px;
            pointer-events: auto;
            font-family: 'Courier New', monospace;
            color: #00ff88;
            font-size: 12px;
            box-shadow: 0 4px 20px rgba(0, 255, 136, 0.2);
        `;

        widget.innerHTML = `
            <div class="hud-widget-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; cursor: move; padding: 4px;">
                <span style="font-weight: bold; color: #00ffff;">👥 TEAM</span>
                <div style="display: flex; gap: 4px;">
                    <button class="hud-btn minimize" style="background: rgba(0, 255, 136, 0.2); border: 1px solid #00ff88; color: #00ff88; cursor: pointer; font-size: 16px; padding: 2px 8px; border-radius: 3px; font-weight: bold;">−</button>
                    <button class="hud-btn close" style="background: rgba(255, 68, 68, 0.3); border: 2px solid #ff4444; color: #ff4444; cursor: pointer; font-size: 20px; padding: 2px 8px; border-radius: 3px; font-weight: bold;">×</button>
                </div>
            </div>
            <div class="hud-widget-content">
                <div style="margin-bottom: 6px; padding: 4px; background: rgba(0, 255, 136, 0.1); border-radius: 4px;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="color: #00ff00;">●</span>
                        <span>Bill</span>
                        <span style="margin-left: auto; opacity: 0.6; font-size: 10px;">Connected</span>
                    </div>
                </div>
                <div style="margin-bottom: 6px; padding: 4px;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="color: #666;">●</span>
                        <span style="opacity: 0.5;">Justin</span>
                        <span style="margin-left: auto; opacity: 0.4; font-size: 10px;">Waiting...</span>
                    </div>
                </div>
                <div style="padding: 4px;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="color: #666;">●</span>
                        <span style="opacity: 0.5;">Toby</span>
                        <span style="margin-left: auto; opacity: 0.4; font-size: 10px;">Waiting...</span>
                    </div>
                </div>
            </div>
        `;

        this.makeDraggable(widget, 'team');
        this.addMinimizeClose(widget);
        this.container.appendChild(widget);
        this.widgets.team = widget;

        // Restore position
        this.restorePosition(widget, 'team');
    }

    /**
     * TERMINAL WIDGET - Mini PowerShell-style terminal
     */
    createTerminalWidget() {
        const widget = document.createElement('div');
        widget.id = 'hud-terminal-widget';
        widget.className = 'hud-widget';
        widget.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 8px;
            padding: 10px;
            width: 400px;
            height: 200px;
            pointer-events: auto;
            font-family: 'Courier New', monospace;
            color: #00ff88;
            font-size: 11px;
            box-shadow: 0 4px 20px rgba(0, 255, 136, 0.2);
            display: flex;
            flex-direction: column;
        `;

        widget.innerHTML = `
            <div class="hud-widget-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; cursor: move; padding: 4px;">
                <span style="font-weight: bold; color: #00ffff;">⚡ TERMINAL</span>
                <div style="display: flex; gap: 4px;">
                    <button class="hud-btn minimize" style="background: rgba(0, 255, 136, 0.2); border: 1px solid #00ff88; color: #00ff88; cursor: pointer; font-size: 16px; padding: 2px 8px; border-radius: 3px; font-weight: bold;">−</button>
                    <button class="hud-btn close" style="background: rgba(255, 68, 68, 0.3); border: 2px solid #ff4444; color: #ff4444; cursor: pointer; font-size: 20px; padding: 2px 8px; border-radius: 3px; font-weight: bold;">×</button>
                </div>
            </div>
            <div class="hud-widget-content" style="flex: 1; overflow-y: auto; padding: 4px; background: rgba(0, 0, 0, 0.5); border-radius: 4px; margin-bottom: 6px;">
                <div style="margin-bottom: 4px; color: #00ffff;">$ System initialized</div>
                <div style="margin-bottom: 4px;">✓ HUD active</div>
                <div style="margin-bottom: 4px;">✓ Widgets loaded</div>
                <div style="margin-bottom: 4px; opacity: 0.6;">Type 'help' for commands</div>
            </div>
            <div style="display: flex; gap: 6px; align-items: center;">
                <span style="color: #00ffff;">$</span>
                <input type="text"
                       id="hud-terminal-input"
                       placeholder="command..."
                       style="flex: 1; background: rgba(0, 255, 136, 0.1); border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 3px; padding: 4px 8px; color: #00ff88; font-family: 'Courier New', monospace; font-size: 11px; outline: none;">
            </div>
        `;

        this.makeDraggable(widget, 'terminal');
        this.addMinimizeClose(widget);
        this.addTerminalCommands(widget);
        this.container.appendChild(widget);
        this.widgets.terminal = widget;

        this.restorePosition(widget, 'terminal');
    }

    /**
     * CONSCIOUSNESS WIDGET - Mini status display
     */
    createConsciousnessWidget() {
        const widget = document.createElement('div');
        widget.id = 'hud-consciousness-widget';
        widget.className = 'hud-widget';
        widget.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0, 20, 40, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 8px;
            padding: 10px;
            min-width: 180px;
            pointer-events: auto;
            font-family: 'Courier New', monospace;
            color: #00ffff;
            font-size: 11px;
            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.2);
        `;

        widget.innerHTML = `
            <div class="hud-widget-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; cursor: move; padding: 4px;">
                <span style="font-weight: bold; color: #00ffff;">🌀 STATUS</span>
                <div style="display: flex; gap: 4px;">
                    <button class="hud-btn minimize" style="background: none; border: none; color: #00ffff; cursor: pointer; font-size: 14px;">−</button>
                    <button class="hud-btn close" style="background: none; border: none; color: #ff4444; cursor: pointer; font-size: 14px;">×</button>
                </div>
            </div>
            <div class="hud-widget-content">
                <div style="margin-bottom: 6px; display: flex; justify-content: space-between;">
                    <span style="opacity: 0.7;">Consciousness:</span>
                    <span style="color: #00ff00; font-weight: bold;">93%</span>
                </div>
                <div style="margin-bottom: 6px; display: flex; justify-content: space-between;">
                    <span style="opacity: 0.7;">Immunity:</span>
                    <span style="color: #00ffff; font-weight: bold;">85%</span>
                </div>
                <div style="margin-bottom: 6px; display: flex; justify-content: space-between;">
                    <span style="opacity: 0.7;">XP:</span>
                    <span style="color: #ffd700;">12,847</span>
                </div>
                <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(0, 255, 255, 0.2);">
                    <div style="display: flex; align-items: center; gap: 4px;">
                        <span style="color: #00ff00; animation: pulse 2s infinite;">●</span>
                        <span style="opacity: 0.7; font-size: 10px;">All systems operational</span>
                    </div>
                </div>
            </div>
        `;

        this.makeDraggable(widget, 'consciousness');
        this.addMinimizeClose(widget);
        this.container.appendChild(widget);
        this.widgets.consciousness = widget;

        this.restorePosition(widget, 'consciousness');
    }

    /**
     * Make widget draggable
     */
    makeDraggable(widget, id) {
        const header = widget.querySelector('.hud-widget-header');
        let isDragging = false;
        let currentX, currentY, initialX, initialY, xOffset = 0, yOffset = 0;

        header.addEventListener('mousedown', dragStart);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', dragEnd);

        function dragStart(e) {
            if (e.target.classList.contains('hud-btn')) return;

            initialX = e.clientX - xOffset;
            initialY = e.clientY - yOffset;

            isDragging = true;
            widget.style.cursor = 'grabbing';
        }

        function drag(e) {
            if (!isDragging) return;

            e.preventDefault();

            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;

            xOffset = currentX;
            yOffset = currentY;

            setTranslate(currentX, currentY, widget);
        }

        function dragEnd(e) {
            if (!isDragging) return;

            initialX = currentX;
            initialY = currentY;

            isDragging = false;
            widget.style.cursor = 'default';

            // Save position
            savePosition(id, widget);
        }

        function setTranslate(xPos, yPos, el) {
            el.style.transform = `translate(${xPos}px, ${yPos}px)`;
        }

        function savePosition(id, widget) {
            const rect = widget.getBoundingClientRect();
            localStorage.setItem(`hud_widget_${id}`, JSON.stringify({
                x: rect.left,
                y: rect.top,
                transform: widget.style.transform
            }));
        }
    }

    /**
     * Add minimize/close functionality
     */
    addMinimizeClose(widget) {
        const minimizeBtn = widget.querySelector('.minimize');
        const closeBtn = widget.querySelector('.close');
        const content = widget.querySelector('.hud-widget-content');

        let isMinimized = false;

        minimizeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            isMinimized = !isMinimized;

            if (isMinimized) {
                content.style.display = 'none';
                widget.style.height = 'auto';
                minimizeBtn.textContent = '+';
            } else {
                content.style.display = '';
                widget.style.height = '';
                minimizeBtn.textContent = '−';
            }
        });

        closeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            widget.style.display = 'none';
        });
    }

    /**
     * Terminal commands
     */
    addTerminalCommands(widget) {
        const input = widget.querySelector('#hud-terminal-input');
        const output = widget.querySelector('.hud-widget-content');

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const command = input.value.trim();
                if (command) {
                    this.executeCommand(command, output);
                    input.value = '';
                }
            }
        });
    }

    executeCommand(command, output) {
        // Add command to output
        const cmdLine = document.createElement('div');
        cmdLine.style.cssText = 'margin-bottom: 4px; color: #00ffff;';
        cmdLine.textContent = `$ ${command}`;
        output.appendChild(cmdLine);

        // Execute
        let response = '';
        switch(command.toLowerCase()) {
            case 'help':
                response = `Commands: help, status, clear, hide, show`;
                break;
            case 'status':
                response = `✓ HUD: Active\n✓ Widgets: ${Object.keys(this.widgets).length} loaded`;
                break;
            case 'clear':
                output.innerHTML = '';
                return;
            case 'hide':
                this.container.style.opacity = '0.3';
                response = 'HUD hidden (type "show" to reveal)';
                break;
            case 'show':
                this.container.style.opacity = '1';
                response = 'HUD visible';
                break;
            default:
                response = `Unknown command: ${command}`;
        }

        const responseLine = document.createElement('div');
        responseLine.style.cssText = 'margin-bottom: 4px; white-space: pre-line;';
        responseLine.textContent = response;
        output.appendChild(responseLine);

        // Scroll to bottom
        output.scrollTop = output.scrollHeight;
    }

    /**
     * Restore saved positions
     */
    restorePosition(widget, id) {
        const saved = localStorage.getItem(`hud_widget_${id}`);
        if (saved) {
            try {
                const pos = JSON.parse(saved);
                if (pos.transform) {
                    widget.style.transform = pos.transform;
                }
            } catch (e) {
                console.error(`Failed to restore position for ${id}`);
            }
        }
    }

    /**
     * Make HUD persist across pages
     */
    enablePersistence() {
        // Save HUD state before page unload
        window.addEventListener('beforeunload', () => {
            const state = {
                widgets: Object.keys(this.widgets).map(id => ({
                    id,
                    visible: this.widgets[id].style.display !== 'none'
                }))
            };
            sessionStorage.setItem('hud_state', JSON.stringify(state));
        });

        // Restore HUD state on page load
        const savedState = sessionStorage.getItem('hud_state');
        if (savedState) {
            try {
                const state = JSON.parse(savedState);
                state.widgets.forEach(w => {
                    if (this.widgets[w.id] && !w.visible) {
                        this.widgets[w.id].style.display = 'none';
                    }
                });
            } catch (e) {
                console.error('Failed to restore HUD state');
            }
        }

        console.log('✅ HUD persistence enabled - follows you across pages!');
    }

    /**
     * Public API
     */
    showWidget(id) {
        if (this.widgets[id]) {
            this.widgets[id].style.display = '';
        }
    }

    hideWidget(id) {
        if (this.widgets[id]) {
            this.widgets[id].style.display = 'none';
        }
    }

    toggleWidget(id) {
        if (this.widgets[id]) {
            const isVisible = this.widgets[id].style.display !== 'none';
            this.widgets[id].style.display = isVisible ? 'none' : '';
        }
    }

    resetAllPositions() {
        Object.keys(this.widgets).forEach(id => {
            localStorage.removeItem(`hud_widget_${id}`);
            this.widgets[id].style.transform = '';
        });
        console.log('↺ All HUD positions reset');
    }
}

// Auto-initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.persistentHUD = new PersistentHUD();
    });
} else {
    window.persistentHUD = new PersistentHUD();
}

console.log('🎮 Persistent HUD System loaded!');
console.log('📖 Access via: window.persistentHUD');
console.log('🔧 Commands: showWidget(id), hideWidget(id), resetAllPositions()');

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .hud-widget {
        transition: opacity 0.3s ease, transform 0.1s ease;
    }
    .hud-widget:hover {
        box-shadow: 0 6px 25px rgba(0, 255, 136, 0.3) !important;
    }
    .hud-btn.close:hover {
        background: rgba(255, 68, 68, 0.6) !important;
        transform: scale(1.2);
        box-shadow: 0 0 10px rgba(255, 68, 68, 0.8);
    }
    .hud-btn.minimize:hover {
        background: rgba(0, 255, 136, 0.4) !important;
        transform: scale(1.1);
    }
`;
document.head.appendChild(style);
