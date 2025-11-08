"""
REAL-TIME MONITORING SYSTEM
Monitor all modules, track metrics, generate reports
"""

import psutil
import time
import json
from typing import Dict, List
from dataclasses import dataclass, asdict

@dataclass
class SystemMetrics:
    timestamp: float
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    active_threads: int

@dataclass
class ModuleStatus:
    name: str
    status: str
    last_check: float
    errors: int

class MonitoringSystem:
    def __init__(self):
        self.metrics_history: List[SystemMetrics] = []
        self.module_status: Dict[str, ModuleStatus] = {}
        self.alerts: List[Dict] = []

    def collect_metrics(self) -> SystemMetrics:
        """Collect system metrics"""
        metrics = SystemMetrics(
            timestamp=time.time(),
            cpu_percent=psutil.cpu_percent(interval=0.1),
            memory_percent=psutil.virtual_memory().percent,
            disk_usage_percent=psutil.disk_usage('/').percent,
            active_threads=len(psutil.Process().threads())
        )

        self.metrics_history.append(metrics)

        # Keep last 1000 metrics
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]

        return metrics

    def check_module(self, module_name: str) -> ModuleStatus:
        """Check module health"""
        try:
            # Try to import module
            exec(f"import {module_name}")

            status = ModuleStatus(
                name=module_name,
                status="healthy",
                last_check=time.time(),
                errors=0
            )
        except Exception as e:
            status = ModuleStatus(
                name=module_name,
                status="error",
                last_check=time.time(),
                errors=1
            )
            self.alerts.append({
                'timestamp': time.time(),
                'module': module_name,
                'error': str(e)
            })

        self.module_status[module_name] = status
        return status

    def generate_report(self) -> str:
        """Generate monitoring report"""
        if not self.metrics_history:
            self.collect_metrics()

        latest = self.metrics_history[-1]

        report = "=" * 70 + "\n"
        report += "MONITORING SYSTEM - REAL-TIME STATUS\n"
        report += "=" * 70 + "\n\n"

        report += "SYSTEM METRICS:\n"
        report += f"  CPU Usage: {latest.cpu_percent:.1f}%\n"
        report += f"  Memory Usage: {latest.memory_percent:.1f}%\n"
        report += f"  Disk Usage: {latest.disk_usage_percent:.1f}%\n"
        report += f"  Active Threads: {latest.active_threads}\n\n"

        report += "MODULE STATUS:\n"
        if self.module_status:
            for module, status in self.module_status.items():
                icon = "✅" if status.status == "healthy" else "❌"
                report += f"  {icon} {module}: {status.status}\n"
        else:
            report += "  (No modules checked yet)\n"

        report += "\nALERTS:\n"
        if self.alerts:
            for alert in self.alerts[-5:]:
                report += f"  ⚠️  {alert['module']}: {alert['error'][:50]}\n"
        else:
            report += "  (No alerts)\n"

        report += "\n" + "=" * 70 + "\n"

        return report

    def save_report(self, filepath: str = "monitoring_report.json"):
        """Save monitoring data"""
        data = {
            'metrics': [asdict(m) for m in self.metrics_history[-100:]],
            'modules': {k: asdict(v) for k, v in self.module_status.items()},
            'alerts': self.alerts[-50:]
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    monitor = MonitoringSystem()

    print("Collecting metrics...")
    monitor.collect_metrics()

    print("\nGenerating report...")
    print(monitor.generate_report())

    print("Saving report...")
    monitor.save_report()

    print("✅ Monitoring complete!")
