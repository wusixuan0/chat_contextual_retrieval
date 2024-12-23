# - The core RAG functionality logic (the functions `retrieve_base` and `answer_query_base` from the tutorial)
# - The business logic of how to process queries and generate answers
# - Methods that work with the VectorDB to get results

# Think of it this way:
# - `rag_engine.py` is like a library that defines HOW things should work
# - `main.py` is like a script that actually USES that library

# class RAGEngine:
#     def __init__(self, anthropic_api_key, voyage_api_key):
#         self.client = Anthropic(api_key=anthropic_api_key)
#         self.vector_db = VectorDB(
#             name="in_memory_vector_db",
#             api_key=voyage_api_key
#         )
# Following dependency injection principles:
# - The VectorDB should be initialized outside and passed to RAGEngine
# - The Anthropic client should also be initialized outside and passed to RAGEngine
# ---
# When you initialize a class with __init__, the parameters become instance variables (or instance attributes) through self.vector_db and self.client. These are now available to all methods in your class.

# This concept where the instance variables (self.vector_db, self.client) are available throughout the class methods is called "instance scope" or "instance state". It's one of the key benefits of OOP - you can initialize these dependencies once and use them throughout the class.

class Retriever:
    def __init__(self, vector_db, client=None, model=None):
        self.vector_db = vector_db
        self.client = client
        self.model = model

    def retrieve_base(self, query):
        results = self.vector_db.search(query, k=3)
        context = ""
        for result in results:
            print(result['metadata']['chunk_link'], '\n')
            chunk = result['metadata']
            context += f"\n{chunk['text']}\n"
        return results, context
