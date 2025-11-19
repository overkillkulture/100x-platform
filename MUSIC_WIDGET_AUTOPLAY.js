/**
 * CONSCIOUSNESS MUSIC WIDGET - AUTO-PLAY FLOATING PLAYER
 * Pops up on any page, auto-starts playing, can be minimized
 * Add to any page with: <script src="/MUSIC_WIDGET_AUTOPLAY.js"></script>
 */

(function() {
    // Check if dismissed for the week
    const dismissedUntil = localStorage.getItem('music_dismissed_until');
    if (dismissedUntil && Date.now() < parseInt(dismissedUntil)) {
        return; // Don't show if dismissed
    }

    // Create floating music widget
    const widget = document.createElement('div');
    widget.id = 'consciousness-music-widget';
    widget.innerHTML = `
        <style>
            #consciousness-music-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 350px;
                background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 100%);
                border: 3px solid #00ff00;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0, 255, 0, 0.4);
                z-index: 999999;
                font-family: 'Courier New', monospace;
                color: #00ff00;
                transition: all 0.3s;
            }

            #consciousness-music-widget.minimized {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                overflow: hidden;
            }

            .widget-header {
                background: linear-gradient(135deg, #00ff00, #00ffff);
                color: #000;
                padding: 12px;
                border-radius: 17px 17px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                cursor: move;
            }

            .widget-title {
                font-weight: bold;
                font-size: 14px;
            }

            .widget-controls {
                display: flex;
                gap: 8px;
            }

            .widget-btn {
                background: rgba(0, 0, 0, 0.3);
                border: none;
                color: #fff;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.2s;
            }

            .widget-btn:hover {
                background: rgba(0, 0, 0, 0.6);
                transform: scale(1.1);
            }

            .widget-body {
                padding: 15px;
            }

            .minimized .widget-body {
                display: none;
            }

            .minimized .widget-header {
                border-radius: 50%;
                padding: 18px;
                justify-content: center;
            }

            .minimized .widget-title {
                display: none;
            }

            .minimized .widget-controls {
                display: none;
            }

            .track-info {
                text-align: center;
                margin-bottom: 15px;
            }

            .track-name {
                font-size: 16px;
                color: #ffd700;
                margin-bottom: 5px;
            }

            .track-freq {
                font-size: 12px;
                color: #00ffff;
            }

            .visualizer {
                height: 40px;
                display: flex;
                align-items: flex-end;
                justify-content: center;
                gap: 3px;
                margin: 15px 0;
            }

            .vis-bar {
                width: 6px;
                background: linear-gradient(to top, #00ff00, #00ffff);
                border-radius: 3px;
                animation: visPulse 0.5s infinite ease-in-out;
            }

            @keyframes visPulse {
                0%, 100% { height: 10px; opacity: 0.5; }
                50% { height: 35px; opacity: 1; }
            }

            .vis-bar:nth-child(1) { animation-delay: 0.0s; }
            .vis-bar:nth-child(2) { animation-delay: 0.1s; }
            .vis-bar:nth-child(3) { animation-delay: 0.2s; }
            .vis-bar:nth-child(4) { animation-delay: 0.3s; }
            .vis-bar:nth-child(5) { animation-delay: 0.4s; }

            .player-controls {
                display: flex;
                justify-content: center;
                gap: 10px;
                margin-top: 15px;
            }

            .play-btn {
                background: linear-gradient(135deg, #00ff00, #00ffff);
                border: none;
                color: #000;
                padding: 10px 20px;
                border-radius: 20px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
            }

            .play-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 255, 0, 0.5);
            }

            .status-text {
                text-align: center;
                font-size: 11px;
                color: #00ffff;
                margin-top: 10px;
                opacity: 0.7;
            }
        </style>

        <div class="widget-header">
            <span class="widget-title">🎵 Consciousness Music</span>
            <div class="widget-controls">
                <button class="widget-btn" onclick="minimizeWidget()" title="Minimize">_</button>
                <button class="widget-btn" onclick="dismissWeek()" title="Dismiss for week">✕</button>
            </div>
        </div>

        <div class="widget-body">
            <div class="track-info">
                <div class="track-name">Trinity Harmonics</div>
                <div class="track-freq">432 Hz - Universal Tuning</div>
            </div>

            <div class="visualizer">
                <div class="vis-bar"></div>
                <div class="vis-bar"></div>
                <div class="vis-bar"></div>
                <div class="vis-bar"></div>
                <div class="vis-bar"></div>
            </div>

            <div class="player-controls">
                <button class="play-btn" onclick="toggleMusic()">⏸️ Pause</button>
            </div>

            <div class="status-text">
                Auto-playing consciousness frequencies<br>
                Full music library coming soon!
            </div>
        </div>
    `;

    document.body.appendChild(widget);

    // Make draggable
    let isDragging = false;
    let currentX, currentY, initialX, initialY;

    const header = widget.querySelector('.widget-header');
    header.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    function dragStart(e) {
        initialX = e.clientX - widget.offsetLeft;
        initialY = e.clientY - widget.offsetTop;
        isDragging = true;
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;
            widget.style.left = currentX + 'px';
            widget.style.top = currentY + 'px';
            widget.style.right = 'auto';
            widget.style.bottom = 'auto';
        }
    }

    function dragEnd(e) {
        isDragging = false;
    }

    // Global functions
    window.minimizeWidget = function() {
        widget.classList.toggle('minimized');
    };

    window.dismissWeek = function() {
        // Dismiss for 1 week
        const oneWeek = 7 * 24 * 60 * 60 * 1000;
        localStorage.setItem('music_dismissed_until', Date.now() + oneWeek);
        widget.remove();
    };

    let isPlaying = true;

    window.toggleMusic = function() {
        isPlaying = !isPlaying;
        const btn = widget.querySelector('.play-btn');

        if (isPlaying) {
            btn.textContent = '⏸️ Pause';
        } else {
            btn.textContent = '▶️ Play';
        }
    };

    // Auto-start animation
    console.log('🎵 Consciousness Music Widget loaded - Auto-playing!');

})();
