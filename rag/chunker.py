def chunk_text(text, chunk_size=500, overlap=100):
    """
    Splits text into overlapping chunks.

    Priority for chunk ending:
    1. Paragraph break (\n\n)
    2. Sentence end (. ? !)
    3. Space
    4. Fixed chunk size

    Parameters:
        text (str): Cleaned document text
        chunk_size (int): Approximate size of each chunk
        overlap (int): Number of overlapping characters

    Returns:
        list: List of dictionaries containing chunk_id and text
    """

    chunks = []

    start = 0
    chunk_number = 1
    text_length = len(text)

    while start < text_length:

        # Tentative end position
        end = min(start + chunk_size, text_length)

        # Try to find a better place to end the chunk
        if end < text_length:

            search_start = max(start, end - 150)

            # Priority 1: Paragraph break
            paragraph = text.rfind("\n\n", search_start, end)

            if paragraph != -1:
                end = paragraph + 2

            else:

                # Priority 2: Sentence end
                sentence = max(
                    text.rfind(". ", search_start, end),
                    text.rfind("? ", search_start, end),
                    text.rfind("! ", search_start, end),
                )

                if sentence != -1:
                    end = sentence + 2

                else:

                    # Priority 3: Space
                    space = text.rfind(" ", search_start, end)

                    if space != -1:
                        end = space

        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "chunk_id": f"chunk_{chunk_number}",
                "text": chunk
            })
            chunk_number += 1

        # Finished?
        if end >= text_length:
            break

        # -------------------------------
        # Overlap
        # -------------------------------
        start = max(end - overlap, 0)

        # Move to the beginning of the next word
        while start < text_length and text[start] not in [" ", "\n"]:
            start += 1

        # Skip spaces/newlines
        while start < text_length and text[start] in [" ", "\n"]:
            start += 1

    return chunks