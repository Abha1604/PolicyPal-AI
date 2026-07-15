"""
Test pipeline.py

Run:
python test_pipeline.py
"""

from rag.pipeline import RAGPipeline

PDF_PATH = "data/sample_contracts/EMPLOYMENT-AGREEMENT.pdf"


def main():

    print("=" * 80)
    print("TESTING COMPLETE RAG PIPELINE")
    print("=" * 80)

    pipeline = RAGPipeline()

    print("\nIngesting document...\n")

    document = pipeline.ingest_document(PDF_PATH)

    print("Document Information")
    print("-" * 50)

    print(f"Filename      : {document['filename']}")
    print(f"Document ID   : {document['document_id']}")
    print(f"Pages         : {document['num_pages']}")
    print(f"Chunks        : {document['num_chunks']}")
    print(f"Stored Chunks : {document['stored_chunks']}")

    questions = [

        "What are the payment terms?",

        "Can the employee resign?",

        "What is the notice period?",

        "What are the termination conditions?",

        "Who resolves disputes?"

    ]

    for question in questions:

        print("\n")
        print("=" * 80)
        print(f"QUESTION")
        print("=" * 80)

        print(question)

        results = pipeline.query(
            question,
            top_k=3
        )

        if not results:

            print("\nNo chunks found.\n")

            continue

        print("\nTop Retrieved Chunks\n")

        for i, chunk in enumerate(results, start=1):

            print("-" * 70)

            print(f"Rank        : {i}")
            print(f"Chunk ID    : {chunk['chunk_id']}")
            print(f"Distance    : {chunk['distance']:.4f}")

            print("\nPreview:\n")

            print(chunk["text"][:350])

            if len(chunk["text"]) > 350:
                print("...")

            print()

    print("=" * 80)
    print("✅ COMPLETE PIPELINE TEST PASSED")
    print("=" * 80)


if __name__ == "__main__":
    main()