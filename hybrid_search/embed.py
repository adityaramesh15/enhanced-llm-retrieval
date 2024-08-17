from sentence_transformers import SentenceTransformer
from pinecone_text.sparse import BM25Encoder
from hybrid_search.utils import singleton

@singleton
class Embed:
    def __init__(self):
        self.dense_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        self.sparse_model = BM25Encoder().default()

    def embed_text(self, text):
        dense_embeddings = self.dense_model.encode(text, convert_to_tensor=True)
        
        try:
            sparse_embeddings = self.sparse_model.encode_documents([text])[0]
            if not sparse_embeddings['indices']:
                raise ValueError("Empty or invalid sparse vector")
        except Exception:
            sparse_embeddings = {
                "indices": [0], 
                "values": [1e-9]  
            }

        return dense_embeddings.tolist(), sparse_embeddings

# Example usage:
# embedder = Embed()
# print(embedder.embed_text("This is a test message"))
