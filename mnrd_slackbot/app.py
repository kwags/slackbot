import json
import os
import logging
import boto3

# Worker Lambda
WORKER_FUNCTION_NAME = os.environ["WORKER_FUNCTION_NAME"]
lambda_client = boto3.client("lambda")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    logger.addHandler(handler)

def lambda_handler(event, context):

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
        return {"statusCode": 200, 
                "body": slack_event.get("challenge")
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
            "channel_type": data.get("channel_type") 
        })
    )
        logger.info(f"Queued message for worker: {user_msg}")
    except Exception as e:
        logger.error(f"Failed to invoke worker Lambda: {str(e)}")

    return {"statusCode": 200, "body": ""}
   
