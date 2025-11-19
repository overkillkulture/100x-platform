"""
FIVERR JOB AUTO-POSTER
Automates posting VA job listing to Fiverr
"""
from playwright.sync_api import sync_playwright
import time

# Load job description
with open('FIVERR_JOB_POST.txt', 'r', encoding='utf-8') as f:
    job_content = f.read()

# Parse job details
lines = job_content.split('\n')
title = "Virtual Assistant for Tech Startup - $400-600/month"
description = job_content.split('DESCRIPTION:')[1].split('REQUIREMENTS:')[0].strip()
requirements = job_content.split('REQUIREMENTS:')[1].split('PREFERRED:')[0].strip()

print("🚀 FIVERR AUTO-POSTER")
print("=" * 60)
print("\n✅ Job loaded from FIVERR_JOB_POST.txt")
print(f"Title: {title}")
print("\n⏳ Opening Fiverr...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Go to Fiverr job posting
    page.goto('https://www.fiverr.com/start_selling')

    print("\n⚠️  ACTION NEEDED:")
    print("Please log into Fiverr in the browser window.")
    print("Once logged in, press ENTER here to continue...")
    input()

    print("\n✅ Logged in! Navigating to job posting...")

    # Navigate to "I'm hiring" section
    try:
        page.goto('https://www.fiverr.com/hiring')
        time.sleep(2)

        # Click "Post a Request" or similar
        post_button = page.locator('text=Post a request').first
        if post_button.is_visible():
            post_button.click()
            time.sleep(2)

        # Fill in job title
        title_input = page.locator('input[name="title"], input[placeholder*="title" i]').first
        if title_input.is_visible():
            title_input.fill(title)
            print(f"✅ Filled title: {title[:50]}...")

        # Fill in description
        desc_input = page.locator('textarea[name="description"], textarea[placeholder*="describe" i]').first
        if desc_input.is_visible():
            full_description = f"{description}\n\n{requirements}"
            desc_input.fill(full_description)
            print(f"✅ Filled description ({len(full_description)} characters)")

        # Budget selection (if available)
        try:
            budget_select = page.locator('select[name="budget"]').first
            if budget_select.is_visible():
                budget_select.select_option(label="$500-$1000")
                print("✅ Set budget range")
        except:
            pass

        print("\n⚠️  MANUAL STEP:")
        print("Please review the form and click Submit when ready.")
        print("Press ENTER when done...")
        input()

        print("\n✅ Job posting process complete!")

    except Exception as e:
        print(f"\n⚠️  Could not fully automate: {e}")
        print("\nFiverr page is open. Please complete manually:")
        print("1. Navigate to job posting section")
        print("2. Copy title and description from FIVERR_JOB_POST.txt")
        print("3. Submit the job")
        print("\nPress ENTER to close browser...")
        input()

    browser.close()

print("\n✅ DONE!")
print("Check Fiverr to verify job was posted.")
