# --- EMPIRE SUPERVISOR MANAGER AGENT & LANGFUSE-STYLE FLIGHT RECORDER v1.0 ---
import os
import sys
import json
import time
import uuid
import asyncio
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

class SupervisorManagerAgent:
    """
    SUPERVISOR / MANAGER OVERSEER AGENT v1.0:
    Performs real-time Manager-Worker oversight & Langfuse-style flight recorder tracing.
    Audits every tool call, trade execution, video publish, and cash-out before execution.
    """
    def __init__(self):
        self._init_supervisor_tables()

    def _init_supervisor_tables(self):
        with db._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS supervisor_traces (
                    trace_id TEXT PRIMARY KEY,
                    worker_name TEXT,
                    action_type TEXT,
                    quality_score INTEGER,
                    status TEXT,
                    payload_json TEXT,
                    reason TEXT,
                    timestamp REAL DEFAULT (strftime('%s', 'now'))
                )
            """)
            conn.commit()

    async def audit_action_before_execution(self, worker_name: str, action_type: str, payload: dict) -> dict:
        """
        MANAGER OVERSIGHT GUARDRAIL:
        Evaluates worker bot action payloads before execution.
        Returns approval status with Quality Score (0-100). Hard failure if score < 85.
        """
        trace_id = f"trace_{uuid.uuid4().hex[:8]}"
        colony_log(f"SUPERVISOR: Auditing worker [{worker_name}] action [{action_type}]...", node="SUPERVISOR")

        score = 100
        reasons = []

        # 1. RISK & FINANCIAL PROTECTION CHECKS
        if "trade" in action_type.lower() or "robinhood" in worker_name.lower():
            stop_loss = payload.get("stop_loss_pct", 1.5)
            if float(str(stop_loss).replace("-", "").replace("%", "")) > 3.0:
                score -= 30
                reasons.append("Stop-loss exceeds maximum 3.0% safety threshold")

        # 2. DUPLICATE & REPETITION CHECKS
        if "title" in payload:
            title = payload["title"]
            with db._get_connection() as conn:
                row = conn.execute("SELECT id FROM empire_events WHERE metadata LIKE ? LIMIT 1", (f"%{title[:30]}%",)).fetchone()
                if row:
                    score -= 40
                    reasons.append(f"Title [{title[:25]}] already exists in DB")

        # 3. CONTENT & JARGON CHECKS
        if "script" in payload:
            script_text = payload["script"].lower()
            forbidden = ["sector 7", "telemetry", "algorithm", "data logs", "in this video"]
            if any(f in script_text for f in forbidden):
                score -= 25
                reasons.append("Contains forbidden AI/backend jargon")

        approved = score >= 85
        status_str = "SUPERVISOR_APPROVED" if approved else "SUPERVISOR_REJECTED"

        # Log trace to Vault DB
        trace_record = {
            "trace_id": trace_id,
            "worker_name": worker_name,
            "action_type": action_type,
            "quality_score": score,
            "status": status_str,
            "payload_json": json.dumps(payload),
            "reason": "; ".join(reasons) if reasons else "Passed all Supervisor Guardrails"
        }

        with db._get_connection() as conn:
            conn.execute("""
                INSERT INTO supervisor_traces (trace_id, worker_name, action_type, quality_score, status, payload_json, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (trace_record["trace_id"], trace_record["worker_name"], trace_record["action_type"], trace_record["quality_score"], trace_record["status"], trace_record["payload_json"], trace_record["reason"]))
            conn.commit()

        if approved:
            colony_log(f" SUPERVISOR APPROVAL: [{worker_name} | {action_type}] Score: {score}/100.", node="SUPERVISOR")
        else:
            colony_log(f"[-] SUPERVISOR REJECTION: [{worker_name} | {action_type}] Score: {score}/100. Reasons: {trace_record['reason']}", node="SUPERVISOR")

        return {
            "approved": approved,
            "quality_score": score,
            "status": status_str,
            "trace_id": trace_id,
            "reasons": reasons
        }

    async def get_recent_supervisor_traces(self, limit: int = 5) -> list:
        """Returns recent Langfuse-style audit traces across all workers."""
        with db._get_connection() as conn:
            cur = conn.cursor()
            rows = cur.execute("SELECT trace_id, worker_name, action_type, quality_score, status, reason FROM supervisor_traces ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
            return [{
                "trace_id": r[0], "worker": r[1], "action": r[2], "score": r[3], "status": r[4], "reason": r[5]
            } for r in rows]

supervisor_agent = SupervisorManagerAgent()

if __name__ == "__main__":
    async def test_supervisor():
        res1 = await supervisor_agent.audit_action_before_execution(
            "RobinhoodMCP", "execute_trade", {"symbol": "BTC", "amount": 100, "stop_loss_pct": 1.5}
        )
        print("SUPERVISOR TRADE AUDIT:", res1)
    asyncio.run(test_supervisor())
