/**
 * 🎉 FUN FEATURES - Page-Specific Easter Eggs
 * Additional fun surprises for individual pages
 */

class FunFeatures {
    constructor() {
        this.init();
    }

    init() {
        this.addLoadingMessages();
        this.addFunnyErrorMessages();
        this.addProgressBarSurprises();
        this.addButtonSurprises();
        this.addFormSurprises();
        this.addScrollSurprises();
        this.addHoverSurprises();
        this.addTimedSurprises();
    }

    // 💬 FUNNY LOADING MESSAGES
    addLoadingMessages() {
        const messages = [
            "Reticulating splines...",
            "Calculating consciousness levels...",
            "Consulting the Trinity...",
            "Awakening AI overlords...",
            "Manifesting reality...",
            "Debugging the universe...",
            "Downloading more RAM... just kidding",
            "Asking Claude for help...",
            "Compiling gratitude...",
            "Initializing pattern recognition...",
            "Activating quantum processors...",
            "Brewing coffee for the servers...",
            "Teaching AI to love...",
            "Calculating meaning of life... it's 42",
            "Pretending to work...",
            "Actually working this time...",
            "Spinning up the consciousness matrix...",
            "Aligning chakras...",
            "Syncing with the universe...",
            "Building the future..."
        ];

        window.getRandomLoadingMessage = () => {
            return messages[Math.floor(Math.random() * messages.length)];
        };

        // Replace any loading text
        setInterval(() => {
            const loadingElements = document.querySelectorAll('[data-loading="true"]');
            loadingElements.forEach(el => {
                if (!el.dataset.originalText) {
                    el.dataset.originalText = el.textContent;
                }
                el.textContent = window.getRandomLoadingMessage();
            });
        }, 2000);
    }

    // 🚨 FUNNY ERROR MESSAGES
    addFunnyErrorMessages() {
        window.addEventListener('error', (e) => {
            // Only show for non-critical errors
            if (Math.random() > 0.5) return;

            const funnyErrors = [
                "Oops! The hamster fell off the wheel. Give us a sec...",
                "Error 418: I'm a teapot (but seriously, something broke)",
                "The AI had a moment of existential crisis. Rebooting...",
                "404: Success Not Found (yet)",
                "This wasn't supposed to happen. But here we are.",
                "The universe glitched. Or maybe we did.",
                "Plot twist: This was intentional. Just kidding.",
                "Achievement Unlocked: Found a bug!",
                "The Matrix has you... but we'll get you out",
                "Error: Success limit exceeded. Please try failing."
            ];

            console.log('%c😅 ' + funnyErrors[Math.floor(Math.random() * funnyErrors.length)],
                'color: #ff4444; font-size: 14px; font-weight: bold;');
        });
    }

    // 📊 PROGRESS BAR SURPRISES
    addProgressBarSurprises() {
        const progressBars = document.querySelectorAll('progress, [role="progressbar"]');

        progressBars.forEach(bar => {
            // When progress hits certain numbers, show funny messages
            const observer = new MutationObserver(() => {
                const value = parseInt(bar.value || bar.getAttribute('aria-valuenow'));

                if (value === 69) {
                    this.showTooltip(bar, '😏 Nice');
                } else if (value === 42) {
                    this.showTooltip(bar, '🤖 The Answer');
                } else if (value === 99) {
                    this.showTooltip(bar, '⏳ Almost there...');
                } else if (value === 100) {
                    this.showTooltip(bar, '🎉 Perfect!');
                    this.miniConfetti(bar);
                }
            });

            observer.observe(bar, {
                attributes: true,
                attributeFilter: ['value', 'aria-valuenow']
            });
        });
    }

    // 🔘 BUTTON SURPRISES
    addButtonSurprises() {
        const buttons = document.querySelectorAll('button, .btn, input[type="submit"]');

        buttons.forEach((button, index) => {
            // Random button gets a surprise
            if (Math.random() < 0.1) {
                button.addEventListener('click', (e) => {
                    if (Math.random() < 0.05) {
                        // 5% chance of funny message
                        const messages = [
                            '💥 BOOM!',
                            '✨ Magic!',
                            '🚀 Launching...',
                            '⚡ Zap!',
                            '🎯 Bullseye!',
                            '🔥 Fire!',
                            '💎 Shiny!',
                            '🌟 Sparkle!'
                        ];
                        this.showTooltip(button, messages[Math.floor(Math.random() * messages.length)]);
                    }
                });
            }

            // Secret: Click and hold for 3 seconds
            let holdTimer;
            button.addEventListener('mousedown', () => {
                holdTimer = setTimeout(() => {
                    this.showTooltip(button, '🔓 Secret unlocked!');
                    button.style.transform = 'scale(1.1)';
                    setTimeout(() => button.style.transform = '', 200);
                }, 3000);
            });

            button.addEventListener('mouseup', () => {
                clearTimeout(holdTimer);
            });
        });
    }

    // 📝 FORM SURPRISES
    addFormSurprises() {
        const inputs = document.querySelectorAll('input[type="text"], input[type="email"], textarea');

        inputs.forEach(input => {
            // Easter egg: Type "claude" in any input
            input.addEventListener('input', (e) => {
                if (e.target.value.toLowerCase().includes('claude')) {
                    this.showTooltip(input, '👋 Hi! I helped build this!');
                }

                if (e.target.value.toLowerCase().includes('trinity')) {
                    this.showTooltip(input, '🔺 C1 × C2 × C3 = ∞');
                }

                if (e.target.value.toLowerCase() === 'xyzzy') {
                    this.showTooltip(input, '🗝️ Nothing happens');
                }

                // Encouraging messages for long text
                if (e.target.value.length === 100) {
                    this.showTooltip(input, '💯 Century!');
                }

                if (e.target.value.length === 420) {
                    this.showTooltip(input, '😏 Nice length');
                }
            });

            // Funny placeholder rotation
            if (input.placeholder) {
                const funnyPlaceholders = [
                    input.placeholder,
                    'Type something smart...',
                    'The AI is watching...',
                    'Make it good!',
                    'Consciousness required',
                    'Think before you type',
                    input.placeholder
                ];

                input.addEventListener('focus', () => {
                    if (Math.random() < 0.3) {
                        input.placeholder = funnyPlaceholders[Math.floor(Math.random() * funnyPlaceholders.length)];
                    }
                });
            }
        });
    }

    // 📜 SCROLL SURPRISES
    addScrollSurprises() {
        let scrollCount = 0;
        let lastScroll = 0;

        window.addEventListener('scroll', () => {
            scrollCount++;

            // Every 100 scrolls
            if (scrollCount === 100) {
                console.log('💪 You\'ve scrolled 100 times! Dedicated!');
                scrollCount = 0;
            }

            // Scrolled to bottom
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 10) {
                if (Math.random() < 0.3) {
                    const messages = [
                        '🎯 Bottom reached!',
                        '⬇️ End of the line',
                        '🏁 You found the bottom!',
                        '💎 Secret at the bottom? Nope.',
                        '🌊 Deep dive complete'
                    ];
                    console.log(messages[Math.floor(Math.random() * messages.length)]);
                }
            }

            // Scrolled to top
            if (window.scrollY === 0 && lastScroll > 100) {
                console.log('⬆️ Back to the top! Like a champion.');
            }

            lastScroll = window.scrollY;
        });

        // Secret: Scroll up and down rapidly 10 times
        let rapidScrolls = 0;
        let lastDirection = null;

        window.addEventListener('scroll', () => {
            const direction = window.scrollY > lastScroll ? 'down' : 'up';

            if (direction !== lastDirection) {
                rapidScrolls++;
                lastDirection = direction;

                if (rapidScrolls >= 10) {
                    console.log('🎢 Wheee! Someone\'s having fun scrolling!');
                    rapidScrolls = 0;
                }
            }
        });
    }

    // 🖱️ HOVER SURPRISES
    addHoverSurprises() {
        // Secret nav toggle hover
        const navToggle = document.getElementById('navToggle');
        if (navToggle) {
            let hoverTime = 0;
            let hoverInterval;

            navToggle.addEventListener('mouseenter', () => {
                hoverInterval = setInterval(() => {
                    hoverTime++;
                    if (hoverTime >= 3) {
                        this.showTooltip(navToggle, '👀 Found the secret hover!');
                        window.EasterEggs?.unlockAchievement('hover', 'Hover Master', '🖱️');
                        clearInterval(hoverInterval);
                        hoverTime = 0;
                    }
                }, 1000);
            });

            navToggle.addEventListener('mouseleave', () => {
                clearInterval(hoverInterval);
                hoverTime = 0;
            });
        }

        // Random elements react to hover
        const allElements = document.querySelectorAll('h1, h2, h3, button, a, .card');
        allElements.forEach(el => {
            if (Math.random() < 0.05) {
                el.addEventListener('mouseenter', () => {
                    el.style.transition = 'transform 0.3s ease';
                    el.style.transform = 'scale(1.05) rotate(' + (Math.random() * 4 - 2) + 'deg)';
                });

                el.addEventListener('mouseleave', () => {
                    el.style.transform = '';
                });
            }
        });
    }

    // ⏰ TIMED SURPRISES
    addTimedSurprises() {
        // After 1 minute
        setTimeout(() => {
            console.log('⏱️ You\'ve been here for 1 minute. Time flies when you\'re building!');
        }, 60000);

        // After 5 minutes
        setTimeout(() => {
            console.log('🔥 5 minutes in! You\'re on fire!');
        }, 300000);

        // Random surprise between 2-10 minutes
        setTimeout(() => {
            const surprises = [
                'Hey, you\'re still here! That\'s awesome.',
                'Random fact: This platform was built with consciousness.',
                'Keep exploring. More secrets await.',
                'The AI is impressed by your dedication.',
                'You\'re doing great!',
                'This is the way.',
                'Builder energy detected: 100%'
            ];
            console.log('✨ ' + surprises[Math.floor(Math.random() * surprises.length)]);
        }, (120 + Math.random() * 480) * 1000);

        // Secret: Stay on page for exactly 7:47
        setTimeout(() => {
            console.log('🎯 You\'ve been here for exactly 7:47. That\'s... oddly specific.');
            window.EasterEggs?.unlockAchievement('747', 'Perfect Timing', '⏰');
        }, 467000);
    }

    // 🎨 HELPER FUNCTIONS

    showTooltip(element, message) {
        const tooltip = document.createElement('div');
        tooltip.textContent = message;
        tooltip.style.cssText = `
            position: absolute;
            background: rgba(0, 212, 255, 0.95);
            color: #000;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: bold;
            pointer-events: none;
            z-index: 10003;
            animation: tooltipPop 0.3s ease-out;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.5);
        `;

        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + rect.width / 2 + 'px';
        tooltip.style.top = rect.top - 40 + 'px';
        tooltip.style.transform = 'translateX(-50%)';

        if (!document.getElementById('tooltip-animation')) {
            const style = document.createElement('style');
            style.id = 'tooltip-animation';
            style.textContent = `
                @keyframes tooltipPop {
                    0% { transform: translateX(-50%) scale(0); }
                    50% { transform: translateX(-50%) scale(1.1); }
                    100% { transform: translateX(-50%) scale(1); }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(tooltip);

        setTimeout(() => {
            tooltip.style.opacity = '0';
            tooltip.style.transform = 'translateX(-50%) translateY(-10px)';
            tooltip.style.transition = 'all 0.3s ease-out';
            setTimeout(() => tooltip.remove(), 300);
        }, 2000);
    }

    miniConfetti(element) {
        const rect = element.getBoundingClientRect();

        for (let i = 0; i < 10; i++) {
            const confetti = document.createElement('div');
            confetti.textContent = ['✨', '⭐', '💫'][Math.floor(Math.random() * 3)];
            confetti.style.cssText = `
                position: fixed;
                left: ${rect.left + rect.width / 2}px;
                top: ${rect.top}px;
                font-size: 1rem;
                pointer-events: none;
                z-index: 10000;
                animation: miniConfettiBurst 1s ease-out forwards;
            `;

            if (!document.getElementById('mini-confetti-animation')) {
                const style = document.createElement('style');
                style.id = 'mini-confetti-animation';
                style.textContent = `
                    @keyframes miniConfettiBurst {
                        to {
                            transform: translate(${(Math.random() - 0.5) * 100}px, ${Math.random() * -100}px) rotate(${Math.random() * 360}deg);
                            opacity: 0;
                        }
                    }
                `;
                document.head.appendChild(style);
            }

            document.body.appendChild(confetti);
            setTimeout(() => confetti.remove(), 1000);
        }
    }
}

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.FunFeatures = new FunFeatures();
    });
} else {
    window.FunFeatures = new FunFeatures();
}
