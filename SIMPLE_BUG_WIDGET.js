// DEAD SIMPLE BUG REPORTER - NO VOICE, JUST WORKS
// Inject this into any page and it will work

(function() {
    // Create the bug button (bottom right)
    const bugButton = document.createElement('div');
    bugButton.id = 'simple-bug-button';
    bugButton.innerHTML = '🐛 Bug?';
    bugButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #ff4444;
        color: white;
        padding: 15px 20px;
        border-radius: 50px;
        cursor: pointer;
        z-index: 999999;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        font-size: 16px;
    `;

    // Create the popup form (hidden by default)
    const bugPopup = document.createElement('div');
    bugPopup.id = 'simple-bug-popup';
    bugPopup.style.cssText = `
        position: fixed;
        bottom: 100px;
        right: 20px;
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        z-index: 999999;
        display: none;
        width: 300px;
        max-width: 90vw;
    `;
    bugPopup.innerHTML = `
        <h3 style="margin: 0 0 15px 0; color: #333;">Report a Bug</h3>
        <textarea id="simple-bug-input" placeholder="Describe the bug..." style="width: 100%; height: 80px; padding: 10px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; resize: none; -webkit-appearance: none;"></textarea>
        <div style="margin-top: 10px; display: flex; gap: 10px;">
            <button id="simple-bug-submit" style="flex: 1; background: #00cc66; color: white; border: none; padding: 16px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; touch-action: manipulation; -webkit-tap-highlight-color: transparent;">Submit</button>
            <button id="simple-bug-cancel" style="background: #999; color: white; border: none; padding: 16px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; touch-action: manipulation; -webkit-tap-highlight-color: transparent;">Cancel</button>
        </div>
        <div id="simple-bug-status" style="margin-top: 10px; font-size: 13px; text-align: center;"></div>
    `;

    // Add to page
    document.body.appendChild(bugButton);
    document.body.appendChild(bugPopup);

    // Toggle popup
    bugButton.addEventListener('click', function() {
        bugPopup.style.display = bugPopup.style.display === 'none' ? 'block' : 'none';
        if (bugPopup.style.display === 'block') {
            document.getElementById('simple-bug-input').focus();
        }
    });

    // Cancel button - with touch support
    const cancelBtn = document.getElementById('simple-bug-cancel');
    const cancelHandler = function(e) {
        e.preventDefault();
        e.stopPropagation();
        bugPopup.style.display = 'none';
        document.getElementById('simple-bug-input').value = '';
        document.getElementById('simple-bug-status').textContent = '';
    };
    cancelBtn.addEventListener('click', cancelHandler);
    cancelBtn.addEventListener('touchend', cancelHandler);

    // Submit button - with touch support
    const submitBtn = document.getElementById('simple-bug-submit');
    const submitHandler = async function(e) {
        e.preventDefault();
        e.stopPropagation();
        const input = document.getElementById('simple-bug-input');
        const status = document.getElementById('simple-bug-status');
        const description = input.value.trim();

        if (!description) {
            status.textContent = '⚠️ Please describe the bug';
            status.style.color = '#ff4444';
            return;
        }

        // Show submitting
        status.textContent = '📤 Submitting...';
        status.style.color = '#666';

        try {
            // Submit to API
            const response = await fetch('/.netlify/functions/web-bug-report', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    description: description,
                    reporter: localStorage.getItem('workspace_user_name') || 'Anonymous',
                    page: window.location.href
                })
            });

            const result = await response.json();

            if (response.ok && result.issue_url) {
                // Success!
                status.textContent = '✅ Bug submitted!';
                status.style.color = '#00cc66';
                input.value = '';

                // Hide popup after 2 seconds
                setTimeout(() => {
                    bugPopup.style.display = 'none';
                    status.textContent = '';
                }, 2000);
            } else {
                throw new Error(result.error || 'Submission failed');
            }
        } catch (error) {
            // Error - show message
            status.textContent = '❌ Error: ' + error.message;
            status.style.color = '#ff4444';
        }
    };
    submitBtn.addEventListener('click', submitHandler);
    submitBtn.addEventListener('touchend', submitHandler);

    // Submit on Enter key
    document.getElementById('simple-bug-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            submitBtn.click();
        }
    });

    // Hide old broken debuggers
    setTimeout(() => {
        const oldDebuggers = [
            'kindergarten-bug-box',
            'bug-reporter-panel',
            'multi-channel-bug-sidebar',
            'floating-bug-reporter'
        ];

        oldDebuggers.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.style.display = 'none';
            }
        });
    }, 500);
})();
