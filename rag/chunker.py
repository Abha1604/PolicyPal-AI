"""
chunker.py

Splits cleaned text into overlapping chunks.

The chunker tries to create chunks at natural text boundaries.

Priority:
1. Paragraph
2. Sentence
3. Word
4. Hard cut

Output Example:
[
    {
        "chunk_id": 1,
        "text": "...",
        "start_char": 0,
        "end_char": 500
    }
]
"""


def _find_chunk_end(text: str, max_end: int, search_window: int = 100):
    """
    Find a natural place to end a chunk.

    Looks ahead for:
    1. Paragraph break
    2. Sentence end
    3. Space
    """

    if max_end >= len(text):
        return len(text)

    limit = min(max_end + search_window, len(text))

    window = text[max_end:limit]

    # -------------------------
    # Paragraph
    # -------------------------

    pos = window.find("\n\n")

    if pos != -1:
        return max_end + pos + 2

    # -------------------------
    # Sentence
    # -------------------------

    for symbol in [".", "!", "?"]:

        pos = window.find(symbol)

        if pos != -1:
            return max_end + pos + 1

    # -------------------------
    # Word Boundary
    # -------------------------

    pos = window.find(" ")

    if pos != -1:
        return max_end + pos

    # Hard cut

    return max_end


def _find_next_start(text: str, start: int):
    """
    Move the next chunk start to the beginning
    of the next complete word.
    """

    if start <= 0:
        return 0

    while start < len(text):

        if text[start] == " ":
            return start + 1

        start += 1

    return start


def create_chunks(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
):
    """
    Split cleaned text into overlapping chunks.

    Parameters
    ----------
    text : str

    chunk_size : int

    chunk_overlap : int

    Returns
    -------
    list
    """

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks = []

    chunk_id = 1

    start = 0

    while start < len(text):

        max_end = min(start + chunk_size, len(text))

        end = _find_chunk_end(text, max_end)

        chunk_text = text[start:end].strip()

        chunks.append(
            {
                "chunk_id": chunk_id,
                "text": chunk_text,
                "start_char": start,
                "end_char": end,
            }
        )

        chunk_id += 1

        if end >= len(text):
            break

        next_start = end - chunk_overlap

        start = _find_next_start(text, next_start)

    return chunks