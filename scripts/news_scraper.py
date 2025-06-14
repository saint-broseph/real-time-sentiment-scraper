import requests
from datetime import datetime
import streamlit as st

def get_news_articles(keyword, limit=20):
    api_key = st.secrets["NEWS_API_KEY"]
    url = f"https://newsapi.org/v2/everything?q={keyword}&sortBy=publishedAt&pageSize={limit}&language=en&apiKey={api_key}"

    try:
        response = requests.get(url)
        articles = response.json().get("articles", [])
        return [
            (f"{a['title']} {a.get('description', '')}", datetime.fromisoformat(a['publishedAt'].replace("Z", "+00:00")).replace(tzinfo=None)
            for a in articles if a.get('title') and a.get('publishedAt')
        ]
    except Exception as e:
        st.error("News API error: " + str(e))
        return []
