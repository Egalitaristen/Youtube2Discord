# YouTube to Discord Bot

This bot automatically checks specified YouTube channels for new videos and posts the video URLs to a Discord channel using a webhook.

## Features

- Monitors multiple YouTube channels for new uploads
- Sends new video URLs to a Discord channel via webhook
- Runs automatically every hour using GitHub Actions
- Avoids duplicate postings by tracking recent video IDs

## Important: GitHub Actions Permissions

**The script will fail without proper permissions set for GitHub Actions.**

To set the correct permissions:

1. Go to your GitHub repository's settings.
2. Click on "Actions" in the left sidebar.
3. Scroll down to the "Workflow permissions" section.
4. Select "Read and write permissions".
5. Save the changes.

These permissions are necessary for the GitHub Action to update the `posted_videos.json` file in your repository.

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

7. Set the correct GitHub Actions permissions as described in the "Important" section above.

8. The GitHub Action should now be set up and will run automatically every hour. You can also manually trigger it from the Actions tab in your GitHub repository.

## How It Works

- The bot checks the specified YouTube channels every hour for new videos.
- When a new video (less than 24 hours old) is found, it posts the video URL to the Discord channel using the webhook.
- The bot keeps track of posted videos to avoid reposting the same videos.

## Troubleshooting

If you encounter any issues:

1. Check the GitHub Actions logs for any error messages.
2. Ensure your `DISCORD_WEBHOOK_URL` secret is set correctly.
3. Verify that the YouTube channel IDs in `channels.json` are correct.
4. Double-check that you've set the correct permissions for GitHub Actions as described in the "Important" section.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
