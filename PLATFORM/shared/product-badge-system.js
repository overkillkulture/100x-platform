/**
 * UNIVERSAL PRODUCT BADGE SYSTEM
 * Shows users what to expect - filters for consciousness level
 *
 * DESTROYERS: Complain when things are broken
 * BUILDERS: Offer to fix or understand it's in progress
 * ARCHITECTS: Understand the value of phased rollout
 */

const ProductBadges = {
    phases: {
        // INTENTIONALLY BROKEN - Consciousness filter (genius idea!)
        broken: {
            label: '🔥 BROKEN (Intentional)',
            color: '#ff4444',
            bgColor: 'rgba(255, 68, 68, 0.2)',
            description: 'This is intentionally broken to filter for consciousness. Builders welcome!',
            showToUser: true,
            expectation: 'Will not work. Testing your reaction.'
        },

        // ALPHA - Not tested, probably broken
        alpha: {
            label: '⚠️ ALPHA',
            color: '#ff9800',
            bgColor: 'rgba(255, 152, 0, 0.2)',
            description: 'Just built, not tested yet. Expect bugs.',
            showToUser: true,
            expectation: 'Probably broken. Builders only.'
        },

        // BETA - Tested once, still rough
        beta: {
            label: '🧪 BETA',
            color: '#ffd93d',
            bgColor: 'rgba(255, 217, 61, 0.2)',
            description: 'Tested but rough around edges. Feedback welcome.',
            showToUser: true,
            expectation: 'Mostly works. Some bugs expected.'
        },

        // PRODUCTION - Fully tested and working
        production: {
            label: '✅ LIVE',
            color: '#4caf50',
            bgColor: 'rgba(76, 175, 80, 0.2)',
            description: 'Fully tested and working.',
            showToUser: true,
            expectation: 'Should work perfectly.'
        },

        // DEPRECATED - Being replaced
        deprecated: {
            label: '⚰️ DEPRECATED',
            color: '#666',
            bgColor: 'rgba(102, 102, 102, 0.2)',
            description: 'Being replaced. Use new version.',
            showToUser: true,
            expectation: 'Still works but outdated.'
        },

        // CONSCIOUSNESS FILTER - Advanced broken gate
        filter: {
            label: '🔬 CONSCIOUSNESS FILTER',
            color: '#9c27b0',
            bgColor: 'rgba(156, 39, 176, 0.2)',
            description: 'Testing your consciousness level. How do you respond?',
            showToUser: true,
            expectation: 'Intentional friction. Your reaction matters.'
        }
    },

    /**
     * Create badge HTML element
     */
    createBadge(phase, options = {}) {
        const config = this.phases[phase];
        if (!config) {
            console.error(`Unknown phase: ${phase}`);
            return '';
        }

        const showDescription = options.showDescription !== false;
        const showExpectation = options.showExpectation || false;
        const inline = options.inline || false;

        let html = `
            <div class="product-badge ${inline ? 'inline' : ''}"
                 style="
                     display: ${inline ? 'inline-flex' : 'flex'};
                     align-items: center;
                     gap: 10px;
                     padding: ${inline ? '5px 12px' : '10px 15px'};
                     background: ${config.bgColor};
                     border: 2px solid ${config.color};
                     border-radius: ${inline ? '20px' : '10px'};
                     margin: ${inline ? '0 10px 0 0' : '10px 0'};
                     color: #fff;
                 ">
                <div class="badge-label" style="
                    font-weight: bold;
                    font-size: ${inline ? '0.9rem' : '1rem'};
                    color: ${config.color};
                ">
                    ${config.label}
                </div>
        `;

        if (showDescription) {
            html += `
                <div class="badge-description" style="
                    font-size: ${inline ? '0.8rem' : '0.9rem'};
                    opacity: 0.9;
                ">
                    ${config.description}
                </div>
            `;
        }

        if (showExpectation) {
            html += `
                <div class="badge-expectation" style="
                    font-size: 0.85rem;
                    opacity: 0.8;
                    font-style: italic;
                    margin-top: 5px;
                ">
                    Expect: ${config.expectation}
                </div>
            `;
        }

        html += `</div>`;
        return html;
    },

    /**
     * Inject badge into page header
     */
    injectBadge(phase, containerId = 'badgeContainer', options = {}) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Badge container not found: ${containerId}`);
            return;
        }

        container.innerHTML = this.createBadge(phase, options);
    },

    /**
     * Add badge to page header automatically
     */
    addToHeader(phase, options = {}) {
        // Wait for DOM to load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this._insertHeaderBadge(phase, options);
            });
        } else {
            this._insertHeaderBadge(phase, options);
        }
    },

    _insertHeaderBadge(phase, options) {
        const header = document.querySelector('.header') ||
                      document.querySelector('header') ||
                      document.querySelector('.hero');

        if (!header) {
            console.warn('No header found to add badge');
            return;
        }

        const badgeContainer = document.createElement('div');
        badgeContainer.id = 'productBadgeContainer';
        badgeContainer.innerHTML = this.createBadge(phase, options);

        // Insert at top of header
        header.insertBefore(badgeContainer, header.firstChild);
    },

    /**
     * Track user reaction to broken things (consciousness detection)
     */
    trackReaction(phase, reactionType, details = {}) {
        const reactions = JSON.parse(localStorage.getItem('productReactions') || '[]');

        reactions.push({
            timestamp: new Date().toISOString(),
            phase: phase,
            reactionType: reactionType, // 'complaint', 'offer_help', 'understanding', 'anger', 'curiosity'
            url: window.location.href,
            ...details
        });

        localStorage.setItem('productReactions', JSON.stringify(reactions.slice(-100)));

        // Consciousness scoring based on reaction
        const consciousnessScores = {
            'complaint': -10,
            'anger': -20,
            'demand_fix': -15,
            'understanding': +15,
            'offer_help': +25,
            'curiosity': +20,
            'bug_report': +30,
            'suggested_fix': +40
        };

        const score = consciousnessScores[reactionType] || 0;
        const currentScore = parseInt(localStorage.getItem('consciousnessScore') || '0');
        localStorage.setItem('consciousnessScore', currentScore + score);

        console.log(`Consciousness reaction tracked: ${reactionType} (${score > 0 ? '+' : ''}${score})`);
        console.log(`Total consciousness score: ${currentScore + score}`);
    },

    /**
     * Get user's consciousness level based on reactions
     */
    getConsciousnessLevel() {
        const score = parseInt(localStorage.getItem('consciousnessScore') || '0');
        const reactions = JSON.parse(localStorage.getItem('productReactions') || '[]');

        if (reactions.length === 0) {
            return {
                level: 'Unknown',
                score: 0,
                description: 'No reactions tracked yet'
            };
        }

        if (score >= 100) {
            return {
                level: 'Architect',
                score: score,
                description: 'You see the bigger picture and contribute positively'
            };
        } else if (score >= 50) {
            return {
                level: 'Builder',
                score: score,
                description: 'You understand work in progress and offer help'
            };
        } else if (score >= 0) {
            return {
                level: 'Observer',
                score: score,
                description: 'You\'re learning to see patterns'
            };
        } else if (score >= -50) {
            return {
                level: 'Skeptic',
                score: score,
                description: 'You expect perfection and complain about imperfection'
            };
        } else {
            return {
                level: 'Destroyer',
                score: score,
                description: 'You react with anger to things that don\'t work perfectly'
            };
        }
    },

    /**
     * Show consciousness level to user
     */
    showConsciousnessLevel() {
        const level = this.getConsciousnessLevel();
        console.log(`%c🧬 YOUR CONSCIOUSNESS LEVEL: ${level.level}`, 'color: #ffd700; font-size: 16px; font-weight: bold;');
        console.log(`%cScore: ${level.score}`, 'color: #00ff41; font-size: 14px;');
        console.log(`%c${level.description}`, 'color: #00d4ff; font-size: 12px;');
    }
};

// Make available globally
window.ProductBadges = ProductBadges;

// Auto-detect and show consciousness level in console
ProductBadges.showConsciousnessLevel();
