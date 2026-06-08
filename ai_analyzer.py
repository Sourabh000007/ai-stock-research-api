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
        You are a professional stock market research analyst.

        Stock Information:
        {stock_data}

        Recent News:
        {news_text}

        Analyze the stock using:
        1. Company fundamentals
        2. Recent news sentiment
        3. Historical returns
        4. Valuation metrics

        Formatting Rules:
        - Use simple language for retail investors.
        - Keep each section concise.
        - Executive Summary must be under 60 words.
        - Use bullet points for Bullish Factors, Bearish Factors, and Risk Assessment.
        - Use 3 to 5 bullets per section.
        - Do not write long paragraphs.
        - Do not use ALL CAPS headings.
        - Do not add a report title.
        - Do not add a disclaimer.
        - Do not say "This is not financial advice".
        - Mention both positives and negatives.

        Return the response in this exact format:

        ## Executive Summary

        Short summary of the stock.

        ## Bullish Factors

        - Point 1
        - Point 2
        - Point 3

        ## Bearish Factors

        - Point 1
        - Point 2
        - Point 3

        ## News Sentiment Analysis

        Short sentiment analysis.

        ## Risk Assessment

        - Risk 1
        - Risk 2
        - Risk 3

        ## Short-Term Outlook (1-3 Months)

        Short outlook.

        ## Medium-Term Outlook (6-12 Months)

        Short outlook.

        ## Overall View

        Short conclusion.

        ## Investment Rating

        BUY / HOLD / SELL

        Confidence: XX%

        IMPORTANT:
        Use Markdown headings exactly as shown above.
        Do not add any other sections.
        """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text

def chat_with_stock(context, question):

    prompt = f"""
        You are a stock market assistant.

        Answer using only the information available in the context.

        CONTEXT:
        {context}

        QUESTION:
        {question}

        Rules:
        - Keep the answer under 150 words.
        - Use simple language.
        - Explain the reasoning clearly.
        - If information is unavailable, say so.
        - Do not invent facts.
        - Do not add a disclaimer.
        """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text