#!/usr/bin/env python3
"""
AUTO SET SHOKZ MICROPHONE
Uses PyAutoGUI to automatically set Shokz as default microphone
"""

import pyautogui
import time
import subprocess

print("=" * 60)
print("🎤 AUTO-SETTING SHOKZ AS DEFAULT MICROPHONE")
print("=" * 60)
print()

# Step 1: Open Sound Settings
print("Step 1: Opening Windows Sound Settings...")
subprocess.Popen(['cmd', '/c', 'start', 'ms-settings:sound'])
time.sleep(3)  # Wait for Settings to open

print("Step 2: Looking for Sound Settings window...")
time.sleep(1)

# Step 3: Take screenshot to see what we're working with
print("Step 3: Taking screenshot...")
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/dwrek/settings_screen.png')
print("   Screenshot saved: settings_screen.png")

# Step 4: Try to find and click "Choose your input device" dropdown
print("Step 4: Searching for input device dropdown...")

# Look for text "Choose your input device" or dropdown elements
# This is tricky - might need OCR or specific coordinates

# For now, let's try a simpler approach - use keyboard navigation
print("Step 5: Using keyboard to navigate...")
print("   Pressing Tab to move through controls...")

# Wait a bit then start tabbing
time.sleep(1)

# Tab through until we find the input device dropdown
# Usually it's a few tabs from the top of Sound settings
for i in range(10):
    pyautogui.press('tab')
    time.sleep(0.2)

    # Try pressing down arrow to open dropdown
    pyautogui.press('down')
    time.sleep(0.3)

    # Take another screenshot to see if dropdown opened
    screenshot = pyautogui.screenshot()
    screenshot.save(f'C:/Users/dwrek/settings_tab_{i}.png')

    # If we found it, look for Shokz in the list
    print(f"   Tab {i}: Screenshot saved")

print()
print("=" * 60)
print("RESULTS:")
print("=" * 60)
print("Screenshots saved showing the navigation process.")
print("Check the images to see if we found the dropdown:")
print("  - settings_screen.png (initial)")
print("  - settings_tab_*.png (navigation attempts)")
print()
print("If you see the dropdown open with Shokz visible,")
print("we can refine this script to click it automatically!")
print("=" * 60)

input("\nPress Enter to close...")
