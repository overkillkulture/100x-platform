"""MODULE #37: TASK SCHEDULER - Cron-like task scheduling"""
import time
import threading
from typing import Callable, List
from dataclasses import dataclass

@dataclass
class ScheduledTask:
    name: str
    func: Callable
    interval: float
    last_run: float = 0
    enabled: bool = True

class TaskScheduler:
    def __init__(self):
        self.tasks: List[ScheduledTask] = []
        self.running = False
        self.thread = None

    def schedule(self, name: str, func: Callable, interval: float):
        """Schedule task to run every interval seconds"""
        task = ScheduledTask(name, func, interval, time.time())
        self.tasks.append(task)
        return task

    def start(self):
        """Start scheduler"""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop scheduler"""
        self.running = False

    def _run(self):
        """Main loop"""
        while self.running:
            now = time.time()
            for task in self.tasks:
                if task.enabled and (now - task.last_run) >= task.interval:
                    try:
                        task.func()
                        task.last_run = now
                    except Exception as e:
                        print(f"Task {task.name} error: {e}")
            time.sleep(0.1)

if __name__ == "__main__":
    scheduler = TaskScheduler()
    scheduler.schedule("greet", lambda: print("Hello!"), interval=2)
    scheduler.start()
    time.sleep(5)
    scheduler.stop()
