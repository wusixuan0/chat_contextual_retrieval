from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from src.util.util import write_json_file
# from src.add_context.situate_context import situate_context

class PreProcessChatText:
    def __init__(self, name='chats'):
        self.name = name

    def process_chat(self, file_dir, file_name='chat_history.txt'):
        file_path = f"{file_dir}/{file_name}"
        docs = self._load_text_file(file_path)
        doc_chunks = self._split_documents(docs)

        # convert doc to string because VoyageAI takes plain text
        string_chunks = [doc_chunks[i].page_content for i in range(len(doc_chunks))]

        # Format chunk to store in metadata
        formatted_chunks = self._process_chunks(string_chunks)
        write_json_file(data=formatted_chunks, file_path=f"{file_dir}/chunks.json")

        return formatted_chunks

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
                "i": i,
                "content": chunk,
            })
        
        return processed_chunks