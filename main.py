import os
import requests
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app_token=os.environ.get("SLACK_APP_TOKEN")
bot_token=os.environ.get("SLACK_BOT_TOKEN")
base_url=os.environ.get("BASE_URL")
endpoint=f"{base_url}/api/v1/nda_status/"

app=App(token=bot_token)

@app.command("/nda")
def handle_some_command(ack, respond, command, logger):
    ack()
    user_message=command.get("text", "").strip()
    user_id=command.get("user_id", "")
    response=requests.get(f"{endpoint}{user_id}")

    respond(f"User: *{user_message}*, user id is {user_id}, {response.json()}")

if __name__ == "__main__":
    SocketModeHandler(app, app_token).start()
