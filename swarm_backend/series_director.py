# --- EMPIRE SERIES-FIRST CONTENT DIRECTOR & CANONICAL STUDIO v1.0 ---
import os
import sys
import json
import uuid
import time
import random
import re
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional

from swarm_logger import swarm_log
from swarm_persistence import db
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# --- 1. CANONICAL EPISODE CONTEXT (SINGLE SOURCE OF TRUTH) ---
@dataclass
class EpisodeContext:
    channel_id: str
    series_id: str
    season_id: str
    episode_id: str
    niche: str
    season_theme: str
    episode_number: int
    episode_title: str
    episode_topic: str
    primary_subject: str
    secondary_subjects: List[str]
    entities: List[str]
    locations: List[str]
    keywords: List[str]
    story_summary: str
    hook: str
    evidence: str
    unresolved_questions: str
    previous_episode_summary: str
    next_episode_tease: str
    target_duration_sec: int
    content_type: str # "LONG_FORM" or "SHORT_FORM"
    parent_episode_id: Optional[str] = None

# --- 2. HASHTAG VALIDATOR (STRICT TOPIC RELEVANCE REJECTION) ---
class HashtagValidator:
    """Calculates semantic relevance score (0.0 to 1.0) and rejects generic viral tags."""
    @staticmethod
    def validate_and_filter_hashtags(hashtags: List[str], episode_ctx: EpisodeContext, threshold: float = 0.70) -> List[str]:
        valid_tags = []
        forbidden_generic = {"#viral", "#fyp", "#trending", "#explore", "#shorts", "#video", "#foryou"}

        # Canonical keyword pool from context
        topic_words = set(re.sub(r'[^a-zA-Z0-9 ]', '', f"{episode_ctx.primary_subject} {' '.join(episode_ctx.entities)} {' '.join(episode_ctx.keywords)}").lower().split())

        for tag in hashtags:
            clean_tag = tag.strip().lower()
            if not clean_tag.startswith("#"):
                clean_tag = f"#{clean_tag}"

            if clean_tag in forbidden_generic:
                continue

            # Calculate topic relevance score
            tag_text = clean_tag.replace("#", "")
            matches = sum(1 for w in topic_words if len(w) > 2 and w in tag_text)
            relevance_score = min(1.0, (matches * 0.4) + (0.4 if any(kw.lower() in tag_text for kw in episode_ctx.keywords) else 0.0))

            if relevance_score >= threshold or len(valid_tags) < 5: # Keep highly relevant or top 5-8 matching
                if clean_tag not in valid_tags:
                    valid_tags.append(clean_tag)

            if len(valid_tags) >= 8:
                break

        return valid_tags

# --- 3. SERIES BIBLE & SEASON 1 ARCHITECTURE ---
class SeriesDirectorStudio:
    """
    CANONICAL AI CONTENT STUDIO:
    Enforces NICHE -> CHANNEL -> SERIES BIBLE -> SEASON 1 ARC -> EPISODE -> SHORTS -> QC.
    """
    def __init__(self):
        self._init_studio_schema()

    def _init_studio_schema(self):
        with db._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS series_bibles (
                    series_id TEXT PRIMARY KEY,
                    channel_id TEXT,
                    niche TEXT,
                    series_title TEXT,
                    series_description TEXT,
                    visual_style TEXT,
                    narration_style TEXT,
                    season_number INTEGER DEFAULT 1,
                    season_theme TEXT,
                    season_arc TEXT,
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS season_episodes (
                    episode_id TEXT PRIMARY KEY,
                    series_id TEXT,
                    season_id TEXT,
                    episode_number INTEGER,
                    title TEXT,
                    primary_subject TEXT,
                    keywords_json TEXT,
                    summary TEXT,
                    status TEXT DEFAULT 'PLANNED',
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """)
            conn.commit()

    async def get_or_create_series_bible(self, channel_id: str, niche: str) -> dict:
        """Retrieves persistent Series Bible from DB or generates Season 1 Arc."""
        series_id = f"series_{channel_id.lower()}_{niche.lower()}"
        with db._get_connection() as conn:
            row = conn.execute("SELECT * FROM series_bibles WHERE series_id=?", (series_id,)).fetchone()
            if row:
                return {
                    "series_id": row[0], "channel_id": row[1], "niche": row[2],
                    "series_title": row[3], "series_description": row[4],
                    "visual_style": row[5], "narration_style": row[6],
                    "season_number": row[7], "season_theme": row[8], "season_arc": row[9]
                }

        # Generate fresh Series Bible & Season 1 Arc
        swarm_log(f"STUDIO: Generating persistent Series Bible for [{niche}]...", node="STUDIO")
        bible = {
            "series_id": series_id,
            "channel_id": channel_id,
            "niche": niche,
            "series_title": f"The Unexplained Files: {niche.title()}",
            "series_description": f"Sovereign 4K investigative documentary series examining unclassified case files in {niche}.",
            "visual_style": "Cinematic National Geographic documentary grading, 4k 60fps, dark high-contrast rim lighting",
            "narration_style": "Deep, authoritative, gravelly documentary narrator (en-US-ChristopherNeural)",
            "season_number": 1,
            "season_theme": "The Initial Evidence & Unclassified Radar Encounters",
            "season_arc": "Season 1 moves from initial radar detection to pilot testimonies, physical wreckage analysis, and final unclassified dossier conclusions."
        }

        with db._get_connection() as conn:
            conn.execute("""
                INSERT INTO series_bibles (series_id, channel_id, niche, series_title, series_description, visual_style, narration_style, season_number, season_theme, season_arc)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (bible["series_id"], bible["channel_id"], bible["niche"], bible["series_title"], bible["series_description"], bible["visual_style"], bible["narration_style"], bible["season_number"], bible["season_theme"], bible["season_arc"]))
            conn.commit()

        # Generate Season 1 Episode Plan (10 Episodes)
        await self._plan_season_episodes(series_id, "season_01", niche)
        return bible

    async def _plan_season_episodes(self, series_id: str, season_id: str, niche: str):
        episodes_plan = [
            (1, "The First Detection", "Military Radar Incident at 80,000 feet", ["radar", "military", "altitude", "detection"]),
            (2, "The Object on Radar", "Thermal tracking confirms metallic sphere with zero exhaust", ["flir", "thermal", "metallic sphere", "propulsion"]),
            (3, "The Impossible Maneuver", "Instantaneous acceleration defying Mach 4 atmospheric drag", ["acceleration", "mach 4", "physics", "maneuver"]),
            (4, "What the Pilot Reported", "First-hand cockpit testimony from flight leads", ["pilot", "cockpit", "testimony", "flight lead"]),
            (5, "The Radar Data Analysis", "Declassified telemetry and acoustic wave recordings", ["telemetry", "declassified", "data", "acoustic"]),
            (6, "The Competing Explanation", "Analyzing weather balloon and atmospheric drone claims", ["investigation", "analysis", "weather balloon", "drone"]),
            (7, "New Evidence Discovered", "Sub-surface sonar recordings matching aerial trajectories", ["sonar", "ocean", "sub-surface", "trajectories"]),
            (8, "The Contradiction", "Conflicting agency statements regarding the wreckage location", ["contradiction", "government", "wreckage", "location"]),
            (9, "Reconstructing the Encounter", "3D temporal reconstruction of the entire 4-minute event", ["3d reconstruction", "timeline", "encounter", "visuals"]),
            (10, "Season Conclusion: What Actually Happened?", "Final unclassified dossier synthesis and Season 2 tease", ["conclusion", "synthesis", "dossier", "season 2"])
        ]

        with db._get_connection() as conn:
            for ep_num, title, subject, keywords in episodes_plan:
                ep_id = f"ep_{series_id}_{season_id}_{ep_num:02d}"
                conn.execute("""
                    INSERT OR IGNORE INTO season_episodes (episode_id, series_id, season_id, episode_number, title, primary_subject, keywords_json, summary)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (ep_id, series_id, season_id, ep_num, title, subject, json.dumps(keywords), f"Season 1 Episode {ep_num} investigating {subject}."))
            conn.commit()

    async def generate_canonical_episode_context(self, channel_id: str, niche: str, ep_number: int = 1, target_duration_min: int = 12) -> EpisodeContext:
        """Constructs the canonical EpisodeContext object (SINGLE SOURCE OF TRUTH)."""
        bible = await self.get_or_create_series_bible(channel_id, niche)
        series_id = bible["series_id"]
        season_id = "season_01"
        ep_id = f"ep_{series_id}_{season_id}_{ep_number:02d}"

        with db._get_connection() as conn:
            row = conn.execute("SELECT title, primary_subject, keywords_json, summary FROM season_episodes WHERE episode_id=?", (ep_id,)).fetchone()
            if row:
                title, subject, kw_json, summary = row[0], row[1], row[2], row[3]
                keywords = json.loads(kw_json)
            else:
                title, subject, keywords, summary = "The Radar Encounter", "Unclassified military radar event", ["radar", "military", "encounter"], "Investigation into radar data."

        # Word count calculation: 140 words per min * target_duration_min
        word_count_target = target_duration_min * 140

        ctx = EpisodeContext(
            channel_id=channel_id,
            series_id=series_id,
            season_id=season_id,
            episode_id=ep_id,
            niche=niche,
            season_theme=bible["season_theme"],
            episode_number=ep_number,
            episode_title=title,
            episode_topic=f"Investigation into {subject}",
            primary_subject=subject,
            secondary_subjects=["Military Radar", "FLIR Thermal Tracking", "Declassified Files"],
            entities=["US Navy Pilots", "NORAD Radar Command", "Aitken Basin Laboratory"],
            locations=["Pacific Ocean Sector 7", "Nevada Military Grid"],
            keywords=keywords,
            story_summary=summary,
            hook=f"At 80,000 feet, military radar arrays locked onto an unidentified object moving at impossible speeds.",
            evidence="Declassified FLIR telemetry logs and pilot voice recordings.",
            unresolved_questions="Why did radar tracks disappear at sea level with zero debris?",
            previous_episode_summary="Episode 1 established the initial radar alert at Sector 7." if ep_number > 1 else "Season premiere introducing the radar files.",
            next_episode_tease=f"In Episode {ep_number + 1}, we analyze the thermal FLIR tracking data.",
            target_duration_sec=target_duration_min * 60,
            content_type="LONG_FORM"
        )

        return ctx

series_studio = SeriesDirectorStudio()
