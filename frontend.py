import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="AI Stock Research",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Stock Research Dashboard")

# ================= INPUT =================
company = st.text_input(
    "Enter Company Name",
    placeholder="Example: TCS"
)

# ================= BUTTON =================
analyze_clicked = st.button("Analyze")

# ================= VALIDATION =================
if analyze_clicked and not company.strip():
    st.warning("⚠️ Please enter a company name")
    st.stop()

# ================= MAIN LOGIC =================
if analyze_clicked and company.strip():

    API_URL = "https://stock-ai-api-d3va.onrender.com"

    response = requests.post(
        f"{API_URL}/analyze",
        json={
            "company": company
        }
    )

    # ================= ERROR HANDLING =================
    if response.status_code != 200:
        st.error("Backend Error")
        st.write(response.text)
        st.stop()

    data = response.json()

    if data.get("status") == "error":
        st.error(data["message"])
        st.stop()

    stock = data["stock"]
    sentiment = data["sentiment"]
    recommendation = data["recommendation"]
    news = data["news"]
    analysis = data["analysis"]

    # ================= STOCK SNAPSHOT =================
    st.subheader("📊 Stock Snapshot")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Price", stock["price"])

    with col2:
        st.metric("P/E Ratio", stock["pe_ratio"])

    with col3:
        st.metric("Market Cap", stock["market_cap"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("1 Month Return", f"{stock['1_month_return']}%")

    with col2:
        st.metric("3 Month Return", f"{stock['3_month_return']}%")

    with col3:
        st.metric("6 Month Return", f"{stock['6_month_return']}%")

    # ================= CHART =================
    if "historical_prices" in stock:

        st.subheader("📈 Historical Price Trend")

        history = stock["historical_prices"]

        df = pd.DataFrame(history)
        df["date"] = pd.to_datetime(df["date"])

        st.line_chart(df.set_index("date")["close"])

    # ================= SENTIMENT =================
    st.subheader("📰 Sentiment Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Sentiment", sentiment["label"])

    with col2:
        st.metric("Score", sentiment["score"])

    # ================= RECOMMENDATION =================
    st.subheader("🎯 Recommendation")

    st.success(
        f"{recommendation['rating']} "
        f"({recommendation['confidence']}% confidence)"
    )

    st.write(f"**Reason:** {recommendation['reason']}")

    # ================= NEWS =================
    st.subheader("🗞 Latest News")

    for item in news:
        st.markdown(f"- [{item['title']}]({item['link']})")

    # ================= AI ANALYSIS =================
    st.subheader("🤖 AI Analysis")

    st.write(analysis)