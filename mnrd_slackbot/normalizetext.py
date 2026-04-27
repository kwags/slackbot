import re

ABBREVIATIONS = {
    "bod": "board",
    "board of directors": "board",
    "loa": "leave of absence",
    "loa-a": "leave of absence non participating",
    "loa-b": "leave of absence participating"
}

def abbreviations(text):
    text = text.lower()

    for k, v in ABBREVIATIONS.items():
        text = re.sub(rf"\b{re.escape(k)}\b", v, text)

    return text


# normalize text
def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = abbreviations(text)
    text = " ".join(text.split())
    return text

