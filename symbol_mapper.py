def get_symbol(user_input: str):

    symbol = user_input.upper().strip()

    # User already specified exchange
    if symbol.endswith(".NS") or symbol.endswith(".BO"):
        return symbol

    # Default to NSE
    return f"{symbol}.NS"