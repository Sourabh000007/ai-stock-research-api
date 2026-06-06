import matplotlib.pyplot as plt


def create_stock_chart(history, filename):

    plt.figure(figsize=(8, 4))

    plt.plot(
        history.index,
        history["Close"]
    )

    plt.title("6 Month Stock Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()