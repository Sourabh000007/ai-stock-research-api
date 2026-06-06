def get_symbol(company_name: str):

    mapping = {
        "TCS": "TCS.NS",
        "INFY": "INFY.NS",
        "RELIANCE": "RELIANCE.NS",
        "HDFC": "HDFCBANK.NS",
        "HDFCBANK": "HDFCBANK.NS",
        "ITC": "ITC.NS",
        "WIPRO": "WIPRO.NS",
        "LT": "LT.NS",
    }

    key = company_name.upper().strip()

    return mapping.get(key, None)