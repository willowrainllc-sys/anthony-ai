# --- WILLOW RAIN COMPANY LLC: ANTHONY DAEMON BASE CLASS v1.0 ---
import time
import json
import os
from pathlib import Path
from swarm_persistence import db

class AnthonyChristopherDaemon:
    """
    ANTHONY DAEMON BASE:
    Provides standard heartbeat and registration for the Director's personal daemons.
    """
    def __init__(self, daemon_name: str):
        self.daemon_name = daemon_name
        self.last_heartbeat = 0
        self._register()

    def _register(self):
        """Registers the daemon in the system registry."""
        with db._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daemon_registry (
                    name TEXT PRIMARY KEY,
                    last_heartbeat REAL,
                    status TEXT,
                    metadata TEXT
                )
            """)
            conn.execute("INSERT OR REPLACE INTO daemon_registry (name, last_heartbeat, status) VALUES (?, ?, ?)",
                         (self.daemon_name, time.time(), "INITIALIZED"))
            conn.commit()

    def send_heartbeat(self, status: str = "RUNNING", metadata: dict = None):
        """Pushes a heartbeat to the registry."""
        self.last_heartbeat = time.time()
        with db._get_connection() as conn:
            conn.execute("UPDATE daemon_registry SET last_heartbeat=?, status=?, metadata=? WHERE name=?",
                         (self.last_heartbeat, status, json.dumps(metadata) if metadata else None, self.daemon_name))
            conn.commit()
