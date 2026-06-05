# AI Stock Research API

AI-powered stock research platform that combines:

- Real-time stock market data
- Latest company news
- AI-generated investment analysis
- Professional PDF report generation
- FastAPI REST API
- Cloud deployment support

---

## Features

### Stock Data Analysis
Fetches:

- Current Stock Price
- Market Capitalization
- PE Ratio
- Sector Information
- 1 Month Return
- 3 Month Return
- 6 Month Return

Source: Yahoo Finance

---

### News Aggregation

Collects latest company news using RSS feeds and extracts:

- Headline
- News Link

---

### AI-Powered Analysis

Generates:

- Executive Summary
- Bullish Factors
- Bearish Factors
- News Sentiment Analysis
- Risk Assessment
- Short-Term Outlook
- Medium-Term Outlook
- Overall View

Powered by Google Gemini.

---

### PDF Report Generation

Creates downloadable research reports in PDF format.

Includes:

- Stock Snapshot
- News Highlights
- Investment Analysis
- Risk Assessment
- Outlook

---

## API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok",
  "message": "API is running"
}
```

### Analyze Stock

```http
POST /analyze
```

Request:

```json
{
  "symbol": "INFY.NS",
  "company": "Infosys"
}
```

Response:

```json
{
  "stock": {},
  "news": [],
  "analysis": ""
}
```

### Download PDF Report

```http
POST /report
```

Request:

```json
{
  "symbol": "INFY.NS",
  "company": "Infosys"
}
```

Returns:

- PDF Research Report

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- Google Gemini AI
- Yahoo Finance (yfinance)
- Feedparser
- ReportLab
- Render Deployment

---

## Project Structure

```text
stock_ai_project/
│
├── main.py
├── data_fetcher.py
├── news_fetcher.py
├── ai_analyzer.py
├── pdf_generator.py
├── requirements.txt
├── .env
├── reports/
└── README.md
```

---

## Installation

Clone repository:

```bash
git clone <repository-url>
cd stock_ai_project
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create .env file:

```env
GEMINI_API_KEY=your_api_key_here
```

Run locally:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Deployment

This project can be deployed on:

- Render
- Railway
- AWS EC2
- Azure
- Google Cloud

---

## Disclaimer

This project is for educational and research purposes only.

It does not provide financial advice, investment recommendations, or guarantees of future returns.