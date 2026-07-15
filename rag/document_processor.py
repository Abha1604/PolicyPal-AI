import uuid

from rag.pdf_loader import extract_text_from_pdf
from rag.text_cleaner import clean_text
from rag.chunker import chunk_text


def process_document(pdf_path):
    """
    Complete document preprocessing pipeline.

    Steps:
    1. Load PDF
    2. Clean text
    3. Chunk text
    4. Generate document ID

    Parameters:
        pdf_path (str)

    Returns:
        dict
    """

    # -----------------------------
    # Step 1 : Extract text
    # -----------------------------
    raw_text, _ = extract_text_from_pdf(pdf_path)

    # -----------------------------
    # Step 2 : Clean text
    # -----------------------------
    cleaned_text = clean_text(raw_text)

    # -----------------------------
    # Step 3 : Chunk text
    # -----------------------------
    chunks = chunk_text(cleaned_text)

    # -----------------------------
    # Step 4 : Generate Document ID
    # -----------------------------
    document_id = f"doc_{uuid.uuid4().hex[:6]}"

    # -----------------------------
    # Final Output
    # -----------------------------
    return {
        "document_id": document_id,
        "chunks": chunks
    }