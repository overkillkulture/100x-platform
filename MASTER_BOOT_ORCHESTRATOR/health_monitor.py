"""
MASTER BOOT ORCHESTRATOR - HEALTH MONITOR
Continuous health checking for all registered services
"""

import time
import threading
import subprocess
import requests
import psutil
from datetime import datetime
from typing import Optional, Dict
import logging

from models import Service
from config import (
    DEFAULT_HEALTH_CHECK_INTERVAL,
    DEFAULT_HEALTH_CHECK_TIMEOUT,
    MAX_HEALTH_CHECK_FAILURES
)

logger = logging.getLogger(__name__)


class HealthMonitor:
    """Monitors health of all services"""

    def __init__(self, registry, auto_healer=None):
        self.registry = registry
        self.auto_healer = auto_healer
        self.running = False
        self.monitor_thread = None
        self.service_status = {}  # service_id -> status dict

    def start(self):
        """Start health monitoring thread"""
        if self.running:
            logger.warning("Health monitor already running")
            return

        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Health monitor started")

    def stop(self):
        """Stop health monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Health monitor stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            services = self.registry.get_all()

            for service in services:
                if service.auto_heal:
                    status = self.check_health(service)

                    # Store status
                    self.service_status[service.service_id] = {
                        "status": status,
                        "last_check": datetime.now(),
                        "failures": service.health_check_failures
                    }

                    # Trigger auto-heal if needed
                    if status == "DOWN" and self.auto_healer:
                        logger.error(f"Service {service.name} is DOWN - triggering auto-heal")
                        self.auto_healer.heal_service(service)
                    elif status == "DEGRADED":
                        logger.warning(f"Service {service.name} is DEGRADED")

            # Sleep before next check
            time.sleep(DEFAULT_HEALTH_CHECK_INTERVAL)

    def check_health(self, service: Service) -> str:
        """
        Check service health
        Returns: "UP", "DOWN", "DEGRADED", or "UNKNOWN"
        """
        try:
            health_check = service.health_check
            check_type = health_check.get("type", "process")

            if check_type == "process":
                return self._check_process(service)
            elif check_type == "port":
                return self._check_port(service)
            elif check_type == "http":
                return self._check_http(service)
            elif check_type == "custom":
                return self._check_custom(service)
            else:
                logger.warning(f"Unknown health check type: {check_type}")
                return "UNKNOWN"

        except Exception as e:
            logger.error(f"Health check failed for {service.name}: {e}")
            service.health_check_failures += 1
            return "DOWN"

    def _check_process(self, service: Service) -> str:
        """Check if process is running"""
        if not service.pid:
            return "DOWN"

        try:
            process = psutil.Process(service.pid)
            if process.is_running():
                service.health_check_failures = 0
                return "UP"
            else:
                service.health_check_failures += 1
                return "DOWN"
        except psutil.NoSuchProcess:
            service.health_check_failures += 1
            return "DOWN"

    def _check_port(self, service: Service) -> str:
        """Check if port is listening"""
        if not service.port:
            return "UNKNOWN"

        try:
            # Check if port is listening
            result = subprocess.run(
                ["netstat", "-an"],
                capture_output=True,
                text=True,
                timeout=5
            )

            port_str = f":{service.port}"
            if port_str in result.stdout and "LISTENING" in result.stdout:
                service.health_check_failures = 0
                return "UP"
            else:
                service.health_check_failures += 1
                return "DOWN"

        except Exception as e:
            logger.error(f"Port check failed for {service.name}: {e}")
            service.health_check_failures += 1
            return "DOWN"

    def _check_http(self, service: Service) -> str:
        """Check HTTP endpoint"""
        health_check = service.health_check
        url = health_check.get("url")
        expected_status = health_check.get("expected_response", 200)
        timeout = health_check.get("timeout_seconds", DEFAULT_HEALTH_CHECK_TIMEOUT)

        if not url:
            logger.warning(f"No URL configured for HTTP health check: {service.name}")
            return "UNKNOWN"

        try:
            response = requests.get(url, timeout=timeout)

            if response.status_code == expected_status:
                service.health_check_failures = 0
                return "UP"
            else:
                logger.warning(
                    f"HTTP check for {service.name} returned {response.status_code}, "
                    f"expected {expected_status}"
                )
                service.health_check_failures += 1
                return "DEGRADED"

        except requests.Timeout:
            logger.error(f"HTTP check timeout for {service.name}")
            service.health_check_failures += 1
            return "DEGRADED"
        except requests.ConnectionError:
            logger.error(f"HTTP connection failed for {service.name}")
            service.health_check_failures += 1
            return "DOWN"
        except Exception as e:
            logger.error(f"HTTP check failed for {service.name}: {e}")
            service.health_check_failures += 1
            return "DOWN"

    def _check_custom(self, service: Service) -> str:
        """Run custom health check script"""
        health_check = service.health_check
        check_command = health_check.get("command")

        if not check_command:
            logger.warning(f"No command configured for custom health check: {service.name}")
            return "UNKNOWN"

        try:
            result = subprocess.run(
                check_command,
                shell=True,
                capture_output=True,
                timeout=DEFAULT_HEALTH_CHECK_TIMEOUT
            )

            if result.returncode == 0:
                service.health_check_failures = 0
                return "UP"
            else:
                service.health_check_failures += 1
                return "DOWN"

        except subprocess.TimeoutExpired:
            logger.error(f"Custom health check timeout for {service.name}")
            service.health_check_failures += 1
            return "DEGRADED"
        except Exception as e:
            logger.error(f"Custom health check failed for {service.name}: {e}")
            service.health_check_failures += 1
            return "DOWN"

    def get_status_summary(self) -> Dict:
        """Get summary of all service statuses"""
        services = self.registry.get_all()

        summary = {
            "total": len(services),
            "up": 0,
            "down": 0,
            "degraded": 0,
            "unknown": 0,
            "services": []
        }

        for service in services:
            status_info = self.service_status.get(service.service_id, {})
            status = status_info.get("status", "UNKNOWN")

            if status == "UP":
                summary["up"] += 1
            elif status == "DOWN":
                summary["down"] += 1
            elif status == "DEGRADED":
                summary["degraded"] += 1
            else:
                summary["unknown"] += 1

            summary["services"].append({
                "service_id": service.service_id,
                "name": service.name,
                "status": status,
                "last_check": status_info.get("last_check"),
                "failures": status_info.get("failures", 0),
                "uptime": service.get_uptime_seconds()
            })

        return summary
