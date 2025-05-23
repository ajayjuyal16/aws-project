import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import os
from dotenv import load_dotenv

dotenv_path = r"C:\Users\maukd\OneDrive\Pictures\ajay-project\.env"
load_dotenv(dotenv_path)

from reddit_api import fetch_reddit_comments_by_keyword, fetch_reddit_comments_by_user
from youtube_api import fetch_youtube_comments, fetch_youtube_comments_by_channel
from tumblr_api import fetch_tumblr_posts, fetch_tumblr_posts_by_blog
from sentiment import analyze_sentiment

st.set_page_config(layout="wide")
st.title("🧠 Live Sentiment Analysis Dashboard")

platform = st.selectbox("Choose platform", ["Reddit", "YouTube", "Tumblr"])

if platform == "Reddit":
    username = st.text_input("Enter Reddit username (leave empty to search keyword):")
    if username:
        query = None
    else:
        query = st.text_input("Enter keyword to search:")
elif platform == "YouTube":
    username = st.text_input("Enter YouTube channel ID (leave empty if you want to input video ID):")
    query = st.text_input("Enter video ID (if channel ID empty):")
elif platform == "Tumblr":
    username = st.text_input("Enter Tumblr blog name (leave empty to search by tag):")
    if not username:
        query = st.text_input("Enter tag to search:")
    else:
        query = None

limit = st.slider("How many items?", 5, 50, 20)
refresh = st.checkbox("🔄 Auto-refresh every 60 seconds")
last_updated = st.empty()

def analyze_platform(platform, username, query, limit):
    try:
        if platform == "Reddit":
            if username:
                return fetch_reddit_comments_by_user(username, limit)
            elif query:
                return fetch_reddit_comments_by_keyword(query, limit)  
        elif platform == "YouTube":
            if username:
                return fetch_youtube_comments_by_channel(username, limit)
            elif query:
                return fetch_youtube_comments(query, limit)
        elif platform == "Tumblr":
            if username:
                return fetch_tumblr_posts_by_blog(username, limit)
            elif query:
                return fetch_tumblr_posts(query, limit)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    return []

def run_analysis():
    st.info("Fetching live data...")
    comments = analyze_platform(platform, username, query, limit)

    if not comments:
        st.warning("No comments/posts found. Try a different input.")
        return

    results = []
    for text in comments:
        label, score = analyze_sentiment(text)
        results.append({"Text": text, "Sentiment": label, "Score": score})

    df = pd.DataFrame(results)
    st.dataframe(df)


    st.subheader("📊 Sentiment Distribution")
    sentiment_counts = df["Sentiment"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%")
    st.pyplot(fig)

    last_updated.text(f"Last updated at {time.strftime('%H:%M:%S')}")

if st.button("Analyze") or refresh:
    while True:
        run_analysis()
        if not refresh:
            break
        time.sleep(60)
        st.experimental_rerun()
