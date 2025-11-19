// CONSOLE LOGGER - Captures all console logs for Claude to read
// Inject this into any page to stream console output

(function() {
    const logs = [];
    const maxLogs = 100;

    // Override console methods
    const originalLog = console.log;
    const originalError = console.error;
    const originalWarn = console.warn;
    const originalInfo = console.info;

    function captureLog(type, args) {
        const timestamp = new Date().toISOString();
        const message = Array.from(args).map(arg => {
            if (typeof arg === 'object') {
                try {
                    return JSON.stringify(arg, null, 2);
                } catch (e) {
                    return String(arg);
                }
            }
            return String(arg);
        }).join(' ');

        logs.push({ timestamp, type, message });

        // Keep only last 100 logs
        if (logs.length > maxLogs) {
            logs.shift();
        }

        // Save to localStorage so Claude can read it
        localStorage.setItem('claude_console_logs', JSON.stringify(logs));

        // Also send to backend if available
        try {
            fetch('/.netlify/functions/console-log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ timestamp, type, message })
            }).catch(() => {}); // Ignore errors
        } catch (e) {}
    }

    console.log = function(...args) {
        captureLog('log', args);
        originalLog.apply(console, args);
    };

    console.error = function(...args) {
        captureLog('error', args);
        originalError.apply(console, args);
    };

    console.warn = function(...args) {
        captureLog('warn', args);
        originalWarn.apply(console, args);
    };

    console.info = function(...args) {
        captureLog('info', args);
        originalInfo.apply(console, args);
    };

    // Capture unhandled errors
    window.addEventListener('error', (event) => {
        captureLog('error', [`Uncaught error: ${event.message}`, `at ${event.filename}:${event.lineno}:${event.colno}`]);
    });

    // Capture unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
        captureLog('error', [`Unhandled promise rejection: ${event.reason}`]);
    });

    console.log('🤖 Claude Console Logger Active - All logs being captured');

    // Expose function to get logs
    window.getConsoleLogs = function() {
        return JSON.parse(localStorage.getItem('claude_console_logs') || '[]');
    };

    // Expose function to clear logs
    window.clearConsoleLogs = function() {
        logs.length = 0;
        localStorage.removeItem('claude_console_logs');
        console.log('Console logs cleared');
    };
})();
