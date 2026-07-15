"""
pipeline.py

End-to-end RAG pipeline for PolicyPal AI.

Pipeline
--------
PDF
    ↓
Process Document
    ↓
Generate Embeddings
    ↓
Store in ChromaDB

Question
    ↓
Generate Query Embedding
    ↓
Retrieve Relevant Chunks
"""

from rag.document_processor import process_document
from rag.embedding_model import generate_embeddings
from rag.vector_store import VectorStore
from rag.retriever import Retriever


class RAGPipeline:
    """
    Complete RAG Pipeline.
    """

    def __init__(self):

        self.vector_store = VectorStore()

        self.retriever = Retriever()

    # ----------------------------------------------------
    # Document Ingestion
    # ----------------------------------------------------

    def ingest_document(
        self,
        pdf_path,
        chunk_size=500,
        chunk_overlap=100
    ):
        """
        Process a PDF and store it in ChromaDB.

        Returns
        -------
        dict
            Processed document information.
        """

        document = process_document(
            pdf_path,
            chunk_size,
            chunk_overlap
        )

        embedded_chunks = generate_embeddings(
            document["chunks"]
        )

        stored = self.vector_store.store_embeddings(
            document["document_id"],
            embedded_chunks
        )

        document["stored_chunks"] = stored

        return document

    # ----------------------------------------------------
    # Query
    # ----------------------------------------------------

    def query(
        self,
        question,
        top_k=3
    ):
        """
        Retrieve relevant chunks.

        Parameters
        ----------
        question : str

        top_k : int

        Returns
        -------
        list
        """

        return self.retriever.retrieve(
            question=question,
            top_k=top_k
        )