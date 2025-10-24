/**
 * UNIVERSAL ERROR REPORTER
 * Add to every page to catch and report all errors
 */

(function() {
  'use strict';

  const ERROR_API = '/.netlify/functions/error-monitor';

  // Catch all JavaScript errors
  window.addEventListener('error', function(event) {
    reportError({
      type: 'javascript_error',
      message: event.message,
      stack: event.error ? event.error.stack : null,
      context: {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
      },
      page: window.location.pathname,
      impact: 'single_user'
    });
  });

  // Catch unhandled promise rejections
  window.addEventListener('unhandledrejection', function(event) {
    reportError({
      type: 'promise_rejection',
      message: event.reason ? event.reason.message : 'Unhandled promise rejection',
      stack: event.reason ? event.reason.stack : null,
      context: {
        reason: event.reason
      },
      page: window.location.pathname,
      impact: 'single_user'
    });
  });

  // Manual error reporting
  window.reportError = function(errorData) {
    const user_id = localStorage.getItem('beta_user_pin') || 'anonymous';

    const payload = {
      ...errorData,
      user_id: user_id,
      timestamp: new Date().toISOString()
    };

    // Send to error monitor
    fetch(ERROR_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).catch(err => {
      console.error('Failed to report error:', err);
      // Store locally as fallback
      try {
        const errors = JSON.parse(localStorage.getItem('offline_errors') || '[]');
        errors.push(payload);
        if (errors.length > 50) errors.shift();
        localStorage.setItem('offline_errors', JSON.stringify(errors));
      } catch (e) {
        // Can't even store locally
      }
    });
  };

  // Monitor Araya API failures specifically
  const originalFetch = window.fetch;
  window.fetch = function(...args) {
    return originalFetch.apply(this, args)
      .then(response => {
        // If Araya API fails, report it
        if (args[0].includes('/araya-chat') && !response.ok) {
          reportError({
            type: 'api_failure',
            message: 'Araya API failed',
            context: {
              url: args[0],
              status: response.status
            },
            page: window.location.pathname,
            impact: 'single_user'
          });
        }
        return response;
      })
      .catch(error => {
        // Network error
        if (args[0].includes('/araya-chat')) {
          reportError({
            type: 'api_failure',
            message: 'Araya API network error: ' + error.message,
            context: {
              url: args[0]
            },
            page: window.location.pathname,
            impact: 'single_user'
          });
        }
        throw error;
      });
  };

  console.log('✅ Error monitoring active');

})();
