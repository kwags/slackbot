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
        logger.info(
            "match_type = exact | score = %.2f | user_question = %s | matched_question = %s",
            100.00,
            user_msg,
            user_msg
        )
        return answer
    
    # check for keywordmatch in faq list
    answer, matched_keywords = get_keyword_match(user_msg)
    if answer:
        logger.info(
            "match_type = keyword | score = %.2f | user_question = %s | matched_keywords = %s",
            100.00,
            user_msg,
            matched_keywords
        )       
        return answer
    
    # check for fuzzy match in faq list
    answer, score, matched_question = get_fuzzy_match(user_msg, return_score=True)
    if answer:
        logger.info(
            "match_type = fuzzy | score = %.2f | user_question = %s | matched_question = %s",
            score,
            user_msg,
            matched_question
        )
        return answer
    
    # check for tfidf match in docs
    answer, score, matched_question = get_tfidf_match(user_msg, return_score=True)
    if answer:
        logger.info(
            "match_type = tfidf | score = %.2f | user_question = %s | matched_section = %s",
            score,
            user_msg,
            matched_question
        )
        return answer
    
    logger.info(
        "match_type = no match | score = %.2f | user_question = %s | matched_question = %s ",
        0.00,
        user_msg,
        "None"
    )
    return None 