import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="AI Stock Research",
    page_icon="📈",
    layout="wide"
)

API_URL = "https://stock-ai-api-d3va.onrender.com"

st.title("📈 AI Stock Research Dashboard")

# ================= INPUT =================
company = st.text_input(
    "Enter Company Name",
    placeholder="Examples: INFY, TCS, RELIANCE or INFY.BO"
)

st.caption(
    "Enter NSE symbols like INFY or TCS. "
    "For BSE stocks use the full symbol ending with .BO"
)

# ================= BUTTON =================
analyze_clicked = st.button("Analyze")

# ================= VALIDATION =================
if analyze_clicked and not company.strip():
    st.warning("⚠️ Please enter a company name")
    st.stop()

# ================= MAIN LOGIC =================
if analyze_clicked and company.strip():

    with st.spinner("📈 Researching stock and generating report..."):

        response = requests.post(
            f"{API_URL}/analyze",
            json={
                "company": company
            }
        )

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

        pdf_response = requests.post(
            f"{API_URL}/report",
            json={"company": company}
        )

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

    st.balloons()

    st.write(f"**Reason:** {recommendation['reason']}")

    # ================= NEWS =================
    st.subheader("🗞 Latest News")

    for item in news:
        st.markdown(f"- [{item['title']}]({item['link']})")

    # ================= AI ANALYSIS =================
    st.subheader("🤖 AI Analysis")

    lines = analysis.split("\n")

    if len(lines) > 0:
        analysis = "\n".join(lines[1:])

    analysis = analysis.replace(
        "EXECUTIVE SUMMARY",
        "## Executive Summary"
    )

    analysis = analysis.replace(
        "BULLISH FACTORS",
        "## Bullish Factors"
    )

    analysis = analysis.replace(
        "BEARISH FACTORS",
        "## Bearish Factors"
    )

    analysis = analysis.replace(
        "NEWS SENTIMENT ANALYSIS",
        "## News Sentiment Analysis"
    )

    analysis = analysis.replace(
        "RISK ASSESSMENT",
        "## Risk Assessment"
    )

    analysis = analysis.replace(
        "SHORT-TERM OUTLOOK (1-3 MONTHS)",
        "## Short-Term Outlook (1-3 Months)"
    )

    analysis = analysis.replace(
        "MEDIUM-TERM OUTLOOK (6-12 MONTHS)",
        "## Medium-Term Outlook (6-12 Months)"
    )

    analysis = analysis.replace(
        "OVERALL VIEW",
        "## Overall View"
    )

    st.markdown(analysis)

    st.subheader("📄 Download Report")

    if pdf_response.status_code == 200:

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_response.content,
            file_name=f"{company}_report.pdf",
            mime="application/pdf"
        )

st.divider()

st.header("📊 Compare Multiple Stocks")

compare_input = st.text_input(
    "Enter symbols separated by commas",
    placeholder="Example: INFY,TCS,WIPRO"
)

if st.button("Compare Stocks"):

    companies = [
        x.strip().upper()
        for x in compare_input.split(",")
        if x.strip()
    ]

    if len(companies) < 2:
        st.warning("Enter at least 2 stocks")
        st.stop()

    with st.spinner("Comparing stocks..."):

        response = requests.post(
            f"{API_URL}/compare",
            json={
                "companies": companies
            }
        )

    if response.status_code != 200:
        st.error("Comparison failed")
        st.stop()

    data = response.json()

    if data.get("status") == "error":
        st.error(data["message"])
        st.stop()

    st.subheader("🏆 Best Pick")

    st.success(
        f"{data['best_pick']} "
        f"(Score: {round(data['best_pick_score'], 2)})"
    )

    st.write(data["reason"])

    winner = next(
    item
    for item in data["comparison"]
        if item["company"] == data["best_pick"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Price",
            winner["price"]
        )

    with col2:
        st.metric(
            "Recommendation",
            winner["rating"]
        )

    with col3:
        st.metric(
            "Confidence",
            f"{winner['confidence']}%"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "1M Return",
            f"{winner['1_month_return']}%"
        )

    with col2:
        st.metric(
            "3M Return",
            f"{winner['3_month_return']}%"
        )

    with col3:
        st.metric(
            "6M Return",
            f"{winner['6_month_return']}%"
        )

    st.subheader("📋 Comparison Table")

    df = pd.DataFrame(data["comparison"])

    df = df.rename(columns={
        "company": "Company",
        "price": "Price",
        "1_month_return": "1M Return",
        "3_month_return": "3M Return",
        "6_month_return": "6M Return",
        "sentiment": "Sentiment",
        "sentiment_score": "Sentiment Score",
        "rating": "Rating",
        "confidence": "Confidence",
        "score": "Score"
    })

    df["Rating"] = df["Rating"].replace({
        "BUY": "🟢 BUY",
        "HOLD": "🟡 HOLD",
        "SELL": "🔴 SELL"
    })

    df = df.sort_values(
        by="Score",
        ascending=False
    )

    styled_df = df.style.map(
        lambda x:
            "background-color: #90EE90"
            if x == "BUY"
            else (
                "background-color: #FFD580"
                if x == "HOLD"
                else (
                    "background-color: #FF7F7F"
                    if x == "SELL"
                    else ""
                )
            ),
        subset=["Rating"]
    )

    st.dataframe(
        styled_df,
        use_container_width=True
    )

    st.divider()

    st.subheader("📄 Download Comparison Report")

    compare_pdf_response = requests.post(
        f"{API_URL}/compare-report",
        json={
            "companies": companies
        }
    )

    if compare_pdf_response.status_code == 200:

        st.download_button(
            label="📄 Download Comparison PDF",
            data=compare_pdf_response.content,
            file_name="comparison_report.pdf",
            mime="application/pdf"
        )

    else:

        st.error("Failed to generate comparison PDF")


st.divider()
st.header("💬 AI Stock Chat Assistant")

chat_company = st.text_input("Enter Company for Chat", placeholder="INFY")

user_question = st.text_input("Ask a question", placeholder="Should I buy this stock?")

if st.button("Ask AI"):

    if not chat_company or not user_question:
        st.warning("Please enter both company and question")
        st.stop()

    with st.spinner("Thinking... 🤖"):

        chat_response = requests.post(
            f"{API_URL}/chat",
            json={
                "company": chat_company,
                "question": user_question
            }
        )

    if chat_response.status_code != 200:
        st.error("Chat API failed")
        st.write(chat_response.text)
        st.stop()

    data = chat_response.json()

    if data.get("status") == "error":
        st.error(data["message"])
        st.stop()

    st.success(data["answer"])