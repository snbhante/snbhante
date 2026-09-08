#!/usr/bin/env python3
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID", "UC3WIwB7nbYMEvWW4CGQGYsA")

if not API_KEY:
    raise SystemExit("YOUTUBE_API_KEY is not set. Add it as a GitHub repository secret.")


def fetch_json(url: str):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def iso_to_date(value: str) -> str:
    if not value:
        return "N/A"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except ValueError:
        return value[:10]


def iso_duration_to_minutes(value: str) -> str:
    if not value:
        return "N/A"
    match = re.search(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value)
    if not match:
        return value
    hours, minutes, seconds = match.groups()
    total_minutes = int(hours or 0) * 60 + int(minutes or 0)
    if total_minutes == 0 and seconds:
        return f"0:{int(seconds):02d}"
    if hours:
        return f"{total_minutes}:{int(seconds or 0):02d}"
    return f"{total_minutes}:{int(seconds or 0):02d}"


def get_channel_stats():
    url = (
        "https://www.googleapis.com/youtube/v3/channels"
        f"?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
    )
    data = fetch_json(url)
    items = data.get("items", [])
    if not items:
        return {"subscribers": "N/A", "views": "N/A", "videos": "N/A"}
    stats = items[0]["statistics"]
    return {
        "subscribers": stats.get("subscriberCount", "N/A"),
        "views": stats.get("viewCount", "N/A"),
        "videos": stats.get("videoCount", "N/A"),
    }


def get_latest_video():
    search_url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&channelId={CHANNEL_ID}&maxResults=1&order=date&type=video&key={API_KEY}"
    )
    search_data = fetch_json(search_url)
    items = search_data.get("items", [])
    if not items:
        return {"date": "N/A", "title": "N/A", "duration": "N/A", "views": "N/A"}

    video_id = items[0]["id"]["videoId"]
    video_url = (
        "https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet,contentDetails,statistics&id={video_id}&key={API_KEY}"
    )
    video_data = fetch_json(video_url)
    details = video_data.get("items", [{}])[0]
    snippet = details.get("snippet", {})
    content = details.get("contentDetails", {})
    stats = details.get("statistics", {})
    return {
        "date": iso_to_date(snippet.get("publishedAt", "")),
        "title": snippet.get("title", "N/A"),
        "duration": iso_duration_to_minutes(content.get("duration", "")),
        "views": stats.get("viewCount", "N/A"),
    }


def get_latest_playlist():
    url = (
        "https://www.googleapis.com/youtube/v3/playlists"
        f"?part=snippet,contentDetails&channelId={CHANNEL_ID}&maxResults=1&key={API_KEY}"
    )
    data = fetch_json(url)
    items = data.get("items", [])
    if not items:
        return {"title": "N/A", "videoCount": "N/A"}
    item = items[0]
    return {
        "title": item.get("snippet", {}).get("title", "N/A"),
        "videoCount": item.get("contentDetails", {}).get("itemCount", "N/A"),
    }


def get_latest_community_post():
    url = (
        "https://www.googleapis.com/youtube/v3/activities"
        f"?part=snippet&channelId={CHANNEL_ID}&maxResults=10&key={API_KEY}"
    )
    data = fetch_json(url)
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        if snippet.get("type") == "community":
            text = snippet.get("text", "N/A")
            return {
                "text": text,
                "date": iso_to_date(snippet.get("publishedAt", "")),
            }
    return {"text": "N/A", "date": "N/A"}


def update_readme():
    readme = README_PATH.read_text(encoding="utf-8")

    stats = get_channel_stats()
    video = get_latest_video()
    playlist = get_latest_playlist()
    post = get_latest_community_post()

    replacements = {
        "{{ video.date }}": str(video.get("date", "N/A")),
        "{{ video.title }}": str(video.get("title", "N/A")),
        "{{ video.duration }}": str(video.get("duration", "N/A")),
        "{{ video.views }}": str(video.get("views", "N/A")),
        "{{ playlist.title }}": str(playlist.get("title", "N/A")),
        "{{ playlist.videoCount }}": str(playlist.get("videoCount", "N/A")),
        "{{ post.text }}": str(post.get("text", "N/A")),
        "{{ post.date }}": str(post.get("date", "N/A")),
    }

    for key, value in replacements.items():
        readme = readme.replace(key, value)

    README_PATH.write_text(readme, encoding="utf-8")
    print("README updated with YouTube stats.")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    update_readme()
