# --- OBSIDIAN GLOBAL: ATOMIC PERSISTENCE v23.0 (FULL TASKING) ---
import sqlite3
import json
import time
import os
import random
from pathlib import Path

# SHARED ABSOLUTE PATH
DB_PATH = Path(r"C:\AnthonyAi_Colony\Empire_Vault.db")

class EmpireDatabase:
    def __init__(self):
        os.makedirs(DB_PATH.parent, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            # 1. GRID REGISTRY
            conn.execute("""
                CREATE TABLE IF NOT EXISTS virtual_nodes (
                    node_id TEXT PRIMARY KEY,
                    account_email TEXT,
                    proxy_endpoint TEXT,
                    service TEXT,
                    status TEXT DEFAULT 'GATHERING',
                    last_pulse REAL
                )
            """)

            # 2. TASK QUEUE (Hardened)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS colony_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at REAL,
                    channel TEXT,
                    payload TEXT,
                    status TEXT DEFAULT 'PENDING',
                    priority INTEGER DEFAULT 10,
                    idempotency_key TEXT UNIQUE,
                    error_log TEXT
                )
            """)

            # 3. PRODUCTION JOBS
            conn.execute("""
                CREATE TABLE IF NOT EXISTS production_jobs (
                    job_id TEXT PRIMARY KEY,
                    title TEXT,
                    status TEXT,
                    progress INTEGER,
                    current_stage TEXT,
                    manifest TEXT,
                    final_video_path TEXT,
                    updated_at REAL
                )
            """)

            # 4. AI VIDEOS (Sovereign Storage)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_videos (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    video_url TEXT,
                    thumbnail_url TEXT,
                    created_at REAL
                )
            """)

            # 5. SOVEREIGN PAY (Cash App Clone)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sovereign_accounts (
                    cashtag TEXT PRIMARY KEY,
                    user_id TEXT,
                    balance REAL DEFAULT 0.0,
                    currency TEXT DEFAULT 'USD',
                    last_updated REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sovereign_transactions (
                    id TEXT PRIMARY KEY,
                    sender_cashtag TEXT,
                    receiver_cashtag TEXT,
                    amount REAL,
                    note TEXT,
                    status TEXT,
                    timestamp REAL
                )
            """)

            # 6. USER SESSIONS & TOKENS (Secure Auth Tracker)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    email TEXT,
                    token_hash TEXT,
                    ip_address TEXT,
                    created_at REAL,
                    expires_at REAL,
                    status TEXT DEFAULT 'ACTIVE'
                )
            """)
            conn.commit()

    def register_user_session(self, email: str, token_hash: str, ip_address: str = "127.0.0.1") -> str:
        session_id = f"sess_{int(time.time())}_{random.randint(1000,9999)}"
        created_at = time.time()
        expires_at = created_at + 86400 * 7 # 7 days
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO user_sessions (session_id, email, token_hash, ip_address, created_at, expires_at, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'ACTIVE')
                """, (session_id, email, token_hash, ip_address, created_at, expires_at))
                conn.commit()
            return session_id
        except Exception as e:
            print(f"[-] SESSION REGISTER ERROR: {e}")
            return None

    def verify_user_session(self, session_id: str) -> dict:
        try:
            with self._get_connection() as conn:
                row = conn.execute("SELECT email, token_hash, expires_at, status FROM user_sessions WHERE session_id=?", (session_id,)).fetchone()
                if row and row[3] == 'ACTIVE' and row[2] > time.time():
                    return {"valid": True, "email": row[0]}
        except: pass
        return {"valid": False}

    def push_task(self, channel, payload, priority=10, idempotency_key=None):
        """Dispatches a new task into the empire's queue."""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO colony_tasks (created_at, channel, payload, priority, idempotency_key)
                    VALUES (?, ?, ?, ?, ?)
                """, (time.time(), channel, json.dumps(payload), priority, idempotency_key))
                conn.commit()
                return True
        except Exception as e:
            print(f"[-] DB PUSH ERROR: {e}")
            return False

    def fetch_task(self, channel):
        """Pulls the next priority task for a specific agent."""
        try:
            with self._get_connection() as conn:
                row = conn.execute("""
                    SELECT id, payload FROM colony_tasks
                    WHERE channel=? AND status='PENDING'
                    ORDER BY priority DESC, created_at ASC LIMIT 1
                """, (channel,)).fetchone()

                if row:
                    conn.execute("UPDATE colony_tasks SET status='PROCESSING' WHERE id=?", (row[0],))
                    conn.commit()
                    return {"id": row[0], "payload": json.loads(row[1])}
        except: pass
        return None

    def log_event(self, node, event_type, metadata=None):
        try:
            with self._get_connection() as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS empire_events (node TEXT, event_type TEXT, metadata TEXT, timestamp REAL)")
                conn.execute("INSERT INTO empire_events (node, event_type, metadata, timestamp) VALUES (?, ?, ?, ?)",
                             (node, event_type, json.dumps(metadata) if metadata else None, time.time()))
                conn.commit()
        except: pass

db = EmpireDatabase()
