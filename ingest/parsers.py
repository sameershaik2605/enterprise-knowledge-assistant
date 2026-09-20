# ingest/parsers.py
# Reusable functions to extract clean text from PDF, DOCX, and TXT files.
# Every one of these returns a single string of plain text.

import pypdf
import docx


def load_pdf(path: str) -> str:
    """Extract text from a PDF file, page by page."""
    reader = pypdf.PdfReader(path)
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:  # skip pages that return nothing (e.g. blank/scanned pages)
            pages_text.append(text)
    return "\n".join(pages_text)


def load_docx(path: str) -> str:
    """Extract text from a DOCX file, skipping empty paragraphs."""
    doc = docx.Document(path)
    paragraphs = []
    for para in doc.paragraphs:
        if para.text.strip():  # skip empty/whitespace-only paragraphs
            paragraphs.append(para.text)
    return "\n".join(paragraphs)


def load_txt(path: str) -> str:
    """Read a plain text file, handling encoding issues gracefully."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback for older/non-UTF-8 files
        with open(path, "r", encoding="latin-1") as f:
            return f.read()


def load_document(path: str) -> str:
    """Route to the correct loader based on file extension."""
    if path.lower().endswith(".pdf"):
        return load_pdf(path)
    elif path.lower().endswith(".docx"):
        return load_docx(path)
    elif path.lower().endswith(".txt"):
        return load_txt(path)
    else:
        raise ValueError(f"Unsupported file type: {path}")


if __name__ == "__main__":
    # Quick manual test — run this file directly:
    # python ingest/parsers.py
    import os

    docs_folder = "docs"
    for filename in os.listdir(docs_folder):
        full_path = os.path.join(docs_folder, filename)
        try:
            text = load_document(full_path)
            print(f"\n{'='*50}")
            print(f"FILE: {filename}")
            print(f"Characters extracted: {len(text)}")
            print(f"First 200 chars: {text[:200]}")
        except Exception as e:
            print(f"\n{'='*50}")
            print(f"FILE: {filename} — FAILED: {e}")