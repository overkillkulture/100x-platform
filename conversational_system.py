#!/usr/bin/env python3
"""
🌀 CONVERSATIONAL SYSTEM - Talk to the Platform

This service creates a conversational interface to the entire 100X Platform.
Instead of searching through files, just ask questions.

Usage:
    python conversational_system.py

Then visit: http://localhost:9000
Or API: curl http://localhost:9000/ask?q=what+is+cyclotron
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import json
import glob
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Simple in-memory index (will be replaced by Cyclotron later)
class SimpleSearch:
    def __init__(self):
        self.docs = {}
        self.index_all_files()

    def index_all_files(self):
        """Index all markdown files for searching"""
        print("📚 Indexing files...")

        patterns = ['*.md', '*.txt', '*.json']
        for pattern in patterns:
            for filepath in glob.glob(pattern):
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self.docs[filepath] = {
                            'content': content,
                            'lines': content.split('\n'),
                            'size': len(content)
                        }
                except Exception as e:
                    print(f"⚠️  Could not read {filepath}: {e}")

        print(f"✅ Indexed {len(self.docs)} documents")

    def search(self, query):
        """Simple keyword search across all documents"""
        query_lower = query.lower()
        results = []

        for filepath, doc in self.docs.items():
            content_lower = doc['content'].lower()

            if query_lower in content_lower:
                # Find relevant snippets
                lines = doc['lines']
                relevant_lines = [
                    (i, line) for i, line in enumerate(lines)
                    if query_lower in line.lower()
                ]

                results.append({
                    'file': filepath,
                    'matches': len(relevant_lines),
                    'snippets': relevant_lines[:3]  # Top 3 matches
                })

        # Sort by number of matches
        results.sort(key=lambda x: x['matches'], reverse=True)
        return results[:10]  # Top 10 results

# Initialize search
search_engine = SimpleSearch()

@app.route('/')
def home():
    """Simple web interface"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌀 Consciousness Revolution - Conversational Interface</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
                color: #e8e8e8;
                padding: 40px;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                background: linear-gradient(135deg, #00ffff 0%, #00ff88 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .tagline {
                color: #999;
                margin-bottom: 30px;
            }
            .search-box {
                width: 100%;
                padding: 15px;
                font-size: 18px;
                background: rgba(255,255,255,0.1);
                border: 2px solid rgba(0,255,136,0.3);
                border-radius: 10px;
                color: #fff;
                margin-bottom: 20px;
            }
            .search-box:focus {
                outline: none;
                border-color: #00ff88;
            }
            button {
                background: rgba(0,255,136,0.2);
                border: 2px solid #00ff88;
                color: #00ff88;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                cursor: pointer;
                font-weight: bold;
            }
            button:hover {
                background: rgba(0,255,136,0.4);
            }
            .results {
                margin-top: 30px;
            }
            .result {
                background: rgba(255,255,255,0.05);
                border-left: 4px solid #00ff88;
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 5px;
            }
            .result-file {
                font-weight: bold;
                color: #00ff88;
                margin-bottom: 10px;
            }
            .result-matches {
                color: #999;
                font-size: 14px;
                margin-bottom: 10px;
            }
            .snippet {
                background: rgba(0,0,0,0.3);
                padding: 10px;
                margin: 5px 0;
                border-radius: 3px;
                font-family: monospace;
                font-size: 13px;
                overflow-x: auto;
            }
            .examples {
                margin-top: 20px;
                padding: 20px;
                background: rgba(255,255,255,0.05);
                border-radius: 10px;
            }
            .examples h3 {
                color: #00ff88;
                margin-bottom: 10px;
            }
            .example {
                color: #00ffff;
                cursor: pointer;
                margin: 5px 0;
            }
            .example:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌀 Ask the System</h1>
            <p class="tagline">Natural language interface to the Consciousness Revolution Platform</p>

            <input type="text" id="query" class="search-box" placeholder="Ask me anything about the system..." />
            <button onclick="search()">Ask</button>

            <div class="examples">
                <h3>Example Questions:</h3>
                <div class="example" onclick="askExample('What is Cyclotron?')">What is Cyclotron?</div>
                <div class="example" onclick="askExample('How do I file Monell claim?')">How do I file Monell claim?</div>
                <div class="example" onclick="askExample('What is Trinity?')">What is Trinity?</div>
                <div class="example" onclick="askExample('How do I onboard Josh?')">How do I onboard Josh?</div>
                <div class="example" onclick="askExample('What are destroyer companies?')">What are destroyer companies?</div>
                <div class="example" onclick="askExample('Security camera recommendations')">Security camera recommendations</div>
            </div>

            <div class="results" id="results"></div>
        </div>

        <script>
            async function search() {
                const query = document.getElementById('query').value;
                const resultsDiv = document.getElementById('results');

                if (!query) return;

                resultsDiv.innerHTML = '<p>🔍 Searching...</p>';

                try {
                    const response = await fetch(`/ask?q=${encodeURIComponent(query)}`);
                    const data = await response.json();

                    if (data.results.length === 0) {
                        resultsDiv.innerHTML = '<p>No results found. Try rephrasing your question.</p>';
                        return;
                    }

                    let html = `<h3>Found ${data.results.length} relevant documents:</h3>`;

                    data.results.forEach(result => {
                        html += `
                            <div class="result">
                                <div class="result-file">📄 ${result.file}</div>
                                <div class="result-matches">${result.matches} matches</div>
                        `;

                        result.snippets.forEach(snippet => {
                            html += `<div class="snippet">Line ${snippet[0]}: ${snippet[1]}</div>`;
                        });

                        html += '</div>';
                    });

                    resultsDiv.innerHTML = html;
                } catch (error) {
                    resultsDiv.innerHTML = `<p>❌ Error: ${error.message}</p>`;
                }
            }

            function askExample(question) {
                document.getElementById('query').value = question;
                search();
            }

            // Allow Enter key to search
            document.getElementById('query').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') search();
            });
        </script>
    </body>
    </html>
    """
    return html

@app.route('/ask')
def ask():
    """API endpoint for questions"""
    query = request.args.get('q', '')

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    results = search_engine.search(query)

    return jsonify({
        'query': query,
        'results': results,
        'count': len(results)
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Conversational System',
        'indexed_documents': len(search_engine.docs)
    })

if __name__ == '__main__':
    print("🌀 CONVERSATIONAL SYSTEM STARTING...")
    print("")
    print("📡 Service: http://localhost:9000")
    print("❓ Ask anything about the system")
    print("")
    print("Examples:")
    print("  - What is Cyclotron?")
    print("  - How do I file Monell claim?")
    print("  - What is Trinity?")
    print("")

    app.run(host='0.0.0.0', port=9000, debug=True)
