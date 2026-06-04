from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime


def create_pdf(stock, news, analysis, filename):

    pdf = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    # Custom Styles (IMPORTANT for professional look)
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=18,
        spaceAfter=10,
        alignment=1  # center
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=styles["BodyText"],
        fontSize=9.5,
        leftIndent=14,
        bulletIndent=6,
        spaceAfter=2
    )

    content = []

    # ================= TITLE =================
    content.append(Paragraph("STOCK RESEARCH REPORT", title_style))
    content.append(Paragraph(datetime.now().strftime("%d %b %Y"), styles["Normal"]))
    content.append(Spacer(1, 12))
    content.append(HRFlowable(width="100%"))
    content.append(Spacer(1, 12))

    # ================= STOCK SNAPSHOT =================
    content.append(Paragraph("STOCK SNAPSHOT", heading_style))

    table_data = [[k, str(v)] for k, v in stock.items()]

    table = Table(table_data, colWidths=[2.5 * inch, 3.5 * inch])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    content.append(table)
    content.append(Spacer(1, 14))

    # ================= NEWS =================
    content.append(Paragraph("NEWS HIGHLIGHTS", heading_style))

    for i, item in enumerate(news, 1):
        content.append(Paragraph(f"{i}. {item['title']}", body_style))

    content.append(Spacer(1, 10))

    # ================= ANALYSIS =================
    content.append(Paragraph("INVESTMENT ANALYSIS", heading_style))
    content.append(HRFlowable(width="100%"))
    content.append(Spacer(1, 8))

    for line in analysis.split("\n"):
        line = line.strip()

        if not line:
            continue

        # Headings detection
        if line.endswith(":") or line.isupper():
            content.append(Paragraph(f"<b>{line}</b>", body_style))
        elif line.startswith("-") or line.startswith("*"):
            content.append(Paragraph(line, bullet_style, bulletText="•"))
        else:
            content.append(Paragraph(line, body_style))

    pdf.build(content)