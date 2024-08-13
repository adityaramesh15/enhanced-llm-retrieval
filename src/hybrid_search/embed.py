from transformers import AutoTokenizer, AutoModel
from pinecone_text.sparse import BM25Encoder
import torch

def initialize():
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    dense_model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    sparse_model = BM25Encoder().default()
    return tokenizer, dense_model, sparse_model

def embed_text(tokenizer, dense_model, sparse_model, text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = dense_model(**inputs)
        dense_embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()

    try:
        sparse_embeddings = sparse_model.encode_documents([text])[0]
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