from loaddocs import DOC_LIST
from normalizetext import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

corpus = [doc["processed_text"] for doc in DOC_LIST]
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), min_df=2, max_df=0.85, sublinear_tf=True)

tfidf_matrix = vectorizer.fit_transform(corpus)


def get_tfidf_match(user_msg, threshold=0.16, return_score=False):   
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
    article = doc.get("article", "")
    section = doc.get("section", "")
    subsection = doc.get("subsection", "")
    text = doc.get("text", "")
    link = doc.get("link", "")
    
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words]) + "..."

    raw_url = link.split("|")[0].strip("<>")
    header_parts = []

    if article:
        header_parts.append(article)
    if section:
        header_parts.append(section)
    if subsection:
        header_parts.append(subsection)

    header = " | ".join(header_parts)

    answer = (
        f"According to the {link} {header}\n"
        f"{text}\n"
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
        "Who is eligible for the bod?",
        "Who is eligible for the board?",
        "Who is eligible for the board of directors",
        "what is the definition of Active Status?",
        "what does Active Status mean?", # embeddings
        "Who is considered active in the league?",
        "What if I don't meet requirements anymore?",
        "Do I lose my membership if I'm inactive?",
        "what is the definition of inactive status?",
        "Do aliens exist?"
    ]

    for q in test_questions:
        answer, score, section = get_tfidf_match(q, return_score=True)
        if answer:
            print(f"Question: {q}\nAnswer: {answer}\nScore: {score}\nSection: {section}")
            print()
        else:
            print(f"Question: {q}\nAnswer: No TF-IDF match found.")
            print()

