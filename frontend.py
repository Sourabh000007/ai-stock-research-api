import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="AI Stock Research",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Stock Research Dashboard")

company = st.text_input(
    "Enter Company Name",
    placeholder="Example: TCS"
)

if st.button("Analyze"):

    response = requests.post(
        "http://127.0.0.1:8000/analyze",
        json={
            "company": company
        }
    )

    data = response.json()

    stock = data["stock"]
    sentiment = data["sentiment"]
    recommendation = data["recommendation"]
    news = data["news"]
    analysis = data["analysis"]

    st.subheader("📊 Stock Snapshot")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Price",
            stock["price"]
        )

    with col2:
        st.metric(
            "P/E Ratio",
            stock["pe_ratio"]
        )

    with col3:
        st.metric(
            "Market Cap",
            stock["market_cap"]
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "1 Month Return",
            f"{stock['1_month_return']}%"
        )

    with col2:
        st.metric(
            "3 Month Return",
            f"{stock['3_month_return']}%"
        )

    with col3:
        st.metric(
            "6 Month Return",
            f"{stock['6_month_return']}%"
        )

    # Historical Price Chart
    if "historical_prices" in stock:

        st.subheader("📈 Historical Price Trend")

        history = stock["historical_prices"]

        df = pd.DataFrame(history)

        df["date"] = pd.to_datetime(df["date"])

        st.line_chart(
            df.set_index("date")["close"]
        )

    st.subheader("📰 Sentiment Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Sentiment",
            sentiment["label"]
        )

    with col2:
        st.metric(
            "Score",
            sentiment["score"]
        )

    st.subheader("🎯 Recommendation")

    st.success(
        f"{recommendation['rating']} "
        f"({recommendation['confidence']}% confidence)"
    )

    st.write(
        f"**Reason:** {recommendation['reason']}"
    )

    st.subheader("🗞 Latest News")

    for item in news:
        st.markdown(
            f"- [{item['title']}]({item['link']})"
        )

    st.subheader("🤖 AI Analysis")

    st.write(analysis)