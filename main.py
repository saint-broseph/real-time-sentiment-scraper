from scripts.twitter_scraper import get_tweets
from scripts.sentiment import analyze_sentiment
from scripts.news_scraper import get_news_articles
import pandas as pd
from datetime import datetime
from scripts.reddit_scraper import get_reddit_posts
from scripts.plot_sentiment import plot_sentiment


def collect_sentiment_all(keyword="Adani", count=20):
    tweets = get_tweets(keyword, count=count)
    reddit_posts = get_reddit_posts(keyword, limit=count)
    news_articles = get_news_articles(keyword, limit=count)

    data = []

    for tweet in tweets:
        score = analyze_sentiment(tweet)
        data.append(["Twitter", datetime.now(), tweet, score])

    for post in reddit_posts:
        score = analyze_sentiment(post)
        data.append(["Reddit", datetime.now(), post, score])

    for text, ts in news_articles:
        score = analyze_sentiment(text)
        data.append(["News", ts, text, score])

    df = pd.DataFrame(data, columns=["Platform", "Timestamp", "Text", "Sentiment"])
    filename = f"data/{keyword.lower()}_sentiment.csv"
    df.to_csv(filename, index=False)
    print(f"\n✅ Saved to {filename}\n")
    print(df.head())
    plot_sentiment(filename)
if __name__ == "__main__":
    collect_sentiment_all("Adani", count=20)

