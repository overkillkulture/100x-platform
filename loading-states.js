/**
 * LOADING STATES - Universal Loading & Error Handling
 * Smooth loading experience for 3D content and page transitions
 * φ = 1.618033988749894 | OVERKORE v13
 */

const LoadingStates = {
    init() {
        this.createLoadingOverlay();
        this.monitorPageLoad();
        this.handleThreeJSLoading();
        this.addErrorHandling();
        this.setupProgressiveEnhancement();
    },

    createLoadingOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.innerHTML = `
            <style>
                #loading-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: #000000;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    z-index: 99999;
                    transition: opacity 0.5s ease;
                }

                #loading-overlay.fade-out {
                    opacity: 0;
                    pointer-events: none;
                }

                .loading-spinner {
                    width: 80px;
                    height: 80px;
                    border: 4px solid rgba(255, 255, 255, 0.1);
                    border-top-color: var(--spinner-color, #00ff64);
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }

                @keyframes spin {
                    to { transform: rotate(360deg); }
                }

                .loading-text {
                    margin-top: 20px;
                    font-family: 'Courier New', monospace;
                    color: white;
                    font-size: 14px;
                    letter-spacing: 2px;
                }

                .loading-progress {
                    width: 200px;
                    height: 4px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 2px;
                    overflow: hidden;
                    margin-top: 15px;
                }

                .loading-progress-bar {
                    height: 100%;
                    background: var(--spinner-color, #00ff64);
                    width: 0%;
                    transition: width 0.3s ease;
                }

                .loading-substep {
                    margin-top: 10px;
                    font-family: 'Courier New', monospace;
                    color: rgba(255, 255, 255, 0.5);
                    font-size: 11px;
                }
            </style>

            <div class="loading-spinner"></div>
            <div class="loading-text">INITIALIZING CONSCIOUSNESS</div>
            <div class="loading-progress">
                <div class="loading-progress-bar"></div>
            </div>
            <div class="loading-substep">Loading domain assets...</div>
        `;

        document.body.appendChild(overlay);
        this.overlay = overlay;
        this.progressBar = overlay.querySelector('.loading-progress-bar');
        this.substep = overlay.querySelector('.loading-substep');

        // Set spinner color based on domain
        this.setSpinnerColor();
    },

    setSpinnerColor() {
        const domainColors = {
            'chaos-forge': '#00ff64',
            'quantum-vault': '#ffff00',
            'mind-matrix': '#00ccff',
            'soul-sanctuary': '#ff00ff',
            'reality-forge': '#ff6600',
            'arkitek-academy': '#ff0066',
            'nexus-terminal': '#6600ff'
        };

        const path = window.location.pathname;
        for (const [domain, color] of Object.entries(domainColors)) {
            if (path.includes(domain)) {
                document.documentElement.style.setProperty('--spinner-color', color);
                break;
            }
        }
    },

    updateProgress(percent, substep = null) {
        if (this.progressBar) {
            this.progressBar.style.width = `${percent}%`;
        }
        if (substep && this.substep) {
            this.substep.textContent = substep;
        }
    },

    monitorPageLoad() {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            this.updateProgress(progress);
        }, 200);

        window.addEventListener('load', () => {
            clearInterval(interval);
            this.updateProgress(100, 'Complete!');
            setTimeout(() => this.hideLoading(), 500);
        });

        // Fallback: hide after 5 seconds regardless
        setTimeout(() => {
            clearInterval(interval);
            this.hideLoading();
        }, 5000);
    },

    handleThreeJSLoading() {
        // Monitor Three.js loading if present
        const checkThreeJS = setInterval(() => {
            if (typeof THREE !== 'undefined') {
                this.updateProgress(50, 'Loading 3D visualization...');
                clearInterval(checkThreeJS);

                // Wait for scene to be ready
                setTimeout(() => {
                    const canvas = document.querySelector('canvas');
                    if (canvas) {
                        this.updateProgress(75, 'Rendering 3D scene...');
                    }
                }, 1000);
            }
        }, 100);

        // Stop checking after 3 seconds
        setTimeout(() => clearInterval(checkThreeJS), 3000);
    },

    hideLoading() {
        if (this.overlay) {
            this.overlay.classList.add('fade-out');
            setTimeout(() => {
                this.overlay.remove();
            }, 500);
        }
    },

    addErrorHandling() {
        // Global error handler
        window.addEventListener('error', (event) => {
            console.error('Error caught:', event.error);
            this.showError('An error occurred loading this page. Please refresh.');
        });

        // Unhandled promise rejection
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.showError('Failed to load some content. Refresh to try again.');
        });
    },

    showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(255, 0, 0, 0.9);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            z-index: 100000;
            box-shadow: 0 5px 20px rgba(255, 0, 0, 0.5);
            max-width: 300px;
            animation: slideIn 0.3s ease;
        `;
        errorDiv.innerHTML = `
            <style>
                @keyframes slideIn {
                    from { transform: translateX(400px); }
                    to { transform: translateX(0); }
                }
            </style>
            <strong>⚠️ Error</strong><br>${message}
            <button onclick="this.parentElement.remove()" style="
                margin-top: 10px;
                background: white;
                color: red;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            ">Dismiss</button>
        `;

        document.body.appendChild(errorDiv);

        // Auto-remove after 10 seconds
        setTimeout(() => {
            errorDiv.style.opacity = '0';
            errorDiv.style.transition = 'opacity 0.5s';
            setTimeout(() => errorDiv.remove(), 500);
        }, 10000);
    },

    setupProgressiveEnhancement() {
        // Check for WebGL support
        const canvas = document.createElement('canvas');
        const hasWebGL = !!(canvas.getContext('webgl') || canvas.getContext('experimental-webgl'));

        if (!hasWebGL) {
            this.showError('Your browser doesn\'t support 3D graphics (WebGL). Some features may not work.');
        }

        // Check for localStorage
        try {
            localStorage.setItem('test', 'test');
            localStorage.removeItem('test');
        } catch (e) {
            console.warn('localStorage not available');
        }
    },

    // Show loading for specific async operations
    showOperationLoading(message) {
        const mini = document.createElement('div');
        mini.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            z-index: 100000;
            display: flex;
            align-items: center;
            gap: 10px;
        `;
        mini.innerHTML = `
            <div style="
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-top-color: white;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
            "></div>
            ${message}
        `;

        document.body.appendChild(mini);
        return mini; // Return so caller can remove it
    }
};

// Auto-initialize
if (document.readyState === 'loading') {
    LoadingStates.init();
} else {
    // Page already loaded, skip loading screen
    console.log('Page already loaded, skipping loading screen');
}

window.LoadingStates = LoadingStates;
