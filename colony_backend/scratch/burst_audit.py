import sqlite3
import json
import os
import time

def audit():
    db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
    if not os.path.exists(db_path):
        print("Database not found")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("\n=== 🔱 SOVEREIGN STRIKE & INTERCONNECTION AUDIT ===\n")

    # 1. Production Jobs
    print("--- 🎬 ACTIVE PRODUCTION JOBS ---")
    jobs = cur.execute("SELECT job_id, status, progress, current_stage, manifest FROM production_jobs ORDER BY created_at DESC LIMIT 5").fetchall()
    for j_id, status, prog, stage, manifest in jobs:
        m = json.loads(manifest) if manifest else {}
        title = m.get('title', 'Unknown')
        print(f"[{j_id}] {title[:40]}... | {status} | {prog}% | {stage}")

    # 2. Recent Social Strikes
    print("\n--- 📡 RECENT GLOBAL SOCIAL STRIKES ---")
    strikes = cur.execute("SELECT node, timestamp, metadata FROM empire_events WHERE event_type='STRIKE_SUCCESS' ORDER BY id DESC LIMIT 10").fetchall()
    for node, ts, meta in strikes:
        m = json.loads(meta) if meta else {}
        t_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
        print(f"[{t_str}] [{node}] {m.get('title', 'Drop')[:40]}... -> {m.get('video_url', 'N/A')}")

    # 3. Interconnection Check (Hubs & Bots)
    print("\n--- 🔗 INTERCONNECTION STATUS ---")
    active_nodes = cur.execute("SELECT node_id, status, last_seen FROM osint_nodes WHERE status='ACTIVE'").fetchall()
    print(f"[✓] Hubs Linked: {len(active_nodes)} Nodes active in the Grid.")

    bot_pulses = cur.execute("SELECT node, MAX(timestamp) FROM empire_events WHERE event_type LIKE '%PULSE%' GROUP BY node").fetchall()
    print(f"[✓] Active Bot Pulses: {len(bot_pulses)} components synchronized.")

    conn.close()

if __name__ == "__main__":
    audit()
