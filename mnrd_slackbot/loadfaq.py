import os
import json
from normalizetext import normalize

# FAQ file
FAQ_FILE = os.path.join(os.path.dirname(__file__), "data/mnrd_FAQ.json")

SYNONYMS = {
    "bod": "board of directors",
    "board": "board of directors",
    "loa": "leave of absence",
    "leave": "leave of absence",
}

def load_FAQ():
    with open(FAQ_FILE, "r") as f:
        data = json.load(f)

    for faq in data:
        faq["normalized_question"] = normalize(faq["question"])

        # normalize keywords
        kws = faq.get("keywords", "")
        faq["normalized_keywords"] = [
            normalize(k.strip()) for k in kws.split(",") if k.strip()
        ]

    return data


FAQ_LIST = load_FAQ()