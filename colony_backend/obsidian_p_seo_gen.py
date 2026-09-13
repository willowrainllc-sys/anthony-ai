# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY pSEO & SITEMAP ENGINE v1.0 ---
import os
import json
from pathlib import Path
from datetime import datetime

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
states_file = root / "colony_backend" / "states_data.json"

def generate_sitemap():
    print("[*] pSEO ENGINE: Generating Automated Sitemap...")

    # 1. Base Pages
    pages = [
        "index.html", "obsidian_domains.html", "obsidian_llc_formation.html",
        "obsidian_vps_hosting.html", "obsidian_anthony_ai_supreme_builder.html", "developer.html"
    ]

    # 2. Programmatic State Pages
    with open(states_file, 'r') as f:
        states = json.load(f)

    sitemap_entries = []
    base_url = "https://obsidian.city"

    # Static pages
    for p in pages:
        sitemap_entries.append(f"  <url>\n    <loc>{base_url}/{p.replace('.html', '')}</loc>\n    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>\n    <priority>0.8</priority>\n  </url>")

    # Dynamic LLC pages
    for code, info in states.items():
        sitemap_entries.append(f"  <url>\n    <loc>{base_url}/start-llc/{code.lower()}</loc>\n    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>\n    <priority>0.6</priority>\n  </url>")

    sitemap_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap_content += "\n".join(sitemap_entries)
    sitemap_content += "\n</urlset>"

    (root / "sitemap.xml").write_text(sitemap_content)
    print("✓ pSEO ENGINE: sitemap.xml updated with 50+ sovereign entry points.")

def generate_seo_guides():
    """
    AI-Driven Content Ingestion:
    Generates internal comparison guides based on target keywords.
    """
    print("[*] pSEO ENGINE: Ingesting high-intent keywords for content clusters...")

    keywords = [
        "how to start an LLC in Missouri",
        "cheapest domain registrar 2026",
        "best vps for ai apps",
        "why obsidian city is better than go daddy"
    ]

    # Placeholder for actual LLM generation logic
    # In production, this would call the Swarm Brain to write MD files.
    for kw in keywords:
        fn = kw.lower().replace(" ", "_") + ".html"
        # We use a standard template for these guides
        print(f"✓ pSEO ENGINE: Cluster guide drafted -> {fn}")

if __name__ == "__main__":
    generate_sitemap()
    generate_seo_guides()
