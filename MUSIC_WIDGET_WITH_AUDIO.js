/**
 * CONSCIOUSNESS MUSIC WIDGET - REAL AUDIO PLAYBACK
 * Auto-playing floating music player with actual audio files
 * Add to any page with: <script src="/MUSIC_WIDGET_WITH_AUDIO.js"></script>
 */

(function() {
    // Check if dismissed for the week
    const dismissedUntil = localStorage.getItem('music_dismissed_until');
    if (dismissedUntil && Date.now() < parseInt(dismissedUntil)) {
        return; // Don't show if dismissed
    }

    // Playlist - consciousness music from The Overkill Tapes
    const playlist = [
        { title: 'Overkill Revolution', file: '/music/overkill-revolution.wav', frequency: '432 Hz' },
        { title: 'Overkill Is The Cure', file: '/music/overkill-is-the-cure.wav', frequency: '528 Hz' },
        { title: 'Color Is The Cure', file: '/music/color-is-the-cure.wav', frequency: '639 Hz' },
        { title: 'Studio Jumanji', file: '/music/studio-jumanji.wav', frequency: '741 Hz' }
    ];

    let currentTrack = 0;

    // Create audio element
    const audio = new Audio();
    audio.volume = 0.5; // Start at 50% volume
    audio.loop = false;

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

            .progress-bar {
                width: 100%;
                height: 6px;
                background: rgba(0, 255, 0, 0.2);
                border-radius: 3px;
                margin: 10px 0;
                overflow: hidden;
                cursor: pointer;
            }

            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #00ff00, #00ffff);
                width: 0%;
                transition: width 0.1s;
            }

            .time-display {
                display: flex;
                justify-content: space-between;
                font-size: 10px;
                color: #00ff00;
                margin-bottom: 10px;
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

            .playing .vis-bar {
                animation-play-state: running;
            }

            .paused .vis-bar {
                animation-play-state: paused;
            }

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
                font-size: 14px;
            }

            .play-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 255, 0, 0.5);
            }

            .nav-btn {
                background: rgba(0, 255, 0, 0.2);
                border: 1px solid #00ff00;
                color: #00ff00;
                padding: 8px 12px;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .nav-btn:hover {
                background: rgba(0, 255, 0, 0.4);
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
                <div class="track-name" id="trackName">Loading...</div>
                <div class="track-freq" id="trackFreq">432 Hz - Universal Tuning</div>
            </div>

            <div class="time-display">
                <span id="currentTime">0:00</span>
                <span id="duration">0:00</span>
            </div>

            <div class="progress-bar" onclick="seekTo(event)">
                <div class="progress-fill" id="progressFill"></div>
            </div>

            <div class="visualizer playing" id="visualizer">
                <div class="vis-bar"></div>
                <div class="vis-bar"></div>
                <div class="vis-bar"></div>
                <div class="vis-bar"></div>
                <div class="vis-bar"></div>
            </div>

            <div class="player-controls">
                <button class="nav-btn" onclick="previousTrack()">⏮️</button>
                <button class="play-btn" id="playBtn" onclick="toggleMusic()">⏸️ Pause</button>
                <button class="nav-btn" onclick="nextTrack()">⏭️</button>
            </div>

            <div class="status-text">
                <span id="statusText">The Overkill Tapes - Track <span id="trackNum">1</span> of ${playlist.length}</span>
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
        const oneWeek = 7 * 24 * 60 * 60 * 1000;
        localStorage.setItem('music_dismissed_until', Date.now() + oneWeek);
        audio.pause();
        widget.remove();
    };

    window.toggleMusic = function() {
        if (audio.paused) {
            audio.play();
        } else {
            audio.pause();
        }
    };

    window.nextTrack = function() {
        currentTrack = (currentTrack + 1) % playlist.length;
        loadTrack();
    };

    window.previousTrack = function() {
        currentTrack = (currentTrack - 1 + playlist.length) % playlist.length;
        loadTrack();
    };

    window.seekTo = function(e) {
        const bar = e.currentTarget;
        const rect = bar.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        audio.currentTime = percent * audio.duration;
    };

    // Load and play track
    function loadTrack() {
        const track = playlist[currentTrack];
        audio.src = track.file;
        audio.play();

        document.getElementById('trackName').textContent = track.title;
        document.getElementById('trackFreq').textContent = track.frequency + ' - Consciousness Frequency';
        document.getElementById('trackNum').textContent = currentTrack + 1;
    }

    // Audio event listeners
    audio.addEventListener('play', () => {
        document.getElementById('playBtn').innerHTML = '⏸️ Pause';
        document.getElementById('visualizer').className = 'visualizer playing';
    });

    audio.addEventListener('pause', () => {
        document.getElementById('playBtn').innerHTML = '▶️ Play';
        document.getElementById('visualizer').className = 'visualizer paused';
    });

    audio.addEventListener('timeupdate', () => {
        if (audio.duration) {
            const percent = (audio.currentTime / audio.duration) * 100;
            document.getElementById('progressFill').style.width = percent + '%';

            document.getElementById('currentTime').textContent = formatTime(audio.currentTime);
            document.getElementById('duration').textContent = formatTime(audio.duration);
        }
    });

    audio.addEventListener('ended', () => {
        nextTrack();
    });

    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    // Auto-start first track
    loadTrack();

    console.log('🎵 Consciousness Music Widget loaded - Playing The Overkill Tapes!');

})();
