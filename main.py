import os
import requests
import re
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
    match=re.search(r"<@([A-Z0-9]+)", user_message)

    if match:
        user_id=match.group(1)
    else:
        respond("Please provide a valid user mention.")
        return
    
    response=requests.get(f"{endpoint}{user_id}", timeout=5)
    
    if response.status_code==429:
        respond(f"Too many requests: {response.json()}")
    elif response.status_code==200:
        data=response.json()
        status=data.get("status", "")
        version=data.get("nda_version", "")
        signed_at=data.get("signed_at", "")
        signature_type=data.get("signature_type", "")
        slack_id=data.get("slack_id", "")

        if status=="not_signed":
            respond(f"User: *{user_message}*\nSlack ID: *{slack_id}*\nNDA status: *{status}*\nNDA version: *{version}*\n")
        else:
            respond(f"User: *{user_message}*\nSlack ID: *{slack_id}*\nNDA status: *{status}*\nNDA version: *{version}*\nSigned at: *{signed_at}*\nSignature type: *{signature_type}*\n")

    elif response.status_code==400:
        respond(f"Bad request: {response.json()}")
    else:
        respond(f"Unexpected error: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    SocketModeHandler(app, app_token).start()
