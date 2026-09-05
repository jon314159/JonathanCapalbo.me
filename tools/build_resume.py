from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfdoc import PDFString, PDFtrue, ViewerPreferencesPDFDictionary
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "resume.pdf"

PAGE_WIDTH, _PAGE_HEIGHT = letter
LEFT_MARGIN = 0.43 * inch
RIGHT_MARGIN = 0.43 * inch
TOP_MARGIN = 0.34 * inch
BOTTOM_MARGIN = 0.32 * inch
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

INK = colors.HexColor("#17233A")
ACCENT = colors.HexColor("#2B5D7E")
MUTED = colors.HexColor("#4D5968")
RULE = colors.HexColor("#9AA8B5")

styles = getSampleStyleSheet()
name_style = ParagraphStyle(
    "Name",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=19.5,
    leading=22,
    textColor=INK,
    alignment=TA_CENTER,
    spaceAfter=1.5,
)
headline_style = ParagraphStyle(
    "Headline",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.7,
    leading=10.5,
    textColor=ACCENT,
    alignment=TA_CENTER,
    tracking=0.25,
    spaceAfter=1.5,
)
contact_style = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.6,
    leading=10.2,
    textColor=MUTED,
    alignment=TA_CENTER,
    spaceAfter=4,
)
section_style = ParagraphStyle(
    "Section",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9.5,
    leading=11,
    textColor=INK,
    spaceBefore=3.5,
    spaceAfter=1.2,
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.8,
    leading=10.7,
    textColor=colors.black,
    alignment=TA_LEFT,
    spaceAfter=1.5,
)
small_style = ParagraphStyle(
    "Small",
    parent=body_style,
    fontSize=8.35,
    leading=10,
    spaceAfter=0.7,
)
role_left_style = ParagraphStyle(
    "RoleLeft",
    parent=body_style,
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=10.4,
    textColor=INK,
    spaceAfter=0,
)
role_right_style = ParagraphStyle(
    "RoleRight",
    parent=body_style,
    fontName="Helvetica",
    fontSize=8.55,
    leading=10.4,
    textColor=MUTED,
    alignment=TA_RIGHT,
    spaceAfter=0,
)
meta_left_style = ParagraphStyle(
    "MetaLeft",
    parent=body_style,
    fontName="Helvetica-Oblique",
    fontSize=8.55,
    leading=10.1,
    textColor=MUTED,
    spaceAfter=0,
)
meta_right_style = ParagraphStyle(
    "MetaRight",
    parent=meta_left_style,
    alignment=TA_RIGHT,
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    fontSize=8.65,
    leading=10.25,
    leftIndent=10,
    firstLineIndent=-10,
    spaceAfter=0.45,
)
project_title_style = ParagraphStyle(
    "ProjectTitle",
    parent=role_left_style,
    spaceAfter=0,
)
project_meta_style = ParagraphStyle(
    "ProjectMeta",
    parent=meta_left_style,
    spaceAfter=0.3,
)


def section(title: str):
    return KeepTogether(
        [
            Paragraph(title, section_style),
            HRFlowable(
                width="100%",
                thickness=0.7,
                color=RULE,
                spaceBefore=0,
                spaceAfter=2.3,
            ),
        ]
    )


def role_header(title: str, date: str, organization: str, location: str):
    table = Table(
        [
            [Paragraph(title, role_left_style), Paragraph(date, role_right_style)],
            [Paragraph(organization, meta_left_style), Paragraph(location, meta_right_style)],
        ],
        colWidths=[CONTENT_WIDTH * 0.70, CONTENT_WIDTH * 0.30],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def bullet(text: str):
    return Paragraph(f"- {text}", bullet_style)


def project(title: str, meta: str, bullets: list[str]):
    content = [
        Paragraph(title, project_title_style),
        Paragraph(meta, project_meta_style),
    ]
    content.extend(bullet(item) for item in bullets)
    content.append(Spacer(1, 0.7))
    return KeepTogether(content)


def education_header(institution: str, location: str):
    table = Table(
        [[Paragraph(institution, role_left_style), Paragraph(location, role_right_style)]],
        colWidths=[CONTENT_WIDTH * 0.72, CONTENT_WIDTH * 0.28],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def configure_page(canvas, _document):
    canvas.setTitle("Jonathan Capalbo - Analysis, Reporting, and Business Systems Resume")
    canvas.setAuthor("Jonathan Capalbo")
    canvas.setSubject(
        "Business analysis, reporting, process improvement, and business systems resume"
    )
    canvas.setKeywords(
        "business analysis, requirements, user stories, UAT planning, operations analysis, reporting, Excel, process improvement, Power Automate, ServiceNow"
    )
    canvas._doc.Catalog.Lang = PDFString("en-US")
    preferences = ViewerPreferencesPDFDictionary()
    preferences["DisplayDocTitle"] = PDFtrue
    canvas._doc.Catalog.ViewerPreferences = preferences


def build():
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title="Jonathan Capalbo - Analysis, Reporting, and Business Systems Resume",
        author="Jonathan Capalbo",
        subject="Business analysis, reporting, process improvement, and business systems resume",
        creator="ReportLab resume generator",
        keywords="business analysis, requirements, user stories, UAT planning, operations analysis, reporting, Excel, process improvement, Power Automate, ServiceNow",
    )

    contact = (
        "Point Pleasant, NJ | Open to remote | "
        '<link href="mailto:jonathancapalbo1@gmail.com" color="#4D5968">'
        "jonathancapalbo1@gmail.com</link> | "
        '<link href="https://jonathancapalbo.me" color="#4D5968">jonathancapalbo.me</link> | '
        '<link href="https://linkedin.com/in/jonathan-capalbo-2a00b9140" color="#4D5968">'
        "linkedin.com/in/jonathan-capalbo-2a00b9140</link> | "
        '<link href="https://github.com/jon314159" color="#4D5968">github.com/jon314159</link>'
    )

    story = [
        Paragraph("Jonathan Capalbo", name_style),
        Paragraph("BUSINESS ANALYSIS | REPORTING | BUSINESS SYSTEMS", headline_style),
        Paragraph(contact, contact_style),
        section("PROFESSIONAL SUMMARY"),
        Paragraph(
            "Customer operations professional with 5+ years of experience investigating policy and system issues, maintaining customer records, and coordinating follow-up. Builds Excel reporting workflows and develops requirements, process maps, and UAT plans through self-directed projects. Pursuing an M.S. in Business & Information Systems at NJIT.",
            body_style,
        ),
        section("CORE STRENGTHS"),
        Paragraph(
            "<b>Reporting &amp; Analysis:</b> Excel reporting | Trend and exception review | Requirements analysis | Process mapping",
            small_style,
        ),
        Paragraph(
            "<b>Operations &amp; Systems:</b> Issue investigation | Documentation | User stories and acceptance criteria | UAT planning | Workload prioritization | Cross-team coordination",
            small_style,
        ),
        Paragraph(
            "<b>Tools:</b> Excel (tables, cross-sheet formulas, SUMIF/COUNTIF, data validation, conditional formatting) | Power Automate | Microsoft Access | CSG | ServiceNow Knowledge Management and Service Portal (academic project) | SQL and Tableau (coursework)",
            small_style,
        ),
        section("PROFESSIONAL EXPERIENCE"),
        KeepTogether(
            [
                role_header(
                    "Customer Account Executive",
                    "April 2022 - Present",
                    "Comcast / Xfinity",
                    "Remote",
                ),
                bullet(
                    "Manage about 25 customer interactions daily, more than 5,000 annually, reviewing customer records and available options to identify appropriate actions."
                ),
                bullet(
                    "Investigate customer-record, policy, procedure, and system questions using current resources and internal support partners."
                ),
                bullet(
                    "Maintain accurate records in CSG and other internal systems, documenting decisions, follow-up, and cross-team handoffs."
                ),
                bullet(
                    "Use Microsoft Power Automate to organize my recurring tracking and follow-up."
                ),
                Spacer(1, 1.5),
            ]
        ),
        KeepTogether(
            [
                role_header(
                    "Customer Service Representative",
                    "February 2021 - January 2022",
                    "Harte Hanks",
                    "Remote",
                ),
                bullet(
                    "Investigated customer inquiries in a remote environment, recorded relevant details, and explained next actions."
                ),
                bullet(
                    "Prioritized, categorized, and routed email requests, maintaining organized records for team handoffs."
                ),
            ]
        ),
        section("SELECTED PROJECTS"),
        project(
            '<link href="https://jonathancapalbo.me/sales-activity-tracker.html" color="#17233A">Excel Activity Reporting System</link>',
            "Portfolio Case Study | Fictional Data",
            [
                "Built a 35-sheet Excel reporting system with 31 standardized daily views, centralized settings, and monthly consolidation.",
                "Added validation controls, configurable goals, and dashboard views to compare results and identify exceptions.",
            ],
        ),
        project(
            '<link href="https://jonathancapalbo.me/arcade-ticketing-modernization.html" color="#17233A">Arcade Operations Ticketing Modernization</link>',
            "Self-Directed BA Case Study | Simulated Scenario",
            [
                "Designed a five-category ticketing pilot with current- and future-state workflows, 110 draft requirements, 34 user stories, requirements traceability, and 31 planned UAT cases."
            ],
        ),
        project(
            '<link href="https://jonathancapalbo.me/servicenow-njit-registrar.html" color="#17233A">Registrar ServiceNow Portal</link>',
            "Academic Project | ServiceNow Lab",
            [
                "Configured a searchable portal, organized 42 lab articles into 12 student-facing categories, and revised registration guidance for steps, common errors, and support contacts."
            ],
        ),
        section("EDUCATION"),
        education_header("New Jersey Institute of Technology", "Newark, NJ"),
        Paragraph("<b>M.S. Business &amp; Information Systems</b> | Expected Summer 2028", body_style),
        Paragraph(
            "<b>Relevant Coursework:</b> System Analysis and Design, Business Data Analytics, Operations Management and Analytics, Project Management, Knowledge Management",
            small_style,
        ),
        Spacer(1, 0.8),
        Paragraph(
            "<b>B.S. Business Administration</b> | 2024 | GPA: 3.97 | Dean's List, all semesters",
            body_style,
        ),
        section("PROFESSIONAL TRAINING"),
        bullet("ServiceNow Administration Fundamentals"),
        bullet("ServiceNow Knowledge Management Fundamentals"),
    ]

    document.build(story, onFirstPage=configure_page, onLaterPages=configure_page)
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    build()
