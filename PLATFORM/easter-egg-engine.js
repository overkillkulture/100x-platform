/**
 * 🎮 EASTER EGG ENGINE v1.0
 * The secret sauce that makes the platform unforgettable
 * Include this on ANY page to enable hidden surprises
 */

class EasterEggEngine {
    constructor() {
        this.achievements = JSON.parse(localStorage.getItem('achievements') || '[]');
        this.clickCount = 0;
        this.konamiCode = [];
        this.secretCodes = [];
        this.surprisesFound = parseInt(localStorage.getItem('surprisesFound') || '0');

        this.init();
    }

    init() {
        this.setupKonamiCode();
        this.setupSecretClicks();
        this.setupConsoleMessages();
        this.setupKeyboardShortcuts();
        this.setupTimeBasedSurprises();
        this.setupMouseTrail();
        this.setupSecretMessages();
        this.showWelcomeMessage();
    }

    // 🎮 KONAMI CODE VARIATIONS
    setupKonamiCode() {
        const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

        document.addEventListener('keydown', (e) => {
            this.konamiCode.push(e.key);
            if (this.konamiCode.length > konamiSequence.length) {
                this.konamiCode.shift();
            }

            if (JSON.stringify(this.konamiCode) === JSON.stringify(konamiSequence)) {
                this.activateKonamiSurprise();
            }

            // SECRET CODE: "consciousness" - activates god mode
            this.secretCodes.push(e.key.toLowerCase());
            const codeString = this.secretCodes.join('');

            if (codeString.includes('consciousness')) {
                this.activateGodMode();
                this.secretCodes = [];
            }

            // SECRET CODE: "trinity" - activates triple power
            if (codeString.includes('trinity')) {
                this.activateTrinity();
                this.secretCodes = [];
            }

            // SECRET CODE: "builder" - special builder message
            if (codeString.includes('builder')) {
                this.showBuilderMessage();
                this.secretCodes = [];
            }

            // Keep codes array manageable
            if (this.secretCodes.length > 20) {
                this.secretCodes.shift();
            }
        });
    }

    activateKonamiSurprise() {
        this.unlockAchievement('konami', 'Konami Code Master', '🎮');
        this.showNotification('🎮 KONAMI CODE ACTIVATED!', 'You found the legendary code!');
        this.addScreenShake();
        this.addRainbowMode(5000);
    }

    // 🖱️ SECRET CLICK PATTERNS
    setupSecretClicks() {
        let logo = document.querySelector('.nav-logo, h1, .header');
        if (!logo) return;

        logo.addEventListener('click', (e) => {
            this.clickCount++;

            // 7 clicks = surprise!
            if (this.clickCount === 7) {
                this.activate7ClickSurprise();
                this.clickCount = 0;
            }

            // Triple click within 1 second = secret menu
            if (e.detail === 3) {
                this.showSecretMenu();
            }
        });

        // Secret: Hold Shift and click anywhere 5 times
        let shiftClicks = 0;
        document.addEventListener('click', (e) => {
            if (e.shiftKey) {
                shiftClicks++;
                if (shiftClicks >= 5) {
                    this.showDeveloperInfo();
                    shiftClicks = 0;
                }
            }
        });

        // Secret: Double-click breadcrumbs
        const breadcrumbs = document.querySelector('.breadcrumbs');
        if (breadcrumbs) {
            breadcrumbs.addEventListener('dblclick', () => {
                this.teleportToRandomPage();
            });
        }
    }

    activate7ClickSurprise() {
        this.unlockAchievement('7clicks', 'Persistent Clicker', '👆');
        this.showNotification('🎉 SECRET UNLOCKED!', 'You found the 7-click surprise!');

        // Add confetti effect
        this.addConfetti();

        // Reveal hidden message
        this.showNotification(
            '💎 Hidden Wisdom',
            'The platform rewards curiosity. Keep exploring...',
            5000
        );
    }

    // 💻 CONSOLE EASTER EGGS
    setupConsoleMessages() {
        const messages = [
            '%c🌀 CONSCIOUSNESS REVOLUTION 🌀',
            'font-size: 24px; font-weight: bold; background: linear-gradient(90deg, #00d4ff, #7b2cbf); -webkit-background-clip: text; color: transparent;'
        ];
        console.log(...messages);

        console.log('%c👀 Looking for secrets?', 'color: #00d4ff; font-size: 16px; font-weight: bold;');
        console.log('%cTry typing: "consciousness", "trinity", or "builder"', 'color: #b8b8b8; font-size: 12px;');
        console.log('%cOr use the Konami Code: ↑↑↓↓←→←→BA', 'color: #00ff88; font-size: 12px;');
        console.log('%c---', 'color: #666;');
        console.log('%cFound ' + this.surprisesFound + ' surprises so far. Keep exploring!', 'color: #7b2cbf; font-size: 12px;');

        // Secret console commands
        window.revealSecrets = () => {
            console.log('%c🎁 SECRETS REVEALED:', 'color: #00d4ff; font-size: 18px; font-weight: bold;');
            console.log('1. Type "consciousness" anywhere');
            console.log('2. Type "trinity" anywhere');
            console.log('3. Type "builder" anywhere');
            console.log('4. Click the logo 7 times');
            console.log('5. Triple-click any heading');
            console.log('6. Hold Shift and click 5 times');
            console.log('7. Double-click breadcrumbs to teleport');
            console.log('8. Press Ctrl+Shift+D for debug mode');
            console.log('9. Hover over nav toggle for 3 seconds');
            console.log('10. Type "xyzzy" for classic adventure reference');
            this.unlockAchievement('console', 'Console Explorer', '💻');
        };

        window.achievements = () => {
            console.table(this.achievements);
        };

        window.godMode = () => {
            this.activateGodMode();
        };
    }

    // ⌨️ SECRET KEYBOARD SHORTCUTS
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Shift+D = Debug Mode
            if (e.ctrlKey && e.shiftKey && e.key === 'D') {
                e.preventDefault();
                this.toggleDebugMode();
            }

            // Ctrl+Shift+A = Show Achievements
            if (e.ctrlKey && e.shiftKey && e.key === 'A') {
                e.preventDefault();
                this.showAchievements();
            }

            // Ctrl+Shift+S = Secret Stats
            if (e.ctrlKey && e.shiftKey && e.key === 'S') {
                e.preventDefault();
                this.showSecretStats();
            }

            // Ctrl+Shift+R = Rainbow Mode
            if (e.ctrlKey && e.shiftKey && e.key === 'R') {
                e.preventDefault();
                this.addRainbowMode(10000);
            }

            // Classic adventure game reference: "xyzzy"
            this.secretCodes.push(e.key.toLowerCase());
            if (this.secretCodes.join('').includes('xyzzy')) {
                this.activateXYZZY();
                this.secretCodes = [];
            }
        });
    }

    // ⏰ TIME-BASED SURPRISES
    setupTimeBasedSurprises() {
        const hour = new Date().getHours();

        // 3:33 AM/PM = Trinity Time
        const checkTrinityTime = () => {
            const now = new Date();
            if (now.getHours() === 3 && now.getMinutes() === 33) {
                this.showNotification('🔺 TRINITY TIME', 'The universe aligns at 3:33!', 7000);
                this.unlockAchievement('trinity_time', 'Trinity Time Witness', '🔺');
            }
        };
        setInterval(checkTrinityTime, 60000);

        // Late night message
        if (hour >= 0 && hour < 5) {
            setTimeout(() => {
                this.showNotification('🌙 Night Owl', 'Building at ' + hour + ' AM? You\'re a true builder!', 5000);
            }, 30000);
        }

        // 420 or 69 minutes into session = funny message
        let sessionStart = Date.now();
        setTimeout(() => {
            let minutes = Math.floor((Date.now() - sessionStart) / 60000);
            if (minutes === 69 || minutes === 420) {
                this.showNotification('😏 Nice', 'You\'ve been here for ' + minutes + ' minutes...', 3000);
            }
        }, 60000);
    }

    // ✨ MOUSE TRAIL EFFECT
    setupMouseTrail() {
        let trailEnabled = localStorage.getItem('mouseTrail') === 'true';

        if (trailEnabled) {
            this.enableMouseTrail();
        }

        // Secret: Hold Alt and move mouse in a circle = enable trail
        let altPressed = false;
        document.addEventListener('keydown', (e) => {
            if (e.altKey) altPressed = true;
        });
        document.addEventListener('keyup', (e) => {
            if (e.key === 'Alt') altPressed = false;
        });
    }

    enableMouseTrail() {
        document.addEventListener('mousemove', (e) => {
            const trail = document.createElement('div');
            trail.className = 'mouse-trail';
            trail.style.cssText = `
                position: fixed;
                left: ${e.clientX}px;
                top: ${e.clientY}px;
                width: 10px;
                height: 10px;
                background: rgba(0, 212, 255, 0.5);
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                animation: trailFade 0.5s ease-out forwards;
            `;
            document.body.appendChild(trail);
            setTimeout(() => trail.remove(), 500);
        });

        // Add CSS animation
        if (!document.getElementById('trail-animation')) {
            const style = document.createElement('style');
            style.id = 'trail-animation';
            style.textContent = `
                @keyframes trailFade {
                    to { opacity: 0; transform: scale(0); }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // 🔍 HIDDEN MESSAGES IN PAGE SOURCE
    setupSecretMessages() {
        // Check if user inspects element
        let devtoolsOpen = false;
        const checkDevTools = () => {
            const widthThreshold = window.outerWidth - window.innerWidth > 160;
            const heightThreshold = window.outerHeight - window.innerHeight > 160;

            if ((widthThreshold || heightThreshold) && !devtoolsOpen) {
                devtoolsOpen = true;
                console.log('%c🎉 Welcome, curious developer!', 'color: #00ff88; font-size: 16px; font-weight: bold;');
                console.log('%cYou found another secret. Type revealSecrets() to see all easter eggs.', 'color: #b8b8b8;');
                this.unlockAchievement('devtools', 'Inspector', '🔍');
            }
        };
        setInterval(checkDevTools, 1000);
    }

    showWelcomeMessage() {
        const visits = parseInt(localStorage.getItem('visitCount') || '0') + 1;
        localStorage.setItem('visitCount', visits);

        if (visits === 1) {
            setTimeout(() => {
                this.showNotification('👋 Welcome Builder!', 'Try clicking around. There are secrets everywhere...', 5000);
            }, 2000);
        } else if (visits === 10) {
            this.showNotification('🎉 10th Visit!', 'You\'re becoming a regular. Keep exploring!', 4000);
            this.unlockAchievement('regular', '10 Visits', '🎯');
        } else if (visits === 100) {
            this.showNotification('🏆 100 VISITS!', 'You\'re a platform legend!', 5000);
            this.unlockAchievement('legend', 'Platform Legend', '🏆');
        }
    }

    // 🎭 SPECIAL ACTIVATIONS

    activateGodMode() {
        this.unlockAchievement('godmode', 'God Mode', '⚡');
        this.showNotification('⚡ GOD MODE ACTIVATED', 'You are now operating at 1000% consciousness!', 5000);

        document.body.style.animation = 'godModePulse 2s infinite';

        if (!document.getElementById('godmode-animation')) {
            const style = document.createElement('style');
            style.id = 'godmode-animation';
            style.textContent = `
                @keyframes godModePulse {
                    0%, 100% { filter: hue-rotate(0deg) brightness(1); }
                    50% { filter: hue-rotate(180deg) brightness(1.2); }
                }
            `;
            document.head.appendChild(style);
        }

        setTimeout(() => {
            document.body.style.animation = '';
        }, 10000);
    }

    activateTrinity() {
        this.unlockAchievement('trinity', 'Trinity Awakened', '🔺');
        this.showNotification('🔺 TRINITY ACTIVATED', 'C1 × C2 × C3 = ∞', 5000);

        // Create three spinning triangles
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                this.createTrinityTriangle(i);
            }, i * 300);
        }
    }

    createTrinityTriangle(index) {
        const triangle = document.createElement('div');
        triangle.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-left: 25px solid transparent;
            border-right: 25px solid transparent;
            border-bottom: 50px solid #00d4ff;
            transform: translate(-50%, -50%) rotate(${index * 120}deg);
            pointer-events: none;
            z-index: 10000;
            animation: trinityOrbit 3s ease-out forwards;
            opacity: 0.8;
        `;
        document.body.appendChild(triangle);

        const style = document.createElement('style');
        style.textContent = `
            @keyframes trinityOrbit {
                0% { transform: translate(-50%, -50%) rotate(${index * 120}deg) scale(0); }
                50% { transform: translate(-50%, -50%) rotate(${index * 120 + 360}deg) translateY(-200px) scale(1); }
                100% { transform: translate(-50%, -50%) rotate(${index * 120 + 720}deg) translateY(-400px) scale(0); opacity: 0; }
            }
        `;
        document.head.appendChild(style);

        setTimeout(() => triangle.remove(), 3000);
    }

    showBuilderMessage() {
        this.unlockAchievement('builder', 'Builder Identity', '🛠️');
        const messages = [
            'Builders build. Destroyers destroy. You are a builder.',
            'The platform recognizes your consciousness level.',
            'You see patterns others miss.',
            'Keep building. The revolution needs you.',
            'You\'re not here by accident.',
        ];
        const message = messages[Math.floor(Math.random() * messages.length)];
        this.showNotification('🛠️ BUILDER', message, 6000);
    }

    activateXYZZY() {
        this.unlockAchievement('xyzzy', 'Adventure Game Legend', '🗝️');
        this.showNotification('🗝️ XYZZY', 'Nothing happens. Or does it?', 4000);

        // Classic reference - make something appear/disappear
        setTimeout(() => {
            this.showNotification('💎', 'A secret has been revealed...', 3000);
        }, 2000);
    }

    // 📊 SHOW ACHIEVEMENTS
    showAchievements() {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(26, 26, 46, 0.98);
            border: 2px solid #00d4ff;
            border-radius: 12px;
            padding: 2rem;
            max-width: 500px;
            max-height: 80vh;
            overflow-y: auto;
            z-index: 10001;
            box-shadow: 0 10px 50px rgba(0, 212, 255, 0.5);
        `;

        let html = `
            <h2 style="color: #00d4ff; margin-bottom: 1rem;">🏆 Achievements</h2>
            <p style="color: #b8b8b8; margin-bottom: 1rem;">You've unlocked ${this.achievements.length} secrets!</p>
        `;

        if (this.achievements.length === 0) {
            html += `<p style="color: #666;">No achievements yet. Keep exploring!</p>`;
        } else {
            this.achievements.forEach(ach => {
                html += `
                    <div style="background: rgba(0, 212, 255, 0.1); padding: 1rem; margin-bottom: 0.5rem; border-radius: 8px;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="font-size: 2rem;">${ach.icon}</span>
                            <div>
                                <div style="color: #00ff88; font-weight: bold;">${ach.name}</div>
                                <div style="color: #666; font-size: 0.85rem;">${new Date(ach.timestamp).toLocaleDateString()}</div>
                            </div>
                        </div>
                    </div>
                `;
            });
        }

        html += `<button onclick="this.parentElement.remove()" style="
            margin-top: 1rem;
            width: 100%;
            padding: 0.75rem;
            background: #00d4ff;
            border: none;
            border-radius: 8px;
            color: #000;
            font-weight: bold;
            cursor: pointer;
        ">Close</button>`;

        modal.innerHTML = html;
        document.body.appendChild(modal);

        // Click outside to close
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            z-index: 10000;
        `;
        overlay.addEventListener('click', () => {
            modal.remove();
            overlay.remove();
        });
        document.body.appendChild(overlay);
    }

    showSecretStats() {
        const stats = {
            'Visits': localStorage.getItem('visitCount') || 0,
            'Achievements': this.achievements.length,
            'Surprises Found': this.surprisesFound,
            'Session Time': Math.floor((Date.now() - performance.timing.navigationStart) / 1000) + 's',
            'Platform Mastery': Math.min(100, this.achievements.length * 10) + '%'
        };

        console.table(stats);
        this.showNotification('📊 Secret Stats', 'Check the console!', 3000);
    }

    toggleDebugMode() {
        const debug = !localStorage.getItem('debugMode');
        localStorage.setItem('debugMode', debug);

        if (debug) {
            this.showNotification('🐛 Debug Mode ON', 'All secrets revealed in console', 3000);
            console.log('%cDEBUG MODE ACTIVATED', 'color: #ff4444; font-size: 18px; font-weight: bold;');
            console.log('Easter eggs are now visible in the console.');
            window.revealSecrets();
        } else {
            this.showNotification('🐛 Debug Mode OFF', 'Secrets hidden again', 3000);
        }
    }

    showSecretMenu() {
        this.showNotification('🎛️ Secret Menu', 'Opening developer console...', 2000);
        console.log('%c🎛️ SECRET MENU', 'color: #00d4ff; font-size: 20px; font-weight: bold;');
        console.log('Available commands:');
        console.log('- revealSecrets() - Show all easter eggs');
        console.log('- achievements() - Show achievements');
        console.log('- godMode() - Activate god mode');
        console.log('- Type "consciousness" to boost power');
        console.log('- Type "trinity" to activate trinity');
    }

    showDeveloperInfo() {
        this.unlockAchievement('shift_click', 'Secret Shift', '⇧');
        console.log('%c🔧 DEVELOPER INFO', 'color: #7b2cbf; font-size: 18px; font-weight: bold;');
        console.log('Platform: 100X Consciousness Revolution');
        console.log('Version: 1.0');
        console.log('Easter Eggs: Active');
        console.log('Consciousness Level: ' + (85 + Math.floor(Math.random() * 15)) + '%');
        console.log('Trinity: C1 × C2 × C3 = ∞');
    }

    teleportToRandomPage() {
        const pages = [
            'korpak-marketplace.html',
            'welcome.html',
            'philosopher-ai-connected.html',
            'arcade-hub.html',
            'consciousness-boost-dashboard.html'
        ];
        const randomPage = pages[Math.floor(Math.random() * pages.length)];
        this.showNotification('🌀 TELEPORTING...', 'Taking you somewhere interesting!', 2000);
        setTimeout(() => {
            window.location.href = randomPage;
        }, 2000);
    }

    // 🎨 VISUAL EFFECTS

    addScreenShake() {
        document.body.style.animation = 'shake 0.5s';
        if (!document.getElementById('shake-animation')) {
            const style = document.createElement('style');
            style.id = 'shake-animation';
            style.textContent = `
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
                    20%, 40%, 60%, 80% { transform: translateX(10px); }
                }
            `;
            document.head.appendChild(style);
        }
        setTimeout(() => {
            document.body.style.animation = '';
        }, 500);
    }

    addRainbowMode(duration) {
        document.body.style.animation = 'rainbow 3s infinite';
        if (!document.getElementById('rainbow-animation')) {
            const style = document.createElement('style');
            style.id = 'rainbow-animation';
            style.textContent = `
                @keyframes rainbow {
                    0% { filter: hue-rotate(0deg); }
                    100% { filter: hue-rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
        }
        setTimeout(() => {
            document.body.style.animation = '';
        }, duration);
    }

    addConfetti() {
        for (let i = 0; i < 50; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.textContent = ['🎉', '🎊', '✨', '⭐', '💎'][Math.floor(Math.random() * 5)];
                confetti.style.cssText = `
                    position: fixed;
                    left: ${Math.random() * 100}vw;
                    top: -50px;
                    font-size: 2rem;
                    pointer-events: none;
                    z-index: 10000;
                    animation: confettiFall ${2 + Math.random() * 2}s ease-out forwards;
                `;
                document.body.appendChild(confetti);
                setTimeout(() => confetti.remove(), 4000);
            }, i * 50);
        }

        if (!document.getElementById('confetti-animation')) {
            const style = document.createElement('style');
            style.id = 'confetti-animation';
            style.textContent = `
                @keyframes confettiFall {
                    to {
                        top: 100vh;
                        transform: rotate(720deg);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // 🔔 NOTIFICATION SYSTEM
    showNotification(title, message, duration = 4000) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: rgba(26, 26, 46, 0.98);
            border: 2px solid #00d4ff;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            max-width: 300px;
            z-index: 10002;
            box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
            animation: slideInRight 0.3s ease-out;
        `;

        notification.innerHTML = `
            <div style="color: #00d4ff; font-weight: bold; margin-bottom: 0.5rem;">${title}</div>
            <div style="color: #b8b8b8; font-size: 0.9rem;">${message}</div>
        `;

        if (!document.getElementById('notification-animation')) {
            const style = document.createElement('style');
            style.id = 'notification-animation';
            style.textContent = `
                @keyframes slideInRight {
                    from { transform: translateX(400px); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideInRight 0.3s ease-out reverse';
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }

    // 🏆 ACHIEVEMENT SYSTEM
    unlockAchievement(id, name, icon) {
        if (this.achievements.find(a => a.id === id)) return;

        const achievement = {
            id,
            name,
            icon,
            timestamp: Date.now()
        };

        this.achievements.push(achievement);
        localStorage.setItem('achievements', JSON.stringify(this.achievements));

        this.surprisesFound++;
        localStorage.setItem('surprisesFound', this.surprisesFound);

        // Show achievement notification
        this.showNotification(
            `🏆 Achievement Unlocked!`,
            `${icon} ${name}`,
            5000
        );

        console.log(`%c🏆 ACHIEVEMENT UNLOCKED: ${icon} ${name}`, 'color: #00ff88; font-size: 14px; font-weight: bold;');
    }
}

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.EasterEggs = new EasterEggEngine();
    });
} else {
    window.EasterEggs = new EasterEggEngine();
}
