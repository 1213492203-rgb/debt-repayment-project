"""
Generate 5 Fiverr Gig cover images (1280x769 PNG)
using Python Pillow — no external dependencies needed.
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT_DIR = r"C:/Users/Administrator/debt-repayment-project/products/04-gig-covers"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1280, 769

GIG_COVERS = [
    {
        "filename": "01-website-dev",
        "title": "Build Your Website",
        "subtitle": "in 2 Days",
        "tags": "Next.js  ·  React  ·  TailwindCSS",
        "desc": "Professional & Responsive Design",
        "colors": ("#4F46E5", "#7C3AED"),  # Blue-Purple
    },
    {
        "filename": "02-automation-script",
        "title": "Automation Scripts",
        "subtitle": "Save Hours Every Week",
        "tags": "Python  ·  Web Scraping  ·  Data Processing",
        "desc": "Custom Scripts for Your Repetitive Tasks",
        "colors": ("#059669", "#0D9488"),  # Green-Teal
    },
    {
        "filename": "03-ppt-design",
        "title": "Stunning PowerPoint",
        "subtitle": "Presentation Design",
        "tags": "Business  ·  Pitch Deck  ·  Report",
        "desc": "Professional Slides with Custom Design",
        "colors": ("#DC2626", "#EA580C"),  # Red-Orange
    },
    {
        "filename": "04-wechat-mini",
        "title": "WeChat Mini Program",
        "subtitle": "Development",
        "tags": "WeChat  ·  E-commerce  ·  Payment",
        "desc": "Expand to China's WeChat Ecosystem",
        "colors": ("#2563EB", "#06B6D4"),  # Blue-Cyan
    },
    {
        "filename": "05-data-analysis",
        "title": "Data Analysis",
        "subtitle": "& Beautiful Reports",
        "tags": "Python  ·  Excel  ·  Charts  ·  Statistics",
        "desc": "Turn Raw Data Into Actionable Insights",
        "colors": ("#9333EA", "#C026D3"),  # Purple-Magenta
    },
]


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def make_gradient(w, h, color1, color2):
    """Create a linear gradient from top-left to bottom-right"""
    img = Image.new('RGBA', (w, h))
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)

    for y in range(h):
        for x in range(w):
            # Diagonal gradient
            ratio = (x / w + y / h) / 2.0
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            img.putpixel((x, y), (r, g, b, 255))
    return img


def draw_icon_shapes(draw, w, h, color):
    """Draw abstract geometric shapes as design elements"""
    alpha = 30  # semi-transparent
    r, g, b = hex_to_rgb(color)

    # Top-right circle
    cx, cy = w - 80, 120
    for radius in range(120, 40, -20):
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            fill=(r, g, b, alpha), outline=None
        )

    # Bottom-left circles
    for i, (cx, cy, r) in enumerate([(100, h - 100, 80), (180, h - 160, 50)]):
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(r, g, b, alpha + 10), outline=None
        )

    # Code-like decorative lines in bottom right
    for i in range(4):
        y_pos = h - 60 - i * 22
        line_w = 180 + i * 40
        draw.rounded_rectangle(
            [w - line_w - 40, y_pos, w - 40, y_pos + 8],
            radius=4, fill=(r, g, b, alpha + 15)
        )

    # Small dots grid pattern (top area)
    for x in range(80, w - 80, 60):
        for y in range(30, 200, 50):
            draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 255, 255, 20))


def draw_cover(gig_data):
    """Generate one cover image"""
    img = make_gradient(W, H, gig_data["colors"][0], gig_data["colors"][1])
    draw = ImageDraw.Draw(img, 'RGBA')

    # Decorative elements
    draw_icon_shapes(draw, W, H, "#FFFFFF")

    # Try to load a nice font, fallback to default
    font_paths = [
        "C:/Windows/Fonts/seguiemj.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/msgothic.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]

    title_font = None
    subtitle_font = None
    tag_font = None
    desc_font = None

    for fp in font_paths:
        if os.path.exists(fp):
            try:
                title_font = ImageFont.truetype(fp, 72)
                subtitle_font = ImageFont.truetype(fp, 52)
                tag_font = ImageFont.truetype(fp, 28)
                desc_font = ImageFont.truetype(fp, 22)
                break
            except Exception:
                continue

    if title_font is None:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        tag_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()

    # Center content block
    center_x, center_y = W // 2, H // 2

    # Title
    title_bbox = draw.textbbox((0, 0), gig_data["title"], font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(
        (center_x - title_w // 2, center_y - 120),
        gig_data["title"], fill=(255, 255, 255, 255), font=title_font
    )

    # Subtitle
    sub_bbox = draw.textbbox((0, 0), gig_data["subtitle"], font=subtitle_font)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(
        (center_x - sub_w // 2, center_y - 30),
        gig_data["subtitle"], fill=(255, 255, 255, 220), font=subtitle_font
    )

    # Tags (bottom)
    tag_bbox = draw.textbbox((0, 0), gig_data["tags"], font=tag_font)
    tag_w = tag_bbox[2] - tag_bbox[0]
    # Semi-transparent background for tags
    draw.rounded_rectangle(
        [center_x - tag_w // 2 - 30, center_y + 50,
         center_x + tag_w // 2 + 30, center_y + 95],
        radius=20, fill=(255, 255, 255, 30)
    )
    draw.text(
        (center_x - tag_w // 2, center_y + 55),
        gig_data["tags"], fill=(255, 255, 255, 230), font=tag_font
    )

    # Description line
    desc_bbox = draw.textbbox((0, 0), gig_data["desc"], font=desc_font)
    desc_w = desc_bbox[2] - desc_bbox[0]
    draw.text(
        (center_x - desc_w // 2, center_y + 115),
        gig_data["desc"], fill=(255, 255, 255, 180), font=desc_font
    )

    # Branding watermark
    draw.text((40, H - 40), "freelancer · Fiverr", fill=(255, 255, 255, 100), font=desc_font)

    # Save
    out_path = os.path.join(OUT_DIR, f"{gig_data['filename']}.png")
    img.save(out_path, "PNG")
    print(f"   ✅ {gig_data['filename']}.png ({os.path.getsize(out_path)//1024} KB)")
    return out_path


if __name__ == "__main__":
    print("Generating 5 Fiverr Gig cover images...")
    print(f"Output: {OUT_DIR}")
    print(f"Size: {W}x{H}")
    print()

    for i, gig in enumerate(GIG_COVERS):
        print(f"[{i+1}/5] {gig['title']} {gig['subtitle']}")
        draw_cover(gig)

    print(f"\n✅ All 5 covers generated!")
    print(f"📁 {OUT_DIR}")
