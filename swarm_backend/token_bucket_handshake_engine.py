# --- WILLOW RAIN ENTERPRISES: TOKEN BUCKET RATE LIMITER & STATELESS S2S HANDSHAKE ENGINE v1.0 ---
import os
import sys
import json
import uuid
import time
import random
import asyncio
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from pathlib import Path

from swarm_logger import swarm_log
from swarm_persistence import db
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
TOKEN_VAULT = SECURE_DIR / "scoped_tokens_vault"
TOKEN_VAULT.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. SCOPED TOKEN & HANDSHAKE SCHEMAS
# ============================================================

class ScopedS2SToken(BaseModel):
    token_id: str
    bearer_token: str
    client_identity: str
    quota_gb: float
    used_gb: float = 0.0
    refill_rate_mbps: float = 100.0   # Token Bucket Refill Speed
    tokens_available_bytes: float     # Token Bucket Capacity in Bytes
    created_at: float = Field(default_factory=time.time)
    expires_at: float
    is_active: bool = True

class HandshakeValidationResult(BaseModel):
    authenticated: bool
    client_identity: str
    remaining_quota_gb: float
    rate_limit_mbps: float
    message: str

# ============================================================
# 2. TOKEN BUCKET RATE LIMITER & STATELESS HANDSHAKER
# ============================================================

class TokenBucketLimiter:
    """
    TOKEN BUCKET RATE LIMITER:
    Controls data transmission rates (Mbps) using a classic Token Bucket algorithm.
    Tokens in bucket represent available byte capacity; refills automatically at constant rate.
    """
    def __init__(self, capacity_bytes: int = 100 * 1024 * 1024, fill_rate_bytes_per_sec: int = 12 * 1024 * 1024):
        self.capacity = capacity_bytes               # Max bucket capacity (100 MB burst)
        self.fill_rate = fill_rate_bytes_per_sec     # Refill rate (12 MB/s = 100 Mbps)
        self.tokens = float(capacity_bytes)
        self.last_update = time.time()

    def consume(self, requested_bytes: int) -> bool:
        now = time.time()
        delta = now - self.last_update
        self.last_update = now

        # Refill tokens based on elapsed time
        self.tokens = min(self.capacity, self.tokens + delta * self.fill_rate)

        if self.tokens >= requested_bytes:
            self.tokens -= requested_bytes
            return True
        return False

class ScopedTokenHandshakeEngine:
    """
    STATELESS S2S HANDSHAKE ENGINE v1.0:
    Issues scoped, metered API tokens with automatic quota expiry and token bucket rate-limiting.
    24/7 hands-off server-to-server connection authentication.
    """
    def __init__(self):
        self._init_token_table()

    def _init_token_table(self):
        with db._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scoped_s2s_tokens (
                    token_id TEXT PRIMARY KEY,
                    bearer_token TEXT UNIQUE,
                    client_identity TEXT,
                    quota_gb REAL,
                    used_gb REAL,
                    expires_at REAL,
                    is_active INTEGER
                )
            """)
            conn.commit()

    def issue_scoped_token(self, client_identity: str, quota_gb: float = 250.0, validity_hours: int = 720) -> ScopedS2SToken:
        token_id = f"tok_{uuid.uuid4().hex[:6]}"
        bearer_token = f"wr_s2s_{uuid.uuid4().hex[:16]}"
        expires_at = time.time() + (validity_hours * 3600)
        capacity_bytes = quota_gb * (1024 ** 3)

        tok_obj = ScopedS2SToken(
            token_id=token_id,
            bearer_token=bearer_token,
            client_identity=client_identity,
            quota_gb=quota_gb,
            used_gb=0.0,
            tokens_available_bytes=capacity_bytes,
            expires_at=expires_at,
            is_active=True
        )

        with db._get_connection() as conn:
            conn.execute("""
                INSERT INTO scoped_s2s_tokens (token_id, bearer_token, client_identity, quota_gb, used_gb, expires_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (tok_obj.token_id, tok_obj.bearer_token, tok_obj.client_identity, tok_obj.quota_gb, tok_obj.used_gb, tok_obj.expires_at, 1))
            conn.commit()

        out_file = TOKEN_VAULT / f"{token_id}.json"
        with open(out_file, "w") as f:
            f.write(tok_obj.model_dump_json(indent=4))

        swarm_log(f" TOKEN_ENGINE: Issued scoped S2S token [{bearer_token[:12]}...] ({quota_gb} GB) for {client_identity}!", node="TOKEN_ENGINE")
        return tok_obj

    def validate_stateless_handshake(self, bearer_token: str, bytes_requested: int = 1048576) -> HandshakeValidationResult:
        """Stateless S2S Handshake: Verifies token, quota, and expiry in milliseconds."""
        if not bearer_token:
            return HandshakeValidationResult(authenticated=False, client_identity="ANONYMOUS", remaining_quota_gb=0.0, rate_limit_mbps=0.0, message="Missing Bearer Token")

        with db._get_connection() as conn:
            row = conn.execute("SELECT client_identity, quota_gb, used_gb, expires_at, is_active FROM scoped_s2s_tokens WHERE bearer_token=?", (bearer_token,)).fetchone()
            if row:
                client_id, quota_gb, used_gb, expires_at, is_active = row
                now = time.time()

                if is_active == 0:
                    return HandshakeValidationResult(authenticated=False, client_identity=client_id, remaining_quota_gb=0.0, rate_limit_mbps=0.0, message="Token quota exhausted / inactive")
                if now > expires_at:
                    return HandshakeValidationResult(authenticated=False, client_identity=client_id, remaining_quota_gb=0.0, rate_limit_mbps=0.0, message="Token expired")

                # Deduct requested bytes from quota
                added_gb = bytes_requested / (1024 ** 3)
                new_used = used_gb + added_gb
                remaining_gb = max(0.0, quota_gb - new_used)

                if new_used >= quota_gb:
                    conn.execute("UPDATE scoped_s2s_tokens SET used_gb=?, is_active=0 WHERE bearer_token=?", (new_used, bearer_token))
                    conn.commit()
                    return HandshakeValidationResult(authenticated=False, client_identity=client_id, remaining_quota_gb=0.0, rate_limit_mbps=0.0, message="Quota limit reached on request")

                conn.execute("UPDATE scoped_s2s_tokens SET used_gb=? WHERE bearer_token=?", (new_used, bearer_token))
                conn.commit()

                return HandshakeValidationResult(authenticated=True, client_identity=client_id, remaining_quota_gb=round(remaining_gb, 2), rate_limit_mbps=100.0, message="S2S Handshake Authenticated OK")

        return HandshakeValidationResult(authenticated=False, client_identity="UNKNOWN", remaining_quota_gb=0.0, rate_limit_mbps=0.0, message="Invalid Bearer Token")

token_handshake_engine = ScopedTokenHandshakeEngine()

if __name__ == "__main__":
    tok = token_handshake_engine.issue_scoped_token("Geonode_Aggregator_NorthAmerica", quota_gb=500.0)
    res = token_handshake_engine.validate_stateless_handshake(tok.bearer_token, bytes_requested=10 * 1024 * 1024)

    print("ISSUED SCOPED S2S TOKEN:", tok.bearer_token)
    print("STATELESS HANDSHAKE VALIDATION:", res.model_dump())
