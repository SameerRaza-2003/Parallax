import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self):
        print("[VectorStore] Initializing embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = 384
        self.index = faiss.IndexFlatL2(self.dim)
        self.texts = []
        print("[VectorStore] Ready.")

    def add(self, text: str):
        print("[VectorStore] Adding text to vector store...")
        embedding = self.model.encode(text)

        if embedding is None or len(embedding) == 0:
            print("[VectorStore] ❌ Empty embedding, skipping")
            return

        embedding = np.array([embedding]).astype("float32")
        self.index.add(embedding)
        self.texts.append(text)

        print(f"[VectorStore] ✅ Vector added. Total vectors: {len(self.texts)}")

    def search(self, query: str, k=1):
        if len(self.texts) == 0:
            print("[VectorStore] ⚠️ Search requested but index is empty")
            return None, 0.0

        query_embedding = self.model.encode(query)
        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, k)
        distance = distances[0][0]
        similarity = 1 / (1 + distance)

        print(f"[VectorStore] 🔎 Search similarity = {similarity}")

        return self.texts[indices[0][0]], similarity
