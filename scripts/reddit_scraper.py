import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def get_reddit_posts(keyword, limit=20, subreddit="stocks"):
    posts = reddit.subreddit(subreddit).search(keyword, sort='new', limit=limit)
    return [post.title + " " + post.selftext for post in posts]
