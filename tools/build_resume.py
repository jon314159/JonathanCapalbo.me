"""Build both portfolio resumes from the same verified background."""

import argparse
from html import unescape
import json
from pathlib import Path
from shutil import copyfile

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfdoc import PDFString
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads(Path(__file__).with_name("resume_content.json").read_text(encoding="utf-8"))
pdfmetrics.registerFont(TTFont("ResumeVera", str(ROOT / "assets/fonts/Vera.ttf")))
pdfmetrics.registerFont(TTFont("ResumeVera-Bold", str(ROOT / "assets/fonts/VeraBd.ttf")))
pdfmetrics.registerFontFamily("ResumeVera", normal="ResumeVera", bold="ResumeVera-Bold")
INK = "#17233A"
ACCENT = "#2B5D7E"
BODY = ParagraphStyle("Body", fontName="ResumeVera", fontSize=10, leading=11.5, spaceAfter=1.5)
NAME = ParagraphStyle("Name", parent=BODY, fontName="ResumeVera-Bold", fontSize=20, leading=23, alignment=TA_CENTER, textColor=colors.HexColor(INK))
HEADLINE = ParagraphStyle("Headline", parent=BODY, fontName="ResumeVera-Bold", fontSize=10.5, leading=13, alignment=TA_CENTER, textColor=colors.HexColor(ACCENT))
CONTACT = ParagraphStyle("Contact", parent=BODY, fontSize=10, leading=12, alignment=TA_CENTER)
SECTION = ParagraphStyle("Section", parent=BODY, fontName="ResumeVera-Bold", textColor=colors.HexColor(INK), spaceBefore=6, spaceAfter=2)
TITLE = ParagraphStyle("Title", parent=BODY, fontName="ResumeVera-Bold", textColor=colors.HexColor(INK), spaceAfter=1)
META = ParagraphStyle("Meta", parent=BODY, fontSize=9.5, leading=11, textColor=colors.HexColor("#4D5968"), spaceAfter=2)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=9, firstLineIndent=-9, spaceAfter=2)


def link(label, url):
    return f'<link href="{url}" color="{ACCENT}"><u>{label}</u></link>'


def section(title):
    return [Paragraph(title, SECTION), HRFlowable(width="100%", thickness=.5, color=colors.HexColor("#9AA8B5"), spaceAfter=3)]


def resume_canvas(*args, **kwargs):
    kwargs["initialFontName"] = "ResumeVera"
    return Canvas(*args, **kwargs)


def build(variant):
    selected = DATA["variants"][variant]
    experience_first = selected.get("layout") == "experience-first"
    output = ROOT / selected["output"]
    output.parent.mkdir(parents=True, exist_ok=True)
    contact = DATA["contact"]
    story = [Paragraph(DATA["name"], NAME), Paragraph(selected["headline"], HEADLINE)]
    story.append(Paragraph(f'{contact["location"]} | {contact["preference"]} | ' + link(contact["email"], "mailto:" + contact["email"]), CONTACT))
    portfolio_label = "jonathancapalbo.me" if experience_first else "Portfolio"
    linkedin_label = "linkedin.com/in/jonathan-capalbo-2a00b9140" if experience_first else "LinkedIn"
    portfolio_url = contact["portfolio"] + "#" + selected["portfolio_fragment"]
    story.append(Paragraph(link(portfolio_label, portfolio_url) + " | " + link(linkedin_label, contact["linkedin"]), CONTACT))
    story.extend(section("SUMMARY"))
    story.append(Paragraph(selected["summary"], BODY))
    if not experience_first:
        story.extend(section("SKILLS"))
        for item in selected["skills"]:
            story.append(Paragraph(item, BODY))
    story.extend(section("PROFESSIONAL EXPERIENCE" if experience_first else "EXPERIENCE"))
    for role in selected.get("experience", DATA["experience"]):
        block = [Paragraph(f'{role["title"]} | {role["company"]}', TITLE), Paragraph(f'{role["dates"]} | {role["location"]}', META)]
        bullets = role["bullets"]
        if isinstance(bullets, dict):
            bullets = bullets[variant]
        bullet_order = selected.get("experience_bullet_order", {}).get(role["company"], range(len(bullets)))
        for index in bullet_order:
            bullet = bullets[index]
            text = bullet[variant] if isinstance(bullet, dict) else bullet
            block.append(Paragraph("- " + text, BULLET))
        block.append(Spacer(1, 3))
        story.append(KeepTogether(block))
    story.extend(section("SELECTED PROJECTS"))
    projects = selected.get("project_details", [DATA["projects"][key] for key in selected["project_order"]])
    for item in projects:
        text = item["description"]
        if isinstance(text, dict):
            text = text[variant]
        description = Paragraph("- " + text, BULLET) if experience_first else Paragraph(text, BODY)
        story.append(KeepTogether([Paragraph(link(item["name"], item["url"]) if item.get("url") else item["name"], TITLE), Paragraph(item["scope"], META), description, Spacer(1, 2)]))
    if experience_first:
        story.extend(section("SKILLS"))
        for item in selected["skills"]:
            story.append(Paragraph(item, BODY))
    story.extend(section("EDUCATION"))
    for line in DATA["education"]:
        story.append(Paragraph(line, BODY))
    if selected.get("coursework"):
        story.append(Paragraph("<b>Relevant coursework:</b> " + selected["coursework"], BODY))
    story.append(Paragraph(DATA["training"], BODY))

    def page_metadata(canvas, _document):
        canvas._doc.Catalog.Lang = PDFString("en-US")

    vertical_margin = 30 if experience_first else 25
    document = SimpleDocTemplate(str(output), pagesize=letter, leftMargin=36, rightMargin=36, topMargin=vertical_margin, bottomMargin=vertical_margin, title=f'Jonathan Capalbo - {unescape(selected["headline"])}', author=DATA["name"], creator="ReportLab")
    document.build(story, onFirstPage=page_metadata, onLaterPages=page_metadata, canvasmaker=resume_canvas)
    if selected.get("alias"):
        copyfile(output, ROOT / selected["alias"])
    print(f"Built {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=["all", *DATA["variants"]], default="all")
    args = parser.parse_args()
    for key in DATA["variants"] if args.variant == "all" else [args.variant]:
        build(key)
