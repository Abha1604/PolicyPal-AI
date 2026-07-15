"""
Test document_processor.py

Run:
python test_document_processor.py
"""

from rag.document_processor import process_document

PDF_PATH = "data/sample_contracts/EMPLOYMENT-AGREEMENT.pdf"


def main():

    print("=" * 70)
    print("TESTING DOCUMENT PROCESSOR")
    print("=" * 70)

    try:

        document = process_document(PDF_PATH)

        print("\n✅ Document Processed Successfully\n")

        print(f"Document ID : {document['document_id']}")
        print(f"Filename    : {document['filename']}")
        print(f"Pages       : {document['num_pages']}")
        print(f"Chunks      : {document['num_chunks']}")

        print("\nFirst Chunk")
        print("-" * 70)

        first = document["chunks"][0]

        print(f"Chunk ID   : {first['chunk_id']}")
        print(f"Start Char : {first['start_char']}")
        print(f"End Char   : {first['end_char']}")

        print("\nText Preview:\n")
        print(first["text"][:300])

        print("\nLast Chunk")
        print("-" * 70)

        last = document["chunks"][-1]

        print(f"Chunk ID   : {last['chunk_id']}")
        print(f"Start Char : {last['start_char']}")
        print(f"End Char   : {last['end_char']}")

        print("\nText Preview:\n")
        print(last["text"][:300])

    except Exception as e:

        print("\n❌ ERROR")
        print(e)


if __name__ == "__main__":
    main()