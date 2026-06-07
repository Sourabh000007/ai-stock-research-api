from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from data_fetcher import get_stock_data
from news_fetcher import get_news
from ai_analyzer import analyze_stock
from pdf_generator import create_pdf
from symbol_mapper import get_symbol  
from sentiment_analyzer import calculate_sentiment
from recommendation_engine import generate_recommendation
from comparison_pdf_generator import create_comparison_pdf
import google.generativeai as genai
from pydantic import BaseModel

import os

genai.configure(api_key="YOUR_GEMINI_API_KEY")

# ---------------- APP INIT ----------------
app = FastAPI(
    title="AI Stock Research API",
    description="Generates stock analysis + PDF reports using AI",
    version="1.0"
)

# ---------------- REQUEST MODEL ----------------
class StockRequest(BaseModel):
    company: str

class CompareRequest(BaseModel):
    companies: list[str]

class ChatRequest(BaseModel):
    company: str
    question: str

# ---------------- FOLDERS ----------------
REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

COMPARE_REPORT_FOLDER = "comparison_reports"
os.makedirs(COMPARE_REPORT_FOLDER, exist_ok=True)

# ---------------- PIPELINE FUNCTION ----------------
def run_pipeline(company: str):
    try:

        symbol = get_symbol(company)

        if not symbol:
            raise Exception(f"Unknown company: {company}")

        stock, history = get_stock_data(symbol)
        news = get_news(company)
        try:
            analysis = analyze_stock(stock, news)
        except Exception:
            analysis = "AI temporarily unavailable due to quota limits."

        sentiment = calculate_sentiment(news)

        recommendation = generate_recommendation(
            stock,
            sentiment
        )

        return (
            stock,
            news,
            analysis,
            history,
            sentiment,
            recommendation
        )

    except Exception as e:
        raise Exception(f"Pipeline Error: {str(e)}")


# ---------------- HEALTH ----------------
@app.get("/health")
def health():
    return {"status": "ok", "message": "API is running"}


# ---------------- ANALYZE ----------------
@app.post("/analyze")
def analyze(req: StockRequest):

    try:
        stock, news, analysis, history, sentiment, recommendation = run_pipeline(
            req.company
        )

        return {
            "stock": stock,
            "news": news,
            "sentiment": sentiment,
            "recommendation": recommendation,
            "analysis": analysis
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ---------------- REPORT (PDF DOWNLOAD) ----------------
@app.post("/report")
def generate_report(req: StockRequest):

    try:
        stock, news, analysis, history, sentiment, recommendation  = run_pipeline(
            req.company
        )

        safe_name = req.company.replace(" ", "_").replace("/", "_")

        file_path = f"{REPORT_FOLDER}/{safe_name}_report.pdf"

        create_pdf(
            stock,
            news,
            analysis,
            history,
            sentiment,
            recommendation,
            file_path
        )

        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=f"{req.company}_report.pdf"
        )

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/compare")
def compare_stocks(req: CompareRequest):

    results = []

    for company in req.companies:

        stock, news, analysis, history, sentiment, recommendation = run_pipeline(
            company
        )

        score = (
            stock["1_month_return"]
            + stock["3_month_return"]
            + stock["6_month_return"]
            + (sentiment["score"] * 10)
        )

        results.append({
            "company": company,
            "price": stock["price"],
            "1_month_return": stock["1_month_return"],
            "3_month_return": stock["3_month_return"],
            "6_month_return": stock["6_month_return"],
            "sentiment": sentiment["label"],
            "sentiment_score": sentiment["score"],
            "rating": recommendation["rating"],
            "confidence": recommendation["confidence"],
            "score": score
        })

    best_stock = max(
        results,
        key=lambda x: x["score"]
    )

    return {
        "best_pick": best_stock["company"],
        "best_pick_score": best_stock["score"],
        "reason": (
            f"{best_stock['company']} has the strongest "
            "combination of returns and sentiment."
        ),
        "comparison": results
    }


@app.post("/compare-report")
def compare_report(req: CompareRequest):

    results = []

    for company in req.companies:

        stock, news, analysis, history, sentiment, recommendation = run_pipeline(
            company
        )

        score = (
            stock["1_month_return"]
            + stock["3_month_return"]
            + stock["6_month_return"]
            + (sentiment["score"] * 10)
        )

        results.append({
            "company": company,
            "price": stock["price"],
            "1_month_return": stock["1_month_return"],
            "3_month_return": stock["3_month_return"],
            "6_month_return": stock["6_month_return"],
            "sentiment": sentiment["label"],
            "rating": recommendation["rating"],
            "score": score
        })

    best_stock = max(
        results,
        key=lambda x: x["score"]
    )

    reason = (
        f"{best_stock['company']} has the strongest "
        "combination of returns and sentiment."
    )

    file_path = (
        f"{COMPARE_REPORT_FOLDER}/comparison_report.pdf"
    )

    create_comparison_pdf(
        results,
        best_stock["company"],
        best_stock["score"],
        reason,
        file_path
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="comparison_report.pdf"
    )


@app.post("/chat")
def chat(req: ChatRequest):

    try:
        stock, news, analysis, history, sentiment, recommendation = run_pipeline(req.company)

        # Build compact context (IMPORTANT: keeps token usage LOW)
        context = f"""
        Company: {stock['name']}
        Price: {stock['price']}
        Sector: {stock['sector']}
        Market Cap: {stock['market_cap']}
        1M Return: {stock['1_month_return']}
        3M Return: {stock['3_month_return']}
        6M Return: {stock['6_month_return']}
        Sentiment: {sentiment['label']}
        News Summary: {news[:3]}
        Recommendation: {recommendation['rating']} ({recommendation['confidence']}%)
        """

        model = genai.GenerativeModel("Gemini 3.1 Flash Lite")

        prompt = f"""
        You are a stock market assistant.

        Use the context below to answer user questions.

        CONTEXT:
        {context}

        USER QUESTION:
        {req.question}

        Give:
        - Simple explanation
        - Clear reasoning
        - No financial advice disclaimer
        """

        response = model.generate_content(prompt)

        return {
            "answer": response.text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)