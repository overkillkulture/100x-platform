"""
Add mobile-responsive.css to pages missing it
"""

import re

files_to_fix = [
    '3-min-boost.html',
    'arg-assembly.html',
    'bug-test-demo.html',
    'character-matrix.html',
    'debugger-leaderboard.html',
    'meritocracy-dashboard.html',
    'trinity-cockpit.html'
]

base_path = 'C:/Users/dwrek/100X_DEPLOYMENT/PLATFORM/'
mobile_css_link = '    <link rel="stylesheet" href="mobile-responsive.css">'

for filename in files_to_fix:
    filepath = base_path + filename

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has mobile CSS (shouldn't, but safety check)
        if 'mobile-responsive.css' in content:
            print(f'✅ {filename} - Already has mobile CSS')
            continue

        # Find the </head> tag and insert before it
        if '</head>' in content:
            # Insert mobile CSS link right before </head>
            content = content.replace('</head>', f'{mobile_css_link}\n</head>')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f'✅ {filename} - Added mobile CSS')
        else:
            print(f'❌ {filename} - No </head> tag found')

    except Exception as e:
        print(f'❌ {filename} - Error: {e}')

print('\n🎉 Mobile CSS injection complete!')
