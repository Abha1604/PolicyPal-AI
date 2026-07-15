import re

def clean_text(text):
    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Replace multiple spaces with one
    text = re.sub(r"[ ]+", " ", text)

    # Remove extra blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove page numbers like "Page 1"
    text = re.sub(r"Page\s+\d+", "", text, flags=re.IGNORECASE)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text