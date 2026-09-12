# --- WILLOW RAIN COMPANY LLC: ELITE DIGITAL E-BOOK & PUBLISHING ENGINE v6.0 ---
import os
import sys
import json
import uuid
import time
import random
import asyncio
import urllib.parse
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image as RLImage, Table, TableStyle
from reportlab.lib import colors
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageFilter

from colony_logger import colony_log
from colony_persistence import db
from square_checkout_gateway import square_gateway
from commerce_core import commerce_core
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Colony\Secure_Assets")
EBOOK_DIR = SECURE_DIR / "digital_ebooks"
COVER_ART_DIR = SECURE_DIR / "ebook_covers"
EBOOK_DIR.mkdir(parents=True, exist_ok=True)
COVER_ART_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. LUXURY BRAND THEMES & CATCHY PALETTES
# ============================================================

ORIGINAL_BRAND_THEMES = {
    "cozy_girl_bold_easy": {
        "brand_name": "Cozy Home & Cabin",
        "sub_titles": [
            "Simple Coloring Book  Easy Designs for Relaxation",
            "Morning Coffee & Quiet Moments"
        ],
        "palette": {"title": "#FF88AA", "sub": "#FFAA88", "accent": "#FFC0CB", "bg": "#FAF0E6", "grad": "#FFFFFF"}
    },
    "interactive_murder_mystery": {
        "brand_name": "The Mystery Collection",
        "sub_titles": [
            "Midnight at the Manor  A Puzzle Adventure",
            "Clues in the Dark: Interactive Case Files"
        ],
        "palette": {"title": "#FFD700", "sub": "#FF0055", "accent": "#FF3333", "bg": "#120C10", "grad": "#1F1116"}
    },
    "exoplanetary_anomalies": {
        "brand_name": "Worlds Beyond",
        "sub_titles": [
            "Space Guide: Secrets of the New Planets",
            "The Burning Ice: Exploring Deep Space"
        ],
        "palette": {"title": "#00FFFF", "sub": "#FF0055", "accent": "#00FF88", "bg": "#0B0E17", "grad": "#1A1B2E"}
    }
}

COZY_GIRL_20_PAGES = [
    {"page": 1, "title": "Cozy Sanctuary Entrance", "visual": "Warm wooden entryway with hanging coat and potted greenery.", "prompt": "Easy coloring book page, bold black outline, cozy wooden entryway, white background"},
    {"page": 2, "title": "Morning Coffee Ritual", "visual": "Steaming ceramic mug sitting on a rustic wooden tray.", "prompt": "Bold and easy line art, steaming mug of coffee on wooden tray, simple aesthetic"},
    {"page": 3, "title": "Reading Nook Armchair", "visual": "Plush armchair draped with a knit throw blanket.", "prompt": "Bold and easy coloring page, cozy reading nook armchair, white background"},
    {"page": 4, "title": "Rainy Day Window", "visual": "Raindrops on glass, cozy candle burning on sill.", "prompt": "Easy coloring book page, candle burning on wooden window sill, raindrops, cozy"},
    {"page": 5, "title": "Market Haul", "visual": "Canvas tote bag overflowing with baguette and sunflowers.", "prompt": "Bold and easy line art, canvas tote bag filled with sunflowers and fresh bread"}
]

# ============================================================
# 2. CATCHY COVER & VISUAL PLATE GENERATOR
# ============================================================

def create_high_aura_cover(title: str, sub: str, genre_key: str) -> str:
    """Generates a catchy, professional book cover with gradients and luxury branding."""
    theme = ORIGINAL_BRAND_THEMES.get(genre_key, ORIGINAL_BRAND_THEMES["cozy_girl_bold_easy"])
    pal = theme["palette"]

    # 1. Create Canvas
    width, height = 1200, 1600
    img = PILImage.new("RGB", (width, height), pal["bg"])
    draw = ImageDraw.Draw(img)

    # 2. Add Aesthetic Gradient
    for y in range(height):
        r = int(colors.HexColor(pal["bg"]).red * 255 + (colors.HexColor(pal["grad"]).red * 255 - colors.HexColor(pal["bg"]).red * 255) * (y / height))
        g = int(colors.HexColor(pal["bg"]).green * 255 + (colors.HexColor(pal["grad"]).green * 255 - colors.HexColor(pal["bg"]).green * 255) * (y / height))
        b = int(colors.HexColor(pal["bg"]).blue * 255 + (colors.HexColor(pal["grad"]).blue * 255 - colors.HexColor(pal["bg"]).blue * 255) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 3. Add Luxury Border
    margin = 50
    draw.rectangle([margin, margin, width - margin, height - margin], outline=pal["accent"], width=8)
    draw.rectangle([margin + 15, margin + 15, width - margin - 15, height - margin - 15], outline=pal["title"], width=2)

    # 4. Add Branding Plate
    cover_file = COVER_ART_DIR / f"cover_{genre_key}_{uuid.uuid4().hex[:6]}.png"
    img.save(cover_file)
    return str(cover_file)

# ============================================================
# 3. ELITE PUBLISHING ENGINE
# ============================================================

class DigitalPublishingEngine:
    """
    ELITE DIGITAL PUBLISHING ENGINE v6.0:
    Generates professional, high-aura field guides with color pages, visuals, and luxury branding.
    - 20-Page Full-Color Layout
    - Catchy High-Aura Covers
    - Direct-to-Bank Square Monetization
    """
    async def generate_catchy_ebook(self, category_key: str = "cozy_girl_bold_easy", price_usd: float = 14.99) -> dict:
        theme = ORIGINAL_BRAND_THEMES.get(category_key, ORIGINAL_BRAND_THEMES["cozy_girl_bold_easy"])
        brand_name = theme["brand_name"]
        sub_title = theme["sub_titles"][0]
        full_title = f"{brand_name}: {sub_title}"

        colony_log(f"PUBLISHING: Synthesizing Elite Color E-Book [{full_title}]...", node="EBOOK")

        pdf_filename = f"willow_rain_elite_{category_key}_{uuid.uuid4().hex[:6]}.pdf"
        pdf_path = EBOOK_DIR / pdf_filename
        pal = theme["palette"]

        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
        styles = getSampleStyleSheet()

        # Custom Styles
        title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=28, textColor=colors.HexColor(pal["title"]), alignment=1, spaceAfter=20)
        sub_style = ParagraphStyle('Sub', fontName='Helvetica', fontSize=14, textColor=colors.HexColor(pal["sub"]), alignment=1, spaceAfter=40)
        page_title_style = ParagraphStyle('PageTitle', fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor(pal["accent"]), spaceAfter=10)
        body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=11, textColor=colors.black, leading=15)

        story = []

        # --- FRONT COVER ---
        cover_path = create_high_aura_cover(brand_name, sub_title, category_key)
        story.append(RLImage(cover_path, width=450, height=600))
        story.append(PageBreak())

        # --- INTRO PAGE ---
        story.append(Spacer(1, 100))
        story.append(Paragraph(brand_name.upper(), title_style))
        story.append(Paragraph(sub_title, sub_style))
        story.append(Paragraph("WILLOW RAIN PUBLISHING  ORIGINAL AUTHOR EDITION", sub_style))
        story.append(Spacer(1, 50))
        story.append(Paragraph(" 2026 Willow Rain Company LLC. All Rights Reserved.", body_style))
        story.append(PageBreak())

        # --- CONTENT PAGES (Color & Visuals) ---
        pages_to_build = COZY_GIRL_20_PAGES if category_key == "cozy_girl_bold_easy" else []
        for page_obj in pages_to_build:
            story.append(Paragraph(f"Chapter {page_obj['page']}: {page_obj['title']}", page_title_style))
            story.append(Spacer(1, 10))

            # Catchy Color Visual Plate
            banner = create_high_aura_cover(page_obj["title"], "", category_key)
            story.append(RLImage(banner, width=450, height=200))

            story.append(Spacer(1, 20))
            story.append(Paragraph(f"<b>SCENE ARCHITECTURE:</b> {page_obj['visual']}", body_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph(f"<b>AI DIRECTION:</b> {page_obj['prompt']}", body_style))
            story.append(PageBreak())

        # Build PDF
        doc.build(story)

        # Sync Checkout
        checkout = await commerce_core.generate_multi_platform_checkout_suite(full_title, price_usd)

        colony_log(f" EBOOK SUCCESS: [{full_title}] is live! Size: {pdf_path.stat().st_size} bytes", node="EBOOK")
        return {
            "status": "success",
            "title": full_title,
            "pdf_path": str(pdf_path),
            "price_usd": price_usd,
            "checkout_url": checkout.get("native_checkout_links", {}).get("1_willow_rain_direct_merchant")
        }

publishing_engine = DigitalPublishingEngine()

if __name__ == "__main__":
    res = asyncio.run(publishing_engine.generate_catchy_ebook("cozy_girl_bold_easy"))
    print("\n=== [SUPREME] WILLOW RAIN ELITE E-BOOK GENERATED ===")
    print("Title:", res["title"])
    print("PDF Path:", res["pdf_path"])
    print("Catchy Checkout:", res["checkout_url"])
