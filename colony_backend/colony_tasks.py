# --- EMPIRE TASK QUEUE: SHIMMER PROTECTED v2.0 ---
from colony_persistence import db
from colony_logger import colony_log
from shimmer_shield import shimmer_shield

class TaskQueue:
    """
    Standardized Interface with Shimmer Protection.
    Ensures 100% burst delivery with Idempotency.
    """
    @staticmethod
    def push(channel: str, payload: dict, priority: int = 5, idempotency_key: str = None):
        # 1. Tiered Command Enforcement
        if not shimmer_shield.authorize_command(priority):
            return False

        # 2. Physical Anchor Check
        if not shimmer_shield.verify_physical_anchor():
            colony_log("SECURITY: Hardware Anchor missing.", node="SHIELD")
            return False

        # 3. DB Push with Idempotency
        success = db.push_task(channel, payload, priority, idempotency_key=idempotency_key)
        if success:
            colony_log(f"QUEUE: [SHIMMER] Pulse registered for {channel}", node="CORE")
        return success

    @staticmethod
    def fetch(channel: str):
        return db.fetch_task(channel)

    @staticmethod
    def complete(task_id: int):
        db.complete(task_id)

    @staticmethod
    def fail(task_id: int, reason: str):
        db.fail(task_id, reason)
