from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_stock(stock_data, news_data):

    news_text = ""

    for item in news_data:
        news_text += f"- {item['title']}\n"

    prompt = f"""
    You are a stock market research assistant.

    Stock Information:
    {stock_data}

    Recent News:
    {news_text}

    Act as a professional stock market research analyst.

    Analyze the stock using:
    1. Company fundamentals
    2. Recent news sentiment
    3. Historical returns
    4. Valuation metrics

    Provide:

    1. Executive Summary
    2. Bullish Factors
    3. Bearish Factors
    4. News Sentiment Analysis
    5. Risk Assessment
    6. Short-Term Outlook (1-3 months)
    7. Medium-Term Outlook (6-12 months)
    8. Overall View

    Important:
    - Do not guarantee returns.
    - Do not give financial advice.
    - Mention both positives and negatives.
    - Use the stock data and news provided.
    - Keep the explanation simple for retail investors.
    - Do NOT use markdown.
    - Do NOT use ###, ####, **, *, or ---.
    - Use plain text headings only.
    - Format the response as a professional report.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text