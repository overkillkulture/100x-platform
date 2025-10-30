// DEAD SIMPLE BUG REPORTER - NO DEPENDENCIES
(function() {
    'use strict';

    // Wait for DOM to be ready
    function init() {
        // Create button
        const btn = document.createElement('button');
    btn.innerHTML = '🐛';
    btn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: #ff4444;
        color: white;
        border: none;
        font-size: 30px;
        cursor: pointer;
        z-index: 999999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;

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
            <h3 style="color: #00ff88; margin-bottom: 1rem;">Report Bug</h3>
            <textarea id="bugDesc" placeholder="What's broken?" style="width: 100%; height: 100px; padding: 0.5rem; border-radius: 6px; border: 2px solid #00ff88; background: #0a0a0a; color: #fff; font-size: 14px; font-family: sans-serif; box-sizing: border-box;"></textarea>
            <div id="bugStatus" style="color: #00ff88; margin-top: 0.5rem; min-height: 20px;"></div>
            <div style="margin-top: 1rem; display: flex; gap: 1rem;">
                <button id="bugCancel" style="flex: 1; padding: 0.8rem; border: 2px solid #666; background: transparent; color: #ccc; border-radius: 6px; cursor: pointer; font-size: 14px;">Cancel</button>
                <button id="bugSubmit" style="flex: 1; padding: 0.8rem; border: none; background: #00ff88; color: #000; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;">Submit</button>
            </div>
        </div>
    `;

    // Add to page
    document.body.appendChild(btn);
    document.body.appendChild(modal);

    // Show modal
    btn.onclick = () => {
        modal.style.display = 'flex';
        document.getElementById('bugDesc').focus();
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
                    page: window.location.href
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
