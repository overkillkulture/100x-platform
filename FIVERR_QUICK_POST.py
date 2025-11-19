"""
FIVERR QUICK POST - Copy job to clipboard
"""
import pyperclip
import webbrowser
import time

# Read job posting
with open('FIVERR_JOB_POST.txt', 'r', encoding='utf-8') as f:
    job_text = f.read()

print("🚀 FIVERR QUICK POST")
print("=" * 60)

# Copy to clipboard
try:
    pyperclip.copy(job_text)
    print("✅ Job description copied to clipboard!")
except:
    print("⚠️  Install pyperclip: pip install pyperclip")
    print("For now, copy manually from FIVERR_JOB_POST.txt")

# Open Fiverr
print("\n⏳ Opening Fiverr in 3 seconds...")
time.sleep(3)

webbrowser.open('https://www.fiverr.com/start_selling')

print("\n" + "=" * 60)
print("📋 INSTRUCTIONS:")
print("=" * 60)
print("1. Log into Fiverr")
print("2. Navigate to 'Requests' or 'Post a Job'")
print("3. Paste the job description (Ctrl+V)")
print("4. Review and submit")
print("\n✅ Job text is in your clipboard ready to paste!")
print("=" * 60)

input("\nPress ENTER to close...")
