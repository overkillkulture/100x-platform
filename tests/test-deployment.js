// 100X Platform - Automated Deployment Tests
// These tests run automatically before each deployment goes live

const fs = require('fs');
const path = require('path');

// Test results tracker
const results = {
    passed: 0,
    failed: 0,
    tests: []
};

// Color output for terminal
const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    reset: '\x1b[0m',
    cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function test(name, fn) {
    try {
        fn();
        results.passed++;
        results.tests.push({ name, status: 'PASS' });
        log(`✓ ${name}`, 'green');
    } catch (error) {
        results.failed++;
        results.tests.push({ name, status: 'FAIL', error: error.message });
        log(`✗ ${name}`, 'red');
        log(`  Error: ${error.message}`, 'red');
    }
}

function assert(condition, message) {
    if (!condition) {
        throw new Error(message || 'Assertion failed');
    }
}

function fileExists(filePath) {
    return fs.existsSync(path.join(__dirname, '..', filePath));
}

function fileContains(filePath, searchString) {
    const fullPath = path.join(__dirname, '..', filePath);
    if (!fs.existsSync(fullPath)) {
        throw new Error(`File not found: ${filePath}`);
    }
    const content = fs.readFileSync(fullPath, 'utf8');
    return content.includes(searchString);
}

function validateHTML(filePath) {
    const fullPath = path.join(__dirname, '..', filePath);
    const content = fs.readFileSync(fullPath, 'utf8');

    // Basic HTML validation checks
    assert(content.includes('<!DOCTYPE html>'), 'Missing DOCTYPE declaration');
    assert(content.includes('<html'), 'Missing opening html tag');
    assert(content.includes('</html>'), 'Missing closing html tag');
    assert(content.includes('<head'), 'Missing head section');
    assert(content.includes('<body'), 'Missing body section');
    assert(content.includes('<title>'), 'Missing title tag');
}

function checkLinks(filePath) {
    const fullPath = path.join(__dirname, '..', filePath);
    const content = fs.readFileSync(fullPath, 'utf8');

    // Find all relative links
    const linkRegex = /href=["'](?!http|https|mailto|tel|#)([^"']+)["']/g;
    const matches = [...content.matchAll(linkRegex)];

    const brokenLinks = [];
    matches.forEach(match => {
        const link = match[1];
        // Skip anchors and protocol links
        if (link.startsWith('#') || link.startsWith('http')) return;

        const linkedFile = path.join(path.dirname(fullPath), link);
        if (!fs.existsSync(linkedFile)) {
            brokenLinks.push(link);
        }
    });

    assert(brokenLinks.length === 0,
           `Broken links found: ${brokenLinks.join(', ')}`);
}

// ==========================================
// TEST SUITE: CRITICAL FILES EXIST
// ==========================================

log('\n🧪 Running Critical Files Tests...', 'cyan');

test('index.html exists', () => {
    assert(fileExists('index.html'), 'index.html not found');
});

test('dashboard.html exists', () => {
    assert(fileExists('dashboard.html'), 'dashboard.html not found');
});

test('success.html exists', () => {
    assert(fileExists('success.html'), 'success.html not found');
});

test('2FA tutorial exists', () => {
    assert(fileExists('2fa-setup-tutorial.html'), '2fa-setup-tutorial.html not found');
});

test('TODO Master exists', () => {
    assert(fileExists('PLATFORM/todo-master.html'), 'TODO Master not found');
});

// ==========================================
// TEST SUITE: HTML VALIDATION
// ==========================================

log('\n🧪 Running HTML Validation Tests...', 'cyan');

test('index.html has valid HTML structure', () => {
    validateHTML('index.html');
});

test('dashboard.html has valid HTML structure', () => {
    validateHTML('dashboard.html');
});

test('success.html has valid HTML structure', () => {
    validateHTML('success.html');
});

test('2FA tutorial has valid HTML structure', () => {
    validateHTML('2fa-setup-tutorial.html');
});

// ==========================================
// TEST SUITE: CONTENT VERIFICATION
// ==========================================

log('\n🧪 Running Content Verification Tests...', 'cyan');

test('index.html shows 100X branding', () => {
    assert(fileContains('index.html', '100X'), 'Missing 100X branding');
    assert(fileContains('index.html', 'BUILDER PLATFORM') ||
           fileContains('index.html', 'Builder Platform'),
           'Missing platform name');
});

test('index.html has system cards', () => {
    assert(fileContains('index.html', 'TODO Master') ||
           fileContains('index.html', 'todo-master'),
           'TODO Master not mentioned');
});

test('success.html has dashboard link', () => {
    assert(fileContains('success.html', 'dashboard.html'),
           'No link to dashboard found');
});

test('2FA tutorial has app store links', () => {
    assert(fileContains('2fa-setup-tutorial.html', 'apps.apple.com'),
           'Missing App Store link');
    assert(fileContains('2fa-setup-tutorial.html', 'play.google.com'),
           'Missing Play Store link');
});

test('2FA tutorial has clear instructions', () => {
    assert(fileContains('2fa-setup-tutorial.html', 'Download an Authenticator App'),
           'Missing download instructions');
    assert(fileContains('2fa-setup-tutorial.html', 'Scan'),
           'Missing scan instructions');
});

// ==========================================
// TEST SUITE: LINK VALIDATION
// ==========================================

log('\n🧪 Running Link Validation Tests...', 'cyan');

test('index.html links are valid', () => {
    checkLinks('index.html');
});

test('dashboard.html links are valid', () => {
    checkLinks('dashboard.html');
});

test('success.html links are valid', () => {
    checkLinks('success.html');
});

// ==========================================
// TEST SUITE: CONFIGURATION
// ==========================================

log('\n🧪 Running Configuration Tests...', 'cyan');

test('netlify.toml exists', () => {
    assert(fileExists('netlify.toml'), 'netlify.toml configuration not found');
});

test('package.json exists', () => {
    assert(fileExists('package.json'), 'package.json not found');
});

// ==========================================
// TEST SUITE: SECURITY
// ==========================================

log('\n🧪 Running Security Tests...', 'cyan');

test('No hardcoded API keys in HTML files', () => {
    const files = ['index.html', 'dashboard.html', 'success.html'];
    files.forEach(file => {
        if (fileExists(file)) {
            const content = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
            assert(!content.includes('apiKey'),
                   `Possible hardcoded API key found in ${file}`);
            assert(!content.includes('api_key'),
                   `Possible hardcoded API key found in ${file}`);
        }
    });
});

test('No sensitive data in production files', () => {
    const files = ['index.html', 'dashboard.html', 'success.html'];
    files.forEach(file => {
        if (fileExists(file)) {
            const content = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
            assert(!content.match(/password\s*=\s*["'][^"']+["']/),
                   `Hardcoded password found in ${file}`);
            assert(!content.match(/secret\s*=\s*["'][^"']+["']/),
                   `Hardcoded secret found in ${file}`);
        }
    });
});

// ==========================================
// RESULTS SUMMARY
// ==========================================

log('\n' + '='.repeat(50), 'cyan');
log('TEST RESULTS SUMMARY', 'cyan');
log('='.repeat(50), 'cyan');

log(`\nTotal Tests: ${results.passed + results.failed}`);
log(`Passed: ${results.passed}`, 'green');
log(`Failed: ${results.failed}`, results.failed > 0 ? 'red' : 'green');

if (results.failed > 0) {
    log('\n❌ DEPLOYMENT BLOCKED - Tests failed!', 'red');
    log('Fix the errors above before deploying.\n', 'yellow');
    process.exit(1);
} else {
    log('\n✅ ALL TESTS PASSED - Deployment approved!', 'green');
    log('Site is ready to go live.\n', 'green');
    process.exit(0);
}
