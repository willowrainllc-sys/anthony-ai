# --- ANTHONY AI: OBSIDIAN SOVEREIGN IDE v1.0 (AGENTIC DEVELOPMENT) ---
import os
import sys
import json
import asyncio
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from swarm_logger import swarm_log
from swarm_persistence import db

app = FastAPI(title="Obsidian Sovereign IDE")

ROOT_DIR = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# --- HTML UI BOILERPLATE ---
IDE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>OBSIDIAN IDE | Sovereign Core</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Space+Mono&display=swap" rel="stylesheet">
    <style>
        body { background: #050505; color: #00FF88; font-family: 'Space Mono', monospace; margin: 0; display: flex; height: 100vh; }
        .sidebar { width: 300px; border-right: 1px solid #111; padding: 20px; overflow-y: auto; background: #000; }
        .editor-container { flex: 1; display: flex; flex-direction: column; padding: 20px; }
        .file-item { cursor: pointer; padding: 5px; font-size: 12px; }
        .file-item:hover { background: #111; }
        .file-name { color: #8B5CF6; margin-bottom: 10px; font-size: 14px; font-weight: bold; border-bottom: 1px solid #111; padding-bottom: 5px; }
        textarea { flex: 1; background: #080808; color: #FFF; border: 1px solid #222; padding: 20px; font-family: 'Space Mono', monospace; resize: none; font-size: 13px; line-height: 1.5; }
        .toolbar { padding-bottom: 20px; display: flex; gap: 20px; }
        button { background: #00FF88; color: #000; border: none; padding: 10px 20px; font-weight: bold; cursor: pointer; font-family: 'Space Grotesk'; border-radius: 4px; }
        button:hover { background: #00CC77; }
        .status { font-size: 10px; color: #444; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div style="font-family: 'Space Grotesk'; letter-spacing: 5px; color: #8B5CF6; margin-bottom: 30px;">🔱 OBSIDIAN_IDE</div>
        <div id="fileTree">Loading Atoms...</div>
    </div>
    <div class="editor-container">
        <div class="file-name" id="currentFile">SELECT A FILE FROM THE GRID</div>
        <div class="toolbar">
            <button onclick="saveFile()">FORCE WRITE</button>
            <button onclick="triggerStrike()" style="background: #8B5CF6; color: #FFF;">TRIGGER STRIKE</button>
            <div class="status" id="statusMsg">READY_FOR_INGRESS</div>
        </div>
        <textarea id="editor" spellcheck="false" placeholder="// Obsidian Codebase open for Agentic Modification..."></textarea>
    </div>

    <script>
        let openFilePath = "";

        async function loadTree() {
            const resp = await fetch('/api/tree');
            const data = await resp.json();
            const tree = document.getElementById('fileTree');
            tree.innerHTML = data.files.map(f => `<div class="file-item" onclick="openFile('${f}')">${f}</div>`).join('');
        }

        async function openFile(path) {
            openFilePath = path;
            document.getElementById('currentFile').innerText = path.toUpperCase();
            document.getElementById('statusMsg').innerText = "FETCHING_DATA...";
            const resp = await fetch(`/api/read?path=${encodeURIComponent(path)}`);
            const data = await resp.json();
            document.getElementById('editor').value = data.content;
            document.getElementById('statusMsg').innerText = "INGRESS_STABLE";
        }

        async function saveFile() {
            if(!openFilePath) return;
            document.getElementById('statusMsg').innerText = "PHYSICAL_WRITE_INITIATED...";
            const content = document.getElementById('editor').value;
            const resp = await fetch('/api/write', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: json.stringify({path: openFilePath, content: content})
            });
            document.getElementById('statusMsg').innerText = "WRITE_COMPLETE_VAULTED";
        }

        function triggerStrike() {
            alert("🔱 [SUPREME]: Global Strike Dispatched. Verify vitals in Terminal.");
        }

        loadTree();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def ide_gateway():
    return IDE_HTML

@app.get("/api/tree")
async def get_tree():
    # Only show primary python files in the backend for speed
    files = []
    backend_path = ROOT_DIR / "swarm_backend"
    for f in backend_path.glob("*.py"):
        files.append(f.name)
    return {"files": sorted(files)}

@app.get("/api/read")
async def read_file(path: str):
    full_path = ROOT_DIR / "swarm_backend" / path
    if not full_path.exists(): raise HTTPException(status_code=404)
    content = full_path.read_text(encoding='utf-8', errors='ignore')
    return {"content": content}

@app.post("/api/write")
async def write_file(data: dict):
    path = data.get("path")
    content = data.get("content")
    full_path = ROOT_DIR / "swarm_backend" / path
    full_path.write_text(content, encoding='utf-8')
    swarm_log(f"IDE: Sovereign write complete for [{path}].", node="IDE")
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    swarm_log("🔱 IDE: Sovereign Development Environment is ONLINE on Port 9005.", node="SUPREME")
    uvicorn.run(app, host="0.0.0.0", port=9005)
