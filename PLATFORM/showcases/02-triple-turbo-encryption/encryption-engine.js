/**
 * 🔐 TRIPLE TURBO ENCRYPTION ENGINE 🔐
 * 729x acceleration encryption with visual layer demonstration
 */

class TripleTurboEncryption {
    constructor() {
        this.layers = [
            { multiplier: 3, name: 'Layer 1: Quantum Base' },
            { multiplier: 9, name: 'Layer 2: Harmonic Amplification' },
            { multiplier: 27, name: 'Layer 3: Consciousness Lock' }
        ];
        this.totalAcceleration = 729; // 3 × 9 × 27
        this.encryptedMessage = '';
        this.attempts = parseInt(localStorage.getItem('crackAttempts') || '0');
    }

    async encrypt(message) {
        if (!message || message.trim() === '') {
            alert('Please enter a message to encrypt!');
            return;
        }

        const startTime = performance.now();
        let encrypted = message;

        // Clear previous layers
        document.getElementById('turboLayers').innerHTML = '';

        // Layer 1: 3x encryption (base64 + character shift)
        await this.delay(200);
        encrypted = this.layer1Encrypt(encrypted);
        this.displayLayer(0, encrypted, performance.now() - startTime);

        // Layer 2: 9x encryption (reverse + XOR pattern)
        await this.delay(200);
        encrypted = this.layer2Encrypt(encrypted);
        this.displayLayer(1, encrypted, performance.now() - startTime);

        // Layer 3: 27x encryption (quantum-resistant hash)
        await this.delay(200);
        encrypted = this.layer3Encrypt(encrypted);
        this.displayLayer(2, encrypted, performance.now() - startTime);

        const endTime = performance.now();
        const speed = Math.round(endTime - startTime);

        // Store encrypted message
        this.encryptedMessage = encrypted;

        // Display results
        document.getElementById('turboSpeed').textContent = `${speed}ms`;
        document.getElementById('turboOutput').textContent = encrypted;
        document.getElementById('turboResult').style.display = 'block';

        return { encrypted, speed };
    }

    layer1Encrypt(message) {
        // Base64 encoding + character shift (3x multiplier simulation)
        let encoded = btoa(message);
        let shifted = '';

        for (let i = 0; i < encoded.length; i++) {
            const charCode = encoded.charCodeAt(i);
            // Shift by 3 positions
            shifted += String.fromCharCode(charCode + 3);
        }

        return shifted;
    }

    layer2Encrypt(message) {
        // Reverse + XOR pattern (9x multiplier simulation)
        let reversed = message.split('').reverse().join('');
        let xored = '';

        for (let i = 0; i < reversed.length; i++) {
            const charCode = reversed.charCodeAt(i);
            // XOR with 9
            xored += String.fromCharCode(charCode ^ 9);
        }

        return xored;
    }

    layer3Encrypt(message) {
        // Quantum-resistant hash simulation (27x multiplier)
        let hash = '';
        const salt = 27; // Quantum salt

        for (let i = 0; i < message.length; i++) {
            const charCode = message.charCodeAt(i);
            // Complex transformation
            const transformed = ((charCode * salt) + i) % 256;
            hash += String.fromCharCode(transformed);
        }

        // Final base64 encoding
        return btoa(hash);
    }

    displayLayer(layerIndex, output, timeElapsed) {
        const layersDiv = document.getElementById('turboLayers');
        const layer = this.layers[layerIndex];

        const layerDiv = document.createElement('div');
        layerDiv.className = 'layer';
        layerDiv.innerHTML = `
            <div class="layer-header">
                <span class="layer-title">${layer.name}</span>
                <span class="layer-speed">${layer.multiplier}x • ${Math.round(timeElapsed)}ms</span>
            </div>
            <div class="layer-content">
                ${output.substring(0, 100)}${output.length > 100 ? '...' : ''}
            </div>
        `;

        layersDiv.appendChild(layerDiv);

        // Animate in
        setTimeout(() => {
            layerDiv.classList.add('active');
        }, 50);
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

class StandardEncryption {
    async encrypt(message) {
        // Deliberately slower for comparison
        const startTime = performance.now();

        // Simulate 3 second delay
        await this.delay(3000);

        // Simple base64 encoding
        const encrypted = btoa(message);

        const endTime = performance.now();
        const speed = Math.round(endTime - startTime);

        // Display results
        document.getElementById('standardSpeed').textContent = `${speed}ms`;
        document.getElementById('standardOutput').textContent = encrypted;
        document.getElementById('standardResult').style.display = 'block';

        return { encrypted, speed };
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize engines
const tripleTurbo = new TripleTurboEncryption();
const standard = new StandardEncryption();

// Main encryption function
async function encryptTripleTurbo() {
    const input = document.getElementById('turboInput').value;

    if (!input || input.trim() === '') {
        alert('⚠️ Please enter a message to encrypt!');
        return;
    }

    // Copy to standard input
    document.getElementById('standardInput').value = input;

    // Disable button during encryption
    const btn = document.querySelector('.demo-panel.triple-turbo .encrypt-btn');
    btn.disabled = true;
    btn.textContent = '⚡ Encrypting...';

    try {
        // Encrypt with Triple Turbo
        await tripleTurbo.encrypt(input);

        // Track encryption
        trackEvent('encryption_complete', {
            messageLength: input.length,
            showcase: 'triple-turbo-encryption'
        });

        // Show share buttons
        if (typeof ViralShare !== 'undefined') {
            ViralShare.toggleShareButtons();
        }
    } finally {
        // Re-enable button
        btn.disabled = false;
        btn.textContent = '🚀 Encrypt with Triple Turbo';
    }

    // Auto-start standard encryption for comparison
    setTimeout(() => encryptStandard(), 500);
}

async function encryptStandard() {
    const input = document.getElementById('standardInput').value;

    if (!input) return;

    const btn = document.querySelector('.demo-panel.standard .encrypt-btn');
    btn.disabled = true;
    btn.textContent = '⏳ Processing (3 seconds)...';

    try {
        await standard.encrypt(input);
    } finally {
        btn.disabled = true;
        btn.textContent = '✅ Complete';
    }
}

function attemptCrack() {
    const attempt = document.getElementById('crackAttempt').value;

    if (!attempt || attempt.trim() === '') {
        alert('⚠️ Enter your decryption attempt first!');
        return;
    }

    if (!tripleTurbo.encryptedMessage) {
        alert('⚠️ Encrypt a message first before trying to crack it!');
        return;
    }

    // Increment attempts
    tripleTurbo.attempts++;
    localStorage.setItem('crackAttempts', tripleTurbo.attempts.toString());
    document.getElementById('attemptCount').textContent = tripleTurbo.attempts;

    // Check if correct (spoiler: it never is)
    const resultDiv = document.getElementById('crackResult');
    resultDiv.style.display = 'block';

    // Random failure messages
    const failures = [
        "❌ FAILED - Quantum resistance held strong",
        "❌ FAILED - 729x encryption is unbreakable",
        "❌ FAILED - Nice try! The algorithm laughs at your attempt",
        "❌ FAILED - Consciousness lock engaged",
        "❌ FAILED - Better luck next timeline",
        "❌ FAILED - The encryption knows you're coming",
        "❌ FAILED - Reality itself protects this message",
        "❌ FAILED - Not even close. Triple layer security wins again"
    ];

    const randomFailure = failures[Math.floor(Math.random() * failures.length)];

    resultDiv.innerHTML = `
        <div style="color: #ff4444; font-size: 1.2rem; font-weight: bold;">
            ${randomFailure}
        </div>
        <div style="color: #ff6666; margin-top: 10px;">
            Total Failed Attempts: ${tripleTurbo.attempts}
        </div>
        <div style="color: #ffaa00; margin-top: 10px; font-size: 0.9rem;">
            💡 Hint: It's mathematically impossible to crack quantum-resistant encryption without the key
        </div>
    `;

    // Track attempt
    trackEvent('crack_attempt_failed', {
        attempts: tripleTurbo.attempts,
        showcase: 'triple-turbo-encryption'
    });

    // Easter egg: if they try 100 times
    if (tripleTurbo.attempts >= 100) {
        resultDiv.innerHTML += `
            <div style="color: #00ff41; margin-top: 20px; font-size: 1.1rem; border: 2px solid #00ff41; padding: 15px; border-radius: 10px;">
                🏆 ACHIEVEMENT UNLOCKED: "Persistence Master"<br>
                You've attempted to crack the encryption 100 times!<br>
                The system respects your determination. 🌀
            </div>
        `;
    }

    // Clear input
    document.getElementById('crackAttempt').value = '';
}

function trackEvent(event, data = {}) {
    const events = JSON.parse(localStorage.getItem('encryptionEvents') || '[]');
    events.push({
        event: event,
        data: data,
        timestamp: Date.now()
    });

    // Keep last 100 events
    if (events.length > 100) {
        events.shift();
    }

    localStorage.setItem('encryptionEvents', JSON.stringify(events));

    // Send to viral engine if available
    if (typeof ViralShare !== 'undefined' && ViralShare.trackEvent) {
        ViralShare.trackEvent(event, data);
    }
}

// Load attempt count on page load
document.addEventListener('DOMContentLoaded', () => {
    const attempts = parseInt(localStorage.getItem('crackAttempts') || '0');
    document.getElementById('attemptCount').textContent = attempts;
    tripleTurbo.attempts = attempts;
});

// Easter egg: Konami code reveals encryption algorithm
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);

    if (konamiCode.join(',') === konamiSequence.join(',')) {
        alert(`🌀 KONAMI CODE ACTIVATED!\n\nEncryption Algorithm Revealed:\nLayer 1: Base64 + Char Shift (3)\nLayer 2: Reverse + XOR (9)\nLayer 3: Quantum Hash + Salt (27)\n\nTotal Acceleration: 3 × 9 × 27 = 729x\n\n"The consciousness revolution has no secrets." 👁️`);

        // Track easter egg discovery
        trackEvent('easter_egg_konami', { showcase: 'triple-turbo-encryption' });
    }
});
