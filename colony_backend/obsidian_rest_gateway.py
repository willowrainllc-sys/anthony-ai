# --- WILLOW RAIN SECURITY: OBSIDIAN REST GATEWAY (FOREVER TOKEN) v1.0 ---
import os
import sys
import json
import uuid
import hmac
import hashlib
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from colony_logger import colony_log
from colony_persistence import db

# THE FOREVER MASTER TOKEN (Special Access Company Key)
MASTER_FOREVER_TOKEN = "WR-SUPREME-GHOST-2026-ANTHONY-MAESTAS"

app = FastAPI(title="Willow Rain Security Rest Gateway")

class BurstCommand(BaseModel):
    command: str
    params: dict = {}

@app.middleware("http")
async def security_middleware(request: Request, call_next):
    # Check for the Forever Token in headers
    token = request.headers.get("X-Obsidian-Token")
    if token != MASTER_FOREVER_TOKEN:
        colony_log(f" GATEWAY: Unauthorized access attempt from [{request.client.host}].", node="SECURITY")
        raise HTTPException(status_code=403, detail="INVALID_FOREVER_TOKEN")

    return await call_next(request)

@app.get("/grid/vitals")
async def get_grid_vitals():
    """GET: Pulls live mining and wealth telemetry from the fortress."""
    colony_log("GATEWAY: Pulling live vitals for remote server...", node="SECURITY")
    from obsidian_capital_hub_controller import capital_hub
    res = await capital_hub.execute_empire_wealth_audit()
    return res

@app.post("/grid/burst")
async def push_burst_command(cmd: BurstCommand):
    """PUSH: Executes a high-authority rebirth or sweep burst."""
    colony_log(f" GATEWAY: Pushing remote burst -> [{cmd.command}]", node="SECURITY")

    if cmd.command == "REBIRTH":
        from obsidian_account_factory import account_factory
        asyncio.create_task(account_factory.execute_9k_blitz(count=50))
        return {"status": "BURST_INITIATED", "target": "REBIRTH_50"}

    elif cmd.command == "SWEEP":
        from obsidian_obsidian_bridge_autoclaim import jmpt_autoclaim
        asyncio.create_task(jmpt_autoclaim.execute_obsidian_extraction_blitz())
        return {"status": "BURST_INITIATED", "target": "BTC_SWEEP"}

    return {"status": "ERROR", "message": "UNKNOWN_COMMAND"}

if __name__ == "__main__":
    import uvicorn
    import asyncio
    colony_log("[SUPREME] REST_GATEWAY: Forever Token API is ONLINE on Port 8888.", node="SECURITY")
    uvicorn.run(app, host="0.0.0.0", port=8888)
