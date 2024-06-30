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

def send_to_discord(video):
    data = {
        "content": f"New video: {video.title}\n{video.link}"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def main():
    channels = load_channels()
    last_video_ids = {channel: None for channel in channels}
    
    while True:
        for channel_id in channels:
            latest_video = get_latest_video(channel_id)
            if latest_video and latest_video.id != last_video_ids[channel_id]:
                send_to_discord(latest_video)
                last_video_ids[channel_id] = latest_video.id
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
