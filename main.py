import os
import requests
import re
import logging
import time
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

    response=None

    logger.info(f"/nda called by {command['user_name']}({command['user_id']}) with text: {command['text']}")

    if match:
        user_id=match.group(1)
    else:
        respond("Please provide a valid user mention.")
        return

    max_attempts=3
    for attempt in range(max_attempts):
        try:
            response=requests.get(f"{endpoint}{user_id}", timeout=5)
            if response.status_code==429:
                logger.warning(f"Rate limited (429). Attempt {attempt + 1}/{max_attempts}.")
                retry_after=int(response.headers.get("Retry-After", 1))
                respond(f"Too many requests: {response.json()}, retrying in {retry_after} seconds...")
                time.sleep(retry_after)
                continue
            else:
                break
        except requests.exceptions.RequestException as e:
            logger.exception(f"Request failed on attempt {attempt + 1}: {e}.")
            
            if attempt < max_attempts - 1:
                time.sleep(1)
                continue
            else:
                respond(f"Request failed: {e}, try again later.")
                return

    if response:
        if response.status_code==200:
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
