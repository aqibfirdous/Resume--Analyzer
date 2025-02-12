# pdf_extraction.py
import requests
import pdfplumber
import io

def extract_text_from_pdf(url):
    """
    Downloads a PDF from the given URL and extracts its text.
    Returns the extracted text or an error message.
    """
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            text = "".join([page.extract_text() or "" for page in pdf.pages]).strip()
            return text or "[No text extracted]"
    except Exception as e:
        return f"[Error: {e}]"
