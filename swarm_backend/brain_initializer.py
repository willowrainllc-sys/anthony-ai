# --- ANTHONY AI: BRAIN SEEDER (HERETIC & AI TOOLKIT) ---
from swarm_persistence import db
import time

HERETIC_SITES = [
    ("haunts.com", "https://haunts.com", "Find haunted places and real ghost stories across states.", "Paranormal"),
    ("nuforc.org", "https://nuforc.org", "Explore 170,000+ UFO sightings from around the world.", "UFO"),
    ("atlasobscura.com", "https://atlasobscura.com", "Discover hidden and unusual places worldwide.", "Exploration"),
    ("anomalist.com", "https://anomalist.com", "Daily unexplained science, technology & mystery news.", "Mystery"),
    ("ancient-origins.net", "https://ancient-origins.net", "Learn about lost civilizations and ancient mysteries.", "Ancient"),
    ("theblackvault.com", "https://theblackvault.com", "Access declassified government files (FOIA).", "Declassified"),
    ("cryptomundo.com", "https://cryptomundo.com", "Explore Bigfoot, cryptids and mysterious creatures.", "Cryptids"),
    ("mysteriousuniverse.org", "https://mysteriousuniverse.org", "In-depth articles, podcasts on strange phenomena.", "Mystery"),
    ("strangesounds.org", "https://strangesounds.org", "Daily reports on mystery booms and unusual events.", "Mystery"),
    ("unsolved.com", "https://unsolved.com", "Explore real unsolved murder cases and missing persons.", "Unsolved"),
    ("historicmysteries.com", "https://historicmysteries.com", "Unexplained historical events and archaeological finds.", "Ancient"),
    ("majesticdocuments.com", "https://majesticdocuments.com", "Leaked Majestic-12 UFO government documents.", "Declassified"),
    ("earthfiles.com", "https://earthfiles.com", "Investigations on animal mutilations and ET encounters.", "UFO"),
    ("ancient-code.com", "https://ancient-code.com", "Hidden history, ancient knowledge and forbidden texts.", "Ancient"),
    ("paranormaldailynews.com", "https://paranormaldailynews.com", "Latest paranormal and supernatural news.", "Paranormal"),
    ("skepticalinquirer.org", "https://skepticalinquirer.org", "Scientific analysis of paranormal claims.", "Scientific"),
    ("hauntedhistorytours.com", "https://hauntedhistorytours.com", "Interactive maps of famous haunted locations.", "Paranormal"),
    ("world-mysteries.com", "https://world-mysteries.com", "Explore lost civilizations and sacred ancient ruins.", "Ancient"),
    ("americanhauntingsink.com", " American Hauntings", "Real haunted places and ghost stories from the US.", "Paranormal"),
    ("cia.gov/readingroom", "https://www.cia.gov/readingroom", "Search declassified CIA documents and Cold War secrets.", "Declassified")
]

AI_TOOLKIT = [
    ("Ideogram", "https://ideogram.ai", "Image", "Create ultra-realistic images with perfect text in seconds."),
    ("Midjourney", "https://midjourney.com", "Image", "Generate stunning, high-end visuals for brands & thumbnails."),
    ("Runway AI", "https://runwayml.com", "Video", "Turn text into videos with effects, motion & green screen."),
    ("OpusClip", "https://opus.pro", "Viral", "Convert long videos into short viral clips instantly."),
    ("Tome AI", "https://tome.app", "Presentation", "Auto-create stunning presentations from a single prompt."),
    ("Durable AI", "https://durable.co", "Web", "Build complete, professional websites in just seconds."),
    ("DoNotPay", "https://donotpay.com", "Legal", "AI lawyer for bills, disputes, cancellations & much more."),
    ("Krisp AI", "https://krisp.ai", "Audio", "Remove background noise from calls for crystal clear audio."),
    ("SlidesAI", "https://slidesai.io", "Presentation", "Turn any text into clean, professional presentation slides."),
    ("Mistral AI", "https://mistral.ai", "LLM", "Fast & lightweight AI for smart answers in any task."),
    ("Pi.ai", "https://pi.ai", "Companion", "Emotional & supportive conversational AI companion."),
    ("HeyGen", "https://heygen.com", "Avatar", "Create realistic AI avatar videos with your voice & face."),
    ("Luma AI", "https://lumalabs.ai", "3D", "Generate 3D models & product shots from your phone."),
    ("Fireflies AI", "https://fireflies.ai", "Meeting", "Automated meeting notes, summaries & action items."),
    ("Gamma AI", "https://gamma.app", "Presentation", "Create beautiful presentations & docs with AI in seconds."),
    ("Vidyo AI", "https://vidyo.ai", "Viral", "Turn long videos into short, engaging viral clips."),
    ("Grok AI", "https://x.ai", "Search", "Real-time AI search engine with smart, accurate results."),
    ("Synthesia", "https://synthesia.io", "Avatar", "AI avatar videos with natural voiceovers in minutes."),
    ("Copy.ai", "https://copy.ai", "Copywriting", "Write ads, emails, scripts & content in seconds."),
    ("QuillBot", "https://quillbot.com", "Writing", "Rewrite, paraphrase & improve your writing instantly.")
]

def seed():
    with db._get_connection() as conn:
        print("[+] Seeding Heretic Open Source...")
        for name, url, desc, cat in HERETIC_SITES:
            conn.execute("INSERT OR IGNORE INTO heretic_resources (name, url, description, category) VALUES (?, ?, ?, ?)", (name, url, desc, cat))

        print("[+] Seeding AI Toolkit...")
        for name, url, utility, desc in AI_TOOLKIT:
            conn.execute("INSERT OR IGNORE INTO ai_toolkit (name, url, utility, description) VALUES (?, ?, ?, ?)", (name, url, utility, desc))

        # Add Specialist Bots
        print("[+] Deploying Special Specialist Disciples...")
        conn.execute("INSERT OR IGNORE INTO neural_disciples (id, name, aura) VALUES ('BOT_SHADOW_LIB', 'Shadow Librarian', 'Forbidden Knowledge & Declassified Files')")
        conn.execute("INSERT OR IGNORE INTO neural_disciples (id, name, aura) VALUES ('BOT_FORGE_ARCH', 'Forge Architect', 'AI Tooling & Production Strategy')")

        conn.commit()
    print("[🚀] Brain Initialized with P-E-W Heretic & AI Mesh.")

if __name__ == "__main__":
    seed()
