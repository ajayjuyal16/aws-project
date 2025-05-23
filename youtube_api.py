import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_youtube_comments(video_id, max_results=20):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.commentThreads().list(
        part="snippet", videoId=video_id, maxResults=max_results, textFormat="plainText"
    )
    response = request.execute()
    comments = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response["items"]]
    return comments

def fetch_youtube_comments_by_channel(channel_id, max_results=20):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    comments = []

    channel_response = youtube.channels().list(part="contentDetails", id=channel_id).execute()
    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    playlist_items = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist_id,
        maxResults=max_results
    ).execute()

    video_ids = [item["snippet"]["resourceId"]["videoId"] for item in playlist_items["items"]]


    for vid in video_ids:
        if len(comments) >= max_results:
            break
        try:
            comment_request = youtube.commentThreads().list(
                part="snippet",
                videoId=vid,
                maxResults=min(10, max_results - len(comments)),
                textFormat="plainText"
            )
            response = comment_request.execute()
            for item in response.get("items", []):
                comments.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
        except Exception as e:
            print(f"Error fetching comments for video {vid}: {e}")

    return comments[:max_results]
