# Youtube2Discord


# YouTube to Discord Bot

This bot automatically checks specified YouTube channels for new videos and posts the video URLs to a Discord channel using a webhook.

## Features

- Monitors multiple YouTube channels for new uploads
- Sends new video URLs to a Discord channel via webhook
- Runs automatically every hour using GitHub Actions
- Avoids duplicate postings by tracking recent video IDs
- Easy to set up and customize

## Setup

1. Fork this repository to your GitHub account.

2. Clone your forked repository to your local machine:
   ```
   git clone https://github.com/your-username/youtube-discord-bot.git
   cd youtube-discord-bot
   ```

3. Edit the `channels.json` file to include the YouTube channel IDs you want to monitor. Each ID should be in quotes and separated by commas:
   ```json
   [
     "UC-lHJZR3Gqxm24_Vd_AJ5Yw",
     "UCq-Fj5jknLsUf-MWSy4_brA",
     "UCX6OQ3DkcsbYNE6H8uQQuVA"
   ]
   ```

4. Create a Discord webhook:
   - In your Discord server, go to Server Settings > Integrations > Webhooks
   - Click "New Webhook", customize it if desired, and copy the webhook URL

5. Add the Discord webhook URL as a secret in your GitHub repository:
   - Go to your repository on GitHub
   - Click on Settings > Secrets > Actions
   - Click "New repository secret"
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: Your Discord webhook URL
   - Click "Add secret"

6. Commit and push your changes:
   ```
   git add channels.json
   git commit -m "Update monitored YouTube channels"
   git push
   ```

7. The GitHub Action should now be set up and will run automatically every hour. You can also manually trigger it from the Actions tab in your GitHub repository.

## How It Works

- The bot checks the specified YouTube channels every hour for new videos.
- When a new video is found, it posts only the video URL to the Discord channel using the webhook.
- The bot keeps track of the last 5 video IDs for each channel to avoid reposting the same videos.

## Customization

- To change how often the bot checks for new videos, edit the cron schedule in `.github/workflows/youtube_check.yml`.
- To modify the check interval within the script, edit the `CHECK_INTERVAL` variable in `main.py`.

## Troubleshooting

If you encounter any issues:
1. Check the Actions tab in your GitHub repository for any error messages.
2. Ensure your `DISCORD_WEBHOOK_URL` secret is set correctly.
3. Verify that the YouTube channel IDs in `channels.json` are correct.
4. Make sure the webhook has the necessary permissions in your Discord server.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
