from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
import os
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 AI Stock Research Bot is running!"
    )


async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage:\n/analyze INFY"
        )
        return

    company = context.args[0]

    await update.message.reply_text(
        "📊 Fetching stock data...\n📰 Analyzing news sentiment...\n🤖 Generating AI report..."
    )

    response = requests.post(
        "http://127.0.0.1:8000/analyze",
        json={
            "company": company
        }
    )

    data = response.json()

    if data.get("status") == "error":

        await update.message.reply_text(
            data["message"]
        )
        return

    stock = data["stock"]
    recommendation = data["recommendation"]

    message = f"""
📈 {company}

Price: {stock['price']}

Rating: {recommendation['rating']}

Confidence: {recommendation['confidence']}%

Reason:
{recommendation['reason']}
"""

    await update.message.reply_text(message)

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage:\n/report INFY"
        )
        return

    company = context.args[0]

    await update.message.reply_text(
        f"🤖 Generating AI report for {company}..."
    )

    response = requests.post(
        "http://127.0.0.1:8000/analyze",
        json={
            "company": company
        }
    )

    data = response.json()

    if data.get("status") == "error":

        await update.message.reply_text(
            data["message"]
        )
        return

    analysis = data["analysis"]

    # Telegram messages have a length limit
    if len(analysis) > 3500:
        analysis = analysis[:3500] + "\n\n...Report truncated..."

    analysis = data["analysis"]

    analysis = analysis.replace(
        "## Executive Summary",
        "📌 Executive Summary"
    )

    analysis = analysis.replace(
        "## Bullish Factors",
        "📈 Bullish Factors"
    )

    analysis = analysis.replace(
        "## Bearish Factors",
        "📉 Bearish Factors"
    )

    analysis = analysis.replace(
        "## News Sentiment Analysis",
        "📰 News Sentiment Analysis"
    )

    analysis = analysis.replace(
        "## Risk Assessment",
        "⚠️ Risk Assessment"
    )

    analysis = analysis.replace(
        "## Short-Term Outlook (1-3 Months)",
        "⏳ Short-Term Outlook (1-3 Months)"
    )

    analysis = analysis.replace(
        "## Medium-Term Outlook (6-12 Months)",
        "📅 Medium-Term Outlook (6-12 Months)"
    )

    analysis = analysis.replace(
        "## Overall View",
        "🎯 Overall View"
    )

    analysis = analysis.replace(
        "## Investment Rating",
        "⭐ Investment Rating"
    )

    await update.message.reply_text(analysis)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("analyze", analyze)
)

app.add_handler(
    CommandHandler("report", report)
)

print("Telegram bot starting...")
app.run_polling()