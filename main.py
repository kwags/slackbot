from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
# Will implement with AWS
# from slack_bolt.adapter.aws_lambda import SlackRequestHandler

import os

load_dotenv()

bot_token = os.environ.get("SLACK_BOT_TOKEN")
app_token = os.environ.get("SLACK_APP_TOKEN")

if not bot_token or not app_token:
    raise ValueError(
        "Missing required environment variables: SLACK_BOT_TOKEN and/or SLACK_APP_TOKEN"
    )

app = App(token=bot_token)

@app.event("mention")
def handle_mention(body, say):
    event = body.get("event", {})
    thread_ts = event.get("thread_ts", event["ts"])
    user = event.get("user")
    text = event.get("text")
    
    say(text=f"Hello <@{user}>! Processing your Question:  {text}", thread_ts=thread_ts)

@app.event("message")
def handle_messages(body, say):
    event = body.get("event", {})
    user = event.get("user")
    text = event.get("text")
    if not event.get("channel_type") == "im":
        return
    say(f"Hello <@{user}>! Processing question: {text}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()