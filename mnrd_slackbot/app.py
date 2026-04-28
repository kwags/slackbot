import json
import os
import logging
import boto3
import urllib.request
import urllib.parse
import time

get_start_time = time.time()

# Worker Lambda
WORKER_FUNCTION_NAME = os.environ["WORKER_FUNCTION_NAME"]
lambda_client = boto3.client("lambda")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def handle_oauth_callback(code):
    try:
        data = urllib.parse.urlencode({
            "client_id": os.environ["SLACK_CLIENT_ID"],
            "client_secret": os.environ["SLACK_CLIENT_SECRET"],
            "code": code
        }).encode()

        req = urllib.request.urlopen(
            "https://slack.com/api/oauth.v2.access",
            data=data
        )

        response = json.loads(req.read().decode())
        logger.info(f"OAUTH RESPONSE: {response}")
        
        return {
            "statusCode": 200,
            "body": "App installed successfully!"
        }

    except Exception:
        logger.exception("OAuth failed")
        return {
            "statusCode": 500,
            "body": "OAuth failed"
        }

def lambda_handler(event, context):

    logger.info(f"event=incoming_event | user={event.get('event', {}).get('user')} | channel={event.get('event', {}).get('channel')} | event_type={event.get('event', {}).get('type')}")
   
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
    try:
        slack_event = json.loads(event.get("body", "{}"))
        
    except json.JSONDecodeError:
        logger.exception("Invalid Slack payload")
        return {"statusCode": 400, "body": "Invalid request"}
    
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
            "team_id": slack_event.get("team_id"),
            "start_time": time.time(),
        })
    )
        logger.info(f"event=message_received | user={user} | channel={channel_id} | text={user_msg}")
        
    except Exception as e:
        logger.exception("Failed to invoke worker Lambda")

    return {"statusCode": 200, "body": ""}
   
