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
    canvas.setTitle("Jonathan Capalbo - Business Operations Analyst Resume")
    canvas.setAuthor("Jonathan Capalbo")
    canvas.setSubject(
        "Business operations, reporting, process improvement, and business systems resume"
    )
    canvas.setKeywords(
        "business operations, operations analysis, reporting, Excel, process improvement, Power Automate, ServiceNow"
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
        title="Jonathan Capalbo - Business Operations Analyst Resume",
        author="Jonathan Capalbo",
        subject="Business operations, reporting, process improvement, and business systems resume",
        creator="ReportLab resume generator",
        keywords="business operations, operations analysis, reporting, Excel, process improvement, Power Automate, ServiceNow",
    )

    contact = (
        '<link href="mailto:jonathancapalbo1@gmail.com" color="#4D5968">'
        "jonathancapalbo1@gmail.com</link> | "
        '<link href="https://www.linkedin.com/in/jonathan-capalbo-2a00b9140" color="#4D5968">'
        "LinkedIn</link> | "
        '<link href="https://github.com/jon314159" color="#4D5968">GitHub</link>'
    )

    story = [
        Paragraph("Jonathan Capalbo", name_style),
        Paragraph("BUSINESS OPERATIONS | REPORTING | BUSINESS SYSTEMS", headline_style),
        Paragraph(contact, contact_style),
        section("PROFESSIONAL SUMMARY"),
        Paragraph(
            "Business operations professional transitioning into analysis, with 5+ years supporting high-volume workflows, including 4+ years at Comcast/Xfinity. Builds Excel reports and dashboards, reviews account and operational data, investigates process and system issues, and documents findings for accurate decisions and follow-up. Uses Microsoft Power Automate and basic scripting to automate recurring workflows, saving several hours of manual work each week. M.S. Business & Information Systems in progress, with ServiceNow training and hands-on academic project experience.",
            body_style,
        ),
        section("CORE STRENGTHS"),
        Paragraph(
            "<b>Data &amp; Analysis:</b> Excel reporting and dashboards | Data validation and accuracy | Trend and exception analysis | Tableau (coursework) | SQL (coursework)",
            small_style,
        ),
        Paragraph(
            "<b>Process &amp; Systems:</b> Process improvement | Process documentation | Issue investigation | Policy and procedure interpretation | Microsoft Power Automate | Basic scripting | ServiceNow Knowledge Management",
            small_style,
        ),
        Paragraph(
            "<b>Communication &amp; Coordination:</b> Cross-team coordination | Workload prioritization | Customer operations | Clear written communication",
            small_style,
        ),
        section("PROFESSIONAL EXPERIENCE"),
        KeepTogether(
            [
                role_header(
                    "Sales Representative",
                    "April 2022 - Present",
                    "Comcast / Xfinity",
                    "Remote",
                ),
                bullet(
                    "Handle 25+ customer interactions daily, more than 5,000 annually, reviewing account data and available options to determine accurate next steps."
                ),
                bullet(
                    "Investigate account, policy, procedure, and system questions using current resources and support partners; organize findings and communicate clear next steps."
                ),
                bullet(
                    "Maintain accurate records in CSG and other internal systems, documenting decisions, follow-up, and cross-team handoffs."
                ),
                bullet(
                    "Build Excel tracking tools and automate recurring workflows using Microsoft Power Automate and basic scripting, saving several hours of manual work each week."
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
                    "Researched customer inquiries in a high-volume remote environment, documented relevant details, and communicated clear next steps."
                ),
                bullet(
                    "Prioritized and routed high-volume email requests, maintaining organized records for accurate, consistent team handoffs."
                ),
            ]
        ),
        section("SELECTED PROJECTS"),
        project(
            "Excel Activity Reporting System",
            "Team-Used Workflow | Portfolio Case Study",
            [
                "Built a team-used Excel workflow that captures multiple data points across recurring activities, consolidates results into a monthly dashboard, and analyzes goal attainment and day-to-day consistency.",
                "Added configurable goals, validation controls, and exception-focused views so users can identify gaps, review results efficiently, and focus follow-up where needed.",
            ],
        ),
        project(
            "Registrar Knowledge Portal",
            "ServiceNow Lab | Academic Project",
            [
                "Configured a searchable ServiceNow knowledge portal, organized 42 lab articles into 12 student-facing categories, and revised registration guidance for faster scanning of steps, common errors, and support contacts."
            ],
        ),
        project(
            "Business and Cost Analysis",
            "CAPSIM | Academic Project",
            [
                "Analyzed seven years of sales, market share, costs, profit, and product strategy; summarized trends and recommended next steps."
            ],
        ),
        section("EDUCATION"),
        education_header("New Jersey Institute of Technology", "Newark, NJ"),
        Paragraph("<b>M.S. Business &amp; Information Systems</b> | In Progress", body_style),
        Paragraph(
            "<b>Relevant Coursework:</b> Business Data Analytics, Operations Management and Analytics, Financial Statement Analysis, Business Research Methods, System Analysis and Design, Project Management, Knowledge Management, Decision Support Tools",
            small_style,
        ),
        Spacer(1, 0.8),
        education_header("New Jersey Institute of Technology", "Newark, NJ"),
        Paragraph(
            "<b>B.S. Business Administration</b> | 2024 | GPA: 3.97 | Dean's List, all semesters",
            body_style,
        ),
        section("ADDITIONAL TRAINING"),
        bullet("ServiceNow Administration Fundamentals"),
        bullet("ServiceNow Knowledge Management Fundamentals"),
    ]

    document.build(story, onFirstPage=configure_page, onLaterPages=configure_page)
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    build()
