# For `main.py`, think about what a user of your retrieve context system would need to do:
# - System initialization and configuration
# - The actual execution flow/usage of retrieve context (Load their chat documents, input query and get relevant context)
# - usage example

import os
from dotenv import load_dotenv
from src.vector_store.vector_db import VectorDB
from src.util.util import write_text_file, read_text_file, write_json_file, load_json_file
import time
import argparse
from src.add_context.situate_context import situate_context


def main(args):
    # if args.test_util:
    #     import sys
    #     sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #     from util.llm_call import get_llm

    if args.message_array_to_text:
        from data.chats.chat_prompt_gemini.messages_array import history
        chat_history = ''.join([part for message in history for part in message['parts']])
        write_text_file(chat_history, 'data/chats/chat_prompt_gemini/chat_history.txt')

    if args.chunk_text:
        text_file_path = 'data/chats/chat_prompt_gemini/chat_history.txt'
        chat_history = read_text_file(text_file_path)

        from src.process_chat.process import PreProcessChatText
        preprocessor = PreProcessChatText()
        formatted_chunks = preprocessor.process_chat(file_dir='data/chats/chat_prompt_gemini', file_name='chat_history.txt') # formatted_chunks saved to f"{file_dir}/chunks.json"

    if args.add_context:
        chunk_file_path = 'data/chats/chat_prompt_gemini/chunks.json'
        text_file_path = 'data/chats/chat_prompt_gemini/flow.txt'
        situate_context(chunk_file_path, text_file_path)

    if args.embed:
        load_dotenv()
        directory = "./data/chats/chat_prompt_gemini"

        # Initialize the VectorDB
        vector_db = VectorDB(
            db_path=f"{directory}vector_db.pkl",
            api_key=os.getenv('VOYAGE_API_KEY')
        )

        # Load existing or create new vector db
        vector_db.load_data(chunk_path=f"{directory}/chunks.json")

    if args.retrieve:
        vector_db = VectorDB(
            db_path="./data/db/vector_db.pkl",
            api_key=os.getenv('VOYAGE_API_KEY')
        )
        vector_db.load_data()

        query = "What was the decision made about human assistant response handling in chunking strategy?"
        results = vector_db.search(query, 10)
        write_json_file(results, f'data/chats/chat_plan_version/_retrieved_{time.time()}.json')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='chat retrieval')
    parser.add_argument('--message_array_to_text', action='store_true')
    parser.add_argument('--chunk_text', action='store_true')
    parser.add_argument('--add_context', action='store_true')
    parser.add_argument('--embed', action='store_true')
    parser.add_argument('--retrieve', action='store_true')
    
    args = parser.parse_args()
    main(args)