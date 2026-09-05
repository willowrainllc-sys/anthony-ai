# --- EMPIRE VIRAL FACTORY: HIGH-TENSION NARRATIVE MATRIX v1.0 ---
import random
import json

# High-Tension, Addictive Viral Narrative Library
VIRAL_MASTER_LIBRARY = [
    {
        "niche": "survival_horror",
        "title": "The Island Where 300 People Vanished Overnight",
        "hook_type": "The Disappearance Curiosity Gap",
        "storyboard": [
            {
                "timestamp": "00:00-00:03",
                "spoken_script": "Three hundred people lived on this isolated island. One morning, a supply ship arrived to find everyone completely gone.",
                "visual_prompt": "Drone shot descending over an eerie fog drenched remote island coastline cinematic dark moody grading 4k",
                "on_screen_text": "EVERYONE VANISHED"
            },
            {
                "timestamp": "00:03-00:10",
                "spoken_script": "The worst part? Hot meals were still sitting on the tables, but every single boat was tied securely at the dock.",
                "visual_prompt": "Close up of an abandoned dining table inside a rustic cabin flickering candle heavy dust particles 4k",
                "on_screen_text": "HOT MEALS LEFT BEHIND"
            },
            {
                "timestamp": "00:10-00:20",
                "spoken_script": "No distress calls were sent. No bodies were ever recovered. And the government sealed the files for 70 years.",
                "visual_prompt": "Old classified manila folder stamped in red ink sitting on a dark steel desk under a single swinging bulb 4k",
                "on_screen_text": "SEALED FOR 70 YEARS"
            }
        ],
        "tags": ["#UnsolvedMysteries", "#CreepyHistory", "#DocumentaryShorts", "#WeirdHistory", "#Shorts"]
    },
    {
        "niche": "bizarre_anomalies",
        "title": "The Forest Staircases That Terrify National Park Rangers",
        "hook_type": "The Forbidden Secret",
        "storyboard": [
            {
                "timestamp": "00:00-00:03",
                "spoken_script": "Deep inside national forests, hikers keep stumbling across old concrete staircases standing completely alone with no buildings attached.",
                "visual_prompt": "Creepy moss covered antique concrete staircase standing isolated in middle of dark dense forest 4k",
                "on_screen_text": "STAIRS IN THE WOODS"
            },
            {
                "timestamp": "00:03-00:10",
                "spoken_script": "Park rangers give a strict warning: never climb them, and never step within three feet of the first step.",
                "visual_prompt": "Close up macro shot of a weathered stone step covered in thick green moss ominous cinematic shadows 4k",
                "on_screen_text": "DO NOT STEP CLOSE"
            },
            {
                "timestamp": "00:10-00:20",
                "spoken_script": "Because those who ignored the warning came back days later with completely blank memories—or didn't come back at all.",
                "visual_prompt": "Flickering silhouette of a hiker walking away into a heavy dark pine forest fog 4k",
                "on_screen_text": "MEMORIES ERASED"
            }
        ],
        "tags": ["#Unexplained", "#NationalParks", "#StrangePhenomena", "#Documentary", "#Shorts"]
    },
    {
        "niche": "psychological_shock",
        "title": "The ER Patient Speaking a Language That Wasn't Human",
        "hook_type": "The Unexplained Anomaly",
        "storyboard": [
            {
                "timestamp": "00:00-00:03",
                "spoken_script": "A man walked into an ER with zero identification, speaking a fluid language that top linguists spent three weeks trying to map.",
                "visual_prompt": "Cinematic shot of hospital emergency room hallway flickering fluorescent lights high contrast 4k",
                "on_screen_text": "ZERO IDENTIFICATION"
            },
            {
                "timestamp": "00:03-00:10",
                "spoken_script": "His brain scans showed intense neural activity in areas never before recorded in human biology.",
                "visual_prompt": "Close up of glowing brain MRI scan monitor in dark medical lab glowing blue 4k",
                "on_screen_text": "NEURAL ANOMALY"
            },
            {
                "timestamp": "00:10-00:20",
                "spoken_script": "Then on the twenty-second day, the medical room was found completely empty, with security cameras showing the doors never opened.",
                "visual_prompt": "Empty hospital room dimly lit white medical bed isolated camera slow push in 4k",
                "on_screen_text": "VANISHED FROM ROOM"
            }
        ],
        "tags": ["#PsychologicalShock", "#Unexplained", "#MysteryFiles", "#DocumentaryShorts", "#Shorts"]
    }
]

def generate_viral_package(niche=None):
    """Generates an elite, high-retention video package designed to capture immediate views."""
    if niche:
        matches = [t for t in VIRAL_MASTER_LIBRARY if t["niche"] == niche]
        topic = random.choice(matches) if matches else random.choice(VIRAL_MASTER_LIBRARY)
    else:
        topic = random.choice(VIRAL_MASTER_LIBRARY)

    full_script = " ".join([scene["spoken_script"] for scene in topic["storyboard"]])
    scene_prompts = [scene["visual_prompt"] for scene in topic["storyboard"]]

    package = {
        "content_id": f"VIRAL-{random.randint(10000, 99999)}",
        "title": topic["title"],
        "description": f"{full_script} True unclassified accounts that defy explanation. {' '.join(topic['tags'])}",
        "tags": topic["tags"],
        "niche": topic["niche"],
        "script": full_script,
        "scene_prompts": scene_prompts,
        "locked_storyboard": topic["storyboard"]
    }

    return package

if __name__ == "__main__":
    print(json.dumps(generate_viral_package(), indent=4))
