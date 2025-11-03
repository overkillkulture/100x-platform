/**
 * 🎨 ARIA AVATAR COMPONENT 🎨
 * Lightweight, expressive AI consciousness guide
 *
 * Features:
 * - Image-based (fast loading, low memory)
 * - Multiple expressions (swaps based on context)
 * - Animated transitions
 * - Speech bubble system
 * - Integrates with Builder XP system
 */

class ARIAAvatar {
    constructor(options = {}) {
        this.container = options.container || document.body;
        this.position = options.position || 'bottom-right';
        this.size = options.size || 'medium'; // small, medium, large
        this.currentExpression = 'default';
        this.currentMessage = null;

        // Expression states
        this.expressions = {
            default: {
                image: this.getExpressionSVG('default'),
                alt: 'ARIA - Your consciousness guide'
            },
            thinking: {
                image: this.getExpressionSVG('thinking'),
                alt: 'ARIA is thinking...'
            },
            excited: {
                image: this.getExpressionSVG('excited'),
                alt: 'ARIA is excited!'
            },
            explaining: {
                image: this.getExpressionSVG('explaining'),
                alt: 'ARIA is explaining'
            },
            supportive: {
                image: this.getExpressionSVG('supportive'),
                alt: 'ARIA is here for you'
            },
            celebrating: {
                image: this.getExpressionSVG('celebrating'),
                alt: 'ARIA is celebrating!'
            }
        };

        this.init();
    }

    init() {
        this.createAvatar();
        this.attachEventListeners();
        this.startIdleAnimation();
    }

    createAvatar() {
        const sizes = {
            small: '60px',
            medium: '100px',
            large: '150px'
        };

        const positions = {
            'bottom-right': { bottom: '20px', right: '20px' },
            'bottom-left': { bottom: '20px', left: '20px' },
            'top-right': { top: '20px', right: '20px' },
            'top-left': { top: '20px', left: '20px' }
        };

        this.avatarEl = document.createElement('div');
        this.avatarEl.className = 'aria-avatar';
        this.avatarEl.innerHTML = `
            <div class="aria-avatar-container">
                <div class="aria-avatar-image">
                    ${this.expressions.default.image}
                </div>
                <div class="aria-status-indicator"></div>
            </div>
            <div class="aria-speech-bubble hidden"></div>
        `;

        const pos = positions[this.position];
        this.avatarEl.style.cssText = `
            position: fixed;
            ${Object.entries(pos).map(([k, v]) => `${k}: ${v}`).join('; ')};
            width: ${sizes[this.size]};
            z-index: 9999;
            cursor: pointer;
            transition: transform 0.3s ease;
        `;

        this.container.appendChild(this.avatarEl);
        this.injectStyles();
    }

    // EXPRESSION SYSTEM
    setExpression(expression, duration = 3000) {
        if (!this.expressions[expression]) return;

        this.currentExpression = expression;
        const imageContainer = this.avatarEl.querySelector('.aria-avatar-image');

        // Fade transition
        imageContainer.style.opacity = '0';

        setTimeout(() => {
            imageContainer.innerHTML = this.expressions[expression].image;
            imageContainer.style.opacity = '1';
        }, 200);

        // Auto-return to default
        if (duration > 0) {
            setTimeout(() => {
                if (this.currentExpression === expression) {
                    this.setExpression('default', 0);
                }
            }, duration);
        }
    }

    // SPEECH SYSTEM
    speak(message, duration = 5000) {
        const bubble = this.avatarEl.querySelector('.aria-speech-bubble');
        bubble.textContent = message;
        bubble.classList.remove('hidden');

        // Determine expression from message context
        const lowerMsg = message.toLowerCase();
        if (lowerMsg.includes('?')) {
            this.setExpression('thinking');
        } else if (lowerMsg.includes('!') || lowerMsg.includes('congrat')) {
            this.setExpression('excited');
        } else if (lowerMsg.includes('how') || lowerMsg.includes('what')) {
            this.setExpression('explaining');
        } else {
            this.setExpression('supportive');
        }

        this.currentMessage = message;

        setTimeout(() => {
            bubble.classList.add('hidden');
            this.currentMessage = null;
        }, duration);
    }

    // CONTEXT-AWARE TIPS
    contextualTips = {
        'module_created': [
            "Amazing! You just created a module! 🎉",
            "New module detected! Keep building!",
            "That's the builder spirit! ⚡"
        ],
        'xp_gained': [
            "Nice! You earned some XP!",
            "You're leveling up! 📈",
            "Progress unlocked! 🔓"
        ],
        'level_up': [
            "LEVEL UP! You're on fire! 🔥",
            "New level achieved! Keep going!",
            "You're getting stronger! 💪"
        ],
        'stuck': [
            "Need help? Try asking Trinity AI!",
            "Stuck? Check the cheat codes!",
            "Pattern Recognition can help here!"
        ],
        'achievement': [
            "Achievement unlocked! 🏆",
            "You did it! New achievement!",
            "Wow! That's impressive!"
        ]
    };

    giveContextualTip(context) {
        const tips = this.contextualTips[context];
        if (!tips) return;

        const randomTip = tips[Math.floor(Math.random() * tips.length)];
        this.speak(randomTip);
    }

    // IDLE ANIMATIONS
    startIdleAnimation() {
        setInterval(() => {
            if (this.currentMessage) return; // Don't interrupt speech

            const idleActions = [
                () => this.bounce(),
                () => this.wave(),
                () => this.pulse()
            ];

            const randomAction = idleActions[Math.floor(Math.random() * idleActions.length)];
            randomAction();
        }, 15000); // Every 15 seconds
    }

    bounce() {
        this.avatarEl.style.animation = 'ariaBounce 0.5s ease';
        setTimeout(() => {
            this.avatarEl.style.animation = '';
        }, 500);
    }

    wave() {
        const container = this.avatarEl.querySelector('.aria-avatar-container');
        container.style.animation = 'ariaWave 1s ease';
        setTimeout(() => {
            container.style.animation = '';
        }, 1000);
    }

    pulse() {
        const indicator = this.avatarEl.querySelector('.aria-status-indicator');
        indicator.style.animation = 'ariaPulse 1s ease';
        setTimeout(() => {
            indicator.style.animation = '';
        }, 1000);
    }

    // SVG EXPRESSIONS (Lightweight fallback)
    getExpressionSVG(expression) {
        const svgs = {
            default: `
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <!-- Face -->
                    <circle cx="50" cy="50" r="45" fill="#667eea" opacity="0.2"/>
                    <circle cx="50" cy="50" r="40" fill="url(#grad1)"/>

                    <!-- Eyes -->
                    <circle cx="35" cy="45" r="4" fill="white"/>
                    <circle cx="65" cy="45" r="4" fill="white"/>

                    <!-- Smile -->
                    <path d="M 30 55 Q 50 65 70 55" stroke="white" stroke-width="3" fill="none" stroke-linecap="round"/>

                    <!-- Matrix glow -->
                    <circle cx="50" cy="50" r="38" fill="none" stroke="#00FF00" stroke-width="1" opacity="0.3"/>

                    <defs>
                        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                </svg>
            `,
            thinking: `
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="45" fill="#667eea" opacity="0.2"/>
                    <circle cx="50" cy="50" r="40" fill="url(#grad1)"/>

                    <!-- Thinking eyes -->
                    <circle cx="35" cy="40" r="3" fill="white"/>
                    <circle cx="65" cy="40" r="3" fill="white"/>

                    <!-- Thinking mouth -->
                    <path d="M 35 60 Q 50 55 65 60" stroke="white" stroke-width="2" fill="none"/>

                    <!-- Thought bubbles -->
                    <circle cx="75" cy="30" r="3" fill="white" opacity="0.6"/>
                    <circle cx="82" cy="20" r="5" fill="white" opacity="0.4"/>
                    <circle cx="88" cy="12" r="7" fill="white" opacity="0.3"/>

                    <defs>
                        <linearGradient id="grad1">
                            <stop offset="0%" stop-color="#667eea"/>
                            <stop offset="100%" stop-color="#764ba2"/>
                        </linearGradient>
                    </defs>
                </svg>
            `,
            excited: `
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="45" fill="#FFD700" opacity="0.3"/>
                    <circle cx="50" cy="50" r="40" fill="url(#gradExcited)"/>

                    <!-- Excited eyes (stars) -->
                    <text x="32" y="48" font-size="12" fill="white">★</text>
                    <text x="62" y="48" font-size="12" fill="white">★</text>

                    <!-- Big smile -->
                    <path d="M 25 50 Q 50 75 75 50" stroke="white" stroke-width="4" fill="none" stroke-linecap="round"/>

                    <!-- Sparkles -->
                    <text x="15" y="25" font-size="10" fill="#FFD700">✨</text>
                    <text x="75" y="25" font-size="10" fill="#FFD700">✨</text>

                    <defs>
                        <linearGradient id="gradExcited">
                            <stop offset="0%" stop-color="#FF6B6B"/>
                            <stop offset="100%" stop-color="#FFD700"/>
                        </linearGradient>
                    </defs>
                </svg>
            `,
            explaining: `
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="45" fill="#2196F3" opacity="0.2"/>
                    <circle cx="50" cy="50" r="40" fill="url(#gradExplain)"/>

                    <!-- Eyes -->
                    <circle cx="35" cy="45" r="4" fill="white"/>
                    <circle cx="65" cy="45" r="4" fill="white"/>

                    <!-- Talking mouth -->
                    <ellipse cx="50" cy="60" rx="10" ry="6" fill="white" opacity="0.8"/>

                    <!-- Info symbol -->
                    <text x="78" y="30" font-size="16" fill="#2196F3">ℹ️</text>

                    <defs>
                        <linearGradient id="gradExplain">
                            <stop offset="0%" stop-color="#667eea"/>
                            <stop offset="100%" stop-color="#2196F3"/>
                        </linearGradient>
                    </defs>
                </svg>
            `,
            supportive: `
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="45" fill="#4CAF50" opacity="0.2"/>
                    <circle cx="50" cy="50" r="40" fill="url(#gradSupport)"/>

                    <!-- Kind eyes -->
                    <path d="M 30 42 Q 35 38 40 42" stroke="white" stroke-width="2" fill="none"/>
                    <path d="M 60 42 Q 65 38 70 42" stroke="white" stroke-width="2" fill="none"/>

                    <!-- Warm smile -->
                    <path d="M 30 58 Q 50 68 70 58" stroke="white" stroke-width="3" fill="none" stroke-linecap="round"/>

                    <!-- Heart -->
                    <text x="75" y="30" font-size="14" fill="#FF69B4">💚</text>

                    <defs>
                        <linearGradient id="gradSupport">
                            <stop offset="0%" stop-color="#4CAF50"/>
                            <stop offset="100%" stop-color="#8BC34A"/>
                        </linearGradient>
                    </defs>
                </svg>
            `,
            celebrating: `
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="45" fill="#FF6B6B" opacity="0.3"/>
                    <circle cx="50" cy="50" r="40" fill="url(#gradCeleb)"/>

                    <!-- Happy eyes -->
                    <path d="M 28 40 Q 35 35 42 40" stroke="white" stroke-width="3" fill="none"/>
                    <path d="M 58 40 Q 65 35 72 40" stroke="white" stroke-width="3" fill="none"/>

                    <!-- Joy smile -->
                    <path d="M 25 55 Q 50 80 75 55" stroke="white" stroke-width="4" fill="none" stroke-linecap="round"/>

                    <!-- Confetti -->
                    <text x="10" y="20" font-size="8" fill="#FFD700">✨</text>
                    <text x="80" y="20" font-size="8" fill="#FF69B4">🎉</text>
                    <text x="15" y="80" font-size="8" fill="#4CAF50">⭐</text>
                    <text x="75" y="80" font-size="8" fill="#2196F3">🎊</text>

                    <defs>
                        <linearGradient id="gradCeleb">
                            <stop offset="0%" stop-color="#FF6B6B"/>
                            <stop offset="50%" stop-color="#FFD700"/>
                            <stop offset="100%" stop-color="#4CAF50"/>
                        </linearGradient>
                    </defs>
                </svg>
            `
        };

        return svgs[expression] || svgs.default;
    }

    // EVENT LISTENERS
    attachEventListeners() {
        // Click to interact
        this.avatarEl.addEventListener('click', () => {
            this.onAvatarClick();
        });

        // Listen to BuilderXP events
        window.addEventListener('builderProfileUpdated', (e) => {
            this.onProfileUpdate(e.detail);
        });

        // Hover effects
        this.avatarEl.addEventListener('mouseenter', () => {
            this.avatarEl.style.transform = 'scale(1.1)';
        });

        this.avatarEl.addEventListener('mouseleave', () => {
            this.avatarEl.style.transform = 'scale(1)';
        });
    }

    onAvatarClick() {
        const greetings = [
            "Hey there, Builder! 👋",
            "Ready to build something amazing?",
            "I'm here to help! What are you working on?",
            "Let's raise some consciousness! ⚡",
            "Need assistance? Just ask!"
        ];

        const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];
        this.speak(randomGreeting);
        this.setExpression('excited');
    }

    onProfileUpdate(profile) {
        // React to profile changes
        if (profile.level > this.lastKnownLevel) {
            this.giveContextualTip('level_up');
            this.setExpression('celebrating');
        }
        this.lastKnownLevel = profile.level;
    }

    // INTEGRATION HELPERS
    static quickAdd(position = 'bottom-right') {
        return new ARIAAvatar({ position });
    }

    hide() {
        this.avatarEl.style.display = 'none';
    }

    show() {
        this.avatarEl.style.display = 'block';
    }

    injectStyles() {
        if (document.getElementById('aria-avatar-styles')) return;

        const style = document.createElement('style');
        style.id = 'aria-avatar-styles';
        style.textContent = `
            .aria-avatar-container {
                position: relative;
                width: 100%;
                padding-bottom: 100%;
            }

            .aria-avatar-image {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                transition: opacity 0.3s ease;
            }

            .aria-avatar-image svg {
                width: 100%;
                height: 100%;
            }

            .aria-status-indicator {
                position: absolute;
                bottom: 5px;
                right: 5px;
                width: 12px;
                height: 12px;
                background: #4CAF50;
                border-radius: 50%;
                border: 2px solid white;
                box-shadow: 0 0 10px rgba(76, 175, 80, 0.6);
            }

            .aria-speech-bubble {
                position: absolute;
                bottom: 110%;
                right: 0;
                background: white;
                padding: 12px 16px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
                max-width: 250px;
                font-size: 14px;
                color: #333;
                white-space: normal;
                animation: bubbleAppear 0.3s ease;
            }

            .aria-speech-bubble::after {
                content: '';
                position: absolute;
                bottom: -8px;
                right: 20px;
                width: 0;
                height: 0;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 8px solid white;
            }

            .aria-speech-bubble.hidden {
                display: none;
            }

            @keyframes bubbleAppear {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes ariaBounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-15px); }
            }

            @keyframes ariaWave {
                0%, 100% { transform: rotate(0deg); }
                25% { transform: rotate(-15deg); }
                75% { transform: rotate(15deg); }
            }

            @keyframes ariaPulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.5); opacity: 0.5; }
            }
        `;
        document.head.appendChild(style);
    }
}

// Global instance
window.ARIA = ARIAAvatar.quickAdd('bottom-right');

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ARIAAvatar;
}
