from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Table,
    TableStyle,
)


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
    fontSize=22,
    leading=23,
    alignment=TA_CENTER,
    textColor=INK,
    spaceAfter=1,
)
subtitle_style = ParagraphStyle(
    "ResumeSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=11,
    alignment=TA_CENTER,
    textColor=TEAL,
    spaceAfter=2,
)
contact_style = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=9.5,
    alignment=TA_CENTER,
    textColor=MUTED,
    spaceAfter=4,
)
section_style = ParagraphStyle(
    "Section",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10.4,
    leading=11.5,
    textColor=TEAL,
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.55,
    leading=10.15,
    textColor=INK,
    spaceAfter=1.5,
)
role_style = ParagraphStyle(
    "Role",
    parent=body_style,
    fontName="Helvetica-Bold",
    fontSize=9.05,
    leading=10.2,
    spaceBefore=1,
    spaceAfter=1,
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=9,
    firstLineIndent=-8,
    spaceAfter=0.7,
)
small_style = ParagraphStyle(
    "Small",
    parent=body_style,
    fontSize=7.9,
    leading=9.2,
    spaceAfter=0.8,
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
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                ("LINEBELOW", (0, 0), (-1, -1), 0.65, RULE),
            ]
        )
    )
    return table


def role(text):
    return Paragraph(escape(text), role_style)


def bullet(text):
    return Paragraph("- " + escape(text), bullet_style)


def build():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.61 * inch,
        rightMargin=0.61 * inch,
        topMargin=0.35 * inch,
        bottomMargin=0.3 * inch,
        title="Jonathan Capalbo - Procurement Analytics Resume",
        author="Jonathan Capalbo",
        subject="Analyst, Procurement",
    )

    story = [
        Paragraph("Jonathan Capalbo", title_style),
        Paragraph("PROCUREMENT ANALYTICS | REPORTING | PROCESS IMPROVEMENT", subtitle_style),
        Paragraph(
            "jonathancapalbo1@gmail.com | linkedin.com/in/jonathan-capalbo-2a00b9140 | jonathancapalbo.me",
            contact_style,
        ),
        section("PROFESSIONAL SUMMARY"),
        paragraph(
            "Operations and data analysis professional with 5+ years of customer operations experience, including 4+ years at Comcast/Xfinity. Uses Excel reporting, data analysis, and structured documentation to improve high-volume work involving approximately 25 customer interactions daily and 5,000+ annually. Ready to apply Comcast systems and policy knowledge to vendor data quality, purchase order reporting, spend analysis, procurement data integrity, audit support, and cross-functional decisions."
        ),
        section("CORE SKILLS"),
        paragraph(
            "Excel analytics and reporting | Dashboard-style report design (Power BI-aligned) | Vendor data quality | Purchase order reporting and exception tracking | Spend analysis and cost trends | Data analysis and data integrity | Process improvement | Audit-support documentation | Policy and process documentation | Cross-functional communication | Tableau and SQL exposure | ServiceNow knowledge management | Comcast/Xfinity operations",
            small_style,
        ),
        section("PROFESSIONAL EXPERIENCE"),
        KeepTogether(
            [
                role("Comcast / Xfinity | Sales Representative | Remote | April 2022 - Present"),
                bullet(
                    "Handle approximately 25 customer interactions per day (5,000+ annually), navigating account data, offers, policies, documentation requirements, and internal support resources."
                ),
                bullet(
                    "Review account and customer data in internal systems; document activity, decisions, and follow-up with attention to accuracy and data integrity."
                ),
                bullet(
                    "Interpret changing policies and internal guidance, investigate questions with knowledge resources and support partners, and translate findings into clear next steps."
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
                    "Reviewed, categorized, and routed email requests while maintaining organized records and consistent handoffs."
                ),
            ]
        ),
        section("SELECTED PROJECTS"),
        KeepTogether(
            [
                role("Sales Performance Tracker | Excel"),
                bullet(
                    "Built a workbook that standardized five recurring data categories - daily activity, product results, account notes, goals, and summary metrics - into one review-ready reporting source."
                ),
                bullet(
                    "Automated recurring cleanup and dashboard summaries, saving an estimated 2-3 hours weekly (100+ hours annually) while reducing manual re-entry, missing-field risk, and inconsistent reporting."
                ),
            ]
        ),
        KeepTogether(
            [
                role("Knowledge Management and Documentation | ServiceNow, Microsoft 365"),
                bullet(
                    "Created support content and proposed a structured author, review, approval, and retrieval workflow for internal information."
                ),
                role("Sales and Strategy Analysis | CAPSIM"),
                bullet(
                    "Analyzed seven years of sales, market share, costs, profit, cash flow, and product strategy to identify cost trends and recommend next steps."
                ),
                role("Movie Rental Database | Oracle SQL"),
                bullet(
                    "Designed relational tables, keys, constraints, sample data, views, and an index to support consistent, queryable data."
                ),
            ]
        ),
        section("EDUCATION AND PROFESSIONAL DEVELOPMENT"),
        role("New Jersey Institute of Technology | Newark, NJ"),
        paragraph("M.S. Business & Information Systems | In Progress"),
        paragraph("B.S. Business Administration | 2024 | GPA: 3.97 | Dean's List, all semesters"),
        paragraph(
            "Relevant coursework: Business Data Analytics; Business Operations Management & Analytics; Decision Support Tools & Technology; Enterprise Database Management; System Analysis and Design; Project Management; Knowledge Management; Financial Statement Analysis.",
            small_style,
        ),
        paragraph(
            "Additional training: ServiceNow Administration Fundamentals and Knowledge Management Fundamentals.",
            small_style,
        ),
    ]

    doc.build(story)
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    build()
