"""
Test retriever.py

Run:
python test_retriever.py
"""

from rag.document_processor import process_document
from rag.embedding_model import generate_embeddings
from rag.vector_store import VectorStore
from rag.retriever import Retriever

PDF_PATH = "data/sample_contracts/EMPLOYMENT-AGREEMENT.pdf"


def main():

    print("=" * 80)
    print("TESTING RETRIEVER")
    print("=" * 80)

    # --------------------------------------------------
    # Step 1: Process Document
    # --------------------------------------------------

    document = process_document(PDF_PATH)

    print(f"\nDocument : {document['filename']}")
    print(f"Document ID : {document['document_id']}")
    print(f"Pages : {document['num_pages']}")
    print(f"Chunks : {document['num_chunks']}")

    # --------------------------------------------------
    # Step 2: Generate Embeddings
    # --------------------------------------------------

    embedded_chunks = generate_embeddings(document["chunks"])

    print("\nGenerating embeddings... Done!")

    # --------------------------------------------------
    # Step 3: Store in Vector Database
    # --------------------------------------------------

    store = VectorStore()

    stored = store.store_embeddings(
        document["document_id"],
        embedded_chunks
    )

    print(f"Stored {stored} chunks into ChromaDB.")

    # --------------------------------------------------
    # Step 4: Initialize Retriever
    # --------------------------------------------------

    retriever = Retriever()

    # --------------------------------------------------
    # Step 5: Test Multiple Questions
    # --------------------------------------------------

    questions = [

        "What is the employee's salary?",

        "What are the payment terms?",

        "Can the employee resign?",

        "What is the notice period?",

        "What are the termination conditions?",

        "Is there any confidentiality clause?",

        "Who will resolve disputes?",

        "How long is the employment period?"

    ]

    for question in questions:

        print("\n")
        print("=" * 80)
        print(f"QUESTION")
        print("=" * 80)

        print(question)

        results = retriever.retrieve(
            question=question,
            top_k=3
        )

        if not results:

            print("\nNo relevant chunks found.\n")
            continue

        print("\nRetrieved Chunks:\n")

        for index, chunk in enumerate(results, start=1):

            print("-" * 70)

            print(f"Rank        : {index}")
            print(f"Document ID : {chunk['document_id']}")
            print(f"Chunk ID    : {chunk['chunk_id']}")
            print(f"Distance    : {chunk['distance']:.4f}")

            print("\nChunk Preview:\n")

            preview = chunk["text"][:400]

            print(preview)

            if len(chunk["text"]) > 400:
                print("...")

            print()

    print("=" * 80)
    print("✅ RETRIEVER TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()