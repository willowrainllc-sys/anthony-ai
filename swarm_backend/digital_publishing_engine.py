# --- EMPIRE DIGITAL E-BOOK & PUBLISHING ENGINE v5.0 (20-PAGE COZY COLORBOOK & MURDER MYSTERY EDITION) ---
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
from PIL import Image as PILImage, ImageDraw

from swarm_logger import swarm_log
from swarm_persistence import db
from square_checkout_gateway import square_gateway
from commerce_core import commerce_core
from science_randomizer import science_randomizer
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\AnthonyAi_Swarm\Secure_Assets")
EBOOK_DIR = SECURE_DIR / "digital_ebooks"
COVER_ART_DIR = SECURE_DIR / "ebook_covers"
EBOOK_DIR.mkdir(parents=True, exist_ok=True)
COVER_ART_DIR.mkdir(parents=True, exist_ok=True)

# ORIGINAL WILLOW RAIN BRAND THEMES & TITLES
ORIGINAL_BRAND_THEMES = {
    "cozy_girl_bold_easy": {
        "brand_name": "WILLOW RAIN: Sanctuary & Hearth",
        "sub_titles": [
            "Bold & Easy Aesthetic Colorbook — Homebody Vibes & Cabin Life (20 Page Full Edition)",
            "Midnight Cabin & Golden Tea — Cozy Relaxation Edition",
            "Vintage Pantry & Wild Herbarium — Mindful Evening Journal"
        ],
        "palette": {"title_color": "#FF88AA", "sub_color": "#FFAA88", "border_color": "#FFC0CB", "bg": "#FAF0E6"}
    },
    "interactive_murder_mystery": {
        "brand_name": "WILLOW RAIN: The Blackwood Dossier",
        "sub_titles": [
            "Interactive Cold Case & Deduction File #1 — Midnight Manor Affair",
            "Silent Manor at Midnight — Interactive Murder Mystery & Logic Puzzles",
            "Redacted Evidence Vault — Noir Investigator Cluebook"
        ],
        "palette": {"title_color": "#FFD700", "sub_color": "#FF0055", "border_color": "#FF3333", "bg": "#120C10"}
    },
    "exoplanetary_anomalies": {
        "brand_name": "WILLOW RAIN: Starlight Horizon",
        "sub_titles": [
            "Deep Space Field Guide & JWST Exoplanet Atlas",
            "The Burning Ice Worlds — Unclassified Celestial Dossier"
        ],
        "palette": {"title_color": "#00FFFF", "sub_color": "#FF0055", "border_color": "#00FF88", "bg": "#0B0E17"}
    }
}

COZY_GIRL_20_PAGES = [
    {"page": 1, "title": "Cozy Sanctuary Entrance", "visual": "Warm wooden entryway with hanging coat, woven mat, and potted greenery.", "prompt": "Easy coloring book page, bold black outline, cozy wooden entryway with coat rack and potted plants, white background --ar 4:5"},
    {"page": 2, "title": "Morning Coffee Ritual", "visual": "Steaming ceramic mug sitting on a rustic wooden tray beside an open journal.", "prompt": "Bold and easy line art coloring page, steaming mug of coffee on wooden tray, simple aesthetic, clean lines, white background, no gray tones --ar 4:5"},
    {"page": 3, "title": "Reading Nook Armchair", "visual": "Plush armchair draped with a knit throw blanket next to a sunlit window.", "prompt": "Bold and easy coloring page, thick black lines, cozy reading nook armchair with throw blanket, white background, zero shading --ar 4:5"},
    {"page": 4, "title": "Rainy Day Window", "visual": "Raindrops on glass, cozy candle burning on sill, autumn leaves falling outside.", "prompt": "Easy coloring book page, bold black outline, candle burning on wooden window sill, raindrops on window pane, falling autumn leaves, cozy atmosphere, white background --ar 4:5"},
    {"page": 5, "title": "Market Haul", "visual": "Canvas tote bag overflowing with baguette, sunflowers, and apple butter.", "prompt": "Bold and easy line art coloring page, canvas tote bag filled with sunflowers and fresh bread, simple aesthetic, clean lines, white background, no gray tones --ar 4:5"},
    {"page": 6, "title": "The Rainy Day Sweater", "visual": "Chunky knit sweater on wooden hanger surrounded by tiny leaves.", "prompt": "Bold and easy coloring page, thick black lines, chunky knit sweater on hanger, autumn leaves, simple outlines, white background, no shading --ar 4:5"},
    {"page": 7, "title": "Bakery Treats", "visual": "Plate stacked high with frosted cinnamon rolls, jar of icing, and fork.", "prompt": "Bold and easy line art coloring page, plate of fresh cinnamon rolls, simple aesthetic, clean lines, white background, no gray tones --ar 4:5"},
    {"page": 8, "title": "Bedtime Routine", "visual": "Nightstand with glowing lamp, journal with pen, and glass of water.", "prompt": "Simple coloring page for adults, bold lines, cozy bedroom nightstand with lamp and journal, clean line art, white background, no gradients --ar 4:5"},
    {"page": 9, "title": "Forest Forage", "visual": "Collection of wild mushrooms, acorns, and pinecones neatly arranged.", "prompt": "Easy coloring book page, bold black outline, mushrooms, acorns, and pinecones, cozy autumn nature, white background --ar 4:5"},
    {"page": 10, "title": "The Porch Steps", "visual": "Front porch step lined with stacked pumpkins and a welcome mat.", "prompt": "Bold and easy coloring page, clean black lines, minimal detail, stacked pumpkins on front steps, cozy porch theme, white background, no shading --ar 4:5"},
    {"page": 11, "title": "Hot Cocoa Station", "visual": "Jar of marshmallows next to a mug filled with cocoa and cinnamon stick.", "prompt": "Bold and easy coloring page, thick black lines, hot chocolate mug with marshmallows, simple outlines, white background, zero shading --ar 4:5"},
    {"page": 12, "title": "Cozy Boots", "visual": "Pair of classic leather rain boots with fuzzy wool socks peeking out.", "prompt": "Simple coloring page for adults, bold lines, autumn rain boots with thick wool socks, clean line art, white background, no gradients --ar 4:5"},
    {"page": 13, "title": "The Bookstore Corner", "visual": "Overflowing bookshelf stacked with books and cozy armchair.", "prompt": "Easy coloring book page, bold black outline, simple bookshelf stacked with books, cozy atmosphere, white background --ar 4:5"},
    {"page": 14, "title": "Apple Cider Donuts", "visual": "Paper bag crinkled open revealing sugar-dusted cider donuts inside.", "prompt": "Bold and easy line art coloring page, apple cider donuts inside paper bag, simple aesthetic, clean lines, white background, no gray tones --ar 4:5"},
    {"page": 15, "title": "Desk Haven", "visual": "Clean wooden desk with laptop displaying fireplace video and plant.", "prompt": "Bold and easy coloring page, clean black lines, minimal detail, cozy desk setup with laptop and small plant, white background, no shading --ar 4:5"},
    {"page": 16, "title": "Scarf Weather", "visual": "Thick patterned flannel scarf folded neatly next to warm mittens.", "prompt": "Bold and easy coloring page, thick black lines, folded plaid scarf and mittens, simple outlines, white background, zero shading --ar 4:5"},
    {"page": 17, "title": "Forest Friends", "visual": "Tiny stylized hedgehog sleeping soundly under giant maple leaf.", "prompt": "Simple coloring page for adults, bold lines, cute hedgehog sleeping under a leaf, clean line art, white background, no gradients --ar 4:5"},
    {"page": 18, "title": "Baking Apple Pie", "visual": "Unbaked pie with lattice crust sitting next to sliced apples.", "prompt": "Easy coloring book page, bold black outline, apple pie with lattice crust, autumn baking, white background --ar 4:5"},
    {"page": 19, "title": "Blanket Pile", "visual": "Wicker basket overflowing with rolled-up fleece and knit blankets.", "prompt": "Bold and easy line art coloring page, basket filled with cozy blankets, simple aesthetic, clean lines, white background, no gray tones --ar 4:5"},
    {"page": 20, "title": "Starry Autumn Night", "visual": "Crescent moon surrounded by stars through bare tree branches.", "prompt": "Bold and easy coloring page, thick black lines, crescent moon and stars through autumn tree branches, simple outlines, white background, zero shading --ar 4:5"}
]

def create_color_cover_banner_png(title: str, genre_key: str = "cozy_girl_bold_easy") -> str:
    palette = ORIGINAL_BRAND_THEMES.get(genre_key, ORIGINAL_BRAND_THEMES["cozy_girl_bold_easy"])["palette"]
    width, height = 1200, 600

    img = PILImage.new("RGB", (width, height), palette["bg"])
    draw = ImageDraw.Draw(img)

    draw.rectangle([20, 20, width - 20, height - 20], outline=palette["border_color"], width=4)
    draw.rectangle([35, 35, width - 35, height - 35], outline=palette["sub_color"], width=1)

    cover_file = COVER_ART_DIR / f"cover_{genre_key}_{uuid.uuid4().hex[:6]}.png"
    img.save(cover_file)
    return str(cover_file)

class DigitalPublishingEngine:
    """
    DIGITAL PUBLISHING ENGINE v5.0 (WILLOW RAIN ORIGINAL BRANDS & 20-PAGE COLORBOOK):
    Generates high-royalties Amazon KDP, Payhip & Square E-Books under custom Willow Rain brand names:
    1. 'WILLOW RAIN: Sanctuary & Hearth' (20-Page Full Cozy Homebody Colorbook).
    2. 'WILLOW RAIN: The Blackwood Dossier' (Interactive Murder Mystery & Logic Casebooks).
    3. 'WILLOW RAIN: Starlight Horizon' (Deep Space & Exoplanet Atlases).
    """
    async def generate_pdf_ebook(self, category_key: str = "cozy_girl_bold_easy", price_usd: float = 14.99) -> dict:
        theme_info = ORIGINAL_BRAND_THEMES.get(category_key, ORIGINAL_BRAND_THEMES["cozy_girl_bold_easy"])
        brand_title = theme_info["brand_name"]
        sub_title = theme_info["sub_titles"][0]
        full_title = f"{brand_title}: {sub_title}"

        swarm_log(f"PUBLISHING: Synthesizing 20-Page Original Brand E-Book [{full_title}] (${price_usd})...", node="EBOOK")

        pdf_filename = f"willow_rain_20page_ebook_{category_key}_{uuid.uuid4().hex[:6]}.pdf"
        pdf_path = EBOOK_DIR / pdf_filename

        palette = theme_info["palette"]

        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('CoverTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, leading=30, textColor=colors.HexColor(palette["title_color"]), alignment=1, spaceAfter=15)
        subtitle_style = ParagraphStyle('CoverSub', parent=styles['Normal'], fontName='Helvetica', fontSize=13, leading=18, textColor=colors.HexColor(palette["sub_color"]), alignment=1, spaceAfter=30)
        chapter_title_style = ParagraphStyle('ChapTitle', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor(palette["border_color"]), spaceBefore=14, spaceAfter=8)
        body_style = ParagraphStyle('BodyDark', parent=styles['BodyText'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor('#12141C'), spaceAfter=8)
        prompt_style = ParagraphStyle('PromptBox', parent=styles['Italic'], fontName='Helvetica-Oblique', fontSize=9, leading=13, textColor=colors.HexColor('#0055FF'), spaceAfter=12)

        story = []

        # COVER PAGE
        cover_banner = create_color_cover_banner_png(full_title, genre_key=category_key)
        if os.path.exists(cover_banner):
            story.append(RLImage(cover_banner, width=500, height=250))
            story.append(Spacer(1, 20))

        story.append(Paragraph("WILLOW RAIN PUBLISHING • ORIGINAL AUTHOR EDITION", subtitle_style))
        story.append(Paragraph(f"<b>{brand_title.upper()}</b>", title_style))
        story.append(Paragraph(f"<i>{sub_title}</i>", subtitle_style))
        story.append(Spacer(1, 40))
        story.append(Paragraph("Willow Rain Company LLC • All Rights Reserved", subtitle_style))
        story.append(PageBreak())

        # 20-PAGE FULL COZY GIRL EDITION
        if category_key == "cozy_girl_bold_easy":
            for page_obj in COZY_GIRL_20_PAGES:
                p_num = page_obj["page"]
                p_title = page_obj["title"]
                p_vis = page_obj["visual"]
                p_prompt = page_obj["prompt"]

                story.append(Paragraph(f"Page {p_num}: {p_title}", chapter_title_style))
                story.append(Paragraph(f"<b>Visual Scene:</b> {p_vis}", body_style))
                story.append(Paragraph(f"<b>Midjourney / AI Prompt:</b> {p_prompt}", prompt_style))

                banner = create_color_cover_banner_png(p_title, genre_key=category_key)
                if os.path.exists(banner):
                    story.append(RLImage(banner, width=480, height=100))
                    story.append(Spacer(1, 10))

                story.append(Spacer(1, 15))

        # Build PDF Document
        doc.build(story)

        # Generate Multi-Platform Native Checkout Suite
        checkout_suite = await commerce_core.generate_multi_platform_checkout_suite(full_title, price_usd=price_usd)

        swarm_log(f"✓ 20-PAGE EBOOK SUCCESS: Generated {pdf_filename} ({pdf_path.stat().st_size} bytes)", node="EBOOK")

        return {
            "status": "success",
            "title": full_title,
            "brand_name": brand_title,
            "category": category_key,
            "pdf_path": str(pdf_path),
            "pdf_size_bytes": pdf_path.stat().st_size,
            "price_usd": price_usd,
            "multi_platform_checkout_suite": checkout_suite.get("native_checkout_links"),
            "merchant": "Willow Rain Company LLC"
        }

publishing_engine = DigitalPublishingEngine()

if __name__ == "__main__":
    res_cozy20 = asyncio.run(publishing_engine.generate_pdf_ebook("cozy_girl_bold_easy", 14.99))
    print("20-PAGE COZY GIRL EBOOK RESULT:")
    print(json.dumps(res_cozy20, indent=2))
