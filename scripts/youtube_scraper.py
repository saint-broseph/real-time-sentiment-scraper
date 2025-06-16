from youtube_transcript_api import YouTubeTranscriptApi
from youtubesearchpython import VideosSearch, Comments
from datetime import datetime

def get_youtube_data(keyword, video_limit=5, comments_per_video=5):
    results = []

    try:
        videos = VideosSearch(keyword, limit=video_limit).result()['result']
        for video in videos:
            video_id = video['id']

            # --- Transcript ---
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                full_text = " ".join([seg['text'] for seg in transcript])
                results.append((f"[Transcript] {full_text}", datetime.now()))
            except Exception:
                pass  # Some videos have no transcript

            # --- Comments ---
            try:
                comments = Comments(video_id).result()['comments'][:comments_per_video]
                for comment in comments:
                    results.append((f"[Comment] {comment['content']}", datetime.now()))
            except Exception:
                pass

    except Exception:
        return []

    return results
