"""
Embedding Model

Generates embeddings using BAAI/bge-small-en-v1.5
"""

from typing import List

from sentence_transformers import SentenceTransformer

from core.config import settings
from core.logger import logger


_model = None


class EmbeddingModel:
    """
    Singleton embedding model.
    """

    @staticmethod
    def load_model():

        global _model

        if _model is None:

            logger.info(
                f"Loading embedding model: {settings.EMBEDDING_MODEL}"
            )

            _model = SentenceTransformer(
                settings.EMBEDDING_MODEL
            )

            logger.success(
                "Embedding model loaded successfully."
            )

        return _model

    @staticmethod
    def embed_text(text: str) -> List[float]:

        model = EmbeddingModel.load_model()

        embedding = model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embedding.tolist()

    @staticmethod
    def embed_batch(
        texts: List[str],
        batch_size: int = 64
    ) -> List[List[float]]:

        model = EmbeddingModel.load_model()

        embeddings = model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embeddings.tolist()

    @staticmethod
    def embedding_dimension():

        model = EmbeddingModel.load_model()

        return model.get_sentence_embedding_dimension()

    @staticmethod
    def cosine_similarity(text1: str, text2: str):

        model = EmbeddingModel.load_model()

        embeddings = model.encode(
            [text1, text2],
            batch_size=2,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        similarity = float(
            embeddings[0] @ embeddings[1]
        )

        return round(similarity, 4)