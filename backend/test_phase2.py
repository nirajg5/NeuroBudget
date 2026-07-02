from rag.retriever import Retriever


retriever = Retriever()

results = retriever.search(

    query="How much did I spend on Amazon?",

    top_k=5

)

Retriever.print_results(results)