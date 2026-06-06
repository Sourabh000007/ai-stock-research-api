from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
from chart_generator import create_stock_chart


def create_pdf(stock,news,analysis,history,sentiment,recommendation,filename):

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

    chart_file = "stock_chart.png"

    create_stock_chart(
        history,
        chart_file
    )

    # ================= TITLE =================
    content.append(Paragraph("STOCK RESEARCH REPORT", title_style))
    content.append(Paragraph(datetime.now().strftime("%d %b %Y"), styles["Normal"]))
    content.append(Spacer(1, 12))
    content.append(HRFlowable(width="100%"))
    content.append(Spacer(1, 12))

    # ================= STOCK SNAPSHOT =================
    content.append(Paragraph("STOCK SNAPSHOT", heading_style))

    table_data = [
        ["Metric", "Value"],
        ["Company", stock["name"]],
        ["Sector", stock["sector"]],
        ["Current Price", f"₹{stock['price']}"],
        ["Market Cap", stock["market_cap"]],
        ["P/E Ratio", str(stock["pe_ratio"])],
        ["1-Month Return", f"{stock['1_month_return']}%"],
        ["3-Month Return", f"{stock['3_month_return']}%"],
        ["6-Month Return", f"{stock['6_month_return']}%"]
    ]

    table = Table(table_data, colWidths=[2.5 * inch, 3.5 * inch])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),

        ("FONTSIZE", (0, 0), (-1, -1), 9),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

        ("PADDING", (0, 0), (-1, -1), 6)
    ]))

    content.append(table)
    content.append(Spacer(1, 14))

    content.append(
    Paragraph(
        "PRICE TREND (6 MONTHS)",
        heading_style
    )
    )

    content.append(
        Image(
            chart_file,
            width=400,
            height=200
        )
    )

    content.append(Spacer(1, 12))

    content.append(
    Paragraph(
        "NEWS SENTIMENT",
        heading_style
        )
    )

    content.append(
        Paragraph(
            f"<b>Sentiment:</b> {sentiment['label']}",
            body_style
        )
    )

    content.append(
        Paragraph(
            f"<b>Score:</b> {sentiment['score']}",
            body_style
        )
    )

    content.append(Spacer(1, 10))

    # ================= NEWS =================
    content.append(
    Paragraph(
        "INVESTMENT RECOMMENDATION",
        heading_style
    )
    )

    content.append(
        Paragraph(
            f"<b>Rating:</b> {recommendation['rating']}",
            body_style
        )
    )

    content.append(
        Paragraph(
            f"<b>Confidence:</b> {recommendation['confidence']}%",
            body_style
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            f"<b>Reason:</b> {recommendation['reason']}",
            body_style
        )
    )

    content.append(Spacer(1, 10))
    
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