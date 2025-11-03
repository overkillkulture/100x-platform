"""
Quick script to log completed work to brain
"""
import sys
sys.path.insert(0, 'C:/Users/dwrek/100X_DEPLOYMENT')
from SIMPLE_BRAIN_SYSTEM import SimpleBrain

brain = SimpleBrain()

# Log all completed tasks
tasks = [
    ("Deploy Music Domain landing page ($29.99/mo)", "https://conciousnessrevolution.io/music-domain.html"),
    ("Create 50% Investment Offer page", "https://conciousnessrevolution.io/invest-50-percent.html"),
    ("Deploy Education Domain landing page ($39.99/mo)", "https://conciousnessrevolution.io/education-domain.html"),
    ("Deploy Intelligence Domain landing page ($49.99/mo)", "https://conciousnessrevolution.io/intelligence-domain.html"),
    ("Deploy Security Domain landing page ($59.99/mo)", "https://conciousnessrevolution.io/security-domain.html"),
]

for task_name, url in tasks:
    brain.log_task(
        task_name=task_name,
        status="COMPLETED",
        result=f"Live at {url}",
        duration=None,
        files_created=[url]
    )
    print(f"✅ Logged: {task_name}")

# Add current priorities
brain.add_priority(
    task="Fiverr job posting ready - needs manual post",
    assigned_to="Commander",
    deadline="NOW"
)

brain.add_priority(
    task="5 landing pages deployed - ready for marketing",
    assigned_to="Commander",
    deadline="NOW"
)

# Report status
brain.report_status()

# Save dashboard
brain.save_dashboard()

print("\n✅ ALL WORK LOGGED TO BRAIN")
print(f"Dashboard: C:/Users/dwrek/.consciousness/brain/dashboard.html")
