"""MODULE #55: CONFIGURATION MANAGER - Distributed config for 6 AI instances"""
import json
import time
import threading
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field

@dataclass
class ConfigValue:
    key: str
    value: Any
    version: int
    updated_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

class ConfigurationManager:
    """Centralized configuration management for distributed system"""

    def __init__(self, config_id: str = "default"):
        self.config_id = config_id
        self.config: Dict[str, ConfigValue] = {}
        self.lock = threading.RLock()

        # Watchers
        self.watchers: Dict[str, List[Callable]] = {}

        # Metrics
        self.metrics = {
            'config_keys': 0,
            'updates': 0,
            'reads': 0,
            'watchers': 0
        }

    def set(self, key: str, value: Any, metadata: Dict[str, Any] = None):
        """Set configuration value"""
        with self.lock:
            if key in self.config:
                version = self.config[key].version + 1
            else:
                version = 1
                self.metrics['config_keys'] += 1

            config_val = ConfigValue(
                key=key,
                value=value,
                version=version,
                metadata=metadata or {}
            )

            self.config[key] = config_val
            self.metrics['updates'] += 1

            # Notify watchers
            self._notify_watchers(key, value)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        with self.lock:
            self.metrics['reads'] += 1

            if key in self.config:
                return self.config[key].value

            return default

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        with self.lock:
            return {key: cfg.value for key, cfg in self.config.items()}

    def delete(self, key: str) -> bool:
        """Delete configuration key"""
        with self.lock:
            if key in self.config:
                del self.config[key]
                self.metrics['config_keys'] -= 1
                return True

            return False

    def watch(self, key: str, callback: Callable[[str, Any], None]):
        """Watch for changes to a key"""
        with self.lock:
            if key not in self.watchers:
                self.watchers[key] = []

            self.watchers[key].append(callback)
            self.metrics['watchers'] += 1

    def unwatch(self, key: str, callback: Callable):
        """Stop watching a key"""
        with self.lock:
            if key in self.watchers and callback in self.watchers[key]:
                self.watchers[key].remove(callback)
                self.metrics['watchers'] -= 1

    def _notify_watchers(self, key: str, value: Any):
        """Notify watchers of config change"""
        if key in self.watchers:
            for callback in self.watchers[key]:
                try:
                    callback(key, value)
                except Exception as e:
                    print(f"Watcher error: {e}")

    def export_json(self, filepath: str):
        """Export configuration to JSON"""
        with self.lock:
            data = {
                'config_id': self.config_id,
                'timestamp': time.time(),
                'config': {key: cfg.value for key, cfg in self.config.items()}
            }

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)

    def import_json(self, filepath: str):
        """Import configuration from JSON"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        with self.lock:
            for key, value in data.get('config', {}).items():
                self.set(key, value)

    def get_version(self, key: str) -> Optional[int]:
        """Get version of a config key"""
        with self.lock:
            if key in self.config:
                return self.config[key].version
            return None

    def get_metrics(self) -> Dict[str, Any]:
        """Get configuration metrics"""
        return dict(self.metrics)


if __name__ == "__main__":
    print("⚙️  MODULE #55: CONFIGURATION MANAGER")
    print("=" * 60)

    config = ConfigurationManager("ai-system")

    print("✅ Configuration manager created")

    # Set configuration
    print("\n📝 Setting configuration...")
    config.set("instances.count", 6)
    config.set("instances.computers", ["A", "B", "C"])
    config.set("sync.interval", 30)
    config.set("heartbeat.timeout", 60)
    config.set("figure8.enabled", True)

    print(f"   Set 5 configuration keys")

    # Get values
    print("\n📖 Reading configuration...")
    print(f"   instances.count = {config.get('instances.count')}")
    print(f"   sync.interval = {config.get('sync.interval')}")
    print(f"   figure8.enabled = {config.get('figure8.enabled')}")

    # Watch for changes
    print("\n👁️  Setting up watchers...")

    changes_detected = []

    def on_config_change(key, value):
        changes_detected.append((key, value))
        print(f"   Config changed: {key} = {value}")

    config.watch("sync.interval", on_config_change)
    config.watch("figure8.enabled", on_config_change)

    # Update values
    print("\n🔄 Updating configuration...")
    config.set("sync.interval", 45)
    config.set("figure8.enabled", False)

    print(f"   Detected {len(changes_detected)} changes via watchers")

    # Export config
    config.export_json('/tmp/ai_config.json')
    print("\n💾 Configuration exported to /tmp/ai_config.json")

    # Show metrics
    metrics = config.get_metrics()
    print(f"\n📊 Configuration Metrics:")
    print(f"   Total keys: {metrics['config_keys']}")
    print(f"   Updates: {metrics['updates']}")
    print(f"   Reads: {metrics['reads']}")
    print(f"   Active watchers: {metrics['watchers']}")

    print("\n✅ Configuration Manager operational!")
    print("🚀 Ready to manage distributed config across 6 instances!")
