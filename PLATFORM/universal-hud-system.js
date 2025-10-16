/**
 * UNIVERSAL HUD SYSTEM
 * Draggable, resizable panels for the 100X Platform
 * Supports: Team board, Terminal, Consciousness metrics, Any widget
 */

class UniversalHUD {
    constructor() {
        this.panels = new Map();
        this.activePanel = null;
        this.init();
    }

    init() {
        // Load saved panel positions
        this.loadPositions();

        // Initialize drag system
        this.initDragSystem();

        // Add global keyboard shortcuts
        this.initKeyboardShortcuts();

        console.log('🎮 Universal HUD System initialized');
    }

    /**
     * Register a draggable panel
     */
    registerPanel(id, element, options = {}) {
        const panel = {
            id,
            element,
            isDragging: false,
            isMinimized: options.minimized || false,
            isLocked: options.locked || false,
            startX: 0,
            startY: 0,
            currentX: 0,
            currentY: 0,
            zIndex: options.zIndex || 1000,
            ...options
        };

        // Add HUD controls if not present
        this.addHUDControls(panel);

        // Restore saved position
        this.restorePosition(panel);

        this.panels.set(id, panel);
        console.log(`✅ Panel registered: ${id}`);

        return panel;
    }

    /**
     * Add drag handle and controls to panel
     */
    addHUDControls(panel) {
        const element = panel.element;

        // Check if controls already exist
        if (element.querySelector('.hud-controls')) return;

        // Create control bar
        const controlBar = document.createElement('div');
        controlBar.className = 'hud-controls';
        controlBar.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 30px;
            background: rgba(0, 255, 136, 0.1);
            border-bottom: 1px solid rgba(0, 255, 136, 0.3);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 10px;
            cursor: move;
            user-select: none;
            z-index: 10;
        `;

        // Drag handle
        const dragHandle = document.createElement('div');
        dragHandle.className = 'hud-drag-handle';
        dragHandle.innerHTML = `<span style="color: #00ff88; font-size: 12px;">⋮⋮ ${panel.title || panel.id}</span>`;

        // Control buttons
        const controls = document.createElement('div');
        controls.style.cssText = 'display: flex; gap: 8px;';

        // Minimize button
        const minimizeBtn = this.createButton('−', 'Minimize', () => this.toggleMinimize(panel.id));

        // Lock button
        const lockBtn = this.createButton('🔓', 'Lock Position', () => this.toggleLock(panel.id));

        // Reset button
        const resetBtn = this.createButton('↺', 'Reset Position', () => this.resetPosition(panel.id));

        // Close button
        const closeBtn = this.createButton('×', 'Close', () => this.closePanel(panel.id));

        controls.appendChild(minimizeBtn);
        controls.appendChild(lockBtn);
        controls.appendChild(resetBtn);
        controls.appendChild(closeBtn);

        controlBar.appendChild(dragHandle);
        controlBar.appendChild(controls);

        // Insert at top of panel
        element.style.position = 'fixed';
        element.insertBefore(controlBar, element.firstChild);

        // Add padding to content
        Array.from(element.children).forEach(child => {
            if (!child.classList.contains('hud-controls')) {
                child.style.marginTop = '30px';
            }
        });

        // Make draggable
        controlBar.addEventListener('mousedown', (e) => this.startDrag(e, panel.id));
    }

    createButton(text, title, onClick) {
        const btn = document.createElement('button');
        btn.textContent = text;
        btn.title = title;
        btn.style.cssText = `
            background: rgba(0, 255, 136, 0.2);
            border: 1px solid rgba(0, 255, 136, 0.5);
            color: #00ff88;
            width: 24px;
            height: 24px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            line-height: 1;
            transition: all 0.2s ease;
        `;
        btn.addEventListener('mouseenter', () => {
            btn.style.background = 'rgba(0, 255, 136, 0.3)';
            btn.style.boxShadow = '0 0 8px rgba(0, 255, 136, 0.5)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.background = 'rgba(0, 255, 136, 0.2)';
            btn.style.boxShadow = 'none';
        });
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            onClick();
        });
        return btn;
    }

    /**
     * Drag system
     */
    initDragSystem() {
        document.addEventListener('mousemove', (e) => this.drag(e));
        document.addEventListener('mouseup', (e) => this.endDrag(e));
    }

    startDrag(e, panelId) {
        const panel = this.panels.get(panelId);
        if (!panel || panel.isLocked) return;

        panel.isDragging = true;
        this.activePanel = panelId;

        const rect = panel.element.getBoundingClientRect();
        panel.startX = e.clientX - rect.left;
        panel.startY = e.clientY - rect.top;

        panel.element.style.cursor = 'grabbing';
        panel.element.style.zIndex = ++this.globalZIndex || 10000;

        e.preventDefault();
    }

    drag(e) {
        if (!this.activePanel) return;

        const panel = this.panels.get(this.activePanel);
        if (!panel || !panel.isDragging) return;

        e.preventDefault();

        panel.currentX = e.clientX - panel.startX;
        panel.currentY = e.clientY - panel.startY;

        // Keep within viewport
        const maxX = window.innerWidth - panel.element.offsetWidth;
        const maxY = window.innerHeight - panel.element.offsetHeight;

        panel.currentX = Math.max(0, Math.min(panel.currentX, maxX));
        panel.currentY = Math.max(0, Math.min(panel.currentY, maxY));

        panel.element.style.left = panel.currentX + 'px';
        panel.element.style.top = panel.currentY + 'px';
        panel.element.style.right = 'auto';
        panel.element.style.bottom = 'auto';
    }

    endDrag(e) {
        if (!this.activePanel) return;

        const panel = this.panels.get(this.activePanel);
        if (!panel) return;

        panel.isDragging = false;
        panel.element.style.cursor = 'default';

        // Save position
        this.savePosition(panel);

        this.activePanel = null;
    }

    /**
     * Panel controls
     */
    toggleMinimize(panelId) {
        const panel = this.panels.get(panelId);
        if (!panel) return;

        panel.isMinimized = !panel.isMinimized;

        if (panel.isMinimized) {
            panel.originalHeight = panel.element.style.height || panel.element.offsetHeight + 'px';
            panel.element.style.height = '30px';
            panel.element.style.overflow = 'hidden';
        } else {
            panel.element.style.height = panel.originalHeight || 'auto';
            panel.element.style.overflow = 'visible';
        }

        this.savePosition(panel);
    }

    toggleLock(panelId) {
        const panel = this.panels.get(panelId);
        if (!panel) return;

        panel.isLocked = !panel.isLocked;

        const lockBtn = panel.element.querySelector('.hud-controls button:nth-child(2)');
        if (lockBtn) {
            lockBtn.textContent = panel.isLocked ? '🔒' : '🔓';
            lockBtn.title = panel.isLocked ? 'Unlock Position' : 'Lock Position';
        }

        const controlBar = panel.element.querySelector('.hud-controls');
        if (controlBar) {
            controlBar.style.cursor = panel.isLocked ? 'default' : 'move';
        }

        this.savePosition(panel);
    }

    resetPosition(panelId) {
        const panel = this.panels.get(panelId);
        if (!panel) return;

        // Remove saved position
        localStorage.removeItem(`hud_panel_${panelId}`);

        // Reset to default
        panel.element.style.left = '';
        panel.element.style.top = '';
        panel.element.style.right = '';
        panel.element.style.bottom = '';
        panel.currentX = 0;
        panel.currentY = 0;

        console.log(`↺ Panel reset: ${panelId}`);
    }

    closePanel(panelId) {
        const panel = this.panels.get(panelId);
        if (!panel) return;

        panel.element.style.display = 'none';
        this.panels.delete(panelId);

        console.log(`✕ Panel closed: ${panelId}`);
    }

    showPanel(panelId) {
        const panel = this.panels.get(panelId);
        if (!panel) return;

        panel.element.style.display = '';
        console.log(`✓ Panel shown: ${panelId}`);
    }

    /**
     * Position persistence
     */
    savePosition(panel) {
        const position = {
            x: panel.currentX,
            y: panel.currentY,
            minimized: panel.isMinimized,
            locked: panel.isLocked,
            zIndex: panel.element.style.zIndex
        };

        localStorage.setItem(`hud_panel_${panel.id}`, JSON.stringify(position));
    }

    restorePosition(panel) {
        const saved = localStorage.getItem(`hud_panel_${panel.id}`);
        if (!saved) return;

        try {
            const position = JSON.parse(saved);

            if (position.x !== undefined && position.y !== undefined) {
                panel.element.style.left = position.x + 'px';
                panel.element.style.top = position.y + 'px';
                panel.element.style.right = 'auto';
                panel.element.style.bottom = 'auto';
                panel.currentX = position.x;
                panel.currentY = position.y;
            }

            if (position.minimized) {
                this.toggleMinimize(panel.id);
            }

            if (position.locked) {
                panel.isLocked = true;
                const lockBtn = panel.element.querySelector('.hud-controls button:nth-child(2)');
                if (lockBtn) {
                    lockBtn.textContent = '🔒';
                    lockBtn.title = 'Unlock Position';
                }
            }

            if (position.zIndex) {
                panel.element.style.zIndex = position.zIndex;
            }

            console.log(`✅ Position restored: ${panel.id}`);
        } catch (e) {
            console.error(`❌ Failed to restore position for ${panel.id}:`, e);
        }
    }

    loadPositions() {
        // Load all saved panel positions on init
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('hud_panel_')) {
                console.log(`📍 Found saved position: ${key}`);
            }
        }
    }

    /**
     * Keyboard shortcuts
     */
    initKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Alt + H = Toggle HUD
            if (e.altKey && e.key === 'h') {
                this.toggleAllPanels();
                e.preventDefault();
            }

            // Alt + R = Reset all positions
            if (e.altKey && e.key === 'r') {
                this.resetAllPositions();
                e.preventDefault();
            }

            // Alt + L = Lock all panels
            if (e.altKey && e.key === 'l') {
                this.toggleAllLocks();
                e.preventDefault();
            }
        });

        console.log('⌨️ HUD keyboard shortcuts active:');
        console.log('   Alt+H = Toggle all panels');
        console.log('   Alt+R = Reset all positions');
        console.log('   Alt+L = Lock/unlock all');
    }

    toggleAllPanels() {
        this.panels.forEach((panel) => {
            const isVisible = panel.element.style.display !== 'none';
            panel.element.style.display = isVisible ? 'none' : '';
        });
    }

    resetAllPositions() {
        this.panels.forEach((panel, id) => {
            this.resetPosition(id);
        });
        console.log('↺ All panels reset');
    }

    toggleAllLocks() {
        const allLocked = Array.from(this.panels.values()).every(p => p.isLocked);
        this.panels.forEach((panel, id) => {
            if (allLocked) {
                if (panel.isLocked) this.toggleLock(id);
            } else {
                if (!panel.isLocked) this.toggleLock(id);
            }
        });
    }
}

// Global instance
window.HUD = new UniversalHUD();

console.log('🎮 Universal HUD System loaded. Use window.HUD to control panels.');
console.log('📖 Documentation: HUD.registerPanel(id, element, options)');
