import json
import os
from slack_sdk import WebClient
from answer import get_answer

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
    thread_ts = data.get("thread_ts", data.get("ts"))

    # Respond to mentions
    if event_type == "app_mention":
        user_msg = data.get("text", "")
        # remove mention from msg
        user_msg = user_msg.split(">", 1)[-1].strip()

        # get answer
        answer = get_answer(user_msg)
        
        if not answer:
            response_text = f"Sorry <@{user}>, I didn't find a match for your question."
        else:
            response_text = answer

        client.chat_postMessage(
            channel=channel_id,
            text=response_text,
            thread_ts=thread_ts
        )

    # Respond to messages
    elif event_type == "message":
        if data.get("channel_type") != "im":
            return {"statusCode": 200, "body": ""}
        user_msg = data.get("text", "")
        
        # get answer
        answer = get_answer(user_msg)
        
        if not answer:
            response_text = f"Sorry <@{user}>, I didn't find a match for your question."
        else:
            response_text = answer

        client.chat_postMessage(
            channel=channel_id,
            text=response_text
        )
    return {"statusCode": 200, "body": ""}

# ------------------------------------ #
#                TEST
# #client = WebClient... to run test
# ------------------------------------ #

if __name__ == "__main__":
    test_questions = [
        "Where can I find the family and friends discount ticket link?", # exact match
        "How do I submit a leave of absence (LOA) or status change form?", # exact match
        "Where is the LOA form?", # keyword match
        "friends and family ticket link", # fuzzy match
        "Where do I submit an LOA form?", # fuzzy match
        "Do aliens really exist?" # no match
    ]

    for q in test_questions:
        answer = get_answer(q)
        if answer:
            print(f"Question: {q}\nAnswer: {answer}\n")
        if not answer:
            print(f"question: {q}\nAnswer: No match found.\n")