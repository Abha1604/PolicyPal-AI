import chromadb

client = chromadb.PersistentClient(path="chroma_db")

client.delete_collection("contracts")

client.get_or_create_collection("contracts")

print("Database reset successfully.")