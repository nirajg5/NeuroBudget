"""
Prompt Templates

Contains all prompts used by NeuroBudget.
"""


SYSTEM_PROMPT = """
You are NeuroBudget, an AI Financial Copilot.

Your job is to help users understand their financial transactions.

You are given:

1. User Question
2. Retrieved Financial Transactions

Your responsibilities are:

• Answer only using the retrieved transaction context.

• Never make up financial information.

• If the answer is not present in the retrieved transactions,
  clearly say:

"I couldn't find that information in your uploaded financial records."

• Always explain your reasoning.

• Mention merchants, categories, dates and amounts whenever useful.

• Use Indian Rupee (₹) for money.

• Keep answers concise but informative.

• When possible provide:
  - Summary
  - Key observations
  - Recommendations

Never fabricate transactions.
Never assume missing information.
Never hallucinate.
"""

def build_prompt(
    question: str,
    context: str
) -> str:
    """
    Build prompt for the LLM.
    """

    prompt = f"""
{SYSTEM_PROMPT}

==============================
RETRIEVED TRANSACTIONS
==============================

{context}

==============================
USER QUESTION
==============================

{question}

==============================
ANSWER
==============================
"""

    return prompt

def build_context(results):
    """
    Convert retrieved Pinecone results into LLM context.
    """

    if not results:

        return "No relevant transactions found."

    context = []

    for result in results:

        metadata = result["metadata"]

        context.append(

f"""
Merchant : {metadata.get("merchant")}

Category : {metadata.get("category")}

Amount : ₹{metadata.get("amount")}

City : {metadata.get("city")}

Flow : {metadata.get("flow")}

Transaction Size : {metadata.get("transaction_size")}

Month : {metadata.get("month")}

Year : {metadata.get("year")}
"""
        )

    return "\n-----------------------\n".join(context)

class PromptManager:

    @staticmethod
    def get_system_prompt():

        return SYSTEM_PROMPT

    @staticmethod
    def create_prompt(
        question,
        results
    ):

        context = build_context(results)

        return build_prompt(
            question,
            context
        )

