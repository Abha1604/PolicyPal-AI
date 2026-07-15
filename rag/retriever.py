"""
retriever.py

Retrieves the most relevant document chunks for a user query.

Responsibilities
----------------
1. Convert a user question into an embedding.
2. Retrieve the most relevant chunks from the Vector Store.
3. Return the retrieved chunks.
"""

from rag.embedding_model import embed_query
from rag.vector_store import VectorStore


class Retriever:
    """
    Retrieves relevant document chunks for user queries.
    """

    def __init__(self):

        self.vector_store = VectorStore()

    def retrieve(
        self,
        question: str,
        top_k: int = 3
    ):
        """
        Retrieve the most relevant chunks.

        Parameters
        ----------
        question : str
            User query.

        top_k : int
            Number of chunks to retrieve.

        Returns
        -------
        list
            Retrieved chunks.
        """

        # -----------------------------
        # Validate Input
        # -----------------------------

        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty.")

        # -----------------------------
        # Generate Query Embedding
        # -----------------------------

        question_embedding = embed_query(question)

        # -----------------------------
        # Retrieve Chunks
        # -----------------------------

        retrieved_chunks = self.vector_store.retrieve_chunks(
            question_embedding=question_embedding,
            top_k=top_k
        )

        return retrieved_chunks