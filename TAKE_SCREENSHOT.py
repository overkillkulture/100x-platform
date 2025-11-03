#!/usr/bin/env python3
"""
Quick Screenshot Tool - Takes screenshot of entire screen or active window
"""

import os
from datetime import datetime
from PIL import ImageGrab

def take_screenshot(output_path=None):
    """Take a screenshot and save it"""

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"screenshot_{timestamp}.png"

    # Take screenshot
    screenshot = ImageGrab.grab()

    # Save it
    screenshot.save(output_path)

    print(f"✅ Screenshot saved: {output_path}")
    print(f"📁 Full path: {os.path.abspath(output_path)}")

    return os.path.abspath(output_path)

if __name__ == "__main__":
    import sys

    # Get output path from command line or use default
    output = sys.argv[1] if len(sys.argv) > 1 else None

    # Take and save screenshot
    path = take_screenshot(output)

    print(f"\n🎯 Screenshot ready for Claude to read!")
    print(f"Tell Claude: 'Read the file at {path}'")
