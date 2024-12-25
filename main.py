# For `main.py`, think about what a user of your retrieve context system would need to do:
# - System initialization and configuration
# - The actual execution flow/usage of retrieve context (Load their chat documents, input query and get relevant context)
# - usage example

import os
from dotenv import load_dotenv
from src.retrieve.retrieve import Retriever
from src.vector_store.vector_db import VectorDB
from src.process_chat.process import PreProcessChatText
from src.add_context.situate_context import generate_context_prompt
from src.util.llm_call import get_llm
from src.util.util import read_text_file, write_json_file, load_json_file

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
    # question = "What was the decision I made about human assistant response handling"
    # results, context = retriever.retrieve_base(question)
    # print(results, context)

    # Split chat history text into chunks
    # raw_chat_file = "./data/chats/chat_plan_version/plan-test-version-flow-context-generate.txt"
    # chunks, formatted_chunks = PreProcessChatText().process_chat(file_path=raw_chat_file)
    chunk_file_path = 'data/chats/chat_plan_version/chunks.json'
    # write_json_file(formatted_chunks, chunk_file_path)

    formatted_chunks = load_json_file(chunk_file_path)
    text_file = 'data/chats/chat_plan_version/flow.txt'
    conversation_flow_summary = read_text_file(text_file)
    num_chunks = len(formatted_chunks)


    for i in range(num_chunks):
        chunk = formatted_chunks[i]

        if "context" in chunk: continue

        context_generation_prompt = generate_context_prompt(
            flow_summary=conversation_flow_summary,
            chunk_content=chunk["content"],
            index=chunk["i"],
            num_chunks=num_chunks,
        )
        try:
            print(i)
            response_text = get_llm(content=context_generation_prompt)
            chunk["context"] = response_text
        except Exception as e:
            print(f"Error occurred at chunk {i}: {str(e)}")
            write_json_file(formatted_chunks, chunk_file_path)
            raise
    write_json_file(formatted_chunks, chunk_file_path)

if __name__ == "__main__":
    main()