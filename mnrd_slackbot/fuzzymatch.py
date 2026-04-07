import os
import json
import re
from rapidfuzz import fuzz, process

# FAQ file
FAQ_FILE = os.path.join(os.path.dirname(__file__), "data/mnrd_FAQ.json")

# load FAQ file
def load_FAQ():
    with open(FAQ_FILE, "r") as f:
        return json.load(f) 

FAQ_LIST = load_FAQ()

# normalize text
def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    text = " ".join(text.split())        # remove extra spaces
    return text

# list of FAQ questions and keywords
FAQ_QUESTIONS = [faq["question"] for faq in FAQ_LIST]
KEYWORDS = []
KEYWORD_MAP = []

# map each keyword to its FAQ index
for i, faq in enumerate(FAQ_LIST):
    kws = faq.get("keywords", "")
    if not kws:
        continue
    kw_list = [k.strip().lower() for k in kws.split(",")]
    KEYWORDS.extend(kw_list)
    KEYWORD_MAP.extend([i]*len(kw_list))  

# search faq for fuzzy match to user's message in questions
# if match ratio is 85%+ return corresponding answer
# otherwise search for fuzzy match to keywords
# otherwise return None
def get_fuzzy_match(user_msg: str, threshold: int = 92, return_score=False):

    user_msg_norm = normalize(user_msg)
    
    # fuzzy match against questions using token set ratio
    result = process.extractOne(user_msg_norm, FAQ_QUESTIONS, scorer=fuzz.token_set_ratio)
    if result:
        best_question, score, index = result
        if score >= threshold:
            answer = FAQ_LIST[index]["answer"]
            if return_score:
                return answer, score, best_question
            return answer
        
    # fuzzy match against keywords using partial ratio
    result = process.extractOne(user_msg_norm, KEYWORDS, scorer=fuzz.partial_ratio)
    if result:
        best_keyword, score, index = result
        if score >= threshold:
            faq_index = KEYWORD_MAP[KEYWORDS.index(best_keyword)]
            answer = FAQ_LIST[faq_index]["answer"]
            if return_score:
                return answer, score, best_keyword
            return answer

    # fuzzy match against keywords using token set ratio
    result = process.extractOne(user_msg_norm, KEYWORDS, scorer=fuzz.token_set_ratio)
    if result:
        best_keyword, score, index = result
        if score >= threshold:
            faq_index = KEYWORD_MAP[KEYWORDS.index(best_keyword)]
            answer = FAQ_LIST[faq_index]["answer"]
            if return_score:
                return answer, score, best_keyword
            return answer
        
    # No match found
    if return_score:
        return None, 0, None
    return None

# -------------- #
#      TEST
# -------------- #

if __name__ == "__main__":
    test_questions = [
        "friends and family ticket link",
        "Where do I submit an LOA form?",
        "Leave of Absence",
        "What is the attendence requirment?",
        "what is the email address for the board?",
        "where is the greivance form?",
        "what is the email for the bod?",
        "Do aliens really exist?"
    ]

    for q in test_questions:
        answer = get_fuzzy_match(q)
        if answer:
            print(f"Question: {q}\nAnswer: {answer}\n")
        else:
            print(f"Question: {q}\nAnswer: No fuzzy match found.\n")