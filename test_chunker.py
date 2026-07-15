from rag.pdf_loader import extract_text_from_pdf
from rag.text_cleaner import clean_text
from rag.chunker import chunk_text


pdf_path = "data/sample_contracts/COE-Sample.pdf"

raw_text, pages = extract_text_from_pdf(pdf_path)

cleaned_text = clean_text(raw_text)

chunks = chunk_text(cleaned_text)

print("=" * 60)
print(f"Total Chunks: {len(chunks)}")
print("=" * 60)

print("\nFirst Chunk:\n")
print(chunks[0])

print("\nSecond Chunk:\n")
print(chunks[1])