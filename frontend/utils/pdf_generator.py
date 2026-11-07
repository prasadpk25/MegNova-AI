
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)


def generate_summary_pdf(
    report_name: str,
    patient_name: str,
    doctor_name: str,
    report_type: str,
    report_date: str,
    summary: str,
) -> bytes:

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"Medical Summary - {report_name}",
        author="MegNova AI Hospital Digital Twin",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "MedicalTitle",
        parent=styles["Title"],
        fontSize=19,
        leading=24,
        textColor=colors.HexColor("#17365D"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#176B87"),
        spaceBefore=12,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "SummaryBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=7,
    )

    story = []

    story.append(Paragraph("MEGNOVA AI", title_style))
    story.append(
        Paragraph("Medical Report Summary", styles["Heading2"])
    )

    story.append(HRFlowable(width="100%", color=colors.HexColor("#176B87")))
    story.append(Spacer(1, 12))

    details = [
        ("Report", report_name),
        ("Patient", patient_name),
        ("Doctor", doctor_name),
        ("Report Type", report_type),
        ("Report Date", report_date),
    ]

    for label, value in details:
        story.append(
            Paragraph(
                f"<b>{escape(str(label))}:</b> "
                f"{escape(str(value or 'N/A'))}",
                body_style,
            )
        )

    story.append(Spacer(1, 10))
    story.append(Paragraph("AI-Generated Summary", heading_style))

    for paragraph in summary.splitlines():
        paragraph = paragraph.strip()

        if not paragraph:
            story.append(Spacer(1, 5))
            continue

        story.append(
            Paragraph(escape(paragraph), body_style)
        )

    story.append(Spacer(1, 18))
    story.append(HRFlowable(width="100%", color=colors.grey))
    story.append(Spacer(1, 7))

    story.append(
        Paragraph(
            "<b>Important Notice:</b> This AI-generated summary "
            "is intended to support clinical review. It is not a "
            "medical diagnosis or a substitute for professional "
            "medical judgment. Verify all findings against the "
            "original report.",
            styles["Italic"],
        )
    )

    document.build(story)

    return buffer.getvalue()
