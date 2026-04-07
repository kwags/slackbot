import os
import json
import re
from normalizetext import normalize

DOC_FILES = [
    "data/mnrd_bylaws.json",
]

def clean_bylaws(text, doc_type):
    if doc_type == "mnrd_bylaws":
        text = re.sub(
            r'(Article|Section)\s+\S+|\d+(\.\d+)*|[|:]',
            '',
            text
        )

    return " ".join(text.split())

def load_docs():
    all_docs = []

    for file_path in DOC_FILES:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        
        doc_type = os.path.basename(file_path).replace(".json", "")

        with open(full_path, "r") as f:
            data = json.load(f)

        for doc in data:
            text = doc.get("text", "")
            section = doc.get("section", "")
            
            combined_text = section + " " + text
            cleaned_text = clean_bylaws(combined_text, doc_type)

            doc["processed_text"] = normalize(cleaned_text)

            doc["source_file"] = os.path.basename(file_path)
            doc["doc_type"] = doc_type
        all_docs.extend(data)

    return all_docs


DOC_LIST = load_docs()