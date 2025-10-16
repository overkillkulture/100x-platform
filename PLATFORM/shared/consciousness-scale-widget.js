/**
 * CONSCIOUSNESS SCALE VISUAL WIDGET
 * Color-coded scale showing user's consciousness level in real-time
 */

const ConsciousnessScale = {
    /**
     * Create visual scale widget
     */
    createWidget(options = {}) {
        const position = options.position || 'bottom-right';
        const collapsed = options.collapsed || false;

        const widget = document.createElement('div');
        widget.id = 'consciousnessScaleWidget';
        widget.innerHTML = `
            <style>
                #consciousnessScaleWidget {
                    position: fixed;
                    ${position.includes('right') ? 'right: 20px;' : 'left: 20px;'}
                    ${position.includes('top') ? 'top: 20px;' : 'bottom: 20px;'}
                    z-index: 9999;
                    font-family: 'Segoe UI', sans-serif;
                }

                .consciousness-widget-container {
                    background: rgba(0, 0, 0, 0.9);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    padding: 15px;
                    border: 2px solid #ffd700;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                    min-width: 280px;
                    transition: all 0.3s ease;
                }

                .consciousness-widget-container.collapsed {
                    min-width: auto;
                    padding: 10px;
                }

                .widget-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                    cursor: pointer;
                }

                .widget-title {
                    font-size: 0.9rem;
                    font-weight: bold;
                    color: #ffd700;
                }

                .widget-toggle {
                    font-size: 1.2rem;
                    cursor: pointer;
                    user-select: none;
                }

                .consciousness-scale {
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                    margin-bottom: 15px;
                }

                .scale-level {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    padding: 8px;
                    border-radius: 8px;
                    transition: all 0.3s ease;
                    opacity: 0.5;
                }

                .scale-level.active {
                    opacity: 1;
                    transform: scale(1.05);
                    box-shadow: 0 0 20px currentColor;
                }

                .scale-indicator {
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    flex-shrink: 0;
                }

                .scale-label {
                    font-size: 0.85rem;
                    font-weight: bold;
                    flex: 1;
                }

                .scale-score {
                    font-size: 0.8rem;
                    opacity: 0.8;
                }

                .current-score {
                    text-align: center;
                    padding: 12px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    margin-bottom: 10px;
                }

                .score-value {
                    font-size: 2rem;
                    font-weight: bold;
                    color: #ffd700;
                }

                .score-label {
                    font-size: 0.8rem;
                    opacity: 0.8;
                    color: #fff;
                }

                .widget-collapsed-view {
                    display: none;
                }

                .consciousness-widget-container.collapsed .widget-collapsed-view {
                    display: block;
                }

                .consciousness-widget-container.collapsed .consciousness-scale,
                .consciousness-widget-container.collapsed .current-score {
                    display: none;
                }

                .collapsed-indicator {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.5rem;
                    font-weight: bold;
                    transition: all 0.3s ease;
                    cursor: pointer;
                }

                .collapsed-indicator:hover {
                    transform: scale(1.1);
                }
            </style>

            <div class="consciousness-widget-container ${collapsed ? 'collapsed' : ''}">
                <div class="widget-header" onclick="ConsciousnessScale.toggle()">
                    <div class="widget-title">🧬 Consciousness</div>
                    <div class="widget-toggle">▼</div>
                </div>

                <div class="current-score">
                    <div class="score-value" id="widgetScoreValue">0</div>
                    <div class="score-label" id="widgetScoreLabel">Unknown</div>
                </div>

                <div class="consciousness-scale">
                    <div class="scale-level" data-level="architect" style="background: rgba(156, 39, 176, 0.2); color: #9c27b0;">
                        <div class="scale-indicator" style="background: #9c27b0;"></div>
                        <div class="scale-label">Architect</div>
                        <div class="scale-score">100+</div>
                    </div>

                    <div class="scale-level" data-level="builder" style="background: rgba(76, 175, 80, 0.2); color: #4caf50;">
                        <div class="scale-indicator" style="background: #4caf50;"></div>
                        <div class="scale-label">Builder</div>
                        <div class="scale-score">50-99</div>
                    </div>

                    <div class="scale-level" data-level="observer" style="background: rgba(255, 217, 61, 0.2); color: #ffd93d;">
                        <div class="scale-indicator" style="background: #ffd93d;"></div>
                        <div class="scale-label">Observer</div>
                        <div class="scale-score">0-49</div>
                    </div>

                    <div class="scale-level" data-level="skeptic" style="background: rgba(255, 152, 0, 0.2); color: #ff9800;">
                        <div class="scale-indicator" style="background: #ff9800;"></div>
                        <div class="scale-label">Skeptic</div>
                        <div class="scale-score">-1 to -50</div>
                    </div>

                    <div class="scale-level" data-level="destroyer" style="background: rgba(255, 68, 68, 0.2); color: #ff4444;">
                        <div class="scale-indicator" style="background: #ff4444;"></div>
                        <div class="scale-label">Destroyer</div>
                        <div class="scale-score">-51+</div>
                    </div>
                </div>

                <div class="widget-collapsed-view">
                    <div class="collapsed-indicator" id="collapsedIndicator" onclick="ConsciousnessScale.toggle()">
                        ?
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(widget);
        this.updateWidget();
    },

    /**
     * Update widget with current consciousness level
     */
    updateWidget() {
        if (!window.ProductBadges) return;

        const level = ProductBadges.getConsciousnessLevel();

        // Update score display
        const scoreValue = document.getElementById('widgetScoreValue');
        const scoreLabel = document.getElementById('widgetScoreLabel');
        const collapsedIndicator = document.getElementById('collapsedIndicator');

        if (scoreValue) scoreValue.textContent = level.score;
        if (scoreLabel) scoreLabel.textContent = level.level;

        // Update collapsed indicator
        if (collapsedIndicator) {
            const levelEmojis = {
                'Architect': '👑',
                'Builder': '🛠️',
                'Observer': '👁️',
                'Skeptic': '🤔',
                'Destroyer': '💀',
                'Unknown': '?'
            };
            collapsedIndicator.textContent = levelEmojis[level.level] || '?';

            const levelColors = {
                'Architect': '#9c27b0',
                'Builder': '#4caf50',
                'Observer': '#ffd93d',
                'Skeptic': '#ff9800',
                'Destroyer': '#ff4444',
                'Unknown': '#666'
            };
            collapsedIndicator.style.background = levelColors[level.level] || '#666';
        }

        // Highlight active level
        document.querySelectorAll('.scale-level').forEach(el => {
            el.classList.remove('active');
        });

        const levelMap = {
            'Architect': 'architect',
            'Builder': 'builder',
            'Observer': 'observer',
            'Skeptic': 'skeptic',
            'Destroyer': 'destroyer'
        };

        const activeLevel = levelMap[level.level];
        if (activeLevel) {
            const activeLevelEl = document.querySelector(`.scale-level[data-level="${activeLevel}"]`);
            if (activeLevelEl) {
                activeLevelEl.classList.add('active');
            }
        }
    },

    /**
     * Toggle widget collapsed/expanded
     */
    toggle() {
        const container = document.querySelector('.consciousness-widget-container');
        const toggle = document.querySelector('.widget-toggle');

        if (container) {
            container.classList.toggle('collapsed');
            if (toggle) {
                toggle.textContent = container.classList.contains('collapsed') ? '▶' : '▼';
            }
        }
    },

    /**
     * Initialize widget on page
     */
    init(options = {}) {
        // Wait for DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.createWidget(options);
            });
        } else {
            this.createWidget(options);
        }

        // Update every 5 seconds
        setInterval(() => {
            this.updateWidget();
        }, 5000);
    }
};

// Make available globally
window.ConsciousnessScale = ConsciousnessScale;

// Auto-initialize if ProductBadges exists
if (window.ProductBadges) {
    ConsciousnessScale.init({ collapsed: true });
}
