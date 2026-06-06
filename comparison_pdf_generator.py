from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def create_comparison_pdf(
    comparison_data,
    best_pick,
    best_pick_score,
    reason,
    filename
):
    
        pdf = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "MULTI-STOCK COMPARISON REPORT",
                styles["Title"]
            )
        )

        content.append(Spacer(1, 12))

        content.append(
            Paragraph(
                f"<b>Best Pick:</b> {best_pick}",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Score:</b> {best_pick_score}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Reason:</b> {reason}",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 12))


        table_data = [
            [
                "Company",
                "Price",
                "1M Return",
                "3M Return",
                "6M Return",
                "Sentiment",
                "Rating",
                "Score"
            ]
        ]

        for stock in comparison_data:

            table_data.append(
                [
                    stock["company"],
                    stock["price"],
                    stock["1_month_return"],
                    stock["3_month_return"],
                    stock["6_month_return"],
                    stock["sentiment"],
                    stock["rating"],
                    round(stock["score"], 2)
                ]
            )

            table = Table(table_data)

            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ]
                )
            )

        content.append(table)

        content.append(Spacer(1, 12))

        content.append(
            Paragraph(
                "COMPARISON SUMMARY",
                styles["Heading1"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Best Stock:</b> {best_pick}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Why?</b> {reason}",
                styles["Normal"]
            )
        )

        sorted_stocks = sorted(
            comparison_data,
            key=lambda x: x["score"],
            reverse=True
        )

        if len(sorted_stocks) > 1:

            content.append(
                Paragraph(
                    f"<b>Runner Up:</b> {sorted_stocks[1]['company']}",
                    styles["Normal"]
                )
            )

        content.append(
            Paragraph(
                f"<b>Weakest Stock:</b> {sorted_stocks[-1]['company']}",
                styles["Normal"]
            )
        )

        pdf.build(content)