def calculate_sentiment(news):

    positive_words = [
        "rise", "rising", "gain", "gains", "jump",
        "surge", "bullish", "strong", "growth",
        "positive", "recovery", "up"
    ]

    negative_words = [
        "fall", "falling", "crash", "slump",
        "drop", "bearish", "weak", "decline",
        "negative", "pressure", "loss", "down"
    ]

    score = 0

    for item in news:

        title = item["title"].lower()

        for word in positive_words:
            if word in title:
                score += 1

        for word in negative_words:
            if word in title:
                score -= 1

    if score > 0:
        label = "POSITIVE"
    elif score < 0:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"

    return {
        "score": score,
        "label": label
    }