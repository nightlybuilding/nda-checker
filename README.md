# nda-checker
A Slack Bot to Check if Someone is Under NDA

This bot listens for the slash command, automatically extracts the pinged user's unique Slack User ID, queries HTTPS endpoint, and returns a formatted status report.

## Features
* **Live Data**- Fetches all the data live from API
* **Slack Connection**— Connects directly to Slack via WebSockets and can be used using a slash command
* **Error Handling** — Handles `HTTP 429` by following `Retry-After`, along with error handling for diagnosing

## Slash Command
* **`nda`** — Check if a User has NDA

## Setup

1. Create a New App on [Slack API Dashboard](https://api.slack.com/apps).

2. Under `OAuth & Permissions`, provide `commands` and `chat:write` Bot Token Scopes.

3. Under `Slash Commands`, create a new command and ensure `Escape channels, users, and links sent to your app` is checked.

4. Install the app from `Install App`

5. Clone the repo

6. **Change `.env.example` to `.env` with the following keys-**
    * Bot User OAuth Token which can be obtained from `OAuth & Permissions`
    * App-Level Tokens which can be obtained from `Basic Information`
    * Base URL

7. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Run `main.py` to start the slack bot.

