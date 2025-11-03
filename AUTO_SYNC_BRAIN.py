"""
AUTO SYNC BRAIN - Report status to brain every 5 minutes
Keeps central nervous system updated with real-time computer status

Created: November 1, 2025
By: C1 Mechanic (Trinity Execution)
"""

import sys
import time
from datetime import datetime

# Add path for brain system
sys.path.insert(0, 'C:/Users/dwrek/100X_DEPLOYMENT')
from SIMPLE_BRAIN_SYSTEM import SimpleBrain

def auto_sync_loop():
    """Run continuous sync loop - report to brain every 5 minutes"""

    brain = SimpleBrain()

    print("=" * 60)
    print("⚡ AUTO-SYNC BRAIN SYSTEM STARTED ⚡")
    print("=" * 60)
    print(f"Computer ID: {brain.computer_id}")
    print(f"Brain Location: {brain.brain_dir}")
    print(f"Sync Interval: 5 minutes")
    print(f"Dashboard: {brain.brain_dir}/dashboard.html")
    print("=" * 60)
    print()

    sync_count = 0

    while True:
        try:
            sync_count += 1
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Report status to brain
            brain.report_status()

            # Get any new priorities from Commander
            priorities = brain.get_priorities()
            pending = [p for p in priorities if p.get('status') == 'PENDING']

            print(f"[{now}] Sync #{sync_count} - Brain updated")

            if pending:
                print(f"  📋 {len(pending)} pending priorities:")
                for p in pending:
                    print(f"     - {p.get('task')}")
            else:
                print(f"  ✅ No pending priorities")

            # Log successful sync
            brain.log_task(
                task_name=f"Auto-sync #{sync_count}",
                status="COMPLETED",
                duration="instant",
                result="Brain updated successfully"
            )

            # Wait 5 minutes
            print(f"  ⏳ Next sync in 5 minutes...\n")
            time.sleep(300)  # 5 minutes = 300 seconds

        except KeyboardInterrupt:
            print("\n\n🛑 Auto-sync stopped by user")
            brain.log_task(
                task_name="Auto-sync shutdown",
                status="STOPPED",
                result=f"Ran {sync_count} sync cycles"
            )
            break

        except Exception as e:
            print(f"❌ Sync error: {e}")
            brain.log_error(
                error_type="Auto-sync error",
                message=str(e),
                context=f"Sync cycle #{sync_count}"
            )
            # Wait 1 minute on error, then retry
            time.sleep(60)

if __name__ == "__main__":
    auto_sync_loop()
