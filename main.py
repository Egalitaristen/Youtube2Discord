import os
import requests
import feedparser
import json
import sys

DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
CHANNELS_FILE = 'channels.json'

def load_channels():
    with open(CHANNELS_FILE, 'r') as f:
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
    else:
        print(f"Successfully sent message: {video_url}")

def main():
    channels = load_channels()
    
    for channel_id in channels:
        latest_video = get_latest_video(channel_id)
        if latest_video:
            video_id = latest_video.yt_videoid
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            send_to_discord(video_url)
        else:
            print(f"No videos found for channel: {channel_id}")

    print("Script execution completed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
