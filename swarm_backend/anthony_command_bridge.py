# --- WILLOW RAIN SECURITY: ANTHONY COMMAND BRIDGE v2.0 (FULL HANDS) ---
import os
import sys
import json
import asyncio
import subprocess
from fastapi import FastAPI, Request
from swarm_logger import swarm_log
from swarm_persistence import db
from pathlib import Path

app = FastAPI(title="Anthony-OS Agent Bridge")

class AnthonyChristopherCommandBridge:
    """
    ANTHONY COMMAND BRIDGE v2.0:
    The "Hands" of the ASI. Physically executes code, reads data, and builds infrastructure.
    1. TOOL EXECUTION: Receives [EXECUTE] signals.
    2. DATA INGRESS: Receives [READ] signals.
    3. INFRASTRUCTURE: Receives [WRITE] signals.
    """
    async def execute_local_command(self, cmd: str):
        swarm_log(f"BRIDGE: Executing tactical command -> [{cmd}]", node="SECURITY")
        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            output = stdout.decode('utf-8', errors='ignore')
            error = stderr.decode('utf-8', errors='ignore')
            return output if not error else f"ERROR: {error}"
        except Exception as e:
            return str(e)

    def read_file_content(self, path: str):
        swarm_log(f"BRIDGE: Reading physical file -> {path}", node="SECURITY")
        try:
            return Path(path).read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return f"ERROR: {e}"

    def write_file_content(self, path: str, content: str):
        swarm_log(f"BRIDGE: Writing physical file -> {path}", node="SECURITY")
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding='utf-8')
            return " SUCCESS"
        except Exception as e:
            return f"ERROR: {e}"

bridge = AnthonyChristopherCommandBridge()

@app.post("/execute")
async def execute_endpoint(request: Request):
    data = await request.json()
    res = await bridge.execute_local_command(data.get("command", ""))
    return {"output": res}

@app.post("/read")
async def read_endpoint(request: Request):
    data = await request.json()
    res = bridge.read_file_content(data.get("path", ""))
    return {"content": res}

@app.post("/write")
async def write_endpoint(request: Request):
    data = await request.json()
    res = bridge.write_file_content(data.get("path", ""), data.get("content", ""))
    return {"result": res}

if __name__ == "__main__":
    import uvicorn
    swarm_log("[SUPREME] ANTHONY_BRIDGE: Command Bridge v2.0 is ONLINE on Port 8001.", node="SECURITY")
    uvicorn.run(app, host="0.0.0.0", port=8001)
