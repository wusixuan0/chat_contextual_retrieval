from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
import pathlib
import json
class PreProcessChatText:
    def __init__(self, name='chats'):
        self.name = name

    def save_json(self, data, file_name, indent=2): # TODO move to util
        folder = self.name
        # os.makedirs(folder, exist_ok=True)
        # file_path = os.path.join(folder, file_name)
        PATH = pathlib.Path().resolve()
        file_path = PATH / 'data' / folder / file_name
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent)
        print(f"Saved {file_name} to {folder}")
    # def process_chat(self, chat_content: str, chat_title: str, chat_link: str):

    def process_chat(self, file_name='claude_chat_context_retrieval.txt'):
        file_path = f'./data/{self.name}/{file_name}'
        chat_content = self._load_text_file(file_path)
        doc_chunks = self._split_documents(chat_content)

        string_chunks = [doc_chunks[i].page_content for i in range(len(doc_chunks))]

        # all_chunks = []
        # for chat in chats_data:
        #     chunks = self.process_chat(chat["content"], chat["title"], chat["link"])
        #     all_chunks.extend(chunks)

        # texts = [chunk["text"] for chunk in all_chunks]
        # Format chunk to store in metadata
        formatted_chunks = self._process_chunks(string_chunks)
        return string_chunks, formatted_chunks

    def _load_text_file(self, file_path):
        loader = TextLoader(file_path, encoding='utf-8')
        return loader.load()

    def _split_documents(self, documents, chunk_size=1000, chunk_overlap=0):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_documents(documents)

    def _process_chunks(self, chunks):
        """
        TODO: chat_dict: list of dicts with format:
        {
            "original_content": "full chat content",
            "title": "chat title",
            "link": "link to chat"
        }
        """
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            processed_chunks.append({
                "original_content": chunk,
            })
        
        return processed_chunks