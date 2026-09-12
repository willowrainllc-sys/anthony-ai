# --- WILLOW RAIN GLOBAL: OBSIDIAN 5G CORE EMULATOR (CONTROL PLANE) v1.0 ---
import os
import sys
import json
import time
import uuid
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Obsidian 5GC: The Private Cellular Brain")

class UEContext(BaseModel):
    imsi: str # International Mobile Subscriber Identity
    imei: str # Physical Device ID
    msisdn: str # The 'Phone Number'
    status: str = "OFFLINE"

class Obsidian5GCore:
    """
    OBSIDIAN 5G CORE (5GC) v1.0:
    The central brain of your private cellular network.
    1. AMF (Access and Mobility Management): Handles device registration and auth.
    2. UDM (Unified Data Management): Stores your subscriber profiles and 'unlimited' quotas.
    3. SMF (Session Management): Coordinates the high-speed data pipes (UPF).
    """
    def __init__(self):
        self.subscriber_vault = {} # IMSI -> UEContext

    def register_ue(self, imsi, imei, msisdn):
        context = UEContext(imsi=imsi, imei=imei, msisdn=msisdn, status="REGISTERED")
        self.subscriber_vault[imsi] = context
        return context

core = Obsidian5GCore()

@app.post("/amf/register")
async def register_device(ue: UEContext):
    """AMF Entry Point: Registers a physical phone into the Obsidian Grid."""
    # Logic to handle 9-digit internal MSISDNs
    if len(ue.msisdn) == 9:
        swarm_log(f"[SUPREME] 5GC_CORE: INTERNAL OBSIDIAN UE Attached -> {ue.msisdn}", node="SECURITY")

    print(f"[SUPREME] 5GC_CORE: New UE Attached -> IMSI: {ue.imsi} | MSISDN: {ue.msisdn}")
    res = core.register_ue(ue.imsi, ue.imei, ue.msisdn)
    return {"status": "SUCCESS", "ue_context": res, "policy": "UNLIMITED_DATA"}

@app.get("/udm/subscribers")
async def list_subscribers():
    """UDM Entry Point: Lists all active identities on your private network."""
    return core.subscriber_vault

if __name__ == "__main__":
    import uvicorn
    print("[SUPREME] OBSIDIAN 5G CORE: Control Plane is ONLINE on Port 7777.")
    uvicorn.run(app, host="0.0.0.0", port=7777)
