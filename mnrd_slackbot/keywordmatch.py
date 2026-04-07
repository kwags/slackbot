from loadfaq import FAQ_LIST
from normalizetext import normalize

# search faq for keyword match
# return corresponding answer if found, otherwise None
def get_keyword_match(user_msg):

    # normalize user message
    user_message_norm = normalize(user_msg)

    # check if there's an exact match to question in FAQ 
    for faq_entry in FAQ_LIST:
            keywords = faq_entry.get("keywords", "")
            answer = faq_entry.get("answer", "")

            if not keywords:
                continue
            
            keyword_list = [normalize(k) for k in keywords.split(",")]

            # if a keyword match is found, return corresponding answer
            for keyword in keyword_list:
                if keyword in user_message_norm:
                    return answer, keyword
            
    # if no keyword match, return none
    return None, None

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