/**
 * WELCOME PAGE FLOW ENHANCEMENTS
 * Improves UX for the welcome wizard with analytics, persistence, and polish
 */

(function() {
    'use strict';

    // ============================================================================
    // CONFIGURATION
    // ============================================================================

    const STORAGE_KEYS = {
        TOUR_COMPLETED: 'welcomeTourCompleted',
        CURRENT_STEP: 'welcomeTourCurrentStep',
        DONT_SHOW_AGAIN: 'welcomeTourDontShowAgain',
        COMPLETION_TIME: 'welcomeTourCompletionTime',
        STEP_TIMES: 'welcomeTourStepTimes'
    };

    // ============================================================================
    // ANALYTICS TRACKING
    // ============================================================================

    function trackStepView(stepNumber) {
        // Track with Plausible if available
        if (window.plausible) {
            window.plausible('Welcome Step', {
                props: {
                    step: stepNumber,
                    stepName: getStepName(stepNumber)
                }
            });
        }

        // Save step time
        const stepTimes = JSON.parse(localStorage.getItem(STORAGE_KEYS.STEP_TIMES) || '{}');
        stepTimes[stepNumber] = Date.now();
        localStorage.setItem(STORAGE_KEYS.STEP_TIMES, JSON.stringify(stepTimes));

        console.log(`📊 Welcome Tour - Step ${stepNumber}/5: ${getStepName(stepNumber)}`);
    }

    function getStepName(stepNumber) {
        const stepNames = {
            1: 'Welcome',
            2: 'KORPAKs',
            3: 'Platform',
            4: 'Trinity AI',
            5: 'Ready'
        };
        return stepNames[stepNumber] || 'Unknown';
    }

    function trackTourCompletion() {
        const completionTime = Date.now();
        localStorage.setItem(STORAGE_KEYS.COMPLETION_TIME, completionTime);

        // Calculate time spent
        const stepTimes = JSON.parse(localStorage.getItem(STORAGE_KEYS.STEP_TIMES) || '{}');
        const startTime = stepTimes[1] || completionTime;
        const duration = Math.round((completionTime - startTime) / 1000); // seconds

        // Track completion
        if (window.plausible) {
            window.plausible('Welcome Tour Completed', {
                props: {
                    duration: duration,
                    steps_completed: 5
                }
            });
        }

        console.log(`✅ Welcome Tour Completed in ${duration}s`);

        // Show completion badge
        showCompletionBadge(duration);
    }

    function trackTourSkipped(fromStep) {
        if (window.plausible) {
            window.plausible('Welcome Tour Skipped', {
                props: {
                    from_step: fromStep
                }
            });
        }
        console.log(`⏭️ Welcome Tour Skipped from step ${fromStep}`);
    }

    // ============================================================================
    // PROGRESS PERSISTENCE
    // ============================================================================

    function saveCurrentStep(stepNumber) {
        localStorage.setItem(STORAGE_KEYS.CURRENT_STEP, stepNumber);
    }

    function loadSavedStep() {
        const saved = localStorage.getItem(STORAGE_KEYS.CURRENT_STEP);
        return saved ? parseInt(saved, 10) : null;
    }

    function offerResumeOption() {
        const savedStep = loadSavedStep();
        const tourCompleted = localStorage.getItem(STORAGE_KEYS.TOUR_COMPLETED);

        if (savedStep && savedStep > 1 && !tourCompleted) {
            const resume = confirm(
                `Welcome back! You were on step ${savedStep} of the tour.\n\n` +
                `Would you like to resume where you left off?\n\n` +
                `Click OK to resume, or Cancel to start from the beginning.`
            );

            if (resume) {
                return savedStep;
            }
        }
        return null;
    }

    // ============================================================================
    // UI ENHANCEMENTS
    // ============================================================================

    function showCompletionBadge(duration) {
        const badge = document.createElement('div');
        badge.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: 3px solid #00ff88;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 0 20px 60px rgba(0, 255, 136, 0.5);
            z-index: 10000;
            animation: badgePop 0.5s ease-out forwards;
        `;

        badge.innerHTML = `
            <div style="font-size: 60px; margin-bottom: 20px;">🎉</div>
            <div>Welcome Tour Complete!</div>
            <div style="font-size: 16px; margin-top: 15px; color: #00ff88;">
                Completed in ${duration} seconds
            </div>
            <div style="font-size: 14px; margin-top: 10px; opacity: 0.8;">
                Achievement Unlocked: Platform Explorer 🏆
            </div>
        `;

        document.body.appendChild(badge);

        // Add animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes badgePop {
                0% { transform: translate(-50%, -50%) scale(0); }
                50% { transform: translate(-50%, -50%) scale(1.1); }
                100% { transform: translate(-50%, -50%) scale(1); }
            }
        `;
        document.head.appendChild(style);

        // Remove after 3 seconds
        setTimeout(() => {
            badge.style.animation = 'fadeOut 0.5s ease-out forwards';
            setTimeout(() => badge.remove(), 500);
        }, 3000);
    }

    function addDontShowAgainCheckbox() {
        const skipBtn = document.querySelector('.btn-skip');
        if (!skipBtn) return;

        const container = document.createElement('div');
        container.style.cssText = 'display: flex; align-items: center; gap: 8px;';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = 'dontShowAgain';
        checkbox.style.cssText = 'width: 16px; height: 16px; cursor: pointer;';

        const label = document.createElement('label');
        label.htmlFor = 'dontShowAgain';
        label.textContent = "Don't show again";
        label.style.cssText = 'font-size: 12px; color: var(--text-secondary); cursor: pointer;';

        container.appendChild(checkbox);
        container.appendChild(label);

        skipBtn.parentElement.insertBefore(container, skipBtn);

        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                localStorage.setItem(STORAGE_KEYS.DONT_SHOW_AGAIN, 'true');
                console.log('📝 Welcome tour will not show again on future visits');
            } else {
                localStorage.removeItem(STORAGE_KEYS.DONT_SHOW_AGAIN);
            }
        });
    }

    function addQuickActionButtons() {
        const finishBtn = document.getElementById('finishBtn');
        if (!finishBtn) return;

        const quickActions = document.createElement('div');
        quickActions.style.cssText = `
            margin-top: 20px;
            padding: 20px;
            background: rgba(0, 212, 255, 0.05);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 10px;
        `;

        quickActions.innerHTML = `
            <div style="font-size: 14px; color: var(--text-secondary); margin-bottom: 15px;">
                Quick Actions:
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;">
                <button class="btn btn-secondary" onclick="window.location.href='ai-guided-tour.html'" style="font-size: 12px; padding: 8px 12px;">
                    📚 Take Guided Tour
                </button>
                <button class="btn btn-secondary" onclick="window.location.href='module-library.html'" style="font-size: 12px; padding: 8px 12px;">
                    📦 Browse Modules
                </button>
                <button class="btn btn-secondary" onclick="window.location.href='builder-workshop.html'" style="font-size: 12px; padding: 8px 12px;">
                    🔨 Start Building
                </button>
                <button class="btn btn-secondary" onclick="window.location.href='showcase-hub.html'" style="font-size: 12px; padding: 8px 12px;">
                    🎭 View Showcases
                </button>
            </div>
        `;

        // Insert before finish button
        finishBtn.parentElement.insertBefore(quickActions, finishBtn);
    }

    function addStepIndicator() {
        const wizard = document.querySelector('.welcome-wizard');
        if (!wizard) return;

        const indicator = document.createElement('div');
        indicator.id = 'stepIndicator';
        indicator.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid var(--accent-primary);
            border-radius: 10px;
            padding: 10px 15px;
            font-size: 12px;
            color: var(--text-secondary);
            z-index: 9999;
        `;

        document.body.appendChild(indicator);
    }

    function updateStepIndicator(current, total) {
        const indicator = document.getElementById('stepIndicator');
        if (indicator) {
            indicator.innerHTML = `
                Step <span style="color: var(--accent-primary); font-weight: bold;">${current}</span> of ${total}<br>
                <span style="font-size: 10px; opacity: 0.7;">Use ← → arrow keys to navigate</span>
            `;
        }
    }

    function addTooltips() {
        // Add tooltip for KORPAK concept
        const korpakSteps = document.querySelectorAll('[data-step="2"]');
        if (korpakSteps.length > 0) {
            const tooltip = document.createElement('div');
            tooltip.textContent = '💡 KORPAK = Complete mission packages that help you execute at 100X speed';
            tooltip.style.cssText = `
                font-size: 11px;
                color: var(--success);
                margin-top: 10px;
                padding: 8px;
                background: rgba(0, 255, 136, 0.1);
                border-radius: 5px;
                border-left: 3px solid var(--success);
            `;
        }
    }

    // ============================================================================
    // ENHANCED NAVIGATION
    // ============================================================================

    let originalNextStep, originalPreviousStep, originalSkipTour;

    function enhanceNavigation() {
        // Store original functions
        if (window.nextStep) {
            originalNextStep = window.nextStep;
            window.nextStep = function() {
                originalNextStep();
                const currentStep = window.currentStep || 1;
                trackStepView(currentStep);
                saveCurrentStep(currentStep);
                updateStepIndicator(currentStep, window.totalSteps || 5);

                // Check if final step
                if (currentStep === (window.totalSteps || 5)) {
                    setTimeout(addQuickActionButtons, 100);
                }
            };
        }

        if (window.previousStep) {
            originalPreviousStep = window.previousStep;
            window.previousStep = function() {
                originalPreviousStep();
                const currentStep = window.currentStep || 1;
                trackStepView(currentStep);
                saveCurrentStep(currentStep);
                updateStepIndicator(currentStep, window.totalSteps || 5);
            };
        }

        if (window.skipTour) {
            originalSkipTour = window.skipTour;
            window.skipTour = function() {
                const currentStep = window.currentStep || 1;
                trackTourSkipped(currentStep);

                const dontShowAgain = document.getElementById('dontShowAgain')?.checked;
                if (dontShowAgain) {
                    localStorage.setItem(STORAGE_KEYS.DONT_SHOW_AGAIN, 'true');
                }

                originalSkipTour();
            };
        }

        // Enhanced finish button
        const finishBtn = document.getElementById('finishBtn');
        if (finishBtn) {
            finishBtn.addEventListener('click', () => {
                trackTourCompletion();
            });
        }
    }

    // ============================================================================
    // INITIALIZATION
    // ============================================================================

    function init() {
        console.log('🎨 Welcome Page Enhancements Loading...');

        // Check if user doesn't want to see tour
        const dontShowAgain = localStorage.getItem(STORAGE_KEYS.DONT_SHOW_AGAIN);
        if (dontShowAgain === 'true') {
            const skip = confirm(
                'You previously chose not to see the welcome tour.\n\n' +
                'Would you like to skip to the dashboard?'
            );
            if (skip) {
                window.location.href = 'user-dashboard.html';
                return;
            } else {
                // User wants to see it again
                localStorage.removeItem(STORAGE_KEYS.DONT_SHOW_AGAIN);
            }
        }

        // Offer resume option
        const resumeStep = offerResumeOption();
        if (resumeStep && window.currentStep !== undefined) {
            window.currentStep = resumeStep;
            if (window.updateUI) window.updateUI();
        }

        // Track initial step
        trackStepView(window.currentStep || 1);

        // Add enhancements
        enhanceNavigation();
        addDontShowAgainCheckbox();
        addStepIndicator();
        updateStepIndicator(window.currentStep || 1, window.totalSteps || 5);
        addTooltips();

        console.log('✅ Welcome Page Enhancements Loaded');
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
