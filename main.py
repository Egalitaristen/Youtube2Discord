import os
import requests
import feedparser
import time
import json

DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
CHECK_INTERVAL = 3600  # Check every hour

def load_channels():
    with open('channels.json', 'r') as f:
        return json.load(f)

def get_latest_video(channel_id):
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)
    return feed.entries[0] if feed.entries else None

def send_to_discord(video_url):
    data = {
        "content": video_url
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"Failed to send message. Status code: {response.status_code}")

def main():
    channels = load_channels()
    last_video_ids = {channel: [] for channel in channels}
    
    while True:
        for channel_id in channels:
            latest_video = get_latest_video(channel_id)
            if latest_video:
                video_id = latest_video.yt_videoid
                if video_id not in last_video_ids[channel_id]:
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    send_to_discord(video_url)
                    last_video_ids[channel_id].append(video_id)
                    last_video_ids[channel_id] = last_video_ids[channel_id][-5:]  # Keep last 5 video IDs
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
