"""
Vector Store

Uploads and manages vectors in Pinecone.
"""

from typing import List

from sqlalchemy.orm import Session

from database.models import Transaction

from rag.embeddings import EmbeddingModel
from rag.document_builder import DocumentBuilder
from rag.pinecone_client import get_index

from core.logger import logger


class VectorStore:
    """
    Pinecone Vector Store
    """

    def __init__(self):

        self.index = get_index()

    # ======================================================
    # Upload Single Transaction
    # ======================================================

    def upload_transaction(
        self,
        transaction: Transaction
    ):

        document = DocumentBuilder.build_document(
            transaction
        )

        embedding = EmbeddingModel.embed_text(
            document
        )

        metadata = DocumentBuilder.build_metadata(
            transaction
        )

        self.index.upsert(
            vectors=[
                {
                    "id": str(transaction.transaction_id),
                    "values": embedding,
                    "metadata": metadata
                }
            ]
        )

        logger.success(
            f"Uploaded Transaction {transaction.transaction_id}"
        )

    # ======================================================
    # Upload Multiple Transactions (Optimized)
    # ======================================================

    def upload_transactions(
        self,
        transactions: List[Transaction]
    ):

        logger.info(
            f"Uploading {len(transactions)} transactions..."
        )

        if not transactions:
            return

        # Build documents
        documents = [
            DocumentBuilder.build_document(t)
            for t in transactions
        ]

        logger.info("Generating embeddings...")

        embeddings = EmbeddingModel.embed_batch(
            documents,
            batch_size=64
        )

        logger.success("Embeddings generated.")

        vectors = []

        for transaction, embedding in zip(
            transactions,
            embeddings
        ):

            vectors.append(
                {
                    "id": str(transaction.transaction_id),
                    "values": embedding,
                    "metadata": DocumentBuilder.build_metadata(
                        transaction
                    )
                }
            )

        batch_size = 100

        for i in range(0, len(vectors), batch_size):

            self.index.upsert(
                vectors=vectors[i:i + batch_size]
            )

            logger.info(
                f"Uploaded {min(i + batch_size, len(vectors))}/{len(vectors)} vectors"
            )

        logger.success(
            f"{len(vectors)} vectors uploaded successfully."
        )

    # ======================================================
    # Upload Entire Database
    # ======================================================

    def upload_database(
        self,
        db: Session
    ):

        transactions = db.query(
            Transaction
        ).all()

        self.upload_transactions(
            transactions
        )

    # ======================================================
    # Delete Vector
    # ======================================================

    def delete_vector(
        self,
        vector_id: int
    ):

        self.index.delete(
            ids=[str(vector_id)]
        )

        logger.success(
            f"Vector {vector_id} deleted."
        )

    # ======================================================
    # Fetch Vector
    # ======================================================

    def fetch_vector(
        self,
        vector_id: int
    ):

        return self.index.fetch(
            ids=[str(vector_id)]
        )

    # ======================================================
    # Vector Count
    # ======================================================

    def vector_count(self):

        stats = self.index.describe_index_stats()

        return stats["total_vector_count"]