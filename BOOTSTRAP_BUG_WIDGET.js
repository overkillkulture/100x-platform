// BOOTSTRAP BUG REPORTER - PROFESSIONAL GRADE, MOBILE-FIRST
// Using real UI framework instead of reinventing the wheel

(function() {
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

    // Create floating bug button
    const bugButton = document.createElement('button');
    bugButton.className = 'btn btn-danger position-fixed bottom-0 end-0 m-3 rounded-circle shadow-lg';
    bugButton.style.cssText = 'width: 60px; height: 60px; z-index: 9999;';
    bugButton.innerHTML = '🐛';
    bugButton.setAttribute('data-bs-toggle', 'modal');
    bugButton.setAttribute('data-bs-target', '#bugModal');

    // Create Bootstrap modal
    const modalHTML = `
    <div class="modal fade" id="bugModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Report a Bug</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="bugDescription" class="form-label">What's broken?</label>
                        <textarea class="form-control" id="bugDescription" rows="4" placeholder="Describe the bug..."></textarea>
                    </div>
                    <div id="bugStatus"></div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-success" id="submitBug">Submit Bug</button>
                </div>
            </div>
        </div>
    </div>
    `;

    // Add to page
    document.body.appendChild(bugButton);
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Wait for Bootstrap to load, then attach handlers
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
                statusDiv.innerHTML = '<div class="alert alert-warning">Please describe the bug</div>';
                return;
            }

            // Show loading
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';

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
                    // Success!
                    statusDiv.innerHTML = '<div class="alert alert-success">✅ Bug submitted to GitHub!</div>';
                    textarea.value = '';

                    // Close modal after 2 seconds
                    setTimeout(() => {
                        const modal = bootstrap.Modal.getInstance(document.getElementById('bugModal'));
                        modal.hide();
                        statusDiv.innerHTML = '';
                    }, 2000);
                } else {
                    throw new Error(result.error || 'Submission failed');
                }
            } catch (error) {
                statusDiv.innerHTML = `<div class="alert alert-danger">❌ Error: ${error.message}</div>`;
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Submit Bug';
            }
        });
    }

    setupHandlers();

    // Hide old broken debuggers
    setTimeout(() => {
        ['kindergarten-bug-box', 'bug-reporter-panel', 'multi-channel-bug-sidebar',
         'floating-bug-reporter', 'simple-bug-button', 'simple-bug-popup'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.style.display = 'none';
        });
    }, 500);
})();
