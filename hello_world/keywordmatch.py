import os
import json

# FAQ file
FAQ_FILE = os.path.join(os.path.dirname(__file__), "data/mnrd_FAQ.json")

# load FAQ file
def load_FAQ():
    with open(FAQ_FILE, "r") as f:
        return json.load(f) 

FAQ_LIST = load_FAQ()

# search faq for keyword match
# return corresponding answer if found, otherwise None
def get_keyword_match(user_msg: str) -> str | None:

    # convert user message to lower case and remove white space
    user_message_lower = user_msg.lower().strip()

    # check if there's an exact match to question in FAQ 
    for faq_entry in FAQ_LIST:
            keywords = faq_entry.get("keywords", "")
            answer = faq_entry.get("answer", "")

            if not keywords:
                continue
            
            keyword_list = [k.strip().lower() for k in keywords.split(",")]

            # if a keyword match is found, return corresponding answer
            for keyword in keyword_list:
                if keyword in user_message_lower:
                    return answer
            
    # if no keyword match, return none
    return None

# -------------- #
#      TEST
# -------------- #

if __name__ == "__main__":
    test_questions = [
        "What is the ticket discount link?",
        "Where is the leave of absence form?",
        "How do I file a complaint about someone?",
        "Who are captains?",
        "Where is the LOA form?",
        "Do aliens really exist?"
    ]

    for q in test_questions:
        answer = get_keyword_match(q)
        if answer:
            print(f"Question: {q}\nAnswer: {answer}\n")
        else:
            print(f"Question: {q}\nAnswer: No keyword match found.\n")