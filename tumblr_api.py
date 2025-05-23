import os
import requests
from dotenv import load_dotenv

# Load .env variables
dotenv_path = r"C:\Users\maukd\OneDrive\Pictures\ajay-project\.env"
load_dotenv(dotenv_path)

API_KEY = os.getenv("TUMBLR_API_KEY")

def fetch_tumblr_posts(tag="AI", limit=10):
    """
    Fetch recent posts by tag from Tumblr public API.
    Returns a list of post texts (summary, body, or caption).
    """
    url = f"https://api.tumblr.com/v2/tagged?tag={tag}&api_key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        posts = data.get("response", [])
        texts = []
        for post in posts:
            # Prefer summary, fallback to body or caption
            if "summary" in post:
                texts.append(post["summary"])
            elif "body" in post:
                texts.append(post["body"])
            elif "caption" in post:
                texts.append(post["caption"])
        return texts[:limit]
    except Exception as e:
        print(f"[ERROR] Tumblr tag search failed: {e}")
        return []

def fetch_tumblr_posts_by_blog(blog_name, limit=10):
    """
    Fetch recent posts from a specific Tumblr blog.
    Returns a list of post texts (summary, caption, or body).
    """
    url = f"https://api.tumblr.com/v2/blog/{blog_name}.tumblr.com/posts?api_key={API_KEY}&limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        posts = data.get("response", {}).get("posts", [])
        texts = []
        for post in posts:
            if "summary" in post:
                texts.append(post["summary"])
            elif "caption" in post:
                texts.append(post["caption"])
            elif "body" in post:
                texts.append(post["body"])
        return texts[:limit]
    except Exception as e:
        print(f"[ERROR] Tumblr blog fetch failed: {e}")
        return []

# Example usage for sentiment analysis:
if __name__ == "__main__":
    tag_posts = fetch_tumblr_posts(tag="AI", limit=10)
    print("Posts by tag 'AI':")
    for p in tag_posts:
        print(p)
        print("-" * 40)

    blog_posts = fetch_tumblr_posts_by_blog(blog_name="staff", limit=5)
    print("Posts by blog 'staff':")
    for p in blog_posts:
        print(p)
        print("-" * 40)
