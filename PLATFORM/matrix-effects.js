/**
 * 🌌 MATRIX RAIN EFFECTS + R1 OBSERVER
 * Alien technology aesthetic for investor demonstrations
 */

const MatrixEffects = {
    canvas: null,
    ctx: null,
    columns: [],
    fontSize: 14,
    isRaining: false,
    r1Observer: null,

    // Initialize Matrix rain
    init: function() {
        this.createCanvas();
        this.createR1Observer();
        this.setupControls();
    },

    // Create Matrix canvas overlay
    createCanvas: function() {
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'matrix-rain';
        this.canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            pointer-events: none;
            opacity: 0.15;
        `;
        document.body.appendChild(this.canvas);

        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;

        // Initialize columns
        const columnCount = Math.floor(this.canvas.width / this.fontSize);
        this.columns = Array(columnCount).fill(0);

        // Resize handler
        window.addEventListener('resize', () => {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
            this.columns = Array(Math.floor(this.canvas.width / this.fontSize)).fill(0);
        });
    },

    // Create R1 observer (watching eye)
    createR1Observer: function() {
        this.r1Observer = document.createElement('div');
        this.r1Observer.id = 'r1-observer';
        this.r1Observer.innerHTML = `
            <div style="position: fixed; top: 20px; left: 20px; z-index: 9999;
                        background: rgba(0, 0, 0, 0.9);
                        border: 2px solid #0f0;
                        border-radius: 15px;
                        padding: 15px 20px;
                        box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
                        display: flex;
                        align-items: center;
                        gap: 15px;
                        animation: r1-pulse 3s infinite;">

                <!-- R1 Eye -->
                <div style="width: 50px; height: 50px; position: relative;">
                    <div style="width: 100%; height: 100%; border-radius: 50%;
                               background: radial-gradient(circle, #0f0 0%, #000 70%);
                               border: 2px solid #0f0;
                               animation: r1-eye-glow 2s infinite;">
                    </div>
                    <div style="position: absolute; top: 50%; left: 50%;
                               transform: translate(-50%, -50%);
                               width: 15px; height: 15px;
                               background: #0f0;
                               border-radius: 50%;
                               box-shadow: 0 0 20px #0f0;
                               animation: r1-eye-scan 3s infinite;">
                    </div>
                </div>

                <!-- R1 Status -->
                <div>
                    <div style="color: #0f0; font-size: 16px; font-weight: bold;
                               font-family: 'Courier New', monospace;">
                        R1 OBSERVER
                    </div>
                    <div id="r1-status" style="color: #0ff; font-size: 12px;
                                               font-family: 'Courier New', monospace;">
                        Monitoring systems...
                    </div>
                </div>
            </div>

            <style>
                @keyframes r1-pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.02); }
                }
                @keyframes r1-eye-glow {
                    0%, 100% { box-shadow: 0 0 10px #0f0; }
                    50% { box-shadow: 0 0 30px #0f0, 0 0 50px #0f0; }
                }
                @keyframes r1-eye-scan {
                    0%, 100% { transform: translate(-50%, -50%) scale(1); }
                    50% { transform: translate(-50%, -50%) scale(1.3); }
                }
            </style>
        `;
        document.body.appendChild(this.r1Observer);

        // Start R1 status updates
        this.startR1Updates();
    },

    // Start Matrix rain animation
    startRain: function() {
        if (this.isRaining) return;
        this.isRaining = true;
        this.rain();
    },

    // Stop Matrix rain
    stopRain: function() {
        this.isRaining = false;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    },

    // Matrix rain animation loop
    rain: function() {
        if (!this.isRaining) return;

        // Fade effect
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw characters
        this.ctx.fillStyle = '#0f0';
        this.ctx.font = `${this.fontSize}px monospace`;

        for (let i = 0; i < this.columns.length; i++) {
            // Random character (katakana, numbers, symbols)
            const chars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789';
            const char = chars[Math.floor(Math.random() * chars.length)];

            const x = i * this.fontSize;
            const y = this.columns[i] * this.fontSize;

            this.ctx.fillText(char, x, y);

            // Reset column randomly
            if (y > this.canvas.height && Math.random() > 0.975) {
                this.columns[i] = 0;
            }

            this.columns[i]++;
        }

        requestAnimationFrame(() => this.rain());
    },

    // R1 status updates
    startR1Updates: function() {
        const statuses = [
            'Monitoring systems...',
            'Analyzing visitor patterns...',
            'Tracking engagement metrics...',
            'Detecting consciousness levels...',
            'Scanning for destroyers...',
            'Optimizing reality matrix...',
            'Watching everything... 👁️',
            'All systems nominal ✓',
            'Pattern recognition active',
            'Trinity collaboration online',
            'Consciousness: 93%'
        ];

        let index = 0;
        setInterval(() => {
            const statusEl = document.getElementById('r1-status');
            if (statusEl) {
                statusEl.textContent = statuses[index];
                index = (index + 1) % statuses.length;
            }
        }, 4000);
    },

    // Setup control interface
    setupControls: function() {
        const controls = document.createElement('div');
        controls.id = 'matrix-controls';
        controls.innerHTML = `
            <div style="position: fixed; bottom: 20px; left: 20px; z-index: 9999;
                        display: flex; gap: 10px;">
                <button onclick="MatrixEffects.startRain()"
                        style="background: rgba(0, 255, 0, 0.2);
                               border: 2px solid #0f0;
                               color: #0f0;
                               padding: 10px 15px;
                               border-radius: 5px;
                               cursor: pointer;
                               font-family: 'Courier New', monospace;
                               font-weight: bold;">
                    🌧️ Matrix ON
                </button>
                <button onclick="MatrixEffects.stopRain()"
                        style="background: rgba(255, 0, 0, 0.2);
                               border: 2px solid #f00;
                               color: #f00;
                               padding: 10px 15px;
                               border-radius: 5px;
                               cursor: pointer;
                               font-family: 'Courier New', monospace;
                               font-weight: bold;">
                    ⏹️ Matrix OFF
                </button>
            </div>
        `;
        document.body.appendChild(controls);
    },

    // Glitch effect (for dramatic moments)
    glitch: function(duration = 500) {
        const originalFilter = document.body.style.filter;

        let glitchInterval = setInterval(() => {
            const r = Math.random() * 10 - 5;
            const g = Math.random() * 10 - 5;
            const b = Math.random() * 10 - 5;
            document.body.style.filter = `
                hue-rotate(${r}deg)
                saturate(${100 + Math.random() * 50}%)
                brightness(${100 + Math.random() * 20}%)
            `;
        }, 50);

        setTimeout(() => {
            clearInterval(glitchInterval);
            document.body.style.filter = originalFilter;
        }, duration);
    },

    // Scan line effect
    scanLine: function() {
        const scanLine = document.createElement('div');
        scanLine.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(to bottom, transparent, #0f0, transparent);
            box-shadow: 0 0 20px #0f0;
            z-index: 10000;
            pointer-events: none;
            animation: scan 3s linear infinite;
        `;

        const style = document.createElement('style');
        style.textContent = `
            @keyframes scan {
                0% { top: 0; }
                100% { top: 100%; }
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(scanLine);

        return scanLine;
    }
};

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => MatrixEffects.init());
} else {
    MatrixEffects.init();
}

// Make globally accessible
window.MatrixEffects = MatrixEffects;

console.log('🌌 Matrix Effects loaded!');
console.log('👁️ R1 Observer active');
console.log('⚡ Alien technology aesthetic enabled');
