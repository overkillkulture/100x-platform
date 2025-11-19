/**
 * THREE-STAMP APPROVAL SYSTEM
 * Trinity → Human → User validation pipeline
 *
 * Every product goes through three approval gates:
 * 1. Trinity Stamp: AI tests and approves
 * 2. Human Stamp: Commander/Creator approves
 * 3. User Stamp: Real users validate
 */

const ThreeStampApproval = {
    /**
     * Approval stages and stamps
     */
    stages: {
        stage1: {
            label: 'Stage 1: Trinity Testing',
            description: 'AI is testing this product',
            requiredStamp: 'trinity'
        },
        stage2: {
            label: 'Stage 2: Human Review',
            description: 'Creator is reviewing and testing',
            requiredStamp: 'human'
        },
        stage3: {
            label: 'Stage 3: User Validation',
            description: 'Real users are testing and validating',
            requiredStamp: 'user'
        },
        complete: {
            label: 'Complete: Triple-Validated',
            description: 'Approved by Trinity, Human, and Users',
            requiredStamp: 'all'
        }
    },

    stamps: {
        trinity: {
            emoji: '🤖',
            label: 'Trinity Approved',
            color: '#9c27b0',
            description: 'AI has tested and validated functionality'
        },
        human: {
            emoji: '✋',
            label: 'Human Approved',
            color: '#2196f3',
            description: 'Creator has reviewed and approved'
        },
        user: {
            emoji: '👥',
            label: 'User Validated',
            color: '#4caf50',
            description: 'Real users have tested and confirmed'
        }
    },

    /**
     * Create three-stamp visual display
     */
    createStampDisplay(productId, approvals = {}) {
        const hasTrinity = approvals.trinity || false;
        const hasHuman = approvals.human || false;
        const hasUser = approvals.user || false;

        // Determine current stage
        let currentStage = 'stage1';
        if (hasTrinity && hasHuman && hasUser) {
            currentStage = 'complete';
        } else if (hasTrinity && hasHuman) {
            currentStage = 'stage3';
        } else if (hasTrinity) {
            currentStage = 'stage2';
        }

        const stage = this.stages[currentStage];

        return `
            <div class="three-stamp-container" style="
                background: rgba(0, 0, 0, 0.3);
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                border: 2px solid rgba(255, 255, 255, 0.2);
            ">
                <!-- Stage Label -->
                <div class="stage-label" style="
                    text-align: center;
                    margin-bottom: 20px;
                ">
                    <div style="
                        font-size: 1.2rem;
                        font-weight: bold;
                        color: #ffd700;
                        margin-bottom: 5px;
                    ">
                        ${stage.label}
                    </div>
                    <div style="
                        font-size: 0.9rem;
                        opacity: 0.8;
                    ">
                        ${stage.description}
                    </div>
                </div>

                <!-- Three Stamps -->
                <div class="stamps-row" style="
                    display: flex;
                    justify-content: center;
                    gap: 30px;
                    flex-wrap: wrap;
                ">
                    ${this.createStamp('trinity', hasTrinity)}
                    ${this.createStamp('human', hasHuman)}
                    ${this.createStamp('user', hasUser)}
                </div>

                <!-- Progress Bar -->
                <div class="approval-progress" style="
                    margin-top: 20px;
                    background: rgba(255, 255, 255, 0.1);
                    height: 8px;
                    border-radius: 4px;
                    overflow: hidden;
                ">
                    <div style="
                        width: ${this.calculateProgress(hasTrinity, hasHuman, hasUser)}%;
                        height: 100%;
                        background: linear-gradient(90deg, #9c27b0, #2196f3, #4caf50);
                        transition: width 0.5s ease;
                    "></div>
                </div>

                <!-- Approval Details -->
                <div class="approval-details" style="
                    margin-top: 15px;
                    font-size: 0.85rem;
                    opacity: 0.7;
                    text-align: center;
                ">
                    ${this.getApprovalDetails(productId, approvals)}
                </div>

                <!-- Action Buttons (if applicable) -->
                ${this.getActionButtons(productId, currentStage, approvals)}
            </div>
        `;
    },

    /**
     * Create individual stamp
     */
    createStamp(type, isApproved) {
        const stamp = this.stamps[type];

        return `
            <div class="approval-stamp ${isApproved ? 'approved' : 'pending'}" style="
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 10px;
                opacity: ${isApproved ? '1' : '0.3'};
                transition: all 0.3s ease;
            ">
                <div class="stamp-icon" style="
                    width: 80px;
                    height: 80px;
                    border-radius: 50%;
                    background: ${isApproved ? stamp.color : 'rgba(255, 255, 255, 0.1)'};
                    border: 3px solid ${stamp.color};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 2.5rem;
                    position: relative;
                    ${isApproved ? 'animation: stamp-approved 0.5s ease;' : ''}
                ">
                    ${stamp.emoji}
                    ${isApproved ? `
                        <div style="
                            position: absolute;
                            top: -5px;
                            right: -5px;
                            width: 25px;
                            height: 25px;
                            background: #4caf50;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 0.8rem;
                        ">✓</div>
                    ` : ''}
                </div>
                <div class="stamp-label" style="
                    font-size: 0.9rem;
                    font-weight: bold;
                    color: ${stamp.color};
                    text-align: center;
                ">
                    ${stamp.label}
                </div>
                <div class="stamp-description" style="
                    font-size: 0.75rem;
                    opacity: 0.7;
                    text-align: center;
                    max-width: 120px;
                ">
                    ${stamp.description}
                </div>
            </div>

            <style>
                @keyframes stamp-approved {
                    0% { transform: scale(0.5) rotate(-10deg); opacity: 0; }
                    50% { transform: scale(1.1) rotate(5deg); }
                    100% { transform: scale(1) rotate(0deg); opacity: 1; }
                }
            </style>
        `;
    },

    /**
     * Calculate progress percentage
     */
    calculateProgress(trinity, human, user) {
        let progress = 0;
        if (trinity) progress += 33.33;
        if (human) progress += 33.33;
        if (user) progress += 33.34;
        return progress;
    },

    /**
     * Get approval details text
     */
    getApprovalDetails(productId, approvals) {
        const details = [];

        if (approvals.trinity) {
            const date = approvals.trinityDate || 'Recently';
            details.push(`🤖 Trinity approved ${date}`);
        }

        if (approvals.human) {
            const date = approvals.humanDate || 'Recently';
            const who = approvals.humanName || 'Creator';
            details.push(`✋ ${who} approved ${date}`);
        }

        if (approvals.user) {
            const count = approvals.userCount || 1;
            const date = approvals.userDate || 'Recently';
            details.push(`👥 ${count} user${count > 1 ? 's' : ''} validated ${date}`);
        }

        return details.length > 0
            ? details.join(' • ')
            : 'Awaiting first approval';
    },

    /**
     * Get action buttons based on current stage
     */
    getActionButtons(productId, currentStage, approvals) {
        const buttons = [];

        // Human approval button (only show if Trinity approved but Human hasn't)
        if (approvals.trinity && !approvals.human) {
            buttons.push(`
                <button onclick="ThreeStampApproval.requestHumanApproval('${productId}')" style="
                    background: linear-gradient(45deg, #2196f3, #1976d2);
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 10px;
                    cursor: pointer;
                    font-weight: bold;
                    margin: 5px;
                ">
                    ✋ Approve as Human
                </button>
            `);
        }

        // User validation button (only show if both Trinity and Human approved)
        if (approvals.trinity && approvals.human && !approvals.user) {
            buttons.push(`
                <button onclick="ThreeStampApproval.submitUserValidation('${productId}')" style="
                    background: linear-gradient(45deg, #4caf50, #45a049);
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 10px;
                    cursor: pointer;
                    font-weight: bold;
                    margin: 5px;
                ">
                    👥 I Tested It - It Works!
                </button>
            `);
        }

        if (buttons.length === 0) return '';

        return `
            <div class="approval-actions" style="
                margin-top: 20px;
                text-align: center;
            ">
                ${buttons.join('')}
            </div>
        `;
    },

    /**
     * Get current approvals for a product
     */
    getApprovals(productId) {
        const key = `approvals_${productId}`;
        const stored = localStorage.getItem(key);
        return stored ? JSON.parse(stored) : {};
    },

    /**
     * Save approvals for a product
     */
    saveApprovals(productId, approvals) {
        const key = `approvals_${productId}`;
        localStorage.setItem(key, JSON.stringify(approvals));
    },

    /**
     * Grant Trinity approval (automated)
     */
    grantTrinityApproval(productId, tests = {}) {
        const approvals = this.getApprovals(productId);
        approvals.trinity = true;
        approvals.trinityDate = new Date().toLocaleDateString();
        approvals.trinityTests = tests;
        this.saveApprovals(productId, approvals);

        console.log(`%c🤖 TRINITY STAMP GRANTED`, 'color: #9c27b0; font-size: 16px; font-weight: bold;');
        console.log(`%cProduct: ${productId}`, 'color: #9c27b0; font-size: 14px;');
        console.log(`%cTests passed: ${Object.keys(tests).length}`, 'color: #9c27b0; font-size: 12px;');

        this.refreshDisplay(productId);
    },

    /**
     * Request human approval (manual)
     */
    requestHumanApproval(productId) {
        const name = prompt('Enter your name (Creator/Reviewer):');
        if (!name) return;

        const approvals = this.getApprovals(productId);
        approvals.human = true;
        approvals.humanDate = new Date().toLocaleDateString();
        approvals.humanName = name;
        this.saveApprovals(productId, approvals);

        alert('✋ Human stamp granted! Product is now ready for user validation.');

        console.log(`%c✋ HUMAN STAMP GRANTED`, 'color: #2196f3; font-size: 16px; font-weight: bold;');
        console.log(`%cApproved by: ${name}`, 'color: #2196f3; font-size: 14px;');

        this.refreshDisplay(productId);
    },

    /**
     * Submit user validation
     */
    submitUserValidation(productId) {
        const feedback = prompt('What did you test? (brief description):');
        if (!feedback) return;

        const approvals = this.getApprovals(productId);
        approvals.user = true;
        approvals.userDate = new Date().toLocaleDateString();
        approvals.userCount = (approvals.userCount || 0) + 1;

        // Store user feedback
        if (!approvals.userFeedback) approvals.userFeedback = [];
        approvals.userFeedback.push({
            date: new Date().toISOString(),
            feedback: feedback
        });

        this.saveApprovals(productId, approvals);

        alert('👥 User validation recorded! Thank you for testing.');

        console.log(`%c👥 USER STAMP GRANTED`, 'color: #4caf50; font-size: 16px; font-weight: bold;');
        console.log(`%cFeedback: ${feedback}`, 'color: #4caf50; font-size: 14px;');

        // Check if triple-validated
        if (approvals.trinity && approvals.human && approvals.user) {
            console.log(`%c🎉 TRIPLE-VALIDATED!`, 'color: #ffd700; font-size: 18px; font-weight: bold;');
            console.log(`%cThis product has been approved by Trinity, Human, and Users!`, 'color: #ffd700; font-size: 14px;');
        }

        this.refreshDisplay(productId);
    },

    /**
     * Refresh display after approval change
     */
    refreshDisplay(productId) {
        const container = document.getElementById('stampContainer');
        if (container) {
            const approvals = this.getApprovals(productId);
            container.innerHTML = this.createStampDisplay(productId, approvals);
        }
    },

    /**
     * Inject stamp display into page
     */
    injectStampDisplay(productId, containerId = 'stampContainer') {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Stamp container not found: ${containerId}`);
            return;
        }

        const approvals = this.getApprovals(productId);
        container.innerHTML = this.createStampDisplay(productId, approvals);
    },

    /**
     * Add stamp display to page header automatically
     */
    addToHeader(productId) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this._insertStampDisplay(productId);
            });
        } else {
            this._insertStampDisplay(productId);
        }
    },

    _insertStampDisplay(productId) {
        const header = document.querySelector('.header') ||
                      document.querySelector('header') ||
                      document.querySelector('.hero');

        if (!header) {
            console.warn('No header found to add stamps');
            return;
        }

        const stampContainer = document.createElement('div');
        stampContainer.id = 'stampContainer';
        const approvals = this.getApprovals(productId);
        stampContainer.innerHTML = this.createStampDisplay(productId, approvals);

        // Insert after badge (if exists) or at top of header
        const badge = header.querySelector('#productBadgeContainer');
        if (badge) {
            badge.after(stampContainer);
        } else {
            header.insertBefore(stampContainer, header.firstChild);
        }
    }
};

// Make available globally
window.ThreeStampApproval = ThreeStampApproval;
