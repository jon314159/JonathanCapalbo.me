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
        subject="Entry-level analyst, procurement support, and operations resume",
        creator="ReportLab resume generator",
        keywords="analyst, operations, reporting, Excel, process improvement, procurement support",
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
        Paragraph("ENTRY-LEVEL ANALYST | OPERATIONS | PROCUREMENT SUPPORT", subtitle_style),
        Paragraph(contact, contact_style),
        section("PROFESSIONAL SUMMARY"),
        paragraph(
            "Operations and reporting professional with 5+ years of customer-facing experience, including 4+ years at Comcast/Xfinity. Reviews account data, interprets changing policies, maintains accurate documentation, and manages about 25 customer interactions daily. Builds Excel reporting tools and uses Microsoft Power Automate and basic scripting to streamline routine work. Pursuing entry-level analyst, procurement support, and operations roles centered on data accuracy, process support, and clear communication."
        ),
        section("CORE SKILLS"),
        paragraph(
            "Excel reporting and dashboards | Data cleanup and validation | Trend and cost analysis | Process improvement | Process documentation | Account review and data accuracy | Policy interpretation | Microsoft Power Automate | Basic scripting | Cross-team communication | High-volume workload management | Tableau (coursework) | SQL (coursework) | ServiceNow Knowledge Management (academic project and training)",
            small_style,
        ),
        section("PROFESSIONAL EXPERIENCE"),
        KeepTogether(
            [
                role("Comcast / Xfinity | Sales Representative | Remote | April 2022 - Present"),
                bullet(
                    "Handle about 25 customer interactions daily, more than 5,000 annually, while reviewing account data, offers, policies, documentation requirements, and current internal guidance."
                ),
                bullet(
                    "Document activity, decisions, and follow-up in internal systems with attention to accuracy and data integrity."
                ),
                bullet(
                    "Interpret policy and offer changes, investigate procedure and system questions, and translate current guidance into clear next steps for customers and teammates."
                ),
                bullet(
                    "Build Excel tracking tools and use Microsoft Power Automate and basic scripting to organize information, schedule Teams messages, and automate routine emails."
                ),
            ]
        ),
        KeepTogether(
            [
                role("Harte Hanks | Customer Service Representative | Remote | February 2021 - January 2022"),
                bullet(
                    "Investigated customer inquiries, documented relevant details, and communicated clear next steps in a remote, high-volume environment."
                ),
                bullet(
                    "Reviewed, categorized, and routed email requests while maintaining organized records, priorities, and consistent handoffs."
                ),
            ]
        ),
        section("SELECTED PROJECTS"),
        KeepTogether(
            [
                role("Excel Activity Reporting System | Fictional public demonstration"),
                bullet(
                    "Designed a controlled 35-sheet workbook with settings, 31 daily logs, monthly consolidation, a dashboard, 32 Excel tables, validation rules, and 2,231 formula cells."
                ),
                bullet(
                    "Reconciled fictional product, point, and daily-status totals and showed how monthly goal attainment can mask uneven daily consistency."
                ),
            ]
        ),
        KeepTogether(
            [
                role("Registrar Knowledge Portal | ServiceNow school lab | Academic project"),
                bullet(
                    "Configured a searchable home page and organized 42 lab articles into 12 student-facing categories at project completion; revised registration guidance for clearer scanning."
                ),
                role("Business and Cost Analysis | CAPSIM | Academic project"),
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
