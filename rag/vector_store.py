"""
vector_store.py

Handles storing and retrieving document embeddings using ChromaDB.

Responsibilities:
-----------------
1. Store embedded document chunks.
2. Replace old embeddings if the same document is uploaded again.
3. Retrieve the most relevant chunks for a query.
4. Count stored chunks.
5. Delete a document from the database.
"""

import chromadb
from chromadb.config import Settings


class VectorStore:
    """
    Wrapper around ChromaDB for storing and retrieving embeddings.
    """

    def __init__(
        self,
        db_path="data/chroma_db",
        collection_name="contracts"
    ):

        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    # ---------------------------------------------------
    # Store Embeddings
    # ---------------------------------------------------

    def store_embeddings(self, document_id, embedded_chunks):
        """
        Store embedded chunks into ChromaDB.

        If embeddings of the same document already exist,
        they are deleted before inserting new ones.

        Parameters
        ----------
        document_id : str

        embedded_chunks : list

        Returns
        -------
        int
            Number of stored chunks.
        """

        existing = self.collection.get(
            where={"document_id": document_id}
        )

        if existing["ids"]:

            self.collection.delete(
                where={"document_id": document_id}
            )

        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for chunk in embedded_chunks:

            ids.append(
                f"{document_id}_{chunk['chunk_id']}"
            )

            embeddings.append(
                chunk["embedding"]
            )

            documents.append(
                chunk["text"]
            )

            metadatas.append(
                {
                    "document_id": document_id,
                    "chunk_id": chunk["chunk_id"],
                    "start_char": chunk["start_char"],
                    "end_char": chunk["end_char"]
                }
            )

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        return len(ids)

    # ---------------------------------------------------
    # Retrieve Chunks
    # ---------------------------------------------------

    def retrieve_chunks(
        self,
        question_embedding,
        top_k=3
    ):
        """
        Retrieve the most relevant chunks.

        Parameters
        ----------
        question_embedding : list

        top_k : int

        Returns
        -------
        list
        """

        results = self.collection.query(

            query_embeddings=[question_embedding],

            n_results=top_k

        )

        if not results["documents"] or not results["documents"][0]:
            return []

        retrieved_chunks = []

        documents = results["documents"][0]

        metadatas = results["metadatas"][0]

        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            retrieved_chunks.append(
                {
                    "document_id": metadata["document_id"],

                    "chunk_id": metadata["chunk_id"],

                    "text": document,

                    "start_char": metadata["start_char"],

                    "end_char": metadata["end_char"],

                    "distance": distance
                }
            )

        return retrieved_chunks

    # ---------------------------------------------------
    # Count Stored Chunks
    # ---------------------------------------------------

    def count(self):
        """
        Returns total number of chunks stored.
        """

        return self.collection.count()

    # ---------------------------------------------------
    # Delete Document
    # ---------------------------------------------------

    def delete_document(self, document_id):
        """
        Delete all chunks of a document.

        Parameters
        ----------
        document_id : str
        """

        self.collection.delete(
            where={
                "document_id": document_id
            }
        )