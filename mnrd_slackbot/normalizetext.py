import re

SYNONYMS = {
    "bod": "board of directors",
    "board": "board of directors",
    "loa": "leave of absence",
    "leave": "leave of absence",
}

# normalize text
def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    text = " ".join(text.split())        # remove extra spaces
    return text

