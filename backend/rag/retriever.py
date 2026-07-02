"""
Retriever

Retrieves relevant transactions from Pinecone.
"""

from typing import List, Dict, Optional

from rag.embeddings import EmbeddingModel
from rag.pinecone_client import get_index

from core.logger import logger


class Retriever:

    """
    Semantic Retriever
    """

    def __init__(self):

        self.index = get_index()

    # ======================================================
    # Search Pinecone
    # ======================================================

    def search(
        self,
        query: str,
        top_k: int = 5,
        metadata_filter: Optional[dict] = None
    ) -> List[Dict]:

        logger.info(f"Searching for: {query}")

        query_embedding = EmbeddingModel.embed_text(query)

        response = self.index.query(

            vector=query_embedding,

            top_k=top_k,

            include_metadata=True,

            filter=metadata_filter

        )

        results = []

        for match in response.matches:

            results.append({

                "id": match.id,

                "score": round(match.score, 4),

                "metadata": match.metadata

            })

        logger.success(
            f"{len(results)} transactions retrieved."
        )

        return results

    # ======================================================
    # Search by Category
    # ======================================================

    def search_category(
        self,
        query: str,
        category: str,
        top_k: int = 5
    ):

        return self.search(

            query=query,

            top_k=top_k,

            metadata_filter={

                "category": category

            }

        )

    # ======================================================
    # Search by Merchant
    # ======================================================

    def search_merchant(
        self,
        query: str,
        merchant: str,
        top_k: int = 5
    ):

        return self.search(

            query=query,

            top_k=top_k,

            metadata_filter={

                "merchant": merchant

            }

        )

    # ======================================================
    # Search Expenses Only
    # ======================================================

    def search_expenses(
        self,
        query: str,
        top_k: int = 5
    ):

        return self.search(

            query=query,

            top_k=top_k,

            metadata_filter={

                "flow": "Expense"

            }

        )

    # ======================================================
    # Search Income Only
    # ======================================================

    def search_income(
        self,
        query: str,
        top_k: int = 5
    ):

        return self.search(

            query=query,

            top_k=top_k,

            metadata_filter={

                "flow": "Income"

            }

        )

    # ======================================================
    # Pretty Print
    # ======================================================

    @staticmethod
    def print_results(results: List[Dict]):

        print()

        for index, result in enumerate(results, start=1):

            print("=" * 60)

            print(f"Result {index}")

            print("=" * 60)

            print("Similarity :", result["score"])

            for key, value in result["metadata"].items():

                print(f"{key}: {value}")

            print()