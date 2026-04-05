import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file."""
    doc = fitz.open(pdf_path)
    full_text = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            full_text.append(text)
    doc.close()
    return "\n\n".join(full_text)
