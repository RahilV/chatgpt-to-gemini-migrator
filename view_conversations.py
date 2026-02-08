"""
Simple HTTP server to view ChatGPT conversations.
Run this script and open http://localhost:8000 in your browser.
"""

import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Change to the migrated_conversations directory
os.chdir(Path(__file__).parent / 'migrated_conversations')

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

print(f">> Starting server at http://localhost:{PORT}")
print(f">> Serving files from: {os.getcwd()}")
print(f"\n>> Opening conversation viewer in your browser...")
print(f"\nPress Ctrl+C to stop the server\n")

# Open browser automatically
webbrowser.open(f'http://localhost:{PORT}/html/conversation_viewer_v2.html')

# Start server
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n>> Server stopped")
