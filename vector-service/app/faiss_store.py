import faiss
import numpy as np

class FAISSStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatIP(dimension)
        self.documents = []

    def add(self, embeddings, docs):
        self.index.add(np.array(embeddings).astype("float32"))
        self.documents.extend(docs)

    def search(self, query_embedding, k=2):
        D, I = self.index.search(
            np.array([query_embedding]).astype("float32"), k
        )
        return [self.documents[i] for i in I[0]]