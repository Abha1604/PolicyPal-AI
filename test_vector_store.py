"""
Test vector_store.py

Run:
python test_vector_store.py
"""

from rag.document_processor import process_document
from rag.embedding_model import generate_embeddings
from rag.vector_store import VectorStore

PDF_PATH = "data/sample_contracts/EMPLOYMENT-AGREEMENT.pdf"
def main():

    print("=" * 70)
    print("TESTING VECTOR STORE")
    print("=" * 70)

    # --------------------------------------------------
    # Step 1: Process PDF
    # --------------------------------------------------
    document = process_document(PDF_PATH)

    document_id = document["document_id"]

    print(f"\nDocument ID : {document_id}")
    print(f"Chunks Created : {document['num_chunks']}")

    # --------------------------------------------------
    # Step 2: Generate Embeddings
    # --------------------------------------------------
    embedded_chunks = generate_embeddings(document["chunks"])

    print(f"Embeddings Generated : {len(embedded_chunks)}")

    # --------------------------------------------------
    # Step 3: Store in ChromaDB
    # --------------------------------------------------
    store = VectorStore()

    stored = store.store_embeddings(
        document_id=document_id,
        embedded_chunks=embedded_chunks
    )

    print(f"\nStored Chunks : {stored}")

    # --------------------------------------------------
    # Step 4: Check Database Count
    # --------------------------------------------------
    print(f"Total Chunks in Database : {store.count()}")

    # --------------------------------------------------
    # Step 5: Test Retrieval
    # --------------------------------------------------
    print("\nTesting Retrieval...")

    query_embedding = embedded_chunks[0]["embedding"]

    retrieved = store.retrieve_chunks(
        question_embedding=query_embedding,
        top_k=3
    )

    print(f"\nRetrieved {len(retrieved)} chunks\n")

    for i, chunk in enumerate(retrieved, start=1):

        print("=" * 60)
        print(f"RESULT {i}")
        print("=" * 60)

        print(f"Document ID : {chunk['document_id']}")
        print(f"Chunk ID    : {chunk['chunk_id']}")
        print(f"Distance    : {chunk['distance']:.6f}")
        print(f"Start Char  : {chunk['start_char']}")
        print(f"End Char    : {chunk['end_char']}")

        print("\nPreview:\n")
        print(chunk["text"][:250])

        print()

    print("=" * 70)
    print("✅ VECTOR STORE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()