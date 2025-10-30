// PROFESSIONAL FEATURE ANNOUNCEMENT SYSTEM
// Shows new features to users automatically - no email needed

(function() {
    'use strict';

    const ANNOUNCEMENTS = [
        {
            id: 'live-bug-monitor-oct-29-2025',
            title: '⚡ NEW: Live Bug Monitor',
            message: 'Bugs now auto-refresh every 5 seconds! Click "Live Bug Monitor" in workspace to see bugs appear instantly.',
            action: {
                text: 'Try It Now',
                url: '/bugs-live.html'
            },
            expires: '2025-11-05', // Show for 1 week
            priority: 'high'
        }
    ];

    function getSeenAnnouncements() {
        const seen = localStorage.getItem('seen_announcements');
        return seen ? JSON.parse(seen) : [];
    }

    function markAsSeen(announcementId) {
        const seen = getSeenAnnouncements();
        if (!seen.includes(announcementId)) {
            seen.push(announcementId);
            localStorage.setItem('seen_announcements', JSON.stringify(seen));
        }
    }

    function isExpired(expiryDate) {
        return new Date() > new Date(expiryDate);
    }

    function showAnnouncements() {
        const seen = getSeenAnnouncements();
        const activeAnnouncements = ANNOUNCEMENTS.filter(a =>
            !seen.includes(a.id) && !isExpired(a.expires)
        );

        if (activeAnnouncements.length === 0) return;

        // Get highest priority announcement
        const announcement = activeAnnouncements.sort((a, b) => {
            const priority = { high: 3, medium: 2, low: 1 };
            return priority[b.priority || 'medium'] - priority[a.priority || 'medium'];
        })[0];

        // Create announcement banner
        const banner = document.createElement('div');
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #00ffff 0%, #00ff88 100%);
            color: #000;
            padding: 1rem 2rem;
            z-index: 999998;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.5);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            animation: slideDown 0.3s ease-out;
        `;

        banner.innerHTML = `
            <div style="display: flex; align-items: center; gap: 1rem; flex: 1;">
                <div style="font-size: 1.5rem;">🎉</div>
                <div>
                    <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 0.2rem;">${announcement.title}</div>
                    <div style="font-size: 0.9rem;">${announcement.message}</div>
                </div>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                ${announcement.action ? `
                    <button id="announcementAction" style="
                        background: #000;
                        color: #00ff88;
                        border: none;
                        padding: 0.7rem 1.5rem;
                        border-radius: 6px;
                        font-weight: bold;
                        cursor: pointer;
                        font-size: 1rem;
                    ">${announcement.action.text}</button>
                ` : ''}
                <button id="dismissAnnouncement" style="
                    background: transparent;
                    border: 2px solid #000;
                    color: #000;
                    padding: 0.7rem 1rem;
                    border-radius: 6px;
                    font-weight: bold;
                    cursor: pointer;
                    font-size: 0.9rem;
                ">Got It</button>
            </div>
        `;

        // Add animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideDown {
                from { transform: translateY(-100%); }
                to { transform: translateY(0); }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(banner);

        // Add event listeners
        if (announcement.action) {
            document.getElementById('announcementAction').onclick = () => {
                window.location.href = announcement.action.url;
                markAsSeen(announcement.id);
            };
        }

        document.getElementById('dismissAnnouncement').onclick = () => {
            banner.style.animation = 'slideDown 0.3s ease-out reverse';
            setTimeout(() => banner.remove(), 300);
            markAsSeen(announcement.id);
        };

        // Auto-dismiss after 30 seconds
        setTimeout(() => {
            if (document.body.contains(banner)) {
                banner.style.animation = 'slideDown 0.3s ease-out reverse';
                setTimeout(() => banner.remove(), 300);
                markAsSeen(announcement.id);
            }
        }, 30000);
    }

    // Show announcements when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', showAnnouncements);
    } else {
        showAnnouncements();
    }
})();
