from src.chunk.chunk_loader import ChunkLoader
from src.add_context.situate_context import situate_context
from src.util.util import write_json_file, read_text_file
from src.vector_store.vector_db import VectorDB
import logging
from typing import Dict
import traceback
import os
from dotenv import load_dotenv

load_dotenv() # TODO

class ChatProcessor:
    def __init__(self, registry):
        self.registry = registry
        self.chunk_loader = ChunkLoader()
        self.situate_context = situate_context

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def process_all_chats(self):
        unprocessed_chats = self.registry.get_unprocessed_chats()
        self.logger.info(f"Found {len(unprocessed_chats)} unprocessed chats")

        # import pdb; pdb.set_trace()

        for chat in unprocessed_chats:
            try:
                self.logger.info(f"Starting to process chat {chat.get('uuid')}")
                if not isinstance(chat, dict) or 'uuid' not in chat:
                    raise ValueError(f"Invalid chat data structure: {chat}")

                self.process_chat(chat)

            except Exception as e:
                self.logger.error(f"Failed to process chat {chat.get('uuid')}")
                self.logger.error(f"Error details: {str(e)}")
                self.logger.error(f"Chat data: {chat}")
                self.logger.error(f"Traceback: {traceback.format_exc()}")
                continue

    def process_chat(self, chat_data):
        try:
            # 1. Update registry status to "processing"
            self.registry.mark_chat_status(chat_data['uuid'], "processing")

            # 2. Process in sequence with temp files
            chunks = self.chunk_loader.load_chunks(chat_data)
            write_json_file(chunks, f'./data/temp_{chat_data["uuid"]}_chunks.json')
            
            chunk_file_path = f'./data/temp_{chat_data["uuid"]}_enriched.json'

            conversation_flow_summary = self.get_flow_summary(chat_data)
            enriched_chunks = self.situate_context(chunks, conversation_flow_summary, chunk_file_path)

            # 3. Atomic vector db update
            # from src.util.util import load_json_file
            # enriched_chunks = load_json_file("./data/temp_9647c851-7a68-4386-a230-a4a24254b191_enriched.json")

            vector_db = VectorDB(db_path="./data/db/vector_db.pkl", api_key=os.getenv('VOYAGE_API_KEY'))
            vector_db.load_data(enriched_chunks)

            # 4. Mark as complete in registry
            self.registry.mark_chat_status(chat_data['uuid'], "embeded")

            # 5. Clean up temp files
            self.cleanup_temp_files(chat_data['uuid'])

        except Exception as e:
            # If anything fails, mark as failed in registry
            self.registry.mark_chat_status(chat_data['uuid'], "failed")
            self.cleanup_temp_files(chat_data['uuid'])
            print("process_chat", e)
            raise e

    def get_flow_summary(self, chat_data):
        flow_text = self._get_flow_text(chat_data)
        if flow_text is None:
            flow_text = self._generate_flow_summary(chat_data)  # LLM call
        return flow_text

    def _get_flow_text(self, chat_data):
        if 'flow_file_path' in chat_data:
            try:
                return read_text_file(chat_data['flow_file_path'])
            except FileNotFoundError:
                return None
        return None

    def _generate_flow_summary(self, chat_data):
        # TODO: LLM call
        pass

    def cleanup_temp_files(self, uuid):
        pass