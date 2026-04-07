from loadfaq import FAQ_LIST, normalize

# search faq for exact match to user's message
# return corresponding answer if found, otherwise None
def get_exact_match(user_msg):

    # normalize user message
    user_message_norm = normalize(user_msg)

    # check if there's an exact match to question in FAQ 
    for faq_entry in FAQ_LIST:
            question = normalize(faq_entry.get("question", ""))
            answer = faq_entry.get("answer", "")
            
            # if it's an exact match, return corresponding answer
            if user_message_norm == question:
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