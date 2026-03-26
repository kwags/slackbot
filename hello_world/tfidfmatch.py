import os
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# DOC file
DOC_FILE = os.path.join(os.path.dirname(__file__), "data/mnrd_bylaws.json")

# load DOC file
with open(DOC_FILE, "r") as f:
    document = json.load(f) 

corpus = [doc["section"] + doc["text"] for doc in document]
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), lowercase=True)
tfidf_matrix = vectorizer.fit_transform(corpus)

def get_tfidf_match(user_msg, threshold=0.2, return_score=False):   
    user_msg = user_msg.lower().strip()
    msg_vec = vectorizer.transform([user_msg])
    similarities = cosine_similarity(msg_vec, tfidf_matrix)[0]

    best_index = similarities.argmax()
    best_score = similarities[best_index]

    if best_score >= threshold:
        answer= document[best_index]
        formatted_answer = format_tfidf_answer(answer)
        matched_section = answer.get("section","")
        return formatted_answer, best_score, matched_section

    return None, 0, None

def format_tfidf_answer(doc, max_words = 20):
    source = doc.get("source", "")
    section = doc.get("section", "")
    text = doc.get("text", "")
    link = doc.get("link", "")
    
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words]) + "..."
    
    answer = (
        f"According to the {source} {section} \n{text} "
        f"You can read more about this here: {link}"
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
        answer, score, section = get_tfidf_match(q)
        if answer:
            print(f"Question: {q}\nAnswer: {answer}\nScore: {score}\nSection: {section}")
        else:
            print(f"Question: {q}\nAnswer: No TF-IDF match found.")

