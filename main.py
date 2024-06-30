import os
import requests
import feedparser
import json
from datetime import datetime, timezone
import time
import random

DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
POSTED_VIDEOS_FILE = 'posted_videos.json'
LOG_FILE = 'bot_log.txt'

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp}: {message}\n")
    print(message)

def load_channels():
    try:
        with open('channels.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        log_message(f"Error loading channels: {str(e)}")
        return []

def load_posted_videos():
    if os.path.exists(POSTED_VIDEOS_FILE):
        try:
            with open(POSTED_VIDEOS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            log_message(f"Error loading posted videos: {str(e)}")
    return {}

def save_posted_videos(posted_videos):
    try:
        with open(POSTED_VIDEOS_FILE, 'w') as f:
            json.dump(posted_videos, f)
    except Exception as e:
        log_message(f"Error saving posted videos: {str(e)}")

def get_latest_video(channel_id):
    try:
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        feed = feedparser.parse(feed_url)
        time.sleep(random.uniform(1, 3))  # Random delay between requests
        return feed.entries[0] if feed.entries else None
    except Exception as e:
        log_message(f"Error fetching feed for channel {channel_id}: {str(e)}")
        return None

def send_to_discord(video_url):
    try:
        data = {"content": video_url}
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
        log_message(f"Successfully sent message: {video_url}")
    except Exception as e:
        log_message(f"Failed to send message: {video_url}. Error: {str(e)}")

def main():
    log_message("Script started.")
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
        else:
            log_message(f"No video found for channel: {channel_id}")
    
    save_posted_videos(posted_videos)
    log_message("Script execution completed successfully.")

if __name__ == "__main__":
    main()
