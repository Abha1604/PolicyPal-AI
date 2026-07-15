from rag.document_processor import process_document


pdf_path = "data/sample_contracts/COE-Sample.pdf"

document = process_document(pdf_path)

print("=" * 60)
print("DOCUMENT PROCESSOR OUTPUT")
print("=" * 60)

print(f"Document ID : {document['document_id']}")
print(f"Total Chunks: {len(document['chunks'])}")

print("\nFirst Chunk:\n")

print(document["chunks"][0])