"""
text_cleaner.py

Cleans extracted PDF text before chunking.

Cleaning includes:
- Remove extra spaces
- Remove extra blank lines
- Remove page numbers
- Remove repeated headers/footers (basic)
- Normalize whitespace
"""

import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
        Cleaned text
    """

    # -------------------------------
    # Normalize newlines
    # -------------------------------
    text = text.replace("\r", "\n")

    # -------------------------------
    # Replace tabs with spaces
    # -------------------------------
    text = text.replace("\t", " ")

    # -------------------------------
    # Remove multiple spaces
    # -------------------------------
    text = re.sub(r"[ ]+", " ", text)

    # -------------------------------
    # Remove multiple blank lines
    # -------------------------------
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # -------------------------------
    # Remove standalone page numbers
    #
    # Example:
    # Page 3
    # PAGE 10
    # page 5
    # -------------------------------
    text = re.sub(
        r"(?im)^\s*page\s+\d+\s*$",
        "",
        text
    )

    # -------------------------------
    # Remove page number only
    #
    # Example:
    # 1
    # 15
    # 104
    # -------------------------------
    text = re.sub(
        r"(?m)^\s*\d+\s*$",
        "",
        text
    )

    # -------------------------------
    # Remove repeated confidentiality labels
    #
    # Example:
    # CONFIDENTIAL
    # Confidential
    # -------------------------------
    text = re.sub(
        r"(?im)^confidential\s*$",
        "",
        text
    )

    # -------------------------------
    # Remove excessive blank lines again
    # -------------------------------
    text = re.sub(r"\n{3,}", "\n\n", text)

    # -------------------------------
    # Final strip
    # -------------------------------
    return text.strip()