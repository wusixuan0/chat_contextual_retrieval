import os
import time
import argparse
from dotenv import load_dotenv
from src.vector_store.vector_db import VectorDB
from src.util.util import write_text_file, read_text_file, write_json_file, load_json_file
from src.add_context.situate_context import situate_context
from src.registry.registry import ChatRegistry

def process_chat(chat_data, registry):
    try:
        # 1. Update registry status to "processing"
        registry.mark_chat_processing(chat_data['uuid'])
        
        # 2. Process in sequence with temp files
        temp_chunks = split_chat(chat_data)
        save_temp_chunks(temp_chunks, f'temp_{chat_data['uuid']}_chunks.json')
        
        flow_text = get_flow_text()  # however you handle flow.txt
        enriched_chunks = add_context(temp_chunks, flow_text)
        save_temp_chunks(enriched_chunks, f'temp_{uuid}_enriched.json')
        
        # 3. Atomic vector db update
        vector_db = VectorDB(db_path="./data/db/vector_db.pkl")
        vector_db.atomic_update(enriched_chunks)
        
        # 4. Mark as complete in registry
        registry.mark_chat_complete(uuid, chunk_count=len(enriched_chunks))
        
        # 5. Clean up temp files
        cleanup_temp_files(uuid)
        
    except Exception as e:
        # If anything fails, mark as failed in registry
        registry.mark_chat_failed(uuid, error=str(e))
        cleanup_temp_files(uuid)
        raise e

def process_all_chats(registry):
    from src.process_chat.process import PreProcessChatText
    preprocessor = PreProcessChatText()
    uuids_to_be_processed = preprocessor.extract_uuids_to_be_processed() # currently using file name, change to check embedded status in registry

    for uuid in uuids_to_be_processed:
        text_file_path = f'data/raw/{uuid}.txt'
        preprocessor.split_chat(file_path=f'./data/raw/{uuid}.txt', uuid=uuid) # chunks automatically saved to "./data/chunks.json", will refactor. i save to json here because the operation used to be separate.
        chunk_path = "./data/chunks.json"
        situate_context(chunk_path, text_file_path) # context saved to "./data/chunks.json"
        vector_db = VectorDB(
            db_path="./data/db/vector_db.pkl",
            api_key=os.getenv('VOYAGE_API_KEY')
        )
        vector_db.load_data(chunk_path=chunk_path)

def main(args):
    registry = ChatRegistry(registry_path="./data/chat_registry.json")

    if args.process_all:
        unprocessed_chats = registry.get_unprocessed_chats()

        for chat in unprocessed_chats:
            process_chat(chat, registry)

    elif args.process:
        # Process specific UUIDs
        uuids = args.process.split(',')  # comma-separated UUIDs
        unprocessed_chats = registry.get_chats(uuids)

        for chat in unprocessed_chats:
            process_chat(chat, registry)

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
    parser.add_argument('--process_all', action='store_true')
    parser.add_argument("--process", type=str, help="Comma-separated list of UUIDs to process.")
    parser.add_argument('--retrieve', action='store_true')
    
    args = parser.parse_args()
    main(args)