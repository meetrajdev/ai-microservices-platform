class VectorStore:

    def add(self, embeddings):
        raise NotImplementedError

    def search(self, query_embedding, k):
        raise NotImplementedError