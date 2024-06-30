import os
import requests
import feedparser
import json
import sys
import traceback

DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
CHANNELS_FILE = 'channels.json'

def load_channels():
    try:
        with open(CHANNELS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {CHANNELS_FILE} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: {CHANNELS_FILE} is not a valid JSON file.")
        return []

def get_latest_video(channel_id):
    try:
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        feed = feedparser.parse(feed_url)
        return feed.entries[0] if feed.entries else None
    except Exception as e:
        print(f"Error fetching feed for channel {channel_id}: {str(e)}")
        return None

def send_to_discord(video_url):
    if not DISCORD_WEBHOOK_URL:
        print("Error: DISCORD_WEBHOOK_URL environment variable is not set.")
        return

    data = {
        "content": video_url
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
        print(f"Successfully sent message: {video_url}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message. Error: {str(e)}")

def main():
    try:
        channels = load_channels()
        if not channels:
            print("No channels found or error loading channels.")
            return

        for channel_id in channels:
            latest_video = get_latest_video(channel_id)
            if latest_video:
                video_id = latest_video.yt_videoid
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                send_to_discord(video_url)
            else:
                print(f"No videos found for channel: {channel_id}")

        print("Script execution completed successfully.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
