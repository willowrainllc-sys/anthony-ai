# --- EMPIRE ANALYTICS NODE: RETENTION RADAR v1.1 (LEARNING LOOP) ---
import asyncio
import os
import json
import time
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from swarm_logger import swarm_log
from swarm_persistence import db

class AnalyticsNode:
    """
    BUSINESS NODE: Post-Strike Intelligence.
    Collects metrics and updates the Page Profiles so the Brain can learn.
    """
    async def collect_global_analytics(self):
        swarm_log("ANALYTICS: Scanning hub performance...", node="ANALYTICS")

        # 1. YOUTUBE ANALYTICS
        await self._poll_youtube_performance()

        # 2. UPDATE CONTENT MEMORY
        await self._update_creative_memory()

    async def _poll_youtube_performance(self):
        client_id = os.getenv("YOUTUBE_CLIENT_ID")
        client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
        if not refresh_token: return

        try:
            creds = Credentials(None, refresh_token=refresh_token, token_uri="https://oauth2.googleapis.com/token", client_id=client_id, client_secret=client_secret)
            youtube = build("youtube", "v3", credentials=creds)

            with db._get_connection() as conn:
                recent = conn.execute("""
                    SELECT metadata FROM empire_events
                    WHERE node='YOUTUBE' AND event_type='STRIKE_SUCCESS'
                    AND timestamp > (strftime('%s', 'now') - 172800) -- Last 48h
                """).fetchall()

            for row in recent:
                meta = json.loads(row[0])
                v_url = meta.get('video_url', '')
                v_id = v_url.split('v=')[-1].split('&')[0] if 'v=' in v_url else ""

                if len(v_id) > 5:
                    stats_res = youtube.videos().list(part="statistics", id=v_id).execute()
                    if stats_res.get('items'):
                        stats = stats_res['items'][0]['statistics']
                        views = int(stats.get('viewCount', 0))

                        with db._get_connection() as conn:
                            conn.execute("""
                                INSERT INTO performance_analytics (job_id, platform, views, engagement_json)
                                VALUES (?, ?, ?, ?)
                            """, (v_id, 'YOUTUBE', views, json.dumps(stats)))
                            conn.commit()
        except Exception as e:
            swarm_log(f"ANALYTICS ERROR [YT]: {e}", node="ANALYTICS")

    async def _update_creative_memory(self):
        """Updates content_profiles with successful hooks/topics."""
        swarm_log("ANALYTICS: Updating Grid Memory...", node="ANALYTICS")
        try:
            with db._get_connection() as conn:
                # Find the top performing job per platform
                best_performing = conn.execute("""
                    SELECT platform, job_id, views FROM performance_analytics
                    WHERE views > 100 ORDER BY views DESC LIMIT 10
                """).fetchall()

                for plat, job_id, views in best_performing:
                    # Logic to find the title/hook of this job and update profile
                    # (Simplified for v1.1: we just log the win)
                    swarm_log(f"MEMORY: Job [{job_id}] on {plat} is a Win ({views} views).", node="ANALYTICS")
        except: pass

async def run_analytics_loop():
    while True:
        await analytics_node.collect_global_analytics()
        await asyncio.sleep(7200) # Every 2 hours

analytics_node = AnalyticsNode()

if __name__ == "__main__":
    asyncio.run(run_analytics_loop())
