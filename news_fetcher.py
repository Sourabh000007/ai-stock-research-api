import feedparser

def get_news(company):

    url = f"https://news.google.com/rss/search?q={company}+share+market&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    news_list = []

    for entry in feed.entries[:5]:

        news_list.append({
            "title": entry.title,
            "link": entry.link
        })

    return news_list