"""
MASTER BOOT ORCHESTRATOR - DATA MODELS
Service definitions and database models
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, List

class Service:
    """Service model for Master Boot Orchestrator"""

    def __init__(self,
                 service_id: str,
                 name: str,
                 service_type: str,
                 command: str,
                 port: Optional[int] = None,
                 dependencies: Optional[List[str]] = None,
                 boot_priority: int = 50,
                 auto_start: bool = True,
                 auto_heal: bool = True,
                 health_check: Optional[Dict] = None,
                 domain: str = "Integration",
                 description: str = "",
                 **kwargs):

        self.service_id = service_id
        self.name = name
        self.service_type = service_type
        self.command = command
        self.port = port
        self.dependencies = dependencies or []
        self.boot_priority = boot_priority
        self.auto_start = auto_start
        self.auto_heal = auto_heal
        self.health_check = health_check or {
            "type": "process",
            "interval_seconds": 30,
            "timeout_seconds": 5
        }
        self.domain = domain
        self.description = description

        # Runtime status (not stored in DB)
        self.status = "stopped"  # stopped, starting, running, degraded, failed
        self.pid = None
        self.uptime_start = None
        self.last_health_check = None
        self.health_check_failures = 0

    def to_dict(self) -> Dict:
        """Convert service to dictionary"""
        return {
            "service_id": self.service_id,
            "name": self.name,
            "service_type": self.service_type,
            "command": self.command,
            "port": self.port,
            "dependencies": json.dumps(self.dependencies),
            "boot_priority": self.boot_priority,
            "auto_start": self.auto_start,
            "auto_heal": self.auto_heal,
            "health_check": json.dumps(self.health_check),
            "domain": self.domain,
            "description": self.description,
            "status": self.status,
            "pid": self.pid,
            "uptime_start": self.uptime_start.isoformat() if self.uptime_start else None,
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None,
            "health_check_failures": self.health_check_failures
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Service':
        """Create service from dictionary"""
        dependencies = json.loads(data.get('dependencies', '[]'))
        health_check = json.loads(data.get('health_check', '{}'))

        service = Service(
            service_id=data['service_id'],
            name=data['name'],
            service_type=data['service_type'],
            command=data['command'],
            port=data.get('port'),
            dependencies=dependencies,
            boot_priority=data.get('boot_priority', 50),
            auto_start=data.get('auto_start', True),
            auto_heal=data.get('auto_heal', True),
            health_check=health_check,
            domain=data.get('domain', 'Integration'),
            description=data.get('description', '')
        )

        # Restore runtime status if present
        service.status = data.get('status', 'stopped')
        service.pid = data.get('pid')

        uptime_str = data.get('uptime_start')
        if uptime_str:
            service.uptime_start = datetime.fromisoformat(uptime_str)

        last_check_str = data.get('last_health_check')
        if last_check_str:
            service.last_health_check = datetime.fromisoformat(last_check_str)

        service.health_check_failures = data.get('health_check_failures', 0)

        return service

    def get_uptime_seconds(self) -> Optional[float]:
        """Get service uptime in seconds"""
        if self.uptime_start:
            return (datetime.now() - self.uptime_start).total_seconds()
        return None


class ServiceRegistry:
    """SQLite-based service registry"""

    def __init__(self, db_path: str = "orchestrator.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                service_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                service_type TEXT NOT NULL,
                command TEXT NOT NULL,
                port INTEGER,
                dependencies TEXT,
                boot_priority INTEGER DEFAULT 50,
                auto_start INTEGER DEFAULT 1,
                auto_heal INTEGER DEFAULT 1,
                health_check TEXT,
                domain TEXT,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def register(self, service: Service) -> bool:
        """Register a new service"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO services (
                    service_id, name, service_type, command, port,
                    dependencies, boot_priority, auto_start, auto_heal,
                    health_check, domain, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                service.service_id,
                service.name,
                service.service_type,
                service.command,
                service.port,
                json.dumps(service.dependencies),
                service.boot_priority,
                service.auto_start,
                service.auto_heal,
                json.dumps(service.health_check),
                service.domain,
                service.description
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get(self, service_id: str) -> Optional[Service]:
        """Get service by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM services WHERE service_id = ?", (service_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Service.from_dict(dict(row))
        return None

    def get_all(self) -> List[Service]:
        """Get all services"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM services ORDER BY boot_priority DESC, name")
        rows = cursor.fetchall()
        conn.close()

        return [Service.from_dict(dict(row)) for row in rows]

    def get_auto_start(self) -> List[Service]:
        """Get all auto-start services in priority order"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM services
            WHERE auto_start = 1
            ORDER BY boot_priority DESC, name
        """)
        rows = cursor.fetchall()
        conn.close()

        return [Service.from_dict(dict(row)) for row in rows]

    def update(self, service: Service) -> bool:
        """Update service"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE services SET
                name = ?,
                service_type = ?,
                command = ?,
                port = ?,
                dependencies = ?,
                boot_priority = ?,
                auto_start = ?,
                auto_heal = ?,
                health_check = ?,
                domain = ?,
                description = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE service_id = ?
        """, (
            service.name,
            service.service_type,
            service.command,
            service.port,
            json.dumps(service.dependencies),
            service.boot_priority,
            service.auto_start,
            service.auto_heal,
            json.dumps(service.health_check),
            service.domain,
            service.description,
            service.service_id
        ))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def delete(self, service_id: str) -> bool:
        """Delete service"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM services WHERE service_id = ?", (service_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def get_by_domain(self, domain: str) -> List[Service]:
        """Get services by domain"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM services
            WHERE domain = ?
            ORDER BY boot_priority DESC, name
        """, (domain,))
        rows = cursor.fetchall()
        conn.close()

        return [Service.from_dict(dict(row)) for row in rows]

    def count(self) -> int:
        """Count total services"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM services")
        count = cursor.fetchone()[0]
        conn.close()
        return count
