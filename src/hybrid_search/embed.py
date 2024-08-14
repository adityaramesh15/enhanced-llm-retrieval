from transformers import AutoTokenizer, AutoModel
from pinecone_text.sparse import BM25Encoder
import torch
from hybrid_search.utils import singleton

@singleton
class Embed:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-mpnet-base-v2")
        self.dense_model = AutoModel.from_pretrained("sentence-transformers/all-mpnet-base-v2")
        self.sparse_model = BM25Encoder().default()

    def embed_text(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.dense_model(**inputs)
            dense_embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()

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

# t, d, s = initialize()
# print(embed_text(t, d, s, "This is a test message"))