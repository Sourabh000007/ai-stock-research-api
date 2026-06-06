def generate_recommendation(stock, sentiment):

    score = 0

    # Returns
    if stock["1_month_return"] > 0:
        score += 1

    if stock["3_month_return"] > 0:
        score += 1

    if stock["6_month_return"] > 0:
        score += 1

    # Sentiment
    score += sentiment["score"]

    # Decision
    if score >= 3:
        rating = "BUY"

    elif score <= -3:
        rating = "SELL"

    else:
        rating = "HOLD"

    confidence = min(
        95,
        max(
            55,
            50 + abs(score) * 5
        )
    )

    if rating == "BUY":
        reason = (
            "Positive price momentum and favorable news sentiment."
        )

    elif rating == "SELL":
        reason = (
            "Negative momentum and bearish news sentiment."
        )

    else:
        reason = (
            "Mixed signals. Wait for stronger confirmation."
        )

    return {
        "rating": rating,
        "confidence": confidence,
        "reason": reason
    }