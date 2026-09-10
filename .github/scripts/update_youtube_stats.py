#!/usr/bin/env python3
import json
import html
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID", "UC3WIwB7nbYMEvWW4CGQGYsA")


def fetch_json(url: str):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"YouTube API request failed: {exc}") from exc
    if "error" in data:
        raise RuntimeError(f"YouTube API returned an error: {data['error']}")
    return data


def api_url(resource: str, **params: str) -> str:
    params["key"] = API_KEY or ""
    return f"https://www.googleapis.com/youtube/v3/{resource}?{urlencode(params)}"


def markdown_text(value: str) -> str:
    return html.escape(
        str(value).replace("\r", " ").replace("\n", " ").replace("|", r"\|")
    )


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
    data = fetch_json(api_url("channels", part="statistics", id=CHANNEL_ID))
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
    search_data = fetch_json(
        api_url(
            "search",
            part="snippet",
            channelId=CHANNEL_ID,
            maxResults="1",
            order="date",
            type="video",
        )
    )
    items = search_data.get("items", [])
    if not items:
        return {"date": "N/A", "title": "N/A", "duration": "N/A", "views": "N/A"}

    video_id = items[0]["id"]["videoId"]
    video_data = fetch_json(
        api_url(
            "videos",
            part="snippet,contentDetails,statistics",
            id=video_id,
        )
    )
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
    data = fetch_json(
        api_url(
            "playlists",
            part="snippet,contentDetails",
            channelId=CHANNEL_ID,
            maxResults="1",
        )
    )
    items = data.get("items", [])
    if not items:
        return {"title": "N/A", "videoCount": "N/A"}
    item = items[0]
    return {
        "title": item.get("snippet", {}).get("title", "N/A"),
        "videoCount": item.get("contentDetails", {}).get("itemCount", "N/A"),
    }


def get_latest_community_post():
    data = fetch_json(
        api_url(
            "activities",
            part="snippet",
            channelId=CHANNEL_ID,
            maxResults="10",
        )
    )
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

    stats_block = f"""<!-- YOUTUBE_STATS:START -->
## 📊 YouTube Channel Stats
<p align="center">
  <img src="https://img.shields.io/youtube/channel/subscribers/{CHANNEL_ID}?style=for-the-badge&label=Subscribers&logo=youtube&color=red" alt="Subscribers">
  <img src="https://img.shields.io/youtube/channel/views/{CHANNEL_ID}?style=for-the-badge&label=Total%20Views&logo=youtube&color=red" alt="Total views">
  <img src="https://img.shields.io/youtube/channel/video-count/{CHANNEL_ID}?style=for-the-badge&label=Videos&logo=youtube&color=red" alt="Videos">
</p>

**Subscribers:** {markdown_text(stats["subscribers"])} · **Views:** {markdown_text(stats["views"])} · **Videos:** {markdown_text(stats["videos"])}

---

## 🎬 Latest YouTube Video
| Date | Title | Duration | Views |
|------|-------|----------|-------|
| {markdown_text(video["date"])} | {markdown_text(video["title"])} | {markdown_text(video["duration"])} | {markdown_text(video["views"])} |

---

## 📚 Latest Playlist
- {markdown_text(playlist["title"])} — {markdown_text(playlist["videoCount"])} videos

---

## 📝 Latest Community Post
> "{markdown_text(post["text"])}"
*(Posted {markdown_text(post["date"])})*
<!-- YOUTUBE_STATS:END -->"""

    pattern = r"<!-- YOUTUBE_STATS:START -->.*?<!-- YOUTUBE_STATS:END -->"
    updated_readme, replacements = re.subn(
        pattern, stats_block, readme, count=1, flags=re.DOTALL
    )
    if replacements != 1:
        raise RuntimeError("README YouTube stats markers were not found exactly once")

    README_PATH.write_text(updated_readme, encoding="utf-8")
    print("README updated with YouTube stats.")
    print(json.dumps(stats, indent=2))


def main() -> int:
    if not API_KEY:
        print("YOUTUBE_API_KEY is not set.", file=sys.stderr)
        return 1

    try:
        update_readme()
    except (OSError, RuntimeError, KeyError, IndexError) as exc:
        print(f"Failed to update YouTube stats: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
