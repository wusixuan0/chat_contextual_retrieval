from src.chunk.chunk_loader import ChunkLoader
from src.add_context.situate_context import situate_context
from src.util.util import write_json_file, read_text_file
from src.vector_store.vector_db import VectorDB
import logging
from typing import Dict
import traceback
import os
import re

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


    def process_file(self, chat_path, url, title=None, flow_path=None):
        """Process a single chat file."""
        try:
            # Extract and validate UUID from URL
            uuid = url.split('/')[-1]
            
            if not uuid or not self.validate_uuid(uuid):
                raise ValueError(f"Invalid Claude chat URL: {url}")

            # Validate input files
            if not os.path.exists(chat_path):
                raise FileNotFoundError(f"Chat file not found: {chat_path}")
            if not chat_path.endswith('.txt'):
                raise ValueError("Chat file must be a .txt file")
            if flow_path and not os.path.exists(flow_path):
                raise FileNotFoundError(f"Flow file not found: {flow_path}")

            # 1. Copy file to raw directory
            dest_path = f"./data/raw/{uuid}.txt"
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            import shutil
            shutil.copy2(chat_path, dest_path)

            # 2. Add to registry
            self.registry.add_chat(
                url=url,
                chat_file_path=dest_path,
                uuid=uuid,
                title=title,
                flow_file_path=flow_path
            )

            # 3. Process chunks
            chat_data = self.registry.get_chat(uuid)

            # Create temp directory
            os.makedirs('./data/temp', exist_ok=True)

            # Process chunks
            self.logger.info("Processing chat chunks...")
            chunks = self.chunk_loader.load_chunks(chat_data)
            write_json_file(chunks, f'./data/temp/temp_{uuid}_chunks.json')
            
            # 4. Add context if flow provided
            chunks_to_embed = chunks

            if flow_path:
                self.logger.info("Adding context from flow summary...")
                conversation_flow_summary = self.get_flow_summary(chat_data)
                enriched_chunks_path = f'./data/temp/temp_{uuid}_enriched.json'
                chunks_to_embed = self.situate_context(chunks, conversation_flow_summary, enriched_chunks_path)

            # 5. Update vector db
            self.logger.info("Updating vector database...")
            vector_db = VectorDB(
                db_path="./data/db/vector_db.pkl", 
                api_key=os.getenv('VOYAGE_API_KEY')
            )
            vector_db.load_data(chunks_to_embed)

            # 6. Mark as complete and cleanup
            self.registry.mark_chat_status(uuid, "embedded")
            self.cleanup_temp_files(uuid)
            
            self.logger.info(f"Successfully processed chat {uuid}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to process file: {str(e)}")
            self.logger.error(traceback.format_exc())
            if uuid:
                self.registry.mark_chat_status(uuid, "failed")
                self.cleanup_temp_files(uuid)
            raise e

    def get_flow_summary(self, chat_data):
        flow_text = self._get_flow_text(chat_data.flow_file_path)
        if flow_text is None:
            flow_text = self._generate_flow_summary(chat_data)  # LLM call
        return flow_text

    def _get_flow_text(self, flow_file_path):
        try:
            return read_text_file(flow_file_path)
        except FileNotFoundError:
            return None

    def cleanup_temp_files(self, uuid):
        """Remove temporary files created during processing."""
        temp_files = [
            f'./data/temp/temp_{uuid}_chunks.json',
            # f'./data/temp/temp_{uuid}_enriched.json'
        ]
        for file_path in temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                self.logger.warning(f"Failed to remove temp file {file_path}: {e}")

    def validate_uuid(self, uuid):
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

        return re.match(uuid_pattern, uuid)

    def validate_path(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

    def validate_folder(self, path):
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Path is not a directory: {folder_path}")

    def _generate_flow_summary(self, chat_data):
        # TODO: LLM call
        pass
