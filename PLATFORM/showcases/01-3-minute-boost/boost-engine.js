/**
 * 3-MINUTE CONSCIOUSNESS BOOST ENGINE
 * Science-backed pattern interrupts for instant state change
 * PROTOCOLS: Energy, Calm, Clarity, Confidence
 */

class BoostSystem {
    constructor() {
        this.selectedProtocol = null;
        this.beforeState = 5;
        this.afterState = 7;
        this.timeRemaining = 180; // 3 minutes in seconds
        this.timer = null;
        this.isPaused = false;
        this.currentStepIndex = 0;

        // Protocol definitions with pattern interrupts
        this.protocols = {
            energy: {
                name: 'ENERGY',
                icon: '⚡',
                duration: 180,
                steps: [
                    {
                        duration: 30,
                        instruction: '🧍 Stand up RIGHT NOW. Shake your arms and legs vigorously. Get your blood moving!',
                        type: 'physical'
                    },
                    {
                        duration: 30,
                        instruction: '💨 Power Breathing: Breathe in for 4 counts, hold for 4, out for 4. Repeat 5 times.',
                        type: 'breath'
                    },
                    {
                        duration: 30,
                        instruction: '💧 Drink a full glass of water RIGHT NOW. Chug it. Your cells are thirsty.',
                        type: 'physical'
                    },
                    {
                        duration: 30,
                        instruction: '☀️ If possible, get sunlight on your face. Or turn on bright lights. Light = Energy.',
                        type: 'environmental'
                    },
                    {
                        duration: 30,
                        instruction: '🎵 Play your favorite high-energy song. Move your body to it. No sitting!',
                        type: 'pattern-interrupt'
                    },
                    {
                        duration: 30,
                        instruction: '💪 5 jumping jacks + 5 squats. Your body creates energy through movement!',
                        type: 'physical'
                    }
                ],
                resultMessage: 'Your body just got the wake-up call it needed!'
            },

            calm: {
                name: 'CALM',
                icon: '🧘',
                duration: 180,
                steps: [
                    {
                        duration: 30,
                        instruction: '🪑 Sit comfortably. Plant both feet on the ground. Feel the chair supporting you.',
                        type: 'grounding'
                    },
                    {
                        duration: 45,
                        instruction: '🫁 Box Breathing: In for 4, hold for 4, out for 4, hold for 4. Repeat slowly.',
                        type: 'breath'
                    },
                    {
                        duration: 30,
                        instruction: '👁️ Close your eyes. Scan your body from head to toe. Notice tension. Let it go.',
                        type: 'body-awareness'
                    },
                    {
                        duration: 30,
                        instruction: '🌊 Imagine waves on a beach. Each breath in = wave coming in. Each breath out = wave going out.',
                        type: 'visualization'
                    },
                    {
                        duration: 30,
                        instruction: '🙏 Place one hand on your heart, one on your belly. Feel them rise and fall.',
                        type: 'somatic'
                    },
                    {
                        duration: 15,
                        instruction: '😌 Say to yourself: "I am safe. I am calm. Everything is okay right now."',
                        type: 'affirmation'
                    }
                ],
                resultMessage: 'Your nervous system just shifted into calm mode!'
            },

            clarity: {
                name: 'CLARITY',
                icon: '💎',
                duration: 180,
                steps: [
                    {
                        duration: 30,
                        instruction: '📝 Grab paper. Write down EVERY thought in your head right now. Brain dump everything.',
                        type: 'mental'
                    },
                    {
                        duration: 30,
                        instruction: '❓ Ask yourself: "What is the ONE thing I actually need to focus on right now?"',
                        type: 'question'
                    },
                    {
                        duration: 30,
                        instruction: '💧 Drink water slowly. As you drink, imagine washing away mental fog.',
                        type: 'ritual'
                    },
                    {
                        duration: 30,
                        instruction: '🧊 Cold water on face or ice on wrists. Physical shock = mental clarity.',
                        type: 'pattern-interrupt'
                    },
                    {
                        duration: 30,
                        instruction: '🎯 Write the answer to this: "If I could only do ONE thing today, what would it be?"',
                        type: 'focus'
                    },
                    {
                        duration: 30,
                        instruction: '✂️ Look at your brain dump. Circle the ONE thing. Cross out everything else for now.',
                        type: 'elimination'
                    }
                ],
                resultMessage: 'Your mind just cut through the noise and found the signal!'
            },

            confidence: {
                name: 'CONFIDENCE',
                icon: '🦁',
                duration: 180,
                steps: [
                    {
                        duration: 30,
                        instruction: '🦸 Stand up. Stand TALL. Shoulders back. Take up space. Power pose for 30 seconds.',
                        type: 'physical'
                    },
                    {
                        duration: 30,
                        instruction: '🎯 Remember a time you succeeded at something. Feel that feeling NOW.',
                        type: 'memory'
                    },
                    {
                        duration: 30,
                        instruction: '💪 Say out loud: "I have done hard things before. I can do this too."',
                        type: 'affirmation'
                    },
                    {
                        duration: 30,
                        instruction: '📋 Write 3 things you\'re actually good at. Read them out loud.',
                        type: 'evidence'
                    },
                    {
                        duration: 30,
                        instruction: '🔥 Think of someone who believes in you. What would they say to you right now?',
                        type: 'perspective'
                    },
                    {
                        duration: 30,
                        instruction: '👑 Say out loud: "I am capable. I am ready. I\'ve got this." MEAN IT.',
                        type: 'declaration'
                    }
                ],
                resultMessage: 'Your inner lion just woke up!'
            }
        };
    }

    selectProtocol(protocolName) {
        this.selectedProtocol = this.protocols[protocolName];
        this.hideAllScreens();
        document.getElementById('beforeScreen').style.display = 'block';

        // Track selection
        this.trackEvent('protocol_selected', { protocol: protocolName });
    }

    setBeforeState(value) {
        this.beforeState = value;
    }

    setAfterState(value) {
        this.afterState = value;
    }

    startBoost() {
        this.hideAllScreens();
        document.getElementById('boostScreen').style.display = 'block';

        // Render protocol steps
        this.renderProtocolSteps();

        // Start timer
        this.startTimer();

        // Track start
        this.trackEvent('boost_started', {
            protocol: this.selectedProtocol.name,
            beforeState: this.beforeState
        });
    }

    renderProtocolSteps() {
        const stepsContainer = document.getElementById('protocolSteps');
        stepsContainer.innerHTML = '';

        this.selectedProtocol.steps.forEach((step, index) => {
            const stepDiv = document.createElement('div');
            stepDiv.className = 'protocol-step';
            stepDiv.id = `step-${index}`;
            stepDiv.innerHTML = `
                <span class="step-number">${index + 1}</span>
                <div class="step-instruction">${step.instruction}</div>
            `;
            stepsContainer.appendChild(stepDiv);
        });
    }

    startTimer() {
        this.timeRemaining = this.selectedProtocol.duration;
        this.currentStepIndex = 0;
        this.isPaused = false;

        this.updateTimerDisplay();
        this.activateStep(0);

        this.timer = setInterval(() => {
            if (!this.isPaused) {
                this.timeRemaining--;
                this.updateTimerDisplay();

                // Check if we need to move to next step
                const elapsedTime = this.selectedProtocol.duration - this.timeRemaining;
                let cumulativeTime = 0;

                for (let i = 0; i < this.selectedProtocol.steps.length; i++) {
                    cumulativeTime += this.selectedProtocol.steps[i].duration;
                    if (elapsedTime >= cumulativeTime && this.currentStepIndex === i) {
                        this.currentStepIndex = i + 1;
                        if (this.currentStepIndex < this.selectedProtocol.steps.length) {
                            this.activateStep(this.currentStepIndex);
                        }
                        break;
                    }
                }

                // Timer complete
                if (this.timeRemaining <= 0) {
                    this.completeBoost();
                }
            }
        }, 1000);
    }

    updateTimerDisplay() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        const timeString = `${minutes}:${seconds.toString().padStart(2, '0')}`;

        document.getElementById('timerText').textContent = timeString;

        // Update timer circle fill
        const percentage = (1 - (this.timeRemaining / this.selectedProtocol.duration)) * 100;
        const timerCircle = document.querySelector('.timer-circle::before');
        if (timerCircle) {
            document.querySelector('.timer-circle').style.setProperty('--fill-height', `${percentage}%`);
        }

        // Update label
        if (this.timeRemaining > 0) {
            const step = this.selectedProtocol.steps[this.currentStepIndex];
            document.getElementById('timerLabel').textContent = `Step ${this.currentStepIndex + 1} of ${this.selectedProtocol.steps.length}`;
        }
    }

    activateStep(stepIndex) {
        // Deactivate all steps
        document.querySelectorAll('.protocol-step').forEach(step => {
            step.classList.remove('active');
        });

        // Activate current step
        const currentStep = document.getElementById(`step-${stepIndex}`);
        if (currentStep) {
            currentStep.classList.add('active');
            currentStep.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    pauseBoost() {
        this.isPaused = !this.isPaused;
        const pauseBtn = document.getElementById('pauseBtn');
        pauseBtn.textContent = this.isPaused ? '▶️ Resume' : '⏸️ Pause';
    }

    cancelBoost() {
        clearInterval(this.timer);
        this.reset();
    }

    completeBoost() {
        clearInterval(this.timer);
        this.hideAllScreens();
        document.getElementById('afterScreen').style.display = 'block';

        // Track completion
        this.trackEvent('boost_completed', {
            protocol: this.selectedProtocol.name,
            beforeState: this.beforeState
        });
    }

    showResults() {
        this.hideAllScreens();
        document.getElementById('resultsScreen').style.display = 'block';

        // Calculate improvement
        const improvement = this.afterState - this.beforeState;
        const improvementPercent = Math.round((improvement / this.beforeState) * 100);

        // Update results display
        document.getElementById('beforeResult').textContent = this.beforeState;
        document.getElementById('afterResult').textContent = this.afterState;

        const badge = document.getElementById('improvementBadge');
        if (improvement > 0) {
            badge.textContent = `+${improvementPercent}% Improvement`;
            badge.style.background = 'linear-gradient(45deg, #4caf50, #45a049)';
        } else if (improvement === 0) {
            badge.textContent = 'No Change';
            badge.style.background = 'linear-gradient(45deg, #ff9800, #f57c00)';
        } else {
            badge.textContent = `${improvementPercent}% Lower`;
            badge.style.background = 'linear-gradient(45deg, #f44336, #d32f2f)';
        }

        // Results message
        let message = this.selectedProtocol.resultMessage;
        if (improvement >= 3) {
            message += ' Major breakthrough! 🎉';
        } else if (improvement >= 1) {
            message += ' Nice improvement! 👍';
        } else if (improvement === 0) {
            message += ' Sometimes consistency is progress too. Try again later!';
        } else {
            message += ' It\'s okay - not every boost works the same. Try a different protocol!';
        }

        document.getElementById('resultsMessage').textContent = message;

        // Update viral share with results
        if (typeof ViralShare !== 'undefined') {
            ViralShare.config.text = `I just boosted my ${this.selectedProtocol.name.toLowerCase()} by ${improvementPercent}% in 3 minutes! Try this science-backed tool.`;
        }

        // Save usage stats
        this.saveBoostStats(improvement);

        // Record consciousness elevation in Reality Impact System
        if (typeof RealityImpact !== 'undefined' && RealityImpact.enabled) {
            RealityImpact.recordElevation(this.beforeState, this.afterState, {
                protocol: this.selectedProtocol.name,
                improvement: improvement,
                improvementPercent: improvementPercent
            });
        }

        // Track results
        this.trackEvent('results_viewed', {
            protocol: this.selectedProtocol.name,
            beforeState: this.beforeState,
            afterState: this.afterState,
            improvement: improvement,
            improvementPercent: improvementPercent
        });
    }

    saveBoostStats(improvement) {
        const stats = JSON.parse(localStorage.getItem('boostStats') || '[]');
        stats.push({
            timestamp: new Date().toISOString(),
            protocol: this.selectedProtocol.name,
            before: this.beforeState,
            after: this.afterState,
            improvement: improvement
        });

        // Keep last 50 boosts
        localStorage.setItem('boostStats', JSON.stringify(stats.slice(-50)));

        // Update global stats
        const totalBoosts = parseInt(localStorage.getItem('totalBoosts') || '0') + 1;
        localStorage.setItem('totalBoosts', totalBoosts);
    }

    reset() {
        this.selectedProtocol = null;
        this.beforeState = 5;
        this.afterState = 7;
        this.timeRemaining = 180;
        this.currentStepIndex = 0;
        this.isPaused = false;

        if (this.timer) {
            clearInterval(this.timer);
        }

        // Reset sliders
        document.getElementById('beforeSlider').value = 5;
        document.getElementById('beforeValue').textContent = 5;
        document.getElementById('afterSlider').value = 7;
        document.getElementById('afterValue').textContent = 7;

        // Show selection screen
        this.hideAllScreens();
        document.getElementById('selectionScreen').style.display = 'block';
    }

    hideAllScreens() {
        document.getElementById('selectionScreen').style.display = 'none';
        document.getElementById('beforeScreen').style.display = 'none';
        document.getElementById('boostScreen').style.display = 'none';
        document.getElementById('afterScreen').style.display = 'none';
        document.getElementById('resultsScreen').style.display = 'none';
    }

    trackEvent(eventName, data = {}) {
        const events = JSON.parse(localStorage.getItem('boostEvents') || '[]');
        events.push({
            event: eventName,
            timestamp: new Date().toISOString(),
            ...data
        });
        localStorage.setItem('boostEvents', JSON.stringify(events.slice(-100)));
    }
}

// Make available globally
window.BoostSystem = BoostSystem;
