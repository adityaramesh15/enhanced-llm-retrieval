from transformers import AutoTokenizer, AutoModel
import torch


def embed_text(text):
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    inputs = tokenizer(text, return_tensors="pt", truncation = True, padding= True)

    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
    

    vector = embeddings.numpy().tolist()
    return vector
