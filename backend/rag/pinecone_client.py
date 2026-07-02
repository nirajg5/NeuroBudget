"""
Pinecone Client

Creates and manages the Pinecone connection.
"""

from pinecone import Pinecone, ServerlessSpec

from core.config import settings
from core.logger import logger


pc = None

index = None


def initialize_pinecone():
    """
    Initialize Pinecone and create the index if it does not exist.
    """

    global pc
    global index

    try:

        pc = Pinecone(
            api_key=settings.PINECONE_API_KEY
        )

        existing_indexes = [

            item["name"]

            for item in pc.list_indexes()

        ]

        if settings.PINECONE_INDEX not in existing_indexes:

            logger.info(
                "Creating Pinecone Index..."
            )

            pc.create_index(

                name=settings.PINECONE_INDEX,

                dimension=384,

                metric="cosine",

                spec=ServerlessSpec(

                    cloud="aws",

                    region=settings.PINECONE_REGION

                )

            )

            logger.success(
                "Pinecone index created."
            )

        index = pc.Index(
            settings.PINECONE_INDEX
        )

        logger.success(
            "Connected to Pinecone."
        )

    except Exception as e:

        logger.exception(e)

        raise

def get_index():
    """
    Returns the Pinecone Index.
    """

    global index

    if index is None:

        initialize_pinecone()

    return index

def get_index_stats():
    """
    Returns index statistics.
    """

    idx = get_index()

    return idx.describe_index_stats()

def delete_all_vectors():
    """
    Delete every vector from Pinecone.
    """

    idx = get_index()

    idx.delete(
        delete_all=True
    )

    logger.success(
        "All vectors deleted."
    )

