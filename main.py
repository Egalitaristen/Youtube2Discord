import os
import requests
import feedparser
import json
from datetime import datetime, timezone

DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
POSTED_VIDEOS_FILE = 'posted_videos.json'

def load_channels():
    with open('channels.json', 'r') as f:
        return json.load(f)

def load_posted_videos():
    if os.path.exists(POSTED_VIDEOS_FILE):
        with open(POSTED_VIDEOS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_posted_videos(posted_videos):
    with open(POSTED_VIDEOS_FILE, 'w') as f:
        json.dump(posted_videos, f)

def get_latest_video(channel_id):
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)
    return feed.entries[0] if feed.entries else None

def send_to_discord(video_url):
    data = {"content": video_url}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def main():
    channels = load_channels()
    posted_videos = load_posted_videos()
    
    for channel_id in channels:
        latest_video = get_latest_video(channel_id)
        if latest_video:
            video_id = latest_video.yt_videoid
            video_date = datetime.strptime(latest_video.published, "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=timezone.utc)
            current_time = datetime.now(timezone.utc)
            
            is_new_video = (current_time - video_date).days < 1
            is_new_channel = channel_id not in posted_videos
            is_new_post = video_id not in posted_videos.get(channel_id, [])
            
            if (is_new_channel and is_new_video) or (is_new_post and is_new_video):
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                send_to_discord(video_url)
                posted_videos.setdefault(channel_id, []).append(video_id)
                posted_videos[channel_id] = posted_videos[channel_id][-5:]  # Keep last 5 video IDs
    
    save_posted_videos(posted_videos)

if __name__ == "__main__":
    main()
