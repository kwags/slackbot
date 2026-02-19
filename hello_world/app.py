import json
import os
from slack_sdk import WebClient

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

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
    
    event_type = data.get("type")
    channel_id = data.get("channel")
    user = data.get("user")

    # Respond to mentions
    if event_type == "app_mention":
        client.chat_postMessage(
            channel=channel_id,
            text=f"👋 Hello <@{user}>! I'm the MNRD Slack Chatbot responding to your mention!"
        )

    # Respond to messages
    elif event_type == "message":
        if data.get("channel_type") != "im":
            return {"statusCode": 200, "body": ""}
        client.chat_postMessage(
            channel=channel_id,
            text=f"👋 Hello <@{user}>! I'm the MNRD Slack Chatbot responding to your message!"
        )
    return {"statusCode": 200, "body": ""}

