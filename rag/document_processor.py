"""
document_processor.py

Complete document preprocessing pipeline.

Pipeline:
PDF
    ↓
Extract Text
    ↓
Clean Text
    ↓
Chunk Text

Output Format:
{
    "document_id": "...",
    "filename": "...",
    "num_pages": 5,
    "num_chunks": 20,
    "chunks": [...]
}
"""

import hashlib
import os

from rag.pdf_loader import extract_text_from_pdf
from rag.text_cleaner import clean_text
from rag.chunker import create_chunks


def generate_document_id(pdf_path: str):
    """
    Generate a deterministic document ID based on the PDF file.

    The same PDF will always generate the same ID,
    while different PDFs will generate different IDs.
    """

    hasher = hashlib.md5()

    with open(pdf_path, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            hasher.update(chunk)

    filename = os.path.splitext(
        os.path.basename(pdf_path)
    )[0]

    file_hash = hasher.hexdigest()[:8]

    return f"{filename}_{file_hash}"


def process_document(
    pdf_path: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
):
    """
    Process a PDF document into chunks.

    Parameters
    ----------
    pdf_path : str

    chunk_size : int

    chunk_overlap : int

    Returns
    -------
    dict
    """

    # ---------------------------------
    # Extract PDF
    # ---------------------------------

    pdf_data = extract_text_from_pdf(pdf_path)

    # ---------------------------------
    # Clean Text
    # ---------------------------------

    cleaned_text = clean_text(pdf_data["text"])

    # ---------------------------------
    # Chunk Text
    # ---------------------------------

    chunks = create_chunks(
        cleaned_text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # ---------------------------------
    # Build Final Output
    # ---------------------------------

    processed_document = {

        "document_id": generate_document_id(pdf_path),

        "filename": pdf_data["filename"],

        "num_pages": pdf_data["num_pages"],

        "num_chunks": len(chunks),

        "chunks": chunks

    }

    return processed_document