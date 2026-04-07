from loaddocs import DOC_LIST
from normalizetext import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

corpus = [doc["processed_text"] for doc in DOC_LIST]
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
tfidf_matrix = vectorizer.fit_transform(corpus)

def get_tfidf_match(user_msg, threshold=0.2, return_score=False):   
    user_msg = normalize(user_msg)
    msg_vec = vectorizer.transform([user_msg])
    similarities = cosine_similarity(msg_vec, tfidf_matrix)[0]

    best_index = similarities.argmax()
    best_score = similarities[best_index]

    if best_score >= threshold:
        answer = DOC_LIST[best_index]
        formatted_answer = format_tfidf_answer(answer)
        matched_section = answer.get("section","")
        if return_score:
            return formatted_answer, best_score, matched_section
        return formatted_answer
    
    if return_score:
        return None, 0, None
    return None

def format_tfidf_answer(doc, max_words = 20):
    section = doc.get("section", "")
    text = doc.get("text", "")
    link = doc.get("link", "")
    
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words]) + "..."

    raw_url = link.split("|")[0].strip("<>")
    answer = (
        f"According to the {link} {section} \n{text} "
        f"<{raw_url}|read more>"
    )

    return answer

# -------------- #
#      TEST
# -------------- #
if __name__ == "__main__":
    test_questions = [
        "When does the board meet?",
        "How long are board members in office?",
        "Who is eligible for the board?",
        "Do aliens exist?"
    ]

    for q in test_questions:
        answer, score, section = get_tfidf_match(q, return_score=True)
        if answer:
            print(f"Question: {q}\nAnswer: {answer}\nScore: {score}\nSection: {section}")
        else:
            print(f"Question: {q}\nAnswer: No TF-IDF match found.")

