/**
 * VIRAL SHARE ENGINE
 * One-click sharing to social media with built-in tracking
 *
 * Usage: Add to any showcase page
 * <script src="../shared/viral-share-engine.js"></script>
 * Then call: ViralShare.init({ title: "Check this out!", text: "Amazing demo..." });
 */

(function() {
    window.ViralShare = {
        config: {
            title: "Consciousness Revolution - Interactive Showcase",
            text: "Check out this mind-blowing AI demo!",
            url: window.location.href,
            hashtags: ["AI", "ConsciousnessRevolution", "TrinityAI"],
            trackingEnabled: true
        },

        init: function(customConfig = {}) {
            // Merge custom config
            this.config = { ...this.config, ...customConfig };

            // Create share buttons
            this.createShareUI();

            // Track page view
            this.trackEvent('page_view');

            console.log('🌀 Viral Share Engine initialized');
        },

        createShareUI: function() {
            // Check if already exists
            if (document.getElementById('viral-share-container')) return;

            // Create floating share bar
            const shareContainer = document.createElement('div');
            shareContainer.id = 'viral-share-container';
            shareContainer.innerHTML = `
                <style>
                    #viral-share-container {
                        position: fixed;
                        right: 20px;
                        top: 50%;
                        transform: translateY(-50%);
                        display: flex;
                        flex-direction: column;
                        gap: 10px;
                        z-index: 9997;
                        transition: all 0.3s ease;
                    }

                    #viral-share-container.hidden {
                        right: -100px;
                    }

                    .viral-share-btn {
                        width: 50px;
                        height: 50px;
                        border-radius: 50%;
                        border: none;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 20px;
                        transition: all 0.3s ease;
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                        position: relative;
                    }

                    .viral-share-btn:hover {
                        transform: scale(1.1);
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
                    }

                    .viral-share-btn.twitter {
                        background: #1DA1F2;
                        color: white;
                    }

                    .viral-share-btn.reddit {
                        background: #FF4500;
                        color: white;
                    }

                    .viral-share-btn.hackernews {
                        background: #FF6600;
                        color: white;
                    }

                    .viral-share-btn.linkedin {
                        background: #0077B5;
                        color: white;
                    }

                    .viral-share-btn.copy {
                        background: #00ff41;
                        color: #0a0e27;
                    }

                    .viral-share-btn .tooltip {
                        position: absolute;
                        right: 60px;
                        background: rgba(0, 0, 0, 0.8);
                        color: white;
                        padding: 5px 10px;
                        border-radius: 5px;
                        white-space: nowrap;
                        opacity: 0;
                        pointer-events: none;
                        transition: opacity 0.3s ease;
                        font-size: 12px;
                        font-family: 'Courier New', monospace;
                    }

                    .viral-share-btn:hover .tooltip {
                        opacity: 1;
                    }

                    .share-toggle {
                        width: 50px;
                        height: 50px;
                        border-radius: 50%;
                        background: linear-gradient(135deg, #00ff41, #00d4ff);
                        border: none;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                        box-shadow: 0 2px 10px rgba(0, 255, 65, 0.4);
                        transition: all 0.3s ease;
                    }

                    .share-toggle:hover {
                        transform: scale(1.1);
                        box-shadow: 0 4px 20px rgba(0, 255, 65, 0.6);
                    }

                    .share-count {
                        position: absolute;
                        top: -5px;
                        right: -5px;
                        background: #ff4757;
                        color: white;
                        border-radius: 50%;
                        width: 20px;
                        height: 20px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 10px;
                        font-weight: bold;
                    }

                    @media (max-width: 768px) {
                        #viral-share-container {
                            right: 10px;
                        }
                        .viral-share-btn {
                            width: 45px;
                            height: 45px;
                        }
                    }
                </style>

                <button class="share-toggle" onclick="ViralShare.toggleShareButtons()" title="Share this showcase">
                    🚀
                    <span class="share-count" id="shareCount">0</span>
                </button>

                <div id="shareButtons" style="display: none;">
                    <button class="viral-share-btn twitter" onclick="ViralShare.shareToTwitter()">
                        𝕏
                        <span class="tooltip">Share on Twitter/X</span>
                    </button>

                    <button class="viral-share-btn reddit" onclick="ViralShare.shareToReddit()">
                        ⬆
                        <span class="tooltip">Share on Reddit</span>
                    </button>

                    <button class="viral-share-btn hackernews" onclick="ViralShare.shareToHackerNews()">
                        Y
                        <span class="tooltip">Share on Hacker News</span>
                    </button>

                    <button class="viral-share-btn linkedin" onclick="ViralShare.shareToLinkedIn()">
                        in
                        <span class="tooltip">Share on LinkedIn</span>
                    </button>

                    <button class="viral-share-btn copy" onclick="ViralShare.copyLink()">
                        📋
                        <span class="tooltip">Copy Link</span>
                    </button>
                </div>
            `;

            document.body.appendChild(shareContainer);
            this.loadShareCount();
        },

        toggleShareButtons: function() {
            const buttons = document.getElementById('shareButtons');
            if (buttons.style.display === 'none') {
                buttons.style.display = 'flex';
                buttons.style.flexDirection = 'column';
                buttons.style.gap = '10px';
            } else {
                buttons.style.display = 'none';
            }
        },

        shareToTwitter: function() {
            const url = encodeURIComponent(this.config.url);
            const text = encodeURIComponent(this.config.text);
            const hashtags = this.config.hashtags.join(',');

            window.open(
                `https://twitter.com/intent/tweet?url=${url}&text=${text}&hashtags=${hashtags}`,
                '_blank',
                'width=550,height=420'
            );

            this.trackEvent('share_twitter');
            this.incrementShareCount();
        },

        shareToReddit: function() {
            const url = encodeURIComponent(this.config.url);
            const title = encodeURIComponent(this.config.title);

            window.open(
                `https://reddit.com/submit?url=${url}&title=${title}`,
                '_blank',
                'width=800,height=600'
            );

            this.trackEvent('share_reddit');
            this.incrementShareCount();
        },

        shareToHackerNews: function() {
            const url = encodeURIComponent(this.config.url);
            const title = encodeURIComponent(this.config.title);

            window.open(
                `https://news.ycombinator.com/submitlink?u=${url}&t=${title}`,
                '_blank',
                'width=800,height=600'
            );

            this.trackEvent('share_hackernews');
            this.incrementShareCount();
        },

        shareToLinkedIn: function() {
            const url = encodeURIComponent(this.config.url);

            window.open(
                `https://www.linkedin.com/sharing/share-offsite/?url=${url}`,
                '_blank',
                'width=550,height=420'
            );

            this.trackEvent('share_linkedin');
            this.incrementShareCount();
        },

        copyLink: function() {
            navigator.clipboard.writeText(this.config.url).then(() => {
                // Show temporary success message
                const copyBtn = document.querySelector('.viral-share-btn.copy');
                const originalText = copyBtn.innerHTML;
                copyBtn.innerHTML = '✅<span class="tooltip">Copied!</span>';

                setTimeout(() => {
                    copyBtn.innerHTML = originalText;
                }, 2000);

                this.trackEvent('copy_link');
                this.incrementShareCount();
            });
        },

        incrementShareCount: function() {
            const currentCount = parseInt(localStorage.getItem('shareCount') || '0');
            const newCount = currentCount + 1;
            localStorage.setItem('shareCount', newCount.toString());
            document.getElementById('shareCount').textContent = newCount;
        },

        loadShareCount: function() {
            const count = parseInt(localStorage.getItem('shareCount') || '0');
            document.getElementById('shareCount').textContent = count;
        },

        trackEvent: function(eventName, data = {}) {
            if (!this.config.trackingEnabled) return;

            const event = {
                event: eventName,
                url: this.config.url,
                timestamp: new Date().toISOString(),
                userAgent: navigator.userAgent,
                ...data
            };

            // Store locally
            const events = JSON.parse(localStorage.getItem('viralEvents') || '[]');
            events.push(event);
            localStorage.setItem('viralEvents', JSON.stringify(events.slice(-100))); // Keep last 100

            // Could send to analytics API here
            console.log('📊 Viral Event:', event);

            // Optional: Send to backend analytics
            if (typeof fetch !== 'undefined') {
                fetch('/api/analytics/track', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(event)
                }).catch(() => {}); // Silent fail if no backend
            }
        },

        getAnalytics: function() {
            const events = JSON.parse(localStorage.getItem('viralEvents') || '[]');
            const shareCount = parseInt(localStorage.getItem('shareCount') || '0');

            return {
                totalShares: shareCount,
                events: events,
                sharesByPlatform: {
                    twitter: events.filter(e => e.event === 'share_twitter').length,
                    reddit: events.filter(e => e.event === 'share_reddit').length,
                    hackernews: events.filter(e => e.event === 'share_hackernews').length,
                    linkedin: events.filter(e => e.event === 'share_linkedin').length,
                    copy: events.filter(e => e.event === 'copy_link').length
                }
            };
        }
    };

    // Auto-initialize with defaults if config provided via data attribute
    document.addEventListener('DOMContentLoaded', () => {
        const metaTitle = document.querySelector('meta[property="og:title"]');
        const metaDescription = document.querySelector('meta[property="og:description"]');

        if (metaTitle || metaDescription) {
            window.ViralShare.init({
                title: metaTitle?.content || document.title,
                text: metaDescription?.content || "Check out this amazing showcase!"
            });
        }
    });
})();

console.log('🌀 Viral Share Engine loaded - Ready for consciousness distribution');
