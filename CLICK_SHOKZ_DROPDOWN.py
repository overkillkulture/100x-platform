#!/usr/bin/env python3
"""
CLICK SHOKZ DROPDOWN - Precision clicking
Finds and clicks the microphone dropdown, then selects Shokz
"""

import pyautogui
import time

print("=" * 60)
print("🎤 CLICKING MICROPHONE DROPDOWN")
print("=" * 60)
print()

# Give user time to see Sound Settings window
print("Make sure Sound Settings window is open and visible!")
print("Starting in 3 seconds...")
time.sleep(3)

# Take screenshot to analyze
print("Taking screenshot...")
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/dwrek/before_click.png')

# Look for "Microphone Array" text on screen
print("Searching for 'Microphone Array' dropdown...")
try:
    # Try to locate the text "Microphone Array"
    location = pyautogui.locateOnScreen('C:/Users/dwrek/before_click.png', confidence=0.8)
    if location:
        print(f"Found at: {location}")
except Exception as e:
    print(f"Auto-locate didn't work: {e}")

# Manual approach - click at approximate coordinates
# Based on the screenshot, the "Microphone Array" dropdown is around:
# - Left side of Settings window
# - Under "Input" heading
# - The dropdown button with arrow

print("\nAttempting to click microphone dropdown...")
print("Method: Click on the dropdown arrow next to 'Microphone Array'")

# Get screen size
screen_width, screen_height = pyautogui.size()
print(f"Screen size: {screen_width}x{screen_height}")

# From the screenshot, Settings window is on the left
# Input section is in the middle of the window
# Dropdown is around x=580, y=478 (from the screenshot)

# Click the dropdown button (the arrow on the right side)
click_x = 577  # Right side of the dropdown
click_y = 478  # Vertical center of "Microphone Array" row

print(f"Clicking at coordinates: ({click_x}, {click_y})")
pyautogui.click(click_x, click_y)

time.sleep(1)

# Take screenshot after click
print("Taking screenshot after click...")
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/dwrek/after_dropdown_click.png')

# Now the dropdown should be open
# Look for "Headset" text and click it
print("\nDropdown should be open now!")
print("Looking for 'Headset (OpenRun Pro by Shokz)' option...")

# The dropdown items appear below the current selection
# Shokz headset is likely first or second in the list
# Click a bit below the current selection

# Wait a moment for dropdown animation
time.sleep(0.5)

# Try clicking on the first item in dropdown
# Usually around 40-50 pixels below the dropdown button
click_y_dropdown_item = click_y + 45

print(f"Clicking first dropdown item at: ({click_x}, {click_y_dropdown_item})")
pyautogui.click(click_x, click_y_dropdown_item)

time.sleep(1)

# Take final screenshot
print("Taking final screenshot...")
screenshot = pyautogui.screenshot()
screenshot.save('C:/Users/dwrek/after_selection.png')

print()
print("=" * 60)
print("DONE!")
print("=" * 60)
print("Check these screenshots:")
print("  1. before_click.png - Initial state")
print("  2. after_dropdown_click.png - Dropdown opened")
print("  3. after_selection.png - After selecting Shokz")
print()
print("If Shokz is now selected, SUCCESS!")
print("If not, we can adjust the click coordinates and try again.")
print("=" * 60)
