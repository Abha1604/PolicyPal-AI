"""
Test chunker.py

Run:
python test_chunker.py
"""

from rag.pdf_loader import extract_text_from_pdf
from rag.text_cleaner import clean_text
from rag.chunker import create_chunks

PDF_PATH = "data/sample_contracts/EMPLOYMENT-AGREEMENT.pdf"


def main():

    print("=" * 70)
    print("TESTING CHUNKER")
    print("=" * 70)

    pdf = extract_text_from_pdf(PDF_PATH)

    cleaned_text = clean_text(pdf["text"])

    chunks = create_chunks(cleaned_text)

    print(f"\nTotal Chunks : {len(chunks)}")

    print("\n" + "=" * 70)
    print("FIRST CHUNK")
    print("=" * 70)

    first = chunks[0]

    print(f"Chunk ID   : {first['chunk_id']}")
    print(f"Start Char : {first['start_char']}")
    print(f"End Char   : {first['end_char']}")
    print(f"Length     : {len(first['text'])}")

    print("\nPreview:\n")
    print(first["text"][:300])

    print("\n" + "=" * 70)
    print("LAST CHUNK")
    print("=" * 70)

    last = chunks[-1]

    print(f"Chunk ID   : {last['chunk_id']}")
    print(f"Start Char : {last['start_char']}")
    print(f"End Char   : {last['end_char']}")
    print(f"Length     : {len(last['text'])}")

    print("\nPreview:\n")
    print(last["text"][:300])

    print("\n" + "=" * 70)
    print("ALL CHUNK DETAILS")
    print("=" * 70)

    for chunk in chunks:

        print(
            f"Chunk {chunk['chunk_id']:>2} | "
            f"Start: {chunk['start_char']:>5} | "
            f"End: {chunk['end_char']:>5} | "
            f"Length: {len(chunk['text'])}"
        )

    print("\n✅ Chunking Successful")

if __name__ == "__main__":
    main()