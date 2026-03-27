import os
import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from answer import get_answer

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    user = event.get("user_id")
    channel_id = event.get("channel_id")
    user_msg = event.get("text", "")
    thread_ts = event.get("thread_ts")
    event_type = event.get("event_type")
    channel_type = event.get("channel_type")


    # Respond to mentions
    if event_type == "app_mention":
        # remove mention
        user_msg = user_msg.split(">", 1)[-1].strip()

        # get answer
        answer = get_answer(user_msg)
        
        if not answer:
            response_text = f"Sorry <@{user}>, I didn't find a match for your question."
        else:
            response_text = f"Hi <@{user}>! {answer}"

        client.chat_postMessage(
            channel=channel_id,
            text=response_text,
            thread_ts=thread_ts,
            unfurl_links=False,
            unfurl_media=False
        )

    # Respond to messages
    elif event_type == "message":
        if channel_type != "im":
            return

        answer = get_answer(user_msg)

        if not answer:
            response_text = f"Sorry <@{user}>, I didn't find a match for your question."
        else:
            response_text = f"Hi <@{user}>! {answer}"

        client.chat_postMessage(
            channel=channel_id,
            text=response_text,
            unfurl_links=False,
            unfurl_media=False
        )

    else:
        logger.info("Ignored event type")

    return {"statusCode": 200, "body": ""}

# ------------------------------------ #
#                TEST
# #client = WebClient... to run test
# ------------------------------------ #

if __name__ == "__main__":
    test_questions = [
        "Where can I find the friends and family discount ticket link?", # exact match
        "How do I submit a leave of absence (LOA) or status change form?", # exact match
        "Where is the LOA form?", # keyword match
        "What is the attendence policy?", # fuzzy match
        "Where do I submit an LOA form?", # keyword
        "what is the email address for the board?", #fuzzy match
        "what is the attendence requirment?", # spellcheck keyword fuzzy
        "what is the email for the bod?",
        "Who is on the board?",
        "where is the greivance form?",
        "When does the board meet?", # tfidf
        "How long are board members in office?", # tfidf
        "Who is eligible for the board?", # tfidf
        "Do aliens really exist?" # no match
    ]

    for q in test_questions:
        answer = get_answer(q)