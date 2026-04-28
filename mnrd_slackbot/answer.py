import logging

from exactmatch import get_exact_match
from keywordmatch import get_keyword_match
from fuzzymatch import get_fuzzy_match
from tfidfmatch import get_tfidf_match

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_answer(user_msg):
    # check for exact match in faq list
    answer = get_exact_match(user_msg)
    if answer:
        return {
            "answer": answer,
            "match_type": "exact",
            "score": 1.0,
            "matched": answer
        }
    
    # check for keywordmatch in faq list
    answer, matched_keywords = get_keyword_match(user_msg)
    if answer:
        return {
            "answer": answer,
            "match_type": "keyword",
            "score": 1.0,
            "matched": matched_keywords
        }
    
    # check for fuzzy match in faq list
    answer, score, matched_question = get_fuzzy_match(user_msg, return_score=True)
    if answer:
        return {
            "answer": answer,
            "match_type": "fuzzy",
            "score": float(score),
            "matched": matched_question
        }
    
    # check for tfidf match in docs
    answer, score, matched_question = get_tfidf_match(user_msg, return_score=True)
    if answer:
        return {
            "answer": answer,
            "match_type": "tfidf",
            "score": float(score),
            "matched": matched_question
        }
    
    return {
        "answer": None,
        "match_type": "no_match",
        "score": 0.0,
        "matched": None
    }