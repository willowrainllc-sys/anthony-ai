# --- EMPIRE AUTONOMOUS AI MEDIA STUDIO BRAIN v7.0 (INSPIRATIONAL KINETIC TEXT ENGINE) ---
import os
import sys
import json
import uuid
import time
import random
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from colony_logger import colony_log
from colony_persistence import db

# --- THE ALL-GENRE A-LIST STORYTELLER & INSPIRATIONAL MATRIX ---
SUPPORTED_CATEGORIES = {
    "inspirational_quotes": {
        "mode": "MOTIVATIONAL",
        "text_only": True,
        "visual_style": "High-altitude mountain drone golden hour 4k, peaceful nature motion graphics, 8k",
        "story_hooks": [
            "Do not ask for a light burden. Ask for broader shoulders. The obstacles before you are not blocking the path. They are the path.",
            "In the middle of the deepest winter, I finally learned that within me lay an invincible summer that no storm could extinguish.",
            "The quietest minds create the loudest impact. Stand firm in your purpose while the world rushes past in noise.",
            "Great oceans are created one drop at a time. Every small step forward rewrites your future, no matter how small it seems today."
        ],
        "story_bodies": [
            "Strength is not measured by what you can carry, but by what you can endure when everything around you collapses.",
            "When the noise of the world grows loud, retreat into your quiet determination and let your results speak."
        ],
        "story_climaxes": [
            "Keep moving forward. Your future self is denegotiating on the choice you make right now.",
            "Master your discipline, and you will master your destiny."
        ]
    },
    "spielberg_sci_fi": {
        "mode": "FICTION",
        "text_only": False,
        "visual_style": "Steven Spielberg 35mm film aesthetic, anamorphic lens flare, volumetric golden mist, 8k cinematic",
        "story_hooks": [
            "In the summer of 1984, three boys riding bicycles past the abandoned airfield saw a brilliant flash of amber light burst through the treeline, followed by a low hum that made every streetlamp in town flicker simultaneously.",
            "Dr. Sarah Lin adjusted the lens on the observatory telescope at midnight and stared in disbelief as a silent metallic sphere hovered three feet above the desert sand, reflecting the starry sky in its mirror surface."
        ],
        "story_bodies": [
            "As they approached the clearing with flashlights trembling, the ground beneath their feet began to vibrate with a warm, steady frequency.",
            "Local authorities arrived with searchlights cutting through the dense fog, but the magnetic field disrupted every radio frequency within a five-mile radius."
        ],
        "story_climaxes": [
            "With a sudden burst of golden light, the central core opened, illuminating the faces of the onlookers in pure awe.",
            "The metallic sphere rose vertically into the cloud layer, leaving a glowing trail of light across the night horizon."
        ]
    },
    "true_crime_interrogations": {
        "mode": "DOCUMENTARY",
        "text_only": False,
        "visual_style": "High contrast police bodycam, dimly lit interrogation room table microphone 4k",
        "story_hooks": [
            "At 2:14 AM, two detectives stepped into Room B. The suspect hadn't moved a single muscle in three hours. He was staring directly into the mirror, whispering a string of numbers that matched the victim's unlisted license plate.",
            "Officer Martinez flipped on his shoulder bodycam as he approached the abandoned sedan idling near the highway overpass. What he recorded through the cracked driver's window forced prosecutors to seal the trial records for thirty years."
        ],
        "story_bodies": [
            "Interrogation tapes revealed that every time detectives asked about the night of the thirteenth, his heart rate monitor dropped instead of spiking.",
            "Forensic analysts cross-referenced three thousand hours of traffic camera footage and identified a black SUV trailing the victim across three county lines."
        ],
        "story_climaxes": [
            "Ten minutes before jury deliberations closed, the lead prosecutor entered a key piece of unsealed dashcam evidence that brought the entire courtroom to absolute silence.",
            "When detectives unlocked the suspect's secondary safe, they found the missing ledger intact along with six unmailed letters."
        ]
    },
    "great_heists": {
        "mode": "STORYTELLING",
        "text_only": False,
        "visual_style": "Sleek museum vault illuminated by blue laser security grid 4k",
        "story_hooks": [
            "At 3:00 AM on a rainy Tuesday, three men walked past four armed guards, bypassed a thermal laser grid, and opened a triple-locked steel safe in under three minutes without setting off a single alarm.",
            "The security monitors in the central control room froze for exactly ninety seconds. When the live feeds reconnected, forty million dollars in raw diamonds had vanished from the display case."
        ],
        "story_bodies": [
            "Architectural schematics revealed that the vault's air filtration system contained a six-inch structural gap only one former engineer knew existed.",
            "Interpol spent three years tracking the stolen bullion across seven offshore accounts before realizing the funds were never transferred digitally."
        ],
        "story_climaxes": [
            "By the time federal agents raided the penthouse in Zurich, the crew had already crossed international waters aboard a private yacht.",
            "Five years after the heist, an anonymous package arrived at police headquarters containing the original blueprints and a handwritten note."
        ]
    },
    "cinematic_nature": {
        "mode": "DOCUMENTARY",
        "text_only": False,
        "visual_style": "Steven Spielberg National Geographic IMAX 4k 60fps nature cinematography, golden hour drone",
        "story_hooks": [
            "For three centuries, alpine guides believed the eastern ridge of Mount Blackwood was impossible to cross until an expedition team discovered a set of concrete steps frozen into the glacier.",
            "Deep inside the national forest, forest rangers have documented isolated concrete staircases standing completely alone in the dense pine wilderness with no ruins or walls nearby."
        ],
        "story_bodies": [
            "Rangers enforce a strict protocol: never approach the steps after dark. Those who ignored the warning returned days later unable to recall a single detail of their time in the woods.",
            "Search and rescue teams tracking a lost hiker recorded their compass needles spinning wildly as thermal drone cameras picked up heat signatures vanishing into the granite rock face."
        ],
        "story_climaxes": [
            "When infrared drone cameras scanned the valley at sunrise, the thermal signature vanished into the cliffside leaving no footprints behind.",
            "Expedition logs confirmed that every digital clock on the mountain lost forty minutes between midnight and dawn."
        ]
    },
    "oceans": {
        "mode": "DOCUMENTARY",
        "text_only": False,
        "visual_style": "Steven Spielberg Jaws/Abyss 35mm cinematography, abyssal Mariana Trench submersible 8k spotlight lighting",
        "story_hooks": [
            "Twelve thousand feet beneath the Atlantic surface, deep-sea research submersibles mapped the outline of a massive submerged hull sitting upright in the abyssal trench.",
            "In pitch-black waters two miles down, high-frequency sonar arrays picked up a series of rhythmic metallic pulses repeating every sixteen seconds."
        ],
        "story_bodies": [
            "Subsea cameras illuminated a galleon that sank in 1641 carrying forty tons of gold bullion, preserved impeccably by cold pressure.",
            "Marine biologists cross-referenced the acoustic pulses with oceanographic records stretching back fifty years."
        ],
        "story_climaxes": [
            "When the remotely operated vehicle touched the ocean floor, its high-powered spotlights revealed the ship's stern sitting intact in the silt with its wooden wheel still in place.",
            "Oceanographic core samples taken from the surrounding seafloor revealed solid metallic alloy structures buried beneath thirty feet of sediment."
        ]
    }
}

# STRICT FORBIDDEN BACKEND & AI JARGON REJECTION SET
FORBIDDEN_TECH_TERMS = [
    "sector", "telemetry", "ai", "model", "backend", "system", "algorithm",
    "prompt", "database", "data logs", "network", "node", "grid", "pipeline",
    "in this video", "today we are going to", "let's uncover", "high-stakes discovery",
    "unclassified discovery", "you won't believe", "what happened next changed everything"
]

@dataclass
class ContentContext:
    channel_id: str
    series_id: str
    season_id: str
    episode_id: str
    category: str
    content_mode: str
    text_only: bool
    audience_profile: str
    emotional_trigger: str
    series_title: str
    series_theme: str
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
    body_evidence: str
    climax_payoff: str
    unresolved_questions: str
    target_duration_sec: int
    content_type: str # "LONG_FORM" or "SHORT_FORM"
    visual_style: str
    narration_style: str

class MediaStudioBrain:
    """
    AUTONOMOUS AI MEDIA STUDIO BRAIN v7.0:
    Supports Inspirational Quote Videos (No Voice Narrator, Native Real Sound + Binaural Beats + Animated Kinetic Captions).
    """
    def __init__(self):
        self._init_studio_tables()

    def _init_studio_tables(self):
        with db._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS studio_series (
                    series_id TEXT PRIMARY KEY,
                    channel_id TEXT,
                    category TEXT,
                    content_mode TEXT,
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
                CREATE TABLE IF NOT EXISTS studio_episodes (
                    episode_id TEXT PRIMARY KEY,
                    series_id TEXT,
                    season_id TEXT,
                    episode_number INTEGER,
                    title TEXT,
                    primary_subject TEXT,
                    keywords_json TEXT,
                    summary TEXT,
                    hook TEXT,
                    climax TEXT,
                    status TEXT DEFAULT 'PLANNED',
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """)
            try:
                conn.execute("ALTER TABLE studio_series ADD COLUMN category TEXT")
                conn.execute("ALTER TABLE studio_episodes ADD COLUMN hook TEXT")
                conn.execute("ALTER TABLE studio_episodes ADD COLUMN climax TEXT")
            except: pass
            conn.commit()

    async def get_or_create_series_bible(self, channel_id: str, category: str) -> dict:
        cat_key = category.lower().replace(" ", "_")
        cat_info = SUPPORTED_CATEGORIES.get(cat_key, SUPPORTED_CATEGORIES["inspirational_quotes"])
        series_id = f"series_{channel_id.lower()}_{cat_key}"

        with db._get_connection() as conn:
            row = conn.execute("SELECT * FROM studio_series WHERE series_id=?", (series_id,)).fetchone()
            if row:
                return {
                    "series_id": row[0], "channel_id": row[1], "category": row[2], "content_mode": row[3],
                    "series_title": row[4], "series_description": row[5], "visual_style": row[6],
                    "narration_style": row[7], "season_number": row[8], "season_theme": row[9], "season_arc": row[10]
                }

        colony_log(f"STUDIO BRAIN: Creating Series Bible for [{category.upper()}]...", node="STUDIO_BRAIN")

        series_title = f"{category.replace('_', ' ').title()}: Season 1"
        series_description = f"Inspirational kinetic text and visual experience exploring {category.replace('_', ' ')}."
        season_theme = f"Season 1: Deep Quotes & Reflections in {category.replace('_', ' ').title()}"
        season_arc = f"10-Episode season exploring wisdom, resilience, focus, and mastery."

        series_data = {
            "series_id": series_id,
            "channel_id": channel_id,
            "category": cat_key,
            "content_mode": cat_info["mode"],
            "series_title": series_title,
            "series_description": series_description,
            "visual_style": cat_info["visual_style"],
            "narration_style": "Text Only - Kinetic Captions & Binaural Soundscape",
            "season_number": 1,
            "season_theme": season_theme,
            "season_arc": season_arc
        }

        with db._get_connection() as conn:
            conn.execute("""
                INSERT INTO studio_series (series_id, channel_id, category, content_mode, series_title, series_description, visual_style, narration_style, season_number, season_theme, season_arc)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (series_data["series_id"], series_data["channel_id"], series_data["category"], series_data["content_mode"], series_data["series_title"], series_data["series_description"], series_data["visual_style"], series_data["narration_style"], series_data["season_number"], series_data["season_theme"], series_data["season_arc"]))
            conn.commit()

        return series_data

    async def generate_canonical_context(self, channel_id: str, category: str, ep_number: int = 1, target_min: int = 12, content_type: str = "SHORT_FORM") -> ContentContext:
        cat_key = category.lower().replace(" ", "_")
        cat_info = SUPPORTED_CATEGORIES.get(cat_key, SUPPORTED_CATEGORIES["inspirational_quotes"])
        series_data = await self.get_or_create_series_bible(channel_id, category)

        series_id = series_data["series_id"]
        season_id = "season_01"
        ep_id = f"ep_{series_id}_{season_id}_{ep_number:02d}"

        hook = random.choice(cat_info["story_hooks"])
        body_ev = random.choice(cat_info["story_bodies"])
        climax = random.choice(cat_info["story_climaxes"])

        title = f"Inspirational Focus: Episode {ep_number}"
        subject = "Mindset & Resilience"
        keywords = ["mindset", "inspiration", "resilience", "wisdom", "quotes"]
        summary = f"Aesthetic inspirational quote experience: {hook}"

        target_sec = (target_min * 60) if content_type == "LONG_FORM" else 90

        return ContentContext(
            channel_id=channel_id,
            series_id=series_id,
            season_id=season_id,
            episode_id=ep_id,
            category=category,
            content_mode=cat_info["mode"],
            text_only=cat_info.get("text_only", True),
            audience_profile="High-retention aesthetic & motivational lovers",
            emotional_trigger="Peace, inspiration, intense focus",
            series_title=series_data["series_title"],
            series_theme=series_data["season_theme"],
            season_theme=series_data["season_theme"],
            episode_number=ep_number,
            episode_title=title,
            episode_topic=f"{title}: {subject}",
            primary_subject=subject,
            secondary_subjects=["Wisdom", "Focus", "Aesthetics"],
            entities=["Mindset Leaders", "Inspirational Thinkers"],
            locations=["High Mountain Ridge", "Ocean Horizon"],
            keywords=keywords,
            story_summary=summary,
            hook=hook,
            body_evidence=body_ev,
            climax_payoff=climax,
            unresolved_questions="Master your discipline, and you will master your destiny.",
            target_duration_sec=target_sec,
            content_type=content_type,
            visual_style=cat_info["visual_style"],
            narration_style=series_data["narration_style"]
        )

studio_brain = MediaStudioBrain()

if __name__ == "__main__":
    import asyncio
    async def test():
        ctx = await studio_brain.generate_canonical_context("ANTHONY_AI_OFFICIAL", "inspirational_quotes", ep_number=1, target_min=1)
        print("INSPIRATIONAL QUOTE CONTEXT CREATED:")
        print("Text Only:", ctx.text_only)
        print("Hook Quote:", ctx.hook)
        print("Body Quote:", ctx.body_evidence)
    asyncio.run(test())
