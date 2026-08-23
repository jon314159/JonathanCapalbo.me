from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfdoc import PDFString, PDFtrue, ViewerPreferencesPDFDictionary
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "resume.pdf"

INK = colors.HexColor("#10262A")
TEAL = colors.HexColor("#14746F")
MUTED = colors.HexColor("#42585B")
RULE = colors.HexColor("#2B827D")

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "ResumeTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=24,
    leading=25,
    alignment=TA_CENTER,
    textColor=INK,
    spaceAfter=1,
)
subtitle_style = ParagraphStyle(
    "ResumeSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=11.5,
    alignment=TA_CENTER,
    textColor=TEAL,
    spaceAfter=2,
)
contact_style = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.9,
    leading=10.3,
    alignment=TA_CENTER,
    textColor=MUTED,
    spaceAfter=4,
)
section_style = ParagraphStyle(
    "Section",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10.8,
    leading=12,
    textColor=TEAL,
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.05,
    leading=11,
    textColor=INK,
    spaceAfter=1.8,
)
role_style = ParagraphStyle(
    "Role",
    parent=body_style,
    fontName="Helvetica-Bold",
    fontSize=9.6,
    leading=11,
    spaceBefore=1.2,
    spaceAfter=1.1,
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=9,
    firstLineIndent=-8,
    spaceAfter=1,
)
small_style = ParagraphStyle(
    "Small",
    parent=body_style,
    fontSize=8.35,
    leading=9.8,
    spaceAfter=1,
)


def paragraph(text, style=body_style):
    return Paragraph(escape(text), style)


def section(title):
    table = Table([[Paragraph(escape(title), section_style)]], colWidths=[7.28 * inch])
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LINEBELOW", (0, 0), (-1, -1), 0.65, RULE),
            ]
        )
    )
    return table


def role(text):
    return Paragraph(escape(text), role_style)


def bullet(text):
    return Paragraph("- " + escape(text), bullet_style)


def configure_page(canvas, _doc):
    """Declare the document language without falsely claiming tagged-PDF support."""
    canvas._doc.Catalog.Lang = PDFString("en-US")
    preferences = ViewerPreferencesPDFDictionary()
    preferences["DisplayDocTitle"] = PDFtrue
    canvas._doc.Catalog.ViewerPreferences = preferences


def build():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.61 * inch,
        rightMargin=0.61 * inch,
        topMargin=0.33 * inch,
        bottomMargin=0.28 * inch,
        title="Jonathan Capalbo Resume",
        author="Jonathan Capalbo",
        subject="Operations, reporting, and business systems resume",
        creator="ReportLab resume generator",
        keywords="business operations, reporting, business systems, Excel, process improvement, documentation, data accuracy",
    )

    contact = (
        '<link href="mailto:jonathancapalbo1@gmail.com" color="#42585B">'
        "jonathancapalbo1@gmail.com</link> | "
        '<link href="https://www.linkedin.com/in/jonathan-capalbo-2a00b9140" color="#42585B">'
        "linkedin.com/in/jonathan-capalbo-2a00b9140</link> | "
        '<link href="https://jonathancapalbo.me" color="#42585B">jonathancapalbo.me</link>'
    )

    story = [
        Paragraph("Jonathan Capalbo", title_style),
        Paragraph("OPERATIONS | REPORTING | BUSINESS SYSTEMS", subtitle_style),
        Paragraph(contact, contact_style),
        section("PROFESSIONAL SUMMARY"),
        paragraph(
            "Operations and business systems professional with 5+ years of experience supporting high-volume workflows, including 4+ years at Comcast/Xfinity. Builds Excel reporting and tracking tools, reviews account data, investigates policy and system questions, documents decisions, and coordinates accurate follow-up. Uses Microsoft Power Automate and basic scripting to streamline recurring work, with ServiceNow knowledge management training and academic project experience. M.S. Business & Information Systems in progress."
        ),
        section("CORE STRENGTHS"),
        paragraph(
            "Data & Analysis: Excel reporting and dashboards | Data validation and accuracy | Trend and exception analysis | Tableau (coursework) | SQL (coursework)",
            small_style,
        ),
        paragraph(
            "Process & Systems: Process improvement | Process documentation | Issue investigation | Policy and procedure interpretation | Microsoft Power Automate | Basic scripting | ServiceNow Knowledge Management",
            small_style,
        ),
        paragraph(
            "Communication & Coordination: Cross-team coordination | Workload prioritization | Customer operations | Clear written communication",
            small_style,
        ),
        section("PROFESSIONAL EXPERIENCE"),
        KeepTogether(
            [
                role("Comcast / Xfinity | Sales Representative | Remote | April 2022 - Present"),
                bullet(
                    "Manage about 25 customer interactions daily, more than 5,000 annually, by clarifying needs, reviewing account data and available options, and determining practical next steps."
                ),
                bullet(
                    "Investigate account, policy, procedure, and system questions using current resources and support partners; organize findings and explain clear, accurate next steps."
                ),
                bullet(
                    "Maintain accurate, complete records in CSG and other internal systems by documenting interactions, decisions, follow-up, and cross-team handoffs."
                ),
                bullet(
                    "Build Excel tracking tools and use Microsoft Power Automate and basic scripting to streamline recurring personal workflows and follow-up."
                ),
            ]
        ),
        KeepTogether(
            [
                role("Harte Hanks | Customer Service Representative | Remote | February 2021 - January 2022"),
                bullet(
                    "Researched customer inquiries in a fast-paced remote environment, documented relevant details, and communicated clear next steps."
                ),
                bullet(
                    "Prioritized and routed high-volume email requests, maintaining organized records for accurate, consistent team handoffs."
                ),
            ]
        ),
        section("SELECTED PROJECTS"),
        KeepTogether(
            [
                role("Excel Activity Reporting System | Independent Portfolio Project | Synthetic Data"),
                bullet(
                    "Built a controlled Excel workflow that captures daily activity, consolidates results into a monthly dashboard, and compares overall goal attainment with day-to-day consistency."
                ),
                bullet(
                    "Added configurable goals, validation controls, and exception-focused views so users can identify gaps, review results efficiently, and focus follow-up on the days that need attention."
                ),
            ]
        ),
        KeepTogether(
            [
                role("Registrar Knowledge Portal | ServiceNow Lab | Academic Project"),
                bullet(
                    "Configured a searchable ServiceNow knowledge portal, organized 42 lab articles into 12 student-facing categories, and revised registration guidance for faster scanning of steps, common errors, and support contacts."
                ),
                role("Business and Cost Analysis | CAPSIM | Academic Project"),
                bullet(
                    "Reviewed seven years of sales, market share, costs, profit, cash flow, and product strategy, then summarized trends and recommended next steps."
                ),
            ]
        ),
        section("EDUCATION AND PROFESSIONAL DEVELOPMENT"),
        role("New Jersey Institute of Technology | Newark, NJ"),
        paragraph("M.S. Business & Information Systems | In Progress"),
        paragraph("B.S. Business Administration | 2024 | GPA: 3.97 | Dean's List, all semesters"),
        paragraph(
            "Relevant coursework: Business Data Analytics; Operations Management & Analytics; Financial Statement Analysis; Business Research Methods; System Analysis & Design; Project Management; Knowledge Management; Decision Support Tools.",
            small_style,
        ),
        paragraph(
            "Additional training: ServiceNow Administration Fundamentals and Knowledge Management Fundamentals.",
            small_style,
        ),
    ]

    doc.build(story, onFirstPage=configure_page, onLaterPages=configure_page)
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    build()
