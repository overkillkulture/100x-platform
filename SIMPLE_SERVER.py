#!/usr/bin/env python3
"""Simple HTTP server for 100X workspace"""
import http.server
import socketserver

PORT = 9000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"✅ Server running on http://localhost:{PORT}")
    print(f"📂 Serving: C:\\Users\\dwrek\\100X_DEPLOYMENT")
    print(f"\n🌐 Access points:")
    print(f"   - screening.html: http://localhost:{PORT}/screening.html")
    print(f"   - access.html: http://localhost:{PORT}/access.html")
    print(f"   - workspace.html: http://localhost:{PORT}/workspace.html")
    print(f"\n⚡ Press Ctrl+C to stop")
    httpd.serve_forever()
