# For `main.py`, think about what a user of your retrieve context system would need to do:
# - System initialization and configuration
# - The actual execution flow/usage of retrieve context (Load their chat documents, input query and get relevant context)
# - usage example

import os
import json
from dotenv import load_dotenv
from src.retrieve.retrieve import Retriever
from src.vector_store.vector_db import VectorDB
from src.process_chat.process import PreProcessChatText
from src.add_context.situate_context import generate_context_prompt, flow_summary_example
from src.util.llm_call import get_completion

def main():
    load_dotenv()

    # # Initialize the VectorDB
    # vector_db = VectorDB(
    #     name="chats",
    #     api_key=os.getenv('VOYAGE_API_KEY')
    # )

    # # Load vector db
    # vector_db.load_data()

    # retriever = Retriever(vector_db)
    question = "What was the decision I made about human assistant response handling"
    # results, context = retriever.retrieve_base(question)
    # print(results, context)
    # ---

    chunks, formatted_chunks = PreProcessChatText().process_chat(file_name="chat-test.txt")

    with open('data/chunks.json', 'w') as f: json.dump(formatted_chunks, f, indent=2)
    # import pdb; pdb.set_trace()
    return 
    chunk_content = chunks[8]
    # import pdb; pdb.set_trace()

    context_generation_prompt = generate_context_prompt(flow_summary=flow_summary_example, chunk_content=chunk_content)
    print(context_generation_prompt)

    model_name = "gemini"
    response_text = get_completion(content=context_generation_prompt, model_name=model_name)

if __name__ == "__main__":
    main()