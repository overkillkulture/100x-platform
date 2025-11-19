// ENHANCED BUG REPORTER - Collapsible with improved positioning
(function() {
    'use strict';

    // Wait for DOM to be ready
    function init() {
        // Get page name from URL
    // Add wiggle animation CSS
    const style = document.createElement("style");
    style.textContent = `
        @keyframes wiggleRotate {
            0%, 100% { transform: rotate(-5deg); }
            50% { transform: rotate(5deg); }
        }
    `;
    document.head.appendChild(style);

        const getPageName = () => {
            const path = window.location.pathname;
            const page = path.split('/').pop() || 'Homepage';
            return page.replace('.html', '').replace(/-/g, ' ').replace(/_/g, ' ')
                       .split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
        };

        // Create collapsible bug button container
        const container = document.createElement('div');
        container.id = 'bug-reporter-container';
        container.style.cssText = `
            position: fixed;
            bottom: 120px;
            right: 20px;
            z-index: 999998;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 10px;
        `;

        // Create expandable label
        const label = document.createElement('div');
        label.id = 'bug-label';
        label.textContent = 'Bug';
        label.style.cssText = `
            background: rgba(255, 68, 68, 0.95);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            opacity: 0;
            transform: translateX(20px);
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            white-space: nowrap;
        `;

        // Create button
        const btn = document.createElement('button');
        btn.innerHTML = '🐛';
        btn.setAttribute('aria-label', 'Report Bug');
        btn.style.cssText = `
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: #ff4444;
            color: white;
            border: none;
            font-size: 28px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        `;

        // Create tooltip cloud
        const tooltip = document.createElement('div');
        tooltip.style.cssText = `
            position: fixed;
            bottom: 185px;
            right: 30px;
            background: rgba(26, 26, 46, 0.98);
            color: white;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 14px;
            opacity: 0;
            pointer-events: none;
            transition: all 0.3s ease;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
            border: 2px solid #ff4444;
            max-width: 250px;
            z-index: 999997;
            transform: translateY(10px);
        `;
        tooltip.innerHTML = `
            <div style="color: #00ff88; font-weight: bold; margin-bottom: 4px;">🐛 Report Bugs</div>
            <div style="color: #ccc;">See something broken? Click the bug button to let us know!</div>
        `;

        // Add arrow to tooltip
        const arrow = document.createElement('div');
        arrow.style.cssText = `
            position: absolute;
            bottom: -8px;
            right: 20px;
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-top: 8px solid #ff4444;
        `;
        tooltip.appendChild(arrow);

        // Add hover effects
        btn.onmouseenter = () => {
            btn.style.transform = 'scale(1.1)';
            label.style.opacity = '1';
            label.style.transform = 'translateX(0)';
            tooltip.style.opacity = '1';
            tooltip.style.transform = 'translateY(0)';
        };

        btn.onmouseleave = () => {
            btn.style.transform = 'scale(1)';
            setTimeout(() => {
                label.style.opacity = '0';
                label.style.transform = 'translateX(20px)';
                tooltip.style.opacity = '0';
                tooltip.style.transform = 'translateY(10px)';
            }, 500);
        };

        // Create modal
        const modal = document.createElement('div');
        modal.style.cssText = `
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 9999999;
            align-items: center;
            justify-content: center;
        `;

        modal.innerHTML = `
            <div style="background: #1a1a2e; padding: 2rem; border-radius: 12px; max-width: 500px; width: 90%;">
                <h3 style="color: #00ff88; margin-bottom: 1rem;">🐛 Bug Report</h3>
                <div style="background: rgba(0, 255, 136, 0.1); border: 1px solid #00ff88; border-radius: 6px; padding: 0.8rem; margin-bottom: 1rem;">
                    <div style="color: #888; font-size: 12px; margin-bottom: 0.3rem;">📍 Reporting from:</div>
                    <div id="bugPageName" style="color: #00ff88; font-weight: bold; font-size: 14px;">${getPageName()}</div>
                    <div style="color: #666; font-size: 11px; margin-top: 0.3rem; word-break: break-all;">${window.location.href}</div>
                </div>
                <textarea id="bugDesc" placeholder="What's broken?" style="width: 100%; height: 100px; padding: 0.5rem; border-radius: 6px; border: 2px solid #00ff88; background: #0a0a0a; color: #fff; font-size: 14px; font-family: sans-serif; box-sizing: border-box;"></textarea>
                <div id="bugStatus" style="color: #00ff88; margin-top: 0.5rem; min-height: 20px;"></div>
                <div style="margin-top: 1rem; display: flex; gap: 1rem;">
                    <button id="bugCancel" style="flex: 1; padding: 0.8rem; border: 2px solid #666; background: transparent; color: #ccc; border-radius: 6px; cursor: pointer; font-size: 14px;">Cancel</button>
                    <button id="bugSubmit" style="flex: 1; padding: 0.8rem; border: none; background: #00ff88; color: #000; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;">Submit</button>
                </div>
            </div>
        `;

        // Assemble container
        container.appendChild(label);
        container.appendChild(btn);

        // Add to page
        document.body.appendChild(container);
        document.body.appendChild(tooltip);
        document.body.appendChild(modal);

        // Splatter animation and open GitHub
        btn.onclick = () => {
            // Splatter/squish animation
            btn.style.transform = 'scale(0.8) rotate(15deg)';
            btn.style.background = '#cc0000';
            btn.innerHTML = '💥';

            setTimeout(() => {
                btn.style.transform = 'scale(1.3) rotate(-10deg)';
                btn.style.borderRadius = '40% 60% 70% 30% / 40% 50% 60% 50%';
            }, 100);

            setTimeout(() => {
                btn.style.transform = 'scale(0.9) rotate(5deg)';
                btn.style.borderRadius = '60% 40% 30% 70% / 60% 30% 70% 40%';
            }, 200);

            setTimeout(() => {
                btn.style.transform = 'scale(1.1)';
                btn.style.borderRadius = '50%';
                btn.style.background = '#ff4444';
                btn.innerHTML = '🐛';

                // Open GitHub issues in new tab
                window.open('https://github.com/overkillkulture/consciousness-bugs/issues', '_blank');

                // Reset after opening
                setTimeout(() => {
                    btn.style.transform = 'scale(1)';
                }, 200);
            }, 400);
        };

        // Hide modal
        document.getElementById('bugCancel').onclick = () => {
            modal.style.display = 'none';
            document.getElementById('bugDesc').value = '';
            document.getElementById('bugStatus').textContent = '';
        };

        // Submit bug
        document.getElementById('bugSubmit').onclick = async () => {
            const desc = document.getElementById('bugDesc').value.trim();
            const status = document.getElementById('bugStatus');

            if (!desc) {
                status.textContent = 'Please describe the bug';
                status.style.color = '#ff4444';
                return;
            }

            try {
                const response = await fetch('/.netlify/functions/web-bug-report', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        description: desc,
                        reporter: localStorage.getItem('workspace_user_name') || 'Anonymous',
                        page: window.location.href,
                        pageName: getPageName()
                    })
                });

                if (response.ok) {
                    status.textContent = '✅ Bug reported!';
                    status.style.color = '#00ff88';
                    setTimeout(() => {
                        modal.style.display = 'none';
                        document.getElementById('bugDesc').value = '';
                        status.textContent = '';
                    }, 1500);
                } else {
                    throw new Error('Failed');
                }
            } catch (e) {
                status.textContent = '❌ Error - try again';
                status.style.color = '#ff4444';
            }
        };
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
