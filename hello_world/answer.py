from exactmatch import get_exact_match
from keywordmatch import get_keyword_match
from fuzzymatch import get_fuzzy_match

def get_answer(user_msg):
    # check for exact match in faq list
    answer = get_exact_match(user_msg)
    # check for keywordmatch in faq list
    if not answer:
        answer = get_keyword_match(user_msg)
    # check for fuzzy match in faq list
    if not answer:
        answer = get_fuzzy_match(user_msg)
        
    return answer
