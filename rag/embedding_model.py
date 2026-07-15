"""
embedding_model.py

Handles all embedding operations using a single shared model.

Functions
---------
1. generate_embeddings(chunks)
   -> Generates embeddings for document chunks.

2. embed_query(query)
   -> Generates embedding for a user query.
"""

from sentence_transformers import SentenceTransformer

# --------------------------------------------------------
# Load the embedding model ONLY ONCE
# --------------------------------------------------------

_MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(_MODEL_NAME)


# --------------------------------------------------------
# Document Embeddings
# --------------------------------------------------------

def generate_embeddings(chunks):
    """
    Generate embeddings for document chunks.

    Parameters
    ----------
    chunks : list
        List of chunk dictionaries.

    Returns
    -------
    list
        Same chunks with embeddings added.
    """

    if not chunks:
        return []

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):

        embedded_chunks.append(
            {
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "start_char": chunk["start_char"],
                "end_char": chunk["end_char"],
                "embedding": embedding.tolist()
            }
        )

    return embedded_chunks


# --------------------------------------------------------
# Query Embedding
# --------------------------------------------------------

def embed_query(query):
    """
    Generate embedding for a user query.

    Parameters
    ----------
    query : str

    Returns
    -------
    list
        Query embedding as a Python list.
    """

    embedding = model.encode(
        query,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return embedding.tolist()


# --------------------------------------------------------
# Utility
# --------------------------------------------------------

def get_embedding_dimension():
    """
    Returns the embedding dimension of the model.

    Returns
    -------
    int
    """

    return model.get_sentence_embedding_dimension()


def get_model_name():
    """
    Returns the embedding model name.
    """

    return _MODEL_NAME