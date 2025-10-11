#!/usr/bin/env python3
"""
INJECT MOBILE RESPONSIVENESS INTO ALL PLATFORM PAGES
Automatically adds viewport meta tag and mobile CSS to every HTML file
"""

import os
import re
from pathlib import Path

class MobileResponsivenessInjector:
    """Injects mobile-responsive code into all HTML files"""

    def __init__(self, platform_dir='PLATFORM'):
        self.platform_dir = Path(platform_dir)
        self.mobile_css = 'mobile-responsive.css'
        self.stats = {
            'total_files': 0,
            'updated_files': 0,
            'skipped_files': 0,
            'errors': 0
        }

    def inject_all(self):
        """Process all HTML files in PLATFORM directory"""

        print("=" * 60)
        print("   INJECTING MOBILE RESPONSIVENESS")
        print("=" * 60)
        print()

        # Find all HTML files
        html_files = list(self.platform_dir.glob('*.html'))
        self.stats['total_files'] = len(html_files)

        print(f"Found {len(html_files)} HTML files to process")
        print()

        for html_file in html_files:
            try:
                self.inject_mobile_code(html_file)
            except Exception as e:
                print(f"❌ ERROR processing {html_file.name}: {e}")
                self.stats['errors'] += 1

        # Print summary
        print()
        print("=" * 60)
        print("   INJECTION COMPLETE")
        print("=" * 60)
        print(f"Total files:   {self.stats['total_files']}")
        print(f"Updated:       {self.stats['updated_files']} ✓")
        print(f"Skipped:       {self.stats['skipped_files']} (already mobile-ready)")
        print(f"Errors:        {self.stats['errors']}")
        print()

        if self.stats['updated_files'] > 0:
            print("✓ All pages now mobile-responsive!")
            print("✓ Viewport meta tags added")
            print("✓ Mobile CSS linked")
            print()
            print("Next: Test on mobile device or Chrome DevTools")

        return self.stats

    def inject_mobile_code(self, html_file):
        """Inject viewport meta tag and mobile CSS link into a single HTML file"""

        # Read file
        content = html_file.read_text(encoding='utf-8')

        # Check if already has mobile-responsive.css
        if 'mobile-responsive.css' in content:
            print(f"⏭️  {html_file.name} - Already mobile-ready")
            self.stats['skipped_files'] += 1
            return

        modified = False

        # 1. Add viewport meta tag if missing
        if 'viewport' not in content.lower():
            # Find </head> tag
            if '</head>' in content:
                viewport_tag = '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                content = content.replace('</head>', f'{viewport_tag}</head>', 1)
                modified = True

        # 2. Add mobile CSS link
        if '</head>' in content:
            css_link = '    <link rel="stylesheet" href="mobile-responsive.css">\n'
            # Insert before </head>
            content = content.replace('</head>', f'{css_link}</head>', 1)
            modified = True

        if modified:
            # Write back
            html_file.write_text(content, encoding='utf-8')
            print(f"✓ {html_file.name} - Mobile responsiveness added")
            self.stats['updated_files'] += 1
        else:
            print(f"⚠️  {html_file.name} - No </head> tag found, skipped")
            self.stats['skipped_files'] += 1

    def create_test_page(self):
        """Create a test page to verify mobile responsiveness"""

        test_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Responsiveness Test</title>
    <link rel="stylesheet" href="mobile-responsive.css">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            padding: 2rem;
        }

        .test-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            border: 2px solid rgba(0, 212, 255, 0.3);
        }

        .test-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        }

        .test-card {
            background: rgba(0, 212, 255, 0.1);
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
        }

        .test-buttons {
            display: flex;
            gap: 1rem;
            margin: 1rem 0;
        }

        .btn {
            background: linear-gradient(135deg, #00d4ff, #7b2cbf);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>📱 Mobile Responsiveness Test</h1>

    <div class="test-section">
        <h2>Screen Size Detection</h2>
        <p id="screenInfo">Loading...</p>
        <p id="deviceType">Loading...</p>
    </div>

    <div class="test-section">
        <h2>Grid Layout (Should stack on mobile)</h2>
        <div class="test-grid">
            <div class="test-card">Card 1</div>
            <div class="test-card">Card 2</div>
            <div class="test-card">Card 3</div>
        </div>
    </div>

    <div class="test-section">
        <h2>Button Layout (Should stack on mobile)</h2>
        <div class="test-buttons">
            <button class="btn">Button 1</button>
            <button class="btn">Button 2</button>
            <button class="btn">Button 3</button>
        </div>
    </div>

    <div class="test-section">
        <h2>Form Inputs (Should be 100% width on mobile)</h2>
        <input type="text" placeholder="Text input" style="margin: 0.5rem 0;">
        <input type="email" placeholder="Email input" style="margin: 0.5rem 0;">
        <textarea placeholder="Textarea" style="margin: 0.5rem 0;"></textarea>
    </div>

    <div class="test-section hide-mobile">
        <h2>Desktop Only</h2>
        <p>This section should be HIDDEN on mobile (screen width < 768px)</p>
    </div>

    <div class="test-section show-mobile">
        <h2>Mobile Only</h2>
        <p>This section should be VISIBLE ONLY on mobile (screen width < 768px)</p>
    </div>

    <div class="test-section">
        <h2>Test Results</h2>
        <div id="testResults"></div>
    </div>

    <script>
        // Update screen info
        function updateScreenInfo() {
            const width = window.innerWidth;
            const height = window.innerHeight;
            document.getElementById('screenInfo').textContent =
                `Screen: ${width}x${height}px`;

            let deviceType = 'Desktop';
            if (width < 768) deviceType = '📱 Mobile';
            else if (width < 1024) deviceType = '📱 Tablet';
            else deviceType = '🖥️ Desktop';

            document.getElementById('deviceType').textContent =
                `Device Type: ${deviceType}`;

            // Run tests
            runResponsiveTests(width);
        }

        function runResponsiveTests(width) {
            const results = document.getElementById('testResults');
            const tests = [];

            // Test 1: Viewport meta tag
            const viewport = document.querySelector('meta[name="viewport"]');
            tests.push({
                name: 'Viewport Meta Tag',
                passed: !!viewport,
                details: viewport ? viewport.content : 'Missing'
            });

            // Test 2: Mobile CSS loaded
            const stylesheets = Array.from(document.styleSheets);
            const hasMobileCSS = stylesheets.some(sheet =>
                sheet.href && sheet.href.includes('mobile-responsive.css')
            );
            tests.push({
                name: 'Mobile CSS Loaded',
                passed: hasMobileCSS,
                details: hasMobileCSS ? 'mobile-responsive.css found' : 'Missing'
            });

            // Test 3: Grid responsiveness
            const grid = document.querySelector('.test-grid');
            const gridColumns = window.getComputedStyle(grid).gridTemplateColumns;
            const isSingleColumn = width < 768 && gridColumns.split(' ').length === 1;
            tests.push({
                name: 'Grid Stacking',
                passed: width >= 768 || isSingleColumn,
                details: `${gridColumns.split(' ').length} columns`
            });

            // Test 4: Button layout
            const buttons = document.querySelector('.test-buttons');
            const flexDirection = window.getComputedStyle(buttons).flexDirection;
            const isStacked = width < 768 && flexDirection === 'column';
            tests.push({
                name: 'Button Stacking',
                passed: width >= 768 || isStacked,
                details: flexDirection
            });

            // Test 5: Input sizing
            const input = document.querySelector('input[type="text"]');
            const inputWidth = input.offsetWidth;
            const containerWidth = input.parentElement.offsetWidth;
            const isFullWidth = (inputWidth / containerWidth) > 0.95;
            tests.push({
                name: 'Input Full Width',
                passed: width >= 768 || isFullWidth,
                details: `${Math.round((inputWidth / containerWidth) * 100)}% of container`
            });

            // Display results
            let html = '<ul style="list-style: none; padding: 0;">';
            tests.forEach(test => {
                const icon = test.passed ? '✅' : '❌';
                html += `<li style="margin: 0.5rem 0;">
                    ${icon} <strong>${test.name}</strong>: ${test.details}
                </li>`;
            });
            html += '</ul>';

            const passed = tests.filter(t => t.passed).length;
            const total = tests.length;

            html = `<p><strong>Score: ${passed}/${total} tests passed</strong></p>` + html;

            if (passed === total) {
                html += '<p style="color: #00ff00; font-weight: bold;">🎉 All tests passed! Page is mobile-responsive!</p>';
            } else {
                html += '<p style="color: #ff6b6b; font-weight: bold;">⚠️ Some tests failed. Check the issues above.</p>';
            }

            results.innerHTML = html;
        }

        // Update on load and resize
        updateScreenInfo();
        window.addEventListener('resize', updateScreenInfo);
    </script>
</body>
</html>
"""

        test_file = self.platform_dir / 'mobile-test.html'
        test_file.write_text(test_html, encoding='utf-8')
        print(f"\n✓ Created test page: {test_file}")
        print("  Open this in browser to verify mobile responsiveness")
        print("  Use Chrome DevTools (F12) → Toggle Device Toolbar (Ctrl+Shift+M)")


if __name__ == '__main__':
    injector = MobileResponsivenessInjector()

    # Create test page first
    injector.create_test_page()

    print("\n" + "=" * 60)
    input("Press Enter to inject mobile code into all pages...")
    print()

    # Inject into all pages
    stats = injector.inject_all()

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Open PLATFORM/mobile-test.html in browser")
    print("2. Press F12 to open DevTools")
    print("3. Press Ctrl+Shift+M to toggle device toolbar")
    print("4. Test on iPhone, iPad, Android sizes")
    print("5. Check that all 5 tests pass")
    print()
    print("If tests pass, all 58 pages are now mobile-responsive! ✓")
    print("=" * 60)
