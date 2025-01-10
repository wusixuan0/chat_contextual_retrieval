import os
import pickle
import json
import numpy as np
import voyageai
from src.util.util import write_json_file

class VectorDB:
    def __init__(self, db_path="./data/db/vector_db.pkl", api_key=None):
        if api_key is None:
            api_key = os.getenv("VOYAGE_API_KEY")
        self.client = voyageai.Client(api_key=api_key)
        self.embeddings = []
        self.metadata = []
        self.query_cache = {}
        self.db_path = db_path

    def load_data(self, chunks=None):
        if os.path.exists(self.db_path):
            print("Loading vector database from disk.")
            self.load_db()

        if not chunks: return
        print("Embedding new chunks.")

        new_texts = []
        for chunk in chunks:
            if chunk.get('context'):
                new_texts.append(f"{chunk['content']}\n\n{chunk['context']}")
            else:
                new_texts.append(chunk['content'])
        
        # Embed new chunks
        new_embeddings = self._create_embeddings(new_texts)
        
        # Append new data
        self.embeddings.extend(new_embeddings)
        self.metadata.extend(chunks)

        self.save_db()
        print(f"Vector database updated and saved to {self.db_path}")

    def _create_embeddings(self, texts):
        batch_size = 128
        result = [
            self.client.embed(
                texts[i : i + batch_size],
                model="voyage-2"
            ).embeddings
            for i in range(0, len(texts), batch_size)
        ]
        return [embedding for batch in result for embedding in batch]

    def search(self, query, k=5, similarity_threshold=0.75):
        if query in self.query_cache:
            query_embedding = self.query_cache[query]
        else:
            query_embedding = self.client.embed([query], model="voyage-2").embeddings[0]
            self.query_cache[query] = query_embedding

        if not self.embeddings:
            raise ValueError("No data loaded in the vector database.")

        similarities = np.dot(self.embeddings, query_embedding)
        top_indices = np.argsort(similarities)[::-1]
        top_examples = []
        
        for idx in top_indices:
            if similarities[idx] >= similarity_threshold:
                example = {
                    "metadata": self.metadata[idx],
                    "similarity": similarities[idx],
                }
                top_examples.append(example)
                
                if len(top_examples) >= k:
                    break

        # If not enough examples found, add top 3
        if not top_examples:
            for idx in top_indices[:3]:
                example = {
                    "metadata": self.metadata[idx],
                    "similarity": similarities[idx],
                }
                top_examples.append(example)

        self.save_db()
        return top_examples

    def save_db(self):
        data = {
            "embeddings": self.embeddings,
            "metadata": self.metadata,
            "query_cache": json.dumps(self.query_cache),
        }
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, "wb") as file:
            pickle.dump(data, file)

    def load_db(self):
        if not os.path.exists(self.db_path):
            raise ValueError("Vector database file not found. Use load_data to create a new database.")
        with open(self.db_path, "rb") as file:
            data = pickle.load(file)
        self.embeddings = data["embeddings"]
        self.metadata = data["metadata"]
        self.query_cache = json.loads(data["query_cache"])

    def inspect_db(self, file_path):
        self.load_db()
        write_json_file({
            "chunks": self.metadata,
            "query_cache": self.query_cache
        }, file_path)
