# --- EMPIRE STORYTELLER V2: MULTI-GENRE DYNAMIC STORY DIRECTOR v6.0 ---
import os
import sys
import json
import uuid
import time
import random
import asyncio
import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from pathlib import Path

from colony_logger import colony_log
from colony_persistence import db
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Colony\Secure_Assets")
STORIES_VAULT = SECURE_DIR / "story_plans"
STORIES_VAULT.mkdir(parents=True, exist_ok=True)

RELIGIOUS_TERMS = {
    "bible", "biblical", "scripture", "jesus", "christ", "moses", "abraham",
    "genesis", "exodus", "revelation", "apostle", "gospel", "old testament",
    "new testament", "ark of the covenant", "garden of eden", "noah"
}

def contains_unrequested_religious_reference(text: str) -> bool:
    if not text: return False
    text_lower = text.lower()
    return any(re.search(rf"\b{re.escape(term)}\b", text_lower) for term in RELIGIOUS_TERMS)

# ============================================================
# 1. PYDANTIC DATA MODELS
# ============================================================

class Character(BaseModel):
    id: str
    name: str
    age: Optional[int] = None
    appearance: str
    clothing: str
    personality: str
    voice_id: Optional[str] = "en-US-ChristopherNeural"

class Location(BaseModel):
    id: str
    name: str
    description: str
    time_of_day: str = "midnight"
    weather: Optional[str] = "clear"

class Action(BaseModel):
    order: int
    actor_id: str
    action: str
    object_id: Optional[str] = None
    emotion: Optional[str] = None
    duration_seconds: float = 3.5

class Shot(BaseModel):
    shot_id: str
    shot_type: str
    camera_position: str
    camera_motion: str
    lens: str = "35mm anamorphic"
    framing: str = "center subject"
    visual_prompt: str
    negative_prompt: str = "blurry, distorted, low quality, static, watermarks, freeze frames"
    duration_seconds: float = 3.5

class Scene(BaseModel):
    scene_id: str
    scene_number: int
    purpose: str
    location_id: str
    character_ids: List[str]
    start_state: str
    actions: List[Action]
    end_state: str
    narration: str
    dialogue: Optional[str] = None
    shots: List[Shot]
    transition_to_next_scene: str = "cut"
    continuity_requirements: List[str] = Field(default_factory=list)

class StoryPlan(BaseModel):
    title: str
    genre: str
    visual_style: str
    tone: str
    characters: List[Character]
    locations: List[Location]
    scenes: List[Scene]

# ============================================================
# 2. MULTI-GENRE DYNAMIC STORY ARCHITECTURES
# ============================================================

GENRE_ARCHETYPES = {
    "exoplanets": {
        "title_prefix": "K2-18b Atmospheric Water Signal",
        "visual_style": "JWST 8K space spectroscopy, deep cobalt blue nebula, ray-traced lighting",
        "char_name": "Dr. Vance",
        "char_desc": "42 years old astrophysics lead, dark navy jumpsuit",
        "loc_name": "Mauna Kea Observatory Control Room",
        "loc_desc": "High altitude telescope control center overlooking pacific clouds",
        "narration_s1": "One hundred and twenty light years from Earth, spectroscopic arrays detected a water vapor signal that defied theoretical models.",
        "narration_s2": "JWST transmission data revealed methane and carbon dioxide absorption bands, with zero trace of ammonia.",
        "narration_s3": "The initial three-sigma detection of dimethyl sulfide meant one thing: a global liquid ocean beneath a hydrogen-rich atmosphere.",
        "prompt_s1": "Astronomer Dr Vance in navy jumpsuit analyzing glowing JWST spectroscopy transmission data in dark high-tech observatory 8k",
        "prompt_s2": "Deep cobalt blue gas giant planet K2-18b in deep space, glowing red dwarf star horizon 8k",
        "prompt_s3": "Macro close up of digital spectroscopy light curve charts glowing green on monitor screen 4k"
    },
    "true_crime": {
        "title_prefix": "Unsealed Room B Interrogation Tapes",
        "visual_style": "High-contrast 1970s film stock, 35mm grain, interrogation room shadows",
        "char_name": "Detective Miller",
        "char_desc": "48 years old senior investigator, brown trenchcoat",
        "loc_name": "Precinct Room B Interrogation Vault",
        "loc_desc": "Concrete walls, single hanging incandescent lamp, two-way mirror",
        "narration_s1": "At three AM, Detective Miller unsealed the Room B audio reels that had sat in the evidence vault for thirty years.",
        "narration_s2": "The suspect's polygraph graph remained completely flat while describing the exact location of the hidden ledger.",
        "narration_s3": "Cross-referencing the tape timestamps with the precinct log revealed that the room was empty when the voice was recorded.",
        "prompt_s1": "Detective Miller in brown trenchcoat holding reel to reel audio tape in dimly lit precinct vault 4k",
        "prompt_s2": "Close up of vintage polygraph needle tracing flatline on grid paper 4k",
        "prompt_s3": "High contrast shot of empty interrogation room B with single hanging lamp casting long shadows 8k"
    },
    "natgeo_nature": {
        "title_prefix": "Abyssal Trench Bioluminescence",
        "visual_style": "National Geographic 4K ocean underwater lighting, bioluminescent deep sea",
        "char_name": "Submersible Pilot Elena",
        "char_desc": "31 years old marine biologist, yellow dive suit",
        "loc_name": "Mariana Trench Sub-Level 10,000 Meters",
        "loc_desc": "Jet black abyssal ocean floor with glowing hydrothermal vents",
        "narration_s1": "Ten thousand meters beneath the Pacific, the submersible spotlight cut through jet-black abyssal waters.",
        "narration_s2": "Thermal sensors registered an eighty-degree water temperature spike near a cluster of ancient hydrothermal chimneys.",
        "narration_s3": "Colonying the mineral vents were thousands of unclassified organisms pulsing in rhythmic bioluminescent light patterns.",
        "prompt_s1": "Deep sea submersible spotlight illuminating glowing hydrothermal vent on ocean floor 8k",
        "prompt_s2": "Macro close up of bioluminescent deep sea organism pulsing with blue light in dark water 4k",
        "prompt_s3": "Submersible cockpit view with marine biologist Elena looking through thick glass viewport 8k"
    }
}

class StoryDirectorOrchestrator:
    """
    STORYTELLER V2  MULTI-GENRE DYNAMIC STORY DIRECTOR v6.0:
    Dynamically generates story plans across Exoplanets, True Crime, NatGeo Nature, and Mystery genres.
    """
    def generate_production_story_plan(self, user_idea: str, genre: str = "exoplanets") -> StoryPlan:
        colony_log(f"STORY_DIRECTOR_V2: Directing [{genre.upper()}] story plan for [{user_idea[:30]}]...", node="DIRECTOR_V2")
        plan_id = f"plan_{uuid.uuid4().hex[:6]}"

        arch = GENRE_ARCHETYPES.get(genre, GENRE_ARCHETYPES["exoplanets"])

        char_lead = Character(
            id=f"char_{arch['char_name'].lower().replace(' ', '_')}",
            name=arch["char_name"],
            age=38,
            appearance=arch["char_desc"],
            clothing=arch["char_desc"],
            personality="Focused expert",
            voice_id="en-US-ChristopherNeural"
        )

        loc_main = Location(
            id="loc_primary",
            name=arch["loc_name"],
            description=arch["loc_desc"],
            time_of_day="midnight",
            weather="clear"
        )

        # SCENE 1
        shot1 = Shot(shot_id="shot_01", shot_type="tracking shot", camera_position="low-angle", camera_motion="slow push-in", visual_prompt=arch["prompt_s1"], duration_seconds=3.5)
        shot2 = Shot(shot_id="shot_02", shot_type="close-up", camera_position="eye-level", camera_motion="slow tilt", visual_prompt=arch["prompt_s2"], duration_seconds=3.5)
        scene1 = Scene(
            scene_id="scene_01", scene_number=1, purpose="HOOK & SETUP", location_id="loc_primary",
            character_ids=[char_lead.id], start_state=f"{arch['char_name']} initiating investigation at {arch['loc_name']}",
            actions=[Action(order=1, actor_id=char_lead.id, action="Initiates primary analysis", duration_seconds=3.5)],
            end_state=f"{arch['char_name']} examining initial anomaly data", narration=arch["narration_s1"], shots=[shot1, shot2]
        )

        # SCENE 2
        shot3 = Shot(shot_id="shot_03", shot_type="medium shot", camera_position="eye-level", camera_motion="pan left", visual_prompt=arch["prompt_s2"], duration_seconds=3.5)
        shot4 = Shot(shot_id="shot_04", shot_type="macro close-up", camera_position="high-angle", camera_motion="macro focus", visual_prompt=arch["prompt_s3"], duration_seconds=3.5)
        scene2 = Scene(
            scene_id="scene_02", scene_number=2, purpose="ACTION & ESCALATION", location_id="loc_primary",
            character_ids=[char_lead.id], start_state=f"{arch['char_name']} examining initial anomaly data",
            actions=[Action(order=2, actor_id=char_lead.id, action="Uncovers critical data match", duration_seconds=3.5)],
            end_state=f"{arch['char_name']} confirming breakthrough finding", narration=arch["narration_s2"], shots=[shot3, shot4]
        )

        # SCENE 3
        shot5 = Shot(shot_id="shot_05", shot_type="extreme close-up", camera_position="eye-level", camera_motion="static hold", visual_prompt=arch["prompt_s1"], duration_seconds=3.5)
        shot6 = Shot(shot_id="shot_06", shot_type="establishing shot", camera_position="high-angle", camera_motion="pull-out", visual_prompt=arch["prompt_s3"], duration_seconds=3.5)
        scene3 = Scene(
            scene_id="scene_03", scene_number=3, purpose="PAYOFF & LOOP", location_id="loc_primary",
            character_ids=[char_lead.id], start_state=f"{arch['char_name']} confirming breakthrough finding",
            actions=[Action(order=3, actor_id=char_lead.id, action="Realizes global impact of discovery", duration_seconds=3.5)],
            end_state=f"{arch['char_name']} concluding investigation", narration=arch["narration_s3"], shots=[shot5, shot6]
        )

        scenes_list = [scene1, scene2, scene3]

        story_plan = StoryPlan(
            title=f"{arch['title_prefix']}: {user_idea}",
            genre=genre,
            visual_style=arch["visual_style"],
            tone="High retention, cinematic, immersive",
            characters=[char_lead],
            locations=[loc_main],
            scenes=scenes_list
        )

        out_file = STORIES_VAULT / f"{plan_id}.json"
        with open(out_file, "w") as f:
            f.write(story_plan.model_dump_json(indent=4))

        db.log_event("DIRECTOR_V2", "STORY_PLAN_VALIDATED", {"title": story_plan.title, "genre": genre, "vault_path": str(out_file)})
        colony_log(f" DIRECTOR_V2 SUCCESS: Validated [{genre.upper()}] Story Plan [{story_plan.title}]!", node="DIRECTOR_V2")
        return story_plan

story_director_v2 = StoryDirectorOrchestrator()

if __name__ == "__main__":
    plan_space = story_director_v2.generate_production_story_plan("Exoplanet K2-18b Ocean Water Discovery", genre="exoplanets")
    plan_crime = story_director_v2.generate_production_story_plan("Unsealed Precinct Polygraph Tapes", genre="true_crime")
    print("SPACE PLAN TITLE:", plan_space.title)
    print("CRIME PLAN TITLE:", plan_crime.title)
