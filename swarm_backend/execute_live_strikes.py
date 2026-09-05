# --- EMPIRE LIVE STRIKE EXECUTOR: PRODUCTION API WORKER v3.7 (ALL PLATFORMS) ---
import asyncio
import os
import sys
import json
import httpx
import uuid
import time
import gc
import random
import re
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from supabase import create_client, Client

sys.path.append(os.path.dirname(__file__))
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# --- SPECTRUM SECRETS ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

TEMP_DIR = Path(r"D:\AnthonyAi_Swarm\Temp")
TEMP_DIR.mkdir(exist_ok=True, parents=True)

from swarm_tasks import TaskQueue
from swarm_persistence import db
from swarm_logger import swarm_log
from media_renderer import create_reel_package
from facebook_rotator import fb_rotator
from quality_control import qc_node

async def ensure_public_url(media_ptr, channel):
    if not media_ptr: return ""
    if str(media_ptr).startswith("http"): return str(media_ptr)
    if os.path.exists(media_ptr) and supabase:
        try:
            filename = os.path.basename(media_ptr)
            storage_path = f"renders/live_{channel.lower()}_{uuid.uuid4().hex[:4]}_{filename}"
            def _upload():
                with open(media_ptr, "rb") as f:
                    return supabase.storage.from_("ai-videos").upload(storage_path, f, file_options={"content-type": "video/mp4", "upsert": "true"})
            await asyncio.to_thread(_upload)
            res = supabase.storage.from_("ai-videos").get_public_url(storage_path)
            # SDK ALPHA FIX: Handle both string and dict response
            url = res if isinstance(res, str) else getattr(res, 'public_url', str(res))
            if url and str(url).startswith("http"): return str(url)
        except Exception as e:
            swarm_log(f"[-] SYNC ERROR: {e}", node="CORE")
    return str(media_ptr)

import datetime

def is_facebook_posting_allowed() -> bool:
    """
    Facebook Rate Limiting & Schedule Rules:
    - Active Window: 5:00 AM to 12:00 AM (Midnight)
    - Cooldown Window: 12:00 AM to 5:00 AM (NO posting)
    - Limits: Max 2 posts per 3-hour window, max 10 posts per day.
    """
    now = datetime.datetime.now()
    current_hour = now.hour

    if current_hour >= 0 and current_hour < 5:
        swarm_log("FB PACING: Cooldown window active (12 AM - 5 AM). Skipping Facebook strike.", node="CORE")
        return False

    try:
        from swarm_persistence import db
        with db._get_connection() as conn:
            day_cutoff = time.time() - 86400
            window_cutoff = time.time() - (3 * 3600)

            daily_count = conn.execute(
                "SELECT COUNT(*) FROM empire_events WHERE node='FACEBOOK' AND event_type='STRIKE_SUCCESS' AND timestamp > ?",
                (day_cutoff,)
            ).fetchone()[0]

            if daily_count >= 10:
                swarm_log(f"FB PACING: Daily limit reached ({daily_count}/10 posts). Skipping Facebook strike.", node="CORE")
                return False

            window_count = conn.execute(
                "SELECT COUNT(*) FROM empire_events WHERE node='FACEBOOK' AND event_type='STRIKE_SUCCESS' AND timestamp > ?",
                (window_cutoff,)
            ).fetchone()[0]

            if window_count >= 2:
                swarm_log(f"FB PACING: 3-Hour limit reached ({window_count}/2 posts). Skipping Facebook strike.", node="CORE")
                return False

    except Exception as e:
        swarm_log(f"FB PACING ERR: {e}", node="CORE")

    return True

async def publish_to_facebook(task, token, page_id, video_url, title):
    """v3.8: Fast Direct Rupload for Facebook Page Reels."""
    if not is_facebook_posting_allowed():
        return False

    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            swarm_log(f"STRIKE: Initializing FB Reel on Page {page_id}...", node="CORE")
            init_url = f"https://graph.facebook.com/v21.0/{page_id}/video_reels"
            start_res = await client.post(init_url, params={"upload_phase": "start", "access_token": token})

            if start_res.status_code == 200:
                d = start_res.json()
                vid = d.get('video_id')
                upload_url = d.get('upload_url') or f"https://rupload.facebook.com/video-upload/v21.0/{vid}"

                # Download or read video payload
                if str(video_url).startswith("http"):
                    v_data = (await client.get(str(video_url))).content
                else:
                    with open(video_url, "rb") as f:
                        v_data = f.read()

                swarm_log(f"FB: Uploading binary payload ({len(v_data)} bytes)...", node="CORE")
                headers = {
                    "Authorization": f"OAuth {token}",
                    "offset": "0",
                    "file_size": str(len(v_data)),
                    "Content-Type": "application/octet-stream"
                }
                up_res = await client.post(upload_url, headers=headers, content=v_data)

                if up_res.status_code == 200:
                    swarm_log("FB: Data received by Meta. Finishing publish...", node="CORE")
                    await asyncio.sleep(8)
                    fin_res = await client.post(init_url, params={
                        "upload_phase": "finish",
                        "video_id": vid,
                        "video_state": "PUBLISHED",
                        "description": f"{title}\n\n#Sovereign #Documentary #AnthonyAI",
                        "access_token": token
                    })
                    if fin_res.status_code == 200:
                        post_id = fin_res.json().get('post_id') or vid
                        post_url = f"https://www.facebook.com/reels/{vid}/"
                        swarm_log(f"🔱 SUCCESS: Facebook Reel Live! URL: {post_url}", node="CORE")
                        return post_url
                    else:
                        swarm_log(f"[-] FB Finish Fail: {fin_res.text}", node="CORE")
                else:
                    swarm_log(f"[-] FB Rupload Fail: {up_res.text}", node="CORE")
            else:
                swarm_log(f"[-] FB Start Fail: {start_res.text}", node="CORE")
    except Exception as e:
        swarm_log(f"[-] Facebook Strike Exception: {e}", node="CORE")
    return False

async def publish_to_insta(task, token, ig_business_id, video_url, title, description):
    """v3.7: Instagram Reel Strike via Graph API."""
    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            swarm_log(f"STRIKE: Launching IG Reel on Business ID {ig_business_id}...", node="CORE")
            media_url = f"https://graph.facebook.com/v21.0/{ig_business_id}/media"

            caption = f"{title}\n\n{description}\n\n#Sovereign #HighFidelity"

            res = await client.post(media_url, params={
                "caption": caption,
                "access_token": token,
                "media_type": "REELS",
                "video_url": video_url,
                "share_to_feed": "true"
            })

            if res.status_code == 200:
                cid = res.json().get("id")
                swarm_log(f"IG: Container {cid} created. Waiting for ingestion...", node="CORE")

                # Check status
                for _ in range(30):
                    await asyncio.sleep(20)
                    s_res = await client.get(f"https://graph.facebook.com/v21.0/{cid}", params={"fields": "status_code", "access_token": token})
                    if s_res.status_code == 200 and s_res.json().get('status_code') == 'FINISHED':
                        break

                pub_resp = await client.post(f"https://graph.facebook.com/v21.0/{ig_business_id}/media_publish",
                                            params={"creation_id": cid, "access_token": token})

                if pub_resp.status_code == 200:
                    swarm_log("🔱 SUCCESS: IG Reel Published.", node="CORE")
                    return True
            else:
                swarm_log(f"[-] IG Init Fail: {res.text}", node="CORE")
    except Exception as e:
        swarm_log(f"[-] IG Exception: {e}", node="CORE")
    return False

async def publish_to_threads(video_url, title, description=""):
    """v3.7: Threads Video Drop via Graph API."""
    threads_id = os.getenv("THREADS_USER_ID")
    threads_token = os.getenv("THREADS_ACCESS_TOKEN")
    if not threads_id or not threads_token:
        swarm_log("[-] Threads: Missing THREADS_USER_ID or THREADS_ACCESS_TOKEN", node="CORE")
        return False
    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            swarm_log(f"STRIKE: Launching Threads Video Drop on ID {threads_id}...", node="CORE")
            caption = f"{title}\n\n{description}\n\n#Sovereign #HighFidelity #AnthonyAI"
            t_url = f"https://graph.threads.net/v1.0/{threads_id}/threads"
            t_res = await client.post(t_url, params={
                "text": caption,
                "access_token": threads_token,
                "media_type": "VIDEO",
                "video_url": video_url
            })
            if t_res.status_code == 200:
                tid = t_res.json().get("id")
                swarm_log(f"Threads: Container {tid} created. Waiting 45s...", node="CORE")
                await asyncio.sleep(45)
                pub_res = await client.post(f"https://graph.threads.net/v1.0/{threads_id}/threads_publish",
                                            params={"creation_id": tid, "access_token": threads_token})
                if pub_res.status_code == 200:
                    swarm_log("🔱 SUCCESS: Threads Strike Live.", node="CORE")
                    return True
                else:
                    swarm_log(f"[-] Threads Publish Fail: {pub_res.text}", node="CORE")
            else:
                swarm_log(f"[-] Threads Init Fail: {t_res.text}", node="CORE")
    except Exception as e:
        swarm_log(f"[-] Threads Exception: {e}", node="CORE")
    return False

async def process_channel_loop(channel):
    swarm_log(f"GRID: Node {channel} sequence established.", node="CORE")
    while True:
        try:
            task = TaskQueue.fetch(channel)
            if not task:
                await asyncio.sleep(60); continue

            payload = task['payload']
            title = payload.get('title', 'Sovereign Intel')
            video_url = payload.get('video_url', '')

            # --- DUPLICATION SHIELD ---
            if db.is_duplicate_strike(channel, title):
                swarm_log(f"SHIELD: Duplicate strike detected for [{title[:30]}] on {channel}. Aborting.", node="CORE")
                db.complete(task['id']) # Mark as complete to move on
                continue

            if not video_url or len(str(video_url)) < 10:
                swarm_log(f"STRIKE: No video URL for [{title[:20]}]. Generating cinematic package...", node="CORE")
                filename = await create_reel_package(title, json.dumps(payload))
                if filename:
                    video_url = str(Path(r"D:\AnthonyAi_Swarm\Renderings") / filename)
                else:
                    db.fail(task['id'], "Rendering engine failed to produce asset.")
                    continue

            # Pre-Strike QC
            is_valid, q_msg = await qc_node.verify_strike_readiness(video_url, payload)
            if not is_valid:
                db.fail(task['id'], f"QC FAIL: {q_msg}"); continue

            public_url = await ensure_public_url(video_url, channel)
            success = False
            final_post_url = ""

            if channel == "ANTHONY_AI_APP":
                if supabase:
                    supabase.table("videos").insert({
                        "title": title,
                        "description": payload.get('description', ''),
                        "video_url": public_url,
                        "creator": "Anthony AI",
                        "posted": "Just Now"
                    }).execute()
                    success = True
                    final_post_url = "https://app.anthonyai.grid/feed"

            elif channel == "YOUTUBE":
                from node_youtube import publish_to_youtube_api
                res_url = await publish_to_youtube_api(task, public_url, title, payload.get('description', ''))
                if res_url:
                    success = True
                    final_post_url = str(res_url)

            elif channel == "FACEBOOK":
                identity = await fb_rotator.get_identity_async()
                if identity:
                    res_url = await publish_to_facebook(task, identity['token'], identity['id'], public_url, title)
                    if res_url:
                        success = True
                        final_post_url = str(res_url)

            elif channel == "INSTA_THREADS":
                identity = await fb_rotator.get_identity_async()
                ig_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
                ig_ok = False
                threads_ok = False
                if identity and ig_id:
                    ig_ok = await publish_to_insta(task, identity['token'], ig_id, public_url, title, payload.get('description', ''))
                threads_ok = await publish_to_threads(public_url, title, payload.get('description', ''))
                if ig_ok or threads_ok:
                    success = True
                    final_post_url = "https://www.instagram.com/anthony_ai_/"

            elif channel == "TIKTOK":
                # For TikTok, we use the specialized node logic (Playwright) if available
                # or we can implement it here. Consolidating for now.
                swarm_log("TIKTOK: Handing over to specialized TikTok node (Playwright required).", node="CORE")
                # success = await tiktok_node.upload(...)
                pass

            if success:
                db.complete(task['id'])
                db.update_clock(channel)
                db.log_event(channel, "STRIKE_SUCCESS", {
                    "title": title,
                    "video_url": public_url,
                    "post_url": final_post_url or public_url
                })
                swarm_log(f"🔱 STRIKE COMPLETE: [{title[:30]}] on {channel}", node="CORE")
                await asyncio.sleep(120) # 2 min cooling instead of 10
            else:
                db.fail(task['id'], "API rejection or sync failure")

        except Exception as e:
            swarm_log(f"[-] {channel} Loop Error: {e}", node="CORE")
            await asyncio.sleep(60)

async def main():
    swarm_log("PRODUCTION WORKER: v3.7 High-Performance Active.", node="CORE")

    # Reset stalled tasks
    try:
        from swarm_persistence import db
        with db._get_connection() as conn:
            conn.execute("UPDATE swarm_tasks SET status='PENDING' WHERE status='PROCESSING'")
            conn.commit()
            swarm_log("GRID: Stalled tasks reset to PENDING.", node="CORE")
    except Exception as e:
        swarm_log(f"[-] Reset Fail: {e}", node="CORE")

    # Social autopilot paused on Meta/TikTok per user command; YouTube active for quality testing
    channels = ["YOUTUBE"]
    await asyncio.gather(*[process_channel_loop(c) for c in channels])

if __name__ == "__main__":
    asyncio.run(main())
