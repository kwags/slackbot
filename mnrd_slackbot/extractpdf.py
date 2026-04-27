import pdfplumber
import re
import json
import os 

BASE_DIR = os.path.dirname(__file__)
pdf_path = os.path.join(BASE_DIR, "data/mnrd_DOC.pdf")
output_path = os.path.join(BASE_DIR, "data/mnrd_DOC_cleaned.json")



def extract_pdf_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def clean_pdf_text(text):
    # 1. Remove page numbers (single numbers on a line)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

    # 2. Add space if a number is smushed to a word, e.g., Election35.1 -> Election 35.1
    text = re.sub(r'([a-zA-Z])(\d+\.\d+(\.\d+)*)', r'\1 \2', text)

    # 3. Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text

heading_pattern = r'(?=(?:ARTICLE\s+[IVXLC]+|(?:\d+\.)+\d*(?:\.\d+)*\s+[A-Z]))'


def fix_sections(text):
    # Add a space before any number that looks like a subsection after a word or colon
    text = re.sub(r'([a-zA-Z])\d+', r'\1', text)
    return text

def chunk_pdf_text(text):
    sections = re.split(heading_pattern, text)
    chunks = []
    
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        
        # If there’s a colon, split section title vs text
        if ':' in sec:
            heading, body = sec.split(':', 1)
            heading = heading.strip() + ':'
            body = body.strip()
        else:
            heading = sec.strip()
            body = ''
        
        chunks.append({
            "section": heading,
            "text": body,
            "source": "MNRD By Laws"
        })
    
    return chunks


def build_documents(pdf_path):
    # Extract raw text
    with pdfplumber.open(pdf_path) as pdf:
        raw_text = "\n".join([page.extract_text() or '' for page in pdf.pages])
    
    # Clean and normalize
    clean_text = clean_pdf_text(raw_text)

    # Split into chunks
    chunks = chunk_pdf_text(clean_text)

    # Filter out chunks with empty text if needed
    chunks = [c for c in chunks if c["text"].strip()]

    return chunks

documents = build_documents(pdf_path)

# Save to JSON
with open(output_path, "w") as f:
    json.dump(documents, f, indent=2)


if __name__ == "__main__":
    docs = build_documents(pdf_path)

    with open(output_path, "w") as f:
        json.dump(docs, f, indent=2)

    print(f"JSON created at: {output_path}")
    print(f"Total sections: {len(docs)}")
          