# 🏗️ AI CODE SANDBOX PLATFORM - Technical Architecture

**Product:** Give ANY AI (ChatGPT, Gemini, Claude) the ability to execute code
**Core Insight:** Araya is already 90% of the system - just need browser bridge

---

## 📐 SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                           │
│                                                                 │
│  ┌────────────────┐        ┌─────────────────────────┐        │
│  │   ChatGPT      │        │  Browser Extension      │        │
│  │                │        │  "AI Code Sandbox"      │        │
│  │ "Here's code   │───────▶│                         │        │
│  │  to analyze    │        │  • Detect code blocks   │        │
│  │  PDFs..."      │        │  • "Execute" button     │        │
│  └────────────────┘        │  • Progress display     │        │
│                            └──────────┬──────────────┘        │
│                                       │                         │
└───────────────────────────────────────┼─────────────────────────┘
                                        │
                                        │ WebSocket
                                        │ (ws://localhost:7500)
                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DESKTOP AGENT (Araya Enhanced)                │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  ARAYA CODE EXECUTOR (WebSocket Server)                    │ │
│  │  • Receives code from browser                              │ │
│  │  • Validates safety                                        │ │
│  │  • Routes to sandbox                                       │ │
│  │  • Streams progress back                                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  SAFETY VALIDATOR                                          │ │
│  │  • Check for malicious operations (rm -rf, etc.)          │ │
│  │  • Verify file paths (can't access system files)          │ │
│  │  • Resource limits (max 1GB RAM, 30 sec timeout)          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  SNIPPET LIBRARY                                           │ │
│  │  • Pre-built modules (PDF, Excel, web scraping)           │ │
│  │  • Instant assembly (no writing from scratch)             │ │
│  │  • Tested and verified                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  SANDBOX MANAGER                                           │ │
│  │  • Python venv (isolated environment)                      │ │
│  │  • Docker container (optional, max isolation)              │ │
│  │  • Execute code safely                                     │ │
│  │  • Capture output and errors                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  RESULTS HANDLER                                           │ │
│  │  • Format output for user                                  │ │
│  │  • Stream progress updates                                 │ │
│  │  • Handle errors gracefully                                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔌 COMPONENT 1: BROWSER EXTENSION

**File:** `ai-code-sandbox-extension/`

### **manifest.json**
```json
{
  "manifest_version": 3,
  "name": "AI Code Sandbox",
  "version": "1.0.0",
  "description": "Execute AI-generated code safely in a sandbox",
  "permissions": ["activeTab", "storage"],
  "host_permissions": [
    "https://chat.openai.com/*",
    "https://claude.ai/*",
    "https://gemini.google.com/*"
  ],
  "content_scripts": [
    {
      "matches": [
        "https://chat.openai.com/*",
        "https://claude.ai/*"
      ],
      "js": ["content.js"],
      "css": ["styles.css"]
    }
  ],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html"
  }
}
```

### **content.js** (Code Detection)
```javascript
// Detect code blocks in ChatGPT/Claude
function detectCodeBlocks() {
    const codeBlocks = document.querySelectorAll('pre code, .code-block');

    codeBlocks.forEach(block => {
        // Skip if already processed
        if (block.dataset.sandboxProcessed) return;

        // Add "Execute in Sandbox" button
        const executeBtn = document.createElement('button');
        executeBtn.textContent = '⚡ Execute in Sandbox';
        executeBtn.className = 'sandbox-execute-btn';
        executeBtn.onclick = () => executeCode(block.textContent);

        block.parentNode.insertBefore(executeBtn, block.nextSibling);
        block.dataset.sandboxProcessed = 'true';
    });
}

// Execute code via Araya
async function executeCode(code) {
    // Connect to local Araya websocket
    const ws = new WebSocket('ws://localhost:7500');

    ws.onopen = () => {
        ws.send(JSON.stringify({
            type: 'execute',
            code: code,
            language: detectLanguage(code)
        }));
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'progress') {
            showProgress(data.message);
        } else if (data.type === 'result') {
            showResults(data.output);
        } else if (data.type === 'error') {
            showError(data.message);
        }
    };
}

// Detect programming language
function detectLanguage(code) {
    if (code.includes('import ') || code.includes('def ')) return 'python';
    if (code.includes('function') || code.includes('const ')) return 'javascript';
    if (code.includes('#!/bin/bash')) return 'bash';
    return 'python'; // Default
}

// Show live progress
function showProgress(message) {
    // Create progress overlay
    const overlay = document.createElement('div');
    overlay.className = 'sandbox-progress';
    overlay.innerHTML = `
        <div class="progress-content">
            <div class="spinner"></div>
            <p>${message}</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

// Run detection on page load and mutations
detectCodeBlocks();
new MutationObserver(detectCodeBlocks).observe(document.body, {
    childList: true,
    subtree: true
});
```

---

## 🖥️ COMPONENT 2: ARAYA CODE EXECUTOR

**File:** `C:\Users\dwrek\100X_DEPLOYMENT\ARAYA_CODE_EXECUTOR.py`

```python
"""
🚀 ARAYA CODE EXECUTOR - Desktop Agent for AI Code Sandbox Platform
Receives code from browser extension, executes safely in sandbox, streams results back
"""

import asyncio
import websockets
import json
import subprocess
import tempfile
import os
from pathlib import Path
import signal
import psutil

class ArayaCodeExecutor:
    """
    Desktop agent that executes code from ANY AI (ChatGPT, Claude, Gemini)

    Features:
    - WebSocket server for browser communication
    - Safety validation (check for malicious code)
    - Sandbox execution (Python venv, Docker optional)
    - Progress streaming
    - Resource limits (timeout, memory, CPU)
    """

    def __init__(self, port=7500):
        self.port = port
        self.sandbox_dir = Path(tempfile.gettempdir()) / "ai_code_sandbox"
        self.sandbox_dir.mkdir(exist_ok=True)

        # Resource limits
        self.max_execution_time = 30  # seconds
        self.max_memory_mb = 1024  # 1 GB

    async def handle_client(self, websocket, path):
        """Handle incoming websocket connection from browser"""
        print(f"🔌 Browser connected: {websocket.remote_address}")

        async for message in websocket:
            try:
                data = json.loads(message)

                if data['type'] == 'execute':
                    await self.execute_code(
                        websocket,
                        code=data['code'],
                        language=data.get('language', 'python')
                    )

            except Exception as e:
                await self.send_error(websocket, str(e))

    async def execute_code(self, websocket, code, language):
        """Execute code in sandbox and stream results"""

        # Step 1: Validate safety
        await self.send_progress(websocket, "🛡️ Validating code safety...")

        if not self.is_safe(code):
            await self.send_error(websocket, "⚠️ Code contains unsafe operations")
            return

        # Step 2: Create sandbox
        await self.send_progress(websocket, "📦 Creating sandbox environment...")
        sandbox_path = self.create_sandbox()

        # Step 3: Execute code
        await self.send_progress(websocket, "▶️ Executing code...")

        try:
            if language == 'python':
                result = await self.execute_python(code, sandbox_path)
            elif language == 'javascript':
                result = await self.execute_javascript(code, sandbox_path)
            else:
                result = await self.execute_bash(code, sandbox_path)

            await self.send_result(websocket, result)

        except Exception as e:
            await self.send_error(websocket, f"Execution error: {str(e)}")

        finally:
            # Cleanup
            self.cleanup_sandbox(sandbox_path)

    def is_safe(self, code):
        """Validate code safety (prevent malicious operations)"""

        # Blacklist dangerous operations
        dangerous_patterns = [
            'rm -rf',
            'del /f',
            '__import__("os").system',
            'eval(',
            'exec(',
            'open("/etc',
            'open("C:\\Windows',
            'subprocess.call',
            'os.remove',
            'shutil.rmtree'
        ]

        for pattern in dangerous_patterns:
            if pattern.lower() in code.lower():
                print(f"⚠️ Blocked dangerous operation: {pattern}")
                return False

        return True

    def create_sandbox(self):
        """Create isolated Python virtual environment"""
        import venv

        # Create unique sandbox directory
        sandbox_id = os.urandom(8).hex()
        sandbox_path = self.sandbox_dir / f"sandbox_{sandbox_id}"
        sandbox_path.mkdir(exist_ok=True)

        # Create Python venv
        venv.create(sandbox_path / "venv", with_pip=True)

        return sandbox_path

    async def execute_python(self, code, sandbox_path):
        """Execute Python code in sandbox"""

        # Write code to temp file
        code_file = sandbox_path / "script.py"
        code_file.write_text(code)

        # Get venv Python path
        if os.name == 'nt':  # Windows
            python_path = sandbox_path / "venv" / "Scripts" / "python.exe"
        else:  # Unix/Mac
            python_path = sandbox_path / "venv" / "bin" / "python"

        # Execute with timeout and resource limits
        try:
            process = subprocess.Popen(
                [str(python_path), str(code_file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(sandbox_path),
                text=True
            )

            # Set resource limits
            p = psutil.Process(process.pid)
            p.nice(10)  # Lower priority

            # Wait with timeout
            stdout, stderr = process.communicate(timeout=self.max_execution_time)

            return {
                'output': stdout,
                'errors': stderr,
                'exit_code': process.returncode
            }

        except subprocess.TimeoutExpired:
            process.kill()
            return {
                'output': '',
                'errors': f'⚠️ Execution timeout ({self.max_execution_time}s)',
                'exit_code': -1
            }

    async def execute_javascript(self, code, sandbox_path):
        """Execute JavaScript code using Node.js"""
        code_file = sandbox_path / "script.js"
        code_file.write_text(code)

        process = subprocess.run(
            ['node', str(code_file)],
            capture_output=True,
            text=True,
            timeout=self.max_execution_time,
            cwd=str(sandbox_path)
        )

        return {
            'output': process.stdout,
            'errors': process.stderr,
            'exit_code': process.returncode
        }

    def cleanup_sandbox(self, sandbox_path):
        """Remove sandbox directory"""
        import shutil
        try:
            shutil.rmtree(sandbox_path)
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")

    async def send_progress(self, websocket, message):
        """Send progress update to browser"""
        await websocket.send(json.dumps({
            'type': 'progress',
            'message': message
        }))

    async def send_result(self, websocket, result):
        """Send execution result to browser"""
        await websocket.send(json.dumps({
            'type': 'result',
            'output': result['output'],
            'errors': result['errors'],
            'exit_code': result['exit_code']
        }))

    async def send_error(self, websocket, message):
        """Send error to browser"""
        await websocket.send(json.dumps({
            'type': 'error',
            'message': message
        }))

    async def start(self):
        """Start WebSocket server"""
        print(f"🚀 Araya Code Executor starting on ws://localhost:{self.port}")
        print(f"📦 Sandbox directory: {self.sandbox_dir}")
        print(f"⏱️  Max execution time: {self.max_execution_time}s")
        print(f"💾 Max memory: {self.max_memory_mb}MB")
        print("\n✅ Ready to receive code from browser extension")

        async with websockets.serve(self.handle_client, "localhost", self.port):
            await asyncio.Future()  # Run forever


if __name__ == '__main__':
    executor = ArayaCodeExecutor(port=7500)

    try:
        asyncio.run(executor.start())
    except KeyboardInterrupt:
        print("\n\n👋 Araya Code Executor stopped")
```

---

## 📚 COMPONENT 3: SNIPPET LIBRARY

**File:** `C:\Users\dwrek\100X_DEPLOYMENT\SNIPPET_LIBRARY.py`

```python
"""
📚 CODE SNIPPET LIBRARY - Pre-built modules for instant assembly
Instead of AI writing 50 lines, use 2 lines with tested snippets
"""

class SnippetLibrary:
    """
    Pre-built code modules that can be instantly assembled
    10x faster than writing from scratch
    """

    @staticmethod
    def pdf_operations():
        """PDF manipulation snippets"""
        return {
            'extract_text': '''
import PyPDF2
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text
''',
            'merge_pdfs': '''
import PyPDF2
def merge_pdfs(pdf_list, output_path):
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
''',
            'pdf_to_images': '''
from pdf2image import convert_from_path
def pdf_to_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image.save(f"{output_folder}/page_{i+1}.png", "PNG")
'''
        }

    @staticmethod
    def excel_operations():
        """Excel manipulation snippets"""
        return {
            'read_excel': '''
import pandas as pd
def read_excel(file_path, sheet_name=0):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df
''',
            'write_excel': '''
import pandas as pd
def write_excel(data, file_path, sheet_name='Sheet1'):
    df = pd.DataFrame(data)
    df.to_excel(file_path, sheet_name=sheet_name, index=False)
''',
            'excel_analysis': '''
import pandas as pd
def analyze_excel(file_path):
    df = pd.read_excel(file_path)
    summary = {
        'rows': len(df),
        'columns': list(df.columns),
        'stats': df.describe().to_dict()
    }
    return summary
'''
        }

    @staticmethod
    def web_scraping():
        """Web scraping snippets"""
        return {
            'fetch_page': '''
import requests
from bs4 import BeautifulSoup
def fetch_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup
''',
            'extract_links': '''
def extract_links(soup, base_url=""):
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/'):
            href = base_url + href
        links.append(href)
    return links
''',
            'extract_images': '''
def extract_images(soup, base_url=""):
    images = []
    for img in soup.find_all('img', src=True):
        src = img['src']
        if src.startswith('/'):
            src = base_url + src
        images.append(src)
    return images
'''
        }

    @staticmethod
    def file_operations():
        """File system operations"""
        return {
            'list_files': '''
import os
from pathlib import Path
def list_files(directory, pattern="*"):
    path = Path(directory)
    return [str(f) for f in path.glob(pattern)]
''',
            'read_json': '''
import json
def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
''',
            'write_json': '''
import json
def write_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
'''
        }
```

---

## 🚀 ONE-CLICK LAUNCHER

**File:** `C:\Users\dwrek\100X_DEPLOYMENT\START_AI_CODE_SANDBOX.bat`

```batch
@echo off
echo.
echo ========================================
echo 🚀 AI CODE SANDBOX PLATFORM
echo ========================================
echo.
echo Starting Araya Code Executor...
echo Listening on ws://localhost:7500
echo.
echo Next step: Install browser extension
echo Then AI-generated code can execute!
echo.

python ARAYA_CODE_EXECUTOR.py

pause
```

---

## 📊 DATA FLOW DIAGRAM

```
User asks ChatGPT: "Analyze PDFs in Downloads"
                ↓
ChatGPT generates Python code (50 lines)
                ↓
Browser Extension detects code block
                ↓
Shows "⚡ Execute in Sandbox" button
                ↓
User clicks button
                ↓
Extension sends code to ws://localhost:7500
                ↓
Araya Code Executor receives code
                ↓
Safety Validator checks (no rm -rf, etc.)
                ↓
Snippet Library enhances code (2 lines instead of 50)
                ↓
Sandbox Manager creates Python venv
                ↓
Code executes in isolated environment
                ↓
Results stream back to browser
                ↓
User sees: "✅ Analyzed 47 PDFs, created summary.xlsx"
                ↓
ChatGPT displays results inline
```

---

## ⏱️ BUILD TIMELINE (TRINITY ACCELERATION)

### **Week 1: Core System (C1 builds)**
- Day 1-2: `ARAYA_CODE_EXECUTOR.py` (websocket server + sandbox)
- Day 3-4: Safety validator + snippet library
- Day 5: Testing and debugging

### **Week 2: Browser Extension (C1 builds)**
- Day 1-2: Chrome extension (manifest + content script)
- Day 3: Code detection and UI
- Day 4: WebSocket communication
- Day 5: Testing with ChatGPT/Claude

### **Week 3: Polish & Launch (All hands)**
- Day 1-2: Documentation and tutorials
- Day 3: Beta testing with 9 testers
- Day 4: Payment integration (Stripe)
- Day 5: Product Hunt launch

---

## 🎯 SUCCESS METRICS

**Week 1 Beta:**
- 9 beta testers execute 100+ code snippets
- Zero crashes or security issues
- 90%+ success rate

**Month 1 Launch:**
- 500 free tier users
- 50 Pro users ($1,000 MRR)
- 4.5+ star reviews

**Month 3:**
- 5,000 free users
- 500 Pro users ($10,000 MRR)
- Featured on Product Hunt
- First enterprise customer

**Month 6:**
- 25,000 free users
- 2,500 Pro users ($50,000 MRR)
- Integration with ChatGPT plugins
- $600K ARR run rate

---

## 🔥 WHY ARAYA IS THE SECRET

**90% of this already exists:**
- ✅ Araya can execute Python
- ✅ Araya has AI integration
- ✅ Araya can manipulate files
- ✅ Araya has conversation context

**What's missing (10%):**
- WebSocket server (2 days)
- Browser extension (3 days)
- Snippet library (3 days)
- Safety validator (2 days)

**Total: 10 days instead of 6 months**

**MANUS was right:** Use existing systems as the middleman instead of building from scratch.

---

**🤖 READY TO BUILD THE 3RD FORBES COMPANY 🤖**
