# MODULE #37: TASK SCHEDULER
Cron-like task scheduling. Run functions at intervals.
```python
from scheduler import TaskScheduler
scheduler = TaskScheduler()
scheduler.schedule("backup", backup_func, interval=3600)
scheduler.start()
```
**#37 COMPLETE** ✅
