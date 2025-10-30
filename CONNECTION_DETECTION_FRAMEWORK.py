"""
CONNECTION DETECTION FRAMEWORK
Automatically detects connection type and quality before operations
"""

import subprocess
import socket
import time
import requests
from typing import Dict, Tuple

class ConnectionDetector:
    """Detects and reports connection status"""

    def __init__(self):
        self.connection_type = None
        self.connection_quality = None
        self.last_check = None

    def get_active_adapter(self) -> Dict[str, any]:
        """Detect which network adapter is active"""
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        output = result.stdout

        adapters = {
            'ethernet': False,
            'wifi': False,
            'ethernet_ip': None,
            'wifi_ip': None
        }

        # Parse ipconfig output
        lines = output.split('\n')
        current_adapter = None

        for line in lines:
            if 'Ethernet adapter Ethernet' in line:
                current_adapter = 'ethernet'
            elif 'Wireless LAN adapter' in line:
                current_adapter = 'wifi'
            elif 'IPv4 Address' in line and current_adapter:
                ip = line.split(':')[-1].strip()
                if current_adapter == 'ethernet':
                    adapters['ethernet'] = True
                    adapters['ethernet_ip'] = ip
                elif current_adapter == 'wifi':
                    adapters['wifi'] = True
                    adapters['wifi_ip'] = ip

        return adapters

    def test_connection_speed(self, timeout: int = 5) -> Tuple[bool, float]:
        """Test connection speed by timing a request"""
        test_urls = [
            'https://www.google.com',
            'https://github.com',
            'https://api.github.com'
        ]

        for url in test_urls:
            try:
                start = time.time()
                response = requests.get(url, timeout=timeout)
                elapsed = time.time() - start

                if response.status_code == 200:
                    return True, elapsed
            except Exception as e:
                continue

        return False, 0

    def test_specific_service(self, service: str) -> bool:
        """Test if specific service is reachable"""
        services = {
            'github': ('github.com', 443),
            'railway': ('backboard.railway.com', 443),
            'netlify': ('api.netlify.com', 443),
        }

        if service not in services:
            return False

        host, port = services[service]

        try:
            socket.create_connection((host, port), timeout=5)
            return True
        except Exception:
            return False

    def get_connection_quality(self) -> str:
        """Rate connection quality"""
        # Test basic connectivity
        can_connect, speed = self.test_connection_speed()

        if not can_connect:
            return "NO_CONNECTION"

        if speed < 0.5:
            return "EXCELLENT"
        elif speed < 1.0:
            return "GOOD"
        elif speed < 3.0:
            return "FAIR"
        else:
            return "POOR"

    def check_all(self) -> Dict[str, any]:
        """Complete connection check"""
        adapters = self.get_active_adapter()
        can_connect, speed = self.test_connection_speed()
        quality = self.get_connection_quality()

        services = {
            'github': self.test_specific_service('github'),
            'railway': self.test_specific_service('railway'),
            'netlify': self.test_specific_service('netlify'),
        }

        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'adapters': adapters,
            'connection_active': can_connect,
            'connection_speed': f"{speed:.2f}s" if can_connect else "N/A",
            'connection_quality': quality,
            'services': services,
            'recommendation': self._get_recommendation(adapters, quality, services)
        }

        self.last_check = report
        return report

    def _get_recommendation(self, adapters: Dict, quality: str, services: Dict) -> str:
        """Get recommendation based on connection status"""
        if quality == "NO_CONNECTION":
            return "❌ NO CONNECTION - Check network cables/WiFi"

        if not adapters['ethernet'] and adapters['wifi']:
            return "⚠️ USING WIFI - Switch to Ethernet for deployments"

        if quality in ["POOR", "FAIR"]:
            return "⚠️ SLOW CONNECTION - May cause deployment timeouts"

        if not all(services.values()):
            failed = [k for k, v in services.items() if not v]
            return f"⚠️ SERVICES UNREACHABLE: {', '.join(failed)}"

        if adapters['ethernet'] and quality in ["EXCELLENT", "GOOD"]:
            return "✅ OPTIMAL - Ready for deployments"

        return "✅ CONNECTION OK"

    def print_report(self):
        """Print formatted connection report"""
        if not self.last_check:
            self.check_all()

        report = self.last_check

        print("=" * 60)
        print("🔍 CONNECTION STATUS REPORT")
        print("=" * 60)
        print(f"\n⏰ Checked: {report['timestamp']}")

        print("\n🌐 NETWORK ADAPTERS:")
        if report['adapters']['ethernet']:
            print(f"  ✅ Ethernet: {report['adapters']['ethernet_ip']}")
        else:
            print("  ❌ Ethernet: Not connected")

        if report['adapters']['wifi']:
            print(f"  ✅ WiFi: {report['adapters']['wifi_ip']}")
        else:
            print("  ❌ WiFi: Not connected")

        print(f"\n📊 CONNECTION QUALITY: {report['connection_quality']}")
        print(f"   Speed: {report['connection_speed']}")

        print("\n🔧 SERVICE AVAILABILITY:")
        for service, available in report['services'].items():
            status = "✅" if available else "❌"
            print(f"  {status} {service.title()}: {'Reachable' if available else 'Unreachable'}")

        print(f"\n💡 RECOMMENDATION:")
        print(f"   {report['recommendation']}")
        print("=" * 60)


def check_before_deployment(operation: str = "deployment") -> bool:
    """
    Check connection before critical operations
    Returns True if safe to proceed, False otherwise
    """
    detector = ConnectionDetector()
    report = detector.check_all()
    detector.print_report()

    # Determine if safe to proceed
    if report['connection_quality'] in ["NO_CONNECTION", "POOR"]:
        print(f"\n⚠️ NOT RECOMMENDED to proceed with {operation}")
        print("   Connection too unstable for critical operations")
        return False

    if operation == "github_push" and not report['services']['github']:
        print(f"\n⚠️ GitHub unreachable - cannot push")
        return False

    if operation == "railway_deploy" and not report['services']['railway']:
        print(f"\n⚠️ Railway unreachable - cannot deploy")
        return False

    if operation == "netlify_deploy" and not report['services']['netlify']:
        print(f"\n⚠️ Netlify unreachable - cannot deploy")
        return False

    print(f"\n✅ Connection OK for {operation}")
    return True


if __name__ == "__main__":
    # Quick connection check
    detector = ConnectionDetector()
    detector.check_all()
    detector.print_report()

    # Test before deployment
    print("\n" + "=" * 60)
    print("🚀 PRE-DEPLOYMENT CHECK")
    print("=" * 60)

    safe_for_github = check_before_deployment("github_push")
    safe_for_railway = check_before_deployment("railway_deploy")
    safe_for_netlify = check_before_deployment("netlify_deploy")

    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    print(f"GitHub Push:     {'✅ SAFE' if safe_for_github else '❌ NOT SAFE'}")
    print(f"Railway Deploy:  {'✅ SAFE' if safe_for_railway else '❌ NOT SAFE'}")
    print(f"Netlify Deploy:  {'✅ SAFE' if safe_for_netlify else '❌ NOT SAFE'}")
    print("=" * 60)
