/**
 * PHASE BADGE SYSTEM
 * Visual indicator for showcase development status
 * Helps users know what to expect & helps us track what needs work
 *
 * Usage: Add to any showcase page
 * <script src="../shared/phase-badge-system.js"></script>
 * Then call: PhaseBadge.init('alpha'); // or 'beta', 'stable', etc.
 */

(function() {
    window.PhaseBadge = {
        phases: {
            concept: {
                label: 'CONCEPT',
                color: '#666666',
                bgColor: 'rgba(102, 102, 102, 0.2)',
                description: 'Idea phase - not yet built',
                icon: '💡'
            },
            alpha: {
                label: 'ALPHA',
                color: '#ff6b6b',
                bgColor: 'rgba(255, 107, 107, 0.2)',
                description: 'Early testing - expect bugs!',
                icon: '🔧'
            },
            beta: {
                label: 'BETA',
                color: '#ffd93d',
                bgColor: 'rgba(255, 217, 61, 0.2)',
                description: 'Testing phase - mostly working',
                icon: '⚡'
            },
            stable: {
                label: 'STABLE',
                color: '#6bcf7f',
                bgColor: 'rgba(107, 207, 127, 0.2)',
                description: 'Production ready - fully tested',
                icon: '✅'
            },
            experimental: {
                label: 'EXPERIMENTAL',
                color: '#00d4ff',
                bgColor: 'rgba(0, 212, 255, 0.2)',
                description: 'Wild experiments - may break',
                icon: '🧪'
            },
            deprecated: {
                label: 'DEPRECATED',
                color: '#999999',
                bgColor: 'rgba(153, 153, 153, 0.2)',
                description: 'Old version - being replaced',
                icon: '📦'
            }
        },

        init: function(phase, options = {}) {
            const phaseData = this.phases[phase] || this.phases.alpha;

            // Create badge element
            const badge = document.createElement('div');
            badge.id = 'phase-badge';
            badge.className = 'phase-badge';
            badge.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9998;
                background: ${phaseData.bgColor};
                backdrop-filter: blur(10px);
                border: 2px solid ${phaseData.color};
                border-radius: 10px;
                padding: 10px 20px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                font-weight: bold;
                color: ${phaseData.color};
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            `;

            badge.innerHTML = `
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 18px;">${phaseData.icon}</span>
                    <span>${phaseData.label}</span>
                    ${options.version ? `<span style="opacity: 0.7; font-size: 11px;">v${options.version}</span>` : ''}
                </div>
            `;

            // Add hover tooltip
            badge.title = phaseData.description;

            // Add hover effect
            badge.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05)';
                this.style.boxShadow = `0 6px 20px ${phaseData.color}40`;
            });

            badge.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.3)';
            });

            // Click to show detailed info
            badge.addEventListener('click', () => {
                this.showPhaseInfo(phase, options);
            });

            document.body.appendChild(badge);

            // Log to console
            console.log(`%c${phaseData.icon} ${phaseData.label} VERSION`, `color: ${phaseData.color}; font-size: 14px; font-weight: bold;`);
            console.log(`%c${phaseData.description}`, `color: ${phaseData.color}; font-size: 12px;`);

            // Optional: Add bug count indicator
            if (options.knownBugs) {
                this.addBugCounter(options.knownBugs);
            }

            return badge;
        },

        showPhaseInfo: function(phase, options) {
            const phaseData = this.phases[phase];

            // Create modal
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(5px);
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.3s ease;
            `;

            modal.innerHTML = `
                <div style="
                    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
                    border: 2px solid ${phaseData.color};
                    border-radius: 20px;
                    padding: 40px;
                    max-width: 600px;
                    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
                    color: #fff;
                    font-family: 'Courier New', monospace;
                ">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <div style="font-size: 48px; margin-bottom: 10px;">${phaseData.icon}</div>
                        <h2 style="color: ${phaseData.color}; margin-bottom: 10px;">${phaseData.label} VERSION</h2>
                        <p style="opacity: 0.8;">${phaseData.description}</p>
                    </div>

                    <div style="background: rgba(0, 0, 0, 0.3); border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                        <h3 style="color: ${phaseData.color}; margin-bottom: 15px;">📊 Status Details</h3>
                        ${options.version ? `<p>• Version: <strong>${options.version}</strong></p>` : ''}
                        ${options.knownBugs ? `<p>• Known Bugs: <strong style="color: #ff6b6b;">${options.knownBugs}</strong></p>` : ''}
                        ${options.lastUpdated ? `<p>• Last Updated: <strong>${options.lastUpdated}</strong></p>` : ''}
                        ${options.completionPercent ? `<p>• Completion: <strong>${options.completionPercent}%</strong></p>` : ''}
                    </div>

                    ${this.getPhaseGuidance(phase)}

                    <button onclick="this.closest('div[style*=fixed]').remove()" style="
                        width: 100%;
                        padding: 15px;
                        background: linear-gradient(135deg, ${phaseData.color}, ${phaseData.color}AA);
                        color: ${phase === 'beta' ? '#0a0e27' : '#fff'};
                        border: none;
                        border-radius: 10px;
                        font-size: 16px;
                        font-weight: bold;
                        cursor: pointer;
                        font-family: 'Courier New', monospace;
                        margin-top: 20px;
                    ">
                        Got it! 👍
                    </button>
                </div>
            `;

            document.body.appendChild(modal);

            // Click outside to close
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    modal.remove();
                }
            });
        },

        getPhaseGuidance: function(phase) {
            const guidance = {
                concept: `
                    <div style="background: rgba(102, 102, 102, 0.2); border-radius: 10px; padding: 15px;">
                        <strong>⚠️ What to Expect:</strong>
                        <ul style="margin-top: 10px; padding-left: 20px;">
                            <li>This is just an idea/mockup</li>
                            <li>Not functional yet</li>
                            <li>Design may change completely</li>
                        </ul>
                    </div>
                `,
                alpha: `
                    <div style="background: rgba(255, 107, 107, 0.2); border-radius: 10px; padding: 15px;">
                        <strong>⚠️ What to Expect:</strong>
                        <ul style="margin-top: 10px; padding-left: 20px;">
                            <li>Features may not work correctly</li>
                            <li>Bugs are expected!</li>
                            <li>Layout/design still evolving</li>
                            <li>Report issues via bug widget</li>
                        </ul>
                    </div>
                `,
                beta: `
                    <div style="background: rgba(255, 217, 61, 0.2); border-radius: 10px; padding: 15px;">
                        <strong>✅ What to Expect:</strong>
                        <ul style="margin-top: 10px; padding-left: 20px;">
                            <li>Most features working</li>
                            <li>Minor bugs may exist</li>
                            <li>Final polish in progress</li>
                            <li>Your feedback helps us improve!</li>
                        </ul>
                    </div>
                `,
                stable: `
                    <div style="background: rgba(107, 207, 127, 0.2); border-radius: 10px; padding: 15px;">
                        <strong>✅ Production Ready:</strong>
                        <ul style="margin-top: 10px; padding-left: 20px;">
                            <li>Fully tested and reliable</li>
                            <li>All features working as intended</li>
                            <li>Continuous improvements ongoing</li>
                            <li>Report any issues you find!</li>
                        </ul>
                    </div>
                `,
                experimental: `
                    <div style="background: rgba(0, 212, 255, 0.2); border-radius: 10px; padding: 15px;">
                        <strong>🧪 Experimental Feature:</strong>
                        <ul style="margin-top: 10px; padding-left: 20px;">
                            <li>Cutting-edge technology</li>
                            <li>May behave unexpectedly</li>
                            <li>Subject to major changes</li>
                            <li>Help us test the future!</li>
                        </ul>
                    </div>
                `,
                deprecated: `
                    <div style="background: rgba(153, 153, 153, 0.2); border-radius: 10px; padding: 15px;">
                        <strong>📦 Legacy Version:</strong>
                        <ul style="margin-top: 10px; padding-left: 20px;">
                            <li>Being replaced with new version</li>
                            <li>Still functional but outdated</li>
                            <li>No new features planned</li>
                            <li>Check for newer version!</li>
                        </ul>
                    </div>
                `
            };

            return guidance[phase] || '';
        },

        addBugCounter: function(bugCount) {
            if (bugCount === 0) return;

            const badge = document.getElementById('phase-badge');
            if (!badge) return;

            const bugBadge = document.createElement('div');
            bugBadge.style.cssText = `
                position: absolute;
                top: -8px;
                right: -8px;
                background: #ff4757;
                color: white;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 11px;
                font-weight: bold;
                box-shadow: 0 2px 8px rgba(255, 71, 87, 0.5);
                animation: pulse 2s ease-in-out infinite;
            `;

            bugBadge.textContent = bugCount;
            bugBadge.title = `${bugCount} known bug${bugCount > 1 ? 's' : ''}`;

            badge.style.position = 'relative';
            badge.appendChild(bugBadge);

            // Add pulse animation
            const style = document.createElement('style');
            style.textContent = `
                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                }
            `;
            document.head.appendChild(style);
        },

        // Quick access functions for common scenarios
        markAsAlpha: function(options = {}) {
            return this.init('alpha', options);
        },

        markAsBeta: function(options = {}) {
            return this.init('beta', options);
        },

        markAsStable: function(options = {}) {
            return this.init('stable', options);
        },

        markAsExperimental: function(options = {}) {
            return this.init('experimental', options);
        }
    };

    // Auto-detect phase from page metadata
    document.addEventListener('DOMContentLoaded', () => {
        const phaseMeta = document.querySelector('meta[name="phase"]');
        const versionMeta = document.querySelector('meta[name="version"]');
        const bugsMeta = document.querySelector('meta[name="known-bugs"]');

        if (phaseMeta) {
            const options = {};
            if (versionMeta) options.version = versionMeta.content;
            if (bugsMeta) options.knownBugs = parseInt(bugsMeta.content);

            window.PhaseBadge.init(phaseMeta.content, options);
        }
    });
})();

console.log('🏷️ Phase Badge System loaded - Track development status visually');
