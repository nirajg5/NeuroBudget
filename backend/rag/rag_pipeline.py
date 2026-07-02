"""
Complete RAG Pipeline
"""

from openai import OpenAI

from core.config import settings
from core.logger import logger

from rag.retriever import Retriever
from rag.prompt import PromptManager


class RAGPipeline:

    def __init__(self):

        self.retriever = Retriever()

        self.client = OpenAI(

            api_key=settings.OPENROUTER_API_KEY,

            base_url="https://openrouter.ai/api/v1"

        )

    # =====================================================
    # Retrieve Context
    # =====================================================

    def retrieve(

        self,

        question: str,

        top_k: int = 5

    ):

        return self.retriever.search(

            query=question,

            top_k=top_k

        )

    # =====================================================
    # Build Prompt
    # =====================================================

    def create_prompt(

        self,

        question,

        retrieved_results

    ):

        return PromptManager.create_prompt(

            question,

            retrieved_results

        )

    # =====================================================
    # Call OpenRouter
    # =====================================================

    def generate_answer(

        self,

        prompt: str

    ):

        response = self.client.chat.completions.create(

            model=settings.OPENROUTER_MODEL,

            messages=[

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            temperature=0.2,

            max_tokens=800

        )

        return response.choices[0].message.content

    # =====================================================
    # Complete Pipeline
    # =====================================================

    def ask(

        self,

        question: str,

        top_k: int = 5

    ):

        logger.info("Running RAG Pipeline...")

        results = self.retrieve(

            question,

            top_k

        )

        prompt = self.create_prompt(

            question,

            results

        )

        answer = self.generate_answer(

            prompt

        )

        return {

            "question": question,

            "answer": answer,

            "retrieved_documents": len(results),

            "sources": results

        }