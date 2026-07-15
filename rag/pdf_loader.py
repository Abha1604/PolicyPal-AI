"""
pdf_loader.py

Reads a PDF contract and extracts:
1. Full text
2. Filename
3. Number of pages

Output Format:
{
    "filename": "...",
    "num_pages": 5,
    "text": "Entire extracted text..."
}
"""

import os
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> dict:
    """
    Extract text and metadata from a PDF.

    Parameters
    ----------
    pdf_path : str
        Path to the PDF document.

    Returns
    -------
    dict
        {
            "filename": str,
            "num_pages": int,
            "text": str
        }
    """

    try:
        document = fitz.open(pdf_path)

        pages_text = []

        for page in document:
            text = page.get_text("text")

            # Ignore completely blank pages
            if text.strip():
                pages_text.append(text)

        extracted_text = "\n".join(pages_text)

        result = {
            "filename": os.path.basename(pdf_path),
            "num_pages": len(document),
            "text": extracted_text
        }

        document.close()

        return result

    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")