# --- EMPIRE 2026 TOP 20 PROFITABLE FACELESS NICHES ENGINE v2.0 (SYNCHRONIZED METADATA) ---
import random
import json
from datetime import datetime

# --- THE 20 MOST PROFITABLE FACELESS NICHES (2026 MASTER MATRIX) ---
FACELESS_20_NICHES = {
    "thefourthencounter": {
        "name": "UFOs & Deep Space Anomalies",
        "reference_channel": "@thefourthencounter",
        "voice": "en-GB-RyanNeural",
        "stories": [
            {
                "title": "A Military Pilot Locked Radar onto a Metallic Sphere Moving at Mach 4",
                "hook": "A military pilot locked radar onto a metallic sphere moving against jetstream winds at Mach 4.",
                "body": "FLIR thermal sensors confirmed zero engine exhaust or propulsion plumes. Radar arrays tracked the sphere descending from eighty thousand feet to sea level in under three seconds.",
                "tags": ["#UFOAnomalies", "#DeepSpace", "#NASA", "#Cosmos", "#Unexplained", "#Astronomy", "#MilitaryRadar", "#USAPilots", "#SecretFiles", "#Documentary"],
                "prompts": [
                    "Military jet cockpit view looking into dark sky night flight 4k",
                    "FLIR thermal imaging radar screen tracking glowing metallic sphere 4k",
                    "High contrast radar dish antenna array spinning under night sky 4k",
                    "Deep space cosmic nebula glowing star cluster 4k"
                ]
            },
            {
                "title": "What Lunar Orbiters Photographed on the Far Side of the Moon Was Wiped",
                "hook": "What lunar orbiters photographed on the far side of the moon was wiped from public feeds.",
                "body": "High-resolution radar scans from lunar orbiters revealed unusual magnetic anomalies deep within the Aitken Basin, suggesting buried structural masses beneath volcanic plains.",
                "tags": ["#MoonMysteries", "#LunarFarSide", "#NASA", "#SpaceDiscovery", "#Astronomy", "#Documentary", "#LunarBase", "#Cosmos", "#Unexplained", "#Space"],
                "prompts": [
                    "Far side of the moon crater surface space perspective 8k",
                    "Topographic radar scan mapping lunar surface structures 4k",
                    "Futuristic lunar orbiter satellite floating over moon crater 4k",
                    "James Webb space telescope cosmic nebula deep space 8k"
                ]
            }
        ]
    },
    "badgesandchrome": {
        "name": "True Crime & Interrogations",
        "reference_channel": "@badgesandchrome",
        "voice": "en-US-GuyNeural",
        "stories": [
            {
                "title": "The Bodycam Footage prosecutors tried to Seal from Public Records",
                "hook": "The bodycam footage captured a detail that prosecutors tried to seal from public court records.",
                "body": "When detectives entered the interrogation room, the suspect sat completely motionless for two hours. Forensic tower data proved he was forty miles away during the crime.",
                "tags": ["#TrueCrime", "#Interrogation", "#PoliceBodycam", "#Documentary", "#Courtroom", "#Investigation", "#Justice", "#CaseFiles", "#Unsolved", "#CrimeStory"],
                "prompts": [
                    "Police bodycam perspective night street investigation 4k",
                    "High contrast dimly lit interrogation room table microphone 4k",
                    "Detectives reviewing evidence dossiers under desk lamp 4k",
                    "Courtroom judge gavel sitting on polished mahogany desk 4k"
                ]
            }
        ]
    },
    "lasthikejoshua": {
        "name": "Wilderness & Hiking Mysteries",
        "reference_channel": "@lasthikejoshua",
        "voice": "en-US-ChristopherNeural",
        "stories": [
            {
                "title": "The Forest Staircases That Terrify National Park Rangers",
                "hook": "Deep inside national forests, hikers keep finding concrete staircases standing completely alone.",
                "body": "Park rangers give a strict warning: never step within three feet of the first step. Those who ignored the warning came back days later with completely blank memories.",
                "tags": ["#Wilderness", "#HikingMysteries", "#Unsolved", "#NationalParks", "#Outdoors", "#Documentary", "#StairsInTheWoods", "#StrangePhenomena", "#Forest", "#Mysteries"],
                "prompts": [
                    "Creepy moss covered antique concrete staircase standing isolated in middle of dark dense forest 4k",
                    "Dense foggy pine forest trail dark moody atmosphere 4k",
                    "Lone hiker trekking through dense alpine forest cinematic 4k",
                    "Extreme mountain wilderness forest hiking drone shot 4k"
                ]
            }
        ]
    }
}

def generate_faceless_package(niche_key=None):
    """
    Generates a 100% synchronized, story-locked production package.
    """
    if niche_key and niche_key in FACELESS_20_NICHES:
        niche_data = FACELESS_20_NICHES[niche_key]
    else:
        chosen_key = random.choice(list(FACELESS_20_NICHES.keys()))
        niche_data = FACELESS_20_NICHES[chosen_key]

    story = random.choice(niche_data["stories"])
    timestamp_id = datetime.now().strftime("%d%H%M%S")

    full_narration = f"{story['hook']} {story['body']}"

    return {
        "package_id": f"FACELESS-{timestamp_id}",
        "channel_name": niche_data["name"],
        "reference_handle": niche_data["reference_channel"],
        "title": story["title"],
        "hook": story["hook"],
        "narration": full_narration,
        "description": f"{full_narration}\n\nUnclassified documentary investigation. Reference channel: {niche_data['reference_channel']}\n\n{' '.join(story['tags'])}",
        "tags": story["tags"],
        "voice": niche_data["voice"],
        "prompts": story["prompts"]
    }

if __name__ == "__main__":
    pkg = generate_faceless_package("thefourthencounter")
    print(json.dumps(pkg, indent=4))
