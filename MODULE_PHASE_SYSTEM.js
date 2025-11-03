/**
 * 🎨 MODULE PHASE SYSTEM 🎨
 * Visual system showing development stage of each module
 *
 * Phases: Planning → Building → Testing → Live → Mastered
 * Colors create transparency + anticipation + gamification
 */

class ModulePhaseSystem {
    constructor() {
        this.phases = {
            planning: {
                name: 'Planning',
                color: '#FF6B6B',
                icon: '📋',
                description: 'Concept & design stage',
                badge: 'COMING SOON',
                progress: 0
            },
            building: {
                name: 'Building',
                color: '#FFA500',
                icon: '🔨',
                description: 'Under construction',
                badge: 'IN PROGRESS',
                progress: 50
            },
            testing: {
                name: 'Testing',
                color: '#FFD700',
                icon: '🧪',
                description: 'Testing & refinement',
                badge: 'BETA',
                progress: 80
            },
            live: {
                name: 'Live',
                color: '#4CAF50',
                icon: '✅',
                description: 'Active & functional',
                badge: 'LIVE',
                progress: 100
            },
            mastered: {
                name: 'Mastered',
                color: '#667eea',
                icon: '⭐',
                description: 'Fully optimized',
                badge: 'MASTERED',
                progress: 100
            }
        };

        // Module registry (update as modules change phases)
        this.modulePhases = this.loadModulePhases();

        this.init();
    }

    loadModulePhases() {
        const saved = localStorage.getItem('modulePhases');
        if (saved) return JSON.parse(saved);

        // Default phases for existing modules
        return {
            // Front pages
            'index.html': 'live',
            'open-house.html': 'live',
            'platform.html': 'live',
            'roadmap.html': 'testing',
            'success.html': 'live',

            // Platform modules (most are live after today's boost)
            'PLATFORM/analytics-dashboard.html': 'live',
            'PLATFORM/consciousness-boost-dashboard.html': 'live',
            'PLATFORM/platform-city-map.html': 'live',
            'PLATFORM/module-pattern-explorer.html': 'live',
            'PLATFORM/cheat-codes.html': 'live',
            'PLATFORM/trinity-ai-interface.html': 'testing',
            'PLATFORM/brain-council.html': 'testing',
            'PLATFORM/module-library.html': 'live',
            'PLATFORM/business-phase-clock.html': 'testing',

            // Arcade
            'PLATFORM/arcade-hub.html': 'live',
            'PLATFORM/pattern-recognition-quiz.html': 'live',
            'PLATFORM/consciousness-speed-test.html': 'live',
            'PLATFORM/destroyer-defense.html': 'live',
            'PLATFORM/trinity-puzzle.html': 'live',

            // Gamification (new!)
            'PLATFORM/builder-xp-demo.html': 'live',

            // Store
            'PLATFORM/store.html': 'testing',
            'PLATFORM/store-products.html': 'testing',
            'PLATFORM/store-campaigns.html': 'testing',
            'PLATFORM/store-investments.html': 'testing',

            // Public
            'PUBLIC/partnership.html': 'testing',
            'PUBLIC/pattern-filter.html': 'testing',
            'PUBLIC/pattern-theory-training.html': 'testing',

            // Coming soon
            'PLATFORM/user-dashboard.html': 'planning',
            'PLATFORM/builder-community.html': 'planning',
            'PLATFORM/live-chat.html': 'planning',
            'PLATFORM/video-courses.html': 'planning'
        };
    }

    saveModulePhases() {
        localStorage.setItem('modulePhases', JSON.stringify(this.modulePhases));
    }

    // Get phase for current module
    getCurrentModulePhase() {
        const path = window.location.pathname;
        const filename = path.split('/').pop() || 'index.html';
        return this.modulePhases[filename] || 'building';
    }

    // Set phase for a module
    setModulePhase(moduleName, phase) {
        if (!this.phases[phase]) {
            console.error('Invalid phase:', phase);
            return;
        }

        this.modulePhases[moduleName] = phase;
        this.saveModulePhases();

        // Trigger XP if moving to better phase
        if (window.BuilderXP) {
            if (phase === 'live') {
                BuilderXP.rewardAction('module_created');
            } else if (phase === 'mastered') {
                BuilderXP.addXP(1000, 'Module mastered!');
                BuilderXP.earnCredits(250, 'Module mastered');
            }
        }
    }

    // Create phase badge
    createPhaseBadge(phase = null) {
        if (!phase) phase = this.getCurrentModulePhase();
        const phaseData = this.phases[phase];

        const badge = document.createElement('div');
        badge.className = 'module-phase-badge';
        badge.innerHTML = `
            <div class="phase-badge-content" style="background: ${phaseData.color}">
                <span class="phase-icon">${phaseData.icon}</span>
                <span class="phase-name">${phaseData.badge}</span>
            </div>
            <div class="phase-tooltip">
                <strong>${phaseData.name}</strong><br>
                ${phaseData.description}
            </div>
        `;

        return badge;
    }

    // Create phase banner (top of page)
    createPhaseBanner(phase = null) {
        if (!phase) phase = this.getCurrentModulePhase();
        const phaseData = this.phases[phase];

        const banner = document.createElement('div');
        banner.className = 'module-phase-banner';
        banner.style.background = `linear-gradient(90deg, ${phaseData.color}, ${phaseData.color}cc)`;
        banner.innerHTML = `
            <div class="banner-content">
                <span class="banner-icon">${phaseData.icon}</span>
                <span class="banner-text">
                    <strong>${phaseData.badge}</strong> - ${phaseData.description}
                </span>
                ${phase !== 'live' && phase !== 'mastered' ? `
                    <span class="banner-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${phaseData.progress}%"></div>
                        </div>
                        <span class="progress-text">${phaseData.progress}%</span>
                    </span>
                ` : ''}
            </div>
        `;

        return banner;
    }

    // Create module status grid (for main page)
    createModuleStatusGrid() {
        const grid = document.createElement('div');
        grid.className = 'module-status-grid';

        const byPhase = {
            planning: [],
            building: [],
            testing: [],
            live: [],
            mastered: []
        };

        // Group modules by phase
        Object.entries(this.modulePhases).forEach(([module, phase]) => {
            byPhase[phase].push(module);
        });

        grid.innerHTML = `
            <h2>🎨 Platform Status</h2>
            <div class="phase-columns">
                ${Object.entries(this.phases).map(([key, phase]) => `
                    <div class="phase-column" style="border-top: 4px solid ${phase.color}">
                        <div class="phase-header">
                            <span class="phase-icon">${phase.icon}</span>
                            <h3>${phase.name}</h3>
                            <span class="phase-count">${byPhase[key].length}</span>
                        </div>
                        <div class="module-list">
                            ${byPhase[key].map(mod => `
                                <div class="module-item">
                                    <a href="${mod}">${mod.split('/').pop().replace('.html', '')}</a>
                                </div>
                            `).join('')}
                            ${byPhase[key].length === 0 ? '<div class="module-item empty">None yet</div>' : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        return grid;
    }

    // Create phase progress chart
    createProgressChart() {
        const chart = document.createElement('div');
        chart.className = 'phase-progress-chart';

        const total = Object.keys(this.modulePhases).length;
        const counts = {
            planning: 0,
            building: 0,
            testing: 0,
            live: 0,
            mastered: 0
        };

        Object.values(this.modulePhases).forEach(phase => {
            counts[phase]++;
        });

        chart.innerHTML = `
            <h3>📊 Development Progress</h3>
            <div class="progress-bars">
                ${Object.entries(this.phases).map(([key, phase]) => {
                    const count = counts[key];
                    const percentage = Math.round((count / total) * 100);
                    return `
                        <div class="phase-progress-row">
                            <div class="phase-label">
                                <span>${phase.icon} ${phase.name}</span>
                                <span>${count} modules (${percentage}%)</span>
                            </div>
                            <div class="phase-progress-bar">
                                <div class="phase-progress-fill"
                                     style="width: ${percentage}%; background: ${phase.color}">
                                </div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
            <div class="total-stat">
                <strong>Total Modules:</strong> ${total}
            </div>
        `;

        return chart;
    }

    // Auto-inject phase indicator on page load
    autoInject() {
        const phase = this.getCurrentModulePhase();
        const phaseData = this.phases[phase];

        // Add badge to bottom-left corner
        const badge = this.createPhaseBadge(phase);
        badge.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            z-index: 9998;
        `;
        document.body.appendChild(badge);

        // Add banner if not live/mastered
        if (phase !== 'live' && phase !== 'mastered') {
            const banner = this.createPhaseBanner(phase);
            document.body.insertBefore(banner, document.body.firstChild);
        }
    }

    init() {
        this.injectStyles();
    }

    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* Phase Badge */
            .module-phase-badge {
                position: relative;
                cursor: help;
            }

            .phase-badge-content {
                padding: 8px 15px;
                border-radius: 20px;
                display: flex;
                align-items: center;
                gap: 8px;
                color: white;
                font-weight: bold;
                font-size: 0.9em;
                box-shadow: 0 3px 10px rgba(0,0,0,0.3);
                transition: transform 0.2s ease;
            }

            .phase-badge-content:hover {
                transform: scale(1.05);
            }

            .phase-tooltip {
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: white;
                color: #333;
                padding: 10px 15px;
                border-radius: 8px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
                white-space: nowrap;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.2s ease;
                margin-bottom: 10px;
            }

            .module-phase-badge:hover .phase-tooltip {
                opacity: 1;
            }

            /* Phase Banner */
            .module-phase-banner {
                padding: 15px 20px;
                color: white;
                text-align: center;
                position: relative;
                z-index: 1000;
            }

            .banner-content {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
                max-width: 1200px;
                margin: 0 auto;
            }

            .banner-icon {
                font-size: 1.5em;
            }

            .banner-progress {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .progress-bar {
                width: 150px;
                height: 10px;
                background: rgba(255,255,255,0.3);
                border-radius: 5px;
                overflow: hidden;
            }

            .progress-fill {
                height: 100%;
                background: white;
                transition: width 0.3s ease;
            }

            .progress-text {
                font-size: 0.9em;
                font-weight: bold;
            }

            /* Module Status Grid */
            .module-status-grid {
                padding: 40px 20px;
                max-width: 1400px;
                margin: 0 auto;
            }

            .module-status-grid h2 {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
                font-size: 2em;
            }

            .phase-columns {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }

            .phase-column {
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }

            .phase-header {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f0f0f0;
            }

            .phase-header h3 {
                flex: 1;
                margin: 0;
                color: #333;
            }

            .phase-count {
                background: #f0f0f0;
                padding: 4px 12px;
                border-radius: 12px;
                font-weight: bold;
                color: #666;
            }

            .module-list {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            .module-item {
                padding: 8px 12px;
                background: #f8f9fa;
                border-radius: 6px;
                font-size: 0.9em;
            }

            .module-item a {
                color: #667eea;
                text-decoration: none;
            }

            .module-item a:hover {
                text-decoration: underline;
            }

            .module-item.empty {
                color: #999;
                font-style: italic;
            }

            /* Progress Chart */
            .phase-progress-chart {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                margin: 20px 0;
            }

            .phase-progress-chart h3 {
                color: #333;
                margin-bottom: 20px;
            }

            .progress-bars {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }

            .phase-progress-row {
                display: flex;
                flex-direction: column;
                gap: 5px;
            }

            .phase-label {
                display: flex;
                justify-content: space-between;
                font-size: 0.9em;
                color: #666;
            }

            .phase-progress-bar {
                height: 24px;
                background: #f0f0f0;
                border-radius: 12px;
                overflow: hidden;
            }

            .phase-progress-fill {
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: flex-end;
                padding: 0 10px;
                color: white;
                font-size: 0.8em;
                font-weight: bold;
                transition: width 0.5s ease;
            }

            .total-stat {
                margin-top: 20px;
                padding-top: 20px;
                border-top: 2px solid #f0f0f0;
                text-align: center;
                color: #333;
            }
        `;
        document.head.appendChild(style);
    }
}

// Global instance
window.ModulePhase = new ModulePhaseSystem();

// Auto-inject on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        ModulePhase.autoInject();
    });
} else {
    ModulePhase.autoInject();
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ModulePhaseSystem;
}
