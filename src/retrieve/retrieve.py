# TODO: draft a very simple prompt for
# reconstructe decision/topic progression timeline
# Example
# Topic: Chunking Strategy
# - Initial Design (Chat 1, chunk 3)
# - Implementation Decision (Chat 2, chunk 2)
# - Problem & Revision (Chat 3, chunk 5)

class Retriever:
    def __init__(self, vector_db, client=None, model=None):
        self.vector_db = vector_db
        self.client = client
        self.model = model

    def retrieve_base(self, query, k=3):
        results = self.vector_db.search(query, k)

        context = ""
        for result in results:
            chunk = result['metadata']
            context += f"\n{chunk['content']}\n"
            context += f"\n{chunk['context']}\n"
        return results, context
