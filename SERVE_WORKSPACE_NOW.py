#!/usr/bin/env python3
"""
🌐 WORKSPACE HTTP SERVER - IMMEDIATE ACCESS
Serves workspace files on port 8003 for ngrok tunneling
"""

import http.server
import socketserver
import os

PORT = 8004
DIRECTORY = "C:/Users/dwrek/100X_DEPLOYMENT"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(DIRECTORY)

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"✅ Workspace server running on port {PORT}")
        print(f"📁 Serving: {DIRECTORY}")
        print(f"🔗 Local: http://localhost:{PORT}/workspace-v3.html")
        print(f"🔗 Local: http://localhost:{PORT}/simple-gate.html")
        print(f"\n🚀 Starting ngrok tunnel...")

        httpd.serve_forever()
