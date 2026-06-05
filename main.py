from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from data_fetcher import get_stock_data
from news_fetcher import get_news
from ai_analyzer import analyze_stock
from pdf_generator import create_pdf
import os

# ---------------- APP INIT ----------------
app = FastAPI(
    title="AI Stock Research API",
    description="Generates stock analysis + PDF reports using AI",
    version="1.0"
)

# ---------------- REQUEST MODEL ----------------
class StockRequest(BaseModel):
    symbol: str
    company: str


# ---------------- FOLDERS ----------------
REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)


# ---------------- PIPELINE FUNCTION ----------------
def run_pipeline(symbol: str, company: str):
    try:
        stock = get_stock_data(symbol)
        news = get_news(company)
        analysis = analyze_stock(stock, news)

        return stock, news, analysis

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
        stock, news, analysis = run_pipeline(
            req.symbol,
            req.company
        )

        return {
            "stock": stock,
            "news": news,
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
        stock, news, analysis = run_pipeline(
            req.symbol,
            req.company
        )

        file_path = f"{REPORT_FOLDER}/{req.company}_report.pdf"

        create_pdf(
            stock,
            news,
            analysis,
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