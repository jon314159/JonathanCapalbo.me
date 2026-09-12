"""Build both portfolio resumes from the same verified background."""

import argparse
from html import unescape
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfdoc import PDFString
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads(Path(__file__).with_name("resume_content.json").read_text(encoding="utf-8"))
INK = "#17233A"
ACCENT = "#2B5D7E"
BODY = ParagraphStyle("Body", fontName="Helvetica", fontSize=10.5, leading=12.5, spaceAfter=2)
NAME = ParagraphStyle("Name", parent=BODY, fontName="Helvetica-Bold", fontSize=20, leading=23, alignment=TA_CENTER, textColor=colors.HexColor(INK))
HEADLINE = ParagraphStyle("Headline", parent=BODY, fontName="Helvetica-Bold", fontSize=10.5, leading=13, alignment=TA_CENTER, textColor=colors.HexColor(ACCENT))
CONTACT = ParagraphStyle("Contact", parent=BODY, fontSize=10, leading=12, alignment=TA_CENTER)
SECTION = ParagraphStyle("Section", parent=BODY, fontName="Helvetica-Bold", textColor=colors.HexColor(INK), spaceBefore=6, spaceAfter=2)
TITLE = ParagraphStyle("Title", parent=BODY, fontName="Helvetica-Bold", textColor=colors.HexColor(INK), spaceAfter=1)
META = ParagraphStyle("Meta", parent=BODY, fontSize=10, leading=12, textColor=colors.HexColor("#4D5968"), spaceAfter=2)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=9, firstLineIndent=-9, spaceAfter=2)


def link(label, url):
    return f'<link href="{url}" color="{ACCENT}"><u>{label}</u></link>'


def section(title):
    return [Paragraph(title, SECTION), HRFlowable(width="100%", thickness=.5, color=colors.HexColor("#9AA8B5"), spaceAfter=3)]


def build(variant):
    selected = DATA["variants"][variant]
    output = ROOT / selected["output"]
    output.parent.mkdir(parents=True, exist_ok=True)
    contact = DATA["contact"]
    story = [Paragraph(DATA["name"], NAME), Paragraph(selected["headline"], HEADLINE)]
    story.append(Paragraph(f'{contact["location"]} | {contact["preference"]} | ' + link(contact["email"], "mailto:" + contact["email"]), CONTACT))
    story.append(Paragraph(link("Portfolio", contact["portfolio"]) + " | " + link("LinkedIn", contact["linkedin"]), CONTACT))
    story.extend(section("SUMMARY"))
    story.append(Paragraph(selected["summary"], BODY))
    story.extend(section("SKILLS"))
    for item in selected["skills"]:
        story.append(Paragraph(item, BODY))
    story.extend(section("EXPERIENCE"))
    for role in DATA["experience"]:
        block = [Paragraph(f'{role["title"]} | {role["company"]}', TITLE), Paragraph(f'{role["dates"]} | {role["location"]}', META)]
        block.extend(Paragraph("- " + item, BULLET) for item in role["bullets"])
        block.append(Spacer(1, 3))
        story.append(KeepTogether(block))
    story.extend(section("SELECTED PROJECTS"))
    for key in selected["project_order"]:
        item = DATA["projects"][key]
        story.append(KeepTogether([Paragraph(link(item["name"], item["url"]), TITLE), Paragraph(item["scope"], META), Paragraph(item["description"], BODY), Spacer(1, 2)]))
    story.extend(section("EDUCATION"))
    story.append(Paragraph("<b>New Jersey Institute of Technology</b> | Newark, NJ", BODY))
    story.append(Paragraph("M.S. Business &amp; Information Systems | Expected Summer 2028", BODY))
    story.append(Paragraph("B.S. Business Administration | 2024 | GPA: 3.97 | Dean's List, all semesters", BODY))
    story.append(Paragraph("<b>Undergraduate coursework:</b> " + selected["coursework"], BODY))
    story.append(Paragraph("<b>Training:</b> ServiceNow Administration Fundamentals; ServiceNow Knowledge Management Fundamentals", BODY))

    def page_metadata(canvas, _document):
        canvas._doc.Catalog.Lang = PDFString("en-US")

    document = SimpleDocTemplate(str(output), pagesize=letter, leftMargin=36, rightMargin=36, topMargin=25, bottomMargin=25, title=f'Jonathan Capalbo - {unescape(selected["headline"])}', author=DATA["name"], creator="ReportLab")
    document.build(story, onFirstPage=page_metadata, onLaterPages=page_metadata)
    print(f"Built {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=["all", *DATA["variants"]], default="all")
    args = parser.parse_args()
    for key in DATA["variants"] if args.variant == "all" else [args.variant]:
        build(key)
