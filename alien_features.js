// 🛸 ALIEN GRADE FEATURES 🛸
// Matrix Rain, Hyperdrive, Kaleidoscope, Glitch Mode, Ejection Seat

let hyperdriveActive = false;
let kaleidoscopeActive = false;
let glitchActive = false;
let matrixActive = false;
let matrixCanvas, matrixCtx;
let matrixColumns = [];

// Matrix Rain Setup
function initMatrix() {
    matrixCanvas = document.getElementById('matrixCanvas');
    if (!matrixCanvas) return;

    matrixCanvas.width = window.innerWidth;
    matrixCanvas.height = window.innerHeight;
    matrixCtx = matrixCanvas.getContext('2d');

    const cols = Math.floor(matrixCanvas.width / 20);
    for (let i = 0; i < cols; i++) {
        matrixColumns[i] = 1;
    }
}

function drawMatrix() {
    if (!matrixActive || !matrixCtx) return;

    matrixCtx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    matrixCtx.fillRect(0, 0, matrixCanvas.width, matrixCanvas.height);

    matrixCtx.fillStyle = '#0F0';
    matrixCtx.font = '15px monospace';

    for (let i = 0; i < matrixColumns.length; i++) {
        const text = String.fromCharCode(0x30A0 + Math.random() * 96);
        const x = i * 20;
        const y = matrixColumns[i] * 20;

        matrixCtx.fillText(text, x, y);

        if (y > matrixCanvas.height && Math.random() > 0.975) {
            matrixColumns[i] = 0;
        }
        matrixColumns[i]++;
    }

    requestAnimationFrame(drawMatrix);
}

// Initialize alien features
window.addEventListener('load', function() {
    initMatrix();

    // Hyperdrive Button
    document.getElementById('hyperdriveBtn').addEventListener('click', function() {
        hyperdriveActive = !hyperdriveActive;
        const container = document.getElementById('stonehenge');

        if (hyperdriveActive) {
            this.textContent = '🛸 DISENGAGE HYPERDRIVE 🛸';
            this.style.background = 'linear-gradient(135deg, #00ff41, #00ffff)';
            container.style.perspective = '800px';
            container.style.animation = 'hyperdrive-zoom 2s ease-in-out infinite';

            const style = document.createElement('style');
            style.id = 'hyperdrive-style';
            style.textContent = `
                @keyframes hyperdrive-zoom {
                    0%, 100% { transform: scale(1) translateZ(0); }
                    50% { transform: scale(1.5) translateZ(500px); }
                }
            `;
            document.head.appendChild(style);
        } else {
            this.textContent = '🛸 ENGAGE HYPERDRIVE 🛸';
            this.style.background = 'linear-gradient(135deg, #ff0080, #ff00ff)';
            container.style.perspective = 'none';
            container.style.animation = '';
            const style = document.getElementById('hyperdrive-style');
            if (style) style.remove();
        }
    });

    // Kaleidoscope Button
    document.getElementById('kaleidoscopeBtn').addEventListener('click', function() {
        kaleidoscopeActive = !kaleidoscopeActive;
        const container = document.getElementById('stonehenge');

        if (kaleidoscopeActive) {
            this.textContent = '🌈 DISABLE KALEIDOSCOPE 🌈';
            this.style.background = 'linear-gradient(135deg, #ff0080, #ffd700)';

            const mirrors = document.createElement('div');
            mirrors.id = 'kaleidoscope-mirrors';
            mirrors.style.cssText = `
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background:
                    linear-gradient(45deg, rgba(255,0,128,0.1) 25%, transparent 25%),
                    linear-gradient(-45deg, rgba(0,255,65,0.1) 25%, transparent 25%),
                    linear-gradient(135deg, rgba(255,215,0,0.1) 25%, transparent 25%);
                background-size: 200px 200px;
                pointer-events: none;
                mix-blend-mode: color-dodge;
                animation: kaleidoscope-spin 10s linear infinite;
            `;

            const style = document.createElement('style');
            style.id = 'kaleidoscope-style';
            style.textContent = `
                @keyframes kaleidoscope-spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
            container.appendChild(mirrors);
            container.style.filter = 'saturate(2) contrast(1.2)';
        } else {
            this.textContent = '🌈 KALEIDOSCOPE MODE 🌈';
            this.style.background = 'linear-gradient(135deg, #00ff41, #00ffff)';
            const mirrors = document.getElementById('kaleidoscope-mirrors');
            if (mirrors) mirrors.remove();
            const style = document.getElementById('kaleidoscope-style');
            if (style) style.remove();
            container.style.filter = '';
        }
    });

    // Glitch Button
    document.getElementById('glitchBtn').addEventListener('click', function() {
        glitchActive = !glitchActive;
        const visualization = document.getElementById('stonehenge');

        if (glitchActive) {
            this.textContent = '⚡ STOP GLITCHING ⚡';
            this.style.background = 'linear-gradient(135deg, #ff0080, #00ff41)';

            window.glitchInterval = setInterval(() => {
                visualization.style.transform = `translate(${Math.random() * 10 - 5}px, ${Math.random() * 10 - 5}px)`;
                visualization.style.filter = `hue-rotate(${Math.random() * 360}deg)`;

                setTimeout(() => {
                    visualization.style.transform = '';
                    visualization.style.filter = '';
                }, 100);
            }, 500);
        } else {
            this.textContent = '⚡ REALITY GLITCH ⚡';
            this.style.background = 'linear-gradient(135deg, #ffd700, #ff6600)';
            if (window.glitchInterval) {
                clearInterval(window.glitchInterval);
                visualization.style.transform = '';
                visualization.style.filter = '';
            }
        }
    });

    // Matrix Button
    document.getElementById('matrixBtn').addEventListener('click', function() {
        matrixActive = !matrixActive;
        const matrixCanvas = document.getElementById('matrixCanvas');

        if (matrixActive) {
            this.textContent = '🔮 STOP MATRIX 🔮';
            this.style.background = 'linear-gradient(135deg, #ff0080, #cc0066)';
            matrixCanvas.style.display = 'block';
            drawMatrix();
        } else {
            this.textContent = '🔮 MATRIX RAIN 🔮';
            this.style.background = 'linear-gradient(135deg, #00ff41, #00cc33)';
            matrixCanvas.style.display = 'none';
        }
    });

    // EJECTION SEAT - Resets everything!
    document.getElementById('ejectBtn').addEventListener('click', function() {
        const ejectSound = new AudioContext();
        const oscillator = ejectSound.createOscillator();
        const gain = ejectSound.createGain();

        oscillator.connect(gain);
        gain.connect(ejectSound.destination);

        oscillator.frequency.setValueAtTime(800, ejectSound.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(200, ejectSound.currentTime + 0.5);
        gain.gain.setValueAtTime(0.3, ejectSound.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ejectSound.currentTime + 0.5);

        oscillator.start();
        oscillator.stop(ejectSound.currentTime + 0.5);

        alert('🚨 EJECTING! 🚨\n\nResetting all systems to normal...');

        if (hyperdriveActive) document.getElementById('hyperdriveBtn').click();
        if (kaleidoscopeActive) document.getElementById('kaleidoscopeBtn').click();
        if (glitchActive) document.getElementById('glitchBtn').click();
        if (matrixActive) document.getElementById('matrixBtn').click();

        document.getElementById('goldenSlider').value = 1.618;
        document.getElementById('fibSlider').value = 7;
        document.getElementById('stoneSlider').value = 12;
        document.getElementById('freqSlider').value = 528;
        document.getElementById('quantumSlider').value = 93;
        document.getElementById('rotationSlider').value = 1;
        document.getElementById('consciousnessSlider').value = 93;

        document.getElementById('goldenSlider').dispatchEvent(new Event('input'));
        document.getElementById('fibSlider').dispatchEvent(new Event('input'));
        document.getElementById('stoneSlider').dispatchEvent(new Event('input'));
        document.getElementById('freqSlider').dispatchEvent(new Event('input'));
        document.getElementById('quantumSlider').dispatchEvent(new Event('input'));
        document.getElementById('rotationSlider').dispatchEvent(new Event('input'));
        document.getElementById('consciousnessSlider').dispatchEvent(new Event('input'));

        if (window.isPlaying) {
            document.getElementById('playButton').click();
        }

        console.log('🚨 EJECTION COMPLETE - All systems normal! 🚨');
    });
});

console.log('%c🛸 ALIEN GRADE FEATURES LOADED! 🛸', 'color: #ff0080; font-size: 20px; font-weight: bold;');
console.log('%c🛸 HYPERDRIVE - Warp speed zoom animation', 'color: #ff0080; font-size: 12px;');
console.log('%c🌈 KALEIDOSCOPE - Mirror reality 6 ways', 'color: #00ff41; font-size: 12px;');
console.log('%c⚡ GLITCH - Reality tears and repairs', 'color: #ffd700; font-size: 12px;');
console.log('%c🔮 MATRIX - Digital rain background', 'color: #00ff41; font-size: 12px;');
console.log('%c🚨 EJECTION SEAT - Emergency reset!', 'color: #ff0000; font-size: 12px;');
