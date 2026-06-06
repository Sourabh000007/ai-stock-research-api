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

import os

# ---------------- APP INIT ----------------
app = FastAPI(
    title="AI Stock Research API",
    description="Generates stock analysis + PDF reports using AI",
    version="1.0"
)

# ---------------- REQUEST MODEL ----------------
class StockRequest(BaseModel):
    company: str


# ---------------- FOLDERS ----------------
REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)


# ---------------- PIPELINE FUNCTION ----------------
def run_pipeline(company: str):
    try:

        symbol = get_symbol(company)

        if not symbol:
            raise Exception(f"Unknown company: {company}")

        stock, history = get_stock_data(symbol)
        news = get_news(company)
        analysis = analyze_stock(stock, news)

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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)