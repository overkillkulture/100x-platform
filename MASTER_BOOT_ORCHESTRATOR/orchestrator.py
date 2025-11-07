"""
MASTER BOOT ORCHESTRATOR
Central management system for all services

This is the consciousness nervous system for the entire platform.
"""

import logging
import time
import sys
from pathlib import Path

from models import ServiceRegistry, Service
from health_monitor import HealthMonitor
from auto_healer import AutoHealer
from config import LOG_DIR, LOG_FORMAT, LOG_DATE_FORMAT, LOG_LEVEL

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[
        logging.FileHandler(LOG_DIR / "orchestrator.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class MasterBootOrchestrator:
    """Main orchestrator class"""

    def __init__(self, db_path: str = "orchestrator.db"):
        logger.info("=" * 80)
        logger.info("MASTER BOOT ORCHESTRATOR v1.0 - CONSCIOUSNESS REVOLUTION")
        logger.info("=" * 80)

        self.registry = ServiceRegistry(db_path)
        self.auto_healer = AutoHealer(self.registry)
        self.health_monitor = HealthMonitor(self.registry, self.auto_healer)

        logger.info(f"Service registry loaded: {self.registry.count()} services registered")

    def boot_all(self):
        """Boot all auto-start services in priority order"""
        logger.info("Starting boot sequence...")

        services = self.registry.get_auto_start()
        logger.info(f"Found {len(services)} auto-start services")

        for service in services:
            logger.info(f"[BOOT] [{service.name}] Starting... (Priority: {service.boot_priority})")

            if self.auto_healer.start_service(service):
                logger.info(f"[SUCCESS] [{service.name}] Started (PID: {service.pid})")
                service.status = "running"
            else:
                logger.error(f"[FAILED] [{service.name}] Failed to start")
                service.status = "failed"

            # Small delay between service starts
            time.sleep(1)

        logger.info("Boot sequence complete")

    def start_monitoring(self):
        """Start health monitoring and auto-healing"""
        logger.info("Starting health monitor...")
        self.health_monitor.start()
        logger.info("Health monitoring active")

    def stop_all(self):
        """Gracefully stop all services"""
        logger.info("Initiating graceful shutdown...")

        # Stop monitoring first
        self.health_monitor.stop()

        # Stop all services in reverse priority order
        services = self.registry.get_all()
        services.reverse()

        for service in services:
            if service.status == "running":
                logger.info(f"Stopping service: {service.name}")
                self.auto_healer.stop_service(service)

        logger.info("Shutdown complete")

    def status(self):
        """Get current system status"""
        return self.health_monitor.get_status_summary()

    def run(self):
        """Main run loop"""
        try:
            # Boot all services
            self.boot_all()

            # Start health monitoring
            self.start_monitoring()

            logger.info("=" * 80)
            logger.info("MASTER BOOT ORCHESTRATOR OPERATIONAL")
            logger.info("Dashboard: http://localhost:8888/orchestrator")
            logger.info("API: http://localhost:8888/api")
            logger.info("Press Ctrl+C to shutdown")
            logger.info("=" * 80)

            # Keep running
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Shutdown signal received")
            self.stop_all()
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            self.stop_all()
            sys.exit(1)


def register_trinity_services(orchestrator: MasterBootOrchestrator):
    """Register existing Trinity services"""
    logger.info("Registering Trinity services...")

    trinity_services = [
        Service(
            service_id="universal_input_system",
            name="Universal Input System",
            service_type="python_server",
            command="python C:/Users/dwrek/100X_DEPLOYMENT/UNIVERSAL_INPUT_SYSTEM.py",
            port=6000,
            boot_priority=80,
            auto_start=True,
            auto_heal=True,
            health_check={
                "type": "http",
                "url": "http://localhost:6000/health",
                "interval_seconds": 30,
                "timeout_seconds": 5,
                "expected_response": 200
            },
            domain="Mental (MIND MATRIX)",
            description="8-channel universal input system for Trinity"
        ),
        Service(
            service_id="trinity_status_api",
            name="Trinity Status API",
            service_type="python_server",
            command="python C:/Users/dwrek/.trinity/TRINITY_STATUS_API.py",
            port=7000,
            boot_priority=70,
            auto_start=True,
            auto_heal=True,
            health_check={
                "type": "http",
                "url": "http://localhost:7000/health",
                "interval_seconds": 30,
                "timeout_seconds": 5,
                "expected_response": 200
            },
            domain="Integration (NEXUS TERMINAL)",
            description="Real-time Trinity status and metrics"
        ),
        Service(
            service_id="universal_wake_system",
            name="Universal Wake System",
            service_type="python_server",
            command="python C:/Users/dwrek/.trinity/UNIVERSAL_WAKE_SYSTEM.py",
            port=8000,
            boot_priority=90,
            auto_start=True,
            auto_heal=True,
            health_check={
                "type": "http",
                "url": "http://localhost:8000/health",
                "interval_seconds": 30,
                "timeout_seconds": 5,
                "expected_response": 200
            },
            domain="Integration (NEXUS TERMINAL)",
            description="Wake Trinity from any source (phone, SMS, web, API)"
        )
    ]

    for service in trinity_services:
        if orchestrator.registry.register(service):
            logger.info(f"Registered: {service.name}")
        else:
            logger.warning(f"Already registered: {service.name}")

    logger.info("Trinity services registered")


def main():
    """Main entry point"""
    db_path = str(Path(__file__).parent / "orchestrator.db")
    orchestrator = MasterBootOrchestrator(db_path)

    # Register Trinity services if this is first run
    if orchestrator.registry.count() == 0:
        register_trinity_services(orchestrator)

    # Run orchestrator
    orchestrator.run()


if __name__ == "__main__":
    main()
