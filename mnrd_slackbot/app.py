import json
import os
import logging
import boto3
import urllib.request
import urllib.parse

# Worker Lambda
WORKER_FUNCTION_NAME = os.environ["WORKER_FUNCTION_NAME"]
lambda_client = boto3.client("lambda")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    logger.addHandler(handler)

def handle_oauth_callback(code):
    data = urllib.parse.urlencode({
        "client_id": os.environ["SLACK_CLIENT_ID"],
        "client_secret": os.environ["SLACK_CLIENT_SECRET"],
        "code": code
    }).encode()
    req = urllib.request.urlopen("https://slack.com/api/oauth.v2.access", data=data)
    response = json.loads(req.read().decode())
    logger.info(f"SLACK OAUTH TOKEN: {response}")
    return {"statusCode": 200, "body": "App installed successfully! You can close this window."}


def lambda_handler(event, context):

    logger.info(f"INCOMING EVENT: {json.dumps(event)}")
    
    # Handle OAuth callback
    query_params = event.get("queryStringParameters") or {}
    if "code" in query_params:
        return handle_oauth_callback(query_params["code"])

    headers = event.get("headers", {})

    # ignore Slack retries
    if headers.get("X-Slack-Retry-Num"):
        logger.info("Ignoring Slack retry")
        return {"statusCode": 200, "body": ""}

    # Parse the incoming event data from Slack
    slack_event = json.loads(event.get("body", "{}"))

    # Check for URL verification during the event subscription process
    if slack_event.get("type") == "url_verification":
        # Respond with the challenge token to verify the endpoint
        return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "challenge": slack_event.get("challenge")
        })
    }

    # Extract event data
    data = slack_event.get("event", {})

    # Ignore messages from bots
    if data.get("bot_id"):
        return {"statusCode": 200, "body": ""}
    
    channel_id = data.get("channel")
    user = data.get("user")
    thread_ts = data.get("thread_ts", data.get("ts"))
    user_msg = data.get("text", "")
    
    # Inovke worker Lambda
    try:
        lambda_client.invoke(
        FunctionName=WORKER_FUNCTION_NAME,
        InvocationType="Event",
        Payload=json.dumps({
            "user_id": user,
            "channel_id": channel_id,
            "text": user_msg,
            "thread_ts": thread_ts,
            "event_type": data.get("type"),
            "channel_type": data.get("channel_type"), 
            "team_id": slack_event.get("team_id")
        })
    )
        logger.info(f"Queued message for worker: {user_msg}")
    except Exception as e:
        logger.error(f"Failed to invoke worker Lambda: {str(e)}")

    return {"statusCode": 200, "body": ""}
   
