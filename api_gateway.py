"""
TRINITY FOUNDATION - API GATEWAY
Single entry point for all backend services
Eliminates the 41-service port chaos

Architecture:
    Frontend → API Gateway (port 8080) → Backend Services (various ports)

Benefits:
    - One port for frontend to call
    - Service discovery via services.json
    - Centralized logging and monitoring
    - Easy to add authentication/rate limiting later
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
from datetime import datetime
from typing import Dict, Optional, Tuple
import logging

from config import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=config.ALLOWED_ORIGINS)

# Load service registry
with open('services.json', 'r') as f:
    SERVICE_REGISTRY = json.load(f)

SERVICES = SERVICE_REGISTRY['services']
ROUTE_PATTERNS = SERVICE_REGISTRY['route_patterns']

# Request tracking
REQUEST_LOG = []
MAX_LOG_SIZE = 1000


def find_target_service(path: str) -> Optional[Dict]:
    """
    Find which backend service should handle this request

    Args:
        path: Request path (e.g., /api/auth/login)

    Returns:
        Service configuration dict or None
    """
    # Check route patterns
    for pattern, service_key in ROUTE_PATTERNS.items():
        if pattern == '_comment':
            continue

        # Simple pattern matching (supports wildcards)
        pattern_prefix = pattern.replace('/*', '')
        if path.startswith(pattern_prefix):
            return SERVICES.get(service_key)

    return None


def proxy_request(service: Dict, path: str, method: str) -> Tuple[Response, int]:
    """
    Proxy request to backend service

    Args:
        service: Service configuration
        path: Original request path
        method: HTTP method

    Returns:
        Tuple of (response, status_code)
    """
    # Build target URL
    service_base = f"http://localhost:{service['port']}"

    # Strip the gateway prefix and add service-specific path if needed
    # Example: /api/auth/login -> /login (for auth service)
    gateway_prefix = service['path']
    if path.startswith(gateway_prefix):
        target_path = path[len(gateway_prefix):]
    else:
        target_path = path

    target_url = f"{service_base}{target_path}"

    logger.info(f"Proxying {method} {path} -> {target_url}")

    try:
        # Prepare request data
        kwargs = {
            'headers': dict(request.headers),
            'timeout': 30
        }

        # Remove host header to avoid conflicts
        kwargs['headers'].pop('Host', None)

        # Add request body if present
        if request.data:
            kwargs['data'] = request.data
            kwargs['headers']['Content-Type'] = request.content_type

        # Add query parameters
        if request.args:
            kwargs['params'] = request.args

        # Make request to backend service
        if method == 'GET':
            response = requests.get(target_url, **kwargs)
        elif method == 'POST':
            response = requests.post(target_url, **kwargs)
        elif method == 'PUT':
            response = requests.put(target_url, **kwargs)
        elif method == 'DELETE':
            response = requests.delete(target_url, **kwargs)
        elif method == 'PATCH':
            response = requests.patch(target_url, **kwargs)
        else:
            return jsonify({'error': f'Unsupported method: {method}'}), 405

        # Create response
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in response.raw.headers.items()
                  if name.lower() not in excluded_headers]

        return Response(response.content, response.status_code, headers)

    except requests.exceptions.Timeout:
        logger.error(f"Timeout calling {target_url}")
        return jsonify({
            'error': 'Service timeout',
            'service': service['name'],
            'message': f"Service did not respond within 30 seconds"
        }), 504

    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error to {target_url}")
        return jsonify({
            'error': 'Service unavailable',
            'service': service['name'],
            'message': f"Could not connect to {service['name']}. Is it running on port {service['port']}?"
        }), 503

    except Exception as e:
        logger.error(f"Error proxying request: {e}")
        return jsonify({
            'error': 'Gateway error',
            'message': str(e)
        }), 500


@app.route('/api/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def api_proxy(subpath):
    """
    Main proxy endpoint - routes all /api/* requests to appropriate backend service
    """
    full_path = f'/api/{subpath}'
    method = request.method

    # Log request
    request_log_entry = {
        'timestamp': datetime.now().isoformat(),
        'method': method,
        'path': full_path,
        'ip': request.remote_addr
    }

    # Find target service
    service = find_target_service(full_path)

    if not service:
        logger.warning(f"No service found for path: {full_path}")
        request_log_entry['status'] = 404
        REQUEST_LOG.append(request_log_entry)
        return jsonify({
            'error': 'No service found',
            'path': full_path,
            'message': 'No backend service is configured to handle this path'
        }), 404

    # Proxy to service
    response, status_code = proxy_request(service, full_path, method)
    request_log_entry['status'] = status_code
    request_log_entry['service'] = service['name']

    # Add to log
    REQUEST_LOG.append(request_log_entry)
    if len(REQUEST_LOG) > MAX_LOG_SIZE:
        REQUEST_LOG.pop(0)

    return response, status_code


@app.route('/health', methods=['GET'])
def health_check():
    """Gateway health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'API Gateway',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.route('/services', methods=['GET'])
def list_services():
    """List all registered services"""
    services_info = []

    for key, service in SERVICES.items():
        services_info.append({
            'key': key,
            'name': service['name'],
            'port': service['port'],
            'path': service['path'],
            'required': service['required'],
            'description': service['description']
        })

    return jsonify({
        'services': services_info,
        'total': len(services_info),
        'gateway_port': config.GATEWAY_PORT
    })


@app.route('/services/health', methods=['GET'])
def check_all_services():
    """
    Check health of all backend services
    Useful for monitoring
    """
    results = {}

    for key, service in SERVICES.items():
        health_url = f"http://localhost:{service['port']}{service.get('health_endpoint', '/health')}"

        try:
            response = requests.get(health_url, timeout=5)
            results[key] = {
                'status': 'healthy' if response.status_code == 200 else 'degraded',
                'name': service['name'],
                'port': service['port'],
                'response_code': response.status_code
            }
        except requests.exceptions.ConnectionError:
            results[key] = {
                'status': 'down',
                'name': service['name'],
                'port': service['port'],
                'error': 'Connection refused'
            }
        except requests.exceptions.Timeout:
            results[key] = {
                'status': 'timeout',
                'name': service['name'],
                'port': service['port'],
                'error': 'Health check timeout'
            }
        except Exception as e:
            results[key] = {
                'status': 'error',
                'name': service['name'],
                'port': service['port'],
                'error': str(e)
            }

    # Overall status
    healthy_count = sum(1 for r in results.values() if r['status'] == 'healthy')
    total_count = len(results)

    return jsonify({
        'overall_status': 'healthy' if healthy_count == total_count else 'degraded',
        'healthy_services': healthy_count,
        'total_services': total_count,
        'services': results,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/stats', methods=['GET'])
def gateway_stats():
    """Gateway statistics"""
    # Calculate stats from request log
    total_requests = len(REQUEST_LOG)

    if total_requests == 0:
        return jsonify({
            'total_requests': 0,
            'message': 'No requests processed yet'
        })

    # Count by service
    service_counts = {}
    status_counts = {}

    for log_entry in REQUEST_LOG:
        service = log_entry.get('service', 'unknown')
        service_counts[service] = service_counts.get(service, 0) + 1

        status = log_entry.get('status', 0)
        status_counts[status] = status_counts.get(status, 0) + 1

    return jsonify({
        'total_requests': total_requests,
        'requests_by_service': service_counts,
        'requests_by_status': status_counts,
        'recent_requests': REQUEST_LOG[-10:] if REQUEST_LOG else []
    })


@app.route('/config', methods=['GET'])
def get_config():
    """Get gateway configuration (non-sensitive only)"""
    return jsonify({
        'gateway_port': config.GATEWAY_PORT,
        'gateway_host': config.GATEWAY_HOST,
        'environment': config.ENVIRONMENT,
        'debug': config.DEBUG,
        'registered_services': len(SERVICES),
        'configuration_status': config.validate()
    })


@app.route('/', methods=['GET'])
def index():
    """Gateway info page"""
    return jsonify({
        'service': 'Trinity Foundation API Gateway',
        'version': '1.0.0',
        'description': 'Unified entry point for all backend services',
        'endpoints': {
            'health': '/health',
            'services': '/services',
            'services_health': '/services/health',
            'stats': '/stats',
            'config': '/config'
        },
        'documentation': 'Send requests to /api/* to be routed to backend services',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    logger.info(f"Starting API Gateway on {config.GATEWAY_HOST}:{config.GATEWAY_PORT}")
    logger.info(f"Loaded {len(SERVICES)} services from registry")
    logger.info(f"Environment: {config.ENVIRONMENT}")

    app.run(
        host=config.GATEWAY_HOST,
        port=config.GATEWAY_PORT,
        debug=config.DEBUG
    )
