import os
import json

# FAQ file
FAQ_FILE = os.path.join(os.path.dirname(__file__), "data/mnrd_FAQ.json")

# load FAQ file
def load_FAQ():
    with open(FAQ_FILE, "r") as f:
        return json.load(f) 

FAQ_LIST = load_FAQ()

# search faq for exact match to user's message
# return corresponding answer if found, otherwise None
def get_exact_match(user_msg: str) -> str | None:

    # convert user message to lower case and remove white space
    user_message_lower = user_msg.lower().strip()

    # check if there's an exact match to question in FAQ 
    for faq_entry in FAQ_LIST:
            question = faq_entry.get("question", "").strip().lower()
            answer = faq_entry.get("answer", "")
            
            # if it's an exact match, return corresponding answer
            if user_message_lower == question:
                return answer 
            
    # if no exact match, return none
    return None

# -------------- #
#      TEST
# -------------- #

if __name__ == "__main__":
    test_questions = [
        "Where can I find the family and friends discount ticket link?",
        "How do I submit a leave of absence (LOA) or status change form?",
        "Do aliens really exist?"
    ]

    for q in test_questions:
        answer = get_exact_match(q)
        if answer:
            print(f"Question: {q}\nAnswer: {answer}\n")
        else:
            print(f"Question: {q}\nAnswer: No exact match found.\n")