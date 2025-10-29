// BOOTSTRAP BUG REPORTER - PROFESSIONAL GRADE, MOBILE-FIRST
// AGGRESSIVELY REMOVES ALL OLD DEBUGGERS

(function() {
    // FIRST: Kill all old debuggers immediately (before anything else)
    const killOldDebuggers = () => {
        const oldDebuggerSelectors = [
            // Known old debuggers
            '#kindergarten-bug-box',
            '#bug-reporter-panel',
            '#multi-channel-bug-sidebar',
            '#floating-bug-reporter',
            '#simple-bug-button',
            '#simple-bug-popup',
            // Pattern-based cleanup
            '[class*="bug-reporter"]',
            '[class*="bug-panel"]',
            '[class*="bug-sidebar"]',
            '[id*="bug-report"]',
            '[id*="bug-box"]',
            '[id*="found-bug"]',
            '[class*="found-bug"]',
            // SOS button (old emergency system)
            '[id*="sos"]',
            '[class*="sos"]',
            // Generic bug UI elements
            'div[style*="position: fixed"][style*="bottom"]',
            'button[style*="position: fixed"][style*="bottom: 20px"]',
            'div[style*="background: white"][style*="padding: 20px"]'
        ];

        oldDebuggerSelectors.forEach(selector => {
            try {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    // Don't delete our Bootstrap modal or bug button
                    if (el &&
                        el.id !== 'bugModal' &&
                        !el.closest('#bugModal') &&
                        !el.hasAttribute('data-bs-toggle') &&
                        el.innerHTML !== '🐛') {
                        el.remove(); // DELETE, not hide
                    }
                });
            } catch (e) {}
        });
    };

    // Kill immediately and keep killing
    killOldDebuggers();
    setInterval(killOldDebuggers, 500);

    // Add Bootstrap CSS if not already loaded
    if (!document.querySelector('link[href*="bootstrap"]')) {
        const bootstrapCSS = document.createElement('link');
        bootstrapCSS.rel = 'stylesheet';
        bootstrapCSS.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css';
        document.head.appendChild(bootstrapCSS);
    }

    // Add Bootstrap JS if not already loaded
    if (!window.bootstrap) {
        const bootstrapJS = document.createElement('script');
        bootstrapJS.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js';
        document.head.appendChild(bootstrapJS);
    }

    // Create floating bug button - SMALL on mobile
    const bugButton = document.createElement('button');
    bugButton.className = 'btn btn-danger position-fixed bottom-0 end-0 m-2 rounded-circle shadow';
    bugButton.style.cssText = 'width: 50px; height: 50px; z-index: 99999; font-size: 20px; padding: 0;';
    bugButton.innerHTML = '🐛';
    bugButton.setAttribute('data-bs-toggle', 'modal');
    bugButton.setAttribute('data-bs-target', '#bugModal');

    // Create Bootstrap modal - MOBILE OPTIMIZED (fits screen properly)
    const modalHTML = `
    <style>
        /* FORCE modal hidden by default */
        #bugModal {
            display: none !important;
        }
        #bugModal.show {
            display: block !important;
        }

        #bugModal .modal-dialog {
            max-width: 90%;
            margin: 1rem auto;
        }
        #bugModal .modal-content {
            width: 100%;
            max-width: 100%;
        }
        #bugModal textarea {
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
        }
        @media (max-width: 576px) {
            #bugModal .modal-dialog {
                max-width: 95%;
                margin: 0.5rem auto;
            }
        }
    </style>
    <div class="modal fade" id="bugModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header py-2">
                    <h6 class="modal-title m-0">Report Bug</h6>
                    <button type="button" class="btn-close btn-close-sm" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body p-3">
                    <textarea class="form-control form-control-sm" id="bugDescription" rows="3" placeholder="What's broken?" style="width: 100%; max-width: 100%;"></textarea>
                    <div id="bugStatus" class="mt-2"></div>
                </div>
                <div class="modal-footer p-2">
                    <button type="button" class="btn btn-sm btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-sm btn-success" id="submitBug">Submit</button>
                </div>
            </div>
        </div>
    </div>
    `;

    // Add to page
    document.body.appendChild(bugButton);
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Setup handlers
    function setupHandlers() {
        const submitBtn = document.getElementById('submitBug');
        const statusDiv = document.getElementById('bugStatus');
        const textarea = document.getElementById('bugDescription');

        if (!submitBtn || !window.bootstrap) {
            setTimeout(setupHandlers, 100);
            return;
        }

        submitBtn.addEventListener('click', async function() {
            const description = textarea.value.trim();

            if (!description) {
                statusDiv.innerHTML = '<small class="text-warning">Please describe the bug</small>';
                return;
            }

            // Show loading
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';

            try {
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
                    statusDiv.innerHTML = '<small class="text-success">✅ Submitted!</small>';
                    textarea.value = '';

                    setTimeout(() => {
                        const modal = bootstrap.Modal.getInstance(document.getElementById('bugModal'));
                        modal.hide();
                        statusDiv.innerHTML = '';
                    }, 1500);
                } else {
                    throw new Error(result.error || 'Failed');
                }
            } catch (error) {
                statusDiv.innerHTML = `<small class="text-danger">❌ Error</small>`;
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Submit';
            }
        });
    }

    setupHandlers();
})();
