import os
import time
import argparse
from dotenv import load_dotenv
from src.vector_store.vector_db import VectorDB
from src.util.util import write_json_file
from src.registry.registry import ChatRegistry
from src.processor.processor import ChatProcessor

load_dotenv()
def main(args):
    registry = ChatRegistry(registry_path="./data/chat_registry.json")

    if args.process_all:
        # Process all unprocessed chats
        ChatProcessor(registry).process_all_chats()

    elif args.process:
        # Process specific UUIDs
        uuids = args.process.split(',')  # comma-separated UUIDs
        unprocessed_chats = registry.get_chats(uuids)

        for chat in unprocessed_chats:
            ChatProcessor(registry).process_chat(chat, registry)

    if args.retrieve:
        vector_db = VectorDB(
            db_path="./data/db/vector_db.pkl",
            api_key=os.getenv('VOYAGE_API_KEY')
        )
        vector_db.load_data()

        query = "atomic update?"
        results = vector_db.search(query, 10)
        write_json_file(results, f'data/retrieved.json')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='chat retrieval')
    parser.add_argument('--process_all', action='store_true')
    parser.add_argument("--process", type=str, help="Comma-separated list of UUIDs to process.")
    parser.add_argument('--retrieve', action='store_true')
    
    args = parser.parse_args()
    main(args)