import os
import praw
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_reddit_comments_by_keyword(keyword, limit=20):
    posts = []
    try:
        for submission in reddit.subreddit("all").search(keyword, sort="relevance", limit=limit):
            if submission.title:
                posts.append(submission.title)
            if submission.selftext:
                posts.append(submission.selftext)
    except Exception as e:
        print(f"[ERROR] Reddit keyword search failed: {e}")
    return posts

def fetch_reddit_comments_by_user(username, limit=20):
    comments = []
    try:
        redditor = reddit.redditor(username)
        for comment in redditor.comments.new(limit=limit):
            comments.append(comment.body)
    except Exception as e:
        print(f"[ERROR] Reddit user fetch failed: {e}")
    return comments
