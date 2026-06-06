import yfinance as yf

def format_market_cap(value):
    if not value:
        return "N/A"
    return f"₹{value/1e12:.2f} Trillion"

def get_stock_data(symbol):

    ticker = yf.Ticker(symbol)

    history = ticker.history(period="6mo")

    historical_data = []

    for date, row in history.iterrows():
        historical_data.append({
            "date": str(date.date()),
            "close": round(row["Close"], 2)
        })

    current_price = history["Close"].iloc[-1]

    one_month_price = history["Close"].iloc[-22]

    three_month_price = history["Close"].iloc[-66]

    six_month_price = history["Close"].iloc[0]

    one_month_return = (
    (current_price - one_month_price)
    / one_month_price
    ) * 100

    three_month_return = (
        (current_price - three_month_price)
        / three_month_price
    ) * 100

    six_month_return = (
        (current_price - six_month_price)
        / six_month_price
    ) * 100

    info = ticker.info

    stock_data = {
        "name": info.get("longName"),
        "price": info.get("currentPrice"),
        "sector": info.get("sector"),
        "market_cap": format_market_cap(info.get("marketCap")),
        "pe_ratio": info.get("trailingPE"),
        "1_month_return": float(round(one_month_return, 2)),
        "3_month_return": float(round(three_month_return, 2)),
        "6_month_return": float(round(six_month_return, 2)),
        "historical_prices": historical_data
    }

    return stock_data, history