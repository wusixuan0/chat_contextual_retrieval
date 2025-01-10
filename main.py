import os
import time
import argparse
from dotenv import load_dotenv
from src.vector_store.vector_db import VectorDB
from src.util.util import write_json_file
from src.registry.registry import ChatRegistry
from src.processor.processor import ChatProcessor

load_dotenv()

def main():
    registry = ChatRegistry(registry_path="./data/chat_registry.json")

    parser = argparse.ArgumentParser(description='Claude Conversation Context Retrieval System')
    subparsers = parser.add_subparsers(dest='command')

    # Add new chat
    add = subparsers.add_parser('add', 
        help='Add a new conversation to the system',
        description="""
        Add a new conversation export file to the system. The URL must be a Claude chat URL 
        containing a UUID (e.g., https://claude.ai/chat/<uuid>). The conversation flow 
        summary is optional but helps provide better context for retrieval.
        """)
    add.add_argument('--chat_path', 
                required=True,
                help='Path to chat conversation export file')
    add.add_argument('--url',
        required=True,
        help='Claude conversation URL (must contain UUID)')
    add.add_argument('--title',
        help='Optional descriptive title for the conversation')
    add.add_argument('--flow_path',
        help='Optional path to conversation flow summary file (.txt)')

    # Search
    search = subparsers.add_parser('search', help='Search through chats')
    search.add_argument('query', help='Search query')
    # search.add_argument('--mode', choices=['semantic', 'topic'], 
    #                    default='semantic',
    #                    help='Search mode: semantic for questions, topic for exploration')

    inspect_db = subparsers.add_parser('db', help='Inspect the vector database content')

    args = parser.parse_args()

    if args.command == 'add':
        ChatProcessor(registry).process_file(
            chat_path=args.chat_path,
            url=args.url,
            title=args.title,
            flow_path=args.flow_path
        )

    elif args.command == 'search':
        query = args.query

        vector_db = VectorDB(
            db_path="./data/db/vector_db.pkl",
        )
        vector_db.load_db()

        results = vector_db.search(query, 10)
        write_json_file(results, f'data/retrieved.json')

    elif args.command == 'db':
        vector_db = VectorDB(
            db_path="./data/db/vector_db.pkl",
        )

        file_path = f"./data/db_content/db_{time.time()}.json"

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        vector_db.inspect_db(file_path)

if __name__ == "__main__":
    main()