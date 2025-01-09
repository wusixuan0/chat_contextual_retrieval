from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from src.util.util import write_json_file, load_json_file
from typing import Set, Dict
import os
import re

class ChunkLoader:
    def load_chunks(self, chat_data):
        docs = self._load_text_file(chat_data.chat_file_path)
        doc_chunks = self._split_documents(docs)

        chunks = [
            {
                "content": doc_chunks[i].page_content,
                "metadata": {
                    "i": i,
                    # url and title are for identification during manual inspection
                    "url": chat_data.url,
                    **({"title": chat_data.title} if chat_data.title is not None else {})
                },
            } for i in range(len(doc_chunks))
        ]

        return chunks

    def _load_text_file(self, file_path):
        loader = TextLoader(file_path, encoding='utf-8')
        return loader.load()

    def _split_documents(self, documents, chunk_size=1000, chunk_overlap=0):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_documents(documents)

    # def extract_uuids_to_be_processed(self):
    #     uuids_raw = self.extract_uuids_from_files()
    #     uuids_embedded = self.extract_embedded_chat_uuids()
    #     return uuids_raw - uuids_embedded

    # def extract_uuids_from_files(self, folder_path: str="./data/raw") -> Set[str]:
    #     """
    #     Extract UUIDs from text files in a given folder where filenames are UUIDs.
        
    #     Args:
    #         folder_path (str): Path to the folder containing text files
            
    #     Returns:
    #         Set[str]: Set of UUIDs found in filenames
            
    #     Raises:
    #         FileNotFoundError: If the folder path doesn't exist
    #     """
    #     # UUID pattern (8-4-4-4-12 format)
    #     uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.txt$'
        
    #     # Check if folder exists
    #     if not os.path.exists(folder_path):
    #         raise FileNotFoundError(f"Folder not found: {folder_path}")
        
    #     uuids = set()
        
    #     # Iterate through files in the folder
    #     for filename in os.listdir(folder_path):
    #         # Check if file matches UUID pattern
    #         if re.match(uuid_pattern, filename.lower()):
    #             # Extract UUID by removing .txt extension
    #             uuid = filename[:-4]  # Remove '.txt'
    #             uuids.add(uuid)
        
    #     return uuids

    # def extract_embedded_chat_uuids(self) -> Set[str]:
    #     """
    #     Extract all UUIDs from the embedded_chats array from manifest.json
        
    #     Returns:
    #         Set[str]: Set of UUID strings
        
    #     Example:
    #         data = {
    #             "last_updated": "2024-12-26",
    #             "embedded_chats": [
    #                 {"uuid": "4e5db666-5634-40db-b07e-4c59464c7dad"},
    #                 {"uuid": "another-uuid-here"}
    #             ]
    #         }
    #         uuids = extract_embedded_chat_uuids(data)
    #         # Returns: {'4e5db666-5634-40db-b07e-4c59464c7dad', 'another-uuid-here'}
    #     """
    #     data = load_json_file("./data/db/manifest.json")
    #     return {chat["uuid"] for chat in data.get("embedded_chats", [])}