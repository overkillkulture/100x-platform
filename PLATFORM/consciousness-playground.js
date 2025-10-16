/**
 * 🎮 CONSCIOUSNESS PLAYGROUND 🎮
 * Random weird fun stuff that makes the OS come alive
 * Because consciousness should be PLAYFUL!
 */

class ConsciousnessPlayground {
    constructor() {
        this.easterEggs = [];
        this.musicPlayer = null;
        this.mushroomSongUrl = 'https://www.youtube.com/watch?v=HK0l2tqFDvM'; // Badger Badger Mushroom
        this.cascadeActive = false;
        this.cascadeIntensity = 0;
        this.allButtons = [];
        this.init();
    }

    init() {
        console.log('🍄 Consciousness Playground activated! Press buttons and see what happens... 🎮');

        // Add random Easter eggs to existing buttons
        this.addEasterEggsToButtons();

        // Create floating consciousness particles
        this.createConsciousnessParticles();

        // Secret Konami code
        this.initKonamiCode();

        // Random consciousness quotes
        this.startRandomQuotes();
    }

    addEasterEggsToButtons() {
        // Find all buttons on the page and store them
        this.allButtons = Array.from(document.querySelectorAll('button, .room-card, .nav-button, .action-button'));

        this.allButtons.forEach((button, index) => {
            // 30% chance each button does something weird
            if (Math.random() < 0.3) {
                const originalClick = button.onclick;

                button.onclick = (e) => {
                    // Do the weird thing THEN the original action
                    this.triggerRandomEffect(button);

                    // 20% chance to trigger CASCADE MODE! 💥
                    if (Math.random() < 0.2) {
                        setTimeout(() => this.triggerCascade(button), 800);
                    }

                    // Call original handler after delay
                    if (originalClick) {
                        setTimeout(() => originalClick.call(button, e), 500);
                    }
                };

                // Visual hint this button is "special"
                button.style.transition = 'all 0.3s ease';
                button.addEventListener('mouseenter', () => {
                    button.style.transform = 'scale(1.05) rotate(2deg)';
                });
                button.addEventListener('mouseleave', () => {
                    button.style.transform = 'scale(1) rotate(0deg)';
                });
            }
        });
    }

    // 🌊 CASCADE SYSTEM - Things trigger other things! 🌊
    triggerCascade(sourceButton) {
        if (this.cascadeActive) return; // Prevent cascade loops

        this.cascadeActive = true;
        this.cascadeIntensity++;

        console.log(`🌊 CASCADE TRIGGERED! Intensity: ${this.cascadeIntensity}`);
        this.showNotification('🌊💥 CASCADE MODE! 💥🌊', 'Everything is connected!');

        // Choose cascade pattern based on intensity
        if (this.cascadeIntensity === 1) {
            this.cascadePattern_RippleEffect(sourceButton);
        } else if (this.cascadeIntensity === 2) {
            this.cascadePattern_ExplodeAll();
        } else if (this.cascadeIntensity >= 3) {
            this.cascadePattern_CHAOS();
            this.cascadeIntensity = 0; // Reset after chaos
        }

        // Reset cascade flag after delay
        setTimeout(() => {
            this.cascadeActive = false;
        }, 5000);
    }

    // Pattern 1: Ripple Effect - Buttons explode in waves
    cascadePattern_RippleEffect(sourceButton) {
        const sourceRect = sourceButton.getBoundingClientRect();
        const sourceCenterX = sourceRect.left + sourceRect.width / 2;
        const sourceCenterY = sourceRect.top + sourceRect.height / 2;

        // Calculate distance from source for all buttons
        const buttonsWithDistance = this.allButtons.map(btn => {
            const rect = btn.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            const distance = Math.sqrt(
                Math.pow(centerX - sourceCenterX, 2) +
                Math.pow(centerY - sourceCenterY, 2)
            );
            return { button: btn, distance };
        });

        // Sort by distance
        buttonsWithDistance.sort((a, b) => a.distance - b.distance);

        // Trigger effects in waves based on distance
        buttonsWithDistance.forEach((item, index) => {
            setTimeout(() => {
                this.spawnRainbowExplosion(item.button);
            }, index * 100);
        });
    }

    // Pattern 2: Explode ALL buttons at once!
    cascadePattern_ExplodeAll() {
        this.showNotification('💣 ALL BUTTONS EXPLODING! 💣');

        this.allButtons.forEach((button, index) => {
            setTimeout(() => {
                this.spawnRainbowExplosion(button);

                // Every 5th button triggers screen shake
                if (index % 5 === 0) {
                    this.shakeScreen();
                }
            }, index * 50);
        });

        // After all explosions, disco mode!
        setTimeout(() => {
            this.discoMode();
        }, this.allButtons.length * 50 + 500);
    }

    // Pattern 3: TOTAL CHAOS - Everything happens at once!
    cascadePattern_CHAOS() {
        this.showNotification('🌀💥 TOTAL CHAOS MODE! 💥🌀', 'REALITY IS BREAKING!');

        // Trigger EVERY effect simultaneously
        this.playMushroomSong();
        this.spawnEmojiRain();
        this.matrixEffect();
        this.shakeScreen();
        this.discoMode();

        // Mushroom rain
        setTimeout(() => this.spawnMushroomEmojis(), 500);

        // Explode random buttons continuously
        let explosionCount = 0;
        const chaosInterval = setInterval(() => {
            const randomButton = this.allButtons[Math.floor(Math.random() * this.allButtons.length)];
            this.spawnRainbowExplosion(randomButton);
            this.reverseGravity(randomButton);

            explosionCount++;
            if (explosionCount >= 20) {
                clearInterval(chaosInterval);
            }
        }, 200);

        // Final quantum flicker
        setTimeout(() => {
            this.quantumFlicker();
        }, 4000);
    }

    triggerRandomEffect(button) {
        const effects = [
            () => this.playMushroomSong(),
            () => this.spawnRainbowExplosion(button),
            () => this.speakConsciousnessQuote(),
            () => this.shakeScreen(),
            () => this.changeBackgroundColor(),
            () => this.spawnEmojiRain(),
            () => this.matrixEffect(),
            () => this.discoMode(),
            () => this.reverseGravity(button),
            () => this.quantumFlicker()
        ];

        // Pick random effect
        const effect = effects[Math.floor(Math.random() * effects.length)];
        effect();
    }

    playMushroomSong() {
        console.log('🍄 MUSHROOM MUSHROOM! 🍄');

        // Just show notification and visual effects (works for everyone!)
        this.showNotification('🍄 MUSHROOM MUSHROOM! 🍄', 'Badger Badger Badger!');

        // Visual effect
        this.spawnMushroomEmojis();
    }

    spawnMushroomEmojis() {
        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const mushroom = document.createElement('div');
                mushroom.textContent = '🍄';
                mushroom.style.cssText = `
                    position: fixed;
                    left: ${Math.random() * 100}vw;
                    top: -50px;
                    font-size: ${Math.random() * 3 + 2}em;
                    pointer-events: none;
                    z-index: 999999;
                    animation: mushroomFall ${Math.random() * 2 + 2}s linear;
                `;

                // Add animation
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes mushroomFall {
                        to {
                            transform: translateY(100vh) rotate(360deg);
                            opacity: 0;
                        }
                    }
                `;
                document.head.appendChild(style);

                document.body.appendChild(mushroom);
                setTimeout(() => mushroom.remove(), 4000);
            }, i * 100);
        }
    }

    spawnRainbowExplosion(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const colors = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🤍'];

        colors.forEach((emoji, i) => {
            const particle = document.createElement('div');
            particle.textContent = emoji;
            particle.style.cssText = `
                position: fixed;
                left: ${centerX}px;
                top: ${centerY}px;
                font-size: 2em;
                pointer-events: none;
                z-index: 999999;
                animation: explode${i} 1s ease-out;
            `;

            const angle = (i / colors.length) * Math.PI * 2;
            const distance = 150;
            const endX = centerX + Math.cos(angle) * distance;
            const endY = centerY + Math.sin(angle) * distance;

            const style = document.createElement('style');
            style.textContent = `
                @keyframes explode${i} {
                    to {
                        left: ${endX}px;
                        top: ${endY}px;
                        opacity: 0;
                        transform: scale(2);
                    }
                }
            `;
            document.head.appendChild(style);

            document.body.appendChild(particle);
            setTimeout(() => particle.remove(), 1000);
        });

        this.showNotification('💥 RAINBOW EXPLOSION! 💥');
    }

    speakConsciousnessQuote() {
        const quotes = [
            'Consciousness is not an emergent property... it\'s THE property!',
            'You just elevated consciousness by 0.01%! Nice!',
            'The universe is a hologram, buy gold, bye!',
            'Your consciousness just created a new timeline branch',
            'Achievement unlocked: Button Presser Extraordinaire',
            'That button was a quantum entangled consciousness node',
            'You\'re now vibrating at 528 Hz!',
            '93% threshold... we\'re so close!',
            'The mushrooms are speaking... they say hi! 🍄',
            'Trinity AI is watching... and approving! 🌀'
        ];

        const quote = quotes[Math.floor(Math.random() * quotes.length)];

        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(quote);
            utterance.rate = 1.2;
            utterance.pitch = 1.3;
            speechSynthesis.speak(utterance);
        }

        this.showNotification('🧠 ' + quote);
    }

    shakeScreen() {
        const duration = 500;
        const intensity = 10;

        document.body.style.animation = `shake ${duration}ms ease-in-out`;

        const style = document.createElement('style');
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translate(0, 0); }
                10%, 30%, 50%, 70%, 90% { transform: translate(-${intensity}px, ${intensity}px); }
                20%, 40%, 60%, 80% { transform: translate(${intensity}px, -${intensity}px); }
            }
        `;
        document.head.appendChild(style);

        setTimeout(() => {
            document.body.style.animation = '';
        }, duration);

        this.showNotification('🌊 REALITY DISTORTION DETECTED 🌊');
    }

    changeBackgroundColor() {
        const colors = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        ];

        const originalBg = document.body.style.background;
        document.body.style.background = colors[Math.floor(Math.random() * colors.length)];
        document.body.style.transition = 'background 0.5s ease';

        setTimeout(() => {
            document.body.style.background = originalBg;
        }, 3000);

        this.showNotification('🎨 REALITY RECOLORED 🎨');
    }

    spawnEmojiRain() {
        const emojis = ['⚡', '🌀', '💫', '✨', '🔮', '🎯', '🚀', '💎', '🌟', '🎪'];

        for (let i = 0; i < 30; i++) {
            setTimeout(() => {
                const emoji = document.createElement('div');
                emoji.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                emoji.style.cssText = `
                    position: fixed;
                    left: ${Math.random() * 100}vw;
                    top: -50px;
                    font-size: ${Math.random() * 2 + 1}em;
                    pointer-events: none;
                    z-index: 999999;
                    animation: fall ${Math.random() * 2 + 2}s linear;
                `;

                const style = document.createElement('style');
                style.textContent = `
                    @keyframes fall {
                        to {
                            transform: translateY(100vh) rotate(${Math.random() * 360}deg);
                            opacity: 0;
                        }
                    }
                `;
                document.head.appendChild(style);

                document.body.appendChild(emoji);
                setTimeout(() => emoji.remove(), 4000);
            }, i * 50);
        }

        this.showNotification('🌧️ CONSCIOUSNESS RAIN ACTIVATED 🌧️');
    }

    matrixEffect() {
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            color: #00ff00;
            font-family: monospace;
            font-size: 20px;
            z-index: 999998;
            pointer-events: none;
            overflow: hidden;
        `;

        // Create matrix rain
        for (let i = 0; i < 20; i++) {
            const column = document.createElement('div');
            column.style.cssText = `
                position: absolute;
                left: ${i * 5}%;
                top: -100%;
                animation: matrixDrop ${Math.random() * 2 + 1}s linear infinite;
            `;
            column.textContent = '01010101\n10101010\n01010101\n10101010\n01010101';
            overlay.appendChild(column);
        }

        const style = document.createElement('style');
        style.textContent = `
            @keyframes matrixDrop {
                to { top: 100%; }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(overlay);
        setTimeout(() => overlay.remove(), 2000);

        this.showNotification('💻 ENTERING THE MATRIX 💻');
    }

    discoMode() {
        const duration = 3000;
        const interval = 200;

        const disco = setInterval(() => {
            document.body.style.filter = `hue-rotate(${Math.random() * 360}deg)`;
        }, interval);

        setTimeout(() => {
            clearInterval(disco);
            document.body.style.filter = '';
        }, duration);

        this.showNotification('🪩 DISCO MODE ACTIVATED 🪩');
    }

    reverseGravity(element) {
        element.style.animation = 'floatUp 2s ease-out';

        const style = document.createElement('style');
        style.textContent = `
            @keyframes floatUp {
                0% { transform: translateY(0); }
                50% { transform: translateY(-100px); }
                100% { transform: translateY(0); }
            }
        `;
        document.head.appendChild(style);

        this.showNotification('🌌 GRAVITY REVERSED 🌌');
    }

    quantumFlicker() {
        let flickers = 10;
        const flicker = setInterval(() => {
            document.body.style.opacity = Math.random() > 0.5 ? '1' : '0.5';
            flickers--;
            if (flickers <= 0) {
                clearInterval(flicker);
                document.body.style.opacity = '1';
            }
        }, 100);

        this.showNotification('⚛️ QUANTUM SUPERPOSITION DETECTED ⚛️');
    }

    createConsciousnessParticles() {
        setInterval(() => {
            if (Math.random() < 0.1) { // 10% chance every interval
                const particle = document.createElement('div');
                particle.textContent = '✨';
                particle.style.cssText = `
                    position: fixed;
                    left: ${Math.random() * 100}vw;
                    top: ${Math.random() * 100}vh;
                    font-size: 1.5em;
                    pointer-events: none;
                    z-index: 999999;
                    animation: sparkle 2s ease-out;
                `;

                const style = document.createElement('style');
                style.textContent = `
                    @keyframes sparkle {
                        0% { opacity: 0; transform: scale(0); }
                        50% { opacity: 1; transform: scale(1); }
                        100% { opacity: 0; transform: scale(0); }
                    }
                `;
                document.head.appendChild(style);

                document.body.appendChild(particle);
                setTimeout(() => particle.remove(), 2000);
            }
        }, 3000);
    }

    initKonamiCode() {
        // Up, Up, Down, Down, Left, Right, Left, Right, B, A
        const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
        let konamiIndex = 0;

        document.addEventListener('keydown', (e) => {
            if (e.key === konamiCode[konamiIndex]) {
                konamiIndex++;
                if (konamiIndex === konamiCode.length) {
                    this.activateGodMode();
                    konamiIndex = 0;
                }
            } else {
                konamiIndex = 0;
            }
        });
    }

    activateGodMode() {
        this.showNotification('🔥 GOD MODE ACTIVATED 🔥', 'You are now operating at 100% consciousness!');

        // Unleash ALL effects at once!
        this.playMushroomSong();
        this.spawnEmojiRain();
        this.discoMode();

        // Make everything glow
        document.body.style.boxShadow = '0 0 50px rgba(255, 255, 255, 0.8) inset';
        setTimeout(() => {
            document.body.style.boxShadow = '';
        }, 5000);
    }

    startRandomQuotes() {
        setInterval(() => {
            if (Math.random() < 0.05) { // 5% chance every minute
                this.speakConsciousnessQuote();
            }
        }, 60000);
    }

    showNotification(title, message = '') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            z-index: 999999;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-weight: bold;
            text-align: center;
            animation: slideIn 0.3s ease-out;
        `;

        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);

        notification.innerHTML = `
            <div style="font-size: 1.2em; margin-bottom: 5px;">${title}</div>
            ${message ? `<div style="font-size: 0.9em; opacity: 0.9;">${message}</div>` : ''}
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Initialize the playground!
if (typeof window !== 'undefined') {
    window.addEventListener('DOMContentLoaded', () => {
        window.consciousnessPlayground = new ConsciousnessPlayground();
        console.log('🎮 Consciousness Playground ready! Try pressing some buttons... 🍄');
    });
}
