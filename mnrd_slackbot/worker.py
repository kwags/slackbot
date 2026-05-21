import os
import logging
import time

from slack_sdk import WebClient
from answer import get_answer

logger = logging.getLogger("worker")
logger.setLevel(logging.INFO)



def get_token(team_id):
    if team_id == os.environ["MNRD_TEAM_ID"]:
        token = os.environ["SLACK_BOT_TOKEN_MNRD"]
    elif team_id == os.environ["MNRD_TEST_TEAM_ID"]:
        token = os.environ["SLACK_BOT_TOKEN_TEST"]
    elif team_id == os.environ["MNRD_LIVE_TEAM_ID"]:
        token = os.environ["SLACK_BOT_TOKEN_LIVE"]
    else:
        raise Exception(f"Unknown team_id: {team_id}")
    
    return token

def lambda_handler(event, context):
    logger.info(f"FULL EVENT: {event}")
    client = WebClient(token=get_token(event["team_id"]))

    worker_start = time.time()
    start_time = event.get("start_time", worker_start)

    try:
        user = event.get("user_id")
        channel_id = event.get("channel_id")
        user_msg = event.get("text", "")
        thread_ts = event.get("thread_ts")
        event_type = event.get("event_type")
        channel_type = event.get("channel_type")

        if not user_msg:
            return {"statusCode": 200, "body": ""}

        if event_type == "app_mention":
            user_msg = user_msg.split(">", 1)[-1].strip()
            result = get_answer(user_msg)
            answer = result.get("answer") if result else None
            match_type = result.get("match_type") if result else "no_match"
            score = result.get("score") if result else 0
                        
            if not answer:
                response_text = f"Sorry <@{user}>, I couldn't find a match for your question. If you'd like to suggest a new FAQ or share feedback, please use this form: <https://forms.gle/pw7GhduacR7n4UJeA|Chatbot Suggestion Form>"
            else:
                response_text = f"Hi <@{user}>! {answer}"

            client.chat_postMessage(
                channel=channel_id,
                text=response_text,
                thread_ts=thread_ts,
                unfurl_links=False,
                unfurl_media=False
            )

        elif event_type == "message":

            if channel_type != "im":
                logger.info("Ignored non-DM message")
                return {"statusCode": 200, "body": ""}

            result = get_answer(user_msg)
            answer = result.get("answer") if result else None
            match_type = result.get("match_type") if result else "no_match"
            score = result.get("score") if result else 0

            if not answer:
                response_text = f"Sorry <@{user}>, I couldn't find a match for your question. If you'd like to suggest a new FAQ or share feedback, please use this form: <https://forms.gle/pw7GhduacR7n4UJeA|Chatbot Suggestion Form>"
            else:
                response_text = f"Hi <@{user}>! {answer}"
            client.chat_postMessage(
                channel=channel_id,
                text=response_text,
                unfurl_links=False,
                unfurl_media=False
            )

        else:
            logger.info(f"Ignored event type: {event_type}")
            return {"statusCode": 200, "body": ""}

        logger.info({
            "event": "response_sent",
            "user": user,
            "question": user_msg,
            "match_type": match_type,
            "score": float(score),
            "total_response_time_ms": (time.time() - start_time) * 1000,
            "response": response_text
        })
        
        return {"statusCode": 200, "body": ""}

    except Exception as e:
        logger.exception("Worker failed")

        try:
            client.chat_postMessage(
                channel=channel_id,
                text="⚠️ The chatbot is currently unavailable. Please try again later."
            )
        except Exception:
            logger.exception("Failed fallback message")

        return {"statusCode": 500, "body": "error"}

# ------------------------------------ #
#                TEST
# #client = WebClient... to run test #
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
        "Who is eligible for the board of directors?", # tfidf 
        "Who is eligible for the bod", # tfidf 
        "what is the definition of Active Status?", # tfidf leave doc
        "What is the definition of Inactive status?",  # tfidf
        "how do i provide feedback for the chatbot?",   
        "What happens if someone doesn't follow the code of conduct?",
        "Can I resign from dmc?",
        "Do aliens really exist?" # no match
    ]

    for q in test_questions:
        answer = get_answer(q)
        print(f"Q: {q}")
        if not answer:
            response_text = f"A: Sorry, I couldn't find a match for your question. If you'd like to suggest a new FAQ or share feedback, please use this form: <https://forms.gle/pw7GhduacR7n4UJeA|Chatbot Suggestion Form>"
        else:
            response_text = f"A: {answer}"
        print(response_text)
        print()