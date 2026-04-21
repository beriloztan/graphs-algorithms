"""
Recreate Beril Oztan CV with edits using ReportLab Platypus.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Image, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# 1. Register fonts
# ---------------------------------------------------------------------------
FONTS_DIR = r"C:\Windows\Fonts"

pdfmetrics.registerFont(TTFont("Arial",   os.path.join(FONTS_DIR, "arial.ttf")))
pdfmetrics.registerFont(TTFont("ArialBd", os.path.join(FONTS_DIR, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("ArialIt", os.path.join(FONTS_DIR, "ariali.ttf")))
pdfmetrics.registerFont(TTFont("ArialBI", os.path.join(FONTS_DIR, "arialbi.ttf")))
pdfmetrics.registerFontFamily(
    "Arial",
    normal="Arial",
    bold="ArialBd",
    italic="ArialIt",
    boldItalic="ArialBI",
)

# ---------------------------------------------------------------------------
# 2. Paths
# ---------------------------------------------------------------------------
PHOTO_PATH  = r"C:\Users\beril.oztan\Downloads\cv_photo_clean.jpg"
OUTPUT_PATH = r"C:\Users\beril.oztan\Downloads\Beril_OztanCV.pdf"

# ---------------------------------------------------------------------------
# 3. Page geometry
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4           # 595.28 x 841.89 pts
MARGIN_L = 1.8 * cm
MARGIN_R = 1.8 * cm
MARGIN_T = 1.5 * cm
MARGIN_B = 1.5 * cm

CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

# ---------------------------------------------------------------------------
# 4. Colour palette
# ---------------------------------------------------------------------------
BLACK       = colors.black
DARK_GRAY   = colors.HexColor("#222222")
MID_GRAY    = colors.HexColor("#555555")
RULE_COLOR  = colors.HexColor("#1a1a1a")

# ---------------------------------------------------------------------------
# 5. Style helpers
# ---------------------------------------------------------------------------
def ps(name, font="Arial", size=10, leading=None, textColor=DARK_GRAY,
       spaceAfter=0, spaceBefore=0, leftIndent=0, firstLineIndent=0,
       alignment=0, **kw):
    """Shorthand ParagraphStyle factory."""
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading or (size * 1.30),
        textColor=textColor,
        spaceAfter=spaceAfter,
        spaceBefore=spaceBefore,
        leftIndent=leftIndent,
        firstLineIndent=firstLineIndent,
        alignment=alignment,
        **kw,
    )

# Define all styles used in the CV
sNAME       = ps("NAME",    "ArialBd",  22, leading=26, textColor=BLACK, spaceAfter=2)
sSUBTITLE   = ps("SUB",     "ArialBd",  11, leading=14, textColor=BLACK, spaceAfter=4)
sCONTACT    = ps("CONTACT", "Arial",     8, leading=11, textColor=MID_GRAY, spaceAfter=0)
sSECHDR     = ps("SECHDR",  "ArialBd",  11, leading=14, textColor=BLACK,
                 spaceBefore=10, spaceAfter=3)
sJOBTITLE   = ps("JOBT",   "ArialBd",   9.5, leading=13, textColor=BLACK,
                 spaceBefore=6, spaceAfter=1)
sBODY       = ps("BODY",   "Arial",      9,  leading=13, textColor=DARK_GRAY,
                 spaceAfter=1)
sBULLET     = ps("BULL",   "Arial",      9,  leading=13, textColor=DARK_GRAY,
                 leftIndent=14, firstLineIndent=-10, spaceAfter=2)
sEDU_INST   = ps("EDUINST","ArialBd",    9.5, leading=13, textColor=BLACK,
                 spaceBefore=5, spaceAfter=1)
sSKILL      = ps("SKILL",  "Arial",      9,  leading=13, textColor=DARK_GRAY,
                 spaceAfter=2)
sLANG       = ps("LANG",   "Arial",      9,  leading=13, textColor=DARK_GRAY,
                 spaceAfter=2)
sCERT       = ps("CERT",   "Arial",      9,  leading=13, textColor=DARK_GRAY,
                 spaceAfter=2)

# ---------------------------------------------------------------------------
# 6. Helper flowables
# ---------------------------------------------------------------------------
def section_header(title):
    """Bold heading + full-width rule."""
    return [
        Paragraph(title, sSECHDR),
        HRFlowable(width="100%", thickness=1, color=RULE_COLOR, spaceAfter=4),
    ]


def bullet_para(text):
    """Single bullet point paragraph."""
    return Paragraph(f"\u2022&nbsp;&nbsp;{text}", sBULLET)


# ---------------------------------------------------------------------------
# 7. Header block (name + subtitle + contact + photo)
# ---------------------------------------------------------------------------
def build_header():
    """Returns a Table that acts as the header of the CV."""

    # Left column: name / subtitle / contact
    name_p     = Paragraph("Beril \u00d6ztan", sNAME)
    subtitle_p = Paragraph("Software and Industrial Engineering Student", sSUBTITLE)
    contact_p  = Paragraph(
        "beriloztan@hotmail.com&nbsp;&nbsp;|&nbsp;&nbsp;"
        "+90 530 855 2818&nbsp;&nbsp;|&nbsp;&nbsp;"
        "\u015ei\u015fli/\u0130stanbul&nbsp;&nbsp;|&nbsp;&nbsp;"
        "<a href=\"https://linkedin.com/in/beril-%C3%B6ztan-009946219\" color=\"#555555\">"
        "linkedin.com/in/beril-\u00f6ztan-009946219</a>",
        sCONTACT,
    )

    left_content = [name_p, subtitle_p, contact_p]

    # Right column: photo (square, ~2.5 cm)
    PHOTO_SIZE = 2.6 * cm
    photo = Image(PHOTO_PATH, width=PHOTO_SIZE, height=PHOTO_SIZE)

    # Put into a 2-column table
    col_left  = CONTENT_W - PHOTO_SIZE - 0.4 * cm
    col_right = PHOTO_SIZE + 0.4 * cm

    header_table = Table(
        [[left_content, photo]],
        colWidths=[col_left, col_right],
    )
    header_table.setStyle(TableStyle([
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",       (1, 0), (1, 0),   "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",(0, 0), (-1, -1), 0),
        ("TOPPADDING",  (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0,0), (-1, -1), 0),
    ]))
    return header_table


# ---------------------------------------------------------------------------
# 8. Helper: job title row (title left, date right-aligned)
# ---------------------------------------------------------------------------
def job_row(title_html, date_str, spaceBefore=6, left_frac=0.72):
    sDATE = ps(f"DATE_{date_str}", "Arial", 9, textColor=MID_GRAY, alignment=2,
               spaceBefore=spaceBefore)
    left  = Paragraph(title_html, ps(f"JT_{date_str}", "ArialBd", 9.5, leading=13,
                                     textColor=BLACK, spaceBefore=spaceBefore, spaceAfter=1))
    right = Paragraph(date_str, sDATE)
    tbl = Table([[left, right]], colWidths=[CONTENT_W * left_frac, CONTENT_W * (1 - left_frac)])
    tbl.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
    ]))
    return tbl


# ---------------------------------------------------------------------------
# 9. Experience section
# ---------------------------------------------------------------------------
def build_experience():
    items = []
    items += section_header("Experience")

    # --- Job 1 ---
    items.append(job_row(
        "<b>Long Term Intern,</b> <i>Kibar Holding \u2013 Assan Bili\u015fim</i>",
        "07/2025 \u2013 Present",
    ))
    bullets_job1 = [
        "Worked with DELMIA Quintiq (Dassault Syst\u00e8mes), an Advanced Planning and "
        "Scheduling (APS) solution, on industrial scale production planning and optimization.",
        "Gained hands on experience in decision support systems, data modeling, and "
        "optimization driven problem solving in real world manufacturing environments.",
        "Analyzed and modeled production data to support constraint based scheduling and "
        "decision making processes.",
        "Performed scenario based optimization by adjusting parameters such as processing "
        "times, priorities, and resource availability, and evaluated alternative production "
        "plans to identify bottlenecks and improve resource utilization.",
    ]
    for b in bullets_job1:
        items.append(bullet_para(b))

    # --- Job 2 ---
    items.append(job_row(
        "<b>Project Management Intern,</b> <i>Sca Social</i>",
        "02/2025 \u2013 03/2025",
    ))
    items.append(Paragraph(
        "Assisted in planning and executing digital campaign projects, tracked progress "
        "using project management tools, and supported cross functional communication to "
        "ensure timely delivery. Gained hands on experience in task coordination, stakeholder "
        "reporting, and agile methodology.",
        sBODY,
    ))

    return items


# ---------------------------------------------------------------------------
# 10. Education section
# ---------------------------------------------------------------------------
def build_education():
    items = []
    items += section_header("Education")

    # Bachelor – date right-aligned, wider left column to fit GPA on one line
    items.append(job_row(
        "<b>Bachelor of Software Engineering (full scholarship),</b> "
        "<i>Istinye University</i>&nbsp;&nbsp;&nbsp;GPA : 3.40",
        "2021 \u2013 2026",
        left_frac=0.82,
    ))

    # Minor (no separate date, part of same degree)
    items.append(Paragraph(
        "<b>Industrial Engineering (minor),</b> <i>Istinye University</i>",
        sEDU_INST,
    ))

    # 42 Istanbul – with 10pt top spacing and date right-aligned
    items.append(Spacer(1, 10))
    items.append(job_row(
        "<b>Piscine Student, 42 Istanbul</b>",
        "05/2024 \u2013 07/2024",
        spaceBefore=0,
    ))
    items.append(Paragraph(
        "Developed C language projects at 42 Istanbul, gaining proficiency in project "
        "management, communication, and team leadership.",
        sBODY,
    ))

    return items


# ---------------------------------------------------------------------------
# 10. Skills section
# ---------------------------------------------------------------------------
def build_skills():
    items = []
    items += section_header("Skills")

    skills_data = [
        ("Programming Languages :", "C, Python, C++, SQL"),
        ("Libraries &amp; Frameworks :", "UnityEditor, .NET, pandas, NumPy, Matplotlib"),
        ("Soft Skills :",
         "Communication Skills, Ability to Multitask, Coordination, Teamwork, "
         "Time Management, Strategic Thinking, Active Listening, Project Scheduling, "
         "Problem Solver, Report Writing"),
    ]
    for label, value in skills_data:
        items.append(Paragraph(f"<b>{label}</b> {value}", sSKILL))

    return items


# ---------------------------------------------------------------------------
# 11. Languages section
# ---------------------------------------------------------------------------
def build_languages():
    items = []
    items += section_header("Languages")
    items.append(Paragraph("Fluent in English and Turkish", sLANG))
    return items


# ---------------------------------------------------------------------------
# 12. Certificates section
# ---------------------------------------------------------------------------
def build_certificates():
    items = []
    items += section_header("Certificates")
    certs = [
        "Dassault Syst\u00e8mes \u2013 DELMIA Operations Management / Quality",
        "Dassault Syst\u00e8mes \u2013 DELMIA Operations Management / Maintenance",
        "DELMIA - Operations Management / Apriso Foundation",
    ]
    for c in certs:
        items.append(Paragraph(f"\u2022&nbsp;&nbsp;{c}", sCERT))
    return items


# ---------------------------------------------------------------------------
# 13. Assemble and build
# ---------------------------------------------------------------------------
def build_cv():
    doc = BaseDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
    )

    frame = Frame(
        MARGIN_L, MARGIN_B,
        PAGE_W - MARGIN_L - MARGIN_R,
        PAGE_H - MARGIN_T - MARGIN_B,
        id="main", leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame])])

    story = []

    # Header
    story.append(build_header())
    story.append(Spacer(1, 8))

    # Sections
    story += build_experience()
    story += build_education()
    story += build_skills()
    story += build_languages()
    story += build_certificates()

    doc.build(story)
    print(f"CV saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_cv()
