import os
import json
from spellchecker import SpellChecker
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
all_keywords = []
keyword_map = []
spell = SpellChecker()

for i, faq in enumerate(FAQ_LIST):
    kws = faq.get("keywords", "")
    if not kws:
        continue
    kw_list = [k.strip().lower() for k in kws.split(",")]
    all_keywords.extend(kw_list)
    keyword_map.extend([i]*len(kw_list))  # map each keyword to its FAQ index

# search faq for fuzzy match to user's message
# if match ratio is 70%+
# return corresponding answer, otherwise None
def get_fuzzy_match(user_msg: str, threshold: int = 75, return_score=False):

    # check spelling and convert user message to lower case and remove white space
    user_msg_corrected = " ".join([spell.correction(w) for w in user_msg.split()])
    user_message_lower = user_msg_corrected.lower().strip()
    
    result = process.extractOne(user_message_lower, FAQ_QUESTIONS, scorer=fuzz.token_set_ratio)
    if result:
        best_question, score, index = result
        if score >= threshold:
            answer = FAQ_LIST[index]["answer"]
            if return_score:
                return answer, score, best_question
            return answer
        
    # fuzzy match against keywords
    result = process.extractOne(user_message_lower, all_keywords, scorer=fuzz.WRatio)
    if result:
        best_keyword, score, _ = result
        if score >= threshold:
            faq_index = keyword_map[all_keywords.index(best_keyword)]
            answer = FAQ_LIST[faq_index]["answer"]
            if return_score:
                return answer, score, best_keyword
            return answer

    # 3No match found
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
        "what is the attendence requirement?", # spellcheck
        "what is the email address for the board?",
        "where is the greivance form?", # spellcheck
        "Do aliens really exist?"
    ]

    for q in test_questions:
        answer = get_fuzzy_match(q)
        if answer:
            print(f"Question: {q}\nAnswer: {answer}\n")
        else:
            print(f"Question: {q}\nAnswer: No fuzzy match found.\n")