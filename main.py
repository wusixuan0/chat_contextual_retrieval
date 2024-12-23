# For `main.py`, think about what a user of your retrieve context system would need to do:
# - System initialization and configuration
# - The actual execution flow/usage of retrieve context (Load their chat documents, input query and get relevant context)
# - usage example

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from src.retrieve.retrieve import Retriever
from src.vector_store.vector_db import VectorDB

def main():
    load_dotenv()

    # Initialize the VectorDB
    vector_db = VectorDB(
        name="chats",
        api_key=os.getenv('VOYAGE_API_KEY')
    )


    # Load vector db
    vector_db.load_data()

    retriever = Retriever(vector_db)
    question = "How do I design rag for the use case of searching in chat history?"
    results, context = retriever.retrieve_base(question)
    print(results, context)


if __name__ == "__main__":
    main()