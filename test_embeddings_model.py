"""
Test embedding_model.py

Run:
python test_embedding_model.py
"""

from rag.document_processor import process_document
from rag.embedding_model import generate_embeddings

PDF_PATH = "data/sample_contracts/EMPLOYMENT-AGREEMENT.pdf"


def main():

    print("=" * 70)
    print("TESTING EMBEDDING MODEL")
    print("=" * 70)

    document = process_document(PDF_PATH)

    embedded_chunks = generate_embeddings(document["chunks"])

    print("\n✅ Embeddings Generated Successfully\n")

    print(f"Total Chunks : {len(embedded_chunks)}")

    print("\nFirst Embedded Chunk")
    print("-" * 70)

    first = embedded_chunks[0]

    print(f"Chunk ID : {first['chunk_id']}")
    print(f"Text Length : {len(first['text'])}")

    print(f"Embedding Dimension : {len(first['embedding'])}")

    print("\nFirst 10 Embedding Values:\n")

    print(first["embedding"][:10])

    print("\nLast Embedded Chunk")
    print("-" * 70)

    last = embedded_chunks[-1]

    print(f"Chunk ID : {last['chunk_id']}")
    print(f"Embedding Dimension : {len(last['embedding'])}")

    print("\n✅ Embedding Model Passed")
    

if __name__ == "__main__":
    main()