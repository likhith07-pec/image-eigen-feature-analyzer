"""
generate_folder_structure_images.py
Generates a print-ready, high-contrast, professional image of the project directory structure
tailored specifically for academic project reports, viva submissions, and printouts.
- docs/ folder completely removed as requested
- Pure white background for crisp paper printing (saves printer ink, 100% sharp text)
- High-contrast typography (Deep Navy / Black) with large legible font sizes
- Vector tree connector lines and folder icons
- 300 DPI resolution formatted for MS Word / PDF A4 reports
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    fonts_dir = "C:\\Windows\\Fonts"
    
    def try_font(names, size):
        for name in names:
            p = os.path.join(fonts_dir, name)
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    return {
        "report_title": try_font(["arialbd.ttf", "segoeuib.ttf"], 26),
        "report_sub":   try_font(["arial.ttf", "segoeui.ttf"], 15),
        "col_header":   try_font(["arialbd.ttf", "segoeuib.ttf"], 14),
        "code_bold":    try_font(["consolab.ttf", "arialbd.ttf"], 16),
        "code":         try_font(["consola.ttf", "arial.ttf"], 15),
        "desc":         try_font(["arial.ttf", "segoeui.ttf"], 15),
        "badge":        try_font(["arialbd.ttf", "segoeuib.ttf"], 11),
        "footer":       try_font(["ariali.ttf", "segoeui.ttf"], 13),
    }

# Directory tree items (docs/ removed completely)
ITEMS = [
    # (is_dir, indent, name, category, role_description)
    (True,  0, "ImageEigenAnalyzer/", "ROOT DIRECTORY", "Project Root — Linear Algebra Image Transformation & Eigen-Feature Analyzer"),
    (False, 1, "manage.py", "DJANGO CLI", "Django execution utility for running server, migrations & diagnostic checks"),
    (False, 1, "requirements.txt", "DEPENDENCIES", "Python libraries: Django, NumPy, SciPy, Pillow, Matplotlib, Sarvam AI"),
    (False, 1, "db.sqlite3", "DATABASE", "Local database storage for user sessions and analysis logs"),
    (False, 1, ".env.example", "CONFIG", "Environment variables template for API credentials & debug settings"),
    
    (True,  1, "ImageEigenAnalyzer/", "CONFIG PACKAGE", "Django Project Core Configuration & Global Routing"),
    (False, 2, "settings.py", "CONFIG", "Application registrations, media/static directories & pipeline settings"),
    (False, 2, "urls.py", "ROUTER", "Root URL routing and development media server endpoints"),
    (False, 2, "asgi.py / wsgi.py", "GATEWAY", "Standard asynchronous & synchronous Web Server Gateway Interfaces"),

    (True,  1, "analyzer/", "APPLICATION", "Core Computational Application & Mathematical Engine"),
    (False, 2, "views.py", "CONTROLLER", "HTTP controller: accepts image upload, invokes math pipeline & returns view"),
    (False, 2, "math_pipeline.py", "PIPELINE", "Master LA pipeline orchestrating ingest, covariance, eigen & reconstruction"),
    (False, 2, "image_processing.py", "IMAGE PROCESSING", "Converts input image to grayscale, resizes to 64x64 and normalizes to [0,1]"),
    (False, 2, "matrix_analysis.py", "LINEAR ALGEBRA", "Computes matrix rank and generates symmetric covariance matrix C = A^T A"),
    (False, 2, "eigen_analysis.py", "LINEAR ALGEBRA", "Symmetric eigensolver (eigh), descending eigenvalue sort & subspace selection"),
    (False, 2, "reconstruction.py", "LINEAR ALGEBRA", "Orthogonal projection (P = A V_k) & rank-k reconstruction (A_k = P V_k^T)"),
    (False, 2, "visualization.py", "VISUALIZATION", "Generates pixel heatmaps, eigenvalue spectrum plots & Frobenius error curves"),
    (False, 2, "sarvam_ai.py", "AI AUDIO", "Sarvam AI voice generation service for interactive audio narration"),
    (False, 2, "urls.py", "ROUTER", "Application URL route endpoints for dashboard, uploads and audio"),
    (False, 2, "forms.py", "VALIDATION", "Image upload form validation rules and file type constraints"),
    (False, 2, "services.py", "SERVICE", "Service layer connecting Django views with underlying LA modules"),

    (True,  2, "templates/analyzer/", "TEMPLATES", "HTML Templates for Frontend Presentation"),
    (False, 3, "home.html", "UI DASHBOARD", "Main interactive dashboard with upload cards, matrix grids & audio player"),
    (False, 3, "table_preview.html", "MODAL VIEW", "Interactive numerical table inspector for raw matrix & eigenvector values"),

    (True,  2, "static/analyzer/", "STATIC ASSETS", "Client-Side Stylesheets, Scripts & Animations"),
    (False, 3, "styles.css", "STYLING", "Responsive glassmorphism UI design, layout grids and CSS variables"),
    (False, 3, "base.css", "DESIGN TOKENS", "Typography tokens, theme variables and CSS reset baseline"),
    (False, 3, "app.js", "JAVASCRIPT", "Client-side interactivity, async pipeline requests and slider controls"),
    (False, 3, "motion.js", "ANIMATION", "Smooth page transitions, loading spinners and micro-animations"),

    (True,  1, "media/", "STORAGE", "Runtime storage directory for uploaded user images & generated plots"),
]

def draw_folder_icon(draw, x, y, color):
    # Sharp folder icon
    w, h = 16, 12
    draw.polygon([(x, y+2), (x+6, y+2), (x+8, y+4), (x+w, y+4), (x+w, y+h), (x, y+h)], fill=color)
    draw.rectangle([x, y+4, x+w, y+h], fill=color)

def draw_file_icon(draw, x, y, color):
    # Sharp document icon with folded corner
    w, h = 11, 14
    c = 4
    draw.polygon([(x, y), (x+w-c, y), (x+w, y+c), (x+w, y+h), (x, y+h)], fill=color)
    draw.polygon([(x+w-c, y), (x+w, y+c), (x+w-c, y+c)], fill=(220, 225, 230, 255))

def render_report_image(fonts, output_path):
    width = 1800
    header_height = 130
    tbl_header_height = 36
    row_height = 42
    footer_height = 60
    total_height = header_height + tbl_header_height + (len(ITEMS) * row_height) + footer_height + 40

    # Crisp pure white background
    img = Image.new("RGB", (width, total_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    margin_x = 30
    margin_y = 25
    content_w = width - (margin_x * 2)
    content_h = total_height - (margin_y * 2)

    # Clean outer border for academic report framing
    draw.rounded_rectangle(
        [margin_x, margin_y, margin_x + content_w, margin_y + content_h],
        radius=8,
        fill=(255, 255, 255),
        outline=(51, 65, 85),
        width=2
    )

    # Header Box (Deep Navy accent)
    hdr_box_h = 75
    draw.rounded_rectangle(
        [margin_x, margin_y, margin_x + content_w, margin_y + hdr_box_h],
        radius=8,
        fill=(15, 23, 42),
        outline=(15, 23, 42),
        width=1
    )
    # Square out bottom rounded corners of the header
    draw.rectangle(
        [margin_x, margin_y + hdr_box_h - 10, margin_x + content_w, margin_y + hdr_box_h],
        fill=(15, 23, 42)
    )

    # Title and Subtitle in Header
    draw.text(
        (margin_x + 30, margin_y + 14),
        "Project Architecture & Directory Hierarchy",
        fill=(255, 255, 255),
        font=fonts["report_title"]
    )
    draw.text(
        (margin_x + 30, margin_y + 46),
        "Image Transformation and Eigen-Feature Analyzer (EigenLab) • Linear Algebra Computational System",
        fill=(203, 213, 225),
        font=fonts["report_sub"]
    )

    # Table Column Headers Bar
    col_y = margin_y + hdr_box_h + 12
    draw.rectangle([margin_x + 6, col_y, margin_x + content_w - 6, col_y + tbl_header_height], fill=(241, 245, 249))
    draw.line([margin_x + 6, col_y + tbl_header_height, margin_x + content_w - 6, col_y + tbl_header_height], fill=(203, 213, 225), width=1)
    
    col1_x = margin_x + 40
    col2_x = margin_x + 520
    col3_x = margin_x + 720

    draw.text((col1_x, col_y + 9), "DIRECTORY / FILE NAME", fill=(15, 23, 42), font=fonts["col_header"])
    draw.text((col2_x, col_y + 9), "COMPONENT TYPE", fill=(15, 23, 42), font=fonts["col_header"])
    draw.text((col3_x, col_y + 9), "MODULE RESPONSIBILITY & MATHEMATICAL ROLE", fill=(15, 23, 42), font=fonts["col_header"])

    # High-contrast badge color palettes for crisp printing
    badge_colors = {
        "ROOT DIRECTORY":    {"bg": (224, 231, 255), "fg": (30, 27, 75),  "border": (165, 180, 252)},
        "DJANGO CLI":        {"bg": (220, 252, 231), "fg": (20, 83, 45),  "border": (134, 239, 172)},
        "DEPENDENCIES":      {"bg": (241, 245, 249), "fg": (15, 23, 42),  "border": (203, 213, 225)},
        "DATABASE":          {"bg": (254, 243, 199), "fg": (120, 53, 15), "border": (253, 230, 138)},
        "CONFIG":            {"bg": (241, 245, 249), "fg": (30, 41, 59),  "border": (203, 213, 225)},
        "CONFIG PACKAGE":    {"bg": (224, 242, 254), "fg": (12, 74, 110), "border": (186, 230, 253)},
        "ROUTER":            {"bg": (243, 232, 255), "fg": (88, 28, 135), "border": (216, 180, 254)},
        "GATEWAY":           {"bg": (241, 245, 249), "fg": (51, 65, 85),  "border": (203, 213, 225)},
        "APPLICATION":       {"bg": (219, 234, 254), "fg": (30, 58, 138), "border": (147, 197, 253)},
        "CONTROLLER":        {"bg": (220, 252, 231), "fg": (20, 83, 45),  "border": (134, 239, 172)},
        "PIPELINE":          {"bg": (254, 235, 200), "fg": (154, 52, 18), "border": (251, 191, 36)},
        "IMAGE PROCESSING":  {"bg": (224, 242, 254), "fg": (3, 105, 161), "border": (125, 211, 252)},
        "LINEAR ALGEBRA":    {"bg": (243, 232, 255), "fg": (107, 33, 168),"border": (192, 132, 252)},
        "VISUALIZATION":     {"bg": (255, 241, 242), "fg": (159, 18, 57), "border": (253, 164, 175)},
        "AI AUDIO":          {"bg": (254, 243, 199), "fg": (146, 64, 14), "border": (252, 211, 77)},
        "VALIDATION":        {"bg": (241, 245, 249), "fg": (51, 65, 85),  "border": (203, 213, 225)},
        "SERVICE":           {"bg": (240, 253, 244), "fg": (22, 101, 52), "border": (187, 247, 208)},
        "TEMPLATES":         {"bg": (255, 241, 242), "fg": (190, 18, 60), "border": (254, 205, 211)},
        "UI DASHBOARD":      {"bg": (254, 226, 226), "fg": (153, 27, 27), "border": (252, 165, 165)},
        "MODAL VIEW":        {"bg": (254, 226, 226), "fg": (153, 27, 27), "border": (252, 165, 165)},
        "STATIC ASSETS":     {"bg": (240, 253, 250), "fg": (15, 118, 110),"border": (153, 246, 228)},
        "STYLING":           {"bg": (204, 251, 241), "fg": (17, 94, 89),  "border": (94, 234, 212)},
        "DESIGN TOKENS":     {"bg": (240, 253, 250), "fg": (15, 118, 110),"border": (204, 251, 241)},
        "JAVASCRIPT":        {"bg": (254, 252, 232), "fg": (133, 77, 14), "border": (253, 224, 71)},
        "ANIMATION":         {"bg": (254, 249, 195), "fg": (133, 77, 14), "border": (250, 204, 21)},
        "STORAGE":           {"bg": (241, 245, 249), "fg": (51, 65, 85),  "border": (203, 213, 225)},
    }

    start_y = col_y + tbl_header_height + 6
    line_connector_col = (148, 163, 184)

    for i, (is_dir, indent, name, cat_text, desc) in enumerate(ITEMS):
        y = start_y + (i * row_height)

        # Subtle zebra striping for high readability across wide page
        if i % 2 == 1:
            draw.rectangle(
                [margin_x + 6, y - 2, margin_x + content_w - 6, y + row_height - 4],
                fill=(248, 250, 252)
            )

        # Connector lines
        base_x = col1_x
        if indent > 0:
            for lvl in range(1, indent):
                col_line_x = base_x + (lvl * 26) - 13
                draw.line([col_line_x, y - 5, col_line_x, y + row_height - 5], fill=line_connector_col, width=1)
            
            node_x = base_x + (indent * 26) - 13
            draw.line([node_x, y - 5, node_x, y + 14], fill=line_connector_col, width=1)
            draw.line([node_x, y + 14, node_x + 10, y + 14], fill=line_connector_col, width=1)

        item_x = base_x + (indent * 26)

        # Draw icon
        if is_dir:
            folder_col = (180, 83, 9) if indent == 0 else (2, 132, 199)
            draw_folder_icon(draw, item_x, y + 7, folder_col)
            name_col = (2, 132, 199) if indent > 0 else (180, 83, 9)
            font_to_use = fonts["code_bold"]
        else:
            file_col = (100, 116, 139)
            draw_file_icon(draw, item_x + 2, y + 6, file_col)
            name_col = (15, 23, 42)
            font_to_use = fonts["code"]

        # Filename text
        text_x = item_x + 22
        draw.text((text_x, y + 4), name, fill=name_col, font=font_to_use)

        # Badge pill
        pal = badge_colors.get(cat_text, {"bg": (241, 245, 249), "fg": (51, 65, 85), "border": (203, 213, 225)})
        
        bbox = fonts["badge"].getbbox(cat_text)
        b_width = (bbox[2] - bbox[0]) + 18
        b_height = 22
        
        draw.rounded_rectangle(
            [col2_x, y + 4, col2_x + b_width, y + 4 + b_height],
            radius=4,
            fill=pal["bg"],
            outline=pal["border"],
            width=1
        )
        draw.text((col2_x + 9, y + 7), cat_text, fill=pal["fg"], font=fonts["badge"])

        # Description text (high contrast dark slate)
        draw.text((col3_x, y + 5), desc, fill=(30, 41, 59), font=fonts["desc"])

    # Footer section
    foot_y = total_height - margin_y - footer_height + 15
    draw.line([margin_x + 20, foot_y - 10, margin_x + content_w - 20, foot_y - 10], fill=(226, 232, 240), width=1)
    
    footer_text = "Figure 3.1: Academic Mini-Project Repository Structure and Architectural Component Map"
    draw.text((margin_x + 30, foot_y), footer_text, fill=(71, 85, 105), font=fonts["footer"])

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Report image saved successfully to: {output_path}")

if __name__ == "__main__":
    fonts = get_fonts()
    out_dir = r"c:\Users\ADMIN\Desktop\maths"
    
    report_path = os.path.join(out_dir, "folder_structure_report.png")
    academic_path = os.path.join(out_dir, "folder_structure_academic.png")
    
    render_report_image(fonts, report_path)
    render_report_image(fonts, academic_path)
