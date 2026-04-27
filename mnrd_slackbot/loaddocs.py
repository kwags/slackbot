import os
import json
import re
from normalizetext import normalize

DOC_FILES = [
    "data/mnrd_bylaws.json",
    "data/mnrd_leave.json"
]

def clean_bylaws(text, doc_type):
    if doc_type == "mnrd_bylaws":
        text = re.sub(r'[|:]', '', text)

    return " ".join(text.split())

def load_docs():
    all_docs = []

    for file_path in DOC_FILES:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        
        doc_type = os.path.basename(file_path).replace(".json", "")

        with open(full_path, "r") as f:
            data = json.load(f)

        for doc in data:
            article = doc.get("article", "")
            section = doc.get("section", "")
            subsection = doc.get("subsection", "")
            text = doc.get("text", "")

            cleaned_text = clean_bylaws(text, doc_type)
            cleaned_section = clean_bylaws(section, doc_type)
            cleaned_article = clean_bylaws(article, doc_type)        
            text_norm = normalize(cleaned_text)

            section_norm = normalize(cleaned_section)
            article_norm = normalize(cleaned_article)
            subsection_norm = normalize(subsection)
            combined_text = section + " " + text + " " + article + " " + subsection
            cleaned_text = clean_bylaws(combined_text, doc_type)

            doc["processed_text"] = (
                text_norm + " " + text_norm + " " + text_norm +
                section_norm + " " +
                subsection_norm + " " +
                article_norm
            )   
            doc["source_file"] = os.path.basename(file_path)
            doc["doc_type"] = doc_type
        all_docs.extend(data)

    return all_docs


DOC_LIST = load_docs()