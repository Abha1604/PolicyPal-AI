from rag.vector_store import collection

print("=" * 60)
print("VECTOR DATABASE INFO")
print("=" * 60)

print("Total Chunks Stored:")

print(collection.count())