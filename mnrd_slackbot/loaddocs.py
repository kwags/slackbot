import os
import json
import re
from normalizetext import normalize

DOC_FILES = [
    "data/mnrd_bylaws.json",
    "data/mnrd_leave.json",
    "data/mnrd_codeofconduct.json"
]

def clean_bylaws(text, doc_type):
    if doc_type == "mnrd_bylaws":
        text = re.sub(r'\b(article|section)\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b\d+(\.\d+)*\b', '', text)
        text = re.sub(r'[|:]', '', text)
        text = re.sub(r'\b[IVX]+\b', '', text)
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

            combined = f"{section} {article} {subsection} {text}"
            combined = clean_bylaws(combined, doc_type)
            doc["processed_text"] = normalize(combined)

            doc["source_file"] = os.path.basename(file_path)
            doc["doc_type"] = doc_type
        all_docs.extend(data)

    return all_docs


DOC_LIST = load_docs()