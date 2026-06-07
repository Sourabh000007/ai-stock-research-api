import feedparser
from urllib.parse import quote_plus


def get_news(company):

    query = quote_plus(f"{company} share market")

    url = (
        f"https://news.google.com/rss/search?"
        f"q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(url)

    news_list = []

    for entry in feed.entries[:5]:

        news_list.append({
            "title": entry.title,
            "link": entry.link
        })

    return news_list