from data_fetcher import get_stock_data
from news_fetcher import get_news
from ai_analyzer import analyze_stock

def run_analysis(symbol: str, company: str):

    stock = get_stock_data(symbol)
    news = get_news(company)
    analysis = analyze_stock(stock, news)

    return stock, news, analysis