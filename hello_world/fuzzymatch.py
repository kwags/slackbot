import os
import json
from rapidfuzz import fuzz, process

# FAQ file
FAQ_FILE = os.path.join(os.path.dirname(__file__), "data/mnrd_FAQ.json")

# load FAQ file
def load_FAQ():
    with open(FAQ_FILE, "r") as f:
        return json.load(f) 

FAQ_LIST = load_FAQ()

# list of only the FAQ Questions
FAQ_QUESTIONS = [faq["question"] for faq in FAQ_LIST]

# search faq for fuzzy match to user's message
# if match ratio is 70%+
# return corresponding answer, otherwise None
def get_fuzzy_match(user_msg: str, threshold: int = 75, return_score=False):

    # convert user message to lower case and remove white space
    user_message_lower = user_msg.lower().strip()
    
    result = process.extractOne(user_message_lower, FAQ_QUESTIONS, scorer=fuzz.token_set_ratio)

    if result is None:
        return (None, 0, None) if return_score else None
    
    best_match_question, score, index = result

    if score >= threshold:
        answer = FAQ_LIST[index]["answer"]
        if return_score:
            return answer, score, best_match_question
        return answer
    return (None, 0, None) if return_score else None

# -------------- #
#      TEST
# -------------- #

if __name__ == "__main__":
    test_questions = [
        "friends and family ticket link",
        "Where do I submit an LOA form?",
        "Leave of Absence",
        "what is the attendence policy?",
        "what is the email address for the board?",
        "Do aliens really exist?"
    ]

    for q in test_questions:
        answer = get_fuzzy_match(q)
        if answer:
            print(f"Question: {q}\nAnswer: {answer}\n")
        else:
            print(f"Question: {q}\nAnswer: No fuzzy match found.\n")