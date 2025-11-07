"""
MASTER BOOT ORCHESTRATOR - AUTO-HEALER
Automatically restarts failed services
"""

import time
import subprocess
import psutil
import logging
from datetime import datetime

from models import Service
from config import MAX_HEAL_ATTEMPTS, HEAL_RETRY_DELAY, HEAL_BACKOFF_MULTIPLIER

logger = logging.getLogger(__name__)


class AutoHealer:
    """Automatically heals failed services"""

    def __init__(self, registry):
        self.registry = registry
        self.heal_history = {}  # service_id -> list of heal attempts

    def heal_service(self, service: Service) -> bool:
        """
        Attempt to heal a failed service
        Returns True if healed, False if failed after max attempts
        """
        logger.info(f"Starting auto-heal for service: {service.name}")

        # Track heal attempt
        if service.service_id not in self.heal_history:
            self.heal_history[service.service_id] = []

        attempt = 0
        retry_delay = HEAL_RETRY_DELAY

        while attempt < MAX_HEAL_ATTEMPTS:
            attempt += 1
            logger.info(f"Heal attempt {attempt}/{MAX_HEAL_ATTEMPTS} for {service.name}")

            # Record attempt
            self.heal_history[service.service_id].append({
                "attempt": attempt,
                "timestamp": datetime.now(),
                "success": False
            })

            # Stop service (if running)
            self.stop_service(service)

            # Clear locks and cleanup
            self._cleanup_service(service)

            # Wait before restart
            time.sleep(2)

            # Start service
            if self.start_service(service):
                # Verify it's actually working
                time.sleep(3)

                # Basic health check
                if self._verify_started(service):
                    logger.info(f"Successfully healed service: {service.name}")
                    self.heal_history[service.service_id][-1]["success"] = True
                    service.health_check_failures = 0
                    return True

            # Failed to heal, wait before retry with exponential backoff
            if attempt < MAX_HEAL_ATTEMPTS:
                logger.warning(f"Heal attempt {attempt} failed for {service.name}, retrying in {retry_delay}s")
                time.sleep(retry_delay)
                retry_delay *= HEAL_BACKOFF_MULTIPLIER

        # Failed to heal after all attempts
        logger.error(f"Failed to heal {service.name} after {MAX_HEAL_ATTEMPTS} attempts")
        self._alert_human(service)
        return False

    def start_service(self, service: Service) -> bool:
        """Start a service"""
        try:
            logger.info(f"Starting service: {service.name}")

            # Start dependencies first
            if service.dependencies:
                for dep_id in service.dependencies:
                    dep_service = self.registry.get(dep_id)
                    if dep_service and dep_service.status != "running":
                        logger.info(f"Starting dependency: {dep_service.name}")
                        self.start_service(dep_service)

            # Start the service
            process = subprocess.Popen(
                service.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') else 0
            )

            service.pid = process.pid
            service.status = "starting"
            service.uptime_start = datetime.now()

            logger.info(f"Service {service.name} started with PID {service.pid}")
            return True

        except Exception as e:
            logger.error(f"Failed to start service {service.name}: {e}")
            service.status = "failed"
            return False

    def stop_service(self, service: Service) -> bool:
        """Stop a service"""
        try:
            if not service.pid:
                logger.info(f"No PID for service {service.name}, assuming already stopped")
                return True

            logger.info(f"Stopping service: {service.name} (PID: {service.pid})")

            try:
                process = psutil.Process(service.pid)

                # Graceful terminate first
                process.terminate()

                # Wait up to 5 seconds for graceful shutdown
                try:
                    process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    # Force kill if didn't stop gracefully
                    logger.warning(f"Service {service.name} didn't stop gracefully, forcing kill")
                    process.kill()

                service.status = "stopped"
                service.pid = None
                service.uptime_start = None

                logger.info(f"Service {service.name} stopped successfully")
                return True

            except psutil.NoSuchProcess:
                logger.info(f"Process {service.pid} no longer exists")
                service.status = "stopped"
                service.pid = None
                service.uptime_start = None
                return True

        except Exception as e:
            logger.error(f"Failed to stop service {service.name}: {e}")
            return False

    def restart_service(self, service: Service) -> bool:
        """Restart a service"""
        logger.info(f"Restarting service: {service.name}")
        self.stop_service(service)
        time.sleep(2)
        return self.start_service(service)

    def _cleanup_service(self, service: Service):
        """Clean up service artifacts (PID files, locks, etc.)"""
        # This is a placeholder for cleanup logic
        # In a real implementation, you might:
        # - Remove .pid files
        # - Clear lock files
        # - Clean up temp files
        # - Reset port bindings
        pass

    def _verify_started(self, service: Service) -> bool:
        """Basic verification that service started"""
        if not service.pid:
            return False

        try:
            process = psutil.Process(service.pid)
            return process.is_running()
        except psutil.NoSuchProcess:
            return False

    def _alert_human(self, service: Service):
        """Alert human that service couldn't be healed"""
        message = f"⚠️ ALERT: Service {service.name} failed to auto-heal after {MAX_HEAL_ATTEMPTS} attempts"
        logger.critical(message)

        # Desktop notification
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(
                "Master Boot Orchestrator",
                message,
                duration=10,
                threaded=True
            )
        except:
            pass  # Notifications not critical

    def get_heal_history(self, service_id: str = None):
        """Get healing history for service or all services"""
        if service_id:
            return self.heal_history.get(service_id, [])
        return self.heal_history
